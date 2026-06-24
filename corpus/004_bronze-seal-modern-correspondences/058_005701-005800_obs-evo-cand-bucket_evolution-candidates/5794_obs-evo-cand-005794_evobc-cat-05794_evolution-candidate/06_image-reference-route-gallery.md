# Image Reference Route Gallery / 图像引用路线图
Project ID: `obs-evo-cand-005794`

EVOBC category candidate ID: `evobc-evo-cat-05794`

English:
This object has EVOBC image-reference metadata, but no local source image is
collected here yet. The route cards below guide later visual evidence review
inside the same object directory and registered source files.

Simplified Chinese:
本对象保存 EVOBC 图像引用 metadata，目前尚未采集本地图像。下面条目只是证据路线卡，用来指导后续视觉证据复核。

## Route Cards / 路线卡

- `obs-evo-cand-005794-route-category-staging`
  type: `category_metadata_staging`
  label: `EVOBC category row with aggregate image-reference counts`
  route file: `001_evobc-evolution-category-staging.csv`
  pending check: 待查：先开 `05_image-reference-route-index.csv` 核对图像路线。
- `obs-evo-cand-005794-route-list-staging`
  type: `list_metadata_staging`
  label: `EVOBC list rows summarized into era/source counts`
  route file: `001_evobc-evolution-category-staging.csv`
  pending check: 待查：先开 `05_image-reference-route-index.csv` 核对图像路线。
- `obs-evo-cand-005794-route-code-index`
  type: `object_local_code_index`
  label: `Object-local era/source code index for locating review buckets`
  route file: `03_era-source-code-index.csv`
  pending check: 待查：先开 `05_image-reference-route-index.csv` 核对图像路线。
- `obs-evo-cand-005794-route-evolution-graph`
  type: `graph_edge_route`
  label: `EVOBC relationship graph edges that reference this category`
  route file: `007_evobc-evolution-graph-edges.jsonl`
  pending check: 待查：先开 `05_image-reference-route-index.csv` 核对图像路线。

## Evidence Boundary / 证据边界

- Local image evidence: 待查：先开 `05_image-reference-route-index.csv` 核对图像路线。
- Formal correspondence: `not_formal_correspondence`
- Evolution-chain claim: `no_claim`
- Modern-character identity: `not_confirmed`
- Boundary marker: `not accepted paleographic correspondences`
- Boundary marker: `not evolution-chain conclusions`
- Review status: `needs_human_evolution_review`

These route cards are preprocessing infrastructure only. They are not accepted
paleographic correspondences, not evolution-chain conclusions, not
modern-character identity confirmations, and not decipherment conclusions.

## Concrete Questions To Check / 具体待查问题

- Open `05_image-reference-route-index.csv` and name the route row.
- Open `02_evolution-source-index.csv` and name the source evidence row.
- Open `03_era-source-code-index.csv` and name the era/source code row.
- Record whether the missing route is image, rubbing, plate, context, or
  later-script source.
- 打开 `05_image-reference-route-index.csv`，写明图像路线行。
- 打开 `02_evolution-source-index.csv`，写明来源证据行。
