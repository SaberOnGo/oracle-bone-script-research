# Original PDF Capture Record
# 原始 PDF 捕获记录

Access date / 访问日期: `2026-08-28`

Capture root / 本地捕获根目录:
`.working/ihp-1222-plate-search-20260828/`

Rights status / 权利状态: `metadata_only_until_verified`

The official PDF and page snapshots remain in ignored local storage. The PDF
is below the repository size limit, but no reuse permission was found, so it
is not committed.

官方 PDF 与网页快照保留在已忽略的本地目录。PDF 虽低于仓库尺寸上限，
但未找到再利用许可，因此不提交。

## Official issue index capture / 官方期次索引捕获

- File: `ntu-journal-index-page6.html`
- Size: `88713` bytes
- SHA-256:
  `2db9d73bf1b6b4cf17c0e9dd98133383ed2436d78c149e6454c047943108760e`
- Use: locates issue 36 in the official journal archive.

## Official issue page capture / 官方第 36 期页面捕获

- File: `ntu-journal-issue36.html`
- Size: `71424` bytes
- SHA-256:
  `437dcc5d62d9b58750d8b4cf47505e8c308ffcb6c1f849793f97c04a3697c099`
- Use: binds the article title, author, issue, and official PDF route.

## Official article PDF / 官方论文 PDF

- File: `song-2012-twelve-carapace-joins.pdf`
- Size: `5809557` bytes
- Length: `34 pages`.
- SHA-256:
  `b25b6841ee7f7e88c12a076a5c3da4cea55d562e7a978956aec4210841b4caf9`
- Relevant pages: printed pages 14-17 and PDF pages 14-17.
- Visual render: passed for pages 14-18 at 180 DPI.

Poppler reported a readable, unencrypted PDF. Reliable Chinese
text extraction failed because embedded font maps produced CID placeholders.
The review therefore used rendered pages rather than recovered plain text.

Poppler 报告 PDF 可读且未加密。因嵌入字库映射只生成 CID 占位，可靠
中文文字提取失败；本次复核依据渲染页，不依据提取文本。

## Workshop report capture / 研习会报道捕获

- File: `2018-workshop-report.html`
- Size: `37491` bytes
- SHA-256:
  `c3e71f85a2dbe80e0b55c7601ec66f0dc9011d37d6560a75be7258d4491cb67b`
- Use: reports the composite as a workshop join example.

## Workshop image capture / 研习会图片捕获

- File: `2018-workshop-heji13517-join.jpeg`
- Size: `21833` bytes.
- Pixel dimensions: `282 x 319`.
- SHA-256:
  `7108f9ec9b5ba25166c73ef6d456a598452c71369e6a4f76fd085183c41bf3d0`
- Use: low-resolution plate-layout corroboration only.

## Derivation and anomaly log / 派生与异常记录

- Temporary PNGs were rendered under `tmp/pdfs/ihp-1222-song2012/`.
- Rendered PNGs are review intermediates and are not committed.
- The official PDF is the evidence anchor for pages 14-17.
- The workshop JPEG has unknown embedded-image reuse rights.
- No captured image provides metric seam close-ups or angled-light views.

- 临时 PNG 渲染于 `tmp/pdfs/ihp-1222-song2012/`。
- 渲染 PNG 是复核中间物，不提交。
- 官方 PDF 是第 14-17 页的证据锚点。
- 研习会 JPEG 的内嵌图片再利用权利未知。
- 已捕获图像均不提供带尺度接缝特写或多角度强光视图。

Review state / 复核状态:
`original_plate_opened_join_not_independently_verified`
