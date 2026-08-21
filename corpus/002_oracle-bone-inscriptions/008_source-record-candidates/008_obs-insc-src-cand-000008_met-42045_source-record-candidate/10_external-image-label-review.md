# External image-label review / 外部图像标签复核

## Purpose / 用途

Wikimedia Commons is a secondary distribution and metadata route for the
Met image files. It is not a substitute for the museum object record. This
page records its view label without changing the Met API fields.

Wikimedia Commons 是大都会图像的次级分发和 metadata 路线，不能替代
博物馆对象记录。本页记录其视图标签，但不改写 Met API 字段。

## Retrieved snapshots / 已取得快照

The two MediaWiki API snapshots remain in the ignored download area:

- `tmp/source_downloads/dl-met-42045-wikimedia-file-001.json`: 5,548 bytes,
  SHA-256 `81d9b7ac88eca2ce1aedc2933600cef2682bdbefd3d69dc4e20904a02fdeaf6a`.
- `tmp/source_downloads/dl-met-42045-wikimedia-file-002.json`: 5,548 bytes,
  SHA-256 `f10e97bb91b32b0bd89b8cc6bbfd41af0f388d38a828b6d907d0000f07cd997b`.

The page routes are:

- `https://commons.wikimedia.org/wiki/File:MET_LC-67_43_14_001.jpg`
- `https://commons.wikimedia.org/wiki/File:MET_LC-67_43_14_002.jpg`

两份 MediaWiki API 快照保存在忽略下载区。前者为 5,548 字节，后者也为
5,548 字节；两者的 SHA-256 已记录在 `90_source-record.json`。

## What the secondary route says / 次级路线的说法

The Commons page for `..._001.jpg` reports the caption
`Oracle bone, China, back (MET, 67.43.14)` and the keyword `Back`. Its
reported media size and SHA-1 exactly match the committed Met
`additionalImages[0]` file. This is a useful external label, not an
independent curatorial statement from the Met.

Commons 的 `..._001.jpg` 页面把图像说明为
`Oracle bone, China, back (MET, 67.43.14)`，关键词为 `Back`。其媒体大小和
SHA-1 与本目录提交的 Met `additionalImages[0]` 文件完全匹配。这是有用的
外部标签，但不是 Met 独立提供的馆藏方向说明。

The observed API metadata for `..._002.jpg` contains no front or back label.
Its reported media size also differs from the committed Met
`primaryImage` bytes, so no byte identity is claimed for that route.

观察到的 `..._002.jpg` API metadata 没有 front 或 back 标签。其报告大小也与
本目录提交的 Met `primaryImage` 字节不同，因此不声称两者字节相同。

## Human research consequence / 对人类研究的影响

The Met API names the files `primaryImage` and `additionalImages[0]` but does
not define a recto-verso relation. The project therefore records:

- external secondary label for the additional image: `back`;
- formal orientation status: `not_established`;
- reading direction, line order, sign count, and inscription identity:
  `not_established`.

Met API 只把两图称为 `primaryImage` 和 `additionalImages[0]`，没有定义正反面
关系。因此项目记录：additional image 有次级路线 `back` 标签，但正式方向仍为
`not_established`；阅读方向、行序、字数和卜辞身份也都未建立。

## Rights and falsification / 权利与可证伪性

The Commons API reports CC0 for both file pages. This is recorded as a
secondary-route rights statement, not as a blanket licence for museum text,
catalogue editions, or future crops. The Met API already reports the fetched
image files as public domain.

Commons API 报告两页均为 CC0。本项目只把它登记为次级路线的权利说法，不能
把它扩大为博物馆文字、著录版本或未来裁切的统一许可。Met API 已报告本项目
取得的两张图像为 public domain。

The orientation label can be promoted only if the Met or a catalogued plate
independently confirms it. It must be withdrawn if the Commons file is shown
to be a different view, upload, or accession mapping.

只有 Met 或有著录依据的图版独立确认方向后，才可提升 orientation 标签；若
证明 Commons 文件是不同视图、不同上传版本或错误馆藏关联，就必须撤回该标签。

This page adds no OCR, transcription, translation, character assignment, or
decipherment claim.

本页没有新增 OCR、摹写、翻译、单字分配或破译主张。
