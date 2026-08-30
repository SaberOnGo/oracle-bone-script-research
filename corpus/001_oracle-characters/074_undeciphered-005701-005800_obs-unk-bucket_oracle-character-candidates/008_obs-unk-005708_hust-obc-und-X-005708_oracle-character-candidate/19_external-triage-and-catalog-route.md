# External Triage And Catalog Route / 外部检索与著录路线

Object / 对象: `obs-unk-005708`

Review date / 复核日期: `2026-08-30`

Adjudication / 裁决: `candidate_route_only`

## Result First / 结果先行

The HUST-OBC archive class used by this object is `X/1264`. A newly inspected
external triage dataset gives its top-1 shape-retrieval route as `U61812`, with
a retrieval score of `0.6742`. A fresh query to the public Yinqi Wenyuan API
returns `U61812`, a blank `JTZ` reading, `合14496（甲3472）`, and a Jitilin child
route `3068`.

本对象实际使用的 HUST-OBC 原包类别是 `X/1264`。本次检查的一项外部
筛查数据把它的形体检索首位路线指向 `U61812`，检索分数为 `0.6742`。
随后对殷契文渊公开接口的实时查询返回 `U61812`、空白 `JTZ` 释读、
`合14496（甲3472）`，以及字统子项路线 `3068`。

This is an auditable candidate catalog route, not a glyph identity, reading,
meaning, or decipherment. The row and downstream API response are checkable,
but the deposited package does not support a complete model rebuild.

The score is not a probability.

这是可审计的候选著录路线，不是字形身份、释读、词义或破译结论。数据行和
下游接口回执可以核查，但归档包尚不能支持完整模型重建。该分数不是概率。

## Source One: Archived Triage Dataset / 来源一：归档筛查数据

- Title / 题名: *A Triage-and-Audit Resource for the 9,408 Undeciphered
  Classes of HUST-OBC, with 279 Verified Metadata Corrections*
- Creator / 创建者: Weiming Shen, independent researcher
- Version DOI / 版本 DOI: `10.5281/zenodo.21290640`
- Concept DOI / 概念 DOI: `10.5281/zenodo.21290639`
- Publication date / 发布日期: `2026-07-10`
- Access date / 访问日期: `2026-08-30`
- Zenodo metadata license / Zenodo 元数据许可: `CC BY 4.0`
- Record / 记录: [Zenodo version record][zenodo-record]
- Code route / 代码路线: [source repository][source-repository]

Downloaded package / 下载包:

- Local ignored path / 本地忽略路径:
  `tmp/source_downloads/dl-zenodo-hustobc-triage-v1.0-20260830.zip`
- Size / 大小: `603639` bytes
- SHA-256:
  `9c0521ca4a6772a5745758f23ef233bf28f41971e419f81ddad209733ebb9eaa`
- Zenodo MD5 / Zenodo MD5: `f68dc110e389b4225cf667986790c123`
- Archive status / 归档状态: ignored local source package

Metadata receipt / 元数据回执:

- Local ignored path / 本地忽略路径:
  `tmp/source_downloads/dl-zenodo-21290639-metadata-20260830.json`
- Size / 大小: `5530` bytes
- SHA-256:
  `c744e6a8dce31d86912565ddf685401470f99b3c6daf41d31684358f7ca3744e`

The ZIP was unpacked only in ignored storage. Its relevant committed-source
row is reproduced here as a human-readable receipt:

```text
X/1264,X,,,,U61812,0.6742,,undeciphered,true,false
```

The source dictionary defines these values as follows:

- `X/1264`: HUST-OBC class and source group `X`.
- `U61812`: top-1 official-code result from shape retrieval.
- `0.6742`: ResNet-18 retrieval similarity, not calibrated probability.
- blank reading: no `JTZ` reading in the source table.
- `undeciphered`: mechanically derived from that blank reading.
- `true`: cached API response had a child with `GLLX=1`.
- `false`: this row is not one of the verified `Y+H` corrections.

来源数据字典还明确区分两类信号：`top1_*` 是形体检索信号；
`identity_*` 只对 `Y+H` 行提供按目录构造确认的身份映射。`X/1264`
属于 `X` 行，没有 `identity_*` 身份映射。因此不得把 `U61812` 提升为
同字结论。

