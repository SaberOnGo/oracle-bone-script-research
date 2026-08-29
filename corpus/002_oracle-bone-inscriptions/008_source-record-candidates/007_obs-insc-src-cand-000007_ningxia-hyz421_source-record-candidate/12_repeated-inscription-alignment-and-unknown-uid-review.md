# Repeated inscription alignment and unknown UID review
# 重复卜辞对齐与未知 UID 复核

## Result / 结果

The checksum-bound OBIMD `HD421` row contains two inscription groups of
twelve boxes each. Sorting both groups by `OrderNumber` gives the same Label
and SubLabel sequence at every order. This is direct evidence for a repeated
dataset sequence, not two independent readings.

带校验和的 OBIMD `HD421` 行含两个各十二框的卜辞组。按 `OrderNumber`
排序后，两组每一次序的 Label 与 SubLabel 都相同。这直接证明数据集中存在
重复序列，但不是两份独立释读证据。

Schwartz 2019 prints two entries, `421.1` and `421.2`, with the same wording
and different crack-sequence marks. The OBIMD structure is compatible with
that report. The opened evidence does not identify which OBIMD sentence group
is `421.1` or `421.2`, so the one-to-one numbering is withheld.

Schwartz 2019 印有 `421.1`、`421.2` 两条，正文相同而兆序标记不同。
OBIMD 结构与此相容，但已打开证据不能确定哪个句组对应 `421.1` 或
`421.2`，因此暂不建立一一编号。

## Reproducible source receipt / 可复跑来源回执

- source: `external_local_archive/source_packages/obimd/data.json`;
- source SHA-256: recorded by the OBIMD source package as
  `b504b0d4e7a0126d494c161f5445c5ee4225659ff5e94182685fce35d261aa19`;
- exact condition: one row has `RubbingName=HD421`;
- zero-based array index: `10039`;
- groups: two 12-box inscription groups, one two-box oracle-sequence group,
  and one one-box oracle-sequence group;
- rights override: `metadata_only_until_verified`;
- detailed mirror: `93_obimd-hd421-occurrence-index.csv`;
- paired mirror: `94_repeated-sentence-pair-index.csv`.

- 来源：`external_local_archive/source_packages/obimd/data.json`；
- 来源包登记 SHA-256 同上；
- 精确条件：只有一行 `RubbingName=HD421`；
- 数组零起始索引：`10039`；
- 分组：两个十二框卜辞组、一个二框兆序组、一个一框兆序组；
- 权利覆盖：`metadata_only_until_verified`；
- 逐框辅助表：`93_obimd-hd421-occurrence-index.csv`；
- 成对辅助表：`94_repeated-sentence-pair-index.csv`。

## Ordered sentence sequence / 句组次序

The shared Label order is:

0. `oesivb520y`
1. `4lgdy5a4ta`
2. `0wfbo7ml5k`
3. `h0gzv3styy`
4. `qmvfvw99v9`
5. `f0j9ho8ua2`
6. `nms96pmn1w`, SubLabel `66js7x9h0l`
7. `jrzjjh3g1r`
8. `jjm889wxay`
9. `60kr6bp9hf`
10. `1k9ogi7w79`
11. `353gxm6hd4`

This order is dataset routing metadata. It is not a project transcription,
Unicode normalization, modern-character mapping, or sentence analysis.

以上次序只是数据集检索元数据，不是项目摹写、Unicode 规范化、今字对应或
句法分析。

## Unknown UID review / 未知 UID 复核

Order 6 uses main UID `nms96pmn1w` and SubLabel `66js7x9h0l` in both groups.
The project has a lookup route to `obs-comp-cand-000329`. Source metadata also
reports code-point strings `U+BDC20;U+F1E8D`. These are source-reported lookup
fields only.

次序 6 在两组中都使用主 UID `nms96pmn1w` 和 SubLabel `66js7x9h0l`。
项目可检索到 `obs-comp-cand-000329`。来源元数据另报
`U+BDC20;U+F1E8D`，这些都只是来源报告的检索字段。

Order 9 uses `60kr6bp9hf` as both Label and SubLabel in both groups. The
project has a lookup route to `obs-comp-cand-000671`. Source metadata reports
`U+2BEE8;U+F3DD7`. This does not confirm a character, component, or reading.

次序 9 在两组中都以 `60kr6bp9hf` 作为 Label 与 SubLabel。项目可检索到
`obs-comp-cand-000671`。来源元数据报告 `U+2BEE8;U+F3DD7`，但这不确认
单字、构件或释读。

Older component registers contain `licensed_for_repository`. The effective
OBIMD rights override is now `metadata_only_until_verified`; the older value
must not be treated as current reuse permission.

旧组件登记中可见 `licensed_for_repository`。当前有效的 OBIMD 权利覆盖是
`metadata_only_until_verified`，旧值不能当作现行再利用授权。

Neither UID may be inferred from the Commons string or Schwartz translation
as a project reading. Such back-solving would reuse the same textual family
and would not be independent corroboration.

