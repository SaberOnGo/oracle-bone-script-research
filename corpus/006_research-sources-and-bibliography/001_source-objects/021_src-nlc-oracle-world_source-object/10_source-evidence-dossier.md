# Source Evidence Dossier / 来源证据档案

This human dossier gathers bibliography, access, download, checksum, rights,
risk, field-map, package, and derivative-route evidence for one source object.

本档案整理来源对象的书目、访问、下载、checksum、权利、风险、字段映射、来源包和派生路线证据。它服务后续人工复核，不给出释读或权利结论。

## Bibliography And Source Identity / 书目与来源身份
- Source ID / 来源 ID: src-nlc-oracle-world
- Title / 标题: 甲骨世界 / Oracle Bones Database
- Provider / 提供方: National Library of China / Chinese Ancient Books Resource
  Platform
- Source type / 来源类型: library_database
- Source URL / 来源链接: https://www.nlc.cn/
- Scope / 适用范围: National Library of China oracle-bone holdings and Oracle World
  database evidence from official NLC PDFs; current notes report NLC holdings of
  35651 oracle bones and Oracle World records for oracle-bone objects, images,
  rubbings and rubbing images.
- Authority tier / 证据等级: national_library
- Adoption status / 采用状态: candidate_institutional_official_scope_confirmed

## Access Download Checksum And Size / 访问、下载、checksum 与大小
- Download route count / 下载路线数: 2
- Download statuses / 下载状态: downloaded
- Checksum route count / checksum 路线数: 2
- Size route count / 大小记录路线数: 2
- Local temp route count / 临时路径路线数: 2
Open `02_download-route-index.csv` before reusing any downloaded file. Check
URL, access date, checksum, file size, local archive path, rights note, and
review status.

复用任何下载文件前，应打开
`02_download-route-index.csv`，核对链接、访问日期、checksum、大小、本地归档路径、权利说明和复核状态。

## Download Route Evidence / 下载路线证据

### Route 001
- Download ID / 下载 ID: dl-nlc-oracle-world-note
- Artifact kind / 资料类型: official_note_pdf
- Status / 状态: downloaded
- HTTP status / HTTP 状态: 200
- File size bytes / 文件大小 bytes: 3339464
- Checksum SHA-256 / checksum SHA-256:
  5b4ef3adb1c0e5b512ab32ee33b206503b8bac2607c9bb55978c940fe2caca7a
- Commit policy / 提交策略: download_to_tmp_log_checksum_only
- Local temp path / 本地临时路径: tmp/source_downloads/dl-nlc-oracle-world-note.pdf
- Risk note / 风险提示: Stored under ignored tmp directory; commit log/checksum
  only.
- Review status / 复核状态: metadata_route_needs_human_review

### Route 002
- Download ID / 下载 ID: dl-nlc-oracle-database-design
- Artifact kind / 资料类型: official_design_pdf
- Status / 状态: downloaded
- HTTP status / HTTP 状态: 200
- File size bytes / 文件大小 bytes: 130034
- Checksum SHA-256 / checksum SHA-256:
  ee69eacf0ad17dc29696d7a80688a56d7bb0d18eb0136671bf32ed179d0f8ed9
- Commit policy / 提交策略: download_to_tmp_log_checksum_only
- Local temp path / 本地临时路径:
  tmp/source_downloads/dl-nlc-oracle-database-design.pdf
- Risk note / 风险提示: Stored under ignored tmp directory; commit log/checksum
  only.
- Review status / 复核状态: metadata_route_needs_human_review

## Package Manifest Field Map And Derivatives / 来源包清单、字段映射与派生记录
- Package route count / 来源包路线数: 2
- Package kinds / 来源包类型: lightweight_pdf
- Field map route count / 字段映射路线数: 4
- Target record types / 目标记录类型: oracle_inscription; oracle_inscription;
  excavation_or_collection_context; source_reference
- Metadata route count / metadata 路线数: 7
Package rows, field maps, and metadata profiles are candidate routes. They do
not approve corpus import until a human reviewer checks the source trail and
target object directory.

来源包清单、字段映射和 metadata profile 只是候选路线。必须由人工复核来源链和目标对象目录后，才可进入语料导入。

## Package Manifest Evidence / 来源包清单证据

