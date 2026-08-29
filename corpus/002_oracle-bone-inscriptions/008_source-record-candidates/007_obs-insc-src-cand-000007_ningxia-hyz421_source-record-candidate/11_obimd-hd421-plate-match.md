# OBIMD HD421 plate match
# OBIMD HD421 图版匹配

## Result / 结果

The OBIMD raw annotation record has one exact `HD421` row. It points to a
rubbing and a facsimile with the same base name. The inspected rubbing page
prints `421` and `H3:1325` below the object and `Rubbing plate 383` above it.

OBIMD 原始标注中只有一条精确的 `HD421` 记录，指向同名拓片与摹本。已检查
拓片页在对象下方印有 `421`、`H3:1325`，上方印有“拓片图版 383”。

The plate and the committed Ningxia photograph show the same distinctive
object-level structure. This changes the photograph identification from a
withheld label-only claim to an uncalibrated candidate supported by a
plate-level visual match. It does not create a formal `obi-*` identity.

图版与已提交宁夏照片显示同一组具有辨识力的对象结构。因此，照片身份从
“仅有标签、暂缓判断”提升为“有图版级视觉匹配支持的未经校准候选”，但仍
不建立正式 `obi-*` 身份。

## Source and extraction receipt / 来源与抽取回执

- source: OBIMD external archive already registered as `src-obimd`;
- annotation package: `data.json`, 41,732,948 bytes, SHA-256
  `b504b0d4e7a0126d494c161f5445c5ee4225659ff5e94182685fce35d261aa19`;
- rubbing package: `rubbing.zip`, 558,367,972 bytes, SHA-256
  `4d07dca94e94c2d17edd7fa25be72b5673161c0c2d03dac4d2c094e5341b7747`;
- facsimile package: `facsimile.zip`, 210,800,641 bytes, SHA-256
  `b1544e34ee1a6a34fc0a83475a227fd2141a67293f795eaa3c52760fedb50b0e`;
- exact annotation row: `RubbingName=HD421`;
- package paths: `rubbing/hd421.jpg` and `facsimile/hd421.jpg`;
- targeted extraction date: 2026-08-28;
- each extracted image: 2,528 by 3,479 pixels;
- rubbing bytes: 414,522; SHA-256
  `ca546645ddac768b3e96a1b112f1054c6f8bd6edd5299c386a55b50401253a74`;
- facsimile bytes: 234,573; SHA-256
  `7d594c69affdec1e56f1b4384788d6c7b9b48d410bd50da9aa6db798ef612f98`.

原始大包和定向抽取图像均留在 Git 忽略区。仓库只提交来源路径、大小、
校验和和原创核查说明。

## Annotation structure / 标注结构

The `HD421` row has four groups:

- two inscription-sentence groups, each with 12 ordered character boxes;
- one oracle-sequence group with two ordered boxes;
- one oracle-sequence group with one box.

`HD421` 行共有四组：

- 两个卜辞句组，各含 12 个有顺序的字框；
- 一个含两个字框的兆序组；
- 一个含一个字框的兆序组。

This structure is compatible with Schwartz 2019 recording two numbered
entries with different crack-sequence marks. The dataset UIDs and boxes are
routing data, not project readings or confirmed character identities.

这一结构与 Schwartz 2019 记录两条编号卜问、兆序标记不同相容。数据集 UID
和字框只是检索路线，不是本项目释读或已确认单字身份。

## Visual landmarks / 视觉地标

The plate and photograph agree on a combination that is much more specific
than the general blunt-rounded outline:

- the same broad upper contour and shallow central change of curvature;
- the same asymmetric lateral notches and lower paired projections;
- the same dense restoration-fracture mosaic across the whole plastron;
- the same circular openings in the middle and right fields;
- two inscription clusters in the same lower-left area;
- matching long seams through and around those inscription clusters.

图版与照片在以下组合特征上相符，其特异性远高于一般的钝圆外轮廓：

- 相同的宽阔上缘及中部浅曲率变化；
- 相同的不对称侧缺口和下部成对突起；
- 遍布整版且形态相同的密集修复裂缝网；
- 中部与右侧区域相同的圆孔位置；
- 同样位于左下区域的两组刻辞；
- 穿过并环绕两组刻辞的长裂缝位置相合。

