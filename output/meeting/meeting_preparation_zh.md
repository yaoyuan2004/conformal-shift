# 10 月 13 日 office hours：自己的准备笔记

## 这次 meeting 的定位

目标不是汇报整个项目已经完成，而是让老师看到：你记住了上次的反馈，把“distribution shift 不止一种”转化成了一个具体、可解释的设计，并且知道哪些选择值得请她判断。

给老师的两页 PDF 只讲实验设计，不展示训练完成情况、完整结果矩阵或模型优劣结论。它是选择性聚焦，不代表实验尚未运行。若老师直接问完成了多少，应如实回答。不要为了显得处于早期而说模型还没训练、结果还没出来，也不要虚构组员分工。

## 建议开场（约 40 秒）

“Last time, you pointed out that distribution shift includes more than image corruption. That helped me think about a second mechanism: changing the class proportions while keeping the images within each class unchanged. I’ve made some progress implementing the setup, and I brought a short design note. I’d especially appreciate your feedback on whether this label-shift construction is appropriate and how broadly we should vary the majority classes.”

这里的 I 指你自己的思考、实现进展与来请教的行为；讨论 group project 的共同研究问题时可以用 we。无需主动强调“我一个人做完了”，也不要把别人的工作说成自己的。PDF 不放组员名单或个人署名，避免材料抢占贡献归属的焦点。

## 5–8 分钟怎么讲

1. **一分钟：回应上次反馈。** “We now separate changes in image quality from changes in class composition.” 不用重复整份 proposal。
2. **两分钟：解释 label shift。** CIFAR-10 十类，保持每张图及其 prediction set 不变，只调整总体中类别出现的比例。两个被强调的类别各占 15%、20%、30%；其他八类平均分剩余概率。
3. **一分钟：解释为什么有意义。** 90% marginal coverage 并不等于每一类都有 90% coverage。类别间 coverage 不同，换类别比例就可能改变总体 coverage。这是设计动机和数学关系，不需要拿实验结果证明才可以讲。
4. **两到三分钟：请老师做一个具体判断。** 优先问下面的第一个问题，听完再决定是否问第二个。不要把三个问题连续念完。

## 最值得问的两个问题

**优先：类别选择是否足够系统？**

“The revised proposal mentions rotating the majority classes. The current setup uses cat/dog and airplane/automobile as two contrasting examples. Would you prefer an interpretable comparison like this, or a systematic sweep over all class pairs?”

你要理解的深一层：十个类别有 45 个无序类别对；现有 class-conditional metrics 足以重新加权，不需要重新训练。如果老师建议全部做，可以答：

“That should be feasible using the cached class-level statistics. I could summarize the range across pairs as well as show a few interpretable examples.”

**重要的思考点：不能只平均所有类别对。** 每一类在 45 个类别对中出现 9 次；固定 shift 强度后，对所有类别对等权平均，会把目标 prior 平均回每类 10%。固定 predictor 下，平均 coverage 因而回到 balanced coverage，可能掩盖不同类别对造成的上升和下降。更合适的是看 range、分位数、低于目标的比例，并展示少数例子。这是由设计推导出的性质，不是新增实验结果。

**其次：项目应偏诊断还是加一个修正方法？**

“Would a careful comparison of the two shift mechanisms be enough for the project, or would you recommend adding one adjustment method as a baseline?”

别把问题问成“还需要我做多少”。你希望老师帮助判断研究问题的边界，而不是发明更多工作。

## 几个可能被追问的点

**Have you run experiments yet?**

“Yes. The implementation and a set of experimental runs are in place. What I’d like to review today is the design and interpretation, especially the class-pair selection, before settling on what to emphasize.”

如果继续问 all the experiments 是否做完，应说明当前设定下已有哪些结果，而不是坚持用 some 淡化事实。已有运行完成，不等于研究范围、论证和最终报告已经定稿。

**Is this covariate shift?**

“I’m calling the first setting image-corruption shift. Keeping the semantic labels unchanged does not automatically establish that P(Y given X) stays fixed. For label shift, the explicit assumption is that P(X given Y) remains fixed while P(Y) changes.”

**Are you retraining for label shift?**

“No. It is a controlled reweighting of clean class-conditional evaluation statistics. The predictor and the individual prediction sets are fixed.”

**Are the three splits independent runs?**

“They are overlapping split-sensitivity checks, not independently trained models or independent replications.”

**Why not always use the method with the highest coverage?**

“Coverage needs to be interpreted together with set size. A predictor that returns all ten labels is not a useful solution to the efficiency question.”

## 只有老师主动要结果时，才用的备用材料

不要主动打开完整 final-analysis notebook 或五张总图。可以先问她更想看哪一个机制，再展示一张相关图。

- `figures/figure4_label_shift_coverage.png`：label-shift 结果；误差棒是三个重叠 split 的 sample SD，不是置信区间。
- 如果她问有没有有趣现象：在 severe cat/dog-heavy 条件下，LAC 的 mean coverage 为 Standard 86.29%、AugMix 84.79%。但在 severity-5 Gaussian noise 下，LAC 为 Standard 16.73%、AugMix 57.67%。这是两个冻结模型在指定条件下的观察，不能概括成 AugMix 普遍改善或恶化所有 shift。
- 对这一反差的解释方向：label shift 放大的是 class-conditional coverage 的差异；corruption robustness 不自动意味着对类别比例变化同样稳健。这里关注 coverage，不要把低 coverage 简化为“分类更差”。

这些数字来自 `results/stage9_label_shift_main_scenarios.csv` 和 `results/stage9_severity5_comparison.csv`。不需要在开场、PDF 或主动汇报中使用。

## 推荐信目标怎么自然服务于这次 meeting

最值得让老师看到的不是工作量，而是三件可以观察到的事：你落实了她的建议；你能解释设计背后的机制；你能辨认设计中的不足并提出可行的修订方式。

这次不必为了推荐信刻意制造“惊人进度”，也不用故意表现得没有进展。认真听她对 class pairs 和 scope 的判断，记下具体建议，之后真正落实，再带着有针对性的结果回来，老师就会有更具体的例子评价你的研究习惯。

可以这样收尾：

“That helps clarify the direction. I’ll use your feedback to refine the class-prior scenarios and organize the comparison around the mechanisms we discussed.”

收尾应根据她实际说的话调整，不要预先承诺她没有要求的实验。

## 可选阅读，不作为老师指定论文的替代

若老师建议加 label-shift adjustment，可查看 Podkopaev and Ramdas (2021), *Distribution-free uncertainty quantification for classification under label shift*: https://proceedings.mlr.press/v161/podkopaev21a.html 。该文研究 label-shift 下的 uncertainty quantification 与重加权。你现在重加权的是 evaluation metrics，不是已经实现了该文的校准修正。没有确认你上次收到的论文是哪一篇，也不声称你已经读完这篇。
