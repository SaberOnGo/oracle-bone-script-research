# Bronze, Seal, And Modern Correspondences / 金文、小篆与今字对应

简体中文：
本区保存跨时期字形比较资料：甲骨文、金文、小篆、后世字形和今字码位。
目前只有 EvoBC 数据集的类别登记，尚无经复核的字形演化链。

English:
This area holds cross-period form-comparison material. It currently contains
only the EvoBC category register; no reviewed evolution chain exists yet.

## 登记表 / Registers

| 文件 | 内容 |
| --- | --- |
| `000_evolution-registers/001_evobc-evolution-category-staging.csv` | EvoBC 13,714 个类别：数据集今字标签、码位、各时期图片数、来源代码计数 |
| `000_evolution-registers/002_evobc-era-source-codebook-staging.csv` | EvoBC 时期与来源代码表 |

每个 `obs-evo-cand-*` ID 对应登记表中的一行，映射见
`project_registry/002_project-id-to-source-reference-map/`
`005_evolution-candidate-id-source-map.csv`。

## 2026-11-02 折叠 / Collapse

按[架构重置][reset]第 2 步，原来 13,714 个 `obs-evo-cand-*` 对象目录
（约 22 万个文件）已折叠回上面的登记表。这些目录没有本地图片，内容
只是登记表同一行数据的重复展示和固定模板，需要时可从提交
`4a0fb8acf25` 恢复。

Per step 2 of the [architecture reset][reset], 13,714 generated directories
were collapsed back into the register above. They held no local images and
only repeated the same register row; they remain recoverable from commit
`4a0fb8acf25`.

## 使用提醒 / Caution

EvoBC 的今字标签和时期分组是数据集标注，不是经复核的字形对应。只有在
打开具体字形图、确认时期来源并有文献依据后，才能在单字档案的"后世
字形"一节写入对应关系。

EvoBC modern labels and era groupings are dataset annotations, not reviewed
correspondences.

[reset]: ../../doc/project/007_architecture-reset-and-human-first-knowledge-base/