No single landmark is decisive. Their joint spatial arrangement is the
identity evidence. This remains a visual review, not a calibrated geometric
registration experiment.

单个地标都不足以裁决；具有辨识力的是这些地标的联合空间配置。本次仍是
目视复核，不是经过校准的几何配准实验。

## Counterevidence and unresolved issues / 反证与未决项

- Schwartz's raw row reports 21.6 by 15.1 cm; Commons reports
  28.3 by 20.0 cm.
- OBIMD does not identify which physical edition or scan copy supplied this
  page in the inspected annotation row.
- No Ningxia Museum accession record has been opened.
- OBIMD's effective repository rights remain
  `metadata_only_until_verified`.

- Schwartz 原始数据行报告 21.6 × 15.1 厘米，Commons 报告
  28.3 × 20.0 厘米；
- 已检查标注行没有说明该页来自哪个物理版本或扫描本；
- 尚未打开宁夏博物馆藏品登记；
- OBIMD 在本仓库的有效权利状态仍是
  `metadata_only_until_verified`。

The dimension conflict now weighs primarily against one source's measurement
metadata, not against the visual identity match. It remains open and must not
be silently corrected.

尺寸冲突现在主要质疑某一来源的测量元数据，而不是否定视觉身份匹配；该冲突
仍保持公开，不得擅自改正。

## Candidate decision / 候选裁决

- proposition: the Ningxia photograph depicts HYZ 421, H3:1325;
- result: `candidate_route_plate_visual_match`;
- strongest alternative: a mislabeled OBIMD page and a different but nearly
  identical restored plastron;
- alternative assessment: not supported by any opened source;
- release: retain as an uncalibrated AI candidate;
- formal promotion: withheld pending independent replay and museum or
  edition provenance;
- decipherment effect: none.

- 命题：宁夏照片所示对象是 HYZ 421、H3:1325；
- 结果：`candidate_route_plate_visual_match`；
- 最强替代解释：OBIMD 页被错标，且照片是另一件几乎完全相同的修复卜甲；
- 替代解释评估：已打开来源均不支持；
- 交付：保留为未经校准的 AI 候选；
- 正式提升：等待独立复跑及馆藏或版本来源链，暂不执行；
- 对释读的影响：无。

No percentage is displayed. The repository has no clean, task-specific
calibration set that could turn this case score into a defensible probability.
The status describes an evidence-ranked candidate, not a measured posterior
probability.

不显示百分比。仓库尚无针对对象身份任务的干净校准集，不能把本案评分转换成
可辩护概率。当前状态只表示按证据排序的候选，不表示已测量的后验概率。

## Falsifiers / 可推翻条件

Reopen or reject the candidate if any of these occurs:

- a provenance-bearing edition page maps plate 383 to another object;
- independent alignment shows that the crack network or holes do not match;
- the OBIMD archive row and image entries fail checksum-bound replay;
- a museum record assigns the photographed object another excavation number;
- evidence shows that the photograph was digitally assembled from another
  source object.

出现以下任一情况时，应重开或否决候选：

- 有来源链的版本页面把图版 383 对应到另一对象；
- 独立配准证明裂缝网或孔位不相符；
- OBIMD 归档行与图像不能按校验和复跑；
- 馆藏记录把照片对象分配给另一发掘号；
- 证据证明照片由另一来源对象数字拼合而成。

## Online access incident / 在线访问异常

The public Oracular viewer advertises the OBIMD rubbing-transcription route.
On 2026-08-28 its `HD421` API request returned HTTP 500 because the server
could not resolve its configured Tencent database host. This is an access
incident, not a negative record result. The checksum-bound local archive was
therefore used for the reproducible review.

公开 Oracular 浏览器说明其提供 OBIMD 拓片与释文路线。2026-08-28 查询
`HD421` 时，接口因服务器无法解析所配置的腾讯数据库主机而返回 HTTP 500。
这属于访问故障，不是“查无记录”。本次因此使用带校验和的本地归档复核。

## Boundary / 边界

This dossier identifies an object-level candidate. It does not confirm a
museum accession, settle the conflicting measurements, create a transcription,
assign characters, or decipher an inscription.

本档案提出对象级身份候选，不确认馆藏号，不解决尺寸冲突，不制作释文，
不分配单字，也不破译卜辞。
