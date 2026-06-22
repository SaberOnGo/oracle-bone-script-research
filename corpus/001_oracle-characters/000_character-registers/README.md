# Character Registers / 甲骨字索引

English:
Register files index character records, staging candidates, source mappings,
review queues, and generated bucket manifests.

## Human Reading Order / 人工阅读顺序

1. Open `001_all-oracle-characters-index.csv` for accepted project character
   records.
2. Open `002_deciphered-oracle-characters-index.csv` for accepted deciphered
   project character records.
3. Open `003_undeciphered-oracle-characters-index.csv` for the 9,408
   HUST-OBC metadata-only undeciphered candidates.
4. Use `004_character-id-assignment-log.md` before treating any staging ID as
   a formal project ID.
5. Use `009_hust-obc-obs-char-promotion-review-queue.csv` only as a review
   queue of reserved suggestions.

## Staging And Review Files / 暂存与复核文件

- `005_hust-obc-validation-class-staging.csv`
- `006_obimd-main-character-staging.csv`
- `007_hust-obc-validation-label-crosswalk-staging.csv`
- `008_hust-obc-source-category-staging.csv`
- `010_hust-obc-promotion-bucket-review-summary.csv`
- `011_hust-obimd-evobc-codepoint-crosswalk-staging.csv`

## Undeciphered Candidate Routes / 未释字候选路线

The 9,408 `obs-unk-*` rows are metadata-only routes. They preserve source class
paths, image-count clues, packet locations, bucket manifests, and rights notes.
They do not assign formal `obs-char-*` IDs and do not make decipherment claims.

AI context packs and review queues under
`corpus/009_statistics-and-derived-features/` support retrieval and routing.
They are auxiliary indexes, not replacements for object-local human dossiers.

## Boundary / 边界

No register in this directory creates a new accepted character identity by
itself. Formal records require cross-source review, source evidence, and
human-readable documentation inside the concrete object directory.

简体中文:
本目录登记甲骨字记录、暂存候选、来源映射、复核队列和生成的分桶
manifest。

## 人工阅读顺序 / Human Reading Order

1. 先打开 `001_all-oracle-characters-index.csv`，查看已接受的项目
   单字记录。
2. 再打开 `002_deciphered-oracle-characters-index.csv`，查看已接受的
   已释读项目单字记录。
3. 打开 `003_undeciphered-oracle-characters-index.csv`，查看 9,408 个
   HUST-OBC metadata-only 未释字候选。
4. 在把任何暂存 ID 当作正式项目 ID 前，先读
   `004_character-id-assignment-log.md`。
5. `009_hust-obc-obs-char-promotion-review-queue.csv` 只能作为保留建议
   的复核队列使用。

## 暂存与复核文件 / Staging And Review Files

- `005_hust-obc-validation-class-staging.csv`
- `006_obimd-main-character-staging.csv`
- `007_hust-obc-validation-label-crosswalk-staging.csv`
- `008_hust-obc-source-category-staging.csv`
- `010_hust-obc-promotion-bucket-review-summary.csv`
- `011_hust-obimd-evobc-codepoint-crosswalk-staging.csv`

## 未释字候选路线 / Undeciphered Candidate Routes

9,408 条 `obs-unk-*` 记录只是 metadata-only 路线。它们保存来源分类
路径、图像数量线索、packet 位置、bucket manifest 和权利说明。它们
不分配正式 `obs-char-*` ID，也不提出释读结论。

`corpus/009_statistics-and-derived-features/` 下的 AI context pack 和
复核队列只辅助检索与路线定位。它们不是对象目录内人类档案的替代品。

## 边界 / Boundary

本目录中的任何 register 都不能单独创建新的已接受单字身份。正式记录
需要跨来源复核、来源证据，以及具体对象目录内的人类可读文档。
