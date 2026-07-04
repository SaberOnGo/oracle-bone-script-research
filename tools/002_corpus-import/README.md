# Corpus Import Tools / 语料导入工具

English:
These tools turn reviewed source material into preparation records for human
research. Their purpose is not to make a database first, but to preserve source
routes, staging indexes, object-local materials, and review queues that a
researcher can inspect before any formal corpus import.

Simplified Chinese:
这些工具把已登记、可追溯的来源资料整理成正式研究前的预处理记录。它们
首先服务人类研究者核查来源、图像、著录和候选路线；数据库、JSON 或 CSV
只是辅助检索、追溯和统计的工具。

## Human Review Entry Order / 人工复核入口顺序

English:
Use this import area in the same order as a source review:

1. Check the source package, download log, checksum, rights note, and risk note.
2. Inspect the staging index before accepting any object or character route.
3. Follow crosswalk rows only as candidate source routes.
4. Build or inspect object-local materials inside the concrete object folder.
5. Record missing evidence as concrete next checks before corpus import.

Simplified Chinese:
使用本目录时，应按来源复核的顺序处理：

1. 先检查来源包、下载日志、checksum、权利说明和风险提示。
2. 在接受任何对象或单字路线前，先复核 staging index。
3. crosswalk 行只能作为候选来源路线使用。
4. 对象内资料必须生成或检查在具体对象目录内。
5. 正式导入前，缺失证据必须写成具体下一步待查问题。

## Source And Staging Scripts / 来源与暂存脚本

English:
These scripts prepare source evidence without making scholarly claims:

- `download_source_manifest.py`
- `build_lightweight_source_package_manifest.py`
- `build_registered_source_metadata_profiles.py`
- `build_evobc_evolution_staging.py`
- `build_ihp_museum_object_staging.py`
- `build_hust_obc_validation_label_crosswalk.py`
- `build_hust_obc_source_category_staging.py`
- `build_hust_obc_undeciphered_candidate_index.py`

Simplified Chinese:
这些脚本负责准备来源证据，但不提出学术结论：

- `download_source_manifest.py`
- `build_lightweight_source_package_manifest.py`
- `build_registered_source_metadata_profiles.py`
- `build_evobc_evolution_staging.py`
- `build_ihp_museum_object_staging.py`
- `build_hust_obc_validation_label_crosswalk.py`
- `build_hust_obc_source_category_staging.py`
- `build_hust_obc_undeciphered_candidate_index.py`

## Object-Local Materials / 对象内资料

English:
These scripts make object-local materials for human review. They keep README
pages, visual routes, source indexes, human review sheets, and AI support
packets in the same concrete `corpus` object directory:

- `build_character_local_materials.py`
- `build_character_human_research_dossiers.py`
- `build_character_context_evidence_dossiers.py`
- `build_character_archaeology_paleography_reviews.py`
- `extract_hust_obc_local_glyph_images.py`
- `build_hust_obc_undeciphered_local_materials.py`
- `build_obimd_component_candidate_materials.py`
- `build_cambridge_hopkins_inscription_crosswalk_materials.py`
- `build_cambridge_hopkins_topic_materials.py`
- `build_evobc_evolution_candidate_materials.py`
- `build_collection_object_candidate_materials.py`
- `build_source_object_materials.py`

Simplified Chinese:
这些脚本生成对象内人类复核资料。README、图像路线、来源索引、人工复核表
和 AI 辅助 packet 必须放在同一个具体 `corpus` 对象目录内：

- `build_character_local_materials.py`
- `build_character_human_research_dossiers.py`
- `build_character_context_evidence_dossiers.py`
- `extract_hust_obc_local_glyph_images.py`
- `build_hust_obc_undeciphered_local_materials.py`
- `build_obimd_component_candidate_materials.py`
- `build_cambridge_hopkins_inscription_crosswalk_materials.py`
- `build_cambridge_hopkins_topic_materials.py`
- `build_evobc_evolution_candidate_materials.py`
- `build_collection_object_candidate_materials.py`
- `build_source_object_materials.py`

## Cross-Source Routes / 跨来源路线

English:
These scripts create lookup or review routes across sources. A route may help a
researcher find evidence, but it is not an identity claim:

- `build_hust_obc_obs_char_promotion_queue.py`
- `build_hust_obc_promotion_bucket_manifests.py`
- `build_hust_obc_first_bucket_candidate_packets.py`
- `build_hust_obc_candidate_packets.py`
- `build_hust_obimd_evobc_codepoint_crosswalk.py`
- `sync_asset_id_source_map_from_asset_index.py`

Simplified Chinese:
这些脚本建立跨来源检索或复核路线。路线可以帮助研究者找到证据，但不是
对象同一性、同字关系或释读结论：

- `build_hust_obc_obs_char_promotion_queue.py`
- `build_hust_obc_promotion_bucket_manifests.py`
- `build_hust_obc_first_bucket_candidate_packets.py`
- `build_hust_obc_candidate_packets.py`
- `build_hust_obimd_evobc_codepoint_crosswalk.py`
- `sync_asset_id_source_map_from_asset_index.py`

## Concrete Questions To Check / 具体待查问题

English:
Before running or accepting an import result, answer these questions:

- Which source package or public page produced the source record?
- Where are the access log, manifest, checksum, size, and rights status?
- Which staging index shows the raw row before local object material exists?
- Which concrete object folder contains the human-readable review material?
- Which fields are still candidates, missing, disputed, or pending review?
- Does any output look like a conclusion before source review is complete?

Simplified Chinese:
运行或接受导入结果前，应回答这些具体问题：

- 该来源记录来自哪个来源包或公开网页？
- 访问日志、manifest、checksum、大小和权利状态在哪里？
- 哪个 staging index 显示了对象内资料生成前的原始行？
- 哪个具体对象目录包含人类可读复核资料？
- 哪些字段仍是候选、缺失、争议或待复核？
- 是否有输出在来源复核完成前看起来像结论？

## Research Boundary / 研究边界

English:
Import outputs are preparation evidence only.
This is not a decipherment conclusion.
It is not a confirmed character assignment, inscription identity claim, or
accepted paleographic correspondence. Large raw packages stay in ignored local
or external archives unless the large-source policy allows a reviewed
derivative to be committed.

Simplified Chinese:
导入输出只是预处理证据，不是释读结论，不是已确认的单字分配，不是卜辞或
馆藏对象同一性结论，也不是已接受的古文字对应。大型原始包应留在已忽略的
本地或外部归档中；只有符合大型来源规则的已复核派生结果才能提交。

## Validation / 校验

English:
After changing these workflows, run the repository skeleton validator, unit
tests, and diff whitespace check. If a new workflow creates temporary or
generated files, update `.gitignore`, validation, and tests in the same change.

Simplified Chinese:
修改这些流程后，需要运行仓库 skeleton validator、单元测试和 diff 空白检查。
如果新增流程会产生临时或生成文件，必须在同一次修改中更新 `.gitignore`、
validation 和 tests。
