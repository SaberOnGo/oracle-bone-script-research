# Character-Inscription Linkage Audit / 字形—卜辞关联审计

## Human Reading Result / 人类阅读结果

- Candidate packet count: 612
- Packets with explicit character-link fields: 0
- Graph edges scanned across JSONL files: 147002
- Cambridge/Hopkins catalog-route graph edges: 4403
- Character-inscription edges promoted: 0
- Character-inscription candidate routes: 7
- Review state: `candidate_only_no_character_inscription_edge_promoted`

## What The Current Evidence Says / 当前证据说明

The raw JSONL row count is used here. The legacy graph summary may count one
edge once per source membership, so its total is not the same denominator.
本审计使用 JSONL 原始行数。旧版图谱统计可能按每个 source membership
重复计数，因此两者的总数分母并不相同。

No packet exposes an explicit linked-character field. The current candidate
rows contain catalog and period/group routing clues, but do not identify a
character project ID or a character position in a plate, image, or inscription
text.

Zero character-inscription graph edges are promoted. 7 candidate route edge(s)
are present, but they remain dataset-only routes until plate, text, position,
and identity evidence is reviewed.

The 4,403 Cambridge/Hopkins graph routes currently describe source, download,
period, group, and catalog references. They do not supply a plate position or
a linked character identity.

当前 Cambridge/Hopkins 图边只描述来源、下载记录、时期、组类和著录路线。
它们没有提供图版位置或已关联的字形身份。

## Evidence Required Before A Relation Edge / 建边前必须补齐的证据

- Open the cited plate, rubbing, photograph, or collection image and record
  its exact source route and rights status.
- Capture the full inscription or OCR as a source transcription, with
  unreadable signs and uncertain positions marked.
- Record the exact plate/image position of each proposed character occurrence;
  do not infer it from a filename or catalog number.
- Link the occurrence to an existing character dossier only when the source
  evidence and project ID are explicit.
- Record the reviewer, source citation, disagreement, and review status before
  changing the edge to a reviewed relation.

## Human Opening Order / 人类复核顺序

- Start with each object-local `07_human-inscription-dossier.md` and
  `21_character-inscription-linkage-review.md`.
- For the H2 source-record candidate, open its
  `02_human-inscription-dossier.md` and
  `09_character-inscription-candidate-graph-route.md`.
- Then open `06_plate-text-gallery.md`, `03_catalog-reference-index.csv`, and
  `13_text-ocr-quality-review.md`.
- Follow the source object dossier and download/manifest records before
  collecting a new image or text route.
- Use `224_character-inscription-linkage-audit-index.json` only as a
  machine-readable count supporting this report.

## Boundary / 边界

This audit is preprocessing and review routing only. It does not make a
character-inscription identity claim, assign a formal `obi-*` ID, accept a
transcription, propose a reading, or conclude decipherment.
It is not a formal `obi-*` ID assignment and does not propose a reading.

本审计只服务于预处理和人工复核路线，不确认字形—卜辞身份关系，
不分配正式 `obi-*` 编号，不接受释文，不提出释读，也不形成破译结论。
