# Statistics And Derived Features / 统计与派生特征

English:
This directory is the human entry point for generated statistics, coverage
audits, route packs, review queues, and source-processing scaffolds. These
files help researchers find what has been prepared, what still needs review,
and which source or object route should be opened next.
The statistics are navigation signals for opening evidence routes, not
substitutes for object-local dossiers, source records, or review sheets.

简体中文：
本目录是统计、覆盖审计、路线包、复核队列和来源处理脚手架的人类入口。
这些文件帮助研究者判断哪些资料已经预处理，哪些仍需复核，以及下一步
应打开哪个来源、对象或证据路线。
这些统计只是帮助打开证据路线的导航信号，不能替代对象内档案、
来源记录或人工复核表。

## Boundary / 边界

- These files are preprocessing and navigation evidence only.
- The statistics are navigation signals, not source or object evidence.
- They are not source evidence by themselves.
- They are not rights decisions or source-promotion decisions.
- They are not corpus imports or reviewed scholarly outcomes.
- They are not a decipherment conclusion.
- 这些文件只属于预处理和导航证据。
- 统计只是导航信号，不是来源证据或对象证据。
- 它们本身不是来源证据、权利裁定或来源提升决定。
- 它们不是语料导入结果，也不是已复核学术结论。
- 它们不构成释读结论。

## Main Human Entry Points / 主要人工入口

- `090_preprocessing-status-audit.csv`
  records high-level preprocessing status rows.
- `094_source-processing-pipeline-audit.csv`
  audits source-processing coverage and next entrances.
- `095_source-processing-pipeline-summary.json`
  summarizes the source-processing pipeline audit.
- `132_ai-agent-source-pipeline-gap-matrix.csv`
  groups per-source preprocessing gaps for human review.
- `133_ai-agent-source-pipeline-gap-review-checklist.csv`
  lists source-level review checks that still need people.
- `134_ai-agent-source-pipeline-evidence-ledger.csv`
  records per-source preprocessing evidence counts and route files.
- `135_core-corpus-phase-coverage-matrix.csv`
  summarizes phase coverage for core corpus areas.
- `136_source-pipeline-phase-coverage-matrix.csv`
  records source-level phase coverage and missing phases.
- `137_source-pipeline-phase-action-queue.csv`
  turns missing source phases into pending review actions.
- `188_object-local-material-coverage-audit.csv`
  audits object-local material coverage for human and AI files.
- `189_object-local-material-coverage-summary.json`
  summarizes object-local coverage counts and boundaries.
- `190_project-id-source-map-audit.csv`
  audits project-local ID to source-reference maps.
- `191_project-id-source-map-summary.json`
  summarizes project ID map coverage and issue counts.
- `213_core-corpus-phase-gap-human-review-guide.md`
  gives a human-readable guide before opening the 192-212 route tables.
- `214_inscription-plate-crosswalk-phase-gap-human-guide.md`
  gives a human-readable guide for inscription and plate phase gaps.
- `217_published-research-note-phase-gap-human-guide.md`
  gives a human-readable guide for published research note gaps.
- `218_character-candidate-phase-gap-human-guide.md`
  gives a human-readable guide for character candidate phase gaps.
- `219_shape-component-evolution-phase-gap-human-guide.md`
  gives a human-readable guide for shape, component, and evolution gaps.

## File Families / 文件族

### Relationship Graph Statistics / 关系图统计

- `001` to `003` summarize graph edge types, node degree, and AI context.
- Use them to find graph coverage and graph-derived routing clues.
- Do not treat graph edges as component, identity, or evolution conclusions.

### Source Route Review / 来源路线复核

- `007` to `015` cover source coverage, route queues, and metadata results.
- Use them to find source register, download log, package, and graph routes.
- They are metadata-only review surfaces, not source promotion.

### Evidence Collection Scaffolds / 证据收集脚手架

- `016` to `039` split source evidence work into not-collected tasks.
- Use them to plan source-register, download-log, package, and rights review.
- Empty scaffold rows must stay empty until a later human review pass.

### Cross-Source And Candidate Queues / 跨来源与候选队列

- `040` to `089` route HUST-OBC, OBIMD, EVOBC, Xiaoxuetang, and OBM checks.
- Use them to find candidate packets, source rows, and download evidence.
- They do not confirm identity, readings, components, or evolution chains.

### Source Engineering Pipeline / 来源工程流水线

- `094` to `185` organize source-processing gaps, actions, handoffs,
  checklists, outcome scaffolds, and route summaries.
