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

The repository is currently in skeleton stage. It contains project rules, repository layout, source-provenance policy, basic skills, schemas, and validation tools. It does not download or include external oracle bone datasets yet.

## Important Entry Points

- `AGENTS.md`: mandatory instructions for AI agents.
- `project_registry/`: repository structure, naming rules, project IDs, external references, asset provenance, and glossary.
- `doc/project/`: project policies and research design.
- `doc/public/user_research/`: user and AI Agent research drafts.
- `research/`: existing published scholarship notes and bibliographic records.
- `skills/`: reusable AI Agent workflows.
- `schemas/`: machine-readable data contracts.
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

## Data Policy

The public GitHub repository should prefer metadata, schemas, indexes, public documentation, and rights-clear sample data. Rights-unclear scans, paper PDFs, large image sets, or commercial publication extracts should not be committed until the project has explicit rights documentation.

公开 GitHub 仓库优先保存 metadata、schema、索引、公开文档和权利清楚的样例数据。权利不明的扫描图、论文 PDF、大规模图片和商业出版物整理文本，在权利说明明确前不应提交。
