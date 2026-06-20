# src-hust-obc Material Access Index / src-hust-obc 资料访问索引

English:
This object-local index tells a human reviewer what source materials are currently visible in this same source directory and which AI-readable files carry the structured routes. It is a preparation-stage access map, not a rights decision or research conclusion.

简体中文：
本对象内索引说明人工复核者在同一个来源目录里可以看到哪些资料入口，以及哪些 AI 可读文件保存了结构化路线。它只是准备阶段的访问地图，不是权利结论，也不是学术结论。

## Human-Readable Entrances / 人类可读入口

| Material area | Local file | Current status | Count or signal |
| --- | --- | --- | --- |
| Source summary / 来源摘要 | `README.md` | present | source ID `src-hust-obc` |
| Human review sheet / 人工复核表 | `06_human-source-review-sheet.md` | present | source provenance and rights checklist |
| Download or access routes / 下载或访问路线 | `02_download-route-index.csv` | route_rows_present | 7 route row(s); statuses: downloaded |
| Package or file manifest routes / 来源包或文件清单路线 | `03_package-route-index.csv` | route_rows_present | 4 route row(s); kinds: mapping_json;raw_dataset_zip |
| Field maps / 字段映射 | `04_field-map-route-index.csv` | field_rows_present | 7 row(s); target records: asset_metadata;oracle_character |
| Downloaded metadata profiles / 已下载 metadata profile | `05_metadata-profile-route-index.csv` | profile_rows_present | 11 row(s); metrics: figshare_file_size_bytes;figshare_license;ocr_inverse_mapping_count;ocr_mapping_count;validation_label_count;validation_label_crosswalk_count;validation_label_multi_component_count;validation_label_single_component_count;validation_label_value_range;validation_source_category_count;validation_source_category_multi_member_count |

## AI-Readable Entrances / AI 可读入口

- Source packet / 来源 packet: `01_source-packet.json`
- Download route table / 下载路线表: `02_download-route-index.csv`
- Package route table / 来源包路线表: `03_package-route-index.csv`
- Field-map route table / 字段映射路线表: `04_field-map-route-index.csv`
- Metadata profile route table / metadata profile 路线表: `05_metadata-profile-route-index.csv`

## Next Review Step / 下一步复核入口

- Rights status / 权利状态: `source_marked_risk_noted`
- Review status / 复核状态: `reviewed`
- Risk note / 风险提示: Dataset is directly relevant to 1500+ deciphered and undeciphered characters, but raw images are large, non-commercially licensed and compiled from diverse sources including an unreliable GuoXueDaShi split.
- Recommended next action / 建议下一步: inspect the route rows above, then decide whether source-safe visual/text derivatives can be added inside the relevant concrete corpus object directories.

## Boundary / 边界

English:
This index does not collect new evidence, clear rights, promote a source, import corpus records, confirm a character identity, assign a component, identify an inscription, confirm an evolution chain, or make a decipherment conclusion.

简体中文：
本索引不采集新证据，不完成权利清理，不提升来源，不导入语料记录，不确认字形身份，不指定构件，不确认卜辞身份，不确认演化链，也不作释读结论。