### Route 001
- Package file ID / 来源包文件 ID: pkg-file-000022
- Source package ID / 来源包 ID: light-src-nlc-oracle-world
- File name / 文件名: dl-nlc-oracle-database-design.pdf
- File kind / 文件类型: lightweight_pdf
- File size bytes / 文件大小 bytes: 130034
- Download ID / 下载 ID: dl-nlc-oracle-database-design
- Commit policy / 提交策略: download_to_tmp_log_checksum_only
- Handling strategy / 处理策略: Lightweight source evidence is represented by
  committed provenance, size, checksum, and derived metadata only; ignored tmp
  downloads are not committed as source content.
- Rights status / 权利状态: metadata_only_until_verified
- Review status / 复核状态: reviewed_metadata_only

### Route 002
- Package file ID / 来源包文件 ID: pkg-file-000023
- Source package ID / 来源包 ID: light-src-nlc-oracle-world
- File name / 文件名: dl-nlc-oracle-world-note.pdf
- File kind / 文件类型: lightweight_pdf
- File size bytes / 文件大小 bytes: 3339464
- Download ID / 下载 ID: dl-nlc-oracle-world-note
- Commit policy / 提交策略: download_to_tmp_log_checksum_only
- Handling strategy / 处理策略: Lightweight source evidence is represented by
  committed provenance, size, checksum, and derived metadata only; ignored tmp
  downloads are not committed as source content.
- Rights status / 权利状态: metadata_only_until_verified
- Review status / 复核状态: reviewed_metadata_only

## Field Map Evidence / 字段映射证据

### Route 001
- Field map ID / 字段映射 ID: field-map-000039
- Source level / 来源层级: database_design_field
- Source field or unit / 来源字段或单位: 馆藏号
- Source meaning / 来源含义: National Library of China holding number such as 北图
  19780
- Target record type / 目标记录类型: oracle_inscription;
  excavation_or_collection_context
- Target project field / 目标字段: nlc_holding_number; collection_item_ref
- Import action / 导入动作: Use as NLC-local object or inscription reference when
  item records become accessible
- Rights boundary / 权利边界: NLC holding number is a local collection identifier
  and must not replace project IDs
- Evidence download ID / 证据下载 ID: dl-nlc-oracle-database-design
- Review status / 复核状态: reviewed_metadata_only

### Route 002
- Field map ID / 字段映射 ID: field-map-000040
- Source level / 来源层级: database_design_field
- Source field or unit / 来源字段或单位: 来源号
- Source meaning / 来源含义: Original collector/source number or older collection
  reference
- Target record type / 目标记录类型: source_reference
- Target project field / 目标字段: source_collection_ref; old_catalog_ref
- Import action / 导入动作: Use to preserve NLC source-chain and older collection
  references
- Rights boundary / 权利边界: NLC source references need row-level citation before
  object-level claims
- Evidence download ID / 证据下载 ID: dl-nlc-oracle-database-design
- Review status / 复核状态: reviewed_metadata_only

### Route 003
- Field map ID / 字段映射 ID: field-map-000041
- Source level / 来源层级: database_design_field
- Source field or unit / 来源字段或单位: 贞人;时期;出土地点;原骨属性;卜辞内容类别
- Source meaning / 来源含义: NLC database design fields for dating context and
  topical classification
- Target record type / 目标记录类型: oracle_inscription
- Target project field / 目标字段: diviner; period; excavation_place;
  bone_material_type; topic_category
- Import action / 导入动作: Use as target field contract for future NLC
  inscription-context import
- Rights boundary / 权利边界: Field design evidence is not a downloaded item-level
  record set
- Evidence download ID / 证据下载 ID: dl-nlc-oracle-database-design
- Review status / 复核状态: reviewed_metadata_only

### Route 004
- Field map ID / 字段映射 ID: field-map-000042
- Source level / 来源层级: database_design_field
- Source field or unit / 来源字段或单位: 著录情况
- Source meaning / 来源含义: NLC bibliographic/catalog references including Heji and
  Yinqi Cuibian
- Target record type / 目标记录类型: source_reference
- Target project field / 目标字段: publication_refs; heji_ref_id;
  yinqi_cuibian_ref_id
- Import action / 导入动作: Use to cross-check NLC records against published catalog
  references before promotion
- Rights boundary / 权利边界: Catalog references must be checked against original
  rows before use as evidence
- Evidence download ID / 证据下载 ID: dl-nlc-oracle-database-design
- Review status / 复核状态: reviewed_metadata_only

## Metadata Profile Evidence / 元数据概况证据

