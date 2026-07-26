# Research Source Phase Gap Human Guide /
研究来源阶段缺口人工复核指南

English:
This guide is the human entrance for research-source
preprocessing phase gaps. It sends reviewers from the phase
queue back to source-object dossiers, source registers,
download logs, package manifests, field maps, extraction
notes, rights notes, risk notes, and safe derived records.
Each source must be checked for the human evidence it can
support: glyph_image, inscription text, components, excavation
context, collection context, relations, and bibliography.
It is not a rights decision, not source promotion,
not corpus import approval, not confirmed scholarship,
and not a decipherment conclusion.

简体中文：
本指南是研究来源预处理阶段缺口的人工入口。
复核者应从阶段缺口回到来源对象档案、来源登记、
下载日志、package manifest、字段映射、抽取说明、
权利说明、风险提示和安全派生记录。
它不是权利决定，不是来源提升，不是语料导入批准，
不是已确认学术结论，也不是释读结论。

## Summary / 摘要

- updated at: 2026-06-30
- checklist rows: 5
- assignment groups: 0
- assignment source ids: 0
- pipeline gap statuses:
- downloaded: `mixed_or_partial`
- unpacked: `mixed_or_partial`
- extracted: `mixed_or_partial`
- cleaned: `mixed_or_partial`
- verified: `mixed_or_partial`

## Human Review Entry Order / 人工复核入口顺序

1. Open the source-object dossier first.
2. Open the source-object `README.md`.
3. Open `07_material-access-index.md`.
4. Open `01_source-packet.json` only after the human file.
5. Open `193_research-source-phase-gap-review-checklist.csv`.
6. Open the matching 185 assignment checklist row.
7. Open the all-sources index and large-source register.
8. Check access or download record, date, and provider.
9. Check source system, provider, catalog, book, paper, museum, or URL.
10. Check package name, file size and checksum.
11. Check package manifest, field map, extraction note.
12. Check rights status, risk note, and public-commit decision.
13. Check glyph_image, inscription, and collection evidence.
14. Check components, excavation context, relations, literature.
15. Check derived paths and safe derived records.
16. Record reviewed outcomes only in the matching result log.

人工复核时，先打开来源对象目录内的人类可读说明，
再打开物料访问索引、来源 packet、阶段缺口清单、
185 分配清单、来源总索引和大型来源登记。
缺失项必须写成具体待查问题，不得写成空泛状态。

## Support Files / 辅助文件

| File | Path |
| --- | --- |
| checklist | `corpus/009_statistics-and-derived-features/193_research-source-phase-gap-review-checklist.csv` |
| action queue | `corpus/009_statistics-and-derived-features/192_core-corpus-phase-gap-action-queue.csv` |
| assignment checklist | `corpus/009_statistics-and-derived-features/185_source-pipeline-missing-evidence-outcome-routes-assignment-checklist.csv` |
| source index | `corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv` |
| source objects | `corpus/006_research-sources-and-bibliography/001_source-objects` |
| large source register | `project_registry/006_large-source-register/001_large-source-register.csv` |
| download log | `project_registry/006_large-source-register/002_source-download-log.csv` |

Use these files after opening a source-object human dossier.
They are support pointers, not reviewed evidence by themselves.

## Concrete Questions To Check / 具体待查问题

- Which source object and source id are being reviewed?
- Which source system, provider, catalog, book, paper, museum,
  or URL supplied the source?
- Which access or download record, access date, package name,
  file size and checksum locate it?
- Which source package, manifest, field map, extraction note,
  and derived paths let a reviewer audit it?
- Which rights status, risk note, and public-commit decision
  are visible beside the source?
- Which glyph_image, inscription text, or plate evidence
  can a human researcher inspect from this source?
- Which components, variants, or near-form comparisons
  can this source support without becoming a conclusion?
- Which excavation, findspot, collection, period, or batch
  evidence is present or still missing?
- Which relations, citation links, bibliography notes,
  proposer records, or disputes can this source support?
- Which safe derived record or object-local dossier can be opened?
- Which missing source, license, checksum, field, or review status
  remains before an outcome can be recorded?
- Which assignment group still has empty outcome slots by design?
- 正在复核哪一个来源对象和来源 ID？
- 哪个来源系统、提供者、著录、图书、论文、博物馆或 URL
  提供了这个来源？
- 哪条访问或下载记录、访问日期、来源包名、文件大小和
  checksum 能够定位它？
- 哪个来源包、manifest、字段映射、抽取说明和派生路径
  能让复核者审计它？
- 来源旁边是否已有权利状态、风险提示和公开提交决定？
- 这个来源能让人检查哪条 glyph_image、卜辞文本或图版证据？
- 这个来源能支持哪些构件、异体或近形比较而不变成结论？
- 哪些出土、地点、馆藏、时期或批次证据存在或仍缺失？
- 这个来源能支持哪些关系、引用、书目、提出者或争议记录？
- 哪条安全派生记录或对象内档案可以直接打开？
- 记录结果前，还缺哪个来源、许可、checksum、字段或状态？
- 哪个分配组按设计仍保留空 outcome 栏位？

## Boundary / 边界

Do not record reviewed outcomes in this guide.
Do not treat a checklist row, assignment group, source packet,
manifest pointer, field-map pointer, or graph edge as scholarship.
Do not decide rights, promote sources, or import corpus records.
This guide is not corpus import approval.
This guide is not confirmed scholarship.
It is not a decipherment conclusion.

不得在本指南中记录复核结论。
不得把清单行、分配组、来源 packet、manifest 路线、
字段映射路线或图路线当作学术结论。
不得裁定权利，不得提升来源，也不得导入正式语料记录。
本指南不是语料导入批准，不是已确认学术结论，
也不是释读结论。
