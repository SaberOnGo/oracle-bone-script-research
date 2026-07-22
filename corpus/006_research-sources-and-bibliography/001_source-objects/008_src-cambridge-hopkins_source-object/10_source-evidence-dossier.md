# Source Evidence Dossier / 来源证据档案

This human dossier gathers bibliography, access, download, checksum, rights,
risk, field-map, package, and derivative-route evidence for one source object.

本档案整理来源对象的书目、访问、下载、checksum、权利、风险、字段映射、来源包和派生路线证据。它服务后续人工复核，不给出释读或权利结论。

## Bibliography And Source Identity / 书目与来源身份
- Source ID / 来源 ID: src-cambridge-hopkins
- Title / 标题: Hopkins Collection of Chinese Oracle Bones Finding List
- Provider / 提供方: Cambridge University Library
- Source type / 来源类型: library_collection
- Source URL / 来源链接: https://www.lib.cam.ac.uk/collections/departments/chinese-c
  ollections/chinese-collections-te-cang-yu-zhuan-cang/finding-list
- Scope / 适用范围: Finding list for the Hopkins Collection with period/topic table
  and cross-references to CUL numbers, Chalfant, Heji and Yingguo suo cang jiagu
  ji references.
- Authority tier / 证据等级: university_library_collection
- Adoption status / 采用状态: adopted_collection_reference

## Access Download Checksum And Size / 访问、下载、checksum 与大小
- Download route count / 下载路线数: 1
- Download statuses / 下载状态: downloaded
- Checksum route count / checksum 路线数: 1
- Size route count / 大小记录路线数: 1
- Local temp route count / 临时路径路线数: 1
Open `02_download-route-index.csv` before reusing any downloaded file. Check
URL, access date, checksum, file size, local archive path, rights note, and
review status.

复用任何下载文件前，应打开
`02_download-route-index.csv`，核对链接、访问日期、checksum、大小、本地归档路径、权利说明和复核状态。

## Download Route Evidence / 下载路线证据

### Route 001
- Download ID / 下载 ID: dl-cambridge-hopkins-finding-list
- Artifact kind / 资料类型: library_finding_list
- Status / 状态: downloaded
- HTTP status / HTTP 状态: 200
- File size bytes / 文件大小 bytes: 74132
- Checksum SHA-256 / checksum SHA-256:
  f11bc30e9893e5d5b3d32371364d59503f100157aaa612800974883f5a78b4e7
- Commit policy / 提交策略: download_to_tmp_log_checksum_only
- Local temp path / 本地临时路径:
  tmp/source_downloads/dl-cambridge-hopkins-finding-list.html
- Risk note / 风险提示: Stored under ignored tmp directory; commit log/checksum
  only.
- Review status / 复核状态: metadata_route_needs_human_review

## Package Manifest Field Map And Derivatives / 来源包清单、字段映射与派生记录
- Package route count / 来源包路线数: 1
- Package kinds / 来源包类型: lightweight_html_page
- Field map route count / 字段映射路线数: 2
- Target record types / 目标记录类型: oracle_inscription; statistics
- Metadata route count / metadata 路线数: 6
Package rows, field maps, and metadata profiles are candidate routes. They do
not approve corpus import until a human reviewer checks the source trail and
target object directory.

来源包清单、字段映射和 metadata profile 只是候选路线。必须由人工复核来源链和目标对象目录后，才可进入语料导入。

## Package Manifest Evidence / 来源包清单证据

### Route 001
- Package file ID / 来源包文件 ID: pkg-file-000015
- Source package ID / 来源包 ID: light-src-cambridge-hopkins
- File name / 文件名: dl-cambridge-hopkins-finding-list.html
- File kind / 文件类型: lightweight_html_page
- File size bytes / 文件大小 bytes: 74132
- Download ID / 下载 ID: dl-cambridge-hopkins-finding-list
- Commit policy / 提交策略: download_to_tmp_log_checksum_only
- Handling strategy / 处理策略: Lightweight source evidence is represented by
  committed provenance, size, checksum, and derived metadata only; ignored tmp
  downloads are not committed as source content.
- Rights status / 权利状态: metadata_only_until_verified
- Review status / 复核状态: reviewed_metadata_only

## Field Map Evidence / 字段映射证据

### Route 001
- Field map ID / 字段映射 ID: field-map-000019
- Source level / 来源层级: finding_list_key
- Source field or unit / 来源字段或单位: y; c; h; j
- Source meaning / 来源含义: Hopkins list cross-reference keys for Yingguo; CUL;
  Chalfant; Heji
- Target record type / 目标记录类型: oracle_inscription
- Target project field / 目标字段: external_ref_ids; catalog_crosswalk
- Import action / 导入动作: Use to build inscription-level crosswalk records and
  Heji links
- Rights boundary / 权利边界: Finding list metadata only; images and 3D assets need
  separate rights review
