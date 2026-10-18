from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color, white
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
import random

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'output/pdf/office_hours_visual_discussion.pdf'
W,H=900,640
c=canvas.Canvas(str(OUT),pagesize=(W,H))
c.setTitle('Two ways a test population can change | Visual design discussion')
NAVY='#19394B'; TEAL='#087F8C'; ORANGE='#D98034'; GRAY='#60717C'; LIGHT='#F0F5F7'; BLUE='#4B78A3'
def text(x,y,s,size=12,color=NAVY,bold=False):
    c.setFillColor(HexColor(color)); c.setFont('Helvetica-Bold' if bold else 'Helvetica',size); c.drawString(x,y,s)
def para(x,y,s,w,size=12,color=NAVY):
    p=Paragraph(s,ParagraphStyle('p',fontName='Helvetica',fontSize=size,leading=size*1.4,textColor=HexColor(color)))
    _,h=p.wrap(w,500);p.drawOn(c,x,y-h);return h
def box(x,y,w,h,fill=LIGHT,stroke=None):
    c.setFillColor(HexColor(fill)); c.setStrokeColor(HexColor(stroke or fill));c.roundRect(x,y,w,h,min(10,h/2,w/2),fill=1,stroke=bool(stroke))
def line(x1,y1,x2,y2,color=GRAY,width=1):
    c.setStrokeColor(HexColor(color));c.setLineWidth(width);c.line(x1,y1,x2,y2)
def arrow(x1,y,x2,color=TEAL):
    line(x1,y,x2,y,color,2);line(x2-7,y+4,x2,y,color,2);line(x2-7,y-4,x2,y,color,2)
def head(n,title,sub):
    text(40,608,'OFFICE HOURS  /  DESIGN DISCUSSION',10,TEAL,True)
    text(40,567,title,27,NAVY,True);text(40,540,sub,12,GRAY)
    line(40,35,860,35,'#D6E0E5');text(40,19,'Conformal coverage under distribution shift  |  October 13, 2026',9,GRAY);text(839,19,f'{n}/3',9,GRAY)
def band(y,label,s):
    box(40,y,820,61,'#EAF4F3');text(55,y+39,label,10,TEAL,True);para(55,y+30,s,790,12)
def tile(x,y,noisy=False):
    rng=random.Random(17)
    for j in range(8):
        for i in range(8):
            val=.83 if (i+j)%2 else .9
            if (2<=i<=5 and 1<=j<=5) or (i in [2,5] and j==6):val=.25
            if noisy: val=max(0,min(1,val+rng.uniform(-.4,.4)))
            c.setFillColor(Color(val*.8,val*.9,val));c.rect(x+i*9,y+j*9,9,9,fill=1,stroke=0)
def stacked(x,y,width,weights):
    colors=[TEAL,ORANGE]+['#BCCAD3']*8
    for v,col in zip(weights,colors):
        c.setFillColor(HexColor(col));c.rect(x,y,width*v,30,fill=1,stroke=0)
        c.setStrokeColor(white);c.setLineWidth(.8);c.rect(x,y,width*v,30,fill=0,stroke=1);x+=width*v

head(1,'Two ways a test population can change','Following the proposal feedback: broaden the mechanism, not just the list of corruptions.')
box(40,188,395,325);box(455,188,405,325)
text(60,484,'01  IMAGE CORRUPTION',14,TEAL,True)
text(60,459,'Change how an image looks.',17,NAVY,True)
tile(94,333);arrow(190,370,280);tile(310,333,True)
text(102,311,'Clean',11);text(301,311,'Corrupted',11)
text(60,282,'Same semantic label; altered pixels.',12,NAVY,True)
para(60,261,'Noise, blur, brightness.<br/>The class mix is held fixed; prediction sets may change because the inputs change.',350,12)
text(475,484,'02  LABEL SHIFT',14,TEAL,True)
text(475,459,'Change which classes appear more.',17,NAVY,True)
text(480,424,'Balanced',11,GRAY);stacked(480,384,350,[.1]*10)
text(480,355,'Cat/dog-heavy example',11,GRAY);stacked(480,315,350,[.3,.3]+[.05]*8)
for x,col,label in [(480,TEAL,'Cat'),(555,ORANGE,'Dog'),(635,'#BCCAD3','Other eight classes')]:
    box(x,288,10,10,col);text(x+16,288,label,10)
