# Relationship Graph / 关系图谱

简体中文：
本目录保存甲骨文对象之间的关系边。2026-11-02 起，研究用的是
`100_scholarly-graph/` 中的学术关系边；其余旧文件是早期生成的"路线边"，
只描述文件之间的引用路线，保留作历史记录。

English:
Since 2026-11-02 the research graph is `100_scholarly-graph/`. The older files
are route edges between files, kept for history.

## 学术关系图谱 / Scholarly Graph

由 `tools/009_scholarly-graph/build_scholarly_graph.py` 生成。每条边都带
`source_ref`（来源行或文献定位）、`status` 和 `note`。

| 边类型 | 含义 | 数量 | 状态 |
| --- | --- | --- | --- |
| `dataset_label` | HUST-OBC 已释类 → 官方对照表中的字 | 1,774 | `source_reported` |
| `same_character_candidate` | 单字档案 → OBIMD 字形或 EvoBC 类别（隶定或标签相同） | 3,099 | `candidate` |
| `catalog_clue` | 单字档案 → 样本文件名中的合集号 | 725 | `filename_clue` |
| `co_occurs` | OBIMD 字形 ↔ 字形，同一句组中共现 5 次及以上 | 7,878 | `source_derived_count` |
| `occurs_in` | OBIMD 字形 → 甲骨片句组与字位 | 91,459 | 只在本地 |

`occurs_in` 边逐字记录位置，合起来就能还原 OBIMD 全文，所以按 OBIMD 权利
状态只写到本地忽略区 `external_local_archive/derived/graph/`。

`same_character_candidate` 只表示两个数据集把字隶定或标注为同一个现代字，
不说明字形相同，也不说明释读正确。

## 已删除的旧边 / Removed Legacy Edges

`005_hust-obc-candidate-graph-edges.jsonl` 与
`010_cross-source-id-graph-edges.jsonl` 建立在错误的 HUST-OBC 标签上
（见 `corpus/001_oracle-characters/000_character-registers/README.md`
"标签更正"一节），2026-11-02 已删除，可从提交 `9a37cb9774c` 恢复。

## 旧路线边 / Legacy Route Edges

`004`、`006`--`009`、`011`--`017` 是早期生成的路线边，描述单字、图片、
构件、来源和对照候选之间的文件路线。其中的路径可能指向已折叠的目录。
它们不是学术关系，研究时请用 `100_scholarly-graph/`。

Files `004`, `006`--`009`, and `011`--`017` are legacy route edges whose paths
may point to collapsed directories.

## Confidence boundary / 置信度边界

`confidence_level` in existing files is route metadata, not a probability.
Use `route_integrity_confidence` for source binding and evidence-route quality.
Use `hypothesis_probability` only for a task-calibrated candidate, together
with `hypothesis_probability_status` and its calibration reference.

现有图边中的 `confidence_level` 只是路线 metadata，不是概率。
来源绑定和证据路线质量使用 `route_integrity_confidence`。只有任务级校准
后的候选才可使用 `hypothesis_probability`，并同时记录状态和校准引用。

## OBIMD Rights Resolution / OBIMD 权利状态解析

The OBIMD staging tables and older graph edges may preserve the historical
source-declared value `licensed_for_repository`. That value is retained for
provenance comparison only. It is not a redistribution grant and must not be
used as the current publication decision.

OBIMD graph consumers must resolve the effective status through the active
[OBIMD rights resolution note](obimd-rights-resolution.md), which points to
the override ledger and the source-object decision.

The effective status is `metadata_only_until_verified`; the current public
decision is no public redistribution or derivative promotion until the
conflicting terms are reconciled. This applies to component, variant, asset,
and package routes. A graph edge remains a candidate review route and cannot
authorize copying an image, raw package, or derived asset.

OBIMD staging 表和较早的图边可能保留来源历史字段
`licensed_for_repository`。该字段只用于来源对照，不是再分发许可，
也不能当作当前公开发布决定。

所有 OBIMD 图谱使用者都必须通过
[OBIMD 权利解析说明](obimd-rights-resolution.md)解析当前状态；该说明
再指向覆盖表和来源对象决定页。

当前有效状态是 `metadata_only_until_verified`；在冲突条款完成对账前，
不得公开再分发或提升派生件。该规则适用于构件、异体、资产和来源包路线。
图边仍只是候选复核路线，不能授权复制图像、原始包或派生资产。
