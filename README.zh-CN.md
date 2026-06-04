# 甲骨文开放研究项目

<table align="center">
  <tr>
    <td align="center"><h3><a href="./README.zh-CN.md">简体中文</a></h3></td>
    <td align="center"><h3><a href="./README.md">English</a></h3></td>
  </tr>
</table>

本项目是“甲骨文知识库 + 知识图谱 + AI Agent 研究助手 + 开放研究基础设施”。

它不是自动破译甲骨文的模型，而是一个把甲骨字、字形变体、构件、卜辞、出土信息、来源引用、学术论证和 AI Agent 证据包结构化的长期项目。目标是降低甲骨文研究的信息差和资料门槛，让普通人也能在规范证据框架下进行检索、比对、提问、假说生成和人工复核。

English summary: Oracle Bone Script Research is a knowledge base, knowledge graph, and AI Agent framework for democratizing access to oracle bone script research and supporting evidence-based decipherment.

## 项目使命

用 AI Agent 推动甲骨文研究民主化。

Democratizing access to oracle bone script research with AI agents.

本项目重点整理：

- 甲骨单字结构化记录
- 字形图片和来源 metadata
- 构件拆分
- 卜辞全文上下文
- 出土地点、时代、著录和图版来源
- 金文、小篆、今文对应关系
- 专家释读依据、争议和研究史
- 支持 AI Agent 透明推理的 evidence pack

## 当前阶段

当前仓库处于骨架阶段。它先建立项目规则、目录结构、来源追溯政策、基础 skills、schema 和校验工具。当前尚未纳入外部甲骨文语料；后续如纳入图片、扫描件、论文或数据库导出，必须同时记录来源、权利状态、风险提示和尺寸处理方式。

## 重要入口

- `AGENTS.md`：所有 AI agent 必须先读的规则。
- `project_registry/`：仓库结构、命名规则、本项目 ID、外部来源引用、资产出处和术语表。
- `doc/project/`：项目政策和研究设计。
- `tmp/`：本地临时工作区，用于 AI Agent 草稿和生成性中间产物。
- `doc/public/user_research/`：普通用户和 AI Agent 的研究草稿。
- `research/`：已有学术研究、已发表观点和书目记录。
- `corpus/`：甲骨字、卜辞、构件、字形对应、出处、图谱和统计记录。
- `skills/`：AI Agent 可复用工作流。
- `schemas/`：机器可校验的数据结构。
- `tools/`：校验、导入和生成脚本。
- `tests/`：仓库规则和脚本测试。

## 研究边界

AI Agent 输出属于草稿研究。未经复核前应放在 `doc/public/user_research/`；已有学术研究和已发表观点应放在 `research/`。

AI Agent output is draft research. It belongs under `doc/public/user_research/` until reviewed and rewritten with reliable sources. Existing scholarship belongs under `research/`.

## AI Agent 快速开始

先读 `AGENTS.md`，再根据任务读取相关的 registry、policy、schema 和 skill 文件。

```powershell
python tools/validation/check_repository_skeleton.py
python -m unittest discover -s tests -v
```

## 来源与风险政策

研究需要时，可以下载或提交外部甲骨图片、扫描件、论文 PDF、大规模图片集和研究语料。每个提交的资料项都必须注明来源、权利状态和显式风险提示，方便人类和 AI Agent 追溯出处并判断复用风险。

`SIZE_LIMIT` 设为单文件 30 MiB。更大的文件需要登记特例，并优先考虑分包、降采样、压缩或抽取其中结构化记录。达到或超过 40 MiB 的文件不得提交到普通 Git。

超过限制但重要的来源包应登记到 `project_registry/006_large-source-register/`，原始包放在已忽略的本地目录或外部存储中，Git 中只保留带来源的 manifest、校验和、抽取说明和复核后的派生记录。AI Agent 临时下载、OCR 中间产物、缓存、生成索引和解压目录应放入 `tmp/` 等已忽略临时区，不进入 Git 历史。

External oracle bone images, scans, paper PDFs, large image sets, and research corpora may be downloaded or committed when they are useful for research. Every committed item must include source provenance, rights status, and a visible risk note, so humans and AI Agents can trace where the material came from and judge reuse risk.

`SIZE_LIMIT` is 30 MiB per file. Larger files require an exception record and should be split, downsampled, compressed, or converted into extracted records when possible. Files at or above 40 MiB must not be committed to regular Git.

Important source packages that exceed the limit should be registered in `project_registry/006_large-source-register/`, kept in ignored local or external storage, and represented in Git by source-marked manifests, checksums, extraction notes, and reviewed derived records. AI Agent temporary downloads, OCR intermediates, caches, generated indexes, and unpacked archives belong in ignored temporary areas such as `tmp/`, not in Git history.