para(475,269,'Same within-class images and per-image sets.<br/>Only their contribution to the population changes.',360,12)
band(103,'DESIGN QUESTION','Does adding class-composition shift provide a useful contrast to image corruption?')
text(40,76,'Illustrations show the design, not measured results. Pixel tiles are schematic, not CIFAR-10 examples.',10,GRAY)
text(40,59,'Label-preserving corruption does not by itself establish the formal assumption that P(Y | X) is unchanged.',9,GRAY)
c.showPage()

head(2,'How label-shift evaluation works','Calibrate once on clean data. Keep the predictor fixed. Reweight the evaluation summaries.')
box(40,405,820,105,'#EAF4F3')
text(58,484,'CALIBRATION BRANCH',10,TEAL,True)
box(58,425,202,43,'#FFFFFF');text(70,442,'5,000 clean calibration images',11)
arrow(272,446,318);box(331,425,214,43,'#FFFFFF');text(346,442,'Choose threshold for 90% target',11)
arrow(558,446,606);box(619,425,220,43,'#FFFFFF');text(633,442,'Freeze model + threshold',12,TEAL,True)
text(40,374,'EVALUATION BRANCH  /  A SEPARATE SET OF 5,000 CLEAN IMAGES',10,TEAL,True)
items=[(40,'1','Build prediction sets','For each evaluation image,<br/>record its fixed set C(x).'),(321,'2','Summarize each class','Estimate coverage and set<br/>size within each true class.'),(602,'3','Change class weights','Combine class summaries<br/>using a chosen target prior.')]
for x,num,title,desc in items:
    box(x,212,258,140)
    box(x+14,310,24,24,TEAL);text(x+22,317,num,12,'#FFFFFF',True)
    text(x+14,287,title,15,NAVY,True);para(x+14,271,desc,230,11)
arrow(301,282,315);arrow(582,282,596)
text(57,228,'True cat, set {cat, dog}: covered',10,TEAL)
text(338,228,'c(cat) = covered cats / all cats',10,TEAL)
text(619,228,'Coverage = sum over y of q(y) c(y)',9,TEAL)
box(40,130,820,62,'#FFF3E8');text(55,170,'WHAT IS FIXED?',10,ORANGE,True)
text(55,148,'Images within each class, model outputs, prediction sets, and calibration thresholds.',12)
band(54,'WHAT THIS EVALUATES','Sensitivity to class composition. Reweighting these metrics does not repair the prediction sets.')
c.showPage()

head(3,'Why the class mix matters','ILLUSTRATIVE NUMBERS ONLY  /  This page contains no fitted-model results.')
box(40,330,285,181)
text(55,485,'Assume fixed class coverages',14,NAVY,True)
for y,label,value,color in [(444,'Cat',.80,TEAL),(400,'Dog',.84,ORANGE),(356,'Each other class',.94,BLUE)]:
    text(55,y+11,label,10);c.setFillColor(HexColor('#DCE5EA'));c.rect(55,y-8,220,10,fill=1,stroke=0)
    c.setFillColor(HexColor(color));c.rect(55,y-8,220*value,10,fill=1,stroke=0);text(279,y-7,f'{value:.0%}',10,color,True)
box(342,330,518,181)
text(358,485,'Only change the population weights',14,NAVY,True)
for y,label,weights,result,formula in [(430,'Balanced',[.1]*10,'91.6%','10% x 80% + 10% x 84% + 80% x 94%'),(360,'Cat/dog-heavy',[.3,.3]+[.05]*8,'86.8%','30% x 80% + 30% x 84% + 40% x 94%')]:
    text(358,y+32,label,11,NAVY,True);stacked(358,y-5,285,weights);arrow(657,y+10,693);text(710,y+2,result,26,TEAL if label=='Balanced' else ORANGE,True)
    text(358,y-20,formula,9,GRAY)
text(40,307,'The sets did not get worse. Classes with lower coverage became more common.',15,NAVY,True)
text(40,282,'The direction can reverse if the emphasized classes have higher coverage.',12,GRAY)
line(40,265,860,265,'#D6E0E5')
text(40,240,'DISCUSSION CHOICE: WHICH CLASSES SHOULD BECOME MORE COMMON?',11,TEAL,True)
box(40,128,385,91);box(446,128,414,91)
text(56,194,'Two interpretable examples',15,NAVY,True)
para(56,181,'Cat + dog; airplane + automobile.<br/>Easy to explain, but limited in scope.',353,12)
text(462,194,'All 45 class pairs',15,NAVY,True)
para(462,181,'Same shift strength, different emphasized classes.<br/>Show the range of outcomes, not only the mean.',382,12)
band(52,'FEEDBACK REQUESTED','Are two examples enough for this project, or should the analysis test sensitivity across more class pairs?')
c.save()
print(OUT)
