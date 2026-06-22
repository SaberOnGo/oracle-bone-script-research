# Schemas / 数据结构

English:
Schemas define machine-readable contracts for character records, inscription
records, source records, graph edges, asset metadata, and AI evidence-pack
drafts. They are machine-readable support for human research dossiers.

简体中文：
本目录定义甲骨单字、卜辞、来源、图边、资产 metadata 和 AI 证据包
草稿的机器可读契约。schema 只是服务人类研究档案的辅助资料。

## Human Review Entry Order / 人工复核入口顺序

English:
Use schemas in this order:

1. Open the object-local dossier, review sheet, or source note first.
2. Check the source provenance, rights status, and review status.
3. Open the JSON, CSV, graph edge, or evidence-pack file only after that.
4. Use the schema to verify field names, required status, and route shape.
5. Preserve candidate status and review status when data is incomplete.
6. Record missing evidence as concrete next checks in a human-readable file.
7. Treat a passing schema check as structure-only validation.

简体中文：
使用 schema 时，按以下顺序处理：

1. 先打开对象目录内的档案、复核表或来源说明。
2. 核对来源追溯、权利状态和复核状态。
3. 然后再打开 JSON、CSV、图边或 evidence-pack 文件。
4. 用 schema 检查字段名、必需状态和路线结构。
5. 资料不完整时，必须保留候选状态和复核状态。
6. 缺失证据要写入人类可读文件中的具体待查问题。
7. schema 通过只说明结构合格，不说明学术内容已确认。

## Current Schema Areas / 当前 schema 分区

- `001_character-record-schema/` checks oracle-character record structure.
- `002_inscription-record-schema/` checks inscription record structure.
- `003_source-record-schema/` checks source and provenance fields.
- `004_graph-edge-schema/` checks relationship graph edge shape.
- `005_asset-metadata-schema/` checks asset metadata fields.
- `006_ai-agent-evidence-pack-schema/` checks AI evidence-pack drafts.

## Concrete Questions To Check / 具体待查问题

- Which object-local dossier does this JSON or CSV support?
- Which source provenance row justifies the external ID and route?
- Does the record keep candidate status instead of promoting a claim?
- Does the record keep review status instead of implying confirmation?
- Are missing images, inscriptions, pages, rights, or fields named directly?
- Does a graph edge remain a route rather than a scholarly conclusion?
- 这个 JSON 或 CSV 服务于哪个对象目录内档案？
- 哪条来源追溯记录支持外部 ID 和路线？
- 记录是否保留候选状态，而不是提升为结论？
- 记录是否保留复核状态，而不是暗示已经确认？
- 缺失图片、卜辞、页码、权利或字段是否被具体写出？
- 图边是否仍只是路线，而不是学术结论？

## Research Boundary / 研究边界

English:
A schema validates structure, not scholarly truth. Passing schema validation
does not confirm a reading, component assignment, inscription identity,
source identity, evolution route, or paleographic correspondence. It is not a
decipherment conclusion. This is not a decipherment conclusion.

简体中文：
schema 校验的是结构，不是学术真实性。通过 schema 不等于确认释读、
构件归属、卜辞身份、来源身份、演化路线或古文字对应关系。它不是
释读结论。这不是释读结论。
