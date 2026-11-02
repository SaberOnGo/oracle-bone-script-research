# obs-char-000269 甲骨字档案

状态：已释字候选（HUST-OBC 数据集类别，未经交叉复核） | 释读史：未收集 | 例句：2 | 更新：2026-11-02

## 1 字形与观察

![obs-char-000269 字形图](images/001_asset-000274_hust-obc-cat-0302_0303_glyph.png)

- 图 1：HUST-OBC 已释字第 0302_0303 类的一张样本，28 × 80 像素〔来源 src-hust-obc `HUST-OBC/deciphered/0302_0303/0302/G_0302_乙102合21398.png`〕。
- 该类别由 2 个来源子类合并而成〔来源 src-hust-obc Validation_label.json〕。
- 观察：图像左侧有三道短而平行的弯曲痕迹，右侧有长下行笔画并带轻微折转。

## 2 隶定与今字候选

- HUST-OBC 官方对照表给本类的字是“又”（U+53C8）、“右”（U+53F3）。这是数据集标注，不是本项目复核过的释读〔来源 src-hust-obc `HUST-OBC/deciphered/ID_to_chinese.json`〕。
- OBIMD 主字表中有 2 个字形被隶定为同一字（UID：0uhj5zj3ce、c40r3zyq5t），可据此查找卜辞字例〔来源 src-obimd 主字表〕。
- EvoBC 有 2 个类别标为同一字（evobc-evo-cat-01449、evobc-evo-cat-01482），可用于跨时期字形比较〔来源 src-evobc〕。
- 更正：本档案 2026-11-02 合并时曾写作“㔤㔥”。那是早期流程把本类号错接到 HUST-OBC OCR 字表的结果，已按官方对照表更正。

## 4 卜辞例句

以下例句取自 OBIMD 标注，按其阅读顺序排列；□ 为未识别或残缺字，◇ 为 OBIMD 自造字。片号 H 后的数字推定为《合集》号，尚待逐片核对（见案件 `case-h2-heji2`）。

| OBIMD 片号 | 释文（OBIMD） | 本字位置 | 来源 |
| --- | --- | --- | --- |
| H17 | 辛亥卜□貞眾□往臿□㞢擒 | 第 11/12 字 | src-obimd H17 句组 1 |
| H18 | 戌寅卜爭貞今春眾㞢工◇ | 第 9/11 字 | src-obimd H18 句组 1 |

- 其他字例所在甲骨：H33、H47、H48、H64、H115、H132、H156、H169、H175、H198等〔来源 src-obimd〕。

## 5 分布

- OBIMD 中共 1937 个字例，见于 1576 片甲骨；按句组类别：卜辞句 1931，未定 6〔来源 src-obimd，统计表 `corpus/002_oracle-bone-inscriptions/010_inscription-texts/002_obimd-glyph-occurrence-stats.csv`〕。
- 同一句组中最常一起出现的字：貞（623）、于（555）、卜（538）、其（359）、王（212）、受（117）。
- OBIMD 没有分期和组类字段，分期分布尚待《合集》分期表或小学堂材料来源表补入。

## 8 实物与出土（著录线索）

样本文件名 `G_0302_乙102合21398.png` 带有著录线索。以下只是文件名解析结果，尚未在著录中核对：

- 合集号：合21398
- 旧著录：乙102。简称“乙”未在小学堂附录简称表中找到。

## 10 来源与权利

- 来源 src-hust-obc，图片资产 `asset-000274`，权利状态 `source_marked_risk_noted`。HUST-OBC 的 Figshare 与期刊页面许可表述不一致，详见来源档案 `corpus/006_research-sources-and-bibliography/001_source-objects/015_src-hust-obc_source-object/`。
- 图片 SHA-256：`64745d956365ded7ad3164afacf22fccd2c78ad0df92720f3e35b89ead0e30b3`；来源包 `large-src-000001`。

## 11 待查项

- 在拓片上核对例句中本字的写法是否与本档案字形图一致；OBIMD 把它们隶定为同一字，不等于字形相同。
- 在《甲骨文合集》21398 号（文件名写作“合21398”）上找到本字例，抄录所在卜辞全文并标出字位。
- 核对旧著录“乙102”的原拓，确认简称所指的书目，以及它与合集号的对应。
- 在小学堂甲骨文字编中查找字头“又右”，核对字形是否与本类样本一致，记录释读、提出者和出处。
