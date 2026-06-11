# Corpus Import Tools / 语料导入工具

English:
Future import scripts will convert repository source files into PostgreSQL or other query stores.

`download_source_manifest.py` downloads approved lightweight source pages into ignored `tmp/source_downloads/` and writes only the provenance log, size, checksum, and status into `project_registry/006_large-source-register/002_source-download-log.csv`.

Use `--download-id <id>` to download only selected manifest rows and merge those rows into the existing log without refreshing unrelated source timestamps.

`build_evobc_evolution_staging.py` reads the logged EVOBC `Key&Value.json` and `List_of_EVOBC.json` files from ignored `tmp/source_downloads/`, then writes reviewed metadata-only staging indexes under `corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/`.

`build_ihp_museum_object_staging.py` reads the logged IHP Museum Oracle Bones collection page from ignored `tmp/source_downloads/`, then writes object-level metadata staging records under `corpus/005_excavation-sites-periods-and-batches/000_collection-registers/`.

`build_hust_obc_validation_label_crosswalk.py` reads the logged HUST-OBC validation-class staging file and `ID_to_Chinese.json`, then writes OCR-label candidate crosswalk records under `corpus/001_oracle-characters/000_character-registers/`.

`build_hust_obc_source_category_staging.py` expands HUST-OBC validation classes into source-category rows so the contiguous `0001..1781` category range can be reviewed before any formal project character import.

`build_hust_obc_obs_char_promotion_queue.py` creates the reserved-only HUST-OBC promotion review queue with suggested `obs-char-*` IDs. The output is a review queue, not a formal character assignment.

`build_hust_obc_promotion_bucket_manifests.py` partitions that promotion queue into 100-ID bucket manifests under `corpus/001_oracle-characters/` and writes `010_hust-obc-promotion-bucket-review-summary.csv` so reviewers and AI Agents can process the 1,588 candidates in smaller batches.

`build_hust_obc_first_bucket_candidate_packets.py` materializes the first 100 HUST-OBC promotion candidates into bucket-level `01_candidate-character-packet.json` files plus a manifest, while preserving the not-accepted, cross-source-review boundary.

`build_hust_obc_candidate_packets.py` materializes all 1,588 HUST-OBC promotion candidates across the 16 bucket directories, writing one candidate packet per suggested `obs-char-*` path and one packet manifest per bucket.

`build_hust_obimd_evobc_codepoint_crosswalk.py` builds a metadata-only codepoint crosswalk from the 1,588 HUST-OBC promotion candidates to OBIMD main-character rows and EVOBC evolution-category rows. The output is a lookup route table only, not an identity claim or decipherment result.

`build_hust_obc_undeciphered_candidate_index.py` reads the HUST-OBC raw figshare zip from local temporary or external archive storage, then writes a metadata-only `obs-unk-*` undeciphered candidate index plus configured 100-row candidate packet buckets. It currently materializes `obs-unk-000001..obs-unk-006800`. It records source image paths and counts only; raw image files stay outside regular Git.

简体中文：
未来导入脚本会把仓库源文件转换到 PostgreSQL 或其他查询存储中。

`download_source_manifest.py` 会把批准的轻量来源页面下载到已忽略的 `tmp/source_downloads/`，并只把出处日志、大小、校验和和状态写入 `project_registry/006_large-source-register/002_source-download-log.csv`。

使用 `--download-id <id>` 可以只下载指定 manifest 行，并把这些行合并进现有日志，避免刷新无关来源的时间戳。

`build_evobc_evolution_staging.py` 会读取已登记的 EVOBC `Key&Value.json` 和 `List_of_EVOBC.json` 临时下载文件，并在 `corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/` 下写出仅含 metadata 的复核暂存索引。

`build_ihp_museum_object_staging.py` 会读取已登记的 IHP Museum Oracle Bones 馆藏页临时下载文件，并在 `corpus/005_excavation-sites-periods-and-batches/000_collection-registers/` 下写出对象级 metadata 暂存记录。

`build_hust_obc_validation_label_crosswalk.py` 会读取已登记的 HUST-OBC validation-class 暂存表和 `ID_to_Chinese.json`，并在 `corpus/001_oracle-characters/000_character-registers/` 下写出 OCR label 候选交叉记录。

`build_hust_obc_source_category_staging.py` 会把 HUST-OBC validation class 展开为 source-category 行，使连续的 `0001..1781` 类别范围可以在正式本项目单字导入前先被复核。

`build_hust_obc_obs_char_promotion_queue.py` 会创建 HUST-OBC 提升复核队列，并给出保留建议性质的 `obs-char-*` ID。该输出只是复核队列，不是正式甲骨字分配。

`build_hust_obc_promotion_bucket_manifests.py` 会把该提升队列按 100 个 ID 一组切分到 `corpus/001_oracle-characters/` 下的 bucket manifest，并写出 `010_hust-obc-promotion-bucket-review-summary.csv`，方便复核者和 AI Agent 分批处理 1,588 个候选。

`build_hust_obc_first_bucket_candidate_packets.py` 会把前 100 个 HUST-OBC 提升候选落实为 bucket 下的 `01_candidate-character-packet.json` 文件和 manifest，同时保持“未接受、待跨来源复核”的边界。

`build_hust_obc_candidate_packets.py` 会把全部 1,588 个 HUST-OBC 提升候选落实到 16 个 bucket 目录中，为每个建议 `obs-char-*` 路径写出一个候选资料包，并为每个 bucket 写出一个 packet manifest。

`build_hust_obimd_evobc_codepoint_crosswalk.py` 会从 1,588 个 HUST-OBC 提升候选出发，按 metadata 中的 codepoint 序列对照 OBIMD main-character 行和 EVOBC evolution-category 行。输出只是一张检索路线表，不是同字确认或释读结果。

`build_hust_obc_undeciphered_candidate_index.py` 会从本地临时区或外部归档中的 HUST-OBC figshare 原始 zip 读取目录结构，写出 metadata-only 的 `obs-unk-*` 未释读候选索引，并按配置生成每 100 条一组的候选 packet bucket。目前已落实 `obs-unk-000001..obs-unk-006800`。它只记录来源图片路径和数量；原始图片文件保留在普通 Git 之外。
