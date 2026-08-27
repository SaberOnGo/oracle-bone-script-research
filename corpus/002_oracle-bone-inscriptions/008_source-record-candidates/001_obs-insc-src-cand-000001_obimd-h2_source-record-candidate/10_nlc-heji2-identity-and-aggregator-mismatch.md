# H2 identity adjudication and image mismatch
# H2 身份裁决与图文错配

## Result / 结果

OBIMD `H2` is a high-confidence candidate for *Jiaguwen Heji* 2 and
National Library of China oracle bone 14427. The decisive new evidence is
an institutional page that prints the catalog crosswalk beside a photograph
and rubbing that visually match the OBIMD object.

OBIMD `H2` 是《甲骨文合集》2、国家图书馆甲骨 14427 的高置信候选。
决定性新增证据来自国家图书馆页面：该页在著录对应关系旁刊出照片和拓片，
其对象与 OBIMD 图像目视相符。

A public *Jiaguwen Heji* search page for number 2 displays the text for
Heji 2 but serves an image matching Heji 1. That route has a page-level
text-image mismatch and must not be used as unqualified image evidence.

一个公开《甲骨文合集》检索页在编号 2 页面显示《合集》2 文字，却提供
与《合集》1 相符的图像。该路线存在页面级图文错配，不能作为无条件图像
证据使用。

## Institutional evidence / 机构证据

The National Library of China article is:

- title: *Talking about tiger in the Year of the Tiger: Spring Festival
  materials in the National Library oracle bones*;
- author: Zhao Aixue, National Library of China Ancient Books Library;
- official PDF URL:
  `https://www.nlc.cn/migrated/www.nlc.cn/newhxjy/wjsy/wjls/`
  `wjqcsy/wjd78q/zhcj/202201/P020220128516783103054.pdf`;
- access date: 2026-08-28;
- file size: 1,427,112 bytes;
- SHA-256:
  `a675739ec1bd43ed83a7b902baad71667d28c378e122d0ee96baab8199c0d0d8`;
- locator: PDF page 3, printed page 30;
- rights treatment: local ignored copy and metadata-only research notes.

国家图书馆文章为赵爱学《虎年说“虎”——国家图书馆甲骨所见“春节”
相关资料》。核查定位为 PDF 第 3 页、印刷页 30。原 PDF 和页面派生图均
留在忽略区，仓库只保存来源回执和原创核查说明。

The page states that National Library oracle bone 14427 is Heji 2. Figure 3
places a color photograph above a rubbing and captions both as National
Library oracle bone 14427. The surrounding text gives the following
source-reported partial transcription:

`……[王大令众人]曰：“畬田。”其受年。[十]一[月]。`

该页明确写明国图甲骨 14427 即《合集》2。图 3 把实物照片和拓片并列，
图注标为“国图藏甲骨 14427”。正文同时给出上列来源报告残辞。本项目
不把它改写成项目释文，也不据此直接分配七个字框。

## Visual comparison / 视觉对照

The National Library figure and OBIMD `rubbing/h00002.jpg` agree on this
joint configuration:

- a broad, near-rectangular fragment with a low irregular top edge;
- a small outward projection on the right edge;
- one central vertical sign column and a separate right-edge cluster;
- the same large top sign with two uprights and crossed lower strokes;
- the same long, narrow middle sign and branching lower sign;
- the same lower curved boundary and right-side surface loss.

国家图书馆图 3 与 OBIMD `rubbing/h00002.jpg` 在以下联合特征上相符：

- 宽阔、近矩形残片及低矮不规则上缘；
- 右边缘相同的小型外凸部分；
- 中央纵向字列及右边缘独立字群的位置；
- 顶部双竖、下部交叉的大字形；
- 中部狭长字形和下部枝状字形；
- 下缘曲线及右侧表面残失位置。

The exact official Yinqi Wenyuan `合2` thumbnail had already ranked the
OBIMD image first among 10,077 package members at dHash distance 0. The new
National Library evidence is institutionally and visually independent of
that algorithmic replay. Together they support the high-confidence candidate.