## Reproducibility Audit / 可复现性审计

The deposit includes `build_triage_resource.py`, but the extracted archive
does not include two inputs named by that script:

- `分析/官方映射_HUSTOBC.json`
- `分析/yqwy_all_glyphs.json`

The archived layout also places the script under `data_package/`, while the
script resolves its outputs through `论文/data_package/` from a different
parent level. Therefore `full_rebuild_blocked` is the present status. This
project verified the deposited row and refreshed its API result; it did not
reproduce the ResNet-18 mapping that generated `U61812`.

归档包包含 `build_triage_resource.py`，但解包内容没有脚本指定的上述两个
输入。归档中的脚本位于 `data_package/`，脚本却从不同父级解析
`论文/data_package/` 输出路径。因此当前状态为 `full_rebuild_blocked`。
本项目核查了归档数据行并刷新了接口结果，没有复现产生 `U61812` 的
ResNet-18 映射。

## Source Two: Fresh Official API Receipt / 来源二：官方接口新回执

The public endpoint was queried on `2026-08-30` with:

- Base endpoint / 接口基址: [Yinqi Wenyuan API][yqwy-api]
- Parameters / 参数: `bm=U61812`, `type=getzxbybm`
- Local ignored receipt / 本地忽略回执:
  `tmp/source_downloads/dl-yqwy-U61812-getzxbybm-20260830.json`
- Size / 大小: `173` bytes
- SHA-256:
  `74d678191f49c78455094d338d1a7235f29cc7fda4787a72366b6351352fcd20`
- Retrieval status / 获取状态: `fresh_direct_response`

Exact returned fields / 返回字段原文：

```text
ZKBM=U61812
JTZ=
FTZ=
SSZT=
XGZX=
JGPH=合14496（甲3472）
child: GLLX=1, GLZ=3068
child: GLLX=4, GLZ=409
child: GLLX=7, GLZ=1171
```

The endpoint directly supports the `U61812` catalog metadata above. It does
not directly support any relation between `U61812` and HUST class `X/1264`;
that bridge comes from the external shape-retrieval dataset.

该接口直接支持上述 `U61812` 著录信息，但不直接支持 `U61812` 与 HUST
类别 `X/1264` 的关系；二者之间的桥接来自外部形体检索数据。

## Official Catalog Search And Thumbnail / 官方著录检索与缩略图

The Yinqi Wenyuan catalog search was then queried directly for the returned
Heji number. The search page and JSON response were fetched on `2026-08-30`:

- Search route / 检索路线:
  [catalog search for PM 14496][yqwy-search]
- Request / 请求: `POST /AynuBone/Search`, field `PM`, value `14496`
- Result count / 结果数: `1`
- Returned plate label / 返回片号: `合14496`
- Record form / 记录形式: `拓片`
- Collection field / 著录库字段: `甲骨文合集`
- Official record ID / 官方记录 ID: `SYS_FLD_SYSID=124308`
- Search receipt / 检索回执:
  `tmp/source_downloads/dl-yqwy-search-PM-14496-20260830.json`
- Receipt size and SHA-256 / 回执大小与 SHA-256: `822` bytes;
  `a796ec60eb4d38169a84325a7aca39c46832df56abc33393055726777820a53d`

殷契文渊随后直接按返回的《合》号检索。检索页和 JSON 回执均于
`2026-08-30` 获取：结果只有一条，片号为 `合14496`，记录形式为拓片，
著录库字段为 `甲骨文合集`，官方记录 ID 为 `124308`。检索 JSON 回执的
大小为 `822` 字节，SHA-256 为
`a796ec60eb4d38169a84325a7aca39c46832df56abc33393055726777820a53d`。

The returned record also exposed a public thumbnail URL. The JPEG was fetched
to ignored storage and opened only for visual quality assessment:

- Thumbnail route / 缩略图路线:
  `http://jgw.aynu.edu.cn/File/GetFirstSmallPic?dbId=34&recordId=124308`
  `&key=BaJ7HxysvSdbCJfe3H6%2fXw%3d%3d`
