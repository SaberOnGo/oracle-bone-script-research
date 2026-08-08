# AI Agent Evidence Pack Schema / AI Agent 证据包结构

English:
This schema defines the draft evidence pack format used by AI Agents before any
oracle bone script decipherment claim is made. A valid evidence pack records the
candidate ID route, source references, missing evidence, supporting evidence,
opposing evidence, and review log. It is a research draft contract, not a
published scholarship format.

Simplified Chinese:
本 schema 定义 AI Agent 在提出任何甲骨文释读结论之前使用的证据包草稿格式。
合格的证据包需要记录候选 ID 路由、资料来源、缺失证据、支持证据、反对证据
和复核记录。它是研究草稿合同，不是已发表学术成果格式。

## Boundary / 边界

- `research_boundary` must be `draft_not_scholarship`.
- `assignment_status` must stay `reserved_candidate_not_assigned` until human
  review promotes the candidate into the formal character corpus.
- Empty scaffold drafts should mark evidence sections as `not_collected`.
- Drafts belong under `doc/public/user_research/`, not under root `research/`.

- `research_boundary` 必须为 `draft_not_scholarship`。
- `assignment_status` 在人工复核正式提升之前必须保持
  `reserved_candidate_not_assigned`。
- 空草稿中的证据章节应标记为 `not_collected`。
- 草稿应放在 `doc/public/user_research/`，不要放入根目录 `research/`。

## Strategy Compatibility / 战略兼容

This v1 schema does not encode the strategy's `delivery_status` axis.
`ai_adjudicated_candidate` is therefore not a valid value for this schema's
`status` or `assignment_status` fields. A v1 pack may remain a hypothesis
while a separate, versioned adjudication record authorizes delivery to the
user.

The value `candidate_promoted_after_human_review` refers only to promotion
into the formal character corpus. It is not a prerequisite for AI candidate
delivery and it does not mean confirmed scholarship.

本 v1 schema 不编码战略中的 `delivery_status` 轴。因此，
`ai_adjudicated_candidate` 不是本 schema 的 `status` 或
`assignment_status` 合法值。v1 证据包可以继续保持 hypothesis，同时由
独立、版本化的裁决记录授权向用户交付。

`candidate_promoted_after_human_review` 只表示提升进入正式单字语料，不是
AI 候选交付的前置条件，也不表示已确认学术结论。
