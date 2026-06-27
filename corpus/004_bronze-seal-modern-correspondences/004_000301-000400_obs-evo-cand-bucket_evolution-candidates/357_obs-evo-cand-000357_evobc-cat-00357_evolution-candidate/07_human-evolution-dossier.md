# Human Evolution And Correspondence Dossier / 字形演化与对应候选档案

Project ID: `obs-evo-cand-000357`

## Purpose / 用途

This dossier is the human-readable working file for one EVOBC evolution or
cross-period correspondence candidate. It records source routes and concrete
checks only; it is not a formal correspondence, not an evolution-chain
conclusion, and not a decipherment conclusion.

本档案是一个 EVOBC 字形演化或跨时期对应候选对象的人类可读工作档案。这里记录来源路线、图像线索和具体待查问题，不作正式对应、演化链或释读结论。

## Candidate Identity / 候选身份

- Project ID: `obs-evo-cand-000357`
- EVOBC category candidate ID: `evobc-evo-cat-00357`
- External category reference: `evobc-cat-00357`
- Source category ID: `00357`
- Source label for human review: `䏬`
- Source codepoints: `U+43EC`
- Image reference count in source metadata: `2`
- Review status: `needs_human_evolution_review`

## Source Image And Route Evidence / 来源图像与路线证据

- Open the EVOBC category staging CSV for the source category row.
- Open the EVOBC era/source codebook CSV for code labels.
- Open `05_image-reference-route-index.csv` before visual review.
- Open `06_image-reference-route-gallery.md` for local route cards.
- Open the EVOBC graph JSONL only as graph-derived routing.
- Check source download records, checksums, rights notes, and manifests before
  using any route as evidence.

## Era And Source-Code Context / 时期与来源代码语境

- era `3`
  token: `SAC`
  image references: 2
- source `4`
  token: `Book:9131`
  image references: 2

## Oracle, Bronze, Seal, And Later-Script Review

- 甲骨 route: check whether the source row only has metadata flags, or whether a
  primary oracle image, rubbing, plate, or inscription context has been
  separately verified.
- 金文 route: treat bronze references as candidate route metadata until a cited
  image, catalog, vessel context, and bibliography are checked.
- 小篆 route: treat seal-script links as later-script comparison clues, not proof
  of identity or development.
- 后世字形 route: record only source-provided hints until dictionaries and published
  scholarship are opened.
- 今字 route: codepoints and labels are lookup aids only; they do not confirm
  modern-character identity.

## Modern Codepoint Route Review / 今字 codepoint 路线复核

Modern codepoints, source labels, and category IDs are lookup routes. They may
guide comparison, but they are not accepted identities until human reviewers
verify images, inscriptions, catalogs, and scholarship.

## Image Reference Route Cards / 图像引用路线卡

- `obs-evo-cand-000357-route-category-staging`
  type: `category_metadata_staging`
  label: `EVOBC category row with aggregate image-reference counts`
  route file: `001_evobc-evolution-category-staging.csv`
  pending check: 待查：先开 `05_image-reference-route-index.csv` 核对图像路线。
- `obs-evo-cand-000357-route-list-staging`
  type: `list_metadata_staging`
  label: `EVOBC list rows summarized into era/source counts`
  route file: `001_evobc-evolution-category-staging.csv`
  pending check: 待查：先开 `05_image-reference-route-index.csv` 核对图像路线。
- `obs-evo-cand-000357-route-code-index`
  type: `object_local_code_index`
  label: `Object-local era/source code index for locating review buckets`
  route file: `03_era-source-code-index.csv`
  pending check: 待查：先开 `05_image-reference-route-index.csv` 核对图像路线。
- `obs-evo-cand-000357-route-evolution-graph`
  type: `graph_edge_route`
  label: `EVOBC relationship graph edges that reference this category`
  route file: `007_evobc-evolution-graph-edges.jsonl`
  pending check: 待查：先开 `05_image-reference-route-index.csv` 核对图像路线。

## Bibliography, Database, And Web Source Routes

- Check Xiaoxuetang, OBIMD, HUST-OBC, IHP/Sinica, museum portals, published
  catalog notes, and paper bibliography before promotion.
- Record proposer, source, page or record ID, and disagreement status when a
  published correspondence or variant history is later found.
- Until bibliography is opened, keep this object as a route dossier with no
  reviewed scholarly conclusion.

