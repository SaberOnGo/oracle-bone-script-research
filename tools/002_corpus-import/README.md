# Corpus Import Tools / 语料导入工具

English:
Future import scripts will convert repository source files into PostgreSQL or other query stores.

`download_source_manifest.py` downloads approved lightweight source pages into ignored `tmp/source_downloads/` and writes only the provenance log, size, checksum, and status into `project_registry/006_large-source-register/002_source-download-log.csv`.

`build_evobc_evolution_staging.py` reads the logged EVOBC `Key&Value.json` and `List_of_EVOBC.json` files from ignored `tmp/source_downloads/`, then writes reviewed metadata-only staging indexes under `corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/`.

简体中文：
未来导入脚本会把仓库源文件转换到 PostgreSQL 或其他查询存储中。

`download_source_manifest.py` 会把批准的轻量来源页面下载到已忽略的 `tmp/source_downloads/`，并只把出处日志、大小、校验和和状态写入 `project_registry/006_large-source-register/002_source-download-log.csv`。

`build_evobc_evolution_staging.py` 会读取已登记的 EVOBC `Key&Value.json` 和 `List_of_EVOBC.json` 临时下载文件，并在 `corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/` 下写出仅含 metadata 的复核暂存索引。
