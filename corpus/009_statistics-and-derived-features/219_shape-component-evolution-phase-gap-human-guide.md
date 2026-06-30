# Shape Component Evolution Phase Gap Human Guide /
形体构件演化阶段缺口人工复核指南

English:
This guide is the human entrance for codepoint-route,
component-candidate, and evolution-correspondence phase gaps.
Reviewers should open concrete object folders and visual evidence
before using CSV rows, graph edges, or JSON packets as pointers.
It is not an identity confirmation, not a component assignment,
not an accepted evolution correspondence,
not confirmed scholarship, and not a decipherment conclusion.

简体中文：
本指南是跨来源 codepoint、构件候选和演化对应阶段缺口的
人工复核入口。
复核者应先打开具体对象目录和可视证据，
再把 CSV 行、图边或 JSON 包当作辅助路线使用。
它不是字形身份确认，不是构件归属，
不是已接受的演化对应，
不是已确认学术结论，也不是释读结论。

## Summary / 摘要

- updated at: 2026-06-30
- checklist rows: 3
- codepoint staging rows: 1588
- component candidate rows: 2747
- component glyph rows: 41686
- evolution candidate rows: 13714
- component graph edges: 44433
- evolution graph edges: 51679
- source ids:
  - `src-evobc`
  - `src-hust-obc`
  - `src-obimd`
  - `src-obimd`
  - `src-evobc`
- phase gap statuses:
  - cross_source_codepoint_routes: verified `missing`
  - graphemic_components: verified `missing`
  - evolution_correspondences: verified `missing`

## Human Review Entry Order / 人工复核入口顺序

1. Open the concrete character, component, or evolution object first.
2. Open an `obs-char-*`, component, or evolution folder.
3. Inspect glyph images, rubbings, photos, or visual routes.
4. Compare variants, near forms, and component clues.
5. Check the source codepoint and source character id.
6. Check HUST, OBIMD, or EvoBC source rows.
7. Check the host character and object-local dossier.
8. Check bronze, seal, or modern correspondence routes.
9. Check source provenance, rights status, and risk note.
10. Record missing items as concrete next-source questions.
11. Open graph edges only as routes, not as conclusions.
12. Do not confirm a component from this guide.
13. Do not accept an evolution chain from this guide.

人工复核时，先打开具体单字、构件或演化对象目录，
再看图像、拓片、照片、异体、近形、构件线索和出处。
结构化清单只能帮助定位，不得替代人类可读档案。

## Support Files / 辅助文件

| File | Path |
| --- | --- |
| checklist | `corpus/009_statistics-and-derived-features/196_shape-component-evolution-verification-gap-review-checklist.csv` |
| action queue | `corpus/009_statistics-and-derived-features/192_core-corpus-phase-gap-action-queue.csv` |
| codepoint staging | `corpus/001_oracle-characters/000_character-registers/011_hust-obimd-evobc-codepoint-crosswalk-staging.csv` |
| codepoint review queue | `corpus/009_statistics-and-derived-features/041_ai-agent-hust-obimd-evobc-codepoint-crosswalk-review-queue.csv` |
| codepoint readiness | `corpus/009_statistics-and-derived-features/048_ai-agent-hust-obimd-evobc-codepoint-crosswalk-evidence-readiness-checklist.csv` |
| HUST promotion queue | `corpus/001_oracle-characters/000_character-registers/009_hust-obc-obs-char-promotion-review-queue.csv` |
| component staging | `corpus/003_graphemic-components/000_component-registers/002_obimd-subcharacter-main-staging.csv` |
| component glyph staging | `corpus/003_graphemic-components/000_component-registers/003_obimd-subcharacter-glyph-staging.csv` |
| component ID source map | `project_registry/002_project-id-to-source-reference-map/004_component-id-source-map.csv` |
| component graph edges | `corpus/008_relationship-graph/006_obimd-component-graph-edges.jsonl` |
| component review route | `doc/public/user_research/002_cross-source-review-queues/obimd` |
| component object folders | `corpus/003_graphemic-components` |
| evolution staging | `corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/001_evobc-evolution-category-staging.csv` |
| evolution ID source map | `project_registry/002_project-id-to-source-reference-map/005_evolution-candidate-id-source-map.csv` |
| evolution graph edges | `corpus/008_relationship-graph/007_evobc-evolution-graph-edges.jsonl` |
| evolution review route | `doc/public/user_research/002_cross-source-review-queues/evobc` |
| evolution object folders | `corpus/004_bronze-seal-modern-correspondences` |

