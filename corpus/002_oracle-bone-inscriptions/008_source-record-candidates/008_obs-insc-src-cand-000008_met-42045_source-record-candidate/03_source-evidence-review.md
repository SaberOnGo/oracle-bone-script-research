# Source evidence and rights review / 来源证据与权利复核

## Evidence layers / 证据层级

| layer | evidence | status |
| --- | --- | --- |
| A | The Met Open Access API JSON | downloaded and hashed |
| A | API primary image | downloaded, hashed, and inspected |
| A | API additional image | downloaded, hashed, and inspected |
| B | Commons historical Met image | downloaded, hashed, and inspected |
| B | Met object page | official route recorded |
| C | Heji, plate, and scholarly records | not supplied; search needed |

The API snapshot was fetched on 2026-08-21. It is 1590 bytes with SHA-256
`74efc7255beeed6cf1400d86c336c5b97a5638a683956e83fa7216ad42f152b9`.
The raw JSON remains ignored; its fields are transcribed into
`90_source-record.json` and the human pages.

API 快照于 2026-08-21 获取，共 1590 字节，SHA-256 为
`74efc7255beeed6cf1400d86c336c5b97a5638a683956e83fa7216ad42f152b9`。
原始 JSON 保留在忽略区；其字段被记录到 `90_source-record.json` 和
人类页面中。

## Rights and risk / 权利与风险

- The API field `isPublicDomain` is `true`.
- Effective image status: `public_domain_verified` for these two fetched
  image files, subject to retaining the API URL and access date.
- The public-domain flag is object-level API metadata. It does not grant
  blanket permission for museum text, future derivatives, or third-party
  catalog editions.
- No crop, enhancement, OCR, or derived image is committed.

- API 字段 `isPublicDomain` 为 `true`。
- 两张获取图像的生效状态为 `public_domain_verified`，但仍保留 API 链接和
  访问日期。
- 公开领域标记是对象级 API metadata，不是博物馆文字、未来派生物或第三方
  著录版本的统一授权。
- 未提交裁切、增强、OCR 或其他图像派生物。

## Provenance boundary / 出处边界

The API checksum proves the fetched bytes. It does not prove the findspot,
Heji number, plate identity, reading order, or inscription interpretation.
Those claims need separate catalog or scholarly evidence.

API 校验和只能证明获取到的字节，不证明出土地、合集号、图版身份、阅读顺序
或卜辞释读。这些主张需要分别寻找著录或学术证据。

## 2026-08-28 refresh / 2026-08-28 刷新

The current Met API response is again 1590 bytes and has the same SHA-256
recorded above. The fields for geography, excavation, locus, reign, and tags
remain empty. This proves that the checked API payload did not change; it does
not prove that the museum holds no unpublished catalog or conservation data.

本次 Met API 响应仍为 1590 字节，SHA-256 与上文相同。geography、
excavation、locus、reign 和 tags 字段仍为空。这只能证明本次检查的 API
内容没有变化，不能证明馆方没有未公开著录或保护资料。

The Commons API snapshot for `MET 67 43 14.jpeg` is 5507 bytes with SHA-256
`3e428163a4e8f59517560dfde11c0bc13d4914e5ce1a74102e472e12eb8da115`.
It reports 35178 media bytes, 900 x 207 pixels, media SHA-1
`bc3f5ec46c6ac1268a61ab05cab50703fc01c0ff`, the Met donation route,
and CC0. The raw API receipt remains under the ignored `.working/` route.

Commons API 快照为 5507 字节，SHA-256 如上；它报告图像大小、像素、
媒体 SHA-1、Met 捐赠路线和 CC0。原始回执保留在被忽略的 `.working/`。

A direct command-line request to the Met object page encountered a Vercel
security checkpoint. A separately rendered public-page route still exposed
the object metadata and the headings `Signatures, Inscriptions, and Markings`
and `Provenance`, but no section body was available in the checked response.
This is an access result, not evidence that those sections are empty.

命令行直接访问 Met 对象页时遇到 Vercel 安全检查。另一路公开页面渲染仍能
看到对象 metadata，以及 `Signatures, Inscriptions, and Markings` 和
`Provenance` 标题，但本次响应没有给出栏目正文。这是访问结果，不是这些
栏目为空的证据。
