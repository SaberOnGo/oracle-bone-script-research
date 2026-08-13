# Field Evidence Guide / 字段证据指南

## Evidence Layers / 证据层

- `Rubbing`: route to a rubbing image, not automatically an original object.
- `Facsimile`: route to a scholarly rendering aligned to the rubbing.
- `RubbingName`: source abbreviation requiring catalog expansion.
- `GroupCategory`: dataset grouping, not a final grammatical analysis.
- `Position`: image coordinate, not archaeological provenience.
- `OrderNumber`: annotated reading order inside a group.
- `Label` and `SubLabel`: external-library UIDs, not Unicode or final readings.
- `SeatFont`: missing-position placeholder indicator.
- `Mark`: exception code, not a resolution record.

- `Rubbing`：拓片图路线，不自动等于原实物。
- `Facsimile`：与拓片对齐的学术摹本路线。
- `RubbingName`：须展开为完整著录的来源简称。
- `GroupCategory`：数据分组，不是最终语法分析。
- `Position`：图像坐标，不是考古出土地。
- `OrderNumber`：组内标注阅读顺序。
- `Label`、`SubLabel`：外部字库 UID，不是 Unicode 或最终释读。
- `SeatFont`：缺字位置占位标志。
- `Mark`：例外代码，不是争议裁决记录。

## SeatFont And Mark / 占位与例外

The journal `Data Records` section reports:

- `SeatFont = 1`: a placeholder for an expected but missing character.
- `Mark = 0`: too damaged for identification even by experts.
- `Mark = 1`: disputed category attribution without consensus.
- `Mark = 2`: visible only in the rubbing.
- `Mark = 3`: visible only in the facsimile.
- `Mark = -1`: regular default.

These meanings are `author-reported`.
A Mark value does not mean the dispute is resolved.
It also does not mean rejection or acceptance.
`Mark` 值不表示争议已经解决、否决或接受。

## Modern Character Reference / 今字参考

The journal says the supplementary JSON provides a platform-supplied modern
character for lookup and explicitly warns that it is not final. Transfer it
only as `source_modern_label_candidate`.

期刊说明补充 JSON 的今字由平台提供，仅便于检索，并非最终解释。转移时
只能标为 `source_modern_label_candidate`。

## Required Object Check / 对象级必查

Before using any field as evidence, open the rubbing, facsimile, transcription
page, catalog expansion, group context, and exception state together.

把任何字段用于证据前，须同时打开拓片、摹本、释文页、完整著录、组内背景
和例外状态。
