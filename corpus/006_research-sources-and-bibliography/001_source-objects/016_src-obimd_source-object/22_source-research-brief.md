# Source Research Brief / 来源研究资料简报

This brief is the first human reading page for this registered source. It
reports only evidence already recorded in this object folder and names the
limits on research use.

本简报是该已登记来源的首个供人阅读页面。它只陈述本对象目录已经记录的证据，并明确该资料可用于研究的范围和限制。

## Source Identity And Scope / 来源身份与范围
- Title / 标题: OBIMD: Oracle Bone Inscriptions Multi-modal Dataset
- Provider / 提供方: Key Laboratory of Oracle Bone Inscriptions Information
  Processing Anyang Normal University; Xiamen University; Tencent Youtu Lab;
  University of Cambridge; Scientific Data
- Evidence level / 证据等级: peer_reviewed_dataset
- Registered scope / 已登记范围: Multi-modal OBI dataset with 10077 oracle bone
  images, 93652 annotated characters, 21941 syntactically validated sentences,
  and reading sequences.
- Source page / 来源页面: https://www.nature.com/articles/s41597-026-06967-0

## Actual Registered Evidence / 已登记的实际证据
- Download or access records / 下载或访问记录: 10
- Recorded checksums / 已记录 checksum: 10
- Recorded file sizes / 已记录文件大小: 10
- Package files / 来源包文件: 7
- Field mappings / 字段映射: 9
- Metadata measurements / 元数据测量: 5

- Recorded access item / 已记录访问项: dl-obimd-hf-readme; downloaded; 3871 bytes
- Recorded access item / 已记录访问项: dl-obimd-github-readme; downloaded; 5543 bytes
- Recorded access item / 已记录访问项: dl-obimd-arxiv-abs; downloaded; 48860 bytes
- Recorded access item / 已记录访问项: dl-obimd-main-character-json; downloaded;
  451652 bytes
- Recorded access item / 已记录访问项: dl-obimd-subchar-glyph-mapping; downloaded;
  668208 bytes
- Recorded access item / 已记录访问项: dl-obimd-subchar-main-mapping; downloaded;
  71318 bytes
- Recorded access item / 已记录访问项: dl-obimd-subcharacter-images;
  downloaded_to_external_archive; 40436910 bytes
- Recorded access item / 已记录访问项: dl-obimd-data-json;
  downloaded_to_external_archive; 41732948 bytes
- Recorded access item / 已记录访问项: dl-obimd-facsimile;
  downloaded_to_external_archive; 210800641 bytes
- Recorded access item / 已记录访问项: dl-obimd-rubbing;
  downloaded_to_external_archive; 558367972 bytes

## Usable Material Routes / 可用资料路径
- Package material / 来源包资料: data.json; raw_annotation_json; Raw annotation JSON
  exceeds SIZE_LIMIT; keep outside regular Git and extract reviewed subsets only
- Package material / 来源包资料: facsimile.zip; raw_image_zip; Raw image package
  stays outside Git; ZIP integrity is verified with 10078 members; commit only
  metadata and reviewed derivatives
- Package material / 来源包资料: rubbing.zip; raw_image_zip; Raw image package stays
  outside Git; ZIP integrity is verified with 10078 members; commit only
  metadata and reviewed derivatives
- Package material / 来源包资料: Sub-character Images.zip; raw_image_zip; Above
  SIZE_LIMIT; raw zip is kept in ignored external archive and only object-local
  PNG derivatives with provenance are committed
- Package material / 来源包资料: Main-character.json; hierarchical_metadata_json; Use
  to build candidate main-character reference mappings
- Package material / 来源包资料: Sub-character to Glyph Code Point Mapping.xlsx;
  hierarchical_metadata_xlsx; Use to map sub-character UID to platform glyph
  code point
- Package material / 来源包资料: Sub-character to Main-character Mapping.xlsx;
  hierarchical_metadata_xlsx; Use to build candidate variant-to-main-character
  hierarchy
- Candidate transfer field / 候选转入字段: Facsimile -> asset_metadata -> asset_type;
  local_or_external_path