此前，殷契文渊 `合2` 官方缩略图已在 10,077 个 OBIMD 包成员中把本图排
第 1，dHash 距离为 0。新增国家图书馆证据独立于该算法复跑，并提供机构
著录和可读上下文；两条证据共同支持高置信候选。

## Aggregator mismatch / 聚合页错配

The checked public page was:

`https://www.guoxuedashi.com/jgwhj/?bh=2&bhfl=1`

Its ignored HTML snapshot was 25,984 bytes with SHA-256:

`f30fe2e94c631b2bd2accd37b7efdc879131cd50379361b64eaf65f0665b6b10`

The page title, query, row number, and displayed transcription all identify
Heji 2. Its image URL was:

`https://pic2.39017.com/jgwhj/1/000002.png`

The image was 31,325 bytes, 1,712 by 2,064 pixels, with SHA-256:

`df8be7e602be409479f38cab78a5217e2e3e60be90d47bb7f0c803179aedfc8f`

该页标题、查询参数、表格编号和显示释文均指向《合集》2，但图像是一块
高而尖的三角形残片。国家图书馆同页图 4 把这一三角形对象明确标为
《甲骨文合集》1；图 3 的《合集》2 则是与 OBIMD `H2` 相符的近矩形对象。

The mismatch is not inferred from text alone. The served triangle and the
National Library Heji 1 figure agree in overall outline, the tall central
inscription field, the transverse lower break, and the lower-right extension.

错配不是只凭文字推断。聚合页所供三角形图像与国家图书馆《合集》1 图在
整体外轮廓、高耸中央刻辞区、下部横向断裂及右下延伸部分相符。

## Candidate decision / 候选裁决

- proposition: OBIMD `H2` maps to Heji 2 and NLC oracle bone 14427;
- result: `high_confidence_candidate_heji2_cross_source_match`;
- strongest alternative: both the NLC caption and Yinqi Wenyuan `合2`
  record independently point to the wrong object;
- alternative assessment: no opened source supports that alternative;
- formal `obi-*` promotion: withheld;
- source transcription: collected as institutional display, not accepted as
  a project transcription;
- decipherment effect: none.

- 命题：OBIMD `H2` 对应《合集》2、国图甲骨 14427；
- 结果：`high_confidence_candidate_heji2_cross_source_match`；
- 最强替代解释：国图图注与殷契文渊 `合2` 记录各自独立指错同一对象；
- 替代解释评估：已打开来源均不支持；
- 正式 `obi-*` 提升：暂缓；
- 来源释文：作为机构页面显示内容收集，不作为项目释文接受；
- 对破译的影响：无。

No percentage is displayed. This object-identity task has no registered,
clean calibration cohort. “High confidence” is an evidence rank, not a
measured posterior probability.

不显示百分比。本仓库尚无为对象身份任务预登记的干净校准群。“高置信”
表示证据等级，不表示已测量的后验概率。

## Falsifiers / 可推翻条件

Reopen or reject the candidate if any of these occurs:

- a provenance-bearing Heji plate shows a different object for number 2;
- the NLC corrects figure 3 or its 14427-to-Heji-2 mapping;
- Yinqi Wenyuan corrects `合2` to a different object;
- checksum-bound replay no longer reproduces the OBIMD member match;
- a collection record assigns NLC 14427 another Heji number.

出现以下任一情况时，应重开或否决候选：

- 有来源链的《合集》图版把编号 2 对应到另一对象；
- 国家图书馆更正图 3 或 14427 与《合集》2 的对应关系；
- 殷契文渊把 `合2` 更正为另一对象；
- 带校验和的复跑无法再得到 OBIMD 成员匹配；
- 馆藏记录把国图 14427 分配给另一《合集》号。

## Boundary / 边界

This finding adjudicates a catalog identity candidate and records a public
page defect. It does not confirm excavation provenance, period, group,
character identities, reading alignment, translation, or decipherment.

本发现裁决一个著录身份候选，并记录公开页面缺陷。它不确认出土信息、
时期、组类、单字身份、逐字释文对齐、翻译或破译。