- Evidence download ID / 证据下载 ID: dl-cambridge-hopkins-finding-list
- Review status / 复核状态: reviewed_metadata_only

### Route 002
- Field map ID / 字段映射 ID: field-map-000020
- Source level / 来源层级: classified_table
- Source field or unit / 来源字段或单位: period and topic totals
- Source meaning / 来源含义: Collection-level period/topic distribution table
- Target record type / 目标记录类型: statistics
- Target project field / 目标字段: topic_distribution_summary;
  period_distribution_summary
- Import action / 导入动作: Use as collection-level summary and not as
  character-level evidence
- Rights boundary / 权利边界: Table values need explicit source citation if
  extracted later
- Evidence download ID / 证据下载 ID: dl-cambridge-hopkins-finding-list
- Review status / 复核状态: reviewed_metadata_only

## Metadata Profile Evidence / 元数据概况证据

### Route 001
- Profile ID / 概况 ID: metadata-profile-000063
- Evidence download ID / 证据下载 ID: dl-cambridge-hopkins-finding-list
- Metadata file / 元数据文件: 21_finding-list-reconciliation.md
- Profile metric / 概况指标: finding_list_imported_row_count
- Profile value / 概况值: 612
- Profile unit / 概况单位: rows
- Import relevance / 导入相关性: Records the number of identifier rows retained in
  the reviewed Cambridge finding-list staging audit
- Caution / 提醒: Staging-row count is a reconciliation fact; it is not a count of
  confirmed objects, inscriptions, or readings
- Review status / 复核状态: reviewed_metadata_only

### Route 002
- Profile ID / 概况 ID: metadata-profile-000064
- Evidence download ID / 证据下载 ID: dl-cambridge-hopkins-finding-list
- Metadata file / 元数据文件: 21_finding-list-reconciliation.md
- Profile metric / 概况指标: finding_list_page_stated_grand_total
- Profile value / 概况值: 609
- Profile unit / 概况单位: rows_stated_by_source_page
- Import relevance / 导入相关性: Preserves the grand total stated by the source page
  for human reconciliation against retained rows
- Caution / 提醒: The page-stated total is source-page metadata and does not
  authorize filling or deleting any row
- Review status / 复核状态: reviewed_metadata_only

### Route 003
- Profile ID / 概况 ID: metadata-profile-000065
- Evidence download ID / 证据下载 ID: dl-cambridge-hopkins-finding-list
- Metadata file / 元数据文件: 21_finding-list-reconciliation.md
- Profile metric / 概况指标: finding_list_import_vs_stated_difference
- Profile value / 概况值: 3
- Profile unit / 概况单位: rows_difference
- Import relevance / 导入相关性: Keeps the unresolved difference visible so a
  researcher can trace it to the source page before any crosswalk promotion
- Caution / 提醒: Difference is an open preprocessing question, not evidence of
  missing or duplicate inscriptions by itself
- Review status / 复核状态: reviewed_metadata_only

### Route 004
- Profile ID / 概况 ID: metadata-profile-000066
- Evidence download ID / 证据下载 ID: dl-cambridge-hopkins-finding-list
- Metadata file / 元数据文件: 21_finding-list-reconciliation.md
- Profile metric / 概况指标: finding_list_sections_with_declared_count_mismatch
- Profile value / 概况值: 4
- Profile unit / 概况单位: sections
- Import relevance / 导入相关性: Routes four section-level count mismatches to the
  human reconciliation dossier for targeted checking
- Caution / 提醒: Section mismatch count is an audit signal and not a period,
  group, identity, or decipherment conclusion
- Review status / 复核状态: reviewed_metadata_only

### Route 005
- Profile ID / 概况 ID: metadata-profile-000067
- Evidence download ID / 证据下载 ID: dl-cambridge-hopkins-finding-list
- Metadata file / 元数据文件: 21_finding-list-reconciliation.md
- Profile metric / 概况指标: finding_list_sections_without_declared_count
- Profile value / 概况值: 2
- Profile unit / 概况单位: sections
- Import relevance / 导入相关性: Records that the source page leaves two observed
  sections without a declared count
- Caution / 提醒: An unstated count remains a source-page omission and must not be
  converted into an inferred total
- Review status / 复核状态: reviewed_metadata_only

### Route 006
- Profile ID / 概况 ID: metadata-profile-000068
- Evidence download ID / 证据下载 ID: dl-cambridge-hopkins-finding-list
- Metadata file / 元数据文件: 21_finding-list-reconciliation.md
- Profile metric / 概况指标: finding_list_unclassified_row_count
- Profile value / 概况值: 4
- Profile unit / 概况单位: rows
- Import relevance / 导入相关性: Keeps the four source-page Unclassified entries
  visible for separate catalogue and image follow-up
- Caution / 提醒: Unclassified is the source-page label; it is not a character
  identity, inscription identity, or scholarly classification
- Review status / 复核状态: reviewed_metadata_only

## Human Research Review Slots / 人工研究复核槽位

