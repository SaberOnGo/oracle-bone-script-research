# Source Literature Scope Review / 来源文献适用范围复核

## English
This human review file keeps bibliography, database notes, source scope,
evidence level, proposer or editor, citation relations, different opinions, and
disputes visible before the source is used in any later character, inscription,
topic, or bibliography dossier.

## 简体中文
本文件在来源进入后续单字、卜辞、主题或文献档案前，先把书目、数据库说明、资料适用范围、证据等级、提出者或整理者、引用关系、不同意见和争议作为人类复核项目保留在同
一来源对象目录内。

## Source / 来源
- Source ID / 来源 ID: src-obimd
- Title / 题名: OBIMD: Oracle Bone Inscriptions Multi-modal Dataset
- Provider / 提供方: Key Laboratory of Oracle Bone Inscriptions Information
  Processing Anyang Normal University; Xiamen University; Tencent Youtu Lab;
  University of Cambridge; Scientific Data
- Source type / 来源类型: open_research_dataset
- Authority tier / 证据等级: peer_reviewed_dataset
- Scope / 适用范围: Multi-modal OBI dataset with 10077 oracle bone images, 93652
  annotated characters, 21941 syntactically validated sentences, and reading
  sequences.
- Legacy rights status / 历史权利状态: licensed_for_repository
- Effective rights status / 当前有效权利状态:
  `metadata_only_until_verified`
- Active override / 生效覆盖:
  `project_registry/004_asset-source-and-rights-index/`
  `006_obimd-rights-status-override.csv`
- Review status / 复核状态: reviewed

## Primary Publication / 主要论文
- Citation / 引用: Li, B., Yang, J., Liang, Y. et al. OBIMD: A Multi-modal Dataset
  for Contextual Interpretation of Oracle Bone Inscriptions. Scientific Data 13,
  681 (2026).
- DOI / DOI: https://doi.org/10.1038/s41597-026-06967-0
- Publication dates / 发表日期: Received 2025-07-16; accepted 2026-02-24; published
  2026-03-14; version of record 2026-04-30.
- Responsible roles / 责任分工: Bang Li and Jing Yang are recorded as equal first
  contributors; Donghao Luo and Taisong Jin are the corresponding authors. The
  paper also records manual annotation and annotation-coordination roles.
- Evidence level / 证据等级: Primary peer-reviewed data descriptor; it documents a
  multimodal dataset and workflow, not a final transcription or accepted
  reading.

## Paper-Reported Research Process / 论文报告的处理过程
- Material base / 资料基础: The paper reports 10,077 rubbing images: 9,913 from
  Jiaguwen Heji and 164 from Huayuanzhuang East material, with aligned facsimile
  and transcription routes.
- Facsimile relation / 摹本关系: Pixel-aligned facsimiles were redrawn by
  integrating selected rubbings with facsimile references; they are not simply
  treated as direct originals of the cited series.
- Annotation stages / 标注阶段: The reported workflow has data acquisition,
  pre-annotation, and collaborative annotation and verification. Graduates
  cross-check cases; experts arbitrate unresolved cases.
- Reported structure / 论文报告结构: The dataset reports 93,652 annotated characters,
  21,667 missing-character positions, 21,941 sentence units, and 4,192
  non-sentential elements.

## Human Research Relevance / 人类研究相关性
- Reading context / 阅读上下文: Rubbing, facsimile, transcription, character boxes,
  groups, and reading-order fields are routes for opening evidence before
  interpretation.
- Uncertainty fields / 不确定字段: SeatFont marks missing positions; Mark records
  exceptional or unresolved cases. Label and SubLabel remain dataset routes, not
  confirmed character identities.
- Modern label boundary / 今字边界: The paper supplies modern-character
  transcription for reference and lookup; local review must not treat it as a
  final decipherment result.

## Citation And Access Relations / 引用与访问关系
- Data and code routes / 数据与代码路线: The article points to Hugging Face
  KLOBIP/OBIMD for data, libang1991/OBIMD on GitHub for code, and the JGWL
  platform for the annotation environment.
- Cited source routes / 被引来源路线: Important routes include YinQiWenYuan, Jiaguwen
  Heji, Huayuanzhuang East material, Jiaguwen Moben Daxi, the Oracular Digital
  Platform, HUST-OBC, and EVOBC.

