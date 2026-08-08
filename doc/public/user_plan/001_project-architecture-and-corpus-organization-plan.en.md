# Oracle Bone Script Research Project Architecture Plan

> Historical status: this file preserves the early architecture discussion.
> Its naming and provenance design remains useful, but its requirement for
> prior human review before candidate delivery is superseded by
> the [AI autonomous candidate strategy][current-strategy].
> Independent AI agents may now adjudicate and deliver high-confidence
> candidates, but those candidates are not confirmed scholarship.
> [Companion index](README.md)

> Status: English companion summary for the historical Chinese planning
> draft.

## Positioning

Oracle Bone Script Research is an open research infrastructure project: a
knowledge base, knowledge graph, and AI Agent research assistant framework
for democratizing access to oracle bone script research.

The early plan did not attempt to train an automatic decipherment model. It
focused on structured evidence: characters, variants, components,
inscriptions, archaeology, periods, later forms, sources, arguments,
disputes, and AI Agent evidence packs.

## Naming Strategy

Because oracle characters do not have one universal authoritative ID, the
project uses:

```text
project-local stable ID + short primary external reference ID
```

Examples:

```text
001_000001-000100_obs-char-bucket_oracle-characters/
001_obs-char-000001_xxt-jgw-0001_oracle-character/
001_asset-000001_xxt-jgw-0001_glyph-image.png
```

Complete source references should live in metadata and `project_registry/`,
not in long file paths.

## Repository Areas

- `AGENTS.md`: mandatory entry point for AI agents.
- `project_registry/`: structure, naming, ID maps, asset provenance, and
  glossary.
- `doc/project/`: stable policies and research design.
- `doc/public/user_research/`: user and AI Agent drafts.
- `research/`: existing published scholarship and bibliographic notes.
- `skills/`: reusable AI Agent workflows.
- `schemas/`: record contracts.
- `tools/`: validation, import, and generation scripts.
- `tests/`: repository checks.

## Research Boundary

AI Agent output belongs under `doc/public/user_research/`. Existing
scholarship belongs under `research/`.

## Implementation Direction

Phase 0 establishes repository rules, bilingual entry documents, ID policy,
source provenance, rights policy, schemas, skills, validators, and tests.

Phase 1 should add a small sample set only. External materials may be used
when useful, but every item must include source provenance, rights status,
and a visible risk note.

[current-strategy]: ../../project/005_ai-agent-research-assistant-design/
