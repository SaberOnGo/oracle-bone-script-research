# Oracle Bone Script Research

[简体中文](README.zh-CN.md)

## Mission / 项目使命

English:

This repository is a human-first oracle bone script research
infrastructure project. It gives oracle-bone scholars, archaeologists,
and other human researchers a place to read, verify, compare, and extend
source materials before formal research begins.

It is not an automatic decipherment model. Machine-readable files,
including JSON, CSV, manifests, staging tables, and graph edges, are
AI-readable support data. They help search, provenance review, statistics,
and validation, but they do not replace human-readable research dossiers.

简体中文：

中文摘要：

本仓库首先是面向甲骨文学者、考古学者和其他人类研究者的资料库。
它用于阅读、核查、比较和继续整理甲骨资料，然后才为 AI 提供索引
和结构化辅助数据。

本项目不是自动释读模型。JSON、CSV、manifest、staging 表和图谱边
都是 AI 可读辅助资料，只服务检索、来源追溯、统计和校验，不能替代
人类可读研究档案。

## Current Stage / 当前阶段

English:

The current stage is pre-formal-research organization and preprocessing.
Work should collect, normalize, and connect images, rubbings, photographs,
catalog records, inscriptions, plates, find spots, museum holdings, periods,
source trails, and review status.

No unreviewed AI hypothesis may be presented as confirmed scholarship.
Unconfirmed material must be marked as candidate, source record, disputed,
to be checked, or pending review.

简体中文：

当前阶段是正式研究开始前的资料整理和预处理。工作重点是收集、清洗
和关联实物、拓片、照片、著录、卜辞、图版、出土地、馆藏、时期、
来源链和复核状态。

不得把未经复核的 AI 假说写成已确认的学术结论。未确认内容必须标为
候选、来源记录、争议、待查或待复核。

## AI Candidate Strategy / AI 候选战略

Independent AI agents may now investigate, falsify, rerun, calibrate, and
adjudicate hypotheses. A candidate may be delivered directly to the user
without prior human-specialist approval only through a versioned adjudication
record that demonstrates every registered gate.

独立 AI Agent 可以调查、反证、复跑、校准并裁决假说。候选只有通过版本化
裁决记录证明全部预登记门槛后，才能在没有真人专家预先批准的情况下提交给用户。

`ai_adjudicated_candidate` is a separate user-facing delivery overlay, not a
value for the legacy v1 evidence-pack `status` or `assignment_status` fields.
It may be used only when a versioned adjudication record passes every
registered calibration, leakage, falsification, rerun, rights, and delivery
gate. This repository currently has no public v2 experiment record, so no
candidate is authorized by this entry page. The normative design is the
[AI autonomous candidate strategy][ai-strategy].

`ai_adjudicated_candidate` 是面向用户的独立交付叠加层，不是旧版 v1
evidence-pack 的 `status` 或 `assignment_status` 字段值。只有版本化裁决
记录通过校准、泄漏、反证、复跑、权利和交付全部门槛后才能使用它。
当前仓库没有公开 v2 实验记录，因此本入口页不授权交付任何候选。规范性
设计见[AI Agent 自主候选裁决战略][ai-strategy]。

## Human Research Entry Order / 人工研究入口顺序

English:

1. Open the object-local dossier for the character, inscription, plate, or
   source package.
2. Read the human Markdown first: visual observations, catalog trail,
   inscription context, source notes, disputes, and concrete missing items.
3. Use the AI-readable support data only after the human dossier is clear.
4. Trace every source through `project_registry/` before reusing a claim.
5. Treat graph edges and statistics as navigation signals, not conclusions.

简体中文：

1. 先打开单字、卜辞、图版或来源包所在的对象目录。
2. 先读人类 Markdown：字形观察、著录链、卜辞上下文、来源说明、
   争议和具体缺失项。
3. 只有在人类档案清楚之后，再使用 AI 可读辅助资料。
4. 复用任何判断前，先通过 `project_registry/` 追溯来源。
5. 图谱边和统计只作为导航信号，不作为结论。

## Concrete Questions To Check / 具体待查问题

- Which image, rubbing, plate, or catalog record is the visible evidence?
- Which source supplied each field, and what rights status applies?
- Is the object directory holding both the human dossier and support data?
- Which inscription context, find spot, period, group, or museum record is
  still missing?
- Which readings or modern labels are only candidates or disputed records?

- 哪一张图片、拓片、图版或著录记录是可见证据？
- 每个字段来自哪一个来源，权利状态是什么？
- 对象目录内是否同时放有人类档案和辅助数据？
- 还缺哪一条卜辞上下文、出土地、时期、组类或馆藏记录？
- 哪些释读或今字标签只是候选、来源记录或争议项？

## Main Entry Points / 主要入口

- `AGENTS.md`: mandatory agent rules and validation requirements.
- `project_registry/`: source provenance, rights, and large-source records.
- `doc/project/`: project boundaries, provenance policy, and record model.
- `doc/project/005_ai-agent-research-assistant-design/`: normative AI
  candidate adjudication strategy.
- `corpus/`: object-local research dossiers and support files.
- `schemas/`: machine-readable contracts for support data.
- `tools/`: generators, validators, audits, and import helpers.

## Validation / 校验

Run these checks before committing repository skeleton, docs, schemas, or
scripts:

```powershell
python tools/validation/check_repository_skeleton.py
python -m unittest discover -s tests -v
git diff --check
```

[ai-strategy]: doc/project/005_ai-agent-research-assistant-design/
