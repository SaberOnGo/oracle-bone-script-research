# Claim-Evidence Locator / 说法—证据定位

## Dataset Scale / 数据规模

- Locator: abstract, Methods, Table 2, and Data Records.
- Source report: 229,170 images and 13,714 categories.
- Allowed use: describe the paper's reported dataset scope.
- Blocked use: treating every category as a confirmed oracle character.
- 定位：摘要、Methods、表 2 和 Data Records。
- 可用：描述论文报告的数据集范围。
- 禁止：把每个类别当作已确认甲骨单字。

## Image Classification / 图像分类

- Locator: Technical Validation, Image Classification, Table 4 and Figure 6.
- Source report: Top-1 results of 85.56% and 86.66% for two classifiers.
- Meaning: closed-set category classification on a reported 9:1 split.
- Blocked use: converting these scores into reading probabilities.
- 定位：Technical Validation 的 Image Classification、表 4、图 6。
- 含义：论文所述 9:1 划分上的闭集类别分类。
- 禁止：把分类分数换算成释读概率。

## Simulated Deciphering / 模拟破译

- Locator: Technical Validation, Oracle Bone Character Deciphering
  Simulation, Figure 7.
- Source report: ResNet-101 Top-1 16.7% and Top-20 55.8%.
- Source report: a conditional diffusion model generates later-script images.
- Meaning: benchmark performance against dataset labels and generated images.
- Blocked use: claiming a calibrated posterior that unknown form A means B.
- 定位：Technical Validation 的 Oracle Bone Character Deciphering
  Simulation 和图 7。
- 来源报告：ResNet-101 Top-1 为 16.7%，Top-20 为 55.8%。
- 含义：相对于数据集标签和生成图像的基准实验。
- 禁止：声称“未知字甲就是乙”的校准后验概率。

Top-k inclusion depends on a predefined candidate universe. It is not a
probability distribution over scholarly readings and includes no calibrated
lower confidence bound for a new undeciphered case.

Top-k 命中依赖预设候选全集，不是学术释读的概率分布，也没有为新未释字
提供经过校准的概率下界。
