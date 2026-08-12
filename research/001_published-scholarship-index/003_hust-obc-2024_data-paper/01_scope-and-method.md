# Scope And Method / 范围与方法

## Paper Scope / 论文范围

The paper is a data descriptor for HUST-OBC. Its unit is mainly a cropped or
drawn single-character image grouped under a dataset category. It does not
provide a complete inscription, plate, findspot, collection record, or
reading history for every image.

本文是 HUST-OBC 数据说明。其主要单位是按数据集类别归组的单字裁图或
手写图，并不为每张图提供完整卜辞、图版、出土地、馆藏或释读史。

## Source-Reported Pipeline / 来源报告的流程

The official HTML locates the workflow under `Methods`, with the following
named stages:

1. `Data Acquisition`: material gathered from books, websites, and existing
   databases.
2. `Automatic Annotation`: source-specific extraction and label generation.
3. `Data Integration`: category comparison and merging across sources.
4. `Data Validation`: review and removal of erroneous samples.

官方 HTML 在 `Methods` 下依次说明下列阶段：

1. `Data Acquisition`：从图书、网站和既有数据库收集资料。
2. `Automatic Annotation`：按来源抽取图像并生成标签。
3. `Data Integration`：跨来源比较和合并类别。
4. `Data Validation`：复核并移除错误样本。

The paper reports scanned or processed rubbing-derived forms, traced forms,
and manually drawn forms. These material types must remain distinct in later
object dossiers.

论文报告的资料包括拓片扫描或处理所得字形、据拓片描摹的字形以及人工
书写字形。后续对象档案必须区分这些资料层。

## Human And Technical Review / 人工与技术复核

Under `Methods` > `Validation`, the authors report that oracle-bone scholars
from Anyang Normal University checked the preliminary dataset against books
and HWOBC database fonts, removing errors and retaining relatively accurate
samples. This is source-reported expert review, not an independent audit by
this repository.

论文在 `Methods` > `Validation` 报告：Anyang Normal University 的甲骨文
研究者依据图书和 HWOBC 数据库字形复核初步数据，删除错误样本并保留
相对准确者。这是来源报告的专家复核，不是本仓库的独立审计。

Under `Technical Validation`, the paper reports an 8:1:1 stratified split,
a ResNet-50 classifier, 94.6% test accuracy, and macro F1 of 0.914. The task is
closed-set image classification over source labels. It does not validate a
new reading or calibrate a decipherment probability.

论文在 `Technical Validation` 报告 8:1:1 分层划分、ResNet-50、94.6%
测试准确率和 0.914 宏平均 F1。该任务是来源标签上的闭集图像分类，
不验证新释读，也不校准破译概率。

## Appropriate Use / 适用范围

- Route an image to its HUST class, source-family code, and package member.
- Compare source-reported dataset categories and preprocessing choices.
- Select cases for later visual, inscription, catalog, and literature review.
- Do not use a class label alone as a modern reading or identity decision.
- 可用于追踪图像的 HUST 类别、来源族代码和包内成员。
- 可用于比较来源报告的数据类别和预处理选择。
- 可用于筛选后续字形、卜辞、著录和文献复核对象。
- 不得仅凭类别标签确认今字释读或对象身份。
