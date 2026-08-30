# 甲骨文开放研究项目

[English](README.md)

## 项目使命 / Mission

简体中文：

本仓库首先是面向甲骨文学者、考古学者和其他人类研究者的资料库。
它用于阅读、核查、比较和继续整理甲骨资料，然后才为 AI 提供索引
和结构化辅助数据。

本项目不是自动释读模型。JSON、CSV、manifest、staging 表和图谱边
都是 AI 可读辅助资料，只服务检索、来源追溯、统计和校验，不能替代
人类研究档案。

English summary:

This repository is a human-first oracle bone script research
infrastructure project. It supports reading, verification, comparison, and
continued material organization before formal scholarship begins. It is not
an automatic decipherment model.

## 当前阶段 / Current Stage

当前阶段是正式研究开始前的资料整理和预处理。工作重点是收集、清洗
和关联实物、拓片、照片、著录、卜辞、图版、出土地、馆藏、时期、
来源链和复核状态。

不得把未经复核的 AI 假说写成已确认的学术结论。未确认内容必须标为
候选、来源记录、争议、待查或待复核。

[当前运行基线][current-baseline]列出少量当前可证伪裁决及其下一项决定性
来源缺口。

## AI 候选战略 / AI Candidate Strategy

独立 AI Agent 可以调查、反证、复跑、校准并裁决假说。候选只有通过版本化
裁决记录证明全部预登记门槛后，才能在没有真人专家预先批准的情况下提交给用户。

`ai_adjudicated_candidate` 是面向用户的独立交付叠加层，不是旧版 v1
evidence-pack 的 `status` 或 `assignment_status` 字段值。只有版本化裁决
记录通过校准、泄漏、反证、复跑、权利和交付全部门槛后才能使用它。
当前仓库没有公开 v2 实验记录，因此本入口页不授权交付任何候选。规范性
设计见[AI Agent 自主候选裁决战略][ai-strategy]。

Independent AI agents may investigate, falsify, rerun, calibrate, and
adjudicate hypotheses. A candidate may be delivered without prior
human-specialist approval only through a versioned adjudication record that
passes every registered gate. It remains a high-confidence AI candidate, not
confirmed scholarship.

## 人工研究入口顺序 / Human Research Entry Order

1. 先打开单字、卜辞、图版或来源包所在的对象目录。
2. 先读人类 Markdown：字形观察、著录链、卜辞上下文、来源说明、
   争议和具体缺失项。
3. 只有在人类档案清楚之后，再使用 AI 可读辅助资料。
4. 复用任何判断前，先通过 `project_registry/` 追溯来源。
5. 图谱边和统计只作为导航信号，不作为结论。

## 具体待查问题 / Concrete Questions To Check

- 哪一张图片、拓片、图版或著录记录是可见证据？
- 每个字段来自哪一个来源，权利状态是什么？
- 对象目录内是否同时放有人类档案和辅助数据？
- 还缺哪一条卜辞上下文、出土地、时期、组类或馆藏记录？
- 哪些释读或今字标签只是候选、来源记录或争议项？

## 对象目录 / Object-Local Dossiers

每个具体对象目录都应同时放人类可读研究资料和 AI 可读辅助资料。
不得另建并行的人类目录。单字目录应像一个考古和文字学档案夹，
让研究者打开后能直接查看字形图片、字形观察、异体、近形、构件线索、
所在卜辞、图版、著录号、合集号、出土地、馆藏、时期、组类、来源证据、
释读史、争议、后世字形关联、缺失项和下一步待查来源。

## 来源追溯 / Source Provenance

每个来源都要有访问或下载记录、checksum、大小、权利状态、风险提示、
manifest、解包清单、字段映射、异常、派生路径和复核状态。超过
`SIZE_LIMIT` 的原始包应留在忽略区或外部归档，Git 中只保留可审计的
来源记录和可复核派生结果。

## 主要入口 / Main Entry Points

- `AGENTS.md`：Agent 必读规则和校验要求。
- `project_registry/`：来源链、权利状态和大文件登记。
- `doc/project/`：项目边界、来源政策和记录模型。
- `doc/project/005_ai-agent-research-assistant-design/`：规范性的 AI 候选
  裁决战略。
- `corpus/`：对象内人类研究档案和辅助文件。
- `schemas/`：辅助数据的机器可读契约。
- `tools/`：生成器、校验器、审计和导入工具。

## 校验 / Validation

提交仓库骨架、文档、schema 或脚本前运行：

```powershell
python tools/validation/check_repository_skeleton.py
python -m unittest discover -s tests -v
git diff --check
```

[ai-strategy]: doc/project/005_ai-agent-research-assistant-design/
[current-baseline]: doc/project/005_ai-agent-research-assistant-design/