Use the source rows above to decide what can be carried into a human object
dossier. The first review task is not import; it is to identify visible glyph
image, rubbing, photograph, plate, catalog, inscription, OCR, provenance,
findspot, collection, period, group, variant, near-form, component,
later-script, bibliography, citation, disagreement, and dispute evidence.

- Glyph image and rubbing check / 字形图像与拓片检查:
  复核：本来源是否提供可复核的字形图像、拓片、照片或图版页，以及这些材料能否放入具体单字、卜辞或图版档案。
- Inscription and catalog context / 卜辞与著录上下文:
  复核：本来源是否记录卜辞全文、OCR、图版号、页码、合集号、著录号或数据库编号，以及文本质量和缺失位置。
- Provenance and dating context / 出处与年代背景:
  复核：本来源是否记录出土地、馆藏、时期、组类、批次、收藏对象或考古背景；没有记录时要写成具体缺口。
- Variant component relation check / 异体构件关系检查:
  复核：本来源是否只提供候选异体、近形、构件、金文、小篆、今字或字形演化关系；不得直接写成确认结论。
- Bibliography citation dispute check / 书目引用争议检查:
  复核：本来源说明、书目、网页或论文中是否有提出者、引用关系、不同意见、争议或适用范围限制。
- Rights and derivative decision / 权利与派生决定:
  复核：本来源哪些图像、文本、OCR、索引、表格或统计结果可公开派生，哪些只能保留来源记录和人工复核问题。

### Source-To-Dossier Research Lenses / 来源进入档案的研究视角

Glyph image lens: compare each visible glyph image with its rubbing, photograph,
plate, catalog note, and object provenance before it is copied into a character
dossier.

Inscription lens: compare inscription text, OCR text, catalog number, plate
number, page number, Heji number, and text quality before linking a form to an
inscription dossier.

Provenance lens: check findspot, collection, period, group, batch, museum
object, excavation note, and catalog provenance before using the source for
dating or archaeological context.

Form relation lens: treat variant, near-form, component, bronze-script,
seal-script, modern-character, and evolution relations as candidate comparison
evidence until reviewed.

Scholarship lens: keep bibliography, citation, proposer, editor, scope,
disagreement, dispute, and rights evidence visible beside any later human note
derived from this source.

Modern labels, dataset names, source fields, and download-route captions are not
an accepted reading, glyph identity, component assignment, inscription identity,
or historical correspondence.

## Scope Evidence Level And Review Status / 适用范围、证据等级与复核状态
- Rights status / 权利状态: metadata_only_until_verified
- Review status / 复核状态: reviewed
- Risk note / 风险提示: Official university library finding list; linked digitized
  assets require separate rights and IIIF review.
- Processing status card / 处理状态卡: 08_source-processing-status.md
- Auxiliary JSON / 辅助 JSON: 11_source-evidence-dossier-index.json

## Citation Disagreement And Risk Notes / 引用、分歧与风险记录
- Citation relationship / 引用关系: 待查：先开
  `07_material-access-index.md`、`11_source-evidence-dossier-index.json`，再核对引用关系。
- Proposer or editor / 提出者或整理者: 待查：先开 `07_material-access-index.md`
  和`04_field-map-route-index.csv` 核对提出者或整理者线索。
- Different opinions / 不同意见: 待查：先开 `07_material-access-index.md`
  和`08_source-processing-status.md` 核对不同意见线索。
- Disputes / 争议: 待查：先开
  `07_material-access-index.md`、`08_source-processing-status.md` 和风险说明核对争议线索。
Do not treat absence of a dispute row as scholarly agreement. It only means the
current preprocessing register still needs a specific follow-up check for that
human review field.

没有争议行不等于学界已经一致，只表示当前预处理登记表尚未采集这类人工复核字段。

## Concrete Questions To Check / 具体待查问题
- Which bibliography or database note defines this source?
- 哪条书目、论文、网页或数据库说明界定本来源？
- Which access, download, checksum, and size rows can be verified?
- 哪些访问、下载、checksum 和大小记录可以复核？
- Which package files are safe derived records rather than raw dumps?
- 哪些来源包文件是安全派生记录，而不是原始大包？
- Which field maps can enter concrete corpus object directories?
- 哪些字段映射可以进入具体语料对象目录？
- Which proposer, citation relation, disagreement, or dispute remains?
- 还缺哪位提出者、引用关系、不同意见或争议？
- Which rights or redistribution risk blocks public promotion?
- 哪些权利或再分发风险阻止公开提升？

## Boundary / 边界
- not a rights decision
- not corpus import approval
- not a confirmed source promotion
- not an accepted modern label or reading
- not a reading
- not a component assignment
- not an inscription identity
- not a decipherment conclusion
- 不是权利结论
- 不是语料导入批准
- 不是已确认来源提升
- 不是释读
- 不是构件归属
- 不是卜辞身份确认
- 不是破译结论
