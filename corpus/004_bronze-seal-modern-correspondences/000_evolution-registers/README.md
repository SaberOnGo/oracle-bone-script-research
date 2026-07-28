# Evolution Registers / 字形演化登记表

English:
This directory stores staging records for cross-period character-evolution
metadata. The staging rows are machine-readable source derivatives, while the
sibling `obs-evo-cand-bucket` directories provide object-local human review
entrances and AI packets.

Simplified Chinese:
本目录保存跨时期字形演化 metadata 的暂存记录。这里的暂存行是机器可读的
来源派生表；同级的 `obs-evo-cand-bucket` 目录提供对象内的人类复核入口和
AI packet。

Current EVOBC files:

- `001_evobc-evolution-category-staging.csv`: EVOBC category-level staging
  index with 13,714 dataset categories and compact image-reference counts by
  script era.
- `002_evobc-era-source-codebook-staging.csv`: EVOBC era/source codebook
  staging table. Era codes are mapped to README shorthands; source codes are
  preserved only as observed filename-token evidence.

当前 EVOBC 文件：

- `001_evobc-evolution-category-staging.csv`：EVOBC 类别级暂存索引，包含
  13,714 个数据集类别，以及按文字时代压缩后的图像引用计数。
- `002_evobc-era-source-codebook-staging.csv`：EVOBC 时代码/source 码暂存表。
  时代码依据 README 缩写映射；source 数字码只保留从文件名 token 观察到的证据。

These records are metadata-only. They help plan oracle-bone, bronze, seal,
Warring States, and clerical-script comparison work, but they are not accepted
paleographic correspondences. Formal import still requires source-chain review
against stronger character dictionaries, inscription records, and image
provenance.

这些记录只属于 metadata。它们可以帮助规划甲骨文、金文、小篆、战国文字和
隶书的比较工作，但不是已接受的古文字学对应关系。正式导入仍需要与更强的
字书、卜辞记录和图像出处进行来源链复核。
