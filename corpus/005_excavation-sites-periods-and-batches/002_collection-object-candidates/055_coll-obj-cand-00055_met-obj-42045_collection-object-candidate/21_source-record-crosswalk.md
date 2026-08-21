# Source-record crosswalk / 来源记录交接

Project object: `coll-obj-cand-00055` / Met object `42045`.

This page joins the collection-object dossier to the separate source-record
candidate for the same museum object. It does not create a second identity,
transcription, or reading.

本页把馆藏对象档案与同一博物馆对象的来源记录候选连接起来。
它不新建第二个身份，也不制作释文或释读。

## Matched routes / 对应路线

- Collection object: `42045`, accession `67.43.14`.
- Source-record candidate: `obs-insc-src-cand-000008`.
- Source-record area:
  [`002_oracle-bone-inscriptions`](../../../002_oracle-bone-inscriptions/)
- Candidate folder: `008_obs-insc-src-cand-000008_met-42045_`
  `source-record-candidate`.
- Read `README.md`, `01_object-and-image-routes.md`, and
  `09_two-view-human-evidence.md` inside that candidate folder.

The two routes share the museum object ID, accession number, title, API URL,
and API checksum. The source-record candidate is the authoritative local
entrance for the two image bytes; this collection-object folder keeps its
single collection-object asset as the compact visual entrance.

两条路线共享博物馆对象 ID、馆藏号、题名、API URL 和 API checksum。
来源记录候选是两张图像字节的本地权利与来源入口；本馆藏对象目录保留
其中一张作为紧凑的对象图像入口。

## Two API image routes / 两条 API 图像路线

- `primaryImage` ->
  `001_asset-000001_met-42045-image-002.jpg`;
  1780568 bytes; SHA-256 `c605ae36...e0333df`.
- `additionalImages[0]` ->
  `002_asset-000002_met-42045-image-001.jpg`;
  1616877 bytes; SHA-256 `c2c09d61...30a480`.

Both files are unchanged API image bytes and are marked
`public_domain_verified` at the object API level. The API does not say that
the second image is a reverse, edge, or reading-order view. The project must
therefore preserve the API field names and avoid recto-verso or text-order
claims.

两张文件都是未改动的 API 图像字节，对象 API 层标为
`public_domain_verified`。API 没有说明第二张图是背面、边缘或阅读顺序视图。
因此项目保留 API 字段名，不作正反面或文字顺序判断。

## What this adds to the human dossier / 对人类档案的补充

- A reader can open the source-record candidate after the compact collection
  image and inspect both original image routes.
- The two-view page records direct visual observations without OCR, cropping,
  enhancement, orientation assignment, or character segmentation.
- The collection dossier's one-view statements mean “one image is kept in this
  collection folder”; they do not deny the second source-record view.

- 读者先看本目录的紧凑对象图，再打开来源记录候选查看两条原图路线。
- 双图页面只记录不经 OCR、裁切、增强、定向或字形切分的直观观察。
- 本目录档案所说的“一张图”是指本馆藏目录内保存一张图；不否认来源
  记录候选中的第二张图。

## Still blocked / 仍然阻断的事项

- No Heji number, plate, page, findspot, excavation unit, or full text is
  supplied by the API snapshot.
- No source establishes a stable orientation or a line-addressable sign
  segmentation across the two views.
- No project inscription ID, character ID, component assignment, reading,
  translation, or decipherment conclusion is assigned.
- Before formal comparison, locate an accession-linked catalog or publication
  plate and bind every proposed text unit to that external evidence.

- API 快照没有提供合集号、图版、页码、出土地、发掘单位或全文。
- 没有来源建立两图之间稳定的方向或可定位字形切分。
- 项目没有分配卜辞 ID、单字 ID、构件归属、释读、翻译或破译结论。
- 正式比较前，必须找到馆藏号关联的著录或出版图版，并把每个拟议文字
  单位绑定到外部证据。

Review status / 复核状态:
`source_record_candidate_needs_text_and_catalog_review`.
