# Statistics Generation Tools / 统计生成工具

English:
These tools generate preprocessing audits, coverage statistics, review
queues, and route packs for human researchers. They help reviewers find
which source, object, phase, or evidence route to open next.

简体中文：
本目录工具生成预处理审计、覆盖统计、复核队列和路线包。它们帮助
研究者判断下一步应打开哪个来源、对象、阶段或证据路线。

## Purpose / 用途

English:
Statistics are navigation signals. They are not scholarship, not source
promotion, not corpus import approval, and not a decipherment conclusion.
Use them after opening the human README, dossier, source note, or review
sheet for the relevant object.

简体中文：
统计只是导航信号。它们不是学术结论，不是来源提升，不是语料
导入批准，也不是释读结论。使用统计前，应先打开相关对象的人类
README、档案、来源说明或复核表。

## Human Review Entry Order / 人工复核入口顺序

1. Open the relevant human README or object-local dossier.
2. Check the source registry, package manifest, checksum, and rights note.
3. Open the matching audit row or review checklist in this directory.
4. Follow route paths back to concrete `corpus` object directories.
5. Treat graph edges, CSV rows, JSON packs, and counters as routes only.
6. Record reviewed outcomes in human-gated review files.
7. Keep unreviewed items as candidate, missing, pending, or needs review.

人工复核时，先读人类 README 或对象内档案，再核对来源登记、
manifest、checksum 和权利说明。然后打开本目录中的审计行或复核
清单，并沿路线回到具体 `corpus` 对象目录。图边、CSV、JSON 和
计数只作为路线，未经复核不得写成结论。

## Main Output Families / 主要输出家族

- Source coverage:
  `007_source-coverage-summary.csv`.
- Preprocessing status:
  `090_preprocessing-status-audit.csv`.
- Source-processing pipeline:
  `094_source-processing-pipeline-audit.csv`.
- Core corpus readiness and phase coverage:
  `134_core-corpus-readiness-matrix.csv`,
  `135_core-corpus-phase-coverage-matrix.csv`.
- Object-local material coverage:
  `186_character-object-material-coverage-audit.csv`,
  `188_object-local-material-coverage-audit.csv`,
  `220_object-local-human-research-depth-audit.csv`,
  `221_object-local-human-research-depth-summary.json`.
- Project ID route integrity:
  `190_project-id-source-map-audit.csv`.
- Core phase gap review:
  `192_core-corpus-phase-gap-action-queue.csv` through
  the `212_*outcome-route-summary.json` route summary, plus
  `213_core-corpus-phase-gap-human-review-guide.md`,
  `216_research-source-phase-gap-human-guide.md`,
  `214_inscription-plate-crosswalk-phase-gap-human-guide.md`,
  `215_collection-provenance-phase-gap-human-guide.md`,
  `217_published-research-note-phase-gap-human-guide.md`,
  `218_character-candidate-phase-gap-human-guide.md`,
  `219_shape-component-evolution-phase-gap-human-guide.md`.

## Current Review Surfaces / 当前复核入口

- Research source phase gaps:
  `193_research-source-phase-gap-review-checklist.csv`.
- Research source human guide:
  `216_research-source-phase-gap-human-guide.md`.
- Collection provenance gaps:
  `194_collection-provenance-phase-gap-review-checklist.csv`.
- Collection provenance human guide:
  `215_collection-provenance-phase-gap-human-guide.md`.
- Inscription and plate crosswalk gaps:
  `195_inscription-plate-crosswalk-phase-gap-review-checklist.csv`.
- Inscription and plate crosswalk human guide:
  `214_inscription-plate-crosswalk-phase-gap-human-guide.md`.
- Shape, component, and evolution verification gaps:
  `196_shape-component-evolution-verification-gap-review-checklist.csv`.
- Shape, component, and evolution human guide:
  `219_shape-component-evolution-phase-gap-human-guide.md`.
- Published research note gaps:
  `197_published-research-note-phase-gap-review-checklist.csv`.
- Published research note human guide:
  `217_published-research-note-phase-gap-human-guide.md`.
- Character candidate phase gaps:
  `198_character-candidate-phase-gap-review-checklist.csv`.
- Character candidate human guide:
  `218_character-candidate-phase-gap-human-guide.md`.
- Joined review index and handoff route packs:
  `199_core-corpus-phase-gap-review-index.csv` through
  the `212_*outcome-route-summary.json` route summary.
- Human-readable phase-gap guide:
  `213_core-corpus-phase-gap-human-review-guide.md`.

## Concrete Questions To Check / 具体待查问题

- Which object has images but still lacks a human-readable dossier?
- Which source lacks checksum, package manifest, field map, or risk note?
- Which phase is missing, mixed, partial, or waiting for human review?
- Which object-local material coverage row points to a partial bundle?
- Which object corpus area still needs human research depth review?
- Which source-processing pipeline row needs a concrete evidence route?
- Which phase gap review row opens the most direct next source file?
- Which human-fillable outcome scaffold is still empty by design?
- Which graph edge or statistic is only a route, not a conclusion?

- 哪个对象已有图像，却仍缺人类可读档案？
- 哪个来源仍缺 checksum、package manifest、字段映射或风险说明？
- 哪个阶段是 missing、mixed、partial 或等待人工复核？
- 哪条 object-local material coverage 行指向部分缺失的对象资料包？
- 哪条 source-processing pipeline 行还需要具体证据路线？
- 哪条 phase gap review 行能打开最直接的下一步来源文件？
- 哪个人工可填写 outcome scaffold 目前按设计仍为空？
- 哪条图边或统计只是路线，不能当成结论？

## Boundaries / 边界

English:
The outputs here may count object-local material coverage, source-processing
pipeline status, phase gap review routes, and human-fillable outcome scaffold
rows. They do not collect new evidence, decide rights, promote sources or
candidates, import formal corpus records, confirm identity, assign
components, accept correspondences, or make decipherment conclusions.

简体中文：
本目录输出可以统计对象内资料覆盖、来源处理流程状态、阶段缺口
复核路线和人工可填写 outcome scaffold 行。它们不采集新证据、
不裁定权利、不提升来源或候选、不导入正式语料、不确认身份、
不归属构件、不接受对应关系，也不是释读结论。

## Regeneration / 重新生成

Run the specific builder for the output family you are updating. After
changing scripts, schemas, docs, or generated preprocessing outputs, run:

```powershell
python tools/validation/check_repository_skeleton.py
python -m unittest discover -s tests -v
git diff --check
```
