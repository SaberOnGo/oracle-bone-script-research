# obs-char-000106 甲骨字档案

状态：已释字候选（HUST-OBC 数据集类别，未经交叉复核） | 释读史：未收集 | 例句：2 | 更新：2026-11-02

## 1 字形与观察

![obs-char-000106 字形图](images/001_asset-000111_hust-obc-cat-0119_0120_glyph.png)

- 图 1：HUST-OBC 已释字第 0119_0120 类的一张样本，49 × 80 像素〔来源 src-hust-obc `HUST-OBC/deciphered/0119_0120/0119/G_0119_乙108合21022𠂤組.png`〕。
- 该类别由 2 个来源子类合并而成〔来源 src-hust-obc Validation_label.json〕。
- 观察：图像上方有两道短横笔，下方有弧形环状笔，左下另有分离的钩状笔。

## 2 隶定与今字候选

- HUST-OBC 官方对照表给本类的字是“云”（U+4E91）、“雲”（U+96F2）。这是数据集标注，不是本项目复核过的释读〔来源 src-hust-obc `HUST-OBC/deciphered/ID_to_chinese.json`〕。
- OBIMD 主字表中有 1 个字形被隶定为同一字（UID：zmixmtzym6），可据此查找卜辞字例〔来源 src-obimd 主字表〕。
- EvoBC 有 2 个类别标为同一字（evobc-evo-cat-00687、evobc-evo-cat-09839），可用于跨时期字形比较〔来源 src-evobc〕。
- 更正：本档案 2026-11-02 合并时曾写作“㑭㑮”。那是早期流程把本类号错接到 HUST-OBC OCR 字表的结果，已按官方对照表更正。

## 4 卜辞例句

以下例句取自 OBIMD 标注，按其阅读顺序排列；□ 为未识别或残缺字，◇ 为 OBIMD 自造字。片号 H 后的数字推定为《合集》号，尚待逐片核对（见案件 `case-h2-heji2`）。

| OBIMD 片号 | 释文（OBIMD） | 本字位置 | 来源 |
| --- | --- | --- | --- |
| H5600 | 貞茲云雨 | 第 3/4 字 | src-obimd H5600 句组 4 |
| H13386 | 庚寅貞茲云其雨 | 第 5/7 字 | src-obimd H13386 句组 1 |

- 其他字例所在甲骨：H13387、H13389、H13394、H13397、H13400、H13402、H14227、H21197、HD161〔来源 src-obimd〕。

## 5 分布

- OBIMD 中共 12 个字例，见于 11 片甲骨；按句组类别：卜辞句 12〔来源 src-obimd，统计表 `corpus/002_oracle-bone-inscriptions/010_inscription-texts/002_obimd-glyph-occurrence-stats.csv`〕。
- 同一句组中最常一起出现的字：茲（6）、貞（6）、其（4）、雨（3）、于（3）、尞（3）。
- OBIMD 没有分期和组类字段，分期分布尚待《合集》分期表或小学堂材料来源表补入。

## 8 实物与出土（著录线索）

样本文件名 `G_0119_乙108合21022𠂤組.png` 带有著录线索。以下只是文件名解析结果，尚未在著录中核对：

- 合集号：合21022
- 旧著录：乙108。简称“乙”未在小学堂附录简称表中找到。
- 组类或附注（文件名原文）：𠂤組

## 10 来源与权利

- 来源 src-hust-obc，图片资产 `asset-000111`，权利状态 `source_marked_risk_noted`。HUST-OBC 的 Figshare 与期刊页面许可表述不一致，详见来源档案 `corpus/006_research-sources-and-bibliography/001_source-objects/015_src-hust-obc_source-object/`。
- 图片 SHA-256：`cf39efeeb8fb52d49897399f0d69361df19fce54da1a05095bad1884504733bb`；来源包 `large-src-000001`。

## 11 待查项

- 在拓片上核对例句中本字的写法是否与本档案字形图一致；OBIMD 把它们隶定为同一字，不等于字形相同。
- 在《甲骨文合集》21022 号（文件名写作“合21022”）上找到本字例，抄录所在卜辞全文并标出字位。
- 核对旧著录“乙108”的原拓，确认简称所指的书目，以及它与合集号的对应。
- 在小学堂甲骨文字编中查找字头“云雲”，核对字形是否与本类样本一致，记录释读、提出者和出处。
