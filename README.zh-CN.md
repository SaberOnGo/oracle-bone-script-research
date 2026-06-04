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

当前仓库处于骨架阶段。它先建立项目规则、目录结构、来源追溯政策、基础 skills、schema 和校验工具。暂时不下载外部甲骨文数据，也不提交权利状态不明的大图、扫描件或论文全文。

## 重要入口

- `AGENTS.md`：所有 AI agent 必须先读的规则。
- `project_registry/`：仓库结构、命名规则、本项目 ID、外部来源引用、资产出处和术语表。
- `doc/project/`：项目政策和研究设计。
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

External oracle bone images, scans, paper PDFs, large image sets, and research corpora may be downloaded or committed when they are useful for research. Every committed item must include source provenance, rights status, and a visible risk note, so humans and AI Agents can trace where the material came from and judge reuse risk.
