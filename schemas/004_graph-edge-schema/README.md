# Graph Edge Schema / 图谱边 Schema

English:
Use this schema area for graph edges connecting characters, components, inscriptions, sources, places, periods, topics, and hypotheses.

简体中文：
本目录用于连接甲骨字、构件、卜辞、来源、地点、时代、主题和假说的图谱边。

## Confidence boundary / 置信度边界

`confidence_level` is retained for compatibility with existing graph files.
It describes route or metadata integrity only. It is never a decipherment
probability.

`route_integrity_confidence` is the preferred explicit route field. A future
`hypothesis_probability` must be a number from 0 to 1 produced by a
task-specific calibrated report. The graph must also carry
`hypothesis_probability_status` and, when calibrated, a
`hypothesis_calibration_ref`.

`uncalibrated_score`, model self-confidence, image similarity, or agreement
among dependent agents must not be written as `hypothesis_probability`.

`confidence_level` 为兼容现有图边而保留，只描述路线或 metadata 完整性，
不是释读概率。

`route_integrity_confidence` 是推荐使用的明确路线字段。未来的
`hypothesis_probability` 只能是 0 到 1 之间、由任务级校准报告产生的数值。
图边还必须带 `hypothesis_probability_status`；校准状态必须带
`hypothesis_calibration_ref`。

`uncalibrated_score`、模型自评置信度、图像相似度或有依赖 Agent 的一致意见，
都不能写入 `hypothesis_probability`。
