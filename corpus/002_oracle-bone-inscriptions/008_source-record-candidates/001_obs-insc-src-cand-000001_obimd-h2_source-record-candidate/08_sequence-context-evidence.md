# H2 Sequence And Group Context Evidence
# H2 逐项与句组上下文证据

Review dates / 复核日期: 2026-08-13, 2026-08-28, 2026-08-30

## English

### What was recomputed

The ignored source package
`external_local_archive/source_packages/obimd/data.json` was parsed directly.
Its SHA-256 is
`b504b0d4e7a0126d494c161f5445c5ee4225659ff5e94182685fce35d261aa19`.
Exactly one row has `RubbingName = H2`.

That row contains one group, `InscriptionSentence1`, and seven occurrence
objects. The source serialization order is `5, 0, 1, 2, 3, 6, 4`.
After sorting by the author-defined `OrderNumber` field, the source-defined
annotation order is `0, 1, 2, 3, 4, 5, 6`.

This difference matters. Array order must not be mistaken for reading order.
The Label sequence is not a transcription. It is a sequence of opaque source
UIDs ordered by an OBIMD annotation field.

### Seven ordered source occurrences

#### Order 0

- Label and SubLabel: `9xhq4zclpe`
- Position `(x,y,w,h)`: `824,483,94,88`
- SeatFont: `0`; Mark: `-1`
- Candidate route: `obs-comp-cand-001085`

#### Order 1

- Label and SubLabel: `ve0ebxq620`
- Position `(x,y,w,h)`: `797,583,143,161`
- SeatFont: `0`; Mark: `-1`
- Candidate route: `obs-comp-cand-002229`

#### Order 2

- Label and SubLabel: `pzvzykmf5e`
- Position `(x,y,w,h)`: `829,769,46,67`
- SeatFont: `0`; Mark: `-1`
- Candidate route: `obs-comp-cand-001781`

#### Order 3

- Label and SubLabel: `qmvfvw99v9`
- Position `(x,y,w,h)`: `526,137,150,151`
- SeatFont: `0`; Mark: `-1`
- Candidate route: `obs-comp-cand-001998`

#### Order 4

- Label and SubLabel: `52a130pcmy`
- Position `(x,y,w,h)`: `508,332,135,214`
- SeatFont: `0`; Mark: `-1`
- Candidate route: `obs-comp-cand-001929`

#### Order 5

- Label and SubLabel: `xkubtjk815`
- Position `(x,y,w,h)`: `558,581,80,218`
- SeatFont: `0`; Mark: `-1`
- Candidate route: `obs-comp-cand-000275`

#### Order 6

- Label and SubLabel: `lstx3iocs6`
- Position `(x,y,w,h)`: `572,846,125,97`
- SeatFont: `0`; Mark: `-1`
- Candidate route: `obs-comp-cand-002627`

Every UID has exactly one current directory route under
`corpus/003_graphemic-components/`. The component main-staging table also maps
each UID to the same UID as its OBIMD main-character UID. Those rows remain
`dataset_candidate_not_promoted`.
UID route does not confirm a character identity, component status, modern
character, or reading.

### Field semantics from the official paper

The version-of-record paper at
`https://doi.org/10.1038/s41597-026-06967-0` describes these fields in
`Data Records` and final Table 2. These meanings are author-reported:

- `GroupCategory` is a dataset group classification, not a final grammatical
  analysis. Here its value is `InscriptionSentence1`.
- `Position` is an image bounding box, not a findspot or object location.
- `OrderNumber` is annotated order within a group.
- `Label` and `SubLabel` are two-level external glyph-library UIDs. Here every
  SubLabel equals Label; equality does not supply a reading.
- `SeatFont = 1` denotes an expected but missing position. All seven H2 rows
  have `SeatFont = 0`, so none is source-flagged with that placeholder code.
- `Mark = -1` is the regular default. All seven rows have this value. It does
  not certify an identification or settle a scholarly dispute.

The paper reports a tri-modal annotation workflow, but the public H2 row does
not contain readable transcription text. Therefore its ordered UID sequence
cannot be rewritten as a sentence or cited as an edition of the inscription.

The OBIMD hierarchy maps the seven subcharacter UIDs to main-character UIDs.
`Main-character.json` then reports lookup routes for orders 0-5 as `曰`,
`協`, `田`, `其`, `受`, and `年`. Order 6 has glyph codepoint PUA
`U+FFB45` and platform reference `十一月`. These are same-family lookup
metadata, not an independent transcription or accepted reading. The full
adjudication is in
`11_text-scope-and-box-alignment-adjudication.md`.

### Spatial context, without image republication

The boxes fit within the registered 1022 by 1180 source image. Orders 0–2 lie
in a right-side band around x 797–829. Orders 3–6 lie in a left-side band
around x 508–572. Within each band, y increases with `OrderNumber`.

The jump from order 2 to order 3 moves from the lower right band to the upper
left band. This is a reproducible coordinate observation, not a claim about
historical line direction, sentence syntax, joins, or missing signs. Such a
claim requires visual inspection and an independent transcription edition.

### Catalog and text access boundary

