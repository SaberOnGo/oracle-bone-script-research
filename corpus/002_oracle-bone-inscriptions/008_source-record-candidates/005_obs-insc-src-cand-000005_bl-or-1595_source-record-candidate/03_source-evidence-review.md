# Source evidence and rights review / 来源证据与权利复核

## Evidence layers / 证据层级

| layer | evidence | status |
| --- | --- | --- |
| A | Commons recto and verso file pages | opened and hashed |
| A | Wikimedia image API metadata | opened, hashed, and kept local |
| B | British Library collection provenance | supplied in page metadata |
| B | Heji and Yingguo references | source-reported, not cross-checked |
| C | Commons inscription strings and eclipse note | source-reported only |

The Commons pages state that the files were provided by the British Library
from its digital collections. The official catalogue now resolves the item
to record `040-003126498` under collection record `032-002915678`. This is a
catalogue identity route, not an image, plate, or transcription route.

Commons 页面说明图像由大英图书馆数字馆藏提供，并给出
`Or. 7694/1595` 著录路线。本次记录了该路线，但尚未取得稳定的逐项
馆藏记录和权威图版扫描。

The ignored retrieval record in `01_object-and-image-routes.md` names the
two API snapshots. The recto snapshot is 9181 bytes with SHA-256
`2ccddd07df6e814efefcfcd51e166fa34cda340c728387cff6fe9ec1e1f39633`;
the verso snapshot is 9327 bytes with SHA-256
`71778aa79e0a99cf9d477d27cc91e269e2170f28c6aa50b626dd69b4e24cf0b7`.
They remain local-only retrieval evidence, not committed page content.

`01_object-and-image-routes.md` 中的访问记录列出了两份 API 快照。正面快照
为 9181 字节，SHA-256 为
`2ccddd07df6e814efefcfcd51e166fa34cda340c728387cff6fe9ec1e1f39633`；
背面快照为 9327 字节，SHA-256 为
`71778aa79e0a99cf9d477d27cc91e269e2170f28c6aa50b626dd69b4e24cf0b7`。
它们只作为本地访问证据，不提交页面正文。

The British Library item HTML was also captured in the ignored download
area. The 41120-byte snapshot has SHA-256
`1a4672c0524d02ca1048e76787c2e5015825671f72023d988d03bb3549e3422c`.
The parent collection snapshot is 166069 bytes with SHA-256
`1f3336ecd238857fb7d5cfa4ff02b7d66ffc8f95f6cfcdc4edb6fbcb057a1b65`.
These hashes bind the catalogue fields in
`09_british-library-catalog-record.md`; the HTML remains local-only under
`tmp/source_downloads/`.

大英图书馆逐项记录 HTML 也已保存到忽略下载区。41120 字节快照的
SHA-256 为
`1a4672c0524d02ca1048e76787c2e5015825671f72023d988d03bb3549e3422c`。
集合快照为 166069 字节，SHA-256 为
`1f3336ecd238857fb7d5cfa4ff02b7d66ffc8f95f6cfcdc4edb6fbcb057a1b65`。
这些校验和绑定 `09_british-library-catalog-record.md` 的馆藏字段；
HTML 仍只保存在 `tmp/source_downloads/` 忽略目录。

## Rights and risk / 权利与风险

- Image pages: `CC0 1.0 Universal Public Domain Dedication`.
- Effective image status: `public_domain_verified` for the two Commons
  files as displayed on their file pages.
- Page text and structured metadata: retain source attribution; do not copy
  long prose or treat the page license as a blanket license for all catalog
  editions.
- Risk: the Commons file page is a dissemination route, not proof that every
  underlying museum object, edition, or future derivative has identical terms.
- Repository use: two unchanged source images are committed under the object
  folder; no crop or OCR derivative is committed.

- 图像页面：`CC0 1.0 Universal Public Domain Dedication`。
- 图像有效状态：两张 Commons 图像页面显示为
  `public_domain_verified`。
- 页面文字和结构化 metadata：保留来源署名，不复制长段落，也不把页面
  许可理解为所有著录版本的统一授权。
- 风险：Commons 文件页面是传播路线，不证明底层馆藏对象、版本或未来
  派生物都具有相同条件。
- 仓库使用：对象目录保存两张未改动的来源图像，不提交裁图或 OCR
  派生物。

## Provenance boundary / 出处边界

The image checksum proves the fetched bytes. It does not prove the Heji
number, the astronomical date, or the page transcription. Those claims need
separate catalog or scholarly evidence.

The catalogue record proves a stable shelfmark and hierarchy only. It does
not independently verify the Commons Heji or Yingcang references, the source
strings, the eclipse date, or the twentieth-century-addition warning.

图像校验和只能证明已下载字节，不证明合集号、天文日期或页面摹写。
这些主张需要分别寻找著录或学术证据。

馆藏记录只证明稳定馆藏号和层级关系，不能独立核验 Commons 的合集号、
英藏号、来源文字、月食年代或“二十世纪添加”警示。
