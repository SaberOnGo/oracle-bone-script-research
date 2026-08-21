# Source evidence review / 来源证据复核

## Evidence chain / 证据链

- `source_id`: `src-ihp-museum-oracle-bones`.
- `source_item`: `503`.
- `accession`: `R044498`.
- `evidence_download_id`: `dl-ihp-museum-oracle-bones`.
- Registered route: IHP museum collection page snapshot.
- Live page capture: 2026-08-14; English HTML SHA-256 begins
  `be3ca1771fc7de10`; Chinese HTML SHA-256 begins
  `dcb5960f9d3986d0`.
- Object-local full hashes are in the linked live-source dossier.
- Rights: `metadata_only_until_verified`.
- Review: `source_record_candidate_needs_catalog_and_text_review`.

The older registered 2026-06-04 HTML log and the new live capture are separate
evidence events. Neither one is silently replaced by the other.

旧的 2026-06-04 HTML 登记和新的现场快照是两条独立证据事件，不能互相静默
替换。

## Live official-page recheck / 官方页面现场复核

On 2026-08-21, the official English and Chinese item pages were re-opened:

- English: `https://museum.sinica.edu.tw/en/collection/32/item/503/`.
- Chinese: `https://museum.sinica.edu.tw/collection/32/item/503/`.

The live page still reports item `R044498`, Late Shang, Pit YH127,
Hsiao-t'un, Anyang, and a turtle plastron. The Chinese page displays
`帝令雨` and describes the source topic as the supreme deity directing the
rain god. This is a source-page recheck, not a new byte snapshot; the
registered HTML hashes above remain the reproducibility record.

2026-08-21 重新打开官方中英文对象页：

- 英文：`https://museum.sinica.edu.tw/en/collection/32/item/503/`。
- 中文：`https://museum.sinica.edu.tw/collection/32/item/503/`。

现场页面仍报告 `R044498`、晚商、YH127 坑、安阳小屯和龟腹甲。中文页显示
`帝令雨`，并把来源主题说明为帝命令雨神。这是页面现场复核，不是新的字节快照；
上面的登记 HTML hash 仍是可复现记录。

On 2026-08-22, new ignored snapshots were retrieved for both official routes
and bound in `90_source-record.json`. The Chinese `.fr-view` block contains
the displayed phrase and the English `.fr-view` block contains source prose.
The two snapshots make the current page display reproducible, but they do not
provide an independent plate, line-addressable edition, or project OCR.

2026-08-22 又取得官方中英文页面的忽略区快照，并在 `90_source-record.json`
中绑定校验和。中文 `.fr-view` 区块包含页面短语，英文 `.fr-view` 区块包含来源
散文。两份快照让当前页面可复核，但仍不提供独立图版、可逐行著录版本或项目 OCR。

## Source and derived evidence / 来源与派生证据

The object-local dossier records image sizes and checksums for private review.
This candidate stores no image bytes and no OCR derivative. Any future text or
image derivative must record permission, source member or URL, checksum, and a
human review status before it can be used here.

本候选不保存图像字节，也不保存 OCR 派生件。未来任何文字或图像派生资料都必
须记录许可、来源成员或 URL、校验和以及人类复核状态。
