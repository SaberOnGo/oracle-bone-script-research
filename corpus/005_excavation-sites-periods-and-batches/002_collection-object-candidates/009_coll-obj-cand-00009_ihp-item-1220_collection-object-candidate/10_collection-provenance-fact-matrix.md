# Collection Provenance Fact Matrix / 馆藏来源事实矩阵: coll-obj-cand-00009

English:
This matrix gives a compact human review order for the collection object
candidate. It points from each fact to the local evidence file that must be
opened before any comparison, citation, or later research use.

简体中文：
本矩阵为馆藏对象候选提供简明的人工复核顺序；每个事实都指向必须先打开的本地证据文件。

The field vocabulary remains explicit for human cross-checking:

- Collection object
- Catalog or accession route
- Image or visual route
- Findspot or provenience
- Period or date
- Batch or excavation context
- Inscription and character links
- Source and rights trail
- Risk note
- Review status

中文字段仍明确保留：著录或登记路线、图像或视觉路线、出土地或来源地、时期或年代、
批次或发掘语境、卜辞与单字关联、来源与权利链、风险提示、复核状态。

The earlier compact table header is retained as a field-label reference:

`| Fact / 项目 | Current status / 当前状态 |`

The full human dossier and evidence index remain the detailed routes:

- `06_human-collection-dossier.md`
- `09_collection-provenance-evidence-index.json`

## Human Review Order / 人工复核顺序

- Start with `10_collection-provenance-fact-matrix.md`.
- Then open `08_collection-provenance-evidence-dossier.md`.
- Use `02_collection-source-index.csv` for source and rights routes.
- Use `18_live-source-evidence-review.md` first, then
  `03_visual-asset-index.csv` and `04_visual-gallery.md` for images.
- Use `11_collection-provenance-fact-matrix-index.json` only as support.

## Collection Object Provenance Fact Matrix / 馆藏对象来源事实矩阵

| Fact / 项目 | Status / 状态 | Open / 打开 |
| --- | --- | --- |
| Object / 对象 | candidate; identity pending | `01` packet; `06` dossier |
| Catalog / 著录 | `1220`; source page only | `02` source index; `06` dossier |
| Images / 图像 | private routes; rights pending | `18` evidence; `03` index |
| Findspot / 出土地 | provenance review pending | `06` dossier; `08` evidence |
| Period / 时期 | source review pending | `06` dossier; `08` evidence |
| Batch / 批次 | pit and plate context pending | `08` evidence |
| Inscription / 卜辞 | candidate only; no identity claim | `06`; `08` |
| Source / 来源权利 | metadata-only; review needed | `02` source; `09` index |
| Risk / 风险 | reuse review before public use | `01` packet; `03` index |
| Review / 复核 | human object review needed | `05` sheet; `09` index |

## Concrete Review Questions / 具体复核问题

- Open the catalog or accession source before trusting the label.
- Open the visual index and gallery before using the object image.
- Check findspot, period, batch, and plate evidence in the dossier.
- Separate candidate inscription or character links from confirmed facts.
- Review source, checksum, rights, and risk notes before public reuse.
- Record the precise missing evidence route for the next researcher.
- 先核对著录或登记来源，再信任对象标签。
- 使用图像前，先打开图像索引和图像入口。
- 把候选卜辞或单字关联与已确认事实分开记录。

## Review Boundary / 复核边界

- not a confirmed collection object identity
- not a confirmed inscription identity
- not a transcription
- not a formal reading
- not a decipherment conclusion
- candidate_collection_object_id: `ihp-mus-obj-00009`