- Local ignored path / 本地忽略路径:
  `tmp/source_downloads/dl-yqwy-smallpic-124308-20260830.jpg`
- JPEG size and SHA-256 / JPEG 大小与 SHA-256: `4204` bytes;
  `1fd22e3992b4b4479d571b0ac026f46cb78844d59f2ba166a5b2d9692fa20638`
- Pixel dimensions / 像素尺寸: `150 x 94`
- Visible label / 可见标记: `14496`
- Image quality / 图像质量: thumbnail only; insufficient for stroke or
  fracture adjudication

返回记录还提供了公开缩略图路线。JPEG 已下载到忽略区，仅用于图像质量
检查。文件大小为 `4204` 字节，SHA-256 为
`1fd22e3992b4b4479d571b0ac026f46cb78844d59f2ba166a5b2d9692fa20638`，
像素尺寸为 `150 x 94`，图中可见 `14496` 标记。它只是缩略图，不能用于
笔画、裂隙或字位裁决。

The catalog detail page documents `GET /AynuBone/DetailData?id=124308`, but
the current unauthenticated request returned `406` with
`登录失效，请先登录`. The saved receipt is:

- Detail page / 详情页:
  [record 124308 detail page][yqwy-detail]
- Detail-data receipt / 详情接口回执:
  `tmp/source_downloads/dl-yqwy-detaildata-124308-20260830.json`
- Receipt size and SHA-256 / 回执大小与 SHA-256: `117` bytes;
  `9c2958e14ec1069ccc49fb919bf3001f6ee0e1bcafc8c76f8112368d921bf83f`
- Access boundary / 访问边界: unauthenticated full-image and detail fields
  were not obtained

著录详情页明确使用 `GET /AynuBone/DetailData?id=124308`，但当前未登录
请求返回 `406` 和 `登录失效，请先登录`。因此目前没有取得未登录状态下的
完整图像和详情字段。该访问边界不是图版缺失，也不是权限已经清理。

This official search result strengthens the catalog leg of the route from
`U61812` to one specific record, but it does not establish that the thumbnail
is the HUST source member, that `甲3472` is the same edition, or that any
visible form has a reading. Rights remain mixed and the thumbnail is not a
committed corpus asset.

这条官方检索结果把 `U61812` 到一个具体著录记录的路线补强了，但仍不能
证明缩略图就是 HUST 来源成员，也不能证明 `甲3472` 与该记录属于同一版本，
更不能由可见形体推出释读。权利仍然混合，缩略图也不作为语料资产提交。

## Cross-Edition Alias Probe / 跨著录别名探查

The same official catalog was queried for `甲3472` using the `PM` field. It
returned exactly one rubbing record:

- Search value / 检索值: `甲3472`
- Collection field / 著录库字段: `殷虚文字甲编`
- Record form / 记录形式: `拓片`
- Official record ID / 官方记录 ID: `SYS_FLD_SYSID=263185`
- Search receipt / 检索回执:
  `tmp/source_downloads/dl-yqwy-search-PM-jia3472-20260830.json`
- Receipt size and SHA-256 / 回执大小与 SHA-256: `820` bytes;
  `b9fd639adc35abc3d704ba525ec2b88350b35dabf74f9d81df2af602072ec9bc`

同一官方著录库随后按 `PM=甲3472` 检索，结果也恰好只有一条拓片记录。
著录库字段为 `殷虚文字甲编`，官方记录 ID 为 `263185`。检索回执大小为
`820` 字节，SHA-256 为
`b9fd639adc35abc3d704ba525ec2b88350b35dabf74f9d81df2af602072ec9bc`。

Its public thumbnail was fetched and compared visually with the `合14496`
thumbnail above:

- Thumbnail route / 缩略图路线:
  `http://jgw.aynu.edu.cn/File/GetFirstSmallPic?dbId=34&recordId=263185`
  `&key=dugE5aeuY9vguTslv36Uuw%3d%3d`
- Local ignored path / 本地忽略路径:
  `tmp/source_downloads/dl-yqwy-smallpic-263185-20260830.jpg`
