# Corpus Import Tools / 语料导入工具

English:
Future import scripts will convert repository source files into PostgreSQL or other query stores.

`download_source_manifest.py` downloads approved lightweight source pages into ignored `tmp/source_downloads/` and writes only the provenance log, size, checksum, and status into `project_registry/006_large-source-register/002_source-download-log.csv`.

Use `--download-id <id>` to download only selected manifest rows and merge those rows into the existing log without refreshing unrelated source timestamps.

`build_evobc_evolution_staging.py` reads the logged EVOBC `Key&Value.json` and `List_of_EVOBC.json` files from ignored `tmp/source_downloads/`, then writes reviewed metadata-only staging indexes under `corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/`.

`build_ihp_museum_object_staging.py` reads the logged IHP Museum Oracle Bones collection page from ignored `tmp/source_downloads/`, then writes object-level metadata staging records under `corpus/005_excavation-sites-periods-and-batches/000_collection-registers/`.

`build_hust_obc_validation_label_crosswalk.py` reads the logged HUST-OBC validation-class staging file and `ID_to_Chinese.json`, then writes OCR-label candidate crosswalk records under `corpus/001_oracle-characters/000_character-registers/`.

简体中文：
未来导入脚本会把仓库源文件转换到 PostgreSQL 或其他查询存储中。

`download_source_manifest.py` 会把批准的轻量来源页面下载到已忽略的 `tmp/source_downloads/`，并只把出处日志、大小、校验和和状态写入 `project_registry/006_large-source-register/002_source-download-log.csv`。

使用 `--download-id <id>` 可以只下载指定 manifest 行，并把这些行合并进现有日志，避免刷新无关来源的时间戳。

`build_evobc_evolution_staging.py` 会读取已登记的 EVOBC `Key&Value.json` 和 `List_of_EVOBC.json` 临时下载文件，并在 `corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/` 下写出仅含 metadata 的复核暂存索引。

`build_ihp_museum_object_staging.py` 会读取已登记的 IHP Museum Oracle Bones 馆藏页临时下载文件，并在 `corpus/005_excavation-sites-periods-and-batches/000_collection-registers/` 下写出对象级 metadata 暂存记录。

`build_hust_obc_validation_label_crosswalk.py` 会读取已登记的 HUST-OBC validation-class 暂存表和 `ID_to_Chinese.json`，并在 `corpus/001_oracle-characters/000_character-registers/` 下写出 OCR label 候选交叉记录。
