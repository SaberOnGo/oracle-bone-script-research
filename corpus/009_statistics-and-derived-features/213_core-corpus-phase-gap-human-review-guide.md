# Core Corpus Phase Gap Human Review Guide / 核心语料阶段缺口人工复核指南

English:
This guide is the human-readable entry for core-corpus preprocessing
phase gaps. It tells reviewers which support file to open after
they have checked the relevant human-readable dossier, source object,
or review sheet. It is not a reviewed outcome, not a rights decision,
not source or candidate promotion, not corpus import approval, and
not a decipherment conclusion.
Each gap must lead back to images, rubbings, inscription text, catalog
numbers, findspot or collection data, period evidence, component and
variant comparison, and published scholarship or dispute notes.

简体中文：
本指南是核心语料预处理阶段缺口的人工入口。复核者应先打开
相关对象的人类可读档案、来源对象或复核表，再按这里列出的
辅助文件继续核查。本指南不是复核结论，不是权利决定，
不是来源或候选记录提升，不是语料导入批准，也不是释读结论。
每个缺口都必须回到字形图像、拓片、卜辞全文、著录号、出土地、
馆藏、时期、构件、异体、近形、释读史、提出者和争议。

## Summary / 摘要

- updated at / 更新日期: 2026-06-30
- gap rows: 20
- review index rows: 20

| Route file | Path |
| --- | --- |
| action queue | `corpus/009_statistics-and-derived-features/192_core-corpus-phase-gap-action-queue.csv` |
| review index | `corpus/009_statistics-and-derived-features/199_core-corpus-phase-gap-review-index.csv` |

### Gap Rows By Corpus Area / 按语料区统计缺口

- collection_provenance_assets: 3
- cross_source_codepoint_routes: 1
- evolution_correspondences: 1
- graphemic_components: 1
- inscriptions_and_plate_crosswalks: 2
- oracle_characters: 1
- published_research_notes: 4
- research_sources_and_bibliography: 5
- undeciphered_oracle_character_candidates: 2

### Gap Rows By Phase Status / 按阶段状态统计缺口

- missing: 9
- mixed_or_partial: 11

### Specialized Checklists / 专项复核清单

- character_candidate_phase_gap_review: 3
- collection_provenance_phase_gap_review: 3
- inscription_plate_crosswalk_phase_gap_review: 2
- published_research_note_phase_gap_review: 4
- research_source_phase_gap_review: 5
- shape_component_evolution_verification_gap_review: 3

## Human Review Entry Order / 人工复核入口顺序

1. Open the related object-local human-readable dossier first.
2. Check glyph images, rubbings, inscriptions, and catalog notes.
3. Check source provenance, rights status, and review status.
4. Check scholarship, reading history, authors, and disputes.
5. Check findspot, collection, period, group, and batch evidence.
6. Check component, variant, near-form, and later-form evidence.
7. Open the support files named below only after those checks.
8. Record reviewed results only in the matching outcome scaffold.
9. Keep empty outcome fields empty until a human review pass.

Support files to open after the human checks:

1. Open `192_core-corpus-phase-gap-action-queue.csv`.
2. Open `199_core-corpus-phase-gap-review-index.csv`.
3. Open the specialized checklist named by the review index row.

人工复核时，先打开对象内人类可读档案，再核对字形图像、拓片、
卜辞全文、图版、著录号、出土地、馆藏、时期、构件、异体、
近形、释读史、提出者、不同意见和争议。完成这些人工核查后，
再查看 192 行动队列、199 复核索引和对应专项清单。只有完成
人工复核后，才把结果写入匹配的 outcome scaffold。

## Research Slots To Recover / 应回收的研究槽位

- Glyph image, rubbing, photograph, and plate evidence.
- Inscription text, OCR, catalog number, and collection number.
- Findspot, collection, period, group, and batch evidence.
- Component, variant, near-form, bronze, seal, and modern links.
- Bibliography, scholarship history, proposer, and disputes.
- Missing evidence and next source to check before formal research.
- 字形图像、拓片、照片和图版证据。
- 卜辞全文、OCR、著录号、合集号和馆藏编号。
- 出土地、馆藏、时期、组类和批次证据。
- 构件、异体、近形、金文、小篆和今字关联。
- 书目、释读史、提出者、不同意见和争议。
- 正式研究前仍缺的证据和下一步待查来源。

## Support File Steps / 辅助文件步骤

1. Open `192_core-corpus-phase-gap-action-queue.csv`.
2. Open `199_core-corpus-phase-gap-review-index.csv`.
3. Open the specialized checklist named by the review index row.

## Concrete Questions To Check / 具体待查问题

- Which gap row points to a missing human-readable dossier?
- Which source still lacks checksum, package manifest, or risk note?
- Which candidate route is still only staging or metadata?
- Which phase gap requires returning to an object-local review sheet?
- Which evidence path is a route rather than collected evidence?
- Which outcome scaffold is intentionally empty before review?
- Which glyph image, rubbing, plate, or photograph is still missing?
- Which inscription text, OCR, catalog, or collection number is absent?
- Which scholarship, proposer, alternate view, or dispute is missing?
- Which component, variant, near-form, or later-form link is unreviewed?
- 哪条缺口行指向仍缺人类可读档案的对象？
- 哪个来源仍缺 checksum、package manifest 或风险提示？
- 哪条候选路线仍只是 staging 或 metadata？
- 哪个阶段缺口必须回到对象内人工复核表？
- 哪条证据路径只是路线，而不是已收集证据？
- 哪个 outcome scaffold 在复核前应按设计保持为空？
- 哪个字形图像、拓片、图版或照片仍缺失？
- 哪条卜辞全文、OCR、著录号或馆藏号仍缺失？
- 哪条书目、提出者、不同意见或争议仍缺失？
- 哪条构件、异体、近形或后世字形关联仍未复核？

## Boundary / 边界

This guide summarizes route tables for preprocessing review. It does not
replace a human-readable dossier, a source record, a rights note, a
bibliographic note, a graph-edge source file, or a review sheet.

本指南只汇总预处理复核路线表。它不能替代人类可读档案、来源
记录、权利说明、书目笔记、图边来源文件或人工复核表。
