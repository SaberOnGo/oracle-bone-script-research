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
- Source ID / 来源 ID: src-evobc
- Title / 题名: EVOBC: Evolution Oracle Bone Characters Dataset
- Provider / 提供方: Yuliang Liu research group / arXiv / Open-Oracle
- Source type / 来源类型: open_research_dataset
- Authority tier / 证据等级: peer_reviewed_or_preprint_dataset
- Scope / 适用范围: Large evolution dataset reported with 229170 images and 13714
  character categories across six historical stages from oracle bone characters
  through clerical script.
- Rights status / 权利状态: source_marked_risk_noted
- Review status / 复核状态: reviewed

## Primary Preprint And Dataset Paper / 主要预印本与数据论文
- Citation / 引用: Guan, H., Wan, J., Liu, Y. et al. An open dataset for the
  evolution of oracle bone characters: EVOBC. arXiv:2401.12467.
- Version and DOI / 版本与 DOI: The arXiv record was submitted 2024-01-23 and
  revised to v2 on 2024-02-13; DOI: https://doi.org/10.48550/arXiv.2401.12467.
- Authors and responsibility / 作者与责任: The record lists Haisu Guan, Jinpeng Wan,
  Yuliang Liu, Pengjie Wang, Kaile Zhang, Zhebin Kuang, Xinyu Wang, Shengwei
  Han, Yongge Liu, Xiang Bai, and Lianwen Jin; Yuliang Liu is the corresponding
  author.
- Evidence level / 证据等级: Primary public preprint and dataset descriptor; it
  reports collection and technical validation, not an archaeological catalog
  identity or confirmed reading.

## Reported Dataset Scope / 论文报告的资料范围
- Historical stages / 历史阶段: The paper defines OBC, BI, SS, SAC, WSC, and CS,
  from oracle bone characters through bronze, seal, Spring and Autumn, Warring
  States, and clerical script.
- Reported scale / 论文报告规模: The dataset reports 229,170 images in 13,714
  character categories. Local metadata records are source evidence only; they do
  not mean all images are in this repository.
- Source split / 来源分布: The paper reports 90,882 images from books and 138,288
  from web repositories. Its table names YinQiWenYuan, GuoXueDaShi, Oracle Bone
  Character Compilation, Compilation of Western Zhou Bronze Inscription, Spring
  and Autumn Script Glyph Table, and Table of Glyphs for Warring States.

## Reported Processing And Review / 论文报告的处理与复核
- Book extraction / 图书抽取: The reported pipeline crops page slices, groups slices
  by header OCR and reading order, then extracts image patches with edge
  detection and iterative box merging.
- Web extraction / 网站抽取: The paper says web repositories supplied already
  cropped and aligned images, so the book segmentation steps were not applied in
  the same way.
- Normalization / 规范化: Reported formatting includes background normalization,
  merging simplified and traditional labels, and a Source_Era_ID naming route.
  These are dataset operations, not proof of historical correspondence.
- Human review / 人工复核: The paper reports comparison with original book
  manuscripts, correction or removal of low-quality and wrongly annotated
  images, and external review by oracle-bone scholars.

## Citation And Source Relations / 引用与来源关系
- Cited source routes / 被引来源路线: The paper connects EVOBC to YinQiWenYuan,
  GuoXueDaShi, Oracle Bone Character Compilation, Western Zhou bronze
  inscriptions, Spring and Autumn glyphs, and Warring States glyphs. Each route
  needs its own bibliography and rights review.
- Local package routes / 本地来源包路线: Key&Value.json and List_of_EVOBC.json provide
  category and image-reference metadata; Statistics.xlsx provides a compact
  statistics route. They are reviewed metadata, not raw image rights clearance.
- Object transfer boundary / 对象转入边界: An OBC-to-later-script link is only a
  candidate comparison route until the visible glyph, source page, catalog
  trail, and human dossier are checked.

## Reported Limits, Disputes, And Rights / 限制、争议与权利
- Modern labels / 今字标签: The paper uses modern-character category labels to
  organize samples. Local review keeps them as lookup labels, not confirmed
  oracle readings or evolution claims.
- Simulated deciphering / 释读模拟: The paper reports classification and
  image-generation experiments as simulated deciphering. Their scores and
  generated images are AI validation evidence, not accepted scholarly
  decipherment.
- Source and identity disputes / 来源与身份争议: The paper combines multiple books and
  websites; category merging, source labels, OCR grouping, and alleged evolution
  links require independent human comparison. No dispute is resolved by this
  source note.
- License / 许可: The arXiv record links a CC BY-NC-ND 4.0 deed. Local rights
  status remains source_marked_risk_noted because component images and
  third-party book or website material need separate rights checks.

## Concrete Bibliography Checks / 具体文献核查
- Verify the arXiv version, DOI, author list, and local checksum
  rows before citing a paper-reported count.
- Open each named book and website route and record page, plate,
  catalog, object, and image provenance where available.
- Compare Key&Value.json, List_of_EVOBC.json, Statistics.xlsx,
  and the paper before promoting any category or stage mapping.
- For every candidate evolution edge, preserve the visible form,
  source route, modern label, and human review status separately.
- 复核 arXiv 版本、DOI、作者名单和本地 checksum 后，才能引用
  论文报告的统计数值。
- 逐一打开论文所列图书和网站，记录页码、图版、著录号、
  馆藏对象和图像出处。
- 将 Key&Value.json、List_of_EVOBC.json、Statistics.xlsx 与
  论文相互核对，再决定是否生成派生字段。
- 每条候选演化边都要分开保存可见字形、来源路线、今字标签
  和人工复核状态，不写成已确认对应关系。

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
