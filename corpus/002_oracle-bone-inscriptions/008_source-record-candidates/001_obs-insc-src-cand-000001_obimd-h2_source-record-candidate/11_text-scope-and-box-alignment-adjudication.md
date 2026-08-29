# H2 Text Scope And Box Alignment Adjudication
# H2 文本范围与七框对齐裁决

Review dates / 复核日期: 2026-08-28, 2026-08-30

## English

### Outcome

The seven H2 boxes now have a reproducible source-metadata alignment
candidate. The chain is H2 `Characters[].UID`, the subcharacter-to-main
mapping, then `Main-character.json`. In annotation order it reports:

| Order | UID | Lookup route | Platform reference | Decision |
| --- | --- | --- | --- | --- |
| 0 | `9xhq4zclpe` | `曰` | `曰` | candidate |
| 1 | `ve0ebxq620` | `協` | `𫩻\|򧅇\|協` | alternatives kept |
| 2 | `pzvzykmf5e` | `田` | `田` | candidate |
| 3 | `qmvfvw99v9` | `其` | `其` | candidate |
| 4 | `52a130pcmy` | `受` | `受` | candidate |
| 5 | `xkubtjk815` | `年` | `年` | candidate |
| 6 | `lstx3iocs6` | `U+FFB45` | `十一月` | granularity warning |

This is a dataset-metadata alignment, not a project transcription. The first
six routes are modern lookup labels reported by OBIMD, not independent
readings. Order 1 also preserves two other platform reference values. At
order 6, PUA glyph codepoint `U+FFB45` and multi-character reference `十一月`
serve different metadata roles and are not contradictory. Their granularity
warns against silently assigning one accepted character to the box.

The project field guide describes this field as a platform-supplied modern
character for lookup, not a final interpretation:
`research/001_published-scholarship-index/004_obimd-2024-2026_data-paper/`
`04_field-evidence-guide.md`. This adjudication preserves that boundary.

The two metadata inputs are checksum-bound in the download register:

- subcharacter-to-main mapping: 71,318 bytes; SHA-256
  `967c1ee8dea2bee444b07657eab05e0fc35f1d9585ebd532ffca7c7c13f65b77`;
- `Main-character.json`: 451,652 bytes; SHA-256
  `17db8ffebf246571dd004c5ef7c42316e6c6dde74210fbdab466a4067c45de6e`.

Both belong to the OBIMD source family. Their agreement is an auditable
internal route, not independent corroboration.

### Direct per-box neutral visual observation

Both registered 1022 by 1180 images were opened. The coordinates in
`91_character-occurrence-index.csv` were checked against the facsimile crop
sheet and the full rubbing. These observations use no modern label:

- `0`: a near-rectangular lower outline, a short detached inner horizontal,
  and a left upright. The object outline crosses the right side. The rubbing
  shows the corresponding pale group at the right edge.
- `1`: three descending curved strokes, lower crossings or loops, and short
  left strokes. The rubbing shows a dense matching group, but local texture
  limits separation of the junctions.
- `2`: a narrow upright outline with two small inner or side divisions. It is
  close to the right object edge; completeness is unresolved in the rubbing.
- `3`: two capped uprights over crossed diagonals and a low curved line. The
  rubbing preserves the interior group; the object outline enters the crop's
  upper-right corner.
- `4`: several oblique and near-horizontal strokes cross a long descending
  curve. The rubbing confirms the group, but exact junctions remain unclear.
- `5`: an upper angular trace, a central crossing cluster, and one long lower
  descent. The rubbing shows the same group with weaker lower contrast.
- `6`: a long upper horizontal is separated from a lower wavy or hooked trace
  and a small dark mark. The box overlaps the lower object boundary, so one
  sign, multiple traces, and damage remain live alternatives.

This completes C2 for the seven registered occurrences only. It does not
validate any lookup label, segmentation, or reading.

### Exact Heji locator and older catalog route

The official Xiaoxuetang Heji Material Source Table was queried directly by
POST with `hejinum=2`. Its one returned row reports:

Query route:
`https://xiaoxue.iis.sinica.edu.tw/obm/Home/PageContent`.

