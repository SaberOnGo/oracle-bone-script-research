# obs-char-000354 甲骨字档案

状态：已释字候选（HUST-OBC 数据集类别，未经交叉复核） | 释读史：未收集 | 例句：2 | 更新：2026-11-02

## 1 字形与观察

![obs-char-000354 字形图](images/001_asset-000359_hust-obc-cat-0401_0402_glyph.png)

- 图 1：HUST-OBC 已释字第 0401_0402 类的一张样本，36 × 80 像素〔来源 src-hust-obc `HUST-OBC/deciphered/0401_0402/0401/G_0401_乙103合20927.png`〕。
- 该类别由 2 个来源子类合并而成〔来源 src-hust-obc Validation_label.json〕。
- 观察：中部尖状闭合轮廓被短横笔画穿过，并连接下方纤细主干。

## 2 隶定与今字候选

- HUST-OBC 官方对照表给本类的字是“執”（U+57F7）、“縶”（U+7E36）。这是数据集标注，不是本项目复核过的释读〔来源 src-hust-obc `HUST-OBC/deciphered/ID_to_chinese.json`〕。
- OBIMD 主字表中有 1 个字形被隶定为同一字（UID：rbq68qstjy），可据此查找卜辞字例〔来源 src-obimd 主字表〕。
- EvoBC 有 2 个类别标为同一字（evobc-evo-cat-01886、evobc-evo-cat-06651），可用于跨时期字形比较〔来源 src-evobc〕。
- 更正：本档案 2026-11-02 合并时曾写作“㖇㖈”。那是早期流程把本类号错接到 HUST-OBC OCR 字表的结果，已按官方对照表更正。

## 4 卜辞例句

以下例句取自 OBIMD 标注，按其阅读顺序排列；□ 为未识别或残缺字，◇ 为 OBIMD 自造字。片号 H 后的数字推定为《合集》号，尚待逐片核对（见案件 `case-h2-heji2`）。

| OBIMD 片号 | 释文（OBIMD） | 本字位置 | 来源 |
| --- | --- | --- | --- |
| H553 | 癸丑卜賓貞令彗墉以□執寇七月 | 第 11/14 字 | src-obimd H553 句组 4 |
| H570 | 丁酉卜古貞◇執寇◇ | 第 7/9 字 | src-obimd H570 句组 1 |

- 其他字例所在甲骨：H572、H578、H693、H796、H797、H798、H799、H801、H804、H10373等〔来源 src-obimd〕。

## 5 分布

- OBIMD 中共 20 个字例，见于 20 片甲骨；按句组类别：卜辞句 20〔来源 src-obimd，统计表 `corpus/002_oracle-bone-inscriptions/010_inscription-texts/002_obimd-glyph-occurrence-stats.csv`〕。
- 同一句组中最常一起出现的字：貞（10）、卜（8）、其（6）、王（5）、寇（4）、印（4）。
- OBIMD 没有分期和组类字段，分期分布尚待《合集》分期表或小学堂材料来源表补入。

## 8 实物与出土（著录线索）

样本文件名 `G_0401_乙103合20927.png` 带有著录线索。以下只是文件名解析结果，尚未在著录中核对：

- 合集号：合20927
- 旧著录：乙103。简称“乙”未在小学堂附录简称表中找到。

## 10 来源与权利

- 来源 src-hust-obc，图片资产 `asset-000359`，权利状态 `source_marked_risk_noted`。HUST-OBC 的 Figshare 与期刊页面许可表述不一致，详见来源档案 `corpus/006_research-sources-and-bibliography/001_source-objects/015_src-hust-obc_source-object/`。
- 图片 SHA-256：`17100dfca202af16af5f43aa6c26ec753d613e05338b43d931af78a93846dee0`；来源包 `large-src-000001`。

## 11 待查项

- 在拓片上核对例句中本字的写法是否与本档案字形图一致；OBIMD 把它们隶定为同一字，不等于字形相同。
- 在《甲骨文合集》20927 号（文件名写作“合20927”）上找到本字例，抄录所在卜辞全文并标出字位。
- 核对旧著录“乙103”的原拓，确认简称所指的书目，以及它与合集号的对应。
- 在小学堂甲骨文字编中查找字头“執縶”，核对字形是否与本类样本一致，记录释读、提出者和出处。