- JPEG size and SHA-256 / JPEG 大小与 SHA-256: `4314` bytes;
  `66359d61078a926099cbdfa0409cd6e1bebca1849c6f5194f26714d24d9c3bf5`
- Pixel dimensions / 像素尺寸: `150 x 97`
- Visual observation / 视觉观察: the fragment contour and inscription cluster
  are compatible with the `合14496` thumbnail, while bottom labels and image
  dimensions differ
- Comparison limit / 比较限制: thumbnail-level visual compatibility only;
  no pixel-identity, edition, plate-position, or HUST-member identity claim

该记录的公开缩略图也已获取，并与上面的 `合14496` 缩略图作视觉比较。JPEG
大小为 `4314` 字节，SHA-256 为
`66359d61078a926099cbdfa0409cd6e1bebca1849c6f5194f26714d24d9c3bf5`，
像素尺寸为 `150 x 97`。骨片轮廓和刻辞簇视觉相容，但底部标注和尺寸不同。
这只支持缩略图层面的相容性，不支持像素同一、版本同一、确切图位或 HUST
成员同一。

The two catalog records share the same Yinqi Wenyuan platform and therefore
are not independent source families. Their agreement is useful for a
cross-catalog alias candidate, but it must not be counted as two independent
votes for the HUST route.

两条著录记录来自同一殷契文渊平台，不是两个独立来源家族。它们的一致只能
支持跨著录别名候选，不能计作支持 HUST 路线的两票独立证据。

## Evidence Ancestry / 证据谱系

1. `src-hust-obc` supplies the 50 raw members under `X/1264`.
2. The Zenodo resource derives a top-1 route from HUST-OBC and official-code
   data. It is an algorithmic bridge, not an independent identity witness.
3. The fresh Yinqi Wenyuan response independently confirms the metadata now
   returned for `U61812`, but was reached through that candidate bridge.

1. `src-hust-obc` 提供 `X/1264` 下的 50 个原包成员。
2. Zenodo 资源利用 HUST-OBC 与官方编码数据产生首位路线；它是算法桥接，
   不是独立的同字证据。
3. 殷契文渊新回执独立确认当前 `U61812` 元数据，但这个编码入口仍是经由
   上述候选桥接找到的。

The three records therefore do not constitute three independent votes for
identity. Counting them that way would duplicate evidence ancestry.

三项记录不能算作支持同字的三个独立投票。那样计算会重复统计证据谱系。

## Bounded Claim Ledger / 有界主张账本

- C1 object identity / 对象身份: `blocked_candidate_route`
- C2 visible form / 可见字形: `direct_checked_for_50_hust_members`
- C3 same-sign grouping / 同字归组: `withhold`
- C4 inscription route / 卜辞路线: `candidate_catalog_route_only`
- C5 reading / 释读: `abstain`
- C6 meaning / 词义: `abstain`
- C7 evolution / 演变: `abstain`
- C8 new decipherment / 新破译: `withhold`

The only positive proposition is:

> The archived resource reports an algorithmic route from HUST-OBC class
> `X/1264` to official code `U61812`. A fresh API response for that code points
> to `合14496（甲3472）` and Jitilin route `3068`.

唯一的正面主张是：归档资源报告一条从 HUST-OBC 类别 `X/1264` 到官方
编码 `U61812` 的算法路线；该编码的新接口回执又指向
`合14496（甲3472）` 和字统路线 `3068`。

## Counterevidence And Failure Risks / 反证与失败风险

- `0.6742` is an uncalibrated retrieval score, not a posterior probability.
- `X` rows have no construction-guaranteed identity mapping.
- The model mapping cannot be rebuilt from the deposited package alone.
- The resource reports only `19.7%` agreement between top-1 and constructive
  identity codes in the `Y+H` subset. This is its own warning against treating
  shape retrieval as identity, even though it also reports held-out retrieval
  accuracy on known classes.
- The 50 HUST members already show strong mixed-group signals.
- `U61812` currently has no `JTZ` reading in the official API response.
- The bridge may inherit dataset errors, domain shift, and source-image reuse.
- The full `合14496` or `甲3472` plate has not yet been opened here.
- The two official records expose thumbnails only; their full detail route is
  still login-gated and the two thumbnails are not pixel-identical receipts.