### Route 001
- Profile ID / 概况 ID: metadata-profile-000024
- Evidence download ID / 证据下载 ID: dl-nlc-oracle-world-note
- Metadata file / 元数据文件: P020200710368724856153.pdf
- Profile metric / 概况指标: oracle_world_object_record_count
- Profile value / 概况值: 2964
- Profile unit / 概况单位: object_records
- Import relevance / 导入相关性: Confirms NLC Oracle World database scope for
  oracle-bone object records from official NLC note
- Caution / 提醒: Database scale note is not a full item-level export
- Review status / 复核状态: reviewed_metadata_only

### Route 002
- Profile ID / 概况 ID: metadata-profile-000025
- Evidence download ID / 证据下载 ID: dl-nlc-oracle-world-note
- Metadata file / 元数据文件: P020200710368724856153.pdf
- Profile metric / 概况指标: oracle_world_object_image_count
- Profile value / 概况值: 5932
- Profile unit / 概况单位: images
- Import relevance / 导入相关性: Confirms NLC Oracle World object-image scale from
  official NLC note
- Caution / 提醒: Do not download or redistribute images before rights and
  endpoint review
- Review status / 复核状态: reviewed_metadata_only

### Route 003
- Profile ID / 概况 ID: metadata-profile-000026
- Evidence download ID / 证据下载 ID: dl-nlc-oracle-world-note
- Metadata file / 元数据文件: P020200710368724856153.pdf
- Profile metric / 概况指标: oracle_world_rubbing_record_count
- Profile value / 概况值: 2975
- Profile unit / 概况单位: rubbing_records
- Import relevance / 导入相关性: Confirms NLC Oracle World rubbing-record scale from
  official NLC note
- Caution / 提醒: Rubbing records still require stable query endpoint before
  import
- Review status / 复核状态: reviewed_metadata_only

### Route 004
- Profile ID / 概况 ID: metadata-profile-000027
- Evidence download ID / 证据下载 ID: dl-nlc-oracle-world-note
- Metadata file / 元数据文件: P020200710368724856153.pdf
- Profile metric / 概况指标: oracle_world_rubbing_image_count
- Profile value / 概况值: 3177
- Profile unit / 概况单位: rubbing_images
- Import relevance / 导入相关性: Confirms NLC Oracle World rubbing-image scale from
  official NLC note
- Caution / 提醒: Do not download or redistribute images before rights and
  endpoint review
- Review status / 复核状态: reviewed_metadata_only

### Route 005
- Profile ID / 概况 ID: metadata-profile-000028
- Evidence download ID / 证据下载 ID: dl-nlc-oracle-database-design
- Metadata file / 元数据文件: P020101227555561563898.pdf
- Profile metric / 概况指标: nlc_oracle_bone_holding_count
- Profile value / 概况值: 35651
- Profile unit / 概况单位: oracle_bones
- Import relevance / 导入相关性: Confirms National Library of China collection-scale
  evidence from official NLC database-design article
- Caution / 提醒: Collection-scale statement is not an item-level record import
- Review status / 复核状态: reviewed_metadata_only

### Route 006
- Profile ID / 概况 ID: metadata-profile-000029
- Evidence download ID / 证据下载 ID: dl-nlc-oracle-database-design
- Metadata file / 元数据文件: P020101227555561563898.pdf
- Profile metric / 概况指标: nlc_heji_cataloged_count
- Profile value / 概况值: 8000+
- Profile unit / 概况单位: heji_refs
- Import relevance / 导入相关性: Records official NLC statement that more than 8000
  holdings were cataloged in Jiaguwen Heji
- Caution / 提醒: Use as collection-level import target only until row-level
  records are available
- Review status / 复核状态: reviewed_metadata_only

### Route 007
- Profile ID / 概况 ID: metadata-profile-000030
- Evidence download ID / 证据下载 ID: dl-nlc-oracle-database-design
- Metadata file / 元数据文件: P020101227555561563898.pdf
- Profile metric / 概况指标: nlc_yinqi_cuibian_cataloged_count
- Profile value / 概况值: 1595
- Profile unit / 概况单位: yinqi_cuibian_refs
- Import relevance / 导入相关性: Records official NLC statement that 1595 holdings
  were cataloged in Yinqi Cuibian
- Caution / 提醒: Use as collection-level cross-reference evidence only
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
- Risk note / 风险提示: Official NLC materials confirm collection/database scope but
  not a stable current bulk endpoint; do not use mirrored summaries or
  third-party portals as source data.
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
