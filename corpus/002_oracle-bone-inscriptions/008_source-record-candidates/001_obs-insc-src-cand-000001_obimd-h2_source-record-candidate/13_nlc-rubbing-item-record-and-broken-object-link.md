# NLC Rubbing Item Record and Broken Object Link
# 国图拓片条目与失效实物链接

## English

### Directly checked item

On 2026-08-30, the National Library of China item page was opened and saved
to ignored local storage. It is an item-level rubbing record with:

- database `data_412` and identifier `2022JGTP0627`;
- title `北圖14427` and type `甲骨拓本`;
- findspot `河南省安陽市殷墟出土`;
- period `商武丁（B.C.1250-B.C.1192）`;
- displayed dimensions `7.7×7.2cm` and quantity `1張`;
- references `善9025` and `合集2`;
- corresponding-object label `甲骨14427T`.

The item-detail route is `allSearch/searchDetail` under `read.nlc.cn` with
`searchType=8`, `showType=1`, `indexName=data_412`, and
`fid=2022JGTP0627`.

The source-preserved transcription is:

> ■[王大令眾人]曰： 04114[田]，其受年。[十]一[月]。

The black square and `04114` remain exactly as supplied. They are not
silently normalized into oracle characters or modern readings.

### Replay and image receipt

The public search replay is a form POST to:

`http://read.nlc.cn/advanceSearch/oneSearch/data`

Use `index=data_412`, `pageNo=1`, and an exact title query for
`北圖14427`. The response has `total=1` and
`identifier=2022JGTP0627`.

The checked public image ends with `JPG/L/14427T.jpg` and is:

- 323,056 bytes and 945 by 1,417 pixels;
- SHA-256
  `314c76798a617ec425e2191ef035c1cdd0dc84b47892455f7ccb1c8f5a1b0f08`.

The HTML receipt is 20,344 bytes with SHA-256
`410db860837b86c9e8c5b32bb3649e63bf1c65745ceef4b94b512f06c50465c0`.
The API receipt is 630 bytes with SHA-256
`08c3f91d8d144af4daf8acc5bb9389d02eb2b36e83e4d2dc31dc7df17ed75036`.

All payloads remain ignored. A public image route is not redistribution
permission.

### Boundary and failed route

The page is a rubbing record. Its dimensions are recorded as
`rubbing_record_dimensions_not_physical_object_dimensions`.
They must not be represented as dimensions of the physical bone.

The corresponding-object link for `甲骨14427T` does not resolve to a usable
physical-object item. Exact physical-database searches for `北圖14427`,
`14427`, and `14427T` returned zero records. This is
`broken_physical_object_link`, not proof that the object is absent.

The entry directly checks a source-reported route among `北圖14427`,
`善9025`, and `合集2`. Physical identity, dimensions, material, old
collection, and acquisition history remain pending. C1 stays a candidate
route; C5 and C6 stay blocked; C8 stays withheld.

### Counterevidence and falsifiers

The NLC and OBIMD rubbings differ in bytes and canvas. A coarse comparison
found only moderate similarity. This permits a shared-rubbing-ancestor
candidate, but proves neither file identity nor independent derivation.

NLC, Heji, Shanzhai, Yinqi Wenyuan, and OBIMD can share catalog or image
ancestry. Agreement is not counted as independent paleographic readings.

Reopen the route if a provenance-bearing export maps `2022JGTP0627`,
`北圖14427`, `甲骨14427T`, `善9025`, or `合集2` to a different object.
A stable physical-object export stating its identifier, dimensions,
material, collection history, and rubbing relation would strengthen it.

The shortest next check is an NLC Social Sciences Consultation request at
`skck@nlc.cn` or `010-88545270` for that export and the written relation
among all five identifiers, plus citation and reuse terms.

This review does not establish a reading or decipherment probability.

## 简体中文

### 直接核验的条目

2026-08-30 已打开并保存国家图书馆的条目页。它是条目级拓片记录：

- 数据库 `data_412`，条目标识 `2022JGTP0627`；
- 题名 `北圖14427`，类型 `甲骨拓本`；
- 出土地 `河南省安陽市殷墟出土`；
- 时代 `商武丁（B.C.1250-B.C.1192）`；
- 页面尺寸字段 `7.7×7.2cm`，数量 `1張`；
- 参考信息 `善9025`、`合集2`；
- 对应实物标签 `甲骨14427T`。

条目位于 `read.nlc.cn` 的 `allSearch/searchDetail` 路由，参数为
`searchType=8`、`showType=1`、`indexName=data_412` 和
`fid=2022JGTP0627`。

来源释文原样保存为：

> ■[王大令眾人]曰： 04114[田]，其受年。[十]一[月]。

黑方块和 `04114` 均不静默规范成甲骨字或现代释读。

### 复跑与图像回执

公开检索可向下列地址发送表单 POST：

`http://read.nlc.cn/advanceSearch/oneSearch/data`

参数为 `index=data_412`、`pageNo=1`，并对 `北圖14427` 作标题精确
检索。返回 `total=1` 和 `identifier=2022JGTP0627`。

已核原图路径以 `JPG/L/14427T.jpg` 结尾。图像为 323,056 字节，
945×1,417 像素，SHA-256 为
`314c76798a617ec425e2191ef035c1cdd0dc84b47892455f7ccb1c8f5a1b0f08`。

HTML 回执为 20,344 字节，SHA-256 为
`410db860837b86c9e8c5b32bb3649e63bf1c65745ceef4b94b512f06c50465c0`。
接口回执为 630 字节，SHA-256 为
`08c3f91d8d144af4daf8acc5bb9389d02eb2b36e83e4d2dc31dc7df17ed75036`。

三项载荷均留在已忽略本地区。公开图像地址不等于再分发许可。

### 范围边界与失效路线

该页属于拓片记录，因此尺寸只记为
`rubbing_record_dimensions_not_physical_object_dimensions`，不得写成
实体骨片尺寸。

页面报告对应实物 `甲骨14427T`，但链接不能打开可用的实物条目。
在实物库精确检索 `北圖14427`、`14427` 和 `14427T` 均为零条。
这里记为 `broken_physical_object_link`，不能反推实体骨片不存在。

该条目直接核验 `北圖14427`、`善9025` 和 `合集2` 的来源报告路线。
实体身份、尺寸、材质、旧藏和入藏经过仍待查。因此 C1 继续是候选
路线，C5、C6 继续阻断，C8 继续扣留。

### 反证与证伪条件

国图与 OBIMD 拓片的字节和画布不同，粗略比较仅呈中等相似。这只
允许“可能共享拓片祖先”的候选，不能证明文件相同或来源独立。

国图、《合集》、善斋著录、殷契文渊和 OBIMD 可能共享目录或图像
祖先，不能把相符重复计算成多个独立古文字释读。

若带来源的馆藏导出把 `2022JGTP0627`、`北圖14427`、`甲骨14427T`、
`善9025` 或 `合集2` 指向不同对象，就必须重开当前路线。若获得稳定
实物条目，并明确实物 ID、尺寸、材质、旧藏、入藏经过以及与本拓片
的关系，当前路线才会加强。

最短下一步是通过国家图书馆社科咨询邮箱 `skck@nlc.cn` 或电话
`010-88545270`，索取实物条目导出、五个编号的书面关系说明、引用与
再利用条件。

本页不成立释读，也不给出破译概率。
