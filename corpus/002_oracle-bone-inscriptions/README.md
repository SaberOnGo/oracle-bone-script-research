# Oracle Bone Inscriptions / 甲骨卜辞

English:
This directory is the human entry point for oracle inscription records,
catalog crosswalk candidates, plate/text routes, and inscription-context
preprocessing. It helps researchers open the relevant registers, candidate
directories, source references, and review queues before any formal `obi-*`
inscription record is created.

简体中文：
本目录是甲骨卜辞记录、目录互证候选、图版/文本路线和卜辞语境
预处理的人类入口。研究者应先从这里打开登记表、候选对象目录、
来源引用和复核队列，再判断是否具备生成正式 `obi-*` 卜辞记录的
条件。

## Boundary / 边界

- Current Cambridge/Hopkins rows are crosswalk candidates.
- They are not formal `obi-*` inscription records.
- They are not transcriptions, readings, or decipherment conclusions.
- They are not a decipherment conclusion.
- They must be checked against plates, object records, Heji/OBM routes,
  source images, and later human review notes before promotion.
- 当前 Cambridge/Hopkins 行只是目录互证候选。
- 它们不是正式 `obi-*` 卜辞记录。
- 它们不是释文、读法或释读结论。
- 进入正式记录前，必须复核图版、馆藏对象、《合集》/OBM 路线、
  来源图像和后续人工复核记录。

## Main Registers / 主要登记表

- `000_inscription-registers/001_all-inscriptions-index.csv`
  will hold accepted project inscription records.
- `000_inscription-registers/002_cambridge-hopkins-crosswalk-staging.csv`
  stores 612 Cambridge/Hopkins finding-list crosswalk candidates.
- `000_inscription-registers/003_cambridge-hopkins-classified-summary.csv`
  summarizes 20 Cambridge/Hopkins topic and period groups.
- `000_inscription-registers/004_human-inscription-plate-presearch-map.md`
  records the current human-readable inscription and plate review gaps.
- `../009_statistics-and-derived-features/098_ai-agent-cambridge-hopkins-`
  `inscription-crosswalk-review-queue.csv`
  routes all 612 candidates into metadata-only human review.
- `../009_statistics-and-derived-features/195_inscription-plate-`
  `crosswalk-phase-gap-review-checklist.csv`
  lists phase-gap checks for inscription and plate crosswalk work.

## Opened Source-Record Candidate / 已打开来源记录候选

The first end-to-end source-record candidate is
[`obs-insc-src-cand-000001`][h2-candidate]. It preserves the OBIMD `H2`
rubbing and facsimile member routes, package and member checksums, seven
source-provided bounding boxes, and their order. The visual payloads remain
in ignored local-private archives because the effective rights status is
`metadata_only_until_verified`.

首个端到端打开的来源记录候选是
[`obs-insc-src-cand-000001`][h2-candidate]。它保存 OBIMD `H2` 的拓片、
摹本包成员路线、包级和成员校验和、七个来源字框及次序。
因有效权利状态为 `metadata_only_until_verified`，图像内容仍保留
在已忽略的本地私有归档中。

This candidate has no readable full transcription or OCR.
H2 is not a confirmed Heji 2, and its seven source UIDs are not confirmed
characters or
readings. It is not a formal `obi-*` record.

A second source-record candidate now captures the IHP Museum item 503 page
description. It records `R044498`, `Ping 0529`, the source phrase `帝令雨`,
and the missing plate, OCR, full-text, and character-link evidence. It remains
metadata-only and is not a formal `obi-*` record:
[`obs-insc-src-cand-000002`][ihp-503-candidate].

A third source-record candidate captures the IHP Museum item 1215 page,
including its short displayed text and three private image checksums. It
records `R044587`, the `Yi Bian` catalog label, and the missing independent
plate, OCR, and character-link evidence. It remains metadata-only and is not
a formal `obi-*` record: [`obs-insc-src-cand-000003`][ihp-1215-candidate].

第二个来源记录候选登记史语所 503 号页面说明，记录 `R044498`、`Ping 0529`、
来源短语 `帝令雨` 以及缺失的图版、OCR、全文和单字关联证据。它仍是仅元数据的
候选，不是正式 `obi-*` 记录：[`obs-insc-src-cand-000002`][ihp-503-candidate]。

该候选尚无可读卜辞全文或 OCR。`H2` 不是已确认的《合集》2，
七个来源 UID 也不是已确认字形或释读。它不是正式 `obi-*`
记录。

## What A Human Should Inspect / 人工应检查什么

- inscription number: candidate ID, Yingguo number, CUL number, Chalfant
  number, Heji number, OBM route, and any old catalog number.
- Text or OCR: full text, partial OCR, transcription route, or concrete
  next-check questions in the object-local human dossier.
- Plate and image: 图版号, source image path, plate/text route index,
  plate/text gallery, thumbnail status, and rights note.
- Bibliographic route: 著录来源, page or plate reference, cited source,
  and source-register row.
