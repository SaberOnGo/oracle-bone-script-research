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

## 2026-11-02 标签更正 / Label Correction

简体中文：
`007`、`008`、`011` 三张表中的 HUST-OBC 今字标签全部错误，已被
`012_hust-obc-official-deciphered-labels.csv` 取代。原因是早期流程把
已释字类号（如 `0001`）接到了 HUST-OBC OCR 子数据集的字表
`OCR/ID_to_Chinese.json`（如 `00001`），两者是不同的编号体系。结果是
1,781 个类全部被标成部首区和扩展 A 区的字，例如 0001 类被写作"⺀"。

正确的对照表是 HUST-OBC 原始包中的
`HUST-OBC/deciphered/ID_to_chinese.json`（SHA-256
`f1ac067eae3092d0bf738e9285cd86ac54a57e6d46deb147b87908b1c9eadd34`），
其中 1,563 个是常用汉字，例如 0100 类是"丹"、0111 类是"九"。用正确标签
重算后，1,294 个已释类能对上 OBIMD 主字表，1,579 个能对上 EvoBC。

旧表保留作历史记录，不要再用其中的标签和码位对照。

English:
The HUST-OBC labels in registers `007`, `008`, and `011` are all wrong and are
superseded by register `012`. The earlier pipeline joined deciphered category
IDs to the OCR sub-dataset table, a different ID space. The correct table is
`HUST-OBC/deciphered/ID_to_chinese.json` in the raw package.

## 多字形类的隶定冲突 / Classes With Conflicting OBIMD Transcriptions

2026-11-05 核查：35 个 HUST-OBC 类对应的 OBIMD 字形中，至少一个的隶定与类标签不同（统计表 `corpus/002_oracle-bone-inscriptions/010_inscription-texts/002_obimd-glyph-occurrence-stats.csv`）。档案的字例计数与例句只取隶定与标签相同的字形；标签不匹配的类不写字例。这些类的标签与 OBIMD 隶定的关系未经文献核对，常见情形有三种：同形异字（如 0508 子 / 0609 巳 / 0815 月夕）、异体或繁简（0479 姬姫、0982 溫）、OBIMD 把字形隶定为另一字（1667 鼎 的两个字形分别为“貞”6,460 例和“鼎”13 例；0155 侑 / 0302 又右 / 0817 有 / 1170 祐 共用“㞢”和“佑”）。

Checked on 2026-11-05: 35 HUST-OBC classes map to an OBIMD glyph whose transcription differs from the class label. Dossiers count only glyphs whose transcription matches the label. The relation between label and transcription is unverified against scholarship; list the class numbers 0155, 0249, 0273, 0292, 0302, 0349, 0357, 0436, 0452, 0479, 0496, 0508, 0609, 0618, 0628, 0714, 0814, 0815, 0817, 0893, 0982, 0995, 1085, 1098, 1100, 1101, 1123, 1170, 1184, 1261, 1504, 1520, 1552, 1667, 1682.

## 013 小学堂底座（100 字）/ Xiaoxuetang Base For 100 Characters

`013_xiaoxuetang-base-100.csv` 列出第 5 步试点的 100 个已释字：按 OBIMD 字例数（只计隶定与标签相同的字形）排序取前 100，并在对应档案第 8 节补入小学堂甲骨文库的字号、字形数、旧著录样例、合集号样例、类组和《甲骨文字詁林》册页。2026-11-05 更正计数后换入 8 个字。释读史（提出者、年份、著作、页码）仍为空，诂林册页只是定位，未核对。

`013_xiaoxuetang-base-100.csv` lists the 100 deciphered characters of the step-5 pilot, ranked by OBIMD occurrences (matching transcriptions only). Reading histories are still empty; the Guilin page numbers are unverified pointers.