## Reported Limits And Disputes / 论文报告限制与争议
- Source-layer distinction / 来源层次区别: Rubbings, facsimiles, redrawn facsimiles,
  and transcriptions must remain distinct; alignment does not prove equal
  evidentiary status.
- Unresolved cases / 待解决情况: Placeholders, uncertain groups, special marks, and
  disputed classifications remain review routes rather than resolved
  scholarship.
- License conflict / 许可冲突: The article states CC BY-NC-ND 4.0, while local
  dataset-card and repository notes use different wording. Keep the rights
  discrepancy visible and review each derivative.
- Large files / 大文件: Raw annotation and image packages remain outside ordinary
  Git where required; only source-marked, reviewed derivatives may enter object
  dossiers.

## Concrete Bibliography Checks / 具体文献核查
- Verify the DOI, Hugging Face snapshot, GitHub revision, and
  local package checksums before reusing any field or count.
- Open the Heji, Huayuanzhuang East, YinQiWenYuan, and facsimile
  routes before transferring a sentence or plate claim.
- Keep rubbing, facsimile, redraw, transcription, Label, and
  SubLabel as separate evidence layers in inscription dossiers.
- Record placeholders, Mark values, disputed labels, and missing
  positions as concrete review questions.
- 复核 DOI、Hugging Face 快照、GitHub 版本和本地来源包 checksum，
  再复用具体字段或统计数值。
- 打开合集、出土地点、殷契文渊和摹本路线后，才能转入卜辞档案。
- 在卜辞档案中分开保存拓片、摹本、重绘摹本、释文、Label 和
  SubLabel，不能把它们合并成单一证据层。
- 把占位框、Mark 值、争议标签和缺失位置写成具体待复核问题。

## Literature And Database Review Slots / 文献与数据库复核槽位
- Bibliography note / 书目说明: Open README.md and 10_source-evidence-dossier.md
  before citing this source in a later research note.
- Database scope / 数据库范围: Record which object type, catalog range, plate range,
  glyph range, or inscription range the source actually covers.
- Evidence level / 证据等级: Keep authority tier and source type visible; do not
  treat them as a scholarly conclusion.
- Proposer or editor / 提出者或整理者: Check source notes, database pages, paper
  metadata, or catalog front matter before assigning responsibility.
- Citation relation / 引用关系: Record whether the source cites a catalog,
  dictionary, paper, museum record, database export, or derived index.
- Different opinions / 不同意见: Absence of a disagreement row is not agreement; it
  is a pending review question until checked against bibliography notes.
- Dispute record / 争议记录: Keep disputed readings, labels, source fields, and
  mappings as pending review routes.

## Concrete Questions To Check / 具体待查问题
- Which book, paper, webpage, museum record, or database note defines
  this source?
- Which source scope is directly supported by the local evidence rows?
- Which proposer, editor, compiler, or institution should be recorded?
- Which catalog, dictionary, paper, or database does this source cite?
- Which alternate label, disagreement, or dispute remains unresolved?
- Which later object dossier should receive only a route, not a claim?
- 哪条书目、论文、网页、馆藏记录或数据库说明界定本来源？
- 哪个资料范围能由本目录内证据行直接支持？
- 哪位提出者、整理者、编者或机构需要记录？
- 本来源引用了哪种著录、字编、论文或数据库？
- 哪个替代标签、不同意见或争议仍未解决？
- 哪个后续对象档案只能接收复核路线，而不能接收结论？

## Local Evidence To Open / 本地证据入口
- README.md
- 06_human-source-review-sheet.md
- 07_material-access-index.md
- 10_source-evidence-dossier.md
- 12_source-provenance-fact-matrix.md
- 14_source-to-dossier-transfer-review.md

## Boundary / 边界
- not a rights decision
- not corpus import approval
- not a confirmed bibliography conclusion
- not an accepted reading
- not a component assignment
- not an inscription identity
- not a correspondence conclusion
- not a decipherment conclusion
- 不是权利结论
- 不是语料导入批准
- 不是已确认的文献学结论
- 不是已接受释读
- 不是构件归属
- 不是卜辞身份确认
- 不是字形对应结论
- 不是破译结论
