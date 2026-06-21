# Lightweight Source Package Manifest / 轻量来源包清单

English:
`build_lightweight_source_package_manifest.py` prepares source-package
manifest rows for lightweight pages, API JSON files, PDFs, and restricted
page captures when a registered source lacks manifest coverage.

Simplified Chinese:
`build_lightweight_source_package_manifest.py` 为缺少 manifest 覆盖的轻量
来源页、API JSON、PDF 和受限页面截取记录准备来源包清单行。

## Human Review Entry Order / 人工复核入口顺序

English:

1. Open the source register row for the source object first.
2. Open the matching download log row and confirm the access route.
3. Check checksum, file size, rights status, risk note, and review status.
4. Compare each manifest row with the registered source package id.
5. Follow each derived path before trusting any corpus or graph route.
6. Record missing access, size, checksum, or permission facts as next checks.

Simplified Chinese:

1. 先打开来源对象对应的 source register 行。
2. 打开匹配的 download log 行，确认访问路线。
3. 核对 checksum、file size、rights status、risk note 和复核状态。
4. 将每条 manifest row 与登记的 source package id 对照。
5. 信任任何 corpus 或图谱路线前，先追踪每条 derived path。
6. 缺失访问、大小、checksum 或许可事实时，写成下一步待查问题。

## Inputs And Output / 输入与输出

English:

- Input: all-sources index rows for registered source objects.
- Input: source download log rows with access and checksum evidence.
- Input: existing source-package manifest rows to avoid duplicates.
- Output: updated lightweight manifest rows in the source register area.

Simplified Chinese:

- 输入：已登记来源对象的 all-sources index 行。
- 输入：带访问和 checksum 证据的 source download log 行。
- 输入：既有来源包 manifest 行，用于避免重复。
- 输出：source register 区中更新后的轻量 manifest 行。

## Concrete Questions To Check / 具体待查问题

English:

- Which source object and source package does this manifest row support?
- Which download log row proves access or download status?
- Is the checksum tied to the correct file name and file size?
- What rights status and risk note limit public repository use?
- Which derived path lets a human reviewer inspect the extracted record?
- Which missing manifest row, field map, or permission still needs review?

Simplified Chinese:

- 这条 manifest row 支持哪个来源对象和 source package？
- 哪条 download log 行证明访问或下载状态？
- checksum 是否对应正确的文件名和 file size？
- rights status 和 risk note 如何限制公开仓库使用？
- 哪条 derived path 能让人工复核者检查抽取记录？
- 还缺哪条 manifest row、字段映射或许可复核？

## Research Boundary / 研究边界

English:
The script reads committed provenance logs only. It does not open ignored
downloads, redownload sources, clear rights, import corpus records, or make
inscription, character, component, correspondence, reading, or decipherment
claims. It is not a decipherment conclusion.

Simplified Chinese:
该脚本只读取已提交的出处日志。它不会打开被忽略的下载文件，不会重新下载
来源，不会完成权利清理，不会导入语料记录，也不会提出卜辞、单字、构件、
对应、释读或破译结论。它不是释读结论。

## Command / 命令

```powershell
python tools/002_corpus-import/build_lightweight_source_package_manifest.py
```