- Object context: collection object, museum or library record, findspot,
  excavation context, period, batch, and group.
- Character links: related glyph candidates, character-sequence evidence,
  component clues, variants, near forms, later-script relations, and missing
  character-context checks.
- Scholarship context: bibliography, cited catalog scope, proposer or
  reviewer notes, disputes, and disagreement routes.
- Review status: 复核状态, reviewer route, missing evidence, and the next
  human-gated action.

人工复核时，应逐项确认：

- 卜辞编号：候选 ID、《英国所藏甲骨集》号、CUL 号、Chalfant 号、
  《合集》号、OBM 路线，以及其他旧著录号。
- 全文或 OCR：是否已有全文、局部 OCR、释文路线，或在对象内
  人类档案中写成具体待查问题。
- 图版和图像：图版号、来源图像路径、图版/文本路线索引、图版/
  文本 gallery、缩略图状态和权利说明。
- 著录路线：著录来源、页码或图版引用、被引用来源和来源登记行。
- 对象语境：馆藏对象、博物馆或图书馆记录、出土地、发掘语境、
  时期、批次和组类。
- 字形关联：关联字形候选、字序证据，以及缺失的字形语境检查。
- 构件与关系：构件线索、异体、近形、金文、小篆、今字和后续
  关系路线。
- 学术语境：书目、著录适用范围、提出者、复核者说明、争议和
  不同意见路线。
- 复核状态：复核状态、复核者路线、缺失证据和下一步人工门控动作。

## Object-Local Files / 对象内文件

Each `obs-insc-cw-cand-*` candidate directory should keep human-readable
materials and structured support together in the same object directory.
Open the human files first:

- `README.md`: local candidate overview and boundary.
- `06_plate-text-gallery.md`: human-readable plate and text route gallery.
- `07_human-inscription-dossier.md`: human dossier for inspection.
- `09_inscription-plate-evidence-dossier.md`: human evidence dossier.
- `11_inscription-review-fact-matrix.md`: human fact matrix.
- `04_human-review-sheet.md`: human checklist.
- `21_character-inscription-linkage-review.md`: human review of evidence
  required before linking a character occurrence.

Structured support files serve the human dossier and review trail:

- `01_candidate-inscription-crosswalk-packet.json`: support packet.
- `02_crosswalk-source-index.csv`: source and crosswalk references.
- `03_catalog-reference-index.csv`: catalog-number support table.
- `05_plate-text-route-index.csv`: plate and text support table.
- `08_inscription-dossier-index.json`: support index for the dossier.
- `10_inscription-plate-evidence-index.json`: support evidence index.
- `12_inscription-review-fact-matrix-index.json`: support fact index.
- `22_character-inscription-linkage-index.json`: support index for the
  character-linkage review.

## Concrete Questions To Check / 具体待查问题

- Which candidate lacks a Heji, CUL, Chalfant, OBM, or source-image route?
- Which candidate has a catalog number but no object or plate evidence yet?
- Which candidate has only metadata and no text/OCR or plate image?
- Which candidate needs comparison with a collection object before `obi-*`
  assignment can even be considered?
- Which dossier records period, batch, or group only as a source hint?
- Which missing item blocks further human review most directly?
- 哪个候选还缺《合集》、CUL、Chalfant、OBM 或来源图像路线？
- 哪个候选只有著录号，还没有对象或图版证据？
- 哪个候选只有 metadata，没有全文/OCR 或图版图像？
- 哪个候选必须先和馆藏对象比对，才可考虑是否进入 `obi-*`？
- 哪个档案中的时期、批次或组类仍只是来源线索？
- 哪个缺失项最直接阻断下一步人工复核？

## Suggested Review Order / 建议复核顺序

1. Open the candidate row in `002_cambridge-hopkins-crosswalk-staging.csv`.
2. Open the matching `obs-insc-cw-cand-*` object directory.
3. Read `07_human-inscription-dossier.md` before the JSON packet.
4. Check `05_plate-text-route-index.csv` and `06_plate-text-gallery.md`.
5. Compare catalog references with Heji, OBM, and collection-object routes.
6. Record only reviewed route outcomes in the matching review scaffold.
7. Do not create a formal `obi-*` record until evidence review justifies it.

## Regeneration Notes / 再生成说明

Object-local inscription crosswalk materials are generated by:

- `tools/002_corpus-import/build_cambridge_hopkins_inscription_crosswalk_`
  `materials.py`

When inscription routes, candidate dossiers, or review queues change, rerun
the relevant builder, then run repository validation and tests before
committing.

[h2-candidate]: 008_source-record-candidates/
  001_obs-insc-src-cand-000001_obimd-h2_source-record-candidate/README.md
[ihp-503-candidate]: 008_source-record-candidates/
  002_obs-insc-src-cand-000002_ihp-item-503_source-record-candidate/README.md
[ihp-1215-candidate]: 008_source-record-candidates/
  003_obs-insc-src-cand-000003_ihp-item-1215_source-record-candidate/README.md