- No HUST member has yet been aligned to one exact plate position.

- `0.6742` 是未校准检索分数，不是后验概率。
- `X` 行没有按构造保证的身份映射。
- 仅凭所存数据包不能重建模型映射。
- 该资源报告 `Y+H` 子集中首位编码与构造身份编码的一致率只有 `19.7%`。
  即使它另报已知类别留出检索准确率，这仍是不得把形体检索当作身份的
  内部警告。
- 50 个 HUST 成员已经显示明显的混组信号。
- 官方接口当前没有给 `U61812` 提供 `JTZ` 释读。
- 桥接可能继承数据集错误、领域偏移和来源图像重复。
- 本项目尚未打开 `合14496` 或 `甲3472` 完整图版。
- 尚未把任何 HUST 成员对齐到图版中的一个确切字位。

## Falsification And Strengthening / 证伪与增强条件

Reject or reopen the route if any of the following occurs:

- A rights-permitted full plate shows that the target graph is visibly
  incompatible with every `X/1264` member.
- The two official catalog records resolve to different physical objects or
  the full images show incompatible fragments.
- The missing model inputs are later supplied but do not reproduce the
  `X/1264` row.
- An authoritative catalog maps the relevant HUST source image elsewhere.
- The API receipt changes materially without a recorded version change.

出现以下任一情况，应拒绝或重新审查路线：

- 权利允许的完整图版显示目标字形与所有 `X/1264` 成员均明显不合。
- 补齐缺失模型输入后仍不能重现 `X/1264` 行。
- 权威著录把相关 HUST 来源图像指向别处。
- 接口回执在没有版本记录的情况下发生实质变化。

Strengthen only the catalog route if a full plate and its neighboring text
align one exact HUST member with one exact `U61812` occurrence. That result
still would not automatically establish a reading or meaning.

只有在完整图版及其邻接文字把一个确定 HUST 成员与一个确定 `U61812`
字位对齐后，才增强著录路线。即便如此，也不会自动建立释读或词义。

## Rights And Reuse / 权利与再利用

Zenodo labels the deposited package `CC BY 4.0`. The package also includes
Yinqi Wenyuan factual records and contains an internal note that redistribution
terms for official reading data still needed confirmation. These are different
rights layers. This repository therefore commits no copied source table or API
cache from the package; it keeps only this attributed human-readable receipt.

Zenodo 把所存数据包标为 `CC BY 4.0`。但数据包还含殷契文渊事实记录，且其
内部说明曾标记官方释读数据的再分发条款仍待确认。两者属于不同权利层。
因此本仓库不提交该包复制的来源表或接口缓存，只提交这份注明出处的人类
可读回执。

Risk status / 风险状态: `source_marked_upstream_rights_unresolved`

## Exact Next Action / 确切下一步

Open a rights-permitted full plate for official record `124308` (`合14496`),
or follow the `甲3472` route with an authenticated, rights-permitted session.
Locate the graph associated with `U61812`, preserve neighboring signs and
fracture boundaries, and compare it separately against all 50 members of
`X/1264`. Record an exact plate, page, crop, and catalog receipt.

打开官方记录 `124308`（`合14496`）对应的权利允许完整图版，或在已认证
且权利允许的会话中沿 `甲3472` 路线查阅。定位 `U61812` 关联字形，保留
邻字与断裂边界，再分别同 `X/1264` 的 50 个成员比较，并记录确切图版、
页码、裁切和著录回执。

Until that check is complete, the correct AI decision is `withhold`.

在完成这项检查前，AI 的正确裁决是 `withhold`。

[zenodo-record]: https://zenodo.org/records/21290640
[source-repository]: https://github.com/shenzxc/hustobc-triage-resource
[yqwy-api]: http://jgw.aynu.edu.cn/home/zx/method/jgwzx.ashx
[yqwy-search]: https://jgw.aynu.edu.cn/home/zl/search/index.html
[yqwy-detail]: https://jgw.aynu.edu.cn/home/zl/detail/index.html?id=124308
