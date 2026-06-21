# Research Sources And Bibliography / 研究来源与书目

English:
This directory is the human entry point for source objects, bibliography
items, database notes, website routes, package manifests, download logs,
field maps, rights notes, and source-engineering review queues.

简体中文：
本目录是来源对象、书目条目、数据库说明、网页路线、来源包清单、
下载记录、字段映射、权利说明和来源工程复核队列的人工入口。

It prepares evidence routes for later oracle-bone research. It does not
approve imports, clear rights, confirm readings, or turn source metadata
into scholarship.

这里准备后续甲骨文研究所需的证据路线。它不批准导入，不完成权利
清理，不确认释读，也不把来源 metadata 写成学术结论。

## Human Research Entry Order / 人工研究入口顺序

1. Open the relevant source object under `001_source-objects/`.
2. Read the source object `README.md` before the AI packet.
3. Check the `06_human-source-review-sheet.md` review sheet.
4. Check `07_material-access-index.md` for local access routes.
5. Compare the download route, package manifest, and checksum records.
6. Compare the field map and metadata profile with the source system.
7. Check rights status, risk note, and public-commit decision.
8. Use registers and graph edges only to find the next review route.

人工复核时，先进入具体来源对象目录，读人类 README 和人工来源复核表，
再核对下载路线、来源包清单、checksum、字段映射、metadata profile、
权利状态、风险提示和派生路径。CSV、JSON 和图边只用于检索、追溯
和验证，不能替代来源档案。

## Current Materials / 当前资料

- `000_source-registers/`
  holds shared source registers, download manifests, field maps,
  package manifests, metadata profiles, and source status codebooks.
- `001_source-objects/`
  holds concrete source object directories with human-readable and
  AI-readable materials colocated in the same object directory.

## Object-Local Source Materials / 对象内来源资料

Each source object should keep these files together:

- `README.md`: human source overview, scope, and boundary.
- `01_source-packet.json`: AI-readable support packet.
- `02_download-route-index.csv`: access and download route index.
- `03_package-route-index.csv`: package manifest route index.
- `04_field-map-route-index.csv`: field mapping route index.
- `05_metadata-profile-route-index.csv`: downloaded metadata profile route.
- `06_human-source-review-sheet.md`: human source review sheet.
- `07_material-access-index.md`: local access and derived-material index.

对象目录内同时放人类可读资料和 AI 可读辅助资料。不要在 `corpus/`
旁边或来源对象旁边另建并行的人类目录。

## Bibliography And Source Dossier Content / 文献与来源档案内容

A human source or bibliography item should let a reviewer check:

- source provenance: source system, provider, URL, book, paper, or museum;
- bibliographic scope: what corpus area or evidence type it can support;
- citation relation: which record cites it, derives from it, or disputes it;
- access evidence: access date, route, file size, checksum, and manifest;
- extraction evidence: field map, OCR note, parser note, and derived path;
- rights evidence: rights status, visible risk note, and commit decision;
- review evidence: reviewer route, open questions, and review status;
- scholarly caution: proposer, disagreement, and dispute when collected.

人类来源或书目档案应让复核者看到：来源系统、提供方、URL、图书、
论文或博物馆记录；资料适用范围；引用、派生或争议关系；访问日期、
访问路线、文件大小、checksum 和 manifest；字段映射、OCR 或解析
说明、派生路径；权利状态、风险提示、公开提交决定；复核路线、
待查问题、复核状态；以及已收集到的提出者、不同意见和争议。

## Concrete Questions To Check / 具体待查问题

- Which source object still lacks a checksum or file-size record?
- Which source object lacks a package manifest or unpacking note?
- Which source object lacks a field map for database or CSV exports?
- Which source object lacks a visible rights status or risk note?
- Which bibliography item lacks scope, citation relation, or evidence level?
- Which downloaded metadata profile still needs source-system comparison?
- Which route points to a source but lacks a human source review sheet?
- Which graph edge is only source provenance and not scholarship?
- 哪个来源对象还缺 checksum 或文件大小记录？
- 哪个来源对象还缺来源包清单或解包说明？
- 哪个来源对象还缺数据库或 CSV 导出的字段映射？
- 哪个来源对象还缺可见的权利状态或风险提示？
- 哪个书目条目还缺适用范围、引用关系或证据等级？
- 哪个下载 metadata profile 还需要和来源系统核对？
- 哪条路线指向来源，但还缺人工来源复核表？
- 哪条图边只是来源追溯，不能当作学术结论？

## Research Boundary / 研究边界

Source records, route indexes, package manifests, field maps, metadata
profiles, and graph edges are source provenance and preprocessing aids.
They are not source promotion, import approval, rights decisions, confirmed
readings, component assignments, inscription identities, accepted
correspondences, or decipherment conclusions.
They are not a rights decision and not a decipherment conclusion.

来源记录、路线索引、来源包清单、字段映射、metadata profile 和图边
只是来源追溯与预处理辅助资料。它们不是来源提升、导入批准、权利
决定、已确认释读、构件归属、卜辞身份、已接受对应关系或释读结论。

## Regeneration Notes / 再生成说明

When source object materials or registers change, rerun the relevant source
builders and then run repository validation and tests before committing.

来源对象资料或登记表变化后，应重新运行相关来源生成器，再运行仓库
校验和测试，然后提交。
