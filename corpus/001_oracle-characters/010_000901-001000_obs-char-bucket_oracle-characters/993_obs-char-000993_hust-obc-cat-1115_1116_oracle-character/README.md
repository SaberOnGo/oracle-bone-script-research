# obs-char-000993 甲骨字档案

状态：已释字候选（HUST-OBC 数据集类别，未经交叉复核） | 释读史：未收集 | 例句：2 | 更新：2026-11-02

## 1 字形与观察

![obs-char-000993 字形图](images/001_asset-000998_hust-obc-cat-1115_1116_glyph.png)

- 图 1：HUST-OBC 已释字第 1115_1116 类的一张样本，30 × 80 像素〔来源 src-hust-obc `HUST-OBC/deciphered/1115_1116/1115/G_1115_七S73.png`〕。
- 该类别由 2 个来源子类合并而成〔来源 src-hust-obc Validation_label.json〕。
- 观察：小型上部分枝笔群位于矩形中央闭合轮廓之上，下方有两条侧笔。

## 2 隶定与今字候选

- HUST-OBC 官方对照表给本类的字是“登”（U+767B）、“𤼷”（U+24F37）。这是数据集标注，不是本项目复核过的释读〔来源 src-hust-obc `HUST-OBC/deciphered/ID_to_chinese.json`〕。
- OBIMD 主字表中有 1 个字形被隶定为同一字（UID：fkhhsjy5jk），可据此查找卜辞字例〔来源 src-obimd 主字表〕。
- EvoBC 有 2 个类别标为同一字（evobc-evo-cat-05711、evobc-evo-cat-11743），可用于跨时期字形比较〔来源 src-evobc〕。
- 更正：本档案 2026-11-02 合并时曾写作“㡑㡒”。那是早期流程把本类号错接到 HUST-OBC OCR 字表的结果，已按官方对照表更正。

## 4 卜辞例句

以下例句取自 OBIMD 标注，按其阅读顺序排列；□ 为未识别或残缺字，◇ 为 OBIMD 自造字。片号 H 后的数字推定为《合集》号，尚待逐片核对（见案件 `case-h2-heji2`）。

| OBIMD 片号 | 释文（OBIMD） | 本字位置 | 来源 |
| --- | --- | --- | --- |
| H205 | 貞□登獲羌 | 第 3/5 字 | src-obimd H205 句组 1 |
| H475 | 貞登王亥羌□ | 第 2/6 字 | src-obimd H475 句组 2 |

- 其他字例所在甲骨：H699、H1333、H4064、H5822、H6540、H6759、H6835、H7310、H7312、H7319等〔来源 src-obimd〕。

## 5 分布

- OBIMD 中共 50 个字例，见于 48 片甲骨；按句组类别：卜辞句 50〔来源 src-obimd，统计表 `corpus/002_oracle-bone-inscriptions/010_inscription-texts/002_obimd-glyph-occurrence-stats.csv`〕。
- 同一句组中最常一起出现的字：貞（24）、卜（13）、于（11）、其（10）、王（9）、人（9）。
- OBIMD 没有分期和组类字段，分期分布尚待《合集》分期表或小学堂材料来源表补入。

## 8 实物与出土（著录线索）

样本文件名 `G_1115_七S73.png` 带有著录线索。以下只是文件名解析结果，尚未在著录中核对：

- 旧著录：七S73。简称“七S”未在小学堂附录简称表中找到。

## 10 来源与权利

- 来源 src-hust-obc，图片资产 `asset-000998`，权利状态 `source_marked_risk_noted`。HUST-OBC 的 Figshare 与期刊页面许可表述不一致，详见来源档案 `corpus/006_research-sources-and-bibliography/001_source-objects/015_src-hust-obc_source-object/`。
- 图片 SHA-256：`de853ee5e362a23619fc9de42e6ad00b5fcc7f6df49b55f075915ff9997661a1`；来源包 `large-src-000001`。

## 11 待查项

- 在拓片上核对例句中本字的写法是否与本档案字形图一致；OBIMD 把它们隶定为同一字，不等于字形相同。
- 核对旧著录“七S73”的原拓，确认简称所指的书目，以及它与合集号的对应。
- 在小学堂甲骨文字编中查找字头“登𤼷”，核对字形是否与本类样本一致，记录释读、提出者和出处。