- Use them to continue preprocessing before any source is promoted.
- Rights, import, source promotion, and evidence outcomes remain human-gated.

### Object-Local And Project-ID Coverage / 对象内与 ID 覆盖

- `186` to `191` audit object-local material bundles and ID-source maps.
- Use them to check whether concrete object directories have human entries,
  AI packets, route galleries, source indexes, and no parallel human folders.

### Core Corpus Phase Gap Review / 核心语料阶段缺口复核

- `192` to `219` route missing or partial preprocessing phases.
- Use `214` to `219` as human-readable entrances into object dossiers,
  sources, inscriptions, plates, published notes, candidates, components,
  and evolution/correspondence candidates.
- Do not treat these guides or checklists as reviewed outcomes.
- These audits show readiness signals, not scholarly truth.

### Human Phase-Gap Guide / 人工阶段缺口指南

- `213` summarizes the 192-212 phase-gap review routes in Markdown.
- Open it before using the CSV or JSON route tables for phase-gap review.
- It is a human reading guide, not a reviewed outcome or import decision.
- `216` specializes the 193 research-source phase gap checklist.
- Open it before using source-pipeline assignment or outcome routes.
- It is not a rights decision, source promotion, or corpus import approval.
- `217` specializes the 197 published research note checklist.
- Open it before promoting any bibliography, web, database, or draft note.
- It is not draft promotion, corpus import approval, or scholarship.
- `218` specializes the 198 character candidate phase gap checklist.
- Open it before any character or undeciphered candidate promotion review.
- It is not candidate promotion, character import, or identity confirmation.
- `214` specializes the 195 inscription and plate crosswalk checklist.
- Open it before using inscription plate route tables or review queues.
- It is not a formal `obi-*` record or decipherment conclusion.
- `215` specializes the 194 collection provenance checklist.
- Open it before using collection, object-map, asset, or rights routes.
- It is not a rights decision, source promotion, or identity claim.

Use this guide to return each phase gap to concrete research evidence:
glyph images, rubbings, photographs, plates, inscription text, OCR, catalog
numbers, collection numbers, findspot, collection, period, group, batch,
component, variant, near-form, bronze, seal, modern-form, bibliography,
reading history, proposer, different opinions, and disputes.

使用本指南时，应把每个阶段缺口回到具体研究证据：字形图像、拓片、
照片、图版、卜辞全文、OCR、著录号、合集号、出土地、馆藏、时期、
组类、批次、构件、异体、近形、金文、小篆、今字、书目、释读史、
提出者、不同意见和争议。

## Concrete Questions To Check / 具体待查问题

- Which source or corpus area has the largest remaining preprocessing gap?
- Which object directory lacks a human-readable local research entrance?
- Which source needs access, checksum, package manifest, or rights review?
- Which route file should a human open before collecting new evidence?
- Which generated queue is still only an empty scaffold?
- Which rows are metadata-only and must not be promoted into scholarship?
- Which statistics should be regenerated after object-local materials change?
- 哪个来源或语料区仍有最大的预处理缺口？
- 哪个对象目录还缺人类可读的本地研究入口？
- 哪个来源还需要访问、checksum、package manifest 或权利复核？
- 人工收集新证据前，应先打开哪一个路线文件？
- 哪个生成队列仍只是空脚手架？
- 哪些行只是 metadata，不能提升为学术结论？
- 对象内资料改变后，哪些统计文件需要重新生成？

## Human Research Entry Order / 人工研究入口顺序

1. Open `189_object-local-material-coverage-summary.json`.
2. Open `188_object-local-material-coverage-audit.csv`.
3. Open `135_core-corpus-phase-coverage-matrix.csv`.
4. Open `136_source-pipeline-phase-coverage-matrix.csv`.
5. Open `137_source-pipeline-phase-action-queue.csv`.
6. Follow the cited source register, object directory, or route pack.
7. Record reviewed outcomes only in the matching result scaffold or log.
8. Use a human-fillable outcome scaffold only after source routes are checked.

人工阅读时，先看覆盖摘要，再打开审计表和阶段矩阵。遇到缺口时，
回到对应的来源登记、对象目录或路线包；只有证据路线已经核对后，
才在人工可填写的 outcome scaffold 或日志中记录复核结果。

## Regeneration Notes / 再生成说明

Many files in this directory are generated by scripts under:

- `tools/003_graph-generation/`
- `tools/004_statistics-generation/`
- `tools/005_ai-context-pack-builder/`

When generated statistics or scaffolds change, rerun the matching builder,
then run repository validation and tests before committing.
