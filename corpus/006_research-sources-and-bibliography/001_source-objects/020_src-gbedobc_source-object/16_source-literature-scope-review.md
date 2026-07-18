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
- Source ID / 来源 ID: src-gbedobc
- Title / 题名: GBEDOBC graph-based evolutionary dataset
- Provider / 提供方: Qingju Jiao et al. / npj Heritage Science / GitHub
- Source type / 来源类型: open_research_dataset
- Authority tier / 证据等级: peer_reviewed_dataset
- Scope / 适用范围: Graph-based evolutionary dataset linking oracle bone characters
  to later scripts.
- Rights status / 权利状态: source_marked_risk_noted
- Review status / 复核状态: reviewed

## Primary Publication / 主要论文
- Citation / 引用: Jiao, Q., Wu, J., Liu, Q. et al. A graph-based evolutionary
  dataset for oracle bone characters from inscriptions to modern Chinese
  scripts. npj Heritage Science 13, 369 (2025).
- DOI and dates / DOI 与日期: DOI: https://doi.org/10.1038/s40494-025-01951-0.
  Received 2025-04-21, accepted 2025-07-13, and published 2025-07-26.
- Responsible roles / 责任分工: The paper records Qingju Jiao, Jingwen Wu, Qi Liu,
  Han Zhang, Zhan Zhang, Bang Li, Jing Xiong, Guoying Liu, and Yongge Liu. It
  assigns design, collection, processing, validation, and writing roles rather
  than a single decipherment authority.
- Evidence level / 证据等级: Primary peer-reviewed dataset article; it reports a
  graph representation and computational comparison, not an archaeological
  catalog identity or accepted reading.

## Reported Dataset And Source Scope / 论文报告的数据范围
- Reported scale / 论文报告规模: The paper reports 756 groups and 3,780 Chinese
  characters across five stages: oracle bone, bronze, seal, official, and
  regular script. Local routes record this as source scope, not as 3,780
  imported corpus records.
- Upstream image source / 上游图像来源: The paper says its 4,860 source images in 972
  groups came from an earlier image-based dataset, with Guo Xue Da Shi and the
  Chinese Character Etymology and Evolution Dictionary named as primary source
  routes.
- Stage and image boundary / 阶段与图像边界: The five-stage graph groups are not the
  six-stage EVOBC scope. Do not merge their stages, labels, images, or group IDs
  without a source-level crosswalk.

## Reported Processing And Graph Method / 处理与图结构方法
- Image preparation / 图像预处理: The paper reports grayscale conversion and
  normalization to 105 by 105 pixels before comparing image and graph routes.
- Graph construction / 图结构构建: The reported method extracts key points, connects
  them by stroke-based relations, compresses the graph, and compares
  adjacency-matrix features across stages.
- Validation / 技术验证: DHC-E, FEATHER, and GL2vec are compared with image-based
  methods for computational similarity and stability. These scores validate a
  method, not a historical correspondence.

## Citation And Access Relations / 引用与访问关系
- Data and code route / 数据与代码路线: The paper provides 3,780 images and graph
  matrices, plus derived vectors, through the BrisksHan/GBEDOBC GitHub route.
  The local package keeps provenance and checksum records only.
- Upstream citations / 上游引用路线: The article cites the earlier image-based
  evolution dataset, EVOBC, Guo Xue Da Shi, and the Chinese Character Etymology
  and Evolution Dictionary. Each needs independent bibliography and rights
  review.
- Human dossier transfer / 人类档案转入: A graph edge may guide comparison, but a
  human dossier must retain the source image, page or catalog trail, modern
  label, graph route, and pending review status separately.

## Limits, Disputes, And Rights / 限制、争议与权利
- Graph identity boundary / 图节点身份边界: A node or edge in a graph is a dataset
  representation. It does not by itself establish a glyph identity, component,
  variant, or evolution relationship.
- Source and label disputes / 来源与标签争议: The dataset inherits upstream image,
  label, stage, and source choices. The paper does not resolve every catalog,
  modern-label, or historical correspondence question.
- License / 许可: The article states CC BY-NC-ND 4.0 and warns that third-party
  material may have separate credit lines. Keep repository and upstream book or
  website rights as separate review items.

## Concrete Bibliography Checks / 具体文献核查
- Verify the DOI, article dates, author roles, PDF checksum, and
  GitHub revision before citing a count or method.
- Open the earlier image dataset, Guo Xue Da Shi, and the cited
  dictionary to record page, image, and label provenance.
- Compare the 756-group/3,780-character scope with EVOBC only after
  a stage, category, and source-level crosswalk is reviewed.
- Keep graph nodes, edges, modern labels, images, and historical
  claims in separate evidence fields in later dossiers.
- 复核 DOI、论文日期、作者分工、PDF checksum 和 GitHub 版本，
  再引用统计数值或处理方法。
- 打开上游图像数据集、国学大师和所引字源工具书，记录页码、
  图像和标签出处。
- 将 756 组、3780 字形与 EVOBC 比较前，先完成阶段、类别和
  来源层级的 crosswalk 复核。
- 后续档案分开保存图节点、图边、今字标签、图像和历史判断，
  不把图结构直接写成已确认演化关系。

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
