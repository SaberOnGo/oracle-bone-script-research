# src-obimd Human Source Review Sheet

## Source Provenance Review / 来源出处复核
Use this sheet to decide which source routes have enough provenance for safe
preprocessing, and which routes still need human review before any derived
record is promoted.

本表用于判断哪些来源路线已有足够出处证据，可以进入安全的预处理；哪些路线仍需人工复核，才能提升为派生记录。

## Review Scope / 复核范围
Review source provenance, access status, package or file metadata, field
mapping, rights status, and whether any raw material is safe to promote into
object-local derived records.

只复核来源出处、访问状态、来源包或文件 metadata、字段映射、权利状态，以及是否可以把某些原始资料提升为对象内派生记录。

## Checklist / 清单
- [ ] Source register row checked against `01_source-packet.json`
- [ ] Download routes checked in `02_download-route-index.csv`
- [ ] Package manifest checked in `03_package-route-index.csv`
- [ ] Field maps checked in `04_field-map-route-index.csv`
- [ ] Metadata profiles checked in `05_metadata-profile-route-index.csv`
- [ ] Processing card checked in `08_source-processing-status.md`
- [ ] Rights status reviewed before any asset promotion
- [ ] No reading, identity, component, or inscription claim added

## Concrete Questions To Check / 具体待查问题
- [ ] Which source register row anchors this source?
- [ ] 哪条来源登记行可以定位本来源？
- [ ] Which download or access routes have dates, sizes, and checksums?
- [ ] 哪些下载或访问路线已有日期、大小和 checksum？
- [ ] Which package manifest rows describe reusable derived files?
- [ ] 哪些来源包 manifest 行描述了可复用的派生文件？
- [ ] Which field maps can safely feed corpus object records?
- [ ] 哪些字段映射可以安全进入语料对象？
- [ ] What rights or redistribution risk blocks public promotion?
- [ ] 哪些权利或再分发风险阻止公开提升？
- [ ] Which object-local corpus directories should receive derivatives?
- [ ] 哪些对象内语料目录应接收派生记录？

## Status / 状态
- Source ID / 来源 ID: src-obimd
- Rights status / 权利状态: licensed_for_repository
- Review status / 复核状态: needs_human_source_review
- Decipherment claim status / 释读结论状态: no_claim
