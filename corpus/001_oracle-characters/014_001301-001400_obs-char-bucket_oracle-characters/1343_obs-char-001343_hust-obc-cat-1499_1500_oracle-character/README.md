# obs-char-001343 甲骨字档案

状态：已释字候选（HUST-OBC 数据集类别，未经交叉复核） | 释读史：未收集 | 例句：2 | 更新：2026-11-02

## 1 字形与观察

![obs-char-001343 字形图](images/001_asset-001348_hust-obc-cat-1499_1500_glyph.png)

- 图 1：HUST-OBC 已释字第 1499_1500 类的一张样本，74 × 80 像素〔来源 src-hust-obc `HUST-OBC/deciphered/1499_1500/1499/G_1499_京津438(甲).png`〕。
- 该类别由 2 个来源子类合并而成〔来源 src-hust-obc Validation_label.json〕。
- 观察：组合图像有狭长左侧分枝标记，右侧较大形体包含上部框形和下部方框。

## 2 隶定与今字候选

- HUST-OBC 官方对照表给本类的字是“鄉”（U+9109）、“饗”（U+9957）。这是数据集标注，不是本项目复核过的释读〔来源 src-hust-obc `HUST-OBC/deciphered/ID_to_chinese.json`〕。
- OBIMD 主字表中有 1 个字形被隶定为同一字（UID：k2sr7n4ffj），可据此查找卜辞字例〔来源 src-obimd 主字表〕。
- EvoBC 有 2 个类别标为同一字（evobc-evo-cat-09181、evobc-evo-cat-10139），可用于跨时期字形比较〔来源 src-evobc〕。
- 更正：本档案 2026-11-02 合并时曾写作“㧑㧒”。那是早期流程把本类号错接到 HUST-OBC OCR 字表的结果，已按官方对照表更正。

## 4 卜辞例句

以下例句取自 OBIMD 标注，按其阅读顺序排列；□ 为未识别或残缺字，◇ 为 OBIMD 自造字。片号 H 后的数字推定为《合集》号，尚待逐片核对（见案件 `case-h2-heji2`）。

| OBIMD 片号 | 释文（OBIMD） | 本字位置 | 来源 |
| --- | --- | --- | --- |
| H3280 | 貞叀邑◇乎鄉◇ | 第 6/7 字 | src-obimd H3280 句组 3 |
| H5237 | 庚午卜爭貞叀王鄉戎 | 第 8/9 字 | src-obimd H5237 句组 1 |

- 其他字例所在甲骨：H5241、H5244、H5246、H5249、H12797、H23003、H26017、H30345、H30910、H31040等〔来源 src-obimd〕。

## 5 分布

- OBIMD 中共 25 个字例，见于 20 片甲骨；按句组类别：卜辞句 25〔来源 src-obimd，统计表 `corpus/002_oracle-bone-inscriptions/010_inscription-texts/002_obimd-glyph-occurrence-stats.csv`〕。
- 同一句组中最常一起出现的字：其（10）、卜（8）、貞（7）、王（7）、甲（6）、乎（4）。
- OBIMD 没有分期和组类字段，分期分布尚待《合集》分期表或小学堂材料来源表补入。

## 8 实物与出土（著录线索）

样本文件名 `G_1499_京津438(甲).png` 带有著录线索。以下只是文件名解析结果，尚未在著录中核对：

- 旧著录：京津438。简称“京津”在小学堂《合集材料来源表》附录中对应《京津散見甲骨文字》；HUST 文件名是否沿用同一体例尚未核实〔来源 src-xiaoxuetang-obm〕。
- 组类或附注（文件名原文）：(甲)

## 10 来源与权利

- 来源 src-hust-obc，图片资产 `asset-001348`，权利状态 `source_marked_risk_noted`。HUST-OBC 的 Figshare 与期刊页面许可表述不一致，详见来源档案 `corpus/006_research-sources-and-bibliography/001_source-objects/015_src-hust-obc_source-object/`。
- 图片 SHA-256：`38b35aaab55a3321ce3801722629ee34be434d2913db468302b43c0b1ff6c554`；来源包 `large-src-000001`。

## 11 待查项

- 在拓片上核对例句中本字的写法是否与本档案字形图一致；OBIMD 把它们隶定为同一字，不等于字形相同。
- 核对旧著录“京津438”的原拓，确认简称所指的书目，以及它与合集号的对应。
- 在小学堂甲骨文字编中查找字头“鄉饗”，核对字形是否与本类样本一致，记录释读、提出者和出处。
