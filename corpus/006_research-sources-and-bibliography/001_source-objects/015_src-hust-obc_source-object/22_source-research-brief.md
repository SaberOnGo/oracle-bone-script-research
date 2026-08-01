# Source Research Brief / 来源研究资料简报

This brief is the first human reading page for this registered source. It
reports only evidence already recorded in this object folder and names the
limits on research use.

本简报是该已登记来源的首个供人阅读页面。它只陈述本对象目录已经记录的证据，并明确该资料可用于研究的范围和限制。

## Source Identity And Scope / 来源身份与范围
- Title / 标题: HUST-OBC: An open dataset for oracle bone character recognition
  and decipherment
- Provider / 提供方: Huazhong University of Science and Technology research team /
  Scientific Data
- Evidence level / 证据等级: peer_reviewed_dataset
- Registered scope / 已登记范围: Scientific Data dataset with 77064 images of 1588
  deciphered characters and 62989 images of 9411 undeciphered characters; total
  140053 images.
- Source page / 来源页面: https://www.nature.com/articles/s41597-024-03807-x

## Actual Registered Evidence / 已登记的实际证据
- Download or access records / 下载或访问记录: 7
- Recorded checksums / 已记录 checksum: 7
- Recorded file sizes / 已记录文件大小: 7
- Package files / 来源包文件: 4
- Field mappings / 字段映射: 7
- Metadata measurements / 元数据测量: 11

- Recorded access item / 已记录访问项: dl-hust-obc-nature; downloaded; 306156 bytes
- Recorded access item / 已记录访问项: dl-hust-obc-nature-pdf; downloaded; 3016746
  bytes
- Recorded access item / 已记录访问项: dl-hust-obc-github-readme; downloaded; 7908
  bytes
- Recorded access item / 已记录访问项: dl-hust-obc-figshare-api; downloaded; 4180
  bytes
- Recorded access item / 已记录访问项: dl-hust-obc-ocr-chinese-to-id; downloaded;
  1483277 bytes
- Recorded access item / 已记录访问项: dl-hust-obc-ocr-id-to-chinese; downloaded;
  1483277 bytes
- Recorded access item / 已记录访问项: dl-hust-obc-validation-label; downloaded; 22087
  bytes

## Usable Material Routes / 可用资料路径
- Package material / 来源包资料: HUST-OBC.zip; raw_dataset_zip; Keep raw package
  outside Git; extract class indexes and source-marked metadata only
- Package material / 来源包资料: Chinese_to_ID.json; mapping_json; Use as auxiliary
  OCR mapping after cross-checking with authoritative character sources
- Package material / 来源包资料: ID_to_Chinese.json; mapping_json; Use as auxiliary
  OCR mapping after cross-checking with authoritative character sources
- Package material / 来源包资料: Validation_label.json; mapping_json; Use to
  understand validation category mapping; not a final corpus identifier
- Candidate transfer field / 候选转入字段: deciphered -> oracle_character ->
  decipherment_status; character_image_class
- Candidate transfer field / 候选转入字段: undeciphered -> oracle_character ->
  decipherment_status; undeciphered_source_class
- Candidate transfer field / 候选转入字段: chinese_to_ID.json -> oracle_character ->
  modern_character; external_ref_id
- Candidate transfer field / 候选转入字段: ID_to_chinese.json -> oracle_character ->
  primary_external_ref_id; modern_character
- Candidate transfer field / 候选转入字段: X; L; G; Y; H -> asset_metadata ->
  source_catalog_refs; source_risk_note
- Candidate transfer field / 候选转入字段: Validation_label.json plus
  ID_to_Chinese.json -> oracle_character -> source_category_id;
  source_modern_label_candidate
- Candidate transfer field / 候选转入字段: expanded Validation_label.json
  source_category_id -> oracle_character -> source_category_id;
  source_modern_label_candidate; linked_candidate_class_id

## Current Pipeline Gap / 当前流水线缺口

- Committed assets: `10996`; committed bytes: `53009139`.
- 已提交资产：`10996`；已提交字节数：`53009139`。
- Object-local bundles/routes: `12585`; review-image objects: `10996`.
- 对象内资料包/路线：`12585`；复核图像对象：`10996`。
- Graph edges: `27291`; promotion-queue candidates: `1588`.
- 图边：`27291`；提升队列候选：`1588`。
- Direct visual observations currently cover `5427` of `10996` images.
- 当前直接视觉观察覆盖 `10996` 幅图像中的 `5427` 幅。
- Human review is still pending; source and image rights remain risk-marked.
- 人工复核仍待完成；来源和图像权利仍标为有风险。

Concrete human checks / 具体人工核查：

- Which remaining image can be opened and recorded next in its object folder?
- 下一张可打开并记录到对象目录的图像是哪一张？
- Which candidate image has a primary plate, catalog, or inscription route?
- 哪个候选图像已有原始图版、著录或卜辞路线？
- Which rights statement governs each derivative and source class?
- 每个派生件和来源类别适用哪条权利说明？

Modern labels and OCR mappings remain source routes, not confirmed readings.
现代标签和 OCR 映射仍是来源路线，不是已确认释读。

## Research-Use Limits / 研究使用限制
- Rights status / 权利状态: source_marked_risk_noted
- Risk note / 风险提示: Dataset is directly relevant to 1500+ deciphered and
  undeciphered characters, but raw images are large, non-commercially licensed
  and compiled from diverse sources including an unreliable GuoXueDaShi split.
- Adoption status / 采用状态: candidate_large_source
Open 10_source-evidence-dossier.md for full checksums, package rows, field-map
details, and source-specific pending questions.

需要完整 checksum、来源包条目、字段映射和具体待查问题时，请打开 10_source-evidence-dossier.md。

## Boundary / 边界
- not a rights decision
- not corpus import approval
- not a reading or component assignment
- not an inscription identity
- not a decipherment conclusion
- 不是权利结论、语料导入批准、释读、构件归属、卜辞身份或破译结论
