# IHP item 1212 Live Source Evidence Review
# IHP 1212 现场来源证据复核

Project ID: `coll-obj-cand-00001`

Object candidate: `ihp-mus-obj-00001`

Review date: `2026-08-14`

## Purpose / 目的

This page records a live check of the official museum page and its image
routes. It adds human-readable evidence to the object dossier. It does not
confirm a plate identity, a transcription, a reading, or a decipherment.

本页记录博物馆官方对象页及其图像路由的现场检查，为对象档案补充可读证据。
本页不确认图版身份、释文、释读或破译结论。

## Official object page / 官方对象页

- Provider / 机构: Museum of the Institute of History and Philology,
  Academia Sinica.
- Object page / 对象页:
  `https://museum.sinica.edu.tw/en/collection/32/item/1212/`
- Source collection item ID / 馆藏对象号: `1212`.
- Item No. / 对象编号: `R035888`.
- Source-reported title / 来源标题: `Ox Scapula for Recording Important
  Events Jia Bian 3333+3361`.
- Source-reported catalog text / 来源著录文字: `Jia Bian 3333+3361`.
- Source-reported period / 来源时期: `Late Shang Period`.
- Source-reported dimensions / 来源尺寸: `38.15(L) x 21.5(W) cm`.
- Source-reported findspot / 来源出土地: `Hsiao-t'un, Anyang County,
  Honan Province`.
- Source-reported material / 来源材质: `Animal Bone`.

The official page also displays the following short source text:
`戊戌帚（婦）喜示一屯。岳。`

官方页还显示以下短来源文字：`戊戌帚（婦）喜示一屯。岳。`

The page gives the source's English rendering as: `On wuxu day, Lady Xi
delivered one pair of ox scapulae. Yue was the recipient.` This is recorded as
source-reported wording, not as a project transcription or new translation.

官方页给出英文译文。这里仅记录为来源报告文字，不把它当作本项目释文或新译文。

The registered local HTML snapshot is 54,136 bytes with SHA-256
`3756b0a5bbf7dc4b595e0f363bd9f5a0ab818d667ca0303903ef74eb7dcdfe57`.
The live page was checked separately, so the snapshot checksum does not prove
byte identity with the live page.

本地登记的 HTML 快照为 54,136 字节，SHA-256 为
`3756b0a5bbf7dc4b595e0f363bd9f5a0ab818d667ca0303903ef74eb7dcdfe57`。
现场页另行检查，因此快照校验和不证明二者逐字节相同。

## Image route checks / 图像路由检查

The page exposes three large-image links. The following results are the
2026-08-14 HTTP checks. The downloaded copies remain only in the ignored
`.working/ihp-1212/` directory for private visual inspection.

官方页提供三条大图链接。以下是 2026-08-14 的 HTTP 检查结果。下载副本只保留
在忽略的 `.working/ihp-1212/` 目录，供本地私下观察。

### Route 1 / 路由 1

- URL host: `https://museum.sinica.edu.tw`
- URL path:
  `/_upload/image/collection_item/large/8876755e62227572.jpg`
- HTTP status: `200`.
- Content type: `image/jpeg`.
- Local temporary file: `.working/ihp-1212/large-1.jpg`.
- Size: `198,619` bytes.
- SHA-256:
  `6d710da16e45592a386bb38988658b3634cc1af57da53de1f14f023c55c20e50`.
- Pixels: `960 x 1280`; RGB JPEG.
- Status: `local_private_visual_inspection_only`.

Human observation: the frame shows an overall ox scapula view with a colour
target, cracks, and visible incised traces. No sign identity or reading is
assigned from this observation.

人类观察：画面显示牛肩胛骨整体视图、色卡、裂隙和可见刻痕。本观察不指定任何
字形身份或释读。

### Route 2 / 路由 2

- URL host: `https://museum.sinica.edu.tw`
- URL path:
  `/_upload/image/collection_item/large/834675e62687616.jpg`
- HTTP status: `200`.
- Returned content type: `text/html; charset=UTF-8`.
- Final URL: `https://museum.sinica.edu.tw/`.
- Returned size: `107,210` bytes.
- SHA-256:
  `79db16fe3b85fb6af975ed98c929db66b0a458e8e1c5cc3003395d0af023ee75`.