## Human Research Review Slots / 人类研究复核槽位

- 字形 image check: compare primary image, rubbing, photograph, handcopy, and
  damaged strokes before any visual comparison.
- 卜辞 check: record inscription number, full text or OCR, plate, catalog, Heji or
  other catalog route, and page evidence.
- 出土 and 馆藏 check: record findspot, collection, period, 组类, batch, and object
  provenance before cross-period comparison.
- 构件 and 组成 check: note component clues only after comparing independent
  character dossiers and published component studies.
- 异体 and 近形 check: compare variant and near-shape evidence against oracle,
  bronze, seal, and later-script examples.
- 金文, 小篆, 今字 check: keep bronze, seal, and modern codepoint relations as
  candidate comparanda until sources are opened.
- 释读史 check: record scholar, proposer, paper, bibliography, dispute,
  disagreement, and review status when found.
- 演化 and 关系 check: do not promote an evolution relation until image,
  inscription, catalog, provenance, and period evidence agree.


## Source Provenance Audit / 来源追溯审计

- Source register row: `src-evobc` / EVOBC: Evolution Oracle Bone Characters
  Dataset
- Rights status: `source_marked_risk_noted`
- Review status: `reviewed`
- Download log path:
  `project_registry/006_large-source-register/002_source-download-log.csv`
- Package manifest: `009_source-package-file-manifest.csv`
- Field map: `007_source-field-map.csv`
- Field map rows: `2`
- Risk note: Useful for evolution-chain experiments, but source texts/websites
  and image rights need separate review before corpus import.

- Download ID: `dl-evobc-key-value-json`
- Download status: `downloaded`
- HTTP status: `200`
- File size bytes: `277219`
- Checksum SHA-256:
  `4cd93a859d975f00831f8b1db91069d859856f04314dc22a9e50aaff464bec38`
- Package file ID: `pkg-file-000012`
- Package file name: `Key&Value.json`
- Commit policy: `download_to_tmp_log_checksum_only`
- Download ID: `dl-evobc-list-json`
- Download status: `downloaded`
- HTTP status: `200`
- File size bytes: `23254733`
- Checksum SHA-256:
  `c81e0f6bc6a839fbd8a30788a2ffb30a9615fc12be00b85ae1f9e9a90e8ba1f7`
- Package file ID: `pkg-file-000013`
- Package file name: `List_of_EVOBC.json`
- Commit policy: `download_to_tmp_log_checksum_only`

This audit is source-route evidence only. It does not confirm a paleographic
correspondence, an evolution chain, a modern identity, image rights, or a
decipherment conclusion.

## Missing Evidence And Next Checks / 缺失证据与下一步

- Open `05_image-reference-route-index.csv` for each image reference route.
- Open `02_evolution-source-index.csv` for source, download, and rights rows.
- Open `03_era-source-code-index.csv` before using era or source labels.
- Open `09_cross-period-review-dossier.md` for oracle, bronze, seal, and
  modern-route gaps.
- Record each missing source as image, inscription, bronze/seal, codepoint,
  bibliography, or rights trail.
- 打开 `05_image-reference-route-index.csv`，逐条核对图像引用路线。
- 打开 `02_evolution-source-index.csv`，记录来源、下载和权利行。
- 打开 `09_cross-period-review-dossier.md`，记录跨时期缺口分类。

## Concrete Questions To Check / 具体待查问题

- Open `05_image-reference-route-index.csv` for each image reference route.
- Open `02_evolution-source-index.csv` for source, download, and rights rows.
- Open `03_era-source-code-index.csv` before using era or source labels.
- Open `09_cross-period-review-dossier.md` for oracle, bronze, seal, and
  modern-route gaps.
- Record each missing source as image, inscription, bronze/seal, codepoint,
  bibliography, or rights trail.
- 打开 `05_image-reference-route-index.csv`，逐条核对图像引用路线。
- 打开 `02_evolution-source-index.csv`，记录来源、下载和权利行。
- 打开 `09_cross-period-review-dossier.md`，记录跨时期缺口分类。

## Review Boundary / 复核边界

- No formal correspondence is recorded in this dossier.
- This dossier is not an evolution-chain conclusion.
- No evolution-chain conclusion is recorded in this dossier.
- No modern-character identity is confirmed in this dossier.
- No decipherment conclusion is recorded in this dossier.
- 本档案只服务资料整理和复核路线，不替代正式文字学研究。
