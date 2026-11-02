# obs-char-000297 甲骨字档案

状态：已释字候选（HUST-OBC 数据集类别，未经交叉复核） | 释读史：未收集 | 例句：2 | 更新：2026-11-02

## 1 字形与观察

![obs-char-000297 字形图](images/001_asset-000302_hust-obc-cat-0336_0337_glyph.png)

- 图 1：HUST-OBC 已释字第 0336_0337 类的一张样本，61 × 101 像素〔来源 src-hust-obc `HUST-OBC/deciphered/0336_0337/0336/G_0336_甲骨文0.png`〕。
- 该类别由 2 个来源子类合并而成〔来源 src-hust-obc Validation_label.json〕。
- 观察：图像由上下叠置的两个圆角长方形轮廓组成，中间有狭窄间隔，未见清楚的内部痕迹。

## 2 隶定与今字候选

- HUST-OBC 官方对照表给本类的字是“吕”（U+5415）、“呂”（U+5442）。这是数据集标注，不是本项目复核过的释读〔来源 src-hust-obc `HUST-OBC/deciphered/ID_to_chinese.json`〕。
- OBIMD 主字表中有 1 个字形被隶定为同一字（UID：7wp6czwrw0），可据此查找卜辞字例〔来源 src-obimd 主字表〕。
- EvoBC 有 2 个类别标为同一字（evobc-evo-cat-01504、evobc-evo-cat-01530），可用于跨时期字形比较〔来源 src-evobc〕。
- 更正：本档案 2026-11-02 合并时曾写作“㕆㕇”。那是早期流程把本类号错接到 HUST-OBC OCR 字表的结果，已按官方对照表更正。

## 4 卜辞例句

以下例句取自 OBIMD 标注，按其阅读顺序排列；□ 为未识别或残缺字，◇ 为 OBIMD 自造字。片号 H 后的数字推定为《合集》号，尚待逐片核对（见案件 `case-h2-heji2`）。

| OBIMD 片号 | 释文（OBIMD） | 本字位置 | 来源 |
| --- | --- | --- | --- |
| H3823 | 癸未卜古貞□令◇易皀吕 | 第 11/11 字 | src-obimd H3823 句组 1 |
| H30354 | 叀歸愆吕用且丁升 | 第 4/8 字 | src-obimd H30354 句组 2 |

- 其他字例所在甲骨：H6779、HD276、HD284、HD401、HD409、HD467〔来源 src-obimd〕。

## 5 分布

- OBIMD 中共 12 个字例，见于 8 片甲骨；按句组类别：卜辞句 12〔来源 src-obimd，统计表 `corpus/002_oracle-bone-inscriptions/010_inscription-texts/002_obimd-glyph-occurrence-stats.csv`〕。
- 同一句组中最常一起出现的字：卜（10）、于（6）、◇（6）、乙（6）、其（5）、用（4）。
- OBIMD 没有分期和组类字段，分期分布尚待《合集》分期表或小学堂材料来源表补入。

## 10 来源与权利

- 来源 src-hust-obc，图片资产 `asset-000302`，权利状态 `source_marked_risk_noted`。HUST-OBC 的 Figshare 与期刊页面许可表述不一致，详见来源档案 `corpus/006_research-sources-and-bibliography/001_source-objects/015_src-hust-obc_source-object/`。
- 图片 SHA-256：`28cdc1a3527c8934e5cb9303b9707352cd104e9df327815f6bfe87e279b6a7a3`；来源包 `large-src-000001`。

## 11 待查项

- 在拓片上核对例句中本字的写法是否与本档案字形图一致；OBIMD 把它们隶定为同一字，不等于字形相同。
- 在小学堂甲骨文字编中查找字头“吕呂”，核对字形是否与本类样本一致，记录释读、提出者和出处。
