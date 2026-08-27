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
- `000_inscription-registers/005_opened-source-record-candidate-guide.md`
  is the human-first queue for the ten opened source-record candidates.
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

A fourth source-record candidate captures the IHP Museum item 771 page and
its source-reported proposed divination. It records `R039275+R043001`,
`I 5867+8202`, three private image checksums, and the missing independent
plate, original text, OCR, and character-link evidence. It remains
metadata-only and is not a formal `obi-*` record:
[`obs-insc-src-cand-000004`][ihp-771-candidate].

A fifth source-record candidate captures the British Library Or. 7694/1595
recto and verso images supplied through Wikimedia Commons. It records the
accession sides, Heji and Yingguo reference hints, two image checksums, and
the page-displayed eclipse strings. The images are marked CC0 on their file
pages, but catalog and text claims remain source-reported and unverified:
[`obs-insc-src-cand-000005`][bl-1595-candidate].

A sixth source-record candidate captures the British Library Or. 7694/1535v
image route. It records the source-displayed Heji 39498v and Yingcang 1117v
hints, one image checksum, direct visual observations, and concrete catalog
and text gaps. The Commons image page reports CC0, but the object identity,
catalog placement, and text remain source-reported and unverified:
[`obs-insc-src-cand-000006`][bl-1535-candidate].

A seventh source-record candidate compares a Wikimedia Commons photograph,
Schwartz 2019, Li 2024, and an OBIMD `HD421` plate scan. Plate 383 prints
`421` and `H3:1325`; its distinctive contour, holes, fracture mosaic, seams,
and two inscription clusters match the photograph. This supports a
high-confidence object-identity candidate, while the conflicting dimensions,
physical edition provenance, and museum accession remain open:
[`obs-insc-src-cand-000007`][ningxia-hyz421-candidate].

An eighth source-record candidate captures The Met Open Access object 42045,
accession `67.43.14`. It preserves two public image files, API metadata,
checksums, and direct visual observations. It has no OCR, plate locator,
Heji reference, or character assignment, and remains a source-record
candidate rather than a formal `obi-*` record:
[`obs-insc-src-cand-000008`][met-42045-candidate].

A ninth source-record candidate captures The Met Open Access object 42022,
accession `18.56.71`. It preserves two public image files, API metadata,
checksums, and direct visual observations. It has no OCR, plate locator,
Heji reference, or character assignment, and remains a source-record
candidate rather than a formal `obi-*` record:
[`obs-insc-src-cand-000009`][met-42022-candidate].

A tenth source-record candidate opens IHP Museum item 1222, accession
`ZR038421`. It binds two official page snapshots, two large-image responses,
three rendered glyph responses, checksums, and fragmentary source display.
Catalog plates, sign locations, transcription history, disputes, and reuse
terms remain unresolved:
[`obs-insc-src-cand-000010`][ihp-1222-candidate].

第二个来源记录候选登记史语所 503 号页面说明，记录 `R044498`、`Ping 0529`、
来源短语 `帝令雨` 以及缺失的图版、OCR、全文和单字关联证据。它仍是仅元数据的
候选，不是正式 `obi-*` 记录：[`obs-insc-src-cand-000002`][ihp-503-candidate]。

该候选尚无可读卜辞全文或 OCR。`H2` 不是已确认的《合集》2，
七个来源 UID 也不是已确认字形或释读。它不是正式 `obi-*`
记录。

第四个来源记录候选保存史语所博物馆 771 号页面及其来源拟译。它记录
`R039275+R043001`、`I 5867+8202`、三份私有图像校验和，以及尚缺的独立图版、
原始文字、OCR 和单字关联证据。它仍是 metadata-only，不是正式 `obi-*` 记录：
[`obs-insc-src-cand-000004`][ihp-771-candidate]。

第五个来源记录候选保存大英图书馆 Or. 7694/1595 正反面图像，图像由
Wikimedia Commons 提供。它记录正反面藏品号、合集和英国所藏线索、两张
图像校验和以及页面显示的月食文字。图像页面标为 CC0，但著录与文字
主张仍是来源报告、尚未独立核验：
[`obs-insc-src-cand-000005`][bl-1595-candidate]。

第六个来源记录候选保存大英图书馆 Or. 7694/1535v 的图像路线，记录
页面显示的 Heji 39498v、Yingcang 1117v 线索、一张图像校验和、直接
视觉观察以及具体著录和文字缺口。Commons 图像页标为 CC0，但对象身份、
著录定位和文字仍是来源报告、尚未独立核验：
[`obs-insc-src-cand-000006`][bl-1535-candidate]。

第七个来源记录候选对照 Wikimedia Commons 照片、Schwartz 2019、李延彦
2024 与 OBIMD `HD421` 图版扫描。图版 383 印有 `421`、`H3:1325`，其外轮廓、
孔位、裂缝网、长接缝和两组刻辞均与照片匹配，支持高置信对象身份候选。
尺寸冲突、物理版本来源和馆藏号仍未解决：
[`obs-insc-src-cand-000007`][ningxia-hyz421-candidate]。

第八个来源记录候选保存大都会艺术博物馆 Open Access 对象 42045，馆藏号
为 `67.43.14`。它保存两张公开图像、API metadata、校验和与直接视觉观察，
但没有 OCR、图版定位、合集号或单字分配，仍是来源记录候选而非正式
`obi-*` 记录：[`obs-insc-src-cand-000008`][met-42045-candidate]。

第九个来源记录候选保存大都会艺术博物馆 Open Access 对象 42022，馆藏号
为 `18.56.71`。它保存两张公开图像、API metadata、校验和与直接视觉观察，
但没有 OCR、图版定位、合集号或单字分配，仍是来源记录候选而非正式
`obi-*` 记录：[`obs-insc-src-cand-000009`][met-42022-candidate]。

第十个来源记录候选打开史语所博物馆 1222 号对象，馆藏号为 `ZR038421`。
它绑定两份官方页面快照、两份大图响应、三份页面渲染字形响应、校验和与
残缺来源文字。著录图版、字形位置、释读史、争议和再利用条款仍未解决：
[`obs-insc-src-cand-000010`][ihp-1222-candidate]。

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
[ihp-771-candidate]: 008_source-record-candidates/
  004_obs-insc-src-cand-000004_ihp-item-771_source-record-candidate/README.md
[bl-1595-candidate]: 008_source-record-candidates/
  005_obs-insc-src-cand-000005_bl-or-1595_source-record-candidate/README.md
[bl-1535-candidate]: 008_source-record-candidates/
  006_obs-insc-src-cand-000006_bl-or-1535_source-record-candidate/README.md
[ningxia-hyz421-candidate]: 008_source-record-candidates/
  007_obs-insc-src-cand-000007_ningxia-hyz421_source-record-candidate/README.md
[met-42045-candidate]: 008_source-record-candidates/
  008_obs-insc-src-cand-000008_met-42045_source-record-candidate/README.md
[met-42022-candidate]: 008_source-record-candidates/
  009_obs-insc-src-cand-000009_met-42022_source-record-candidate/README.md
[ihp-1222-candidate]: 008_source-record-candidates/
  010_obs-insc-src-cand-000010_ihp-item-1222_source-record-candidate/README.md
