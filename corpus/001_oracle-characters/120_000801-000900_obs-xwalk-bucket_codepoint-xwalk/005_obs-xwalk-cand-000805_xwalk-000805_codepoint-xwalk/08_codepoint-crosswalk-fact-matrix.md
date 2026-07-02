# obs-xwalk-cand-000805 Codepoint Crosswalk Fact Matrix

## Human Review Order / 人类复核顺序

- 1. Open the HUST candidate route and local glyph materials.
- 2. Check the Source Codepoint Route against the staging row.
- 3. Open the OBIMD route only if a match row is present.
- 4. Open the EVOBC route only if a match row is present.
- 5. Write missing evidence before any promotion review.

## Fact Matrix / 事实矩阵

| Slot / 项目 | Current route evidence / 当前路线证据 | Review boundary / 复核边界 |
|---|---|---|
| Source Codepoint Route / 来源码位路线 | `U+3786` | not identity |
| HUST candidate route / HUST 候选路线 | `hust-obc-cat-0912` | not reading |
| OBIMD route / OBIMD 路线 | `pending route` | not component |
| EVOBC route / EVOBC 路线 | `pending route` | not evolution |
| Source and rights trail / 来源与权利链 | `source_marked_risk_noted` | source-marked risk note required |
| Missing evidence route / 缺失证据路线 | `no_obimd_or_evobc_codepoint_match` | not decipherment |
| Review status / 复核状态 | `needs_cross_source_review` | needs human cross-source review |

## Human Comparison Order / 人工比对顺序

- Open the matched oracle-character human dossier first.
- Open local glyph images, rubbing routes, and plate routes.
- Compare OBIMD and EVOBC rows only after the glyph dossier.
- Record disagreement before any promotion review.
- Do not promote this codepoint route into identity.

## Required Routes / 必查路线

| Route / 路线 | File / 文件 | Human action / 人工动作 |
|---|---|---|
| Codepoint crosswalk staging | `corpus/001_oracle-characters/000_character-registers/011_hust-obimd-evobc-codepoint-crosswalk-staging.csv` | open row before any human claim |
| HUST candidate route | `corpus/001_oracle-characters/009_000801-000900_obs-char-bucket_oracle-characters/805_obs-char-000805_hust-obc-cat-0912_oracle-character/01_candidate-character-packet.json` | open packet and local glyph dossier first |
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
