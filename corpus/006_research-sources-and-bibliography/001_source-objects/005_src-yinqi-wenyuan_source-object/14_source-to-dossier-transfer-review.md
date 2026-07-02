# Source-To-Dossier Transfer Review / 来源进入档案复核表

## English
This human worksheet decides how evidence from this source may enter concrete
character, inscription, plate, collection, later-form, and bibliography
dossiers. It is a review map, not an import approval or scholarship conclusion.

## 简体中文
本表用于人工判断本来源的证据如何进入具体单字、卜辞、图版、馆藏、后世字形和文献档案。它只是复核地图，不是导入批准，也不是学术结论。

## Human Transfer Order / 人工转入顺序
- Open `10_source-evidence-dossier.md` and
  `12_source-provenance-fact-matrix.md`.
- Check route CSV files only as supporting evidence.
- Decide the target object directory before deriving any record.
- Record missing evidence as a concrete question in the target dossier.
- Keep every unresolved reading, relation, and dispute as pending.
- 先读来源证据档案和来源事实矩阵。
- 结构化 CSV/JSON 只作为辅助路线。
- 先确定目标对象目录，再生成派生记录。
- 缺失证据必须写成目标档案中的具体待查问题。
- 未复核释读、关系和争议都保持待查状态。

## Source / 来源
- Source ID / 来源 ID: src-yinqi-wenyuan
- Title / 标题: 殷契文渊 / Oracle Bones Corpus
- Provider / 提供方: Key Laboratory of Oracle Bone Inscriptions Information
  Processing Anyang Normal University; CASS Oracle Studies Center
- Rights status / 权利状态: source_marked_risk_noted
- Review status / 复核状态: reviewed

## Transfer Slots / 转入复核槽位

### 01. Character dossier transfer
- Target / 目标目录: corpus/001_oracle-characters/
- Source evidence / 来源证据: glyph images, rubbings, photographs, variant notes,
  near-form routes, component clues, and source labels
- Next check / 下一步核查: Open character folders only after image rights, source
  identity, and candidate-status wording are checked.

### 02. Inscription and plate transfer
- Target / 目标目录: corpus/002_oracle-bone-inscriptions/
- Source evidence / 来源证据: inscription text, OCR, plate number, catalog number,
  page, Heji or OBM route, text quality, and image path
- Next check / 下一步核查: Keep inscription identity and text readings pending until
  a reviewer checks the source record and plate evidence.

### 03. Collection and findspot transfer
- Target / 目标目录: corpus/005_excavation-sites-periods-and-batches/
- Source evidence / 来源证据: museum object, collection, findspot, period, group,
  batch, excavation note, and catalog provenance
- Next check / 下一步核查: Record each missing archaeology field as a concrete source
  question before using it for context.

### 04. Later-form and relation transfer
- Target / 目标目录: corpus/004_bronze-seal-modern-correspondences/
- Source evidence / 来源证据: variant, near-form, component, bronze-script,
  seal-script, modern-character, and evolution routes
- Next check / 下一步核查: Treat every relation as candidate comparison evidence, not
  an accepted paleographic correspondence.

### 05. Bibliography and dispute transfer
- Target / 目标目录: research/
- Source evidence / 来源证据: book, paper, web page, database note, citation
  relation, proposer, editor, evidence level, disagreement, and dispute
- Next check / 下一步核查: Move nothing into research notes until the bibliography
  route and claim boundary are reviewed.

### 06. Rights and public derivative transfer
- Target / 目标目录: object-local human dossier
- Source evidence / 来源证据: rights status, risk note, checksum, file size, package
  manifest, commit policy, and derived path
- Next check / 下一步核查: Keep raw files local or metadata-only when rights, size,
  or redistribution risk is unresolved.

## Concrete Questions To Carry Forward / 需带入目标档案的问题
- Which visible image, rubbing, plate, or catalog image can be cited?
- Which inscription text, OCR, catalog number, page, or Heji route
  applies?
- Which findspot, collection, period, group, or batch remains missing?
- Which variant, component, later-form, or evolution route is only
  candidate?
- Which bibliography, proposer, disagreement, or dispute must be opened?
- Which rights, checksum, size, or commit-policy issue blocks
  promotion?
- 哪个字形图像、拓片、图版或著录图像可以引用？
- 哪条卜辞全文、OCR、著录号、页码或合集路线适用？
- 哪个出土地、馆藏、时期、组类或批次仍然缺失？
- 哪条异体、构件、后世字形或演化路线仍只是候选？
- 哪条文献、提出者、不同意见或争议必须先打开？
- 哪个权利、checksum、大小或提交策略问题阻止公开提升？

## Boundary / 边界
- not a rights decision
- not corpus import approval
- not a confirmed source promotion
- not an accepted reading
- not a component assignment
- not an inscription identity
- not a correspondence conclusion
- not a decipherment conclusion
- 不是权利结论
- 不是语料导入批准
- 不是来源提升结论
- 不是已接受释读
- 不是构件归属
- 不是卜辞身份确认
- 不是字形对应结论
- 不是破译结论