- Heji plate: `2`;
- earliest catalog route: `粹866`;
- selected route: `善9025`;
- original bone or rubbing holding: `北圖`;
- duplicate, join, and note fields: blank.

The database legend states that a Heji number is a plate identifier and that
one Heji plate number represents one physical oracle-bone object. Its data
are based on the 1999 printed Heji material source table. The response was
captured as 2,337 bytes with SHA-256
`3181ca77e710c733f7c9b1c81e83f1d69935b2076560f92c62c21b8c825cacba`.

The CiNii Books record `BN05177578` places Heji 2 in volume 1, first period,
whose range is plates 1-1139. It reports the first printing of volume 1 as
October 1982. The printed leaf or page number carrying plate 2 was not
obtained. The stable research locator is therefore volume 1, first period,
plate 2, not an invented page number.

### Published same-text evidence

Liu Ying's article, *Four New Joins of Bin-group Ox Scapulae*, appeared in
*Palace Museum Journal*, 2011 issue 1, total issue 153, pages 22-27. The
official page PDFs for printed pages 22 and 23 were opened and rendered.

Printed page 23 states that Heji 2 and Heji 5 are same-text inscriptions. It
does not reproduce Heji 2. It presents a different, more complete join of
Heji 1 and Heji Supplement 657, then uses same-text comparison to restore a
longer passage. The article assigns this material to the Bin group.

The printed passage supports the literal order of routes 0 and 2-5: `曰`,
`田`, `其`, `受`, and `年`, followed by a month phrase. The graph between
`曰` and `田` is not established here as the OBIMD lookup route `協`. Order 1
is unresolved and supplies no corroboration, but is not treated as
disconfirmation without a reviewed reading. The month phrase also does not
prove whether order 6 covers one sign, several traces, or damage.

The two official DPM page captures remain in ignored storage:

- page 22: 644,706 bytes; SHA-256
  `b1efa2adb056734d8db24aa93c4a5998253057831970b6dca3b1488033461f48`;
- page 23: 616,833 bytes; SHA-256
  `8a3033f66bb3f6c252c54d5dbf9e3bbc694b104818f9b892741cbcf89dfbe8d5`.

The object-local download IDs are
`dl-dpm-liu-2011-bin-group-joins-p022-20260828` and
`dl-dpm-liu-2011-bin-group-joins-p023-20260828`. Their ignored paths begin with
`tmp/source_downloads/` and are recorded in `90_source-record.json`.

Official page routes are recorded in `90_source-record.json`. Public Git
keeps the locators, checksums, scope, rights note, and decision, but not the
copyrighted page images.

### Source-family analysis

The evidence families are not all independent:

1. OBIMD `data.json`, its subcharacter-to-main mapping, and
   `Main-character.json` belong to one dataset family. Their agreement proves
   an internal route, not a reading.
2. The National Library article supplies institutional object identity and a
   source-reported partial transcription for NLC 14427 / Heji 2.
3. Liu 2011 supplies a published same-text argument and Bin-group context,
   but its longer text is reconstructed from a different joined object.
4. Xiaoxuetang supplies the 1999 material-source-table catalog route. It does
   not supply a transcription or a Heji 2 plate image in the captured row.

The National Library and Xiaoxuetang both ultimately concern the Heji catalog
tradition. They are separate access and institutional routes, but they must
not be counted as wholly independent paleographic readings.

### Claim-gate decision

- `C1`: object-identity `candidate_route`; formal promotion withheld.
- `C2`: `direct_checked` for the local rubbing and facsimile, with checksums,
  dimensions, exact boxes, and per-box neutral observations.
- `C4`: `candidate_route`. Boxes and order are `direct_checked`; the National
  Library partial text and Liu page are opened source-text evidence. Full H2
  text has an explicit bounded absence, and Bin-group status is
  `source_reported`.
- `C5`: `blocked`. The forms are source-reported metadata, including an
  order-1 unresolved divergence and the order-6 granularity warning. There is
  no completed reading history with disagreements and negative evidence.
