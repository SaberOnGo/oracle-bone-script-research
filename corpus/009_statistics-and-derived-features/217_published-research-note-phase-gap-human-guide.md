# Published Research Note Phase Gap Human Guide /
已发表研究笔记阶段缺口人工复核指南

English:
This guide is the human entrance for published-research-note
preprocessing gaps. It sends reviewers back to opened
source-object dossiers, bibliography notes, published scholarship
review rules, and the boundary between
`research/` and `doc/public/user_research/`.
The reviewer should ask what human evidence the note can support:
glyph_image, components, excavation context, collection context,
relations, citation history, proposer, disagreement, and dispute.
It is not a rights decision, not draft promotion,
not corpus import approval, not confirmed scholarship,
and not a decipherment conclusion.

简体中文：
本指南是已发表研究笔记阶段缺口的人工复核入口。
复核者应回到已打开的来源对象档案、书目笔记、
已发表研究复核规则，以及 `research/` 与
`doc/public/user_research/` 的边界。
先问这条笔记能支持哪些人类证据：glyph_image、components、
excavation context、collection context、relations、引用史、
提出者、不同意见和争议。
它不是权利决定，不是草稿提升，不是语料导入批准，
不是已确认学术结论，也不是释读结论。

## Summary / 摘要

- updated at: 2026-06-30
- checklist rows: 4
- research note files: 7
- user or AI draft review files: 122
- source register files: 522
- source index rows: 21
- phase gap statuses:
  - extracted: `mixed_or_partial`
  - cleaned: `mixed_or_partial`
  - linked: `mixed_or_partial`
  - verified: `missing`

## Human Review Entry Order / 人工复核入口顺序

1. Open the source-object dossier first.
2. Open its human README and material access index.
3. Open `002_published-scholarship-review-guide.md`.
4. Open the 197 published research note checklist.
5. Open the 192 core corpus phase action queue.
6. Open `001_all-sources-index.csv`.
7. Open the related `research/` note only as reviewed context.
8. Open `doc/public/user_research/` only as draft context.
9. Compare draft wording against opened source evidence.
10. Record unresolved items as concrete next checks.
11. Keep any unreviewed draft outside `research/`.
12. Do not move user or AI drafts into `research/`
    until a human rewrites them from opened source evidence.

人工复核时，先打开来源对象档案，再看人类 README、
资料访问索引和已发表研究复核指南。
索引和 draft 只能帮助定位材料，不能替代来源证据。
未复核草稿必须留在 `doc/public/user_research/`。

## Support Files / 辅助文件

- statistics directory:
  `corpus/009_statistics-and-derived-features/`
- checklist:
  `197_published-research-note-phase-gap-review-checklist.csv`
- action queue:
  `192_core-corpus-phase-gap-action-queue.csv`
- source register directory:
  `corpus/006_research-sources-and-bibliography/`
  `000_source-registers/`
- source index:
  `001_all-sources-index.csv`
- source objects:
  `corpus/006_research-sources-and-bibliography/001_source-objects`
- research notes: `research/`
- user or AI drafts: `doc/public/user_research/`
- scholarship review directory:
  `research/001_published-scholarship-index/`
- scholarship review guide:
  `002_published-scholarship-review-guide.md`

Open these files after the relevant human source dossier.
They are pointers for review, not reviewed evidence by themselves.

## Required Human Content / 必须人工核对的内容

- bibliographic identity
- source trail
- scope
- evidence level
- citation relation
- reading process status
- proposer and disagreement
- dispute record
- review status

Each note must keep these items human-readable.
Do not replace them with field names, data files, or empty status.
每条笔记都应把这些项目写成人可读内容。
不得用字段名、数据文件或空状态替代人工档案。

## Research Evidence Slots / 研究证据槽位

- glyph_image evidence: image, rubbing, photo, plate, and asset path
- glyph observation: strokes, outline, damage, uncertainty
- components: visible component clues and near-form comparisons
- inscription context: text, OCR, divination context, and plate
- excavation context: findspot, collection, period, group, batch
- relations: citation, derivation, dispute, and later-form links
- bibliography: author, title, venue, year, page, and catalog number
- missing items: exact source, page, plate, or object still pending

这些槽位先服务甲骨文学和考古研究者打开证据，
然后才服务后续索引、统计和追溯。

## Source Trail Fields / 来源链字段

- `source_object_id`
- `source_register_row`
- `access_or_download_route`
- `checksum`
- `file_size`
- `manifest`
- `derived_path`
- `rights_status`
- `risk_note`
- `review_status`

The source trail must be visible before any note is rewritten.
来源链必须先可见，才能改写为研究笔记。

## Concrete Questions To Check / 具体待查问题

- Which source object and register row prove this bibliography item?
- Which page, plate, URL, catalog number, or object record locates it?
- Which checksum, file size, manifest, or field map supports the route?
- Which corpus object can this source actually support?
- What evidence level is justified by the opened source?
- Who is the proposer, and where is the proposal recorded?
- Which disagreement or dispute is documented, and where?
- Which user or AI draft must stay outside `research/` until reviewed?
- What exact source must be opened before any note can be promoted?
- Which proposer, disagreement, or dispute is named in the source?
- Which page or catalog evidence should be opened next?
- Which reviewed source fact can be written in human prose?
- Which exact missing source keeps this note pending?
- Which glyph_image, component, excavation, or relation evidence
  can a researcher inspect directly?
- Which bibliography claim is only a reported reading history?
- 哪个提出者、不同意见或争议已经在来源中具名？
- 下一步应打开哪一页、图版、著录号或对象记录？
- 哪条已复核来源事实可以改写成人类研究笔记？
- 还缺哪一个具体来源，使本条笔记只能保持待查？
- 哪条 glyph_image、components、excavation 或 relations 证据
  可以让研究者直接查看？
- 哪个书目说法只是被报道的释读史，而不是结论？

## Boundary / 边界

Do not record reviewed outcomes in this guide.
Do not treat a checklist row, route path, source index row,
draft paragraph, OCR line, data packet, or graph edge as scholarship.
Do not decide rights.
Do not promote drafts.
Do not import corpus records.
Do not write any row as confirmed scholarship.
Do not write any row as a decipherment conclusion.

不得在本指南中记录复核结论。
不得把清单行、路线、来源索引行、草稿段落、OCR 行、
data packet 或图边当成学术结论。
不得裁定权利，不得提升草稿，不得导入正式语料记录。
不得把任何一行写成已确认学术结论或释读结论。
