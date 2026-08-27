# Join Database and Bibliographic Review
# 缀合数据库与书目复核

Review date / 复核日期: `2026-08-28`

Status / 状态: `historical-stage crosswalk candidate`

This review queries Fudan University's official `Zhuiyu Lianzhu` oracle-bone
join database. It separates two published join stages and normalizes one R
number. It does not replace either original plate or the physical object.

本次复核查询复旦大学官方“缀玉联珠”甲骨缀合信息库，区分两条出版
缀合阶段，并规范一个 R 号。数据库记录不能替代原始图版或实物。

## Reproducible query route / 可复跑查询路线

- Host: `https://www.fdgwz.org.cn`
- Path: `/ZhuiHeLab/Home`
- Method: `POST`
- Form field: `txtname`
- Queries: `合集13517`, `乙6087`, `R060751`, and `綴彙1028`.
- Access date: `2026-08-28`.

数据库说明要求著录简称加足位片号。四个查询分别从合集号、乙编号、
六位 R 号和缀合汇编号进入；结果不是搜索引擎摘要。

## Later stage returned by the database / 数据库返回的后续阶段

Queries for `合集13517`, `乙6087`, and `R060751` return the same record:

`Heji 13517 (Yi 4817+5061+5520+5804) + Yi 6087 + R060751`.

The database attributes it to Song Yaping and cites both the 2012 article and
the 2018 article by Zhang Weijie and Song Yaping. The museum label writes the
last unit as `R60751`; zero padding is therefore retained only as an
`R-number normalization candidate`.

查询 `合集13517`、`乙6087`、`R060751` 返回同一条记录：

`《合》13517（《乙》4817+5061+5520+5804）+《乙》6087+R060751`。

数据库把缀者记为宋雅萍，出处列 2012 年论文和张惟捷、宋雅萍 2018 年
论文。馆方标签写作 `R60751`，所以补零形式仅登记为 R 号规范化候选。

## Earlier stage returned by the database / 数据库返回的较早阶段

Queries for `乙6087` and `綴彙1028` also return a shorter record:

`Heji 13517 (Heji Supplement 00417 is one part) + Yi 6087`.

Its sources are `Zhuihui 1028` and Song Yaping's 2012 article. This record
does not include `R060751`. It also adds a candidate relation from
`Heji Supplement 00417` to part of `Heji 13517`.

查询 `乙6087` 与 `綴彙1028` 还返回一条较短记录：

`《合》13517（《合补》00417 为一部分）+《乙》6087`。

出处为《缀彙》1028 和宋雅萍 2012 年论文。该条没有 `R060751`，并新增
《合补》00417 是《合》13517 一部分的候选关系。

Together, the two rows support a `two-stage source record`: the shorter
`Zhuihui 1028` stage and a later source-reported addition of `R060751`.
This is a `historical-stage crosswalk candidate`, not independent proof that
either join is physically correct.

两条记录共同支持一项`两阶段来源记录`：较短的《缀彙》1028 阶段，
以及来源报告的后加 `R060751` 阶段。这只是历史阶段对应候选，不是对
任一实物缀合成立的独立证明。

## Bibliographic correction and anomaly / 书目校正与异常

Fudan's official publication notice for volume 7 states that the 2018 paper
starts on page 20 and the next paper starts on page 30. The defensible page
range is therefore `20-29`, not `20-30` as some secondary records report.

复旦官方第七辑出版页显示，2018 年论文始于第 20 页，下一篇始于第 30 页。
因此可据此写作第 20-29 页，不沿用部分二手记录的第 20-30 页。

A 2024 repost says the 2012 article was included in a book published in
2011. That chronology is impossible as written. The database's separate rows
suggest that `Zhuihui 1028` represents an earlier join state cited alongside
the later article. This remains a `bibliographic anomaly`, not a correction
to the unopened original book.

2024 年转载页称 2012 年论文“收入”2011 年出版的书，按字面理解年代矛盾。
数据库的分条记录提示，《缀彙》1028 更可能是与后出论文并列引用的较早
缀合阶段。此处只登记为`书目异常`，不擅自改写尚未打开的原书。

