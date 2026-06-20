# Lightweight Source Package Manifest / 轻量来源包清单

English:
`build_lightweight_source_package_manifest.py` records package-manifest rows for lightweight downloaded source pages, API JSON files, PDFs, and access-restricted page captures when a registered source does not yet have source-package manifest rows.

The script reads only committed source registers and download logs. It does not open ignored `tmp/` downloads, does not redownload sources, does not clear rights, does not import corpus records, and does not make inscription, character, component, correspondence, reading, or decipherment claims.

Simplified Chinese:
`build_lightweight_source_package_manifest.py` 用于给尚无来源包清单行的轻量来源下载页、API JSON、PDF 和访问受限页面记录补充 package manifest。

该脚本只读取已提交的来源登记表和下载日志；不会打开被忽略的 `tmp/` 下载文件，不会重新下载来源，不会完成权利清理，不会导入语料记录，也不会提出卜辞、单字、构件、对应、释读或破译结论。

## Inputs / 输入

- `corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv`
- `project_registry/006_large-source-register/002_source-download-log.csv`
- `corpus/006_research-sources-and-bibliography/000_source-registers/009_source-package-file-manifest.csv`

## Output / 输出

- `corpus/006_research-sources-and-bibliography/000_source-registers/009_source-package-file-manifest.csv`

## Command / 命令

```powershell
python tools/002_corpus-import/build_lightweight_source_package_manifest.py
```
