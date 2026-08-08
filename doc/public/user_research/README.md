# User And AI Agent Research Drafts / 用户与 AI Agent 研究草稿

English:
This directory is for exploratory research created by users, contributors,
or AI Agents. It may contain hypotheses, comparison notes, evidence packs,
review logs, and rejected ideas.

简体中文：
本目录用于保存普通用户、贡献者或 AI Agent 的探索性研究。可以包含假说、对比笔记、证据包、复核记录和被否定的想法。

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