- `C6`: `blocked` because C5 is blocked; no semantic probability is allowed.
- `C7`: `not_applicable_no_diachronic_proposition`.
- `C8`: delivery is `withhold`; action is `abstain`. There is no task-specific
  calibration, clean holdout, or complete C5-C6 evidence.

The deliverable result is therefore a falsifiable source-metadata alignment
candidate plus an explicit reading abstention. No numeric probability is
displayed.

### Claim recording contract

Adjudication version: `2026-08-30-h2-text-scope-v1`.

Stable adjudication path:
`11_text-scope-and-box-alignment-adjudication.md#claim-recording-contract`.

- `C1`: `candidate_route`; items `ev-h2-obimd-row`, `ev-h2-nlc-fig3`,
  and `ev-h2-xxt-heji2-row`. Shared ancestry blocks formal identity.
- `C2`: `direct_checked`; items `ev-h2-obimd-rubbing` and
  `ev-h2-obimd-facsimile`. This applies only to seven occurrences.
- `C3`: `not_asserted_not_applicable`; no same-sign, variant, or component
  claim is made.
- `C4`: `candidate_route`; items `ev-h2-obimd-main-route`,
  `ev-h2-nlc-fig3`, and `ev-h2-liu-2011-p23`. Full text and segmentation
  remain incomplete.
- `C5`: `blocked`; items `ev-h2-obimd-main-route` and
  `ev-h2-liu-2011-p23`. Order 1 and the reading history remain unresolved.
- `C6`: `blocked` by C5. No semantic probability or translation is allowed.
- `C7`: `not_applicable_no_diachronic_proposition`; no evolution claim was
  tested.
- `C8`: delivery `withhold`; action `abstain`. There is no calibrated,
  independent delivery basis.

Evidence families and dependencies:

- `family-obimd-derived`: the H2 row, rubbing, facsimile, and main route.
  OBIMD reports that its image route derives from Yinqi Wenyuan.
- `family-nlc-heji-publication`: `ev-h2-nlc-fig3`, an institutional access
  route within the Heji catalog and image tradition.
- `family-liu-2011-same-text`: `ev-h2-liu-2011-p23`, a published same-text
  argument within the Heji text tradition.
- `family-xxt-1999-heji-table`: `ev-h2-xxt-heji2-row`, a database route based
  on the 1999 printed material-source table.
- `ev-h2-cinii-bn05177578` supplies source-reported bibliography only.
- `family-public-aggregator-quality-control`: `ev-h2-guoxue-mismatch`,
  retained only as negative quality-control evidence.

Each applicable claim below records its own alternative, falsifier, blocker,
next-source question, abstention reason, delivery state, version, and path.
The machine mirror is `90_source-record.json` under `per_claim_contract`.

- `C1`: strongest alternative is shared Heji-catalog or image ancestry, or an
  unseen mapping or version error, repeating one wrong identity. Falsifier:
  a provenance-bearing plate 2 shows a different object. Blocker and impact:
  plate 2 is absent, so formal identity is withheld. Next-source question:
  does a rights-permitted Heji volume 1 plate 2 match the H2 object? Abstain
  from formal identity; delivery is `withhold`. Evidence and state:
  `ev-h2-obimd-row`, `ev-h2-nlc-fig3`, and `ev-h2-xxt-heji2-row` are
  `direct_checked`; their roles remain source identity or catalog metadata.
  Their named families share Heji catalog or image ancestry.
- `C2`: strongest alternative is that one or more boxes include damage or
  multiple traces. Falsifier: a reviewed plate changes a box boundary or the
  two registered images fail checksum replay. Blocker and impact: plate-level
  segmentation is absent, so the check applies only to visible occurrences.
  Next-source question: does plate 2 preserve the same seven bounded groups?
  Abstain from sign identity; delivery is `withhold`. Evidence and state:
  `ev-h2-obimd-rubbing` and `ev-h2-obimd-facsimile` are `direct_checked`
  within `family-obimd-derived` and share that visual ancestor.