Open these files after object-local human materials.
They are route and provenance aids, not accepted readings.

## Required Verification Slots / 必查复核槽位

- source codepoint
- source character id
- matched project character route
- matched source ids
- readiness route
- promotion review route
- missing evidence
- review status
- component candidate
- component shape label
- glyph image route
- host character route
- subcharacter source row
- component graph edge route
- missing visual evidence
- evolution candidate
- oracle source route
- bronze, seal, or modern route
- correspondence category
- source category row
- evolution graph edge route
- missing comparison evidence
- variant and near-form comparison
- component visual evidence
- bronze, seal, and modern-script comparison
- source provenance and risk note
- unresolved dispute or missing evidence

Each slot should point back to a visible source, object folder,
or review note before any later human reviewer decides status.
每个槽位都应指回可见来源、对象目录或复核记录，
等待后续人工判断状态。

## Source Context Fields / 来源语境字段

- `source_id`
- `source_register_row`
- `external_reference`
- `rights_status`
- `risk_note`
- `review_status`

These fields support provenance review only.
They do not confirm identity, component, or correspondence.
这些字段只服务来源复核，
不确认身份、构件或对应关系。

## Concrete Questions To Check / 具体待查问题

- Which source codepoint route is being compared?
- Which project character route is the match candidate?
- Which HUST, OBIMD, or EVOBC source row supports the route?
- Which readiness or promotion review route must be opened?
- What missing evidence or review status remains before identity review?
- Which component candidate and source row are being checked?
- Which glyph image or visual route supports the component candidate?
- Which host character or object-local route must be opened?
- Which graph edge is only a route and not a component claim?
- What missing visual evidence or review status remains?
- Which evolution candidate and source category row are being checked?
- Which bronze, seal, or modern correspondence route supports the candidate?
- Which oracle-source route must be opened before comparison?
- Which graph edge is only a route and not an accepted correspondence?
- What missing comparison evidence or review status remains?
- Which glyph image or visual route can be opened directly?
- Which variant, near form, or component clue must be compared?
- Which bronze, seal, or modern correspondence is only a route?
- Which source row, field map, or extraction note is missing?
- Which review note records disagreement or uncertainty?
- 哪一张字形图片或可视路线可以直接打开？
- 哪一个异体、近形或构件线索必须比较？
- 哪一条金文、小篆或今字对应还只是路线？
- 哪一条来源行、字段映射或抽取说明仍然缺失？
- 哪一条复核记录写有分歧或不确定性？

## Boundary / 边界

Do not record reviewed outcomes in this guide.
Do not treat a checklist row as evidence by itself.
Do not treat a graph edge as a component claim.
Do not treat an EvoBC route as an evolution conclusion.
Do not confirm identity from a codepoint route.
Do not confirm a component from this guide.
Do not accept an evolution chain from this guide.
Do not write any candidate as confirmed scholarship.
Do not write any candidate as a decipherment conclusion.

不得在本指南中记录复核结论。
不得把清单行本身当作证据。
不得把图边当作构件结论。
不得把 EvoBC 路线当作演化结论。
不得根据 codepoint 路线确认字形身份。
不得从本指南确认构件。
不得从本指南接受演化链。
不得把任何候选写成已确认学术结论。
不得把任何候选写成释读结论。
