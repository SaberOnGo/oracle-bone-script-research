# Character-Inscription Linkage Review / 字形—卜辞关联复核

Project ID: `obs-insc-cw-cand-000153`

Candidate crosswalk ID: `cam-hopkins-crosswalk-000153`

## Current Evidence State / 当前证据状态

The current staging row has no explicit character project ID, character
position, or linked-glyph field. Catalog and period/group clues cannot
create a character-inscription relation by themselves.

当前 staging 行没有明确的字形项目 ID、字形位置或关联字形字段。著录线索以及时期、组类线索本身不能建立字形—卜辞关系。

- Promoted character-inscription edge: `none`
- 提升为正式关系边：`无`
- Global audit:
  `corpus/009_statistics-and-derived-features/`
  `223_character-inscription-linkage-audit.md`
- Global audit index:
  `corpus/009_statistics-and-derived-features/`
  `224_character-inscription-linkage-audit-index.json`
- Review status: `needs_plate_text_position_and_character_id_review`

The zero-edge result is an audited evidence gap. It does not mean that the
inscription contains no characters. It means that this candidate does not yet
provide enough source evidence to connect an occurrence to a character dossier.

零关系边是已经审计的证据缺口，不表示卜辞中没有字形；它只表示当前候选
还没有足够的来源证据，把某个字形出现位置连接到具体单字档案。

## Evidence To Collect / 待补证据

- Open the cited plate, rubbing, photograph, or collection image.
- Record the exact source route, page or plate number, rights status, and
  checksum.
- Capture the full inscription or OCR and mark unreadable or uncertain signs.
- Record the exact position of each proposed character occurrence.
- Use an existing character project ID only when the source evidence names it.
- Record the reviewer, source citation, disagreement, and review status.

- 打开所引图版、拓片、照片或馆藏图像。
- 记录来源路径、页码或图版号、权利状态和 checksum。
- 保存卜辞全文或 OCR，并标记不可辨、缺失和不确定字位。
- 记录每个候选字形出现的准确位置。
- 只有来源明确指向时，才能使用现有单字项目 ID。
- 记录复核者、来源引用、不同意见和复核状态。

## Human Opening Order / 人类复核顺序

1. Open `07_human-inscription-dossier.md` for the catalog and source route.
2. Open `06_plate-text-gallery.md` for image, plate, and text routes.
3. Open `13_text-ocr-quality-review.md` before using OCR or transcription.
4. Follow `15_inscription-context-review.md` for archaeology and occurrence.
5. Open the global human audit before changing any graph edge.

先看本对象的人类卜辞档案、图版文本路线和 OCR 质量复核，再查看考古与
字形出处上下文。没有图版位置、文本证据和来源记录时，不得建边。

## Boundary / 边界

This file is a human review record for preprocessing. It is not a formal
inscription record, object identity claim, transcription, inscription reading,
component assignment, variant judgment, or decipherment conclusion.

本文件是预处理阶段的人类复核档案，不是正式卜辞记录、器物身份结论、
释文、释读、构件判断、异体判断或破译结论。
