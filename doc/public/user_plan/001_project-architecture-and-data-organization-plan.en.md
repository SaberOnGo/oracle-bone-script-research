# Oracle Bone Script Research Project Architecture Plan

> Status: English companion summary for the Chinese planning draft. The authoritative discussion draft is `001_project-architecture-and-data-organization-plan.zh-CN.md`.

## Positioning

Oracle Bone Script Research is an open research infrastructure project: a knowledge base, knowledge graph, and AI Agent research assistant framework for democratizing access to oracle bone script research.

The project does not attempt to train an automatic decipherment model in the first stage. It focuses on structured evidence: deciphered and undeciphered characters, glyph variants, components, inscriptions, excavation context, period, topics, bronze/seal/modern correspondences, source references, scholarly arguments, disputes, and AI Agent evidence packs.

## Naming Strategy

Because oracle characters do not have one universal authoritative ID, the project uses:

```text
project-local stable ID + short primary external reference ID
```

Examples:

```text
001_000001-000100_obs-char-bucket_oracle-characters/
001_obs-char-000001_xxt-jgw-0001_oracle-character/
001_asset-000001_xxt-jgw-0001_glyph-image.png
```

Complete source references should live in metadata and `project_registry/`, not in long file paths.

## Repository Areas

- `AGENTS.md`: mandatory entry point for AI agents.
- `project_registry/`: structure, naming rules, project-to-source ID maps, asset provenance, and glossary.
- `doc/project/`: stable policies and research design.
- `doc/public/user_research/`: user and AI Agent drafts.
- `research/`: existing published scholarship and bibliographic notes.
- `skills/`: reusable AI Agent workflows.
- `schemas/`: data contracts.
- `tools/`: validation, import, and generation scripts.
- `tests/`: repository checks.

## Research Boundary

AI Agent output belongs under `doc/public/user_research/` until reviewed. Existing scholarship belongs under `research/`.

## Implementation Direction

Phase 0 establishes repository rules, bilingual entry documents, ID policy, source provenance registry, rights policy, schemas, basic skills, validation scripts, and tests.

Phase 1 should add a small sample set only. The project should not download external data or commit rights-unclear images in the skeleton stage.
