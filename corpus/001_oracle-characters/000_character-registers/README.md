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
- `009_hust-obc-obs-char-promotion-review-queue.csv`: review queue with 1,588 HUST-OBC candidate classes and suggested `obs-char-*` IDs. These IDs are reserved suggestions only and are not formal assignments until cross-source review.
- `010_hust-obc-promotion-bucket-review-summary.csv`: batch-level summary for the 16 HUST-OBC promotion bucket manifests. It helps reviewers and AI Agents choose review batches and preserves the reserved-only boundary.
- `011_hust-obimd-evobc-codepoint-crosswalk-staging.csv`: metadata-only codepoint crosswalk candidates from HUST-OBC promotion rows to OBIMD and EVOBC dataset rows. Exact codepoint matches are retrieval routes only, not confirmed character identity, readings, component assignments, or evolution chains.
- Bucket manifests named `001_hust-obc-candidate-packet-manifest.csv`: manifests for 1,588 HUST-OBC candidate packets across the 16 bucket directories. These packets are source-marked candidate metadata, not accepted oracle-character records.
- Bucket manifests named `000_hust-obc-promotion-bucket-manifest.csv`: 100-ID slices of the same HUST-OBC promotion queue under `corpus/001_oracle-characters/`. These files make review batches easier to locate, but they still do not assign formal IDs.

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
- `009_hust-obc-obs-char-promotion-review-queue.csv`：包含 1,588 个 HUST-OBC candidate class 的提升复核队列，并给出建议 `obs-char-*` ID。这些 ID 只是保留建议，经过跨来源复核前不是正式分配。
- `010_hust-obc-promotion-bucket-review-summary.csv`：16 个 HUST-OBC promotion bucket manifest 的批次级摘要。它帮助复核者和 AI Agent 选择复核批次，并保持“仅保留建议、未正式分配”的边界。
- `011_hust-obimd-evobc-codepoint-crosswalk-staging.csv`：从 HUST-OBC 提升候选到 OBIMD、EVOBC 数据集行的 metadata-only 码位交叉候选表。完全相同的 codepoint 只作为检索路线，不是已确认同字、释读、构件关系或演化链。
- 名为 `001_hust-obc-candidate-packet-manifest.csv` 的 bucket manifest：覆盖 16 个 bucket 目录中的 1,588 个 HUST-OBC 候选资料包。这些 packet 是带来源标记的候选 metadata，不是已接受的甲骨单字记录。
- 名为 `000_hust-obc-promotion-bucket-manifest.csv` 的 bucket manifest：位于 `corpus/001_oracle-characters/` 下，是同一 HUST-OBC 提升队列按 100 个 ID 切分的复核批次文件。这些文件便于定位分批审查，但仍不分配正式 ID。
