# obs-evo-cand-005444 跨时期字形复核档案

本文件是给人工复核者打开的跨时期字形复核档案。它把 EVOBC
候选路线、图像引用、时期/来源代码和下一步待查证据放在同一对象目录内；它不是正式对应结论，也不是释读结论。

## 候选身份

- 本项目 ID：`obs-evo-cand-005444`
- EVOBC 候选类别 ID：`evobc-evo-cat-05444`
- 外部类别引用：`evobc-cat-05444`
- 来源类别 ID：`05444`
- 来源标签：`瑟`
- 来源 codepoints：`U+745F`
- EVOBC 图像引用数量：`43`
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

## 已登记时期与来源代码

- era `0`
  token: `OBC`
  image references: 7
- era `2`
  token: `SS`
  image references: 3
- era `4`
  token: `WSC`
  image references: 32
- era `5`
  token: `CS`
  image references: 1
- source `0`
  token: `Web:1633`
  image references: 1
- source `1`
  token: `Web:105952;說文Web:58`
  image references: 26
- source `2`
  token: `Book:17600`
  image references: 4
- source `5`
  token: `Book:32794`
  image references: 12

## 图像引用路线卡

- `obs-evo-cand-005444-route-category-staging`
  type: `category_metadata_staging`
  label: `EVOBC category row with aggregate image-reference counts`
  route file: `001_evobc-evolution-category-staging.csv`
  status: `not_collected_route_indexed`
- `obs-evo-cand-005444-route-list-staging`
  type: `list_metadata_staging`
  label: `EVOBC list rows summarized into era/source counts`
  route file: `001_evobc-evolution-category-staging.csv`
  status: `not_collected_route_indexed`
- `obs-evo-cand-005444-route-code-index`
  type: `object_local_code_index`
  label: `Object-local era/source code index for locating review buckets`
  route file: `03_era-source-code-index.csv`
  status: `not_collected_route_indexed`
- `obs-evo-cand-005444-route-evolution-graph`
  type: `graph_edge_route`
  label: `EVOBC relationship graph edges that reference this category`
  route file: `007_evobc-evolution-graph-edges.jsonl`
  status: `not_collected_route_indexed`

## 具体待查问题

- 哪一条 EVOBC 图像引用路线应先打开？
- 哪一个甲骨卜辞、馆藏、出土地或时期批次仍未核对？
- 哪一个金文器物、铭文、著录号或图版仍未核对？
- 哪一个小篆、字书、数据库或论文来源仍未核对？
- 哪一个今字 codepoint 只是检索键，尚不能作为对应结论？
- 是否存在释读史、提出者、不同意见或争议需要记录？
- 哪一条来源还缺 checksum、manifest、字段映射或权利复核？

## 复核边界

- 这不是正式对应结论。
- 这不是演化链结论。
- 这不是今字身份确认。
- 这不是释读结论。
- 所有未打开的一手材料、著录和论文均保持待查状态。
