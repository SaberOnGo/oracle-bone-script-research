# obs-evo-cand-009915 跨时期字形复核档案

本文件是给人工复核者打开的跨时期字形复核档案。它把 EVOBC
候选路线、图像引用、时期/来源代码和下一步待查证据放在同一对象目录内；它不是正式对应结论，也不是释读结论。

## 候选身份

- 本项目 ID：`obs-evo-cand-009915`
- EVOBC 候选类别 ID：`evobc-evo-cat-09915`
- 外部类别引用：`evobc-cat-09915`
- 来源类别 ID：`09915`
- 来源标签：`鞘`
- 来源 codepoints：`U+9798`
- EVOBC 图像引用数量：`1`
- 复核状态：`needs_human_evolution_review`

## 甲骨侧待查证据

- 先查是否有对应的甲骨实物、拓片、照片、图版或摹本。
- 再查甲骨侧卜辞编号、全文或 OCR、合集号、著录号和页码。
- 继续核对馆藏、出土地、时期、组类、批次和关联字形。
- 若只存在 EVOBC metadata，不得写成已确认甲骨字形对应。

## 金文、小篆与后世字形路线

- 金文路线只作为待核对比较线索，须另查器物、铭文和著录。
- 小篆路线只作为后世字形比较线索，须另查字书和释读史。
- 后世字形或今字路线须记录来源、提出者和不同意见。
- 任何跨时期对应在人工复核前均保持候选和待查状态。

## 今字与 codepoint 路线

- codepoint 和来源标签只是检索键，不确认今字身份。
- 若要记录今字对应，需先打开可复核字典、数据库或论文来源。
- 若来源之间有不同意见，应记录争议而不是合并成结论。

## 来源证据、争议与释读史路线

- 先打开 `02_evolution-source-index.csv` 查来源与下载路线。
- 再打开 `03_era-source-code-index.csv` 查时期和来源代码。
- 再打开 `05_image-reference-route-index.csv` 查图像引用路线。
- 图边和统计只作检索路线，不作学术结论。
- 后续应核对小学堂、OBIMD、HUST-OBC、史语所和博物馆来源。

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

## 已登记时期与来源代码

- era `2`
  token: `SS`
  image references: 1
- source `1`
  token: `Web:105952;說文Web:58`
  image references: 1

## 图像引用路线卡

- `obs-evo-cand-009915-route-category-staging`
  type: `category_metadata_staging`
  label: `EVOBC category row with aggregate image-reference counts`
  route file: `001_evobc-evolution-category-staging.csv`
  pending check: 待查：先开 `05_image-reference-route-index.csv` 核对图像路线。
- `obs-evo-cand-009915-route-list-staging`
  type: `list_metadata_staging`
  label: `EVOBC list rows summarized into era/source counts`
  route file: `001_evobc-evolution-category-staging.csv`
  pending check: 待查：先开 `05_image-reference-route-index.csv` 核对图像路线。
- `obs-evo-cand-009915-route-code-index`
  type: `object_local_code_index`
  label: `Object-local era/source code index for locating review buckets`
  route file: `03_era-source-code-index.csv`
  pending check: 待查：先开 `05_image-reference-route-index.csv` 核对图像路线。
- `obs-evo-cand-009915-route-evolution-graph`
  type: `graph_edge_route`
  label: `EVOBC relationship graph edges that reference this category`
  route file: `007_evobc-evolution-graph-edges.jsonl`
  pending check: 待查：先开 `05_image-reference-route-index.csv` 核对图像路线。

## 具体待查问题

- 打开 `02_evolution-source-index.csv`，写明来源和下载证据行。
- 打开 `03_era-source-code-index.csv`，写明时期和来源代码行。
- 打开 `05_image-reference-route-index.csv`，写明图像路线行。
- 打开 `07_human-evolution-dossier.md`，记录跨时期缺口分类。
- 打开 `09_cross-period-review-dossier.md`，逐项记录甲骨、金文、小篆、今字缺口。
- 记录缺口属于图像、卜辞、金文小篆、今字、文献还是权利来源。

## 复核边界

- 这不是正式对应结论。
- 这不是演化链结论。
- 这不是今字身份确认。
- 这不是释读结论。
- 所有未打开的一手材料、著录和论文均保持待查状态。
