---
name: oracle-character-record-curation
description: Use when creating or updating structured oracle bone script character records, glyph variant notes, component breakdowns, inscription occurrences, or character source references in this repository.
---

# Oracle Character Record Curation / 甲骨单字记录整理

## Use This Skill When / 何时使用

English:
Use this skill before creating or editing `obs-char-*` records under `corpus/001_oracle-characters/`.

简体中文：
在创建或编辑 `corpus/001_oracle-characters/` 下的 `obs-char-*` 记录前使用本 skill。

## Required Reading / 必读

- `AGENTS.md`
- `project_registry/001_repository-structure-and-naming-rules/README.md`
- `project_registry/002_project-id-to-source-reference-map/README.md`
- `doc/project/003_record-model-and-id-system/README.md`
- `schemas/001_character-record-schema/character-record.schema.json`

## Workflow / 工作流

1. Confirm whether the character already has a project-local ID.
   确认该字是否已有本项目 ID。
2. If no ID exists, assign the next `obs-char-000000` ID and record it in the character assignment log.
   如无 ID，分配下一个 `obs-char-000000` ID，并写入 ID 分配记录。
3. Use one short primary external reference ID in the directory name.
   目录名只放一个简短首选外部来源 ID。
4. Put all additional external references in metadata and `project_registry/`.
   其他外部来源引用全部写入 metadata 和 `project_registry/`。
5. Do not use modern readings, pinyin, liding forms, or English meaning as primary path identity.
   不要把现代释读、拼音、隶定字或英文意义作为路径主身份。
6. Mark every record as `draft`, `needs_review`, or `reviewed`.
   每条记录标记为 `draft`、`needs_review` 或 `reviewed`。

## Minimum Record / 最小记录

English:
A minimal character record needs project ID, primary external reference ID, source references, decipherment status, rights status for assets, and review status.

简体中文：
最小甲骨字记录需要本项目 ID、首选外部来源 ID、来源引用、释读状态、资产权利状态和复核状态。
