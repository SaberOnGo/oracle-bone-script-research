# Evolution Review Fact Matrix / 字形演化复核事实矩阵: obs-evo-cand-004372

English:
This human first-read matrix tells a reviewer what can be checked in this EVOBC
object directory before any paleographic, cross-period, modern-character,
meaning, reading, or decipherment claim is made.

Simplified Chinese:
本矩阵是人工首读路线，用来将字形图像、卜辞、图版、著录、出土、馆藏、时期、组类、金文、小篆、今字、释读史和争议放回同一对象目录内复核。

## Human Review Order

- Open `11_evolution-review-fact-matrix.md` first.
- Then open `07_human-evolution-dossier.md` for the full dossier.
- Open `09_cross-period-review-dossier.md` before correspondence claims.
- Use structured route files only as secondary route support.
- 结构化路线文件只作检索、追溯和复核辅助。
- Record missing image, inscription, catalog, bibliography, rights, meaning,
  reading, dispute, findspot, collection, period, and batch evidence before any
  promotion.

## Human Comparison Order / 人工比对顺序

- Open `07_human-evolution-dossier.md` before route tables.
- Open image and source route indexes only after the human dossier.
- Open `09_cross-period-review-dossier.md` before correspondence claims.
- Do not promote graph or codepoint routes into evolution evidence.

## Evolution And Correspondence Fact Matrix / 字形演化与对应事实矩阵

| Fact area / 事实领域 | Human review use / 人工复核用途 | Open these routes / 打开这些路线 |
| --- | --- | --- |
| Evolution candidate / 演化候选 | Dataset category candidate only; no accepted correspondence. | `01_candidate-evolution-packet.json`; `07_human-evolution-dossier.md` |
| Oracle-side route / 甲骨侧路线 | Check image, rubbing, inscription, plate, catalog, Heji, findspot, collection, period, group, and batch evidence. | `09_cross-period-review-dossier.md` |
| Bronze seal modern route / 金文小篆今字路线 | Treat bronze, seal, variant, component, modern codepoint, meaning, and reading links as candidates until sources are opened. | `09_cross-period-review-dossier.md` |
| Image reference route / 图像引用路线 | 4 route rows; local visual evidence must still be opened from source routes. | `05_image-reference-route-index.csv`; `06_image-reference-route-gallery.md` |
| Era and source-code route / 时期与来源代码路线 | 2 era/source rows; dataset labels are search aids only. | `03_era-source-code-index.csv` |
| Graph edge route / 图边路线 | Graph route only; not an accepted paleographic correspondence. | `corpus/008_relationship-graph/007_evobc-evolution-graph-edges.jsonl` |
| Bibliography and dispute route / 文献与争议路线 | Check proposer, bibliography, web database scope, reading history, dispute, and disagreement before any claim. | `research/`; `09_cross-period-review-dossier.md` |
| Source and rights trail / 来源与权利链 | `src-evobc` with rights status `source_marked_risk_noted`. | `02_evolution-source-index.csv`; `project_registry/` |
| Missing evidence route / 缺失证据路线 | Record exact gaps for image, inscription, bronze, seal, codepoint, bibliography, rights, findspot, collection, period, group, and batch. | `07_human-evolution-dossier.md`; `09_cross-period-review-dossier.md` |
| Review status / 复核状态 | `needs_human_evolution_review`. | `08_evolution-dossier-index.json`; `10_cross-period-review-index.json` |

## Concrete Review Questions

- Open `02_evolution-source-index.csv` before trusting source rows.
- Open `03_era-source-code-index.csv` before using era labels.
- Open `05_image-reference-route-index.csv` before visual review.
- Open `07_human-evolution-dossier.md` before recording gaps.
- Open `09_cross-period-review-dossier.md` before correspondence claims.
- Record the exact missing source route before any promotion.
- 打开 `02_evolution-source-index.csv`，先核对来源和下载行。
- 打开 `05_image-reference-route-index.csv`，先核对图像和图版路线。
- 打开 `09_cross-period-review-dossier.md`，先记录金文、小篆、今字和释读争议缺口。

## Review Boundary

- This is not an accepted paleographic correspondence.
- This is not an evolution-chain conclusion.
- This is not a confirmed modern-character identity.
- This is not a decipherment conclusion.
- All unopened primary images, rubbings, plates, catalogs, papers, and database
  routes remain pending human review.