- `C4`: strongest alternative is a different edition line order or span.
  Falsifier: a page-located edition disagrees with the recorded order.
  Blocker and impact: the full text and exact edition page are missing, so
  context remains a candidate route. Next-source question: what page-located
  transcription aligns to plate 2? Abstain from full-text delivery;
  delivery is `withhold`. Evidence: `ev-h2-obimd-main-route` is
  `direct_checked`; `ev-h2-nlc-fig3` and `ev-h2-liu-2011-p23` are
  `direct_checked`; their roles identify source-reported text. Their named
  families share the Heji text tradition.
- `C5`: strongest alternative is that OBIMD lookup normalization differs from
  an accepted reading or segmentation. Falsifier: a reviewed reading history
  resolves orders 1 and 6 with negative evidence. Blocker and impact: the
  reading history is incomplete, so form claims are blocked. Next-source
  question: which named editions discuss the two positions? Abstain from
  character reading; delivery is `withhold`. Evidence: the OBIMD main route is
  `direct_checked`; their roles are `source_reported_lookup_metadata` and
  `source_reported_same_text`. Both named families share Heji text ancestry.
- `C6`: strongest alternative is that a semantic interpretation depends on a
  different C5 reading. Falsifier: C5 passes and opposing semantic readings
  are adjudicated. Blocker and impact: C5 is blocked, so translation and
  semantic probability are blocked. Next-source question: none before C5
  passes. Abstain from semantics; delivery is `withhold`. There is no C6
  evidence item or family while C5 remains blocked.
- `C8`: strongest alternative is that apparent agreement comes from shared
  ancestry rather than independent correctness. Falsifier: a preregistered,
  leakage-audited calibration with distinct source ancestors supports
  delivery. Blocker and impact: no such calibration exists, so no numeric
  probability or candidate reading may be delivered. Next-source question:
  can a clean benchmark with independent ancestors be built? Abstain from
  candidate delivery; delivery is `withhold`. The item
  `ev-h2-guoxue-mismatch` is `direct_checked`, with role
  `negative_quality_control`, in
  `family-public-aggregator-quality-control`; it does not create an
  independent paleographic witness.

### Strongest alternative and falsifiers

The strongest alternative is that the OBIMD hierarchy normalizes several
signs or a phrase-like span under a main-character UID. Order 6 supplies
direct internal warning for that possibility. Sequence agreement alone
cannot exclude incorrect segmentation or normalization.

The alignment must be reopened if any of the following occurs:

- an opened Heji 2 printed plate differs from the registered H2 object;
- a plate-bearing edition assigns a different line or box order;
- a box covers damage, punctuation, or multiple signs rather than one sign;
- an edition-specific transcription disagrees with one of orders 0-5;
- a reviewed source identifies order 6 as something other than the visible
  remnant expected by the month phrase.

The highest-value next source is a rights-permitted scan or physical copy of
Heji volume 1 showing plate 2 and its neighboring printed locator. It should
be compared beside the H2 image, not substituted by an aggregator image.

## 简体中文

### 裁决结果

H2 七个字框现已有可复跑的来源元数据对齐候选。证据链依次为 H2
`Characters[].UID`、子字到主字映射、`Main-character.json`。按标注顺序：

| 次序 | UID | 检索路线 | 平台参考今字 | 裁决 |
| --- | --- | --- | --- | --- |
| 0 | `9xhq4zclpe` | `曰` | `曰` | 候选 |
| 1 | `ve0ebxq620` | `協` | `𫩻\|򧅇\|協` | 保留异值 |
| 2 | `pzvzykmf5e` | `田` | `田` | 候选 |
| 3 | `qmvfvw99v9` | `其` | `其` | 候选 |
| 4 | `52a130pcmy` | `受` | `受` | 候选 |
| 5 | `xkubtjk815` | `年` | `年` | 候选 |
| 6 | `lstx3iocs6` | `U+FFB45` | `十一月` | 粒度警告 |

这是一条数据集元数据对齐，不是本项目释文。前六项是 OBIMD 报告的今字
检索标签，不是本项目独立释出的字；次序 1 还保留两个平台参考异值。
次序 6 的 PUA 字形码位 `U+FFB45` 与多字参考值 `十一月` 用途不同，并不
互相矛盾；但其粒度警告我们，不能静默把该框判成一个已接受的字。

