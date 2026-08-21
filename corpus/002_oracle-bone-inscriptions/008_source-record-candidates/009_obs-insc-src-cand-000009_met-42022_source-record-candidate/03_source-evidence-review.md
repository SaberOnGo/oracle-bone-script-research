# Source evidence and rights review / 来源证据与权利复核

## Evidence layers / 证据层级

| layer | evidence | status |
| --- | --- | --- |
| A | Met API object record | registry snapshot downloaded and hashed |
| A | primary and additional image URLs | fetched and hashed |
| B | Met object page | official route recorded |
| C | Heji, plate, excavation, and scholarship records | not supplied |

The existing source-object dossier records the API route, size, checksum,
package row, field map, and metadata profile. This object folder repeats only
the routes needed for human review.

已有来源对象档案记录 API 路线、大小、校验和、包清单、字段映射和 metadata
profile。本目录只重复人类复核所需的路线。

## Rights and risk / 权利与风险

- The API field `isPublicDomain` is `true` for object 42022.
- Effective image status: `public_domain_verified` for the two fetched image
  files, while the API URL and access date remain attached.
- The public-domain flag is object/API metadata. It is not blanket permission
  for museum prose, third-party catalogs, future crops, or OCR derivatives.
- The two files are unchanged source images. No crop or enhancement is
  committed.

- API 字段 `isPublicDomain` 对对象 42022 为 `true`。
- 两张获取图像的生效状态为 `public_domain_verified`，并保留 API 链接和
  访问日期。
- 公版字段是对象/API metadata，不是博物馆文字、第三方著录、未来裁图或
  OCR 派生物的统一授权。
- 两张文件是未改动来源图像，没有提交裁切或增强版本。

## Provenance boundary / 出处边界

The image checksums prove the fetched bytes. They do not prove a Heji number,
plate identity, findspot, object history, inscription identity, or reading.
Those claims need separate catalog or scholarly evidence.

图像校验和只能证明获取到的字节，不证明合集号、图版身份、出土地、收藏史、
卜辞身份或释读。这些主张需要分别寻找著录或学术证据。

## Review state / 复核状态

- source status: `museum_api_route_reviewed_metadata_only`
- image status: `public_direct_route_and_committed_source_bytes`
- text status: `museum_metadata_only_without_project_transcription`
- formal promotion: blocked pending catalog and text review

- 来源状态：`museum_api_route_reviewed_metadata_only`
- 图像状态：`public_direct_route_and_committed_source_bytes`
- 文字状态：`museum_metadata_only_without_project_transcription`
- 正式提升：等待著录和文字复核，当前阻断
