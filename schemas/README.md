# Schemas / 数据结构

English:
Schemas define the machine-readable contracts for character records, inscription records, source records, graph edges, asset metadata, and AI Agent evidence-pack drafts. They make corpus records easier to validate, compare, import, and review.

简体中文：
schemas 定义甲骨字记录、卜辞记录、来源记录、图边、资产 metadata 和 AI Agent evidence pack 草稿的机器可读契约。它们让语料记录更容易校验、比较、导入和复核。

## Use / 用途

- Validate JSON records before they are promoted or reused.
- 在记录提升或复用前校验 JSON。
- Keep field names stable across scripts, tests, and object-local packets.
- 让脚本、测试和对象内 packet 使用稳定字段名。
- Preserve candidate and review status instead of silently converting metadata into scholarship.
- 保留候选状态和复核状态，避免把 metadata 悄悄变成学术结论。
- Support future import into databases, knowledge graphs, dashboards, and AI Agent context packs.
- 支持未来导入数据库、知识图谱、仪表盘和 AI Agent context pack。

## Boundary / 边界

English:
A schema validates structure, not scholarly truth. Passing schema validation does not confirm a decipherment, component assignment, inscription identity, or paleographic correspondence.

简体中文：
schema 校验的是结构，不是学术真实性。通过 schema 校验并不确认释读、构件归属、卜辞身份或古文字对应关系。