## What remains unopened / 仍未打开的资料

The query opens a line-addressable database record, but the `Zhuihui 1028`
original plate still unopened. It supplies no metric seam image, page scan,
or rights statement for the book. The 2018 original paper is also not openly
retrieved; only its official table of contents and later quotation routes are
open.

本次已打开可定位的数据库记录，但《缀彙》1028 `原始图版仍未打开`。
数据库没有提供带尺度接缝图、原书扫描页或该书权利声明。2018 年论文原文
也尚未公开取得；目前只有官方目录页和后出引文路线。

Direct padded-number searches for `R053740`, `R053840`, `R054970`, and
`R062431` returned no join row on this access date. This is negative search
evidence only. The subsequent IHP artifact-register review in file `14`
opened all four official artifact records and their `ZR038421` membership.
The negative result therefore means only that this join database has no row
for those search keys.

本次以补零号查询 `R053740`、`R053840`、`R054970`、`R062431`，未返回
缀合条目。后续文件 `14` 已打开四个正式实物登记及其 `ZR038421` 成员
关系。因此阴性结果只说明本缀合库未按这些检索键返回条目。

## Capture and provenance / 捕获与追溯

All snapshots remain under the ignored local capture root:

`.working/ihp-1222-plate-search-20260828/`

- `fd-join-search-heji13517.html`: `41638` bytes;
  SHA-256 `d0f3c87f46aa01d05e9c9bd48f91ce72dbb90e02128333bce642e52bc15289e7`.
- `fd-join-search-r060751.html`: `41041` bytes;
  SHA-256 `348476beaf101f0e8bc93590cb9069c882cc00ecde5a1e133456dbff67b0c006`.
- `fd-join-search-yi6087.html`: `41634` bytes;
  SHA-256 `d9818f9eb07b3f843627d15cb923f19f459ebdb95ec4ef29911734d222983615`.
- `fd-join-search-zhuihui1028.html`: `40844` bytes;
  SHA-256 `54f1fc0bf967ca7e2001f1b1f2c2764a0759315b3808d7453ca959bba7d4e8a1`.
- `fd-2018-volume7-publication.html`: `24210` bytes;
  SHA-256 `0f959eb722fb6a99238396986cf14fbe7994fa91cabe36aab7d662ec7f24514e`.
- `fd-join-search-r053740.html`: `40248` bytes;
  SHA-256 `218d5ff5ad2bb8b1d72ea92b7e22693cf2f2fa76bd367d2ff03495b86539af7d`.
- `fd-join-search-r053840.html`: `40248` bytes;
  SHA-256 `3268a09f576e57d9db7937ffb12719ee3f6473b98eee3d05edee02fe3b087990`.
- `fd-join-search-r054970.html`: `40248` bytes;
  SHA-256 `1ef812c511c60c0c7b8f7d6ed094b4f6cdbe56b0eeb2f7d0e453582d51857540`.
- `fd-join-search-r062431.html`: `40248` bytes;
  SHA-256 `dc111211d1c5bf6323460adc24dcc63418d790976a01fe111381d1ab317748cf`.

Rights status / 权利状态: `metadata_only_until_verified`.

## Claim gate and next checks / 主张门槛与下一步

- Keep both database rows instead of flattening them into one timeless join.
- Do not promote zero padding to a formal identity match without IHP records.
- Open the `Zhuihui 1028` original plate and bibliographic volume.
- Obtain the original 2018 paper at pages 20-29 through a lawful route.
- Compare the opened IHP scale-bearing images without geometric warping.
- Require physical seam evidence before any join verdict.

- 保留两条数据库记录，不压平成一条无时间层次的缀合。
- 未取得史语所正式记录前，不把补零号提升为正式身份对应。
- 打开《缀彙》1028 原始图版和原书书目信息。
- 通过合法路线取得 2018 年论文第 20-29 页原文。
- 在禁止几何形变条件下比较已打开的史语所带尺度图像。
- 任何缀合裁决前仍需实物接缝证据。
