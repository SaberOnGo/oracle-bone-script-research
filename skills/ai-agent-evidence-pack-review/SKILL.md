---
name: ai-agent-evidence-pack-review
description: >-
  Use when preparing, reviewing, or critiquing an AI Agent evidence pack,
  decipherment hypothesis, or user research draft for oracle bone analysis.
---

# AI Agent Evidence Pack Review / AI Agent 证据包复核

## Use This Skill When / 何时使用

English:
Use this skill before asking an AI Agent to produce or review a
decipherment-support hypothesis.

简体中文：
在让 AI Agent 生成或复核释读辅助假说前使用本 skill。

## Required Reading / 必读

- `AGENTS.md`
- `doc/project/005_ai-agent-research-assistant-design/README.md`
- `doc/project/004_oracle-bone-script-research-methods/README.md`
- `doc/public/user_research/README.md`
- [strategy](../../doc/project/005_ai-agent-research-assistant-design/)

The linked directory contains the claim matrix at
`02_claim-evidence-gate-matrix.md`.

## Evidence Pack Must Include / 证据包必须包含

- Character or unknown glyph ID / 甲骨字或未知字 ID
- Source references and asset metadata / 来源引用与资产 metadata
- Full inscription context / 卜辞全文上下文
- Neighboring characters / 周边字
- Component breakdown and variant notes / 构件拆分与变体笔记
- Excavation, period, and catalog provenance / 出土、时代和著录来源
- Comparable bronze, seal, or modern forms when available / 可用时的金文、小篆或今文比较
- Supporting evidence / 支持证据
- Opposing evidence / 反对证据
- Open questions and next checks / 未决问题和下一步检查

## Claim Gate Before Hypothesis / 假说前命题门槛

Apply the [claim evidence gate matrix][claim-matrix] before proposing a
reading, meaning, grammar function, component, variant, or diachronic link.
For every applicable claim, record its `claim_id`, evidence state, independent
family IDs, mandatory blockers, counterevidence, and one concrete next-source
question in the human dossier.

在提出读音、意义、语法功能、构件、异体或历时关系前，必须应用[命题证据
门槛矩阵][claim-matrix]。对每个适用命题，在人类档案中记录 `claim_id`、
证据状态、独立家族 ID、必需阻断项、反证和一个具体下一来源问题。

`route_only`, `source_reported`, or missing mandatory evidence is a blocker.
A v1 schema pass, a modern-label match, or an Agent self-score cannot clear
the blocker. If C4--C7 is incomplete, the Agent must abstain from reading,
meaning, grammar, or correspondence claims and may only return a source route,
candidate relation, or withheld decision.

`route_only`、`source_reported` 或缺失必需证据都是阻断项。v1 schema 通过、
现代标签匹配或 Agent 自评分都不能解除阻断。若 C4--C7 不完整，Agent 必须
对读音、意义、语法或对应关系弃权，只能返回来源路线、关系候选或扣留决定。

The matrix controls delivery semantics, not the v1 lifecycle enum. Keep v1
`status` in its existing values and keep `assignment_status` separate from
the strategy's `delivery_status`.

矩阵控制交付语义，不改 v1 生命周期枚举。v1 `status` 继续使用现有值，
`assignment_status` 与战略的 `delivery_status` 保持分离。

## Output Rule / 输出规则

English:
The legacy v1 evidence-pack `status` follows its existing lifecycle enum:
`draft`, `hypothesis`, `needs_review`, `reviewed`, or `deprecated`. Human
review controls only its separate `assignment_status` promotion into the
formal corpus. It is not a prerequisite for delivery through the strategy's
separate `ai_adjudicated_candidate` channel.

Until a versioned adjudication contract exists, do not write
`ai_adjudicated_candidate` into the v1 `status` or `assignment_status` fields.
Keep the pack under `doc/public/user_research/`, not under `research/`.

Temporary downloads, OCR intermediates, vector indexes, scratch comparisons,
and generated caches must stay in ignored temporary directories such as
`tmp/`, `_tmp/`, `scratch/`, `.working/`, or `.cache/`. Promote only reviewed,
source-marked evidence into Git.

简体中文：
旧版 v1 evidence-pack `status` 按现有生命周期枚举使用 `draft`、
`hypothesis`、`needs_review`、`reviewed` 或 `deprecated`。人工复核只控制
独立的 `assignment_status` 是否提升到正式语料，不是 AI 候选交付的前置
条件。规范性战略另行定义 `ai_adjudicated_candidate` 交付通道。

在版本化裁决契约落地前，不要把 `ai_adjudicated_candidate` 写入 v1 的
`status` 或 `assignment_status`。证据包继续放在
`doc/public/user_research/`，不要放在 `research/`。

临时下载、OCR 中间产物、向量索引、草稿对比和生成缓存必须放在
`tmp/`、`_tmp/`、`scratch/`、`.working/` 或 `.cache/` 等已忽略临时目录。
只有经过复核、标注来源的证据才可以提升进入 Git。

[claim-matrix]: ../../doc/project/005_ai-agent-research-assistant-design/