- Candidate transfer field / 候选转入字段: Rubbing -> asset_metadata -> asset_type;
  local_or_external_path
- Candidate transfer field / 候选转入字段: RubbingName -> oracle_inscription ->
  primary_external_ref_id
- Candidate transfer field / 候选转入字段: GroupCategory -> oracle_inscription ->
  group_category; inscription_context_group
- Candidate transfer field / 候选转入字段: Position -> asset_metadata ->
  bounding_box_xywh
- Candidate transfer field / 候选转入字段: OrderNumber -> oracle_character_occurrence
  -> reading_order_index
- Candidate transfer field / 候选转入字段: Label -> oracle_character ->
  primary_external_ref_id; source_label
- Candidate transfer field / 候选转入字段: SubLabel -> oracle_character_variant ->
  variant_external_ref_id; parent_character_ref
- Candidate transfer field / 候选转入字段: SeatFont; Mark ->
  oracle_character_occurrence -> missing_or_special_marker

## Research-Use Limits / 研究使用限制
- Legacy rights status / 历史权利状态: licensed_for_repository
- Effective rights status / 当前有效权利状态:
  metadata_only_until_verified
- Active override / 生效覆盖:
  `project_registry/004_asset-source-and-rights-index/`
  `006_obimd-rights-status-override.csv`
- Public decision / 公开决定:
  metadata_only_no_public_redistribution_until_reconciled
- Read the full decision / 完整决定:
  `25_effective-rights-decision.md`
- Risk note / 风险提示: The dataset card says CC-BY 4.0, the GitHub README
  narrows use to academic research, and the article records CC BY-NC-ND with
  possible third-party terms.
- Adoption status / 采用状态: candidate_large_source
Open 10_source-evidence-dossier.md for full checksums, package rows, field-map
details, and source-specific pending questions.

需要完整 checksum、来源包条目、字段映射和具体待查问题时，请打开 10_source-evidence-dossier.md。

## Current Pipeline Gap / 当前流水线缺口
The repository currently records 10,364 committed source-marked assets,
38,387,085 committed asset bytes, 2,770 object-local material bundles,
2,719 object-local review-image objects, and 57,603 graph edges. These are
preprocessing routes and candidate records; the OBIMD source has not been
promoted into accepted scholarship.

当前仓库记录 10,364 个带来源标记的已提交资产、38,387,085 字节资产、2,770 个
对象内资料包、2,719 个对象内复核图像对象和 57,603 条图边。这些只是预处理路线
和候选记录；OBIMD 尚未提升为已接受的学术资料。

The raw data.json, facsimile.zip, and rubbing.zip packages remain in the
external archive. Before any source promotion, a reviewer must match selected
members to source UIDs, an extraction manifest, image/object dossiers, and
rights wording. The data rows and package members are not accepted identities,
readings, components, inscriptions, periods, or decipherment claims.

原始 data.json、facsimile.zip 和 rubbing.zip 仍在外部归档。提升来源前，复核者
必须把选定成员与来源 UID、抽取 manifest、图像或对象档案及权利措辞逐项匹配。
数据行和来源包成员不是已确认身份、释读、构件、卜辞、时期或破译结论。

Concrete human checks / 具体人工核查：

- Which image, bounding box, order number, and sentence support each edge?
- How do the CC-BY statement and narrower README wording reconcile?
- Which source catalog or plate route confirms a database row?
- Does `data.json` remain a source-record package rather than an accepted
  character identity, reading, component, or inscription claim?
- 每条关系边由哪幅图像、边界框、序号和卜辞支持？
- CC-BY 说明与 README 较窄的学术使用措辞如何互证？
- 哪条来源著录或图版路线能确认数据库行？
- `data.json` 是否仍只是来源记录包，而不是已确认的字形身份、释读、
  构件或卜辞结论？

Sub-character mappings remain candidate routes until image and context review.
子字映射在图像和语境复核前仍只是候选路线。

## Boundary / 边界
- not a rights decision
- not corpus import approval
- not a reading or component assignment
- not an inscription identity
- not a decipherment conclusion
- 不是权利结论、语料导入批准、释读、构件归属、卜辞身份或破译结论