- Status: `route_redirected_not_image`.

This response is negative evidence for this access attempt. The HTML response
must not be treated as a second object image or as a checksum for one.

这次响应是该访问尝试的负证据。HTML 响应不能当作第二张对象图像，也不能当作
第二张图像的校验和。

### Route 3 / 路由 3

- URL host: `https://museum.sinica.edu.tw`
- URL path:
  `/_upload/image/collection_item/large/4656755e636be034.jpg`
- HTTP status: `200`.
- Content type: `image/jpeg`.
- Local temporary file: `.working/ihp-1212/large-3.jpg`.
- Size: `122,839` bytes.
- SHA-256:
  `9c286d8829a572386c26dbd8edb0574c18c2f3c042761dee1ec3ba5e40916020`.
- Pixels: `613 x 1280`; RGB JPEG.
- Status: `local_private_visual_inspection_only`.

Human observation: the frame is a closer side view with incised traces and
surface cracks. It is a visual route only; no character segmentation, reading,
or inscription reconstruction is asserted.

人类观察：画面是较近的侧面视图，可见刻痕和表面裂隙。它只是图像路线；本页不
提出字形切分、释读或卜辞重建。

## Text quality and provenance / 文本质量与来源

The museum page supplies a short source text and a short source translation,
but not a complete OCR transcript, plate page locator, sentence segmentation
record, or publication citation for the exact displayed object. The text is
therefore `source_reported_short_text`, not `verified_full_inscription`.

博物馆页提供短来源文字和短来源译文，但没有给出该对象完整 OCR、图版页码、句子
切分记录或精确出版物引文。因此文本状态为 `source_reported_short_text`，不是
`verified_full_inscription`。

The live page, the registered snapshot, the three image URLs, the two JPEG
hashes, and the redirected HTML response must remain separate provenance
records. They are not silently merged into one plate record.

现场页、登记快照、三条图像 URL、两份 JPEG 校验和以及重定向 HTML 响应必须保持为
分开的来源记录，不能静默合并为一个图版记录。

## Concrete next checks / 具体下一步待查

1. Obtain the museum's item-level image permission and reuse terms before any
   public derivative is made.
2. Ask whether route 2 has a corrected stable image or IIIF endpoint.
3. Re-fetch the live page and compare it with the registered snapshot under a
   new access log and checksum.
4. Locate the exact `Jia Bian 3333+3361` publication page, volume, and plate.
5. Match the publication locator to item `R035888` using an independent catalog
   or accession record, not the title alone.
6. Obtain a cited full transcription, OCR, neighbouring signs, and sentence
   context for this exact object.
7. Verify period, findspot, excavation batch, collection history, and shelf
   or accession details from institutional records.
8. Search for named proposers, reading history, contrary readings, and disputes
   without treating the museum's short translation as consensus.

1. 先取得馆方的对象级图像许可和再利用条款，再制作任何公开派生物。
2. 查询路由 2 是否有修正后的稳定图像或 IIIF 端点。
3. 重新抓取现场页，在新的访问记录和校验和下与登记快照比较。
4. 定位 `Jia Bian 3333+3361` 的具体出版物卷册、页码和图版。
5. 使用独立著录或登录记录把出版物位置与 `R035888` 对应，不能只凭标题。
6. 获取该对象的带出处完整释文、OCR、邻字和卜辞上下文。
7. 从机构记录核对时期、出土地、发掘批次、收藏史及库位或登录信息。
8. 查找提出者、释读史、不同释读和争议，不能把馆方短译文当作共识。

## Rights and research boundary / 权利与研究边界

Effective rights status remains `metadata_only_until_verified`. The two JPEG
copies are ignored local inspection files only; no image is committed, copied
into a public dossier, or redistributed here.

有效权利状态仍为 `metadata_only_until_verified`。两份 JPEG 只是忽略区的本地观察
文件；本次不提交图像、不复制到公开档案，也不再分发。

This page is a source-evidence and preprocessing record. It is not a confirmed
collection identity, inscription identity, transcription, formal reading,
component assignment, or decipherment result.

本页是来源证据和预处理记录，不是已确认的馆藏身份、卜辞身份、释文、正式释读、
构件归属或破译结果。
