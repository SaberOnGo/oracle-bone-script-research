# Independent catalog leads / 独立著录线索

## Lead A: Senri Kinran repository / 线索 A：千里金兰大学库

Search results on 2026-08-22 exposed a relevant journal PDF route:

The URL is split only for the 80-column rule:

- base: `https://kinran.repo.nii.ac.jp/record/424/files/`
- file: `133-146%E6%9C%AB%E6%AC%A12019.pdf`

The result identifies *Senri Kinran University Bulletin* volume 16,
pages 133--146 (2019). Its indexed excerpt mentions `乙5867＝合集補3539反面`,
`YH127`, a turtle object, red writing and engraving, and the source books
*Dang Jiaguwen Yushang Kaogu* p. 76 and `乙編（二版）`.

2026-08-22 搜索结果显示一条相关期刊 PDF 路线：

中文 URL 同样只为满足每行 80 字符而拆分：

- 基址：`https://kinran.repo.nii.ac.jp/record/424/files/`
- 文件：`133-146%E6%9C%AB%E6%AC%A12019.pdf`

结果标明《千里金兰大学纪要》第 16 卷 133--146 页（2019）。索引摘要提到
`乙5867＝合集補3539反面`、`YH127`、龟材、朱书与契刻，并引用
《当甲骨遇上考古》第 76 页和《乙编（二版）》。

The direct HEAD request returned HTTP 410 on the audit date. No PDF bytes,
checksum, author, or article title were accepted into the evidence record.
The indexed excerpt is therefore a lead only, not an independent catalog match.

直接 HEAD 请求在审计日返回 HTTP 410。本档案没有取得 PDF 字节、校验和、作者或
文章题名。索引摘要只能作为线索，不能作为已核验的独立著录对应。

## Lead B: group-class table / 线索 B：分组分类表

The Sinica-hosted table route is:

`https://cdp.sinica.edu.tw/zip/temp/yyuyen.pdf`

Search indexing exposes a row for `8202` with period column `4` and group
label `典賓`. The PDF is very large and the direct request returned an error;
no local bytes or checksum were obtained. This row is a route clue only and
does not establish that the museum's `I 5867+8202` join equals a Heji plate.

中研院托管的表格路线为：

`https://cdp.sinica.edu.tw/zip/temp/yyuyen.pdf`

搜索索引显示 `8202` 一行的时期栏为 `4`、组类为 `典賓`。该 PDF 很大，直接
请求返回错误；没有取得本地字节或校验和。该行只是路线线索，不能证明博物馆的
`I 5867+8202` 拼接等于某一合集图版。

## Required follow-up / 必须后续核对

1. Recover Lead A from the repository or library mirror and record its
   bibliographic metadata, checksum, author, title, and cited page images.
2. Check whether `I 5867` is the same notation as `乙5867` before joining it
   to any `合集補3539` reference.
3. Retrieve the cited `乙編（二版）` and *Dang Jiaguwen Yushang Kaogu* page
   under a rights-permitted route, then compare the object image.
4. Retrieve the group table or an authoritative mirror and record its
   methodology before using `典賓` as a period or group observation.

1. 从原库或图书馆镜像取得线索 A，记录书目、校验和、作者、题名和所引页图像。
2. 先核对 `I 5867` 是否等同于 `乙5867`，再连接任何 `合集補3539` 记录。
3. 在权利允许的路线取得《乙编（二版）》和《当甲骨遇上考古》所引页，
   再与对象图像对照。
4. 取得分组表或权威镜像，先记录其方法，再使用 `典賓` 作为时期或组类观察。

## Boundary / 边界

Both leads remain `unverified_catalog_lead`. They do not establish a plate,
Heji identity, period, group, text, reading, or decipherment.

两条线索均保持 `unverified_catalog_lead`。它们不能建立图版、合集身份、时期、
组类、文字、释读或破译结论。
