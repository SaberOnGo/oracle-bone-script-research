# Official page text evidence / 官方页面文字证据

## Snapshot route / 快照路线

The official IHP item page was retrieved on 2026-08-22 and kept in the
ignored local area:

`https://museum.sinica.edu.tw/en/collection/32/item/1215/`

- Local snapshot: `.working/ihp-1215/item-page-20260822.html`
- HTTP status: `200`
- Content type: `text/html; charset=utf-8`
- Size: `56,558` bytes
- SHA-256:
  `7100895f3b873c9a829055ca05bff761a0ca7b077b7a61272a8943711f394c93`

史语所官方对象页于 2026-08-22 抓取，并保存在忽略区。HTML 快照为
56,558 字节，HTTP 200，类型为 `text/html; charset=utf-8`；校验和已经写入
`90_source-record.json`。原始 HTML 不进入 Git，也不作为正式释文。

## Stable page anchors / 稳定页面定位

The snapshot contains one article block with these source anchors:

- CSS-like locator `.fr-view > strong`: `帚（婦）井示。韋。`
- CSS-like locator `.fr-view > div`: the museum's English source prose.
- The same block is followed by `R044587`, `Late Shang Period`, dimensions,
  findspot, and `Turtle Plastron` fields.

快照中有一个来源文章区块：

- `.fr-view > strong`：`帚（婦）井示。韋。`
- `.fr-view > div`：馆方英文来源散文。
- 同一区块后依次出现 `R044587`、`Late Shang Period`、尺寸、出土地和
  `Turtle Plastron` 字段。

The HTML strong element is a source display field, not a line-addressable
edition. The English paragraph is source-reported interpretation. It has no
author, publication page, plate number, or independent citation in this
snapshot.

HTML 的 strong 元素只是来源显示字段，不是可逐行定位的著录版本。英文段落是
来源方解释；本快照没有给出提出者、出版页码、图版号或独立引文。

## Human research use / 人类研究用途

This snapshot makes the displayed text and the associated object metadata
reproducible for a researcher. It does not establish whether the short
string is complete, a fragment, a caption, or a later catalog annotation.

本快照让研究者可以复核页面显示文字及同页对象元数据，但不能确定短文字是
完整卜辞、残片、说明文字还是后加著录标记。

The three private image routes remain a separate evidence family. The page
text is not assigned to a particular visible fragment, line, stroke, or
character. No OCR, normalization, translation, or character linkage is
created here.

三条私有图像路线仍是独立证据族。页面文字没有对应到任何具体残片、行、笔画
或单字。本页没有建立 OCR、规范化文本、译文或单字关联。

## Concrete next checks / 具体待查

1. Re-fetch the same URL and compare the new HTML hash and the `.fr-view`
   anchors before relying on the displayed text.
2. Locate the catalog label in *Yi Bian* and record edition, volume, page,
   plate, and exact citation.
3. Check whether an independent plate identifies the same object and text,
   and preserve any differing characters or punctuation.
4. Ask whether the museum's English paragraph is a catalog quotation,
   curator summary, or translation with a named proposer.

1. 重新抓取同一网址，比较新的 HTML 校验和及 `.fr-view` 定位后，再使用页面
   显示文字。
2. 在《逸编》中定位著录标签，记录版本、卷、页、图版和完整引文。
3. 用独立图版核对对象和文字，并保留任何不同字形或标点。
4. 查明馆方英文段落是著录引文、策展摘要，还是有提出者的译文。

## Boundary / 边界

Effective rights remain `metadata_only_until_verified`. The snapshot is an
access and provenance record, not a permission to redistribute the private
images or museum text.

有效权利仍为 `metadata_only_until_verified`。快照是访问和出处记录，不代表可
再分发私有图像或博物馆文字。

This page is a source-record preprocessing aid. It is not a confirmed
inscription identity, transcription, reading, or decipherment result.

本页是来源记录预处理辅助资料，不是已确认的卜辞身份、释文、释读或破译结果。
