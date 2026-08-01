# Human Inscription And Plate Pre-Research Map
# 人类卜辞与图版预研究地图

Review date / 复核日期: 2026-08-01

## Current Material / 当前资料

- Cambridge/Hopkins staging rows: `612`
- Cambridge/Hopkins 暂存行：`612`
- Object-local candidate dossiers: `612`
- 已生成对象内候选档案：`612`
- Period groups represented: `68`
- 已出现的时期—组别组合：`68`
- Explicit character-link fields in packets: `0`
- 候选包中的明确字形关联字段：`0`
- Promoted character-inscription edges: `0`
- 已提升的字形—卜辞关系边：`0`

All 612 staging rows remain `dataset_candidate_not_promoted` and
`metadata_only_until_verified`. This is the current review boundary, not a
negative statement about the inscriptions.

612 条暂存行目前都仍是 `dataset_candidate_not_promoted` 和
`metadata_only_until_verified`。这只是当前复核边界，不是否定这些卜辞。

## Reference Completeness / 著录路线完整性

The current staging audit records these missing reference flags:

当前暂存审计记录了以下著录缺失标记：

- Missing CUL reference: `6` rows.
- 缺 CUL 参考号：`6` 行。
- Missing Chalfant reference: `171` rows.
- 缺 Chalfant 参考号：`171` 行。
- Missing Heji reference: `316` rows.
- 缺合集参考号：`316` 行。

These flags identify rows for source review. They do not establish that a
catalogue, plate, or object is absent from every external source.

这些标记只用于定位来源复核行，不表示所有外部来源都没有著录、图版或对象
记录。

## Human Reading Order / 人类阅读顺序

1. Open `002_cambridge-hopkins-crosswalk-staging.csv` and note the row ID.
2. Open the matching `obs-insc-cw-cand-*` directory.
3. Read `07_human-inscription-dossier.md` and `09_inscription-plate-
   evidence-dossier.md` before structured files.
4. Open `05_plate-text-route-index.csv` and `06_plate-text-gallery.md`.
5. Follow the cited Yingguo, CUL, Chalfant, Heji, OBM, and collection routes.
6. Record plate, page, image, text, rights, and provenance outcomes.
7. Open `21_character-inscription-linkage-review.md` only after the plate and
   text position are visible.

## What Is Still Missing / 仍缺什么

- A primary plate, rubbing, photograph, or collection-image route for each
  candidate is not yet confirmed by this register.
- 本登记表尚未为每个候选确认原始图版、拓片、照片或馆藏图像路线。
- A full inscription text or OCR route is not supplied by the crosswalk row.
- 互证行本身没有提供完整卜辞文本或 OCR 路线。
- A character position cannot be inferred from a catalogue number or file name.
- 不能从著录号或文件名推断字形在图版中的位置。
- Findspot, collection, batch, and pit context require separate source review.
- 出土地、馆藏、批次和坑位语境仍需另行来源复核。
- Bibliography, reading history, proposer, and disputes require cited
  scholarship notes, not empty fields.
- 书目、释读史、提出者和争议必须补充有引文的学术笔记，不能用空字段替代。

## Character-Link Boundary / 字形关联边界

The zero-edge audit means that no candidate currently provides both a visible
plate/text position and an explicit character project ID. It does not mean
that a plate contains no characters.

零关系边审计表示当前没有候选项同时提供可见的图版/文本位置和明确单字
项目 ID，不表示图版中没有字形。

Before a relation route can be reviewed, preserve the exact image or plate
route, position, text/OCR evidence, source citation, reviewer, disagreement,
rights status, and checksum where applicable.

在复核关系路线前，必须保留确切图像或图版路线、位置、文本/OCR 证据、来源
引用、复核者、不同意见、权利状态以及适用时的 checksum。

## Boundary / 边界

This map is a human preprocessing aid. It does not assign an `obi-*` ID,
accept a transcription, propose a reading, or make a decipherment claim.

本地图只是人类预处理辅助，不分配 `obi-*` 编号，不接受释文，不提出释读，
也不形成破译结论。

## Evidence Paths / 证据路径

- `002_cambridge-hopkins-crosswalk-staging.csv`
- `223_character-inscription-linkage-audit.md`
- `224_character-inscription-linkage-audit-index.json`
- `098_ai-agent-cambridge-hopkins-inscription-crosswalk-review-queue.csv`
- `195_inscription-plate-crosswalk-phase-gap-review-checklist.csv`
- `corpus/006_research-sources-and-bibliography/001_source-objects/
  008_src-cambridge-hopkins_source-object/10_source-evidence-dossier.md`
