# Inscription Context Review / 卜辞上下文复核卡

Project ID: `obs-insc-cw-cand-000389`

Candidate crosswalk ID: `cam-hopkins-crosswalk-000389`

## Research Desk Summary / 案头复核摘要

- Object type: `inscription_crosswalk_candidate`
- Formal `obi-*` ID: `not_assigned_formal_obi_id`
- Period label: `II`
- Classification group: `17`
- Declared group count: `36`
- Rights status: `metadata_only_until_verified`
- Review status: `needs_human_inscription_crosswalk_review`

This card is the object-local human starting point for checking one
inscription candidate. It tells a reviewer which image, rubbing, text,
catalog, collection, period, batch, and character-occurrence routes must be
opened before the candidate can become a formal inscription record.

本卡片是单个卜辞候选对象的本地人类复核入口。复核者必须先打开图版、拓片、文本、著录、馆藏、时期、批次和字形出处路线，才能讨论是否可进入正式卜辞记录。

## Text Plate And Catalog Routes / 文本、图版与著录路线

- Full inscription text: `待查: primary full-text route`
- OCR or transcription: `待查: OCR or transcription route`
- Plate image path: `待查: plate image or rubbing route`
- Page number route: `待查: catalog page route`
- Heji route: `待查: Heji or OBM route`
- Collection object: `待查: CUL or catalog object record`
- Catalog reference count: `4`
- Plate and text route count: `5`

Present catalog reference routes:

- yingguo
- cambridge_university_library
- chalfant

Missing catalog reference routes:

- heji

Plate, text, and collection route types:

- cambridge_hopkins_finding_list
- yingguo_catalog_reference
- cambridge_university_library_reference
- chalfant_reference
- heji_reference

- Note: no unresolved source character marker in catalog refs.

Open `03_catalog-reference-index.csv`, `05_plate-text-route-index.csv`,
and `06_plate-text-gallery.md` before recording any text, image, page,
Heji, CUL, Chalfant, Yingguo, or OBM evidence.

## Archaeological And Occurrence Context / 考古与字形出处上下文

- Excavation site: `待查: source route for excavation context`
- Findspot: `待查: source route for findspot`
- Batch or pit context: `待查: batch or pit source route`
- Period and group basis: `imported metadata; needs source review`
- Linked glyph occurrences: `待查: character occurrence routes`
- Component or variant links: `待查: separate glyph review routes`
- Later-script comparison: `待查: not part of this candidate record`

Imported period and group labels are routing clues only. They do not create
a new chronology, object identity, transcription, or reading.

导入的时期和组类标签只作为复核路线提示，不构成新的断代、馆藏对象
同一性、释文或读法结论。

## Source Trail And Quality Blockers / 来源链与质量阻断项

- Source ID: `src-cambridge-hopkins`
- Evidence download ID: `dl-cambridge-hopkins-finding-list`
- Source object area: `corpus/006_research-sources-and-bibliography`
- Source object directory: `008_src-cambridge-hopkins_source-object`
- Local packet: `01_candidate-inscription-crosswalk-packet.json`
- Catalog routes: `03_catalog-reference-index.csv`
- Plate and text routes: `05_plate-text-route-index.csv`
- Text quality review: `13_text-ocr-quality-review.md`

## Source Provenance Audit / 来源追溯审计

- Download log path:
- `project_registry/006_large-source-register/002_source-download-log.csv`
- Download status: `downloaded`
- HTTP status: `200`
- File size bytes: `74132`
- Checksum SHA-256:
- `f11bc30e9893e5d5b3d32371364d59503f100157aaa612800974883f5a78b4e7`
- Source object directory:
- `corpus/006_research-sources-and-bibliography/001_source-objects/`
- `008_src-cambridge-hopkins_source-object/`
- Source object dossier: `10_source-evidence-dossier.md`
- Source evidence index: `11_source-evidence-dossier-index.json`
- Source register directory:
- `corpus/006_research-sources-and-bibliography/000_source-registers/`
- Source register file: `001_all-sources-index.csv`
- Package manifest: `009_source-package-file-manifest.csv`
- Package file ID: `pkg-file-000015`
- Field map: `007_source-field-map.csv`
- Field map rows: `field-map-000019; field-map-000020`
- Rights status: `metadata_only_until_verified`
- Review status: `reviewed`
- Risk note:
Stored under ignored tmp directory; commit log/checksum only.

This audit is a source route checklist. It does not confirm any inscription
identity, image right, OCR text, transcription, or decipherment conclusion.

本审计段只是来源路线清单，不确认卜辞身份、图像权利、OCR、释文或释读。


Quality blockers to resolve before formal use:

- primary full text or OCR route is not reviewed
- plate image or rubbing route is not reviewed
- catalog page, Heji, and collection routes are not reconciled
- findspot, period, group, batch, or pit context is not verified
- linked glyph occurrences remain candidate routes
- bibliography, reading history, and dispute records are not reviewed

## Concrete Questions To Check / 具体待查问题

- Which plate, rubbing, image, page, or OCR text should be opened first?
- Which catalog row anchors the candidate: Yingguo, CUL, Chalfant, or Heji?
- Which collection object or shelfmark must be checked against the plate?
- Which findspot, period, group, batch, or pit source is still missing?
- Which linked glyph occurrence is only a candidate route?
- Which source manifest, checksum, field map, or risk note applies?
- Which bibliography or dispute record must be read before conclusions?

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
