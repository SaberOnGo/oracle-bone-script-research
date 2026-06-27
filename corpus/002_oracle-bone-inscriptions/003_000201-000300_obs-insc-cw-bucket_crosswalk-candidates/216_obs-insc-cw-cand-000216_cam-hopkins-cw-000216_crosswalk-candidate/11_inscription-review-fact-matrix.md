# Inscription Review Fact Matrix / 卜辞复核事实矩阵

Project ID: `obs-insc-cw-cand-000216`

Candidate crosswalk ID: `cam-hopkins-crosswalk-000216`

## Human Review Order / 人工复核顺序

Open this Inscription And Plate Fact Matrix first, then open
`09_inscription-plate-evidence-dossier.md`, and then use the CSV and JSON
files only as route support.

先读本卜辞与图版事实矩阵，再读
`09_inscription-plate-evidence-dossier.md`。
CSV 和 JSON 只作检索、追溯和复核辅助。

## Inscription And Plate Fact Matrix

### Inscription number
- Status:
  `candidate row only; formal obi ID is not assigned`
- Evidence:
  - `01_candidate-inscription-crosswalk-packet.json`
  - `03_catalog-reference-index.csv`
- Next check: check candidate ID, source row, and formal record status

### Full text or OCR
- Status:
  `needs_primary_text_or_OCR_route_review`
- Evidence:
  - `05_plate-text-route-index.csv`
  - `09_inscription-plate-evidence-dossier.md`
- Next check: open plate or catalog route before recording text

### Plate or rubbing image
- Status:
  `route indexed; image rights and local file need review`
- Evidence:
  - `05_plate-text-route-index.csv`
  - `06_plate-text-gallery.md`
- Next check: locate plate image, rubbing, or object image route

### Catalog references
- Status:
  `present_in_metadata_routes`
- Evidence:
  - `03_catalog-reference-index.csv`
- Next check: compare Yingguo, CUL, Chalfant, and Heji references

### Heji route
- Status:
  `present_in_metadata_route`
- Evidence:
  - `03_catalog-reference-index.csv`
  - `05_plate-text-route-index.csv`
- Next check: open Heji or OBM route before using as text evidence

### Collection object
- Status:
  `present_in_metadata_route`
- Evidence:
  - `03_catalog-reference-index.csv`
  - `07_human-inscription-dossier.md`
- Next check: check CUL or catalog object record and shelfmark

### Findspot period batch
- Status:
  `period and group imported; findspot and batch need review`
- Evidence:
  - `01_candidate-inscription-crosswalk-packet.json`
  - `09_inscription-plate-evidence-dossier.md`
- Next check: verify findspot, pit, batch, period, and group routes

### Linked character occurrences
- Status:
  `needs character occurrence and component route review`
- Evidence:
  - `07_human-inscription-dossier.md`
  - `05_plate-text-route-index.csv`
- Next check: record only candidate links until source signs are checked

### Rights and source trail
- Status:
  `metadata route rights status: metadata_only_until_verified`
- Evidence:
  - `02_crosswalk-source-index.csv`
  - `09_inscription-plate-evidence-dossier.md`
- Next check: review download log, checksum, manifest, and risk note

### Review status
- Status:
  `needs_human_inscription_crosswalk_review`
- Evidence:
  - `04_human-review-sheet.md`
  - `10_inscription-plate-evidence-index.json`
- Next check: finish source, plate, text, and object checks first

## Human Research Slots / 人类研究待查槽位

- Image, rubbing, or plate: check `06_plate-text-gallery.md`.
- Inscription text or OCR: check `05_plate-text-route-index.csv`.
- Catalog and Heji: compare `03_catalog-reference-index.csv`.
- Collection, findspot, period, or batch: open object and catalog routes.
- Linked characters, components, or variants: record candidate links only.
- Bibliography, proposer, reading history, and disputes: add reviewed notes.
- Source trail, checksum, manifest, rights, and risk note: review source rows.
- AI route support: `10_inscription-plate-evidence-index.json`.
- Matrix support index: `12_inscription-review-fact-matrix-index.json`.


## Concrete Questions To Check / 具体待查问题

- Which plate, rubbing, image, OCR, or full text route should be opened?
- Which catalog number, page, Heji number, or CUL object anchors this object?
- Which collection, findspot, period, group, batch, or pit route is relevant?
- Which linked character occurrences remain only candidate routes?
- Which source download log, checksum, manifest, or field map applies?
- Which rights status or risk note must be checked?
- Which bibliography or dispute record must be reviewed before any conclusion?

## Boundary / 边界

- not a formal inscription record
- not an object identity claim
- not a transcription
- not an inscription reading
- not corpus import approval
- not a decipherment conclusion
- 不是正式卜辞记录
- 不是馆藏对象同一性结论
- 不是释文
- 不是卜辞读法
- 不是语料导入批准
- 不是释读结论
