# Character-Variant Linkage Audit / 字形—异体关联审计

## Human Reading Result / 人类阅读结果

- OBIMD staging rows: 2747
- Candidate variant graph edges: 2747
- Unique sub-character references: 2747
- Unique main-character references: 1730
- Relation types: blank=2747
- Promotion statuses: blank=2747
- Graph review status: all rows remain `needs_cross_source_review`.

## What The Current Evidence Says / 当前证据说明

The rows reproduce the relation recorded by the OBIMD staging table. They are
source metadata and a review route, not a paleographic decision that two forms
are variants.

The project-local source node is an OBIMD sub-character candidate and the
target is an OBIMD main-character reference. It does not confirm an identity,
variant relation, or specific oracle-bone sign.

## Evidence Required Before Promotion / 提升关系前必须补齐的证据

- Open both glyph images and record a neutral side-by-side observation.
- Check the source workbook row, checksum, rights note, and manifest.
- Compare the forms against HUST-OBC, Xiaoxuetang, and other sources.
- Record period, findspot, inscription context, and catalog references.
- Record published proposals, dissent, reviewer, and review date.
- Keep the edge candidate-only when any of these checks is missing.

## Human Opening Order / 人类复核顺序

- Start with the component-candidate human dossier and visual gallery.
- Open `002_obimd-subcharacter-main-staging.csv` for the source row.
- Follow the co-located image, rights, and source-manifest routes.
- Compare the candidate with character dossiers only after visual review.
- Use `226_character-variant-linkage-audit-index.json` for counts only.

## Boundary / 边界

This audit and its graph edges support preprocessing and human review only.
They do not confirm an identity, variant relation, reading, inscription
assignment, or decipherment conclusion.

本审计及图边只服务于预处理和人工复核，不确认字形身份、异体关系、
释读、卜辞归属或破译结论。
