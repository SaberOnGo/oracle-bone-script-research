# Published Scholarship Index / 已发表研究索引

English:
This directory indexes published papers, monographs, catalogs, museum
records, web pages, and databases used by the project. It is the entry point
for deciding whether a source can become a reviewed research note.

简体中文：
本目录索引本项目使用的已发表论文、专著、著录、博物馆记录、网页和
数据库，用于判断某一来源能否进入已复核研究笔记。

## Human Review Entry Order / 人工复核入口顺序

1. Open `002_published-scholarship-review-guide.md`.
2. Open the source object directory and source register row.
3. Check bibliography identity, source trail, rights note, and risk note.
4. Check scope, evidence level, and citation relation.
5. Check reading process status, proposer, disagreement, and dispute.
6. Record unresolved items as concrete next checks, not empty placeholders.

## Item-Level Dossiers / 逐项文献档案

- [HUST-OBC 2024 data paper dossier][hust-paper]: bibliographic identity,
  method and scope, claim-evidence locators, citation relations, limitations,
  rights, object-transfer boundaries, and review log.
- [HUST-OBC 2024 数据论文档案][hust-paper]：记录书目身份、方法与范围、
  说法—证据定位、引用关系、限制、权利、对象转移边界和复核日志。
- [EVOBC 2024 data paper dossier][evobc-paper]: dataset scope, source split,
  technical validation, simulated-deciphering limits, rights, and transfer
  rules.
- [EVOBC 2024 数据论文档案][evobc-paper]：记录数据范围、来源分布、
  技术验证、模拟破译边界、权利和转移规则。
- [OBIMD 2024/2026 paper dossier][obimd-paper]: version relationship,
  fields, evidence locators, proposers, rights conflicts, and transfer rules.
- [OBIMD 2024/2026 论文档案][obimd-paper]：记录版本关系、字段、
  证据定位、责任角色、权利冲突和转移规则。
- [Cambridge Hopkins Finding List dossier][cambridge-hopkins-list]: page
  structure, catalog keys, count reconciliation, rights, and transfer gates.
- [Cambridge Hopkins 馆藏目录档案][cambridge-hopkins-list]：记录页面结构、
  著录代码、数量对账、权利和对象转移门槛。
- [Schwartz Huayuanzhuang East monograph dossier][schwartz-hyz]: publisher
  metadata, HYZ 421 citation route, rights, and page-verification gates.
- [Schwartz 花园庄东甲骨专著档案][schwartz-hyz]：记录出版社 metadata、
  HYZ 421 引用路线、权利和页码核验门槛。

The HUST-OBC paper dossier keeps dataset counts and expert review as
`source-reported`. Its 94.6% closed-set image-classification accuracy is not
a decipherment probability and cannot support an “A means B” claim.

HUST-OBC 论文档案将数据规模和专家复核保持为 `source-reported`。其
94.6%
闭集图像分类准确率不是释读概率，不能支持“甲就是乙”的主张。

人工复核时，先读 `002_published-scholarship-review-guide.md`，再打开来源
对象目录和来源登记行。随后核对书目身份、来源链、权利说明、适用范围、
证据等级、引用关系、释读过程状态、提出者、不同意见和争议。

## Required Content / 必须记录内容

- bibliographic identity: author, title, venue, year, page, plate, URL,
  catalog number, database name, or object record.
- source trail: source object id, source register row, access route,
  checksum, file size, manifest, field map, derived path, and review status.
- scope: which corpus area, inscription, glyph, component, period, batch,
  collection, findspot, or later-script relation the source supports.
- evidence level: primary object record, catalog, database export,
  peer-reviewed paper, book, web note, OCR text, or unreviewed draft.
- citation relation: cites, derives from, summarizes, disputes, or only
  routes to another record.
- reading process status: reported, accepted by cited source, rejected,
  disputed, needs checking, or out of scope.
- proposer and disagreement: who proposed the claim, who disagreed, and
  where the dispute is recorded.

## Concrete Questions To Check / 具体待查问题

- Which source object and register row prove this bibliography item?
- Which page, plate, URL, catalog number, or object record locates it?
- Which corpus object can this source actually support?
- What evidence level is justified by the opened source?
- What is the citation relation to another note or source record?
- What is the reading process status, and is it only reported?
- Who is the proposer, and where is the proposal recorded?
- Which disagreement or dispute is documented, and where?

## Boundary / 边界

An index row is a review route, not confirmed scholarship.
It is not a decipherment conclusion.
It is not a rights decision, source promotion, or corpus import approval.

[hust-paper]: 003_hust-obc-2024_data-paper/README.md
[obimd-paper]: 004_obimd-2024-2026_data-paper/README.md
[evobc-paper]: 005_evobc-2024_data-paper/README.md
[cambridge-hopkins-list]: 006_cambridge-hopkins_finding-list/README.md
[schwartz-hyz]: 007_schwartz-2019_hyz-monograph/README.md