不得根据 Commons 字符串或 Schwartz 译文反推这两个 UID 的项目释读；这种
反推仍复用同一文字来源家族，不能形成独立互证。

## Oracle-sequence adjacency / 兆序邻接

`OracleSequence1` has two boxes and is spatially near
`InscriptionSentence1`. `OracleSequence2` has one box and is spatially near
`InscriptionSentence2`. This supports an adjacency candidate only. It does
not assign either sentence to edition number `421.1` or `421.2`.

`OracleSequence1` 有两个框，空间上邻近 `InscriptionSentence1`；
`OracleSequence2` 有一个框，空间上邻近 `InscriptionSentence2`。这只支持
邻接候选，不把任一句组指定为版本号 `421.1` 或 `421.2`。

## Evidence ancestry / 证据祖先

The OBIMD row, boxes, UIDs, rubbing, and facsimile are one OBIMD-derived
family. Schwartz supplies an edition report, while the Commons string cites
that scholarship and is incomplete. Repeated boxes inside one row are not
independent witnesses, and shared-source agreement must not be multiplied.

OBIMD 行、字框、UID、拓片和摹本属于同一 OBIMD 派生家族。Schwartz 提供
版本报告，Commons 字符串引用该研究且内容不完整。同一行内的重复框不是独立
见证，共享来源的一致性不得重复计数。

## Claim-gate decision / 主张门槛裁决

- `C1`: object identity remains `candidate_route`; formal promotion is
  withheld because museum accession and dimension conflict remain open.
- `C2`: `direct_checked` for the 27 source boxes, their order, coordinates,
  labels, SubLabels, SeatFont, and Mark values.
- `C3`: `not_asserted_not_applicable`; no variant or component claim is made.
- `C4`: `candidate_route`; repeated sentence structure and edition context
  are compatible, but group-to-entry numbering remains unresolved.
- `C5`: `blocked`; reading history, disagreements, negative examples, and
  independent form evidence are incomplete.
- `C6`: `blocked` by C5; no translation or semantic probability is allowed.
- `C7`: `not_applicable_no_diachronic_proposition`.
- `C8`: delivery `withhold`; action `abstain`. No numeric probability is
  displayed because there is no task-specific calibration or clean holdout.

- `C1`：对象身份仍为 `candidate_route`；馆藏登记和尺寸冲突未解决，暂不
  正式提升。
- `C2`：二十七个来源框及其次序、坐标、Label、SubLabel、SeatFont 与
  Mark 已 `direct_checked`。
- `C3`：`not_asserted_not_applicable`，不提出异体或构件主张。
- `C4`：`candidate_route`；重复句组结构与版本上下文相容，但组与条目编号
  的对应未决。
- `C5`：`blocked`；释读史、不同意见、负例和独立字形证据不完整。
- `C6`：受 C5 阻断，不允许翻译或语义概率。
- `C7`：`not_applicable_no_diachronic_proposition`。
- `C8`：交付 `withhold`，动作 `abstain`。无任务级校准和干净留出集，
  不显示数值概率。

## Strongest alternative and falsifiers / 最强替代解释与反证

The strongest alternative is that OBIMD duplicated or normalized one source
sequence and that spatial adjacency does not preserve edition numbering.
This would explain the exact UID repetition without proving two correctly
segmented edition entries.

最强替代解释是：OBIMD 复制或规范化了一个来源序列，而空间邻接不保留版本
编号。这能解释 UID 完全重复，却不能证明两个版本条目都被正确切分。

Reopen or reject the alignment if checksum replay changes the unique row,
box count, order, Label, SubLabel, coordinate, SeatFont, or Mark; if a
page-located edition assigns a different sequence; or if an independent
plate review maps either oracle-sequence group differently.

若校验和复跑改变唯一行、框数、次序、Label、SubLabel、坐标、SeatFont 或
Mark，若有逐页版本给出不同序列，或独立图版复核改变兆序组对应，应重开或
否决本对齐。

## Next-source questions / 下一来源问题

1. Which printed plate or source edition supplied OBIMD rubbing plate 383?
2. Can a page-located edition map the two sentence groups to 421.1 and 421.2?
3. Which publications discuss the two unknown UID positions and alternatives?
4. Can an independent image family reproduce all 27 box boundaries?
5. Can a museum record resolve the accession and dimension conflict?

1. OBIMD 拓片图版 383 来自哪个印刷图版或底本？
2. 有逐页定位的版本能否把两句组对应到 421.1 与 421.2？
3. 哪些出版物讨论两个未知 UID 位置及其不同意见？
4. 独立图像家族能否复现二十七个框边界？
5. 馆藏记录能否解决馆藏号和尺寸冲突？

## Boundary / 边界

This dossier delivers a falsifiable metadata alignment and an explicit
reading abstention. It is not a transcription, character assignment,
translation, decipherment, or calibrated probability claim.

本档案交付可证伪的元数据对齐和明确的释读弃权，不是摹写、单字分配、翻译、
破译或经过校准的概率主张。
