# src-obimd Material Access Index

## English
This object-local index tells a human reviewer what source materials are visible
here and which structured support files carry the route data. It is an access
map, not a rights decision.

## 简体中文
本索引说明同一来源对象目录中有哪些资料入口，以及哪些结构化辅助文件保存结构化路线。它只是访问地图，不是权利结论或学术结论。

## Human-Readable Entrances / 人类可读入口
- Source summary / 来源摘要: README.md
- Human review sheet / 人工复核单: 06_human-source-review-sheet.md
- Material access index / 资料访问索引: 07_material-access-index.md
- Processing status card / 处理状态卡: 08_source-processing-status.md

## Structured Support Entrances / 结构化辅助入口
- Structured source packet / 结构化来源包: 01_source-packet.json
- Download route table / 下载路线表: 02_download-route-index.csv
- Package route table / 来源包路线表: 03_package-route-index.csv
- Field-map route table / 字段映射表: 04_field-map-route-index.csv
- Metadata profile table / 元数据概况表: 05_metadata-profile-route-index.csv
- Processing status JSON / 处理状态索引: 09_source-processing-status-index.json

Structured support files only serve the human source dossier. They must not
replace the source summary, review sheet, evidence dossier, fact matrix, rights
note, or concrete next-check questions.

结构化辅助文件只服务人类来源档案，不得替代来源摘要、复核单、证据档案、事实矩阵、权利说明或具体待查问题。

## Route Signals / 路线信号
- Download route count / 下载路线数: 7
- Download statuses / 下载状态: downloaded; downloaded_to_external_archive
- Package route count / 来源包路线数: 7
- Package kinds / 来源包类型: hierarchical_metadata_json; hierarchical_metadata_xlsx;
  raw_annotation_json; raw_image_zip
- Field map count / 字段映射数: 9
- Target records / 目标记录: asset_metadata; oracle_character;
  oracle_character_occurrence; oracle_character_variant; oracle_inscription
- Metadata profile count / 元数据概况数: 5
- Profile metrics / 概况指标: empty_codepoint_count; main_character_uid_count;
  row_count; transcription_empty_count

## Next Review Step / 下一步复核入口
- Rights status / 权利状态: licensed_for_repository
- Review status / 复核状态: reviewed
- Risk note / 风险提示: Dataset card reports CC-BY 4.0 while the GitHub README
  includes narrower academic-use wording; raw files remain large and need rights
  review before import.

Inspect the route rows above, then decide whether source-safe visual or text
derivatives can be added inside the relevant concrete corpus object directories.

请先复核上述路线，再判断能否把安全的图像或文本派生记录放入对应的具体语料对象目录。

## Boundary / 边界
This index does not collect new evidence, clear rights, promote a source, import
corpus records, confirm a character identity, assign a component, identify an
inscription, confirm an evolution chain, or make a decipherment conclusion.

本索引不采集新证据，不完成权利清理，不提升来源等级，不导入正式语料，不确认字形身份，不指定构件，不确认卜辞身份，不确认演化链，也不作释读结论。
