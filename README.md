# Oracle Bone Script Research

<table align="center">
  <tr>
    <td align="center"><h3><a href="./README.md">English</a></h3></td>
    <td align="center"><h3><a href="./README.zh-CN.md">简体中文</a></h3></td>
  </tr>
</table>

Oracle Bone Script Research is a knowledge base, knowledge graph, and AI Agent framework for democratizing access to oracle bone script research and supporting evidence-based study.

This repository is not an automatic decipherment model. It is an open research infrastructure project: it organizes characters, glyph variants, component candidates, inscriptions, collection context, source references, scholarly materials, graph edges, statistics, and AI Agent review queues so that people can research oracle bone script with a transparent source trail.

中文摘要：本项目是“甲骨文知识库 + 知识图谱 + AI Agent 研究助手 + 开放研究基础设施”。目标是降低甲骨文研究的信息差和资料门槛，让普通人也能在规范证据框架下参与检索、比对、提问、假说生成和人工复核。

## Mission / 项目使命

Democratize access to oracle bone script research with AI agents while preserving source provenance, review status, and research boundaries.

用 AI Agent 推动甲骨文研究民主化，同时保留来源追溯、复核状态和研究边界。

The project focuses on:

- structured oracle-character records and undeciphered-character candidates
- glyph images, image references, and source metadata
- graphemic component candidates and glyph-codepoint links
- inscription and catalog-crosswalk staging records
- collection, excavation, period, batch, and plate provenance
- bronze script, seal script, later script-stage labels, and modern codepoint correspondence candidates
- bibliography, source registers, download logs, manifests, and rights-risk notes
- relationship graph edges, coverage statistics, quality audits, and review queues
- AI Agent evidence packs and review scaffolds for transparent hypothesis work

## Current Stage / 当前阶段

The repository is in the preprocessing and research-infrastructure stage. It already contains source registers, download logs, staging tables, object-local candidate materials, graph edges, statistics, and validation tools. All unconfirmed material remains candidate-only or pending human review.

本仓库处于正式研究开始前的资料工程和预处理阶段。当前已经包含来源登记、下载日志、暂存表、对象内候选资料、图边、统计和校验工具。所有未确认内容都保持候选或待人工复核状态。

## Important Entry Points / 重要入口

- `AGENTS.md`: mandatory instructions for AI agents.
- `project_registry/`: repository structure, naming rules, project IDs, external references, asset provenance, large-source register, and glossary.
- `doc/project/`: project policies and research design.
- `corpus/`: oracle characters, inscriptions, component candidates, correspondence candidates, provenance records, graph records, statistics, and derived features.
- `research/`: existing published scholarship notes and bibliographic records.
- `doc/public/user_research/`: user and AI Agent drafts, evidence packs, comparison logs, and review notes.
- `skills/`: reusable AI Agent workflows.
- `schemas/`: machine-readable record contracts.
- `tools/`: validation, import, extraction, graph, statistics, and context-pack generation scripts.
- `tests/`: tests for repository rules, scripts, and data contracts.
- `tmp/`: ignored local-only workspace for temporary downloads, OCR intermediates, caches, and generated scratch files.

## Research Boundary / 研究边界

AI Agent output is draft research. It belongs under `doc/public/user_research/` until it is reviewed and rewritten with reliable sources. Existing scholarship and published research notes belong under `research/`.

AI Agent 输出属于草稿研究。未经复核前应放在 `doc/public/user_research/`；已有学术研究和已发表观点应放在 `research/`。

Dataset labels, graph edges, codepoint matches, component candidates, catalog crosswalks, and evolution/correspondence candidates are routing evidence only. They must not be presented as confirmed decipherment, formal component assignments, inscription identities, or accepted paleographic correspondences.

数据集标签、图边、codepoint 匹配、构件候选、目录互证和字形演化/对应候选都只是研究路径证据。不得把它们写成已确认释读、正式构件归属、卜辞身份或已接受的古文字对应关系。

## Quick Start For AI Agents / AI Agent 快速开始

Read `AGENTS.md` first, then read the relevant files under `project_registry/`, `doc/project/`, `schemas/`, `skills/`, and `tools/` before editing.

先读 `AGENTS.md`，再根据任务读取 `project_registry/`、`doc/project/`、`schemas/`、`skills/` 和 `tools/` 下的相关文件，然后再修改。

```powershell
python tools/validation/check_repository_skeleton.py
python -m unittest discover -s tests -v
git diff --check
```

## Source And Risk Policy / 来源与风险政策

External oracle bone images, scans, paper PDFs, large image sets, and research corpora may be downloaded or committed when they are useful for research. Every committed item must include source provenance, rights status, and a visible risk note so humans and AI Agents can trace where the material came from and judge reuse risk.

研究需要时，可以下载或提交外部甲骨图片、扫描件、论文 PDF、大型图片集和研究语料。每个提交的资料项都必须注明来源、权利状态和显式风险提示，方便人类和 AI Agent 追溯出处并判断复用风险。

`SIZE_LIMIT` is 30 MiB per file. Larger files require an exception record and should be split, downsampled, compressed, or converted into extracted records when possible. Files at or above 40 MiB must not be committed to regular Git.

`SIZE_LIMIT` 设为单文件 30 MiB。更大的文件需要登记特例，并优先考虑分包、降采样、压缩或抽取成结构化记录。达到或超过 40 MiB 的文件不得提交到普通 Git。

Important source packages that exceed the limit should be registered in `project_registry/006_large-source-register/`, kept in ignored local or external storage, and represented in Git by source-marked manifests, checksums, extraction notes, and reviewed derived records.

超过限制但重要的来源包应登记到 `project_registry/006_large-source-register/`，原始包保存在已忽略的本地或外部存储中，Git 中只保留带来源标记的 manifest、checksum、抽取说明和已复核派生记录。
