# src-gbedobc Source Processing Status

## English
This card summarizes the current preprocessing stage for this source. It shows
what has evidence, what has only candidate routes, and what still needs human
review before formal research use.

## 简体中文
本卡片汇总该来源目前的预处理阶段。它说明哪些环节已有证据，哪些只是候选路线，哪些仍需人工复核后才能进入正式研究。

## Source / 来源
- Title / 标题: GBEDOBC graph-based evolutionary dataset
- Provider / 提供方: Qingju Jiao et al. / npj Heritage Science / GitHub
- Rights status / 权利状态: source_marked_risk_noted
- Risk note / 风险提示: Useful for graph/evolution research and reports 756
  groups/3780 graph-based characters, but not a primary corpus authority.

## Phase Status / 阶段状态

### discovered
- Status / 状态: registered_source_row_present
- Evidence file / 证据文件: 001_all-sources-index.csv
- Evidence count / 证据数量: 1
- Review status / 复核状态: reviewed

### download_or_access
- Status / 状态: download_or_access_routes_present
- Evidence file / 证据文件: 02_download-route-index.csv
- Evidence count / 证据数量: 2
- Review status / 复核状态: metadata_route_needs_human_review

### checksum_and_size
- Status / 状态: partial_or_complete_checksum_size_evidence
- Evidence file / 证据文件: 02_download-route-index.csv
- Evidence count / 证据数量: not recorded
- Review status / 复核状态: needs_human_source_review

### package_manifest
- Status / 状态: package_manifest_routes_present
- Evidence file / 证据文件: 03_package-route-index.csv
- Evidence count / 证据数量: 2
- Review status / 复核状态: needs_human_source_review

### field_mapping
- Status / 状态: field_map_routes_present
- Evidence file / 证据文件: 04_field-map-route-index.csv
- Evidence count / 证据数量: 1
- Review status / 复核状态: candidate_mapping_needs_human_review

### metadata_profile
- Status / 状态: metadata_profile_rows_present
- Evidence file / 证据文件: 05_metadata-profile-route-index.csv
- Evidence count / 证据数量: 3
- Review status / 复核状态: needs_human_source_review

### cleaned_structured_linked
- Status / 状态: candidate_routes_available_not_final_import
- Evidence file / 证据文件: 08_source-processing-status.md
- Evidence count / 证据数量: 6
- Review status / 复核状态: pending_human_review

## Missing Or Review Items / 缺失或待复核项
- Items / 项目: none_recorded

## Concrete Questions To Check / 具体待查问题
- 应核对哪些下载、访问或 checksum 记录？
- 哪些来源包 manifest 行需要打开原始路径复核？
- 哪些字段映射可以安全进入语料对象？
- 哪些 metadata profile 行提示数据质量或 OCR 风险？
- 哪些权利状态或风险提示阻止公开提交原始资料？
- 哪些派生记录路径仍缺少人工复核结论？

## Human Next Step / 人工下一步
Open the route CSV files listed above, compare them with the source register and
download log, and record whether derived records can be safely created in the
relevant corpus objects.

请打开上述路线 CSV，与来源登记和下载日志比对，并记录能否在相应语料对象中安全生成派生记录。

## Human Research Relevance / 人类研究关联
Before formal research, use this status card to keep visible the possible glyph,
inscription, provenance, variant, component, bibliography, and dispute questions
attached to the source. A route status does not answer any of them.

正式研究前，应在本卡片中保留与来源相关的字形、卜辞、出处、异体、构件、书目和争议问题。路线状态本身不能回答这些问题。

- Form and component / 字形与构件: 若来源出现字形、构件或近形材料，须回到具体对象目录比较，暂不确认归属。
- Inscription and context / 卜辞与上下文: 须核对全文、OCR、图版、著录、出土、馆藏、时期和组类，暂不建立正式身份关系。
- Scholarship and dispute / 学术与争议: 须保留书目、提出者、释读史、不同意见和争议，暂不写成研究结论。

## Boundary / 边界
All statuses here are infrastructure statuses. They are not scholarly
conclusions and do not start formal decipherment work.

这里的所有状态都是资料工程状态，不是学术结论，也不开始正式释读研究。
