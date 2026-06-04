# Oracle Bone Script Research

<table align="center">
  <tr>
    <td align="center"><h3><a href="./README.md">English</a></h3></td>
    <td align="center"><h3><a href="./README.zh-CN.md">简体中文</a></h3></td>
  </tr>
</table>

Oracle Bone Script Research is a knowledge base, knowledge graph, and AI Agent framework for democratizing access to oracle bone script research and supporting evidence-based decipherment.

This repository is not an automatic decipherment model. It is an open research infrastructure project: it organizes characters, glyph variants, components, inscriptions, excavation context, source references, scholarly arguments, and AI Agent evidence packs so that people can research oracle bone script with a transparent source trail.

中文摘要：本项目是“甲骨文知识库 + 知识图谱 + AI Agent 研究助手 + 开放研究基础设施”。目标是降低甲骨文研究的信息差和资料门槛，让普通人也能在规范证据框架下参与检索、比对、提问、假说生成和人工复核。

## Mission

Democratizing access to oracle bone script research with AI agents.

用 AI Agent 推动甲骨文研究民主化。

The project focuses on:

- structured oracle character records
- glyph images and source metadata
- graphemic component breakdowns
- full inscription context
- excavation, period, and catalog provenance
- bronze script, seal script, and modern character correspondences
- scholarly evidence, disputes, and research history
- AI Agent evidence packs for transparent hypothesis generation

## Current Stage

The repository is currently in skeleton stage. It contains project rules, repository layout, source-provenance policy, basic skills, schemas, and validation tools. It does not include external oracle bone corpora yet.

## Important Entry Points

- `AGENTS.md`: mandatory instructions for AI agents.
- `project_registry/`: repository structure, naming rules, project IDs, external references, asset provenance, and glossary.
- `doc/project/`: project policies and research design.
- `doc/public/user_research/`: user and AI Agent research drafts.
- `research/`: existing published scholarship notes and bibliographic records.
- `corpus/`: oracle character, inscription, component, correspondence, provenance, graph, and statistics records.
- `skills/`: reusable AI Agent workflows.
- `schemas/`: machine-readable record contracts.
- `tools/`: validation, import, and generation scripts.
- `tests/`: tests for repository rules and scripts.

## Research Boundary

AI Agent output is treated as draft research. It belongs under `doc/public/user_research/` until it is reviewed and rewritten with reliable sources. Existing scholarship and published research notes belong under `research/`.

AI Agent 输出属于草稿研究。未经复核前应放在 `doc/public/user_research/`；已有学术研究和已发表观点应放在 `research/`。

## Quick Start For AI Agents

Read `AGENTS.md` first, then read the relevant project registry, policy, schema, and skill files before editing.

```powershell
python tools/validation/check_repository_skeleton.py
python -m unittest discover -s tests -v
```

## Source And Risk Policy

External oracle bone images, scans, paper PDFs, large image sets, and research corpora may be downloaded or committed when they are useful for research. Every committed item must include source provenance, rights status, and a visible risk note, so humans and AI Agents can trace where the material came from and judge reuse risk.

研究需要时，可以下载或提交外部甲骨图片、扫描件、论文 PDF、大规模图片集和研究语料。每个提交的资料项都必须注明来源、权利状态和显式风险提示，方便人类和 AI Agent 追溯出处并判断复用风险。
