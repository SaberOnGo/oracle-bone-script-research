# Public Agent Instructions / 公共 Agent 指令

This file is the mandatory entry point for AI agents working from a downloaded copy of this repository.

本文件是 AI agent 下载或打开本仓库后必须首先读取的入口规则。

## Mandatory Rules / 强制规则

- Before doing any task in this repository, read this `AGENTS.md` first. Then read the relevant files under `project_registry/`, `doc/project/`, `schemas/`, and `skills/` before editing.
- 在本仓库执行任何任务前，必须先读取本 `AGENTS.md`。然后根据任务读取 `project_registry/`、`doc/project/`、`schemas/` 和 `skills/` 下的相关文件。

- Do not rely on memory, previous chats, or assumptions about this project. Inspect the current files on disk before making changes.
- 不要依赖记忆、历史对话或对项目的想当然理解。修改前必须检查当前磁盘上的文件。

- This repository is an oracle bone script knowledge base, knowledge graph, and AI Agent research assistant framework. It is not an automatic decipherment model and must not present AI hypotheses as confirmed scholarship.
- 本仓库是甲骨文知识库、知识图谱和 AI Agent 研究助手框架，不是自动破译模型；不得把 AI 假说写成已确认的学术结论。

- Human-facing project documents must be bilingual in English and Simplified Chinese, or must have a clearly linked English/Chinese companion file.
- 面向人类阅读的项目文档必须中英双语，或者有清楚互链的英文/中文配套文件。

- Keep file and directory names short, stable, ASCII-friendly, and self-describing. Do not use modern Chinese characters, liding characters, pinyin, or English readings as primary path identity for oracle characters.
- 文件和目录名应短、稳定、兼容 ASCII，并能自说明。甲骨单字路径不要把现代汉字、隶定字、拼音或英文释义作为主要身份标识。

- Use the project ID plus one short external reference ID in paths. Store the complete source trail in metadata and `project_registry/`.
- 路径中使用本项目 ID 加一个简短外部来源 ID；完整来源链写入 metadata 和 `project_registry/`。

- External oracle bone images, scans, paper PDFs, and large research corpora may be downloaded or committed when research needs them, but every item must include source provenance, rights status, and a visible risk note.
- 研究需要时，可以下载或提交外部甲骨图片、扫描件、论文 PDF 或大型研究资料；但每项资料都必须注明来源、权利状态和显式风险提示。

## Required Reading / 必读文件

For repository-wide work, read these first:

仓库级任务优先读取：

- `README.md`
- `README.zh-CN.md`
- `project_registry/README.md`
- `project_registry/001_repository-structure-and-naming-rules/README.md`
- `project_registry/002_project-id-to-source-reference-map/README.md`
- `doc/project/001_project-positioning-and-research-boundaries/README.md`
- `doc/project/002_source-rights-and-provenance-policy/README.md`
- `doc/project/003_record-model-and-id-system/README.md`
- `skills/README.md`

For corpus and record curation, also read:

语料和记录整理任务还要读取：

- `skills/oracle-character-record-curation/SKILL.md`
- `skills/source-provenance-review/SKILL.md`
- `schemas/README.md`

For AI Agent hypothesis or evidence-pack work, also read:

AI Agent 假说或 evidence pack 任务还要读取：

- `skills/ai-agent-evidence-pack-review/SKILL.md`
- `doc/project/005_ai-agent-research-assistant-design/README.md`

## Research Area Boundaries / 研究区边界

- `research/` is for existing scholarship: published research, bibliographic notes, scholarly arguments, decipherment history, and carefully sourced summaries.
- `research/` 用于已有学术研究：已发表研究、书目笔记、学术论证、释读史和有明确来源的严谨摘要。

- `doc/public/user_research/` is for user and AI Agent drafts: hypotheses, exploratory notes, evidence packs, comparison logs, and review notes.
- `doc/public/user_research/` 用于用户和 AI Agent 草稿：假说、探索笔记、证据包、对比记录和复核记录。

- Do not mix user/AI drafts into `research/` unless they have been reviewed and rewritten as sourced scholarship notes.
- 未经复核并改写成有来源的学术笔记前，不要把用户/AI 草稿混入 `research/`。

## Naming Rules / 命名规则

Use this shape for large bucket directories:

大量资料分桶目录使用：

```text
数字前缀_区段_本项目ID类型-bucket_资料类型
001_000001-000100_obs-char-bucket_oracle-characters/
```

Use this shape for one oracle character directory:

单个甲骨字目录使用：

```text
数字前缀_本项目ID_首选外部ID_简短类型
001_obs-char-000001_xxt-jgw-0001_oracle-character/
```

Use this shape for assets:

资料资产使用：

```text
数字前缀_资产ID_首选外部ID_简短类型
001_asset-000001_xxt-jgw-0001_glyph-image.png
```

If no external ID is available yet, use `extid-unassigned` in the path and record the source image, catalog, batch, or provenance in metadata.

如果暂时没有外部 ID，路径中使用 `extid-unassigned`，并在 metadata 中记录来源图像、著录、批次或出处。

## Validation / 校验

Run these checks before committing repository skeleton, docs, schemas, or scripts:

提交仓库骨架、文档、schema 或脚本前运行：

```powershell
python tools/validation/check_repository_skeleton.py
python -m unittest discover -s tests -v
git diff --check
```

Before pushing to GitHub, validate commit messages:

推送到 GitHub 前校验提交信息：

```powershell
python tools/git/check_commit_messages.py --range origin/main..HEAD
```

## GitHub Push Commit Rules / GitHub 推送提交规则

- Before pushing to GitHub, every pushed commit must have a concise title and a detailed commit body.
- 推送到 GitHub 前，每个将被推送的 commit 必须有简洁标题和详细正文。

- The detailed commit body must contain separate `ZH:`, `EN:`, and `JA:` sections. Each language label must be alone on its own line, with summary text below it.
- commit 正文必须包含独立的 `ZH:`、`EN:`、`JA:` 三段。每个语言标签必须独占一行，摘要正文写在下一行。

- Do not use one-line commits for changes that will be pushed.
- 将要推送的修改不得使用只有一行标题的 commit。

Recommended commit form:

推荐提交格式：

```powershell
git commit -m "Initialize research project skeleton" `
  -m "ZH:" `
  -m "- 建立项目骨架、AGENTS 入口、双语 README、来源追溯规则、基础 skills 和校验脚本。" `
  -m "EN:" `
  -m "- Add the project skeleton, AGENTS entry point, bilingual README files, provenance rules, basic skills, and validation scripts." `
  -m "JA:" `
  -m "- プロジェクト骨格、AGENTS 入口、日英中ではなく中英中心の README、出典追跡規則、基本 skills、検証スクリプトを追加。"
```

## Output Discipline / 输出要求

- State what was inspected, what changed, what was verified, and what remains.
- 说明已经检查了什么、修改了什么、验证了什么、还剩什么。

- If a check was not run, say so clearly.
- 如果某项检查没有运行，必须明确说明。
