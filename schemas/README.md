# Schemas / 数据结构

English:
Schemas define machine-readable contracts for character records, inscription
records, source records, graph edges, asset metadata, AI evidence-pack drafts,
and reproducible AI benchmark experiments. They are machine-readable support
for human research dossiers.

简体中文：
本目录定义甲骨单字、卜辞、来源、图边、资产 metadata、AI 证据包草稿和
可复跑 AI 基准实验的机器可读契约。schema 只是服务人类研究档案的
辅助资料。

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
使用 schema 时，先打开对象目录内档案、复核表或来源说明；核对来源
追溯、权利状态和复核状态后，再打开 JSON、CSV、图边或 evidence-pack
文件。schema 只验证结构，不证明学术内容已经确认。

## Current Schema Areas / 当前 schema 分区

- `001_character-record-schema/` checks oracle-character record structure.
- `002_inscription-record-schema/` checks inscription record structure.
- `003_source-record-schema/` checks source and provenance fields.
- `004_graph-edge-schema/` checks relationship graph edge shape.
- `005_asset-metadata-schema/` checks asset metadata fields.
- [schema 006][schema-006] checks AI evidence-pack drafts.
- [schema 007][schema-007] checks calibrated, blinded, reproducible AI
  benchmark and candidate-adjudication records.

Schema 006 remains the v1 draft lifecycle contract. Schema 007 is the separate
v2 benchmark, adjudication, scoring, and delivery contract. Neither silently
changes the fields or meaning of the other.

Schema 006 继续作为 v1 草稿生命周期合同。Schema 007 是独立的 v2 基准、
裁决、评分和交付合同；两者都不能静默改变另一方的字段或含义。

## v2 Validation And Delivery / v2 校验与交付

The v2 validator evaluates the complete JSON Schema first, then applies
cross-field gates. These gates require all four case types, blind aliases,
evidence cutoffs, source checksums, pretraining eligibility, dependency
manifests, and `unknown_or_other` in every candidate universe.

v2 validator 先执行完整 JSON Schema，再执行跨字段门禁。门禁要求四类案件
齐全，每案具有盲别名、证据时间截点、来源 checksum、预训练资格和依赖
manifest，并在每个候选全集中包含 `unknown_or_other`。

A same-model repeat is an execution rerun only. A delivery record requires a
separately marked model-independent rerun, a scorer-derived clean holdout, an
external isolated scorer, one-shot scoring followed by retirement, a complete
human delivery package, and at least two reviewed independent evidence
families.

同模型重复只能算执行复跑。交付记录要求单独标记模型独立复跑、scorer
派生的干净留出集、外部隔离评分器、一次评分后退役、完整人类交付包，
以及至少两个经复核的独立证据家族。

Ignored-local gold is diagnostic only. Every source snapshot and evidence item
must expose rights, risk, allowed delivery, large-source registration,
checksum, and dependency review. See the [strategy], [rights policy], and
[large-source policy].

本地忽略 gold 只能用于诊断。每个来源快照和证据项都必须展示权利、风险、
允许交付形式、大来源登记、checksum 和依赖复核。参见[战略][strategy]、
[权利政策][rights-policy]和[大型来源政策][large-source-policy]。

A public-record `PASS` with `METRICS_NOT_RECOMPUTED` is not metric verification
or delivery authorization. `ai_adjudicated_candidate` remains a candidate,
not confirmed scholarship.

带 `METRICS_NOT_RECOMPUTED` 的公开记录 `PASS` 不是指标复核或交付授权。
`ai_adjudicated_candidate` 仍是候选，不是已确认学术结论。

## Concrete Questions To Check / 具体待查问题

- Which object-local dossier does this JSON or CSV support?
- Which source provenance row justifies the external ID and route?
- Does the record keep candidate status instead of promoting a claim?
- Does the record keep review status instead of implying confirmation?
- Are missing images, inscriptions, pages, rights, or fields named directly?
- Does a graph edge remain a route rather than a scholarly conclusion?
- Is a candidate probability calibrated from a locked, family-separated set?
- Does an out-of-domain case withhold numeric candidate delivery?
- Did the external scorer retire the clean holdout after exactly one score?
- Is the bilingual human delivery package complete and free of blockers?
- Do two dependency-reviewed evidence families permit the delivery form?
- 这个 JSON 或 CSV 服务于哪个对象目录内档案？
- 哪条来源追溯记录支持外部 ID 和路线？
- 记录是否保留候选状态，而不是提升为结论？
- 记录是否保留复核状态，而不是暗示已经确认？
- 缺失图片、卜辞、页码、权利或字段是否被具体写出？
- 图边是否仍只是路线，而不是学术结论？
- 候选概率是否来自已锁定并按资料家族分割的校准集？
- 域外案件是否停止数值候选交付？
- 外部 scorer 是否在一次评分后退役干净留出集？
- 双语人类交付包是否完整且没有阻断项？
- 是否有两个通过依赖复核的证据家族允许该交付形式？

## Research Boundary / 研究边界

English:
A schema validates structure, not scholarly truth. Passing schema validation
does not confirm a reading, component assignment, inscription identity,
source identity, evolution route, or paleographic correspondence.
It is not a decipherment conclusion and not a scholarly confirmation.

简体中文：
schema 校验的是结构，不是学术真实性。通过 schema 不等于确认释读、
构件归属、卜辞身份、来源身份、演化路线或古文字对应关系。它不是释读结论。

[strategy]: ../doc/project/005_ai-agent-research-assistant-design/
[schema-006]: 006_ai-agent-evidence-pack-schema/
[schema-007]: 007_ai-agent-benchmark-experiment-schema/
[rights-policy]: ../doc/project/002_source-rights-and-provenance-policy/
[large-source-policy]: ../doc/project/006_large-source-material-handling/
