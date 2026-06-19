# Project Registry / 项目注册表

English:
`project_registry/` is the first place to understand repository structure, naming rules, project-local IDs, external source IDs, asset provenance, large-source handling, and bilingual terminology.

简体中文：
`project_registry/` 是理解仓库结构、命名规则、本项目 ID、外部来源 ID、资产出处、大型来源处理和中英术语的第一入口。

## Purpose / 用途

- Keep file paths short while preserving source traceability.
- 在保持路径简短的同时保留来源可追溯性。
- Map project-local IDs to external catalogs, databases, plate numbers, old catalog numbers, URLs, rights status, and review status.
- 把本项目 ID 映射到外部字编、数据库、图版号、旧著录号、URL、权利状态和复核状态。
- Help humans and AI Agents answer where each record, object, asset, or derived table came from.
- 帮助人类和 AI Agent 回答每条记录、对象、资产或派生表来自哪里。
- Track large external source packages that are too big or too risky for regular Git while preserving checksums, storage hints, and derived record paths.
- 追踪不适合进入普通 Git 的大型或高风险外部来源包，同时保留 checksum、存放线索和派生记录路径。

## Main Areas / 主要区域

- `001_repository-structure-and-naming-rules/`: path and naming rules.
- `002_project-id-to-source-reference-map/`: project-local ID to external reference maps.
- `003_external-source-prefixes/`: source prefix and external ID prefix registry.
- `004_asset-source-and-rights-index/`: asset provenance, rights status, and size-limit exceptions.
- `006_large-source-register/`: large source package register and download log.

## Boundary / 边界

English:
Registry rows are provenance and routing records. They do not confirm readings, component assignments, inscription identities, or paleographic correspondences by themselves.

简体中文：
注册表行是来源追溯和研究路径记录。它们本身不确认释读、构件归属、卜辞身份或古文字对应关系。
