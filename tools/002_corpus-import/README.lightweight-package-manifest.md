# Lightweight Source Package Manifest / 轻量来源包清单

## Purpose / 用途

English:

`build_lightweight_source_package_manifest.py` prepares package-manifest rows
for small pages, API JSON files, PDFs, and restricted-page captures when a
registered source has a successfully downloaded payload but no manifest row.

简体中文：

`build_lightweight_source_package_manifest.py` 为已有成功下载载荷、但尚无
清单行的轻量来源准备 package manifest。适用对象包括网页、API JSON、PDF
和受限页面截取记录。

The script must not create a file row for an HTTP error, TLS failure, timeout,
or another attempt that produced no payload and checksum.

脚本不得为 HTTP 错误、TLS 失败、超时或其他未产生载荷与校验和的访问尝试
创建文件行。

## Human Review Entry Order / 人工复核顺序

English:

1. Open the source-register row for the source object.
2. Open the matching download-log row and confirm the access route.
3. Check status, checksum, size, rights status, risk note, and review status.
4. Compare each manifest row with its registered source-package ID.
5. Follow each derived path before trusting any corpus or graph route.
6. Write missing facts as concrete next questions.

简体中文：

1. 先打开来源对象对应的 source register 行。
2. 打开匹配的 download log 行，确认访问路线。
3. 核对状态、checksum、大小、权利状态、风险提示和复核状态。
4. 将每条 manifest 行与登记的 source-package ID 对照。
5. 信任任何语料或图谱路线前，先追踪每条派生路径。
6. 将缺失事实写成具体的下一步待查问题。

## Inputs And Output / 输入与输出

English:

- Input: registered source-object rows in the all-sources index.
- Input: successful download-log rows with payload and checksum evidence.
- Input: existing package-manifest rows, used to avoid duplicates.
- Output: updated lightweight manifest rows in the source-register area.

简体中文：

- 输入：all-sources index 中已登记的来源对象行。
- 输入：带载荷和 checksum 证据的成功 download log 行。
- 输入：已有 package manifest 行，用于避免重复。
- 输出：来源登记区内更新后的轻量 manifest 行。

## Concrete Questions To Check / 具体待查问题

- Which source object and package does the row support?
- 该行支持哪个来源对象和来源包？
- Which download-log row proves that a payload was obtained?
- 哪条 download log 行证明实际取得了载荷？
- Does the checksum match the file name and file size?
- checksum 是否对应正确的文件名和文件大小？
- Which rights status and risk note limit repository use?
- 哪些权利状态和风险提示限制仓库使用？
- Which derived path lets a human inspect the extracted record?
- 哪条派生路径可供人工检查抽取记录？

## Research Boundary / 研究边界

English:

The script reads committed provenance logs only. It does not open ignored
downloads, redownload sources, clear rights, import corpus records, or make
inscription, character, component, correspondence, reading, or decipherment
claims.

This is not a decipherment conclusion.

简体中文：

脚本只读取已提交的来源追溯日志。它不打开忽略区下载物，不重新下载来源，
不完成权利清理，不导入语料记录，也不提出卜辞、单字、构件、对应、释读或
破译结论。

这不是释读结论。

## Command / 命令

```powershell
python tools/002_corpus-import/build_lightweight_source_package_manifest.py
```
