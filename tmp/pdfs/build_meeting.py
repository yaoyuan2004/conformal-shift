from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'output/pdf/office_hours_design_discussion.pdf'
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleX', fontName='Helvetica-Bold', fontSize=23, leading=28, textColor=colors.HexColor('#17354A'), spaceAfter=12))
styles.add(ParagraphStyle(name='Deck', fontSize=11, leading=15, textColor=colors.HexColor('#4B606D'), spaceAfter=10))
styles.add(ParagraphStyle(name='H', fontName='Helvetica-Bold', fontSize=12, leading=15, textColor=colors.HexColor('#146B70'), spaceBefore=10, spaceAfter=5))
styles.add(ParagraphStyle(name='B', fontSize=10, leading=14, spaceAfter=7))
styles.add(ParagraphStyle(name='S', fontSize=8.5, leading=12, textColor=colors.HexColor('#52616B'), spaceAfter=6))
styles.add(ParagraphStyle(name='Cell', fontSize=9.5, leading=13))
styles.add(ParagraphStyle(name='CH', fontName='Helvetica-Bold', fontSize=9.5, leading=13, textColor=colors.white))
story=[]
def p(t, s='B'): story.append(Paragraph(t,styles[s]))
def table(rows,widths):
    data=[[Paragraph(v,styles['CH' if i==0 else 'Cell']) for v in r] for i,r in enumerate(rows)]
    t=Table(data,colWidths=widths,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#17354A')),('BACKGROUND',(0,1),(-1,-1),colors.HexColor('#F1F5F7')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,-1),0.6,colors.white)]))
    story.append(t)

p('OFFICE HOURS  /  OCTOBER 13, 2026','S')
p('Beyond image corruption','TitleX')
p('Design update: adding label shift to the conformal prediction study','Deck')
p('<b>Purpose of this discussion.</b> Following the previous proposal meeting, the design now distinguishes two shift mechanisms. I would appreciate feedback on the label-shift setup and the scope of the comparison before settling the analysis and interpretation.')
p('1  How the feedback changed the question','H')
p('The original focus was image corruption. The feedback that distribution shift has more than one form motivated a separate label-shift component: can aggregate coverage change even when the images within each class, the model, and the prediction sets remain fixed?')
table([
['Experiment','What changes?','What stays fixed?'],
['Image corruption','Image appearance: Gaussian noise, defocus blur, or brightness.','Class labels and evaluation identities; clean-calibrated thresholds.'],
['Label shift','The proportions of the ten classes in the evaluation population.','Within-class image distributions; per-image predictions and sets.'],
],[110,202,192])
p('Image corruption is an operational input perturbation here. Preserving class labels does not, by itself, establish the formal covariate-shift assumption that P(Y | X) is unchanged.','S')
p('2  Shared setup for a controlled comparison','H')
p('<b>Data and calibration:</b> CIFAR-10; 5,000 clean calibration images and 5,000 disjoint evaluation images per split. Corruption evaluation uses only the corresponding evaluation-image indices. Target marginal coverage: 90%; thresholds remain fixed under shift.')
p('<b>Comparison under consideration:</b> LAC as the simplest starting point, with APS and RAPS for score sensitivity; standard and AugMix ResNet-18 for the role of robustness-oriented training. Corruption severities are 1, 3, and 5. The two shift mechanisms are evaluated separately.')
p('<b>Readouts:</b> coverage together with average set size, supplemented by empty-set rate and class-conditional coverage. Three overlapping calibration/evaluation splits describe split sensitivity, not independent replications.')
p('Feedback requested','H')
p('Does this separation of mechanisms capture the intended extension of the proposal? Is the two-model, three-score comparison appropriate, or should the main analysis focus on fewer comparisons?')
story.append(PageBreak())
p('DISCUSSION NOTE  /  LABEL-SHIFT DESIGN','S')
p('Changing the class mix','TitleX')
p('A controlled way to separate population composition from image quality','Deck')
p('3  A concrete label-shift construction','H')
p('Use the clean evaluation images to estimate coverage within each class. Reweight those class-level estimates under a specified target class distribution. No additional model inference or recalibration is required for this component.')
table([
['Target prior','Each emphasized class','Each other class','Total for the pair'],
['Balanced','10%','10%','20%'],
['Mild','15%','8.75%','30%'],
['Moderate','20%','7.5%','40%'],
['Severe','30%','5%','60%'],
],[95,146,133,130])
p('Current contrasting pairs: cat/dog and airplane/automobile. These are illustrative cases, not an exhaustive evaluation of possible majority classes.','S')
p('<b>Coverage under a target prior:</b> C(q) = sum over classes y of q(y) c(y), where q(y) is the target class probability and c(y) is coverage conditional on class y.')
p('This makes the mechanism interpretable: placing more weight on classes with lower coverage decreases marginal coverage; emphasizing higher-coverage classes can increase it. A stronger shift therefore need not always make coverage worse.')
p('4  Decisions I would value your guidance on','H')
p('<b>Class selection.</b> The revised proposal mentions rotating majority classes. Would it be better to retain two interpretable pairs, or evaluate all 45 unordered class pairs to reduce dependence on the chosen examples? If expanded, should results show the range as well as the average?')
p('<b>Scope.</b> Is a controlled stress test of fixed, clean-calibrated predictors sufficient, or would one shift-aware calibration baseline add enough value to justify the additional scope?')
p('<b>Interpretation.</b> Is class-conditional coverage the right main explanation for label-shift sensitivity, with set size and empty-set rate as supporting diagnostics?')
p('After this discussion','H')
p('Use the feedback to settle the class-pair strategy, prioritize the model/score comparisons, and decide whether an adjustment method belongs in scope. Then organize the evidence around those decisions.')
p('Boundary of the design: label-shift estimates assume unchanged P(X | Y) and are based on finite clean evaluation samples. Reweighting evaluation metrics measures sensitivity; it does not itself correct the conformal procedure.','S')
p('Basis: revised_conformal_proposal.pdf; notebooks/04_label_shift_experiments.ipynb; results/label_shift_target_priors.csv. This note focuses on design choices; numerical performance comparisons are reserved for follow-up discussion.','S')

def footer(c,doc):
    c.setStrokeColor(colors.HexColor('#D5DFE5')); c.line(54,44,558,44)
    c.setFont('Helvetica',8); c.setFillColor(colors.HexColor('#52616B'))
    c.drawString(54,30,'Conformal coverage under distribution shift | Design discussion')
    c.drawRightString(558,30,str(doc.page))
doc=SimpleDocTemplate(str(OUT),pagesize=(612,792),rightMargin=54,leftMargin=54,topMargin=42,bottomMargin=56,title='Beyond image corruption: office-hours design discussion',author='')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
