# Character Candidate Phase Gap Human Guide /
单字候选阶段缺口人工复核指南

English:
This guide is the human entrance for oracle-character and
undeciphered-character candidate phase gaps. It sends reviewers
back to concrete `obs-char-*` and `obs-unk-*` object folders,
where glyph images, observations, variants, near forms,
components, inscription context, plates, catalog numbers,
findspot, collection, period, group, sources, reading history,
disputes, and next sources must be checked by people.
It is not a rights decision, not candidate promotion,
not formal character import, not a character identity claim,
not confirmed scholarship, and not a decipherment conclusion.

简体中文：
本指南是甲骨单字候选和未释字候选阶段缺口的人工入口。
复核者应回到具体 `obs-char-*` 或 `obs-unk-*` 对象目录，
先看字形图片、观察记录、异体、近形、构件线索、
卜辞语境、图版、著录号、出土地、馆藏、时期、组类、
来源证据、释读史、争议和下一步待查来源。
它不是权利决定，不是候选提升，不是正式单字导入，
不是字形身份结论，不是已确认学术结论，也不是释读结论。

## Summary / 摘要

- updated at: 2026-06-30
- checklist rows: 3
- HUST promotion review rows: 1588
- candidate evidence request rows: 1588
- undeciphered index rows: 9408
- undeciphered review queue rows: 9408
- undeciphered evidence readiness rows: 2
- character object material audit rows: 10996
- source ids:
  - `src-hust-obc`
- phase gap statuses:
  - oracle_characters: verified `missing`
  - undeciphered_oracle_character_candidates: linked `missing`
  - undeciphered_oracle_character_candidates: verified `missing`

## Human Review Entry Order / 人工复核入口顺序

1. Open the concrete character object directory first.
2. Open a sample `obs-char-*` or `obs-unk-*` folder.
3. Read the human README, dossier, and review sheet.
4. Inspect glyph images, rubbings, photos, and plates.
5. Check variants, near forms, and component clues.
6. Check inscription occurrence and surrounding context.
7. Check catalog number, Heji number, findspot, collection,
   period, group, and batch evidence.
8. Check source evidence, rights status, risk note, and review.
9. Check decipherment history, proposer, disagreement, dispute.
10. Write unresolved items as concrete next-source questions.
11. Open support files only after the human object dossier.
12. Do not promote candidates from this guide.

人工复核时，先打开具体单字或未释字对象目录，
再看人类 README、研究档案和复核表。
清单、索引和统计只帮助定位对象，不能替代人工档案。

## Support Files / 辅助文件

| File | Path |
| --- | --- |
| checklist | `corpus/009_statistics-and-derived-features/198_character-candidate-phase-gap-review-checklist.csv` |
| action queue | `corpus/009_statistics-and-derived-features/192_core-corpus-phase-gap-action-queue.csv` |
| HUST promotion queue | `corpus/001_oracle-characters/000_character-registers/009_hust-obc-obs-char-promotion-review-queue.csv` |
| HUST promotion buckets | `corpus/001_oracle-characters/000_character-registers/010_hust-obc-promotion-bucket-review-summary.csv` |
| candidate evidence requests | `corpus/009_statistics-and-derived-features/005_ai-agent-hust-obc-candidate-evidence-pack-request-queue.csv` |
| undeciphered index | `corpus/001_oracle-characters/000_character-registers/003_undeciphered-oracle-characters-index.csv` |
| undeciphered review queue | `corpus/009_statistics-and-derived-features/051_ai-agent-hust-obc-undeciphered-candidate-review-queue.csv` |
| undeciphered readiness | `corpus/009_statistics-and-derived-features/060_ai-agent-hust-obc-undeciphered-candidate-evidence-readiness-checklist.csv` |
| character material audit | `corpus/009_statistics-and-derived-features/186_character-object-material-coverage-audit.csv` |
| character material summary | `corpus/009_statistics-and-derived-features/187_character-object-material-coverage-summary.json` |

Open these files after the object-local human materials.
They are review pointers, not evidence or scholarship by themselves.

## Required Character Dossier Slots / 单字档案槽位

- glyph image
- glyph observation
- variant forms
- near forms
- component clues
- inscription occurrence
- inscription context
- plate
- catalog number
- Heji number
- findspot
- collection
- period
- group
- source evidence
- decipherment history
- dispute notes
- later script routes
- missing items
- next sources to check

Every opened candidate folder should let a researcher see
what is present, what is only a candidate, what is disputed,
and which exact source must be checked next.
每个候选目录都应让研究者看清已有什么、什么仍是候选、
哪里存在争议，以及下一步必须打开哪一个具体来源。

## Source Context Fields / 来源语境字段

- `source_id`
- `source_row`
- `external_reference`
- `field_map`
- `extraction_note`
- `rights_status`
- `risk_note`
- `review_status`

These fields support provenance review only.
They do not confirm identity, reading, component, or correspondence.
这些字段只服务来源复核，不确认字形身份、释读、构件或对应关系。

## Concrete Questions To Check / 具体待查问题

- Which glyph image and observation route can be opened?
- Which variant, near-form, or component clue route must be compared?
- Which inscription occurrence and context route supports this candidate?
- Which plate, catalog number, Heji number, findspot, collection, period, or
  group route is present?
- Which source row, field map, or extraction note supports this route?
- Which decipherment-history or dispute route remains to be checked?
- Which later-script route remains to be checked?
- Which missing item or next source should be reviewed before promotion?
- Which glyph image, rubbing, photograph, or plate is visible?
- Which inscription occurrence and context can be opened?
- Which catalog number, Heji number, findspot, collection,
  period, group, or batch evidence is still absent?
- Which decipherment history, proposer, or dispute is documented?
- Which source evidence and rights note must be opened next?
- Which candidate is still only metadata or staging?
- 哪张字形图片、拓片、照片或图版可以直接查看？
- 哪条卜辞出现位置和上下文可以打开？
- 还缺哪一个著录号、合集号、出土地、馆藏、时期、组类或批次？
- 哪条释读史、提出者记录或争议已经有来源？
- 下一步必须打开哪条来源证据和权利说明？
- 哪个候选仍只是 metadata 或 staging？

## Boundary / 边界

Do not record reviewed outcomes in this guide.
Do not treat a checklist row, queue row, object count,
metadata packet, graph edge, or staging row as scholarship.
Do not decide rights.
Do not promote candidates.
Do not import formal character records.
Do not make a character identity claim.
Do not write any candidate as confirmed scholarship.
Do not write any candidate as a decipherment conclusion.

不得在本指南中记录复核结论。
不得把清单行、队列行、对象计数、metadata packet、
图边或 staging 行当成学术结论。
不得裁定权利，不得提升候选，不得导入正式单字记录。
不得作出字形身份结论。
不得把任何候选写成已确认学术结论或释读结论。