项目字段指南明确说明，该字段是平台提供的今字检索值，不是最终解释：
`research/001_published-scholarship-index/004_obimd-2024-2026_data-paper/`
`04_field-evidence-guide.md`。本裁决保持这一边界。

两个元数据输入均已有下载登记和校验和：子字到主字映射为 71,318 字节，
SHA-256 为
`967c1ee8dea2bee444b07657eab05e0fc35f1d9585ebd532ffca7c7c13f65b77`；
`Main-character.json` 为 451,652 字节，SHA-256 为
`17db8ffebf246571dd004c5ef7c42316e6c6dde74210fbdab466a4067c45de6e`。
二者同属 OBIMD 来源家族，只能证明可审计的内部路线，不能充当独立互证。

### 七框直接中性视觉观察

本次打开了两张已登记的 1022×1180 图像，并把
`91_character-occurrence-index.csv` 的坐标与摹本裁切、拓片全图逐一核对。
以下观察不使用任何今字标签：

- `0`：下部近矩形轮廓、内部一条短横和左侧竖画；实物轮廓穿过右侧。
  拓片右缘可见对应浅色刻画组。
- `1`：三条下行曲画、下部交叉或回环及左侧短画。拓片有对应密集画组，
  但局部纹理使交接关系难分。
- `2`：狭长竖向轮廓，内侧或右侧有两个小分隔；紧邻实物右缘，拓片中
  是否完整仍不确定。
- `3`：两条顶端带短横的竖画，下接交叉斜画和低位曲线；拓片保留主体，
  实物轮廓进入裁切框右上角。
- `4`：多条斜画和近横画与一条长下行曲画相交；拓片确认画组，但交点
  关系仍不明确。
- `5`：上部折角、中部交叉画组和一条长下行画；拓片有对应画组，下端
  对比度较弱。
- `6`：上部长横与下部波折或钩状痕迹分离，中间另有小暗痕；字框覆盖
  实物下缘，因此单字、多痕迹和残损都仍是有效替代解释。

这只补足七个已登记出现位置的 C2，不验证任何检索标签、切分或释读。

### 《合集》确切定位与旧著录路线

本次以 `hejinum=2` 直接 POST 查询小學堂《甲骨文合集材料來源表》。唯一
返回行记录：

查询 URL 记录在同目录 `90_source-record.json`。

- 合集图版号：`2`；
- 著拓号：`粹866`；
- 选定号：`善9025`；
- 原骨拓藏：`北圖`；
- 重见、拼合和备注栏为空。

数据库凡例说明，合集号是图版编号，每个编号对应一件甲骨实物；数据以
1999 年印行的《甲骨文合集材料來源表》为基础。响应为 2,337 字节，
SHA-256 为英文部分所列值。

CiNii Books 书目记录 `BN05177578` 把《合集》2 定位在第 1 册、第一期；
该册范围为图版 1-1139，并报告第 1 册第一次印刷为 1982 年 10 月。本次
没有取得图版 2 所在的印刷叶码。因此稳定定位应写成“第 1 册、第一期、
图版 2”，不得编造页码。

### 已发表同文证据

刘影《宾组牛胛骨新缀四组》发表于《故宫博物院院刊》2011 年第 1 期、
总第 153 期，第 22-27 页。本次已打开并渲染故宫官方第 22、23 页 PDF。

论文第 23 页明确称《合集》2、《合集》5 等为同文卜辞，并把相关材料归入
宾组。但该页没有刊出《合集》2，而是刊出《合集》1 与《合补》657 的另组
缀合，并借同文卜辞拟补更长文本。

该页印刷文本可支持次序 0、2-5 的字面顺序：`曰`、`田`、`其`、`受`、
`年`，随后是月份语句。但 `曰` 与 `田` 之间的字形，本档不能证明就是
OBIMD 检索路线 `協`。次序 1 仍未解决，不提供互证；在没有复核释读前，
也不判成反证。月份语句也不能证明次序 6 覆盖一个字、多个痕迹还是残损。