The safe institutional route is recorded in
`07_identifier-crosswalk-investigation.md`. On 2026-08-12 the public search
showed candidate record `合2`, system ID `108548`; its detail endpoint returned
`Code=406` and required login. No login was bypassed. No official
transcription, page, plate, collection record, or archaeological metadata was
obtained from that route. H2 remains an inscription source-record candidate.

### Falsifiable next checks

1. Obtain a rights-permitted transcription edition and test whether it has
   seven positions corresponding one-to-one with orders 0–6. A different
   count or order falsifies the simple one-box-per-written-sign model.
2. Obtain an official row-level mapping between OBIMD `H2` and `合2`. A mapping
   to another catalog record falsifies the current visual crosswalk candidate.
3. Open both local private modalities under the recorded rights conditions.
   Test each bounding box against the rubbing and facsimile; a box outside or
   covering no sign falsifies the corresponding occurrence route.
4. Compare the two spatial bands with an edition that marks line order. A
   conflicting line order falsifies any provisional right-band-first model.
5. For each UID, compare the boxed sign with its candidate dossier assets.
   A shape mismatch falsifies that UID-to-occurrence route; a match still does
   not confirm a reading.
6. Open Heji volume 1, first period, plate 2 and identify its printed leaf or
   page. Failure of the registered image to match that plate falsifies the
   proposed catalog link.

## 简体中文

### 已复算内容

本次直接解析忽略区 `data.json`，其 SHA-256 见英文部分。`RubbingName = H2`
只命中一行。该行只有一个 `InscriptionSentence1` 组和七个 occurrence 对象。

源数组物理顺序是 `5, 0, 1, 2, 3, 6, 4`；按 `OrderNumber` 排序后，标注顺序是
`0, 1, 2, 3, 4, 5, 6`。因此不能把数组物理顺序当作阅读顺序。
来源标签序列不是释文，而是按 OBIMD 标注字段排列的不透明 UID 序列。

### 七项逐项证据

七项的 UID、坐标、`SeatFont`、`Mark` 和候选路线完整列在英文部分，也逐字段写入
`91_character-occurrence-index.csv`。真实源行复算结果与该索引完全一致。

七个 UID 都唯一路由到 `corpus/003_graphemic-components/` 下的现有候选对象。
OBIMD main staging 也把每个 UID 路由到同名 main-character UID，但状态仍是
`dataset_candidate_not_promoted`。UID 路由不确认单字身份、构件地位、今字或释读。

### 官方论文字段语义

正式版论文 `Data Records` 和最终表 2 报告：

- `GroupCategory` 是数据集分组，不是最终语法分析。
- `Position` 是图像框坐标，不是出土地或实物位置。
- `OrderNumber` 是组内标注顺序。
- `Label` 与 `SubLabel` 是两级外部字形库 UID。本行中 SubLabel equals Label，
  但相等关系不提供释读。
- `SeatFont = 1` 表示预期有字但缺失的占位。H2 七项都是 `SeatFont = 0`，
  即来源没有用该占位代码标记它们。
- `Mark = -1` 是常规默认值。H2 七项都如此，但这不认证身份，也不裁决争议。

公开 H2 行没有可读释文文本。因此不能把有序 UID 串改写成一句卜辞，也不能把它
当作任何释文版本引用。

OBIMD 层级文件先把七个子字 UID 路由到主字 UID；`Main-character.json`
再为次序 0-5 报告 `曰`、`協`、`田`、`其`、`受`、`年` 检索路线。
次序 6 的字形码位为 PUA `U+FFB45`，平台参考今字值为 `十一月`。它们
属于同一数据集家族的检索元数据，不是独立释文或已接受释读。完整裁决见
`11_text-scope-and-box-alignment-adjudication.md`。

### 空间上下文与边界

所有框都在已登记的 1022×1180 图像范围内。顺序 0–2 位于右侧 x 797–829 带，
顺序 3–6 位于左侧 x 508–572 带；各带内部 y 随顺序增加。顺序 2 到 3 从右下带
跳到左上带。这只是可复算的坐标观察，不证明行款方向、句法、缀合或缺字。

2026-08-12，安全公开路线显示候选 `合2`、系统 ID `108548`，但详情接口返回
`Code=406` 并要求登录。本次没有绕过登录，也没有取得官方释文、页码、图版、
馆藏或考古字段。H2 仍是卜辞来源记录候选。

### 具体可证伪的下一步

1. 取得权利允许的释文版本，检验是否恰有七个位置与顺序 0–6 一一对应；计数或
   顺序不同即可否定“每框对应一个书写单位”的简单模型。
2. 取得 OBIMD `H2` 与 `合2` 的官方逐条映射；若指向其他著录，即否定当前视觉
   互证候选。
3. 在既定权利条件下同时打开本地私有拓片和摹本，逐框检查；若框越界或未覆盖
   字形，即否定对应 occurrence 路由。
4. 用标明行序的独立释文版本核对左右两带；若行序冲突，即否定任何“右带优先”
   的临时模型。
5. 逐 UID 对照候选档案资产；形态不符即可否定该 UID 路由，形态相符仍不确认
   释读。
6. 打开《合集》第 1 册、第一期、图版 2，并查明印刷叶码或页码；若登记
   图像与该图版不符，即否定当前著录联系。

Rights / 权利: `metadata_only_until_verified`.
Review / 复核: `source_context_recomputed_candidate_identity_unconfirmed`.
