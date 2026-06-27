# obs-xwalk-cand-001571 Codepoint Crosswalk Fact Matrix

## Human Review Order / 人类复核顺序

- 1. Open the HUST candidate route and local glyph materials.
- 2. Check the Source Codepoint Route against the staging row.
- 3. Open the OBIMD route only if a match row is present.
- 4. Open the EVOBC route only if a match row is present.
- 5. Write missing evidence before any promotion review.

## Fact Matrix / 事实矩阵

| Slot | Current route evidence | Review boundary |
|---|---|---|
| Source Codepoint Route | `U+3AD9` | not identity |
| HUST candidate route | `hust-obc-cat-1763` | not reading |
| OBIMD route | `pending route` | not component |
| EVOBC route | `pending route` | not evolution |
| Source and rights trail | `source_marked_risk_noted` | source-marked risk note required |
| Missing evidence route | `no_obimd_or_evobc_codepoint_match` | not decipherment |
| Review status | `needs_cross_source_review` | needs human cross-source review |

## Required Routes / 必查路线

| Route | File | Human action |
|---|---|---|
| Codepoint crosswalk staging | `corpus/001_oracle-characters/000_character-registers/011_hust-obimd-evobc-codepoint-crosswalk-staging.csv` | open row before any human claim |
| HUST candidate route | `corpus/001_oracle-characters/016_001501-001600_obs-char-bucket_oracle-characters/1571_obs-char-001571_hust-obc-cat-1763_oracle-character/01_candidate-character-packet.json` | open packet and local glyph dossier first |
| All source register | `corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv` | check title, scope, rights, and risk note |
| Large source download log | `project_registry/006_large-source-register/002_source-download-log.csv` | check checksum, size, status, and risk note |
| OBIMD route | `corpus/001_oracle-characters/000_character-registers/006_obimd-main-character-staging.csv` | open matched OBIMD rows when present |
| EVOBC route | `corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/001_evobc-evolution-category-staging.csv` | open matched EVOBC rows when present |

## Required Files / 必查文件

- 011_hust-obimd-evobc-codepoint-crosswalk-staging.csv
- 01_candidate-character-packet.json
- 006_obimd-main-character-staging.csv
- 001_evobc-evolution-category-staging.csv
- 001_all-sources-index.csv
- 002_source-download-log.csv

## Boundary / 边界

- This matrix records lookup-route facts only: not identity, not reading,
  not component, not evolution, and not decipherment.