故宫两页官方 PDF 均留在忽略区。第 22 页为 644,706 字节，第 23 页为
616,833 字节；SHA-256、对象内下载编号、忽略路径和页面 URL 见同目录
JSON。公开 Git 只保存定位、checksum、适用范围、权利风险与裁决，不复制
论文页面。

### 来源家族分析

这些证据不能全部按独立来源计数：

1. OBIMD `data.json`、子字到主字映射和 `Main-character.json` 属于同一
   数据集家族；三者相合只证明内部路线，不证明释读。
2. 国家图书馆文章提供国图 14427 /《合集》2 的机构身份及来源报告残辞。
3. 刘影 2011 提供同文论证和宾组语境，但较长文本来自另一件缀合对象。
4. 小學堂提供 1999 年材料来源表的著录路线；本次响应没有释文或图版图像。

国图与小學堂都继承《合集》著录传统。它们是不同访问和机构路线，但不能
直接当作完全独立的古文字释读。

### 命题门槛裁决

- `C1`：对象身份为 `candidate_route`；正式提升仍扣留。
- `C2`：本地拓片与摹本已 `direct_checked`，有 checksum、尺寸、字框和
  逐框中性观察。
- `C4`：`candidate_route`。字框和顺序为 `direct_checked`；国图残辞及
  刘影页面是已打开的来源文本证据；H2 全文明确限界缺失，宾组归属仍为
  `source_reported`。
- `C5`：`blocked`。这些形式仍是来源元数据，其中含次序 1 异值集和次序 6
  粒度警告；尚未形成完整释读史、替代说、分歧和反例证据。
- `C6`：因 C5 阻断而 `blocked`；不得给出语义概率。
- `C7`：`not_applicable_no_diachronic_proposition`，本档未提出历时命题。
- `C8`：交付为 `withhold`，动作为 `abstain`。尚无任务级校准、干净
  留出集和完整 C5-C6 证据。

因此，本阶段交付的是“可证伪的来源元数据对齐候选 + 明确释读弃权”，不显示
任何数值概率。

### 主张记录合同

裁决版本：`2026-08-30-h2-text-scope-v1`。

稳定裁决路径：
`11_text-scope-and-box-alignment-adjudication.md#claim-recording-contract`。

各门槛状态、证据编号和阻断影响以英文清单为规范副本：C1 为
`candidate_route`，C2 为 `direct_checked`，C3 为
`not_asserted_not_applicable`，C4 为 `candidate_route`，C5、C6 均为
`blocked`，C7 为 `not_applicable_no_diachronic_proposition`，C8 为
`withhold`，动作是 `abstain`。

稳定来源家族为 `family-obimd-derived`、
`family-nlc-heji-publication`、`family-liu-2011-same-text` 和
`family-xxt-1999-heji-table`。公开聚合页另属
`family-public-aggregator-quality-control`，只作负向质量控制。OBIMD
图像路线直接继承殷契文渊；国图、小學堂和刘影论文又共享《合集》著录、
图像或文本传统，不能盲目计成多个独立古文字释读见证。

最强替代解释是：共享《合集》著录或图像祖先，或尚未发现的映射、版本
错误，使多个路线重复同一错误身份。阻断项是尚未取得权利允许核验的
《合集》第 1 册图版 2。下一来源就是该图版及相邻印刷定位。交付继续
`withhold`，动作继续 `abstain`。

### 最强替代解释与证伪条件

最强替代解释是：OBIMD 层级把若干字形或短语状片段规范到一个主字 UID；
次序 6 已提供这种可能性的内部警告。只有次序相合，不能排除切框或规范化
错误。

出现下列任一证据时必须重开：

- 打开的《合集》2 印刷图版与当前 H2 对象不一致；
- 带图版的版本给出不同的行序或字框次序；
- 某框实际覆盖残损、界划或多个字，而不是一个字；
- 版本级释文与次序 0-5 中任一项不合；
- 经复核来源把第 6 框识别为与月份残文预期不同的内容。

下一项最高价值来源，是权利允许的《合集》第 1 册图版 2 扫描件或实体书。
应把它与 H2 图像并排核对，不能用聚合站图片替代。
