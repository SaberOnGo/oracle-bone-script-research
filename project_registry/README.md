# Project Registry / 项目登记表

English:
`project_registry/` is the repository-level entrance for naming rules,
project-local ID maps, external source prefixes, asset rights, and large
source package records. It preserves source provenance for human review.

简体中文：
`project_registry/` 是仓库级登记入口，用于查看命名规则、本项目 ID
映射、外部来源前缀、资产权利和大型来源包记录。它为人工复核保留
来源追溯链。

## Human Review Entry Order / 人工复核入口顺序

English:
Use the registry in this order:

1. Open the relevant object-local dossier or review sheet first.
2. Open `001_repository-structure-and-naming-rules/` for path rules.
3. Open `002_project-id-to-source-reference-map/` for ID maps.
4. Open `003_external-source-prefixes/` for source abbreviations.
5. Open `004_asset-source-and-rights-index/` for asset rights.
6. Open `006_large-source-register/` for the large-source register.
7. Return to the object-local dossier before recording review outcomes.

简体中文：
使用登记表时，先打开对象目录内档案或人工复核表，再查路径规则、
ID 映射、来源前缀、资产权利和大型来源登记。记录复核结果前，要
回到对象目录内档案核对。

## Main Areas / 主要分区

- `001_repository-structure-and-naming-rules/` records path rules.
- `002_project-id-to-source-reference-map/` maps repository IDs to sources.
- `003_external-source-prefixes/` lists source system abbreviations.
- `004_asset-source-and-rights-index/` records asset provenance and rights.
- `006_large-source-register/` records oversized or risky source packages.

## Concrete Questions To Check / 具体待查问题

- Which object-local dossier needs this registry row?
- Which project-local ID, external ID, source system, or catalog is cited?
- Which source provenance row proves the access or download route?
- Does the asset rights index give rights status and a visible risk note?
- Does the large-source register record size, checksum, and storage hint?
- Which manifest, field map, or extraction note supports a derivative?
- Which missing source, rights, checksum, or review status remains?
- 哪个对象目录内档案需要这条登记记录？
- 引用了哪个本项目 ID、外部 ID、来源系统或著录？
- 哪条来源追溯记录证明访问或下载路线？
- 资产权利索引是否给出权利状态和显式风险提示？
- 大型来源登记是否记录大小、checksum 和存放线索？
- 哪个 manifest、字段映射或抽取说明支持派生记录？
- 还缺哪个来源、权利、checksum 或复核状态？

## Research Boundary / 研究边界

English:
Registry rows are source provenance and routing records. They are not
scholarship, not a rights decision, not corpus import approval, not an object
identity claim, and not a decipherment conclusion.

简体中文：
登记表行只是来源追溯和复核路线记录。它们不是学术结论，不是权利
决定，不是语料导入批准，不是对象身份判断，也不是释读结论。
