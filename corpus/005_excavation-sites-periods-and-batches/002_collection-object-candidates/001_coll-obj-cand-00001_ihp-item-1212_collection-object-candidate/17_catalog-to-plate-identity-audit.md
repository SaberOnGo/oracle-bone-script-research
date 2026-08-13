# IHP item 1212 Catalog-to-Plate Identity Audit
# IHP 1212 馆藏对象与图版身份核对

Project ID: `coll-obj-cand-00001`

Object candidate: `ihp-mus-obj-00001`

English:

This is a human-readable preprocessing audit. It does not confirm an
inscription identity, a plate identity, a transcription, or a reading.

本页是人类可读的预处理核对记录，不确认卜辞身份、图版身份、释文或
释读。

简体中文：

## Evidence opened / 已打开证据

- Provider / 机构: Museum of the Institute of History and Philology.
- Item ID / 对象号: `1212`.
- Object page / 对象页:
  `https://museum.sinica.edu.tw/en/collection/32/item/1212/`
- Source row / 来源行:
  `corpus/005_excavation-sites-periods-and-batches/000_collection-registers/`
  `002_ihp-museum-oracle-bone-object-staging.csv`, row `1`.
- Registered snapshot / 登记快照: 54,136 bytes.
- Snapshot SHA-256 / 快照 SHA-256:
  `3756b0a5bbf7dc4b595e0f363bd9f5a0ab818d667ca0303903ef74eb7dcdfe57`.
- Access route / 访问记录: `dl-ihp-museum-oracle-bones`.

The checksum proves the registered HTML snapshot route. It does not prove
that the current live page has the same bytes.

该 checksum 只证明登记的 HTML 快照路线，不证明当前网页字节相同。

## Catalog values / 著录取值

| Field / 字段 | Source-reported value / 来源记录 |
| --- | --- |
| Collection / 收藏 | `Oracle Bones` |
| Title / 标题 | `Ox Scapula for Recording Important Events Jia Bian 3333+3361` |
| Catalog text / 著录文字 | `Jia Bian 3333+3361` |
| Thumbnail route / 缩略图 | `8876755e62227572.jpg` URL in the packet |
| Findspot / 出土地 | Not recorded in the current object packet |
| Period / 时期 | Not recorded in the current object packet |
| Repository / 馆藏地 | Institution is recorded; shelf location is not |

The plus sign in the catalog string is preserved as source text. It is not
treated as a verified physical join or a reconstructed plate.

著录字符串中的加号按来源原样保留，不把它当作已验证的合缀或重建图版。

## Catalog-to-plate status / 著录到图版状态

- The object page and source row establish a metadata route to item `1212`.
- No local image, rubbing, publication plate, page locator, or full text is
  present in this object directory.
- The thumbnail is an external URL metadata route only. It was not imported.
- Therefore the relation `item 1212 -> Jia Bian 3333+3361` is a source-record
  candidate, not a confirmed plate or inscription identity.

- 对象页和来源行建立了指向 `1212` 的 metadata 路线。
- 本目录没有本地图像、拓片、出版图版、页码定位或卜辞全文。
- 缩略图只是外部 URL 路线，没有导入本地。
- 因此 `对象 1212 -> Jia Bian 3333+3361` 只是来源记录候选，不是已确认
  的图版或卜辞身份。

## Concrete next checks / 具体下一步核查

1. Does the official item page expose a stable image or IIIF route for item
   `1212`, and what are its access and rights terms?
2. Which publication or catalog page contains the plate for
   `Jia Bian 3333+3361`?
3. Can the plate locator be matched to the exact museum object without using
   the title alone?
4. Is a rubbing, OCR, transcription, or sentence context available for this
   exact object, with a page and source citation?
5. Which source proves period, findspot, batch, and repository details?

1. 官方对象页是否为 `1212` 提供稳定图像或 IIIF 路线，权利条件是什么？
2. 哪一部出版物或著录页包含 `Jia Bian 3333+3361` 的图版？
3. 能否不用标题本身，将图版定位与同一馆藏对象逐项对应？
4. 该对象是否有带页码和出处的拓片、OCR、释文或卜辞上下文？
5. 哪个来源可以证明时期、出土地、批次和馆藏位置？

## Rights and boundary / 权利与边界

Effective rights status: `metadata_only_until_verified`.

Do not download or publish the thumbnail as a project asset until item-level
rights and a checksum record are reviewed. Do not promote this candidate into
the formal inscription corpus or use it as a decipherment result.

生效权利状态为 `metadata_only_until_verified`。在复核对象级权利和
checksum 前，不下载或发布缩略图。不得把本候选提升为正式卜辞资料，
也不得把它作为释读结果。
