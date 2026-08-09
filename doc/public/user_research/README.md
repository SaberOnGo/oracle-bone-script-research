# User And AI Agent Research Drafts / 用户与 AI Agent 研究草稿

English:
This directory is for exploratory research created by users, contributors,
or AI Agents. It may contain hypotheses, comparison notes, evidence packs,
review logs, and rejected ideas.

简体中文：
本目录用于保存普通用户、贡献者或 AI Agent 的探索性研究。可以包含假说、
对比笔记、证据包、复核记录和被否定的想法。

## Rules / 规则

- Mark every note as `draft`, `hypothesis`, `needs_review`, `reviewed`, or
  `deprecated`.
- 每份笔记都要标记为 `draft`、`hypothesis`、`needs_review`、`reviewed`
  或 `deprecated`。
- Do not present content here as published scholarship.
- 不要把本目录内容当作已发表学术研究。
- If a draft matures into a sourced scholarship note, rewrite it and move the
  sourced version under `research/`.
- 如果草稿成熟为有来源的学术笔记，应改写后把有来源版本移入
  `research/`。
- AI Agent evidence-pack drafts should follow the schema under
  `schemas/006_ai-agent-evidence-pack-schema/`.
- AI Agent 证据包草稿应遵循
  `schemas/006_ai-agent-evidence-pack-schema/` 下的 schema。
- Empty scaffold evidence packs must keep evidence sections as
  `not_collected` and must not claim decipherment.
- 空白证据包骨架必须把证据章节保持为 `not_collected`，不得声称已经完成
  释读。

## Strategy Status Mapping / 战略状态映射

The v1 `status` is a pack-lifecycle field. The strategy's
`delivery_status=ai_adjudicated_candidate` belongs in a separate versioned
adjudication record. `reviewed` does not by itself mean delivered, published,
or confirmed scholarship.

v1 `status` 是证据包生命周期字段。战略中的
`delivery_status=ai_adjudicated_candidate` 应放在独立、版本化的裁决记录
中。`reviewed` 本身不表示已交付、已发表或已确认学术结论。

The [v2 benchmark and adjudication contract][schema-007] is separate from v1.
Active generated runs belong in the ignored
`generated/ai-agent-benchmark-experiments/` directory. Private gold must stay
outside Git.

[v2 基准与裁决合同][schema-007]与 v1 分离。进行中的生成实验放在被忽略的
`generated/ai-agent-benchmark-experiments/`。私有 gold 必须留在 Git 外。

## v2 Candidate Delivery / v2 候选交付

Each benchmark must contain masked-known, historically disputed, null or
negative-control, and hard-challenge cases. Each case uses a blind alias,
evidence cutoff, checksummed source snapshots, training-cutoff evidence, and a
source and image-derivative dependency manifest. Its closed candidate universe
must include `unknown_or_other`.

每个 benchmark 必须包含隐藏已释案、历史争议案、空白或负对照及困难
挑战案。每案使用盲别名、证据时间截点、带 checksum 的来源快照、训练截止
证据，以及来源与图片派生依赖 manifest。封闭候选全集必须包含
`unknown_or_other`。

Same-model runs are execution reruns only. Model-independent reruns use a
separate role and independence tier. Candidate delivery requires both a
model-independent rerun and at least two reviewed independent evidence
families.

同模型运行只能算执行复跑。模型独立复跑使用单独角色和独立等级。候选
交付必须具备模型独立复跑，以及至少两个经复核的独立证据家族。

Every delivered candidate must lead with a complete bilingual human delivery
package. It links object dossiers, inscription contexts, source evidence, the
adjudication memo, dependency graph, and claim-evidence matrix. Rights and
content reviews must be complete, with no blocking missing item.

每个已交付候选都必须以完整双语人类交付包为入口，链接对象档案、卜辞
上下文、来源证据、裁决说明、依赖图和主张证据矩阵。权利与内容复核必须
完成，且不能存在 blocking 缺失项。

Ignored-local gold is diagnostic only. Candidate delivery requires a clean
holdout scored once by an external isolated scorer and then retired. A
validator `PASS`, including a structure-only pass with
`METRICS_NOT_RECOMPUTED`, does not itself authorize delivery.

本地忽略 gold 只能用于诊断。候选交付要求干净留出集由外部隔离评分器
评分一次后退役。validator `PASS`，包括带 `METRICS_NOT_RECOMPUTED` 的
公开结构通过，本身不构成交付授权。

Every source and evidence item must expose its rights status, risk note,
allowed delivery form, large-source register reference, checksum, and
dependency review. Follow the [strategy], [v1 schema][schema-006],
[rights policy], and [large-source policy].

每个来源与证据项都必须展示权利状态、风险提示、允许交付形式、大来源
登记引用、checksum 和依赖复核。应遵循[战略][strategy]、
[v1 schema][schema-006]、[权利政策][rights-policy]和
[大型来源政策][large-source-policy]。

An `ai_adjudicated_candidate` is still an AI candidate under
`benchmark_experiment_not_scholarship`. It is not confirmed scholarship and
does not move automatically into `research/`.

`ai_adjudicated_candidate` 仍是
`benchmark_experiment_not_scholarship` 边界内的 AI 候选，不是已确认学术
结论，也不会自动移入 `research/`。

## Current Draft Areas / 当前草稿区

- `001_ai-agent-evidence-packs/`: empty evidence-pack drafts and examples.
  Sections marked `not_collected` are not evidence.
- `001_ai-agent-evidence-packs/`：空白证据包草稿和示例。
  标记为 `not_collected` 的章节不是证据。
- `002_cross-source-review-queues/`: empty cross-source review drafts.
  They route evidence collection but do not promote claims or graph edges.
- `002_cross-source-review-queues/`：空白交叉来源复核草稿。
  它们只提供证据路线，不提升主张或图边。
- `003_evidence-collection-tasks/`: empty evidence-collection notes.
  They name routes but contain no collected evidence or promotion decision.
- `003_evidence-collection-tasks/`：空白证据收集记录。
  它们只标出路线，不包含已收集证据或提升决定。
- `004_codepoint-crosswalk-review-queues/`: empty HUST, OBIMD, and EvoBC
  crosswalk reviews. They are not identity or decipherment conclusions.
- `004_codepoint-crosswalk-review-queues/`：HUST、OBIMD 和 EvoBC 的空白
  crosswalk 复核。它们不是身份或释读结论。
- `005_undeciphered-candidate-review-queues/`: empty HUST `obs-unk-*`
  reviews. They do not assign a reading, component, or formal `obs-char` ID.
- `005_undeciphered-candidate-review-queues/`：HUST `obs-unk-*` 空白复核。
  它们不分配释读、构件或正式 `obs-char` ID。
- `006_undeciphered-candidate-evidence-collection-tasks/`: empty HUST
  `obs-unk-*` evidence tasks. They remain `not_collected` until reviewed.
- `006_undeciphered-candidate-evidence-collection-tasks/`：HUST
  `obs-unk-*` 空白证据任务。复核前保持 `not_collected`。

[strategy]: ../../project/005_ai-agent-research-assistant-design/
[schema-006]: ../../../schemas/006_ai-agent-evidence-pack-schema/
[schema-007]: ../../../schemas/007_ai-agent-benchmark-experiment-schema/
[rights-policy]: ../../project/002_source-rights-and-provenance-policy/
[large-source-policy]: ../../project/006_large-source-material-handling/
