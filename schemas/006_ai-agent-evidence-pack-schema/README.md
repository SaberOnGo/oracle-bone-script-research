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
