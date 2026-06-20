# Source Object Materials / 来源对象资料

English:
`build_source_object_materials.py` creates object-local human and AI materials for registered research sources under `corpus/006_research-sources-and-bibliography/001_source-objects/`.

简体中文：
`build_source_object_materials.py` 会在 `corpus/006_research-sources-and-bibliography/001_source-objects/` 下为已登记研究来源生成对象内人类/AI 资料。

## Generated Files / 生成文件

Each concrete `src-*` source object directory contains:

每个具体 `src-*` 来源对象目录包含：

- `README.md`: human-readable source summary and risk boundary.
- `01_source-packet.json`: AI-readable source packet.
- `02_download-route-index.csv`: download/access route index joined with log status.
- `03_package-route-index.csv`: source package and file manifest routes.
- `04_field-map-route-index.csv`: field mapping routes.
- `05_metadata-profile-route-index.csv`: downloaded metadata profile routes.
- `06_human-source-review-sheet.md`: human review checklist.

## Boundary / 边界

English:
These source objects are provenance and data-engineering entrances only. They are not rights clearance, import approval, formal character readings, component assignments, inscription identities, correspondence conclusions, or decipherment conclusions.

简体中文：
这些来源对象只作为出处追溯和资料工程入口。它们不是权利清理结论、导入批准、正式释读、构件归属、卜辞身份、字形对应结论或破译结论。
