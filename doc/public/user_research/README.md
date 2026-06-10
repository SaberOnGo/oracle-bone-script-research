# User And AI Agent Research Drafts / 用户与 AI Agent 研究草稿

English:
This directory is for exploratory research created by users, contributors, or AI Agents. It may contain hypotheses, comparison notes, evidence packs, review logs, and rejected ideas.

简体中文：
本目录用于保存普通用户、贡献者或 AI Agent 的探索性研究。可以包含假说、对比笔记、证据包、复核记录和被否定的想法。

## Rules / 规则

- Mark every note as `draft`, `hypothesis`, `needs_review`, or `reviewed`.
- 每份笔记都要标记为 `draft`、`hypothesis`、`needs_review` 或 `reviewed`。
- Do not present content here as published scholarship.
- 不要把本目录内容当作已发表学术研究。
- If a draft matures into a sourced scholarship note, rewrite it and move the sourced version under `research/`.
- 如果草稿成熟为有来源的学术笔记，应改写后把有来源版本移入 `research/`。
- AI Agent evidence-pack drafts should follow `schemas/006_ai-agent-evidence-pack-schema/ai-agent-evidence-pack.schema.json`.
- AI Agent 证据包草稿应遵循 `schemas/006_ai-agent-evidence-pack-schema/ai-agent-evidence-pack.schema.json`。
- Empty scaffold evidence packs must keep evidence sections as `not_collected` and must not claim decipherment.
- 空白证据包骨架必须把证据章节保持为 `not_collected`，不得声称已经完成释读。

## Current Draft Areas / 当前草稿区

- `001_ai-agent-evidence-packs/`: empty AI Agent evidence-pack drafts and examples; sections marked `not_collected` are not evidence.
- `001_ai-agent-evidence-packs/`：空白 AI Agent 证据包草稿和示例；标记为 `not_collected` 的章节不是证据。
- `002_cross-source-review-queues/`: empty cross-source review log drafts generated from graph-source scaffolds; they route later evidence collection but do not promote source records, graph edges, component assignments, evolution chains, or decipherment conclusions.
- `002_cross-source-review-queues/`：从 graph-source scaffold 生成的空白交叉来源复核日志草稿；它们只为后续证据收集提供路由，不提升来源记录、图谱边、构件判定、演化链或释读结论。
- `003_evidence-collection-tasks/`: empty evidence-collection note drafts generated from task queues; they identify route files to open but do not contain collected evidence or promotion decisions.
- `004_codepoint-crosswalk-review-queues/`: empty codepoint crosswalk review-log drafts for HUST/OBIMD/EVOBC matched rows; they route later evidence collection and must not be read as identity, reading, component, evolution-chain, or decipherment conclusions.
- `003_evidence-collection-tasks/`：从任务队列生成的空白证据收集记录草稿；它们只标出待打开路由文件，不包含已收集证据或提升决定。
