# 甲骨文开放研究项目

<table align="center">
  <tr>
    <td align="center"><h3><a href="./README.zh-CN.md">简体中文</a></h3></td>
    <td align="center"><h3><a href="./README.md">English</a></h3></td>
  </tr>
</table>

本项目是“甲骨文知识库 + 知识图谱 + AI Agent 研究助手 + 开放研究基础设施”。

它不是自动破译甲骨文的模型，而是一个把甲骨单字、字形变体、构件候选、卜辞、馆藏/出土信息、来源引用、学术资料、图边、统计和 AI Agent 复核队列结构化的长期项目。目标是降低甲骨文研究的信息差和资料门槛，让普通人也能在规范证据框架下进行检索、比对、提问、假说生成和人工复核。

English summary: Oracle Bone Script Research is a knowledge base, knowledge graph, and AI Agent framework for democratizing access to oracle bone script research. It preserves source trails and review boundaries instead of presenting AI hypotheses as confirmed scholarship.

## 项目使命 / Mission

用 AI Agent 推动甲骨文研究民主化，同时保留来源追溯、复核状态和研究边界。

Democratize access to oracle bone script research with AI agents while preserving source provenance, review status, and research boundaries.

本项目重点整理：

- 甲骨单字结构化记录和未释字候选
- 字形图片、图片引用和来源 metadata
- 构件候选和 glyph-codepoint 关系
- 卜辞记录、著录记录和目录互证暂存表
- 馆藏、出土、时期、批次和图版出处
- 金文、小篆、后续文字阶段标签和现代 codepoint 对应候选
- 书目、来源登记、下载日志、manifest 和权利风险说明
- 关系图边、覆盖率统计、质量审计和复核队列
- 支持透明假说工作的 AI Agent evidence pack 和复核脚手架

## 当前阶段 / Current Stage

本仓库处于正式研究开始前的资料工程和预处理阶段。当前已经包含来源登记、下载日志、暂存表、对象内候选资料、图边、统计和校验工具。所有未确认内容都保持候选或待人工复核状态。

The repository is in the preprocessing and research-infrastructure stage. It already contains source registers, download logs, staging tables, object-local candidate materials, graph edges, statistics, and validation tools.

## 重要入口 / Important Entry Points

- `AGENTS.md`：所有 AI agent 必须先读的规则。
- `project_registry/`：仓库结构、命名规则、本项目 ID、外部来源引用、资产出处、大型来源登记和术语表。
- `doc/project/`：项目政策和研究设计。
- `corpus/`：甲骨字、卜辞、构件候选、字形对应候选、出处、图谱和统计记录。
- `research/`：已有学术研究、已发表观点和书目记录。
- `doc/public/user_research/`：用户和 AI Agent 的研究草稿、证据包、对比记录和复核记录。
- `skills/`：AI Agent 可复用工作流。
- `schemas/`：机器可校验的数据结构。
- `tools/`：校验、导入、抽取、图谱、统计和 context pack 生成脚本。
- `tests/`：仓库规则、脚本和数据契约测试。
- `tmp/`：本地临时工作区，用于 AI Agent 草稿、临时下载、OCR 中间产物、缓存和生成性临时文件。

## 研究边界 / Research Boundary

AI Agent 输出属于草稿研究。未经复核前应放在 `doc/public/user_research/`；已有学术研究和已发表观点应放在 `research/`。

AI Agent output is draft research. It belongs under `doc/public/user_research/` until reviewed and rewritten with reliable sources. Existing scholarship belongs under `research/`.

数据集标签、图边、codepoint 匹配、构件候选、目录互证和字形演化/对应候选都只是研究路径证据。不得把它们写成已确认释读、正式构件归属、卜辞身份或已接受的古文字对应关系。

Dataset labels, graph edges, codepoint matches, component candidates, catalog crosswalks, and evolution/correspondence candidates are routing evidence only, not confirmed scholarship.

## AI Agent 快速开始 / Quick Start

先读 `AGENTS.md`，再根据任务读取 `project_registry/`、`doc/project/`、`schemas/`、`skills/` 和 `tools/` 下的相关文件，然后再修改。

Read `AGENTS.md` first, then read the relevant project registry, policy, schema, skill, and tool files before editing.

```powershell
python tools/validation/check_repository_skeleton.py
python -m unittest discover -s tests -v
git diff --check
```

## 来源与风险政策 / Source And Risk Policy

研究需要时，可以下载或提交外部甲骨图片、扫描件、论文 PDF、大型图片集和研究语料。每个提交的资料项都必须注明来源、权利状态和显式风险提示，方便人类和 AI Agent 追溯出处并判断复用风险。

External oracle bone images, scans, paper PDFs, large image sets, and research corpora may be downloaded or committed when they are useful for research. Every committed item must include provenance, rights status, and a visible risk note.

`SIZE_LIMIT` 设为单文件 30 MiB。更大的文件需要登记特例，并优先考虑分包、降采样、压缩或抽取成结构化记录。达到或超过 40 MiB 的文件不得提交到普通 Git。

`SIZE_LIMIT` is 30 MiB per file. Files at or above 40 MiB must not be committed to regular Git.

超过限制但重要的来源包应登记到 `project_registry/006_large-source-register/`，原始包保存在已忽略的本地或外部存储中，Git 中只保留带来源标记的 manifest、checksum、抽取说明和已复核派生记录。

Important source packages that exceed the limit should be registered in `project_registry/006_large-source-register/`, kept outside regular Git, and represented by source-marked manifests, checksums, extraction notes, and reviewed derived records.
