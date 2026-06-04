# Character Registers / 甲骨字索引

English:
Register files index all character records and their source mappings.

Current registers:

- `001_all-oracle-characters-index.csv`: accepted project character records.
- `002_deciphered-oracle-characters-index.csv`: accepted deciphered project character records.
- `003_undeciphered-oracle-characters-index.csv`: accepted undeciphered project character records.
- `004_character-id-assignment-log.md`: formal project ID assignment notes.
- `005_hust-obc-validation-class-staging.csv`: HUST-OBC validation-class staging index with 1,588 dataset candidate classes. These rows do not assign formal `obs-char-*` IDs and must not be treated as accepted paleographic readings.
- `006_obimd-main-character-staging.csv`: OBIMD main-character UID staging index with 3,936 dataset candidate main characters. These rows preserve UID/codepoint/transcription metadata for review and do not assign formal `obs-char-*` IDs.
- `007_hust-obc-validation-label-crosswalk-staging.csv`: HUST-OBC validation-class to OCR-label crosswalk with 1,588 dataset label candidates. These labels are useful for lookup but are not accepted oracle-character readings.
- `008_hust-obc-source-category-staging.csv`: HUST-OBC source-category staging index with 1,781 dataset category labels expanded from the 1,588 validation classes. These rows are lower-level dataset references, not formal project character IDs.

简体中文：
索引文件用于登记所有甲骨字记录及其来源映射。

当前索引：

- `001_all-oracle-characters-index.csv`：正式本项目甲骨单字记录。
- `002_deciphered-oracle-characters-index.csv`：正式已释甲骨单字记录。
- `003_undeciphered-oracle-characters-index.csv`：正式未释甲骨单字记录。
- `004_character-id-assignment-log.md`：正式项目 ID 分配说明。
- `005_hust-obc-validation-class-staging.csv`：HUST-OBC validation class 暂存索引，包含 1,588 个数据集候选类别。这些行不分配正式 `obs-char-*` ID，也不得当作已接受的古文字学释读。
- `006_obimd-main-character-staging.csv`：OBIMD main-character UID 暂存索引，包含 3,936 个数据集候选主字。该表保留 UID、codepoint 和 transcription metadata 以供复核，不分配正式 `obs-char-*` ID。
- `007_hust-obc-validation-label-crosswalk-staging.csv`：HUST-OBC validation class 到 OCR label 的交叉暂存表，包含 1,588 个数据集标签候选。这些标签可用于检索，但不是已接受的甲骨文字释读。
- `008_hust-obc-source-category-staging.csv`：HUST-OBC source category 暂存索引，把 1,588 个 validation class 展开为 1,781 个数据集类别标签。这些行是更底层的数据集引用，不是正式本项目甲骨单字 ID。
