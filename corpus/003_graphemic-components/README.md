# Graphemic Components / 字形构件

简体中文：
本区保存字形构件资料。目前只有 OBIMD 数据集的子字形登记和视觉观察，
尚无经复核的构件归属。

English:
This area holds graphemic-component material. It currently contains only
OBIMD sub-character registers and visual observations; no component
assignment has been reviewed.

## 登记表 / Registers

| 文件 | 内容 |
| --- | --- |
| `000_component-registers/002_obimd-subcharacter-main-staging.csv` | OBIMD 2,747 个子字形与主字形的对应 |
| `000_component-registers/003_obimd-subcharacter-glyph-staging.csv` | 子字形与字形码位对应 |
| `000_component-registers/004_obimd-component-visual-observations.csv` | 2,743 条视觉观察：描述性观察与像素画像两类，带资产 ID 与校验和 |

每个 `obs-comp-cand-*` ID 对应登记表中的一行，映射见
`project_registry/002_project-id-to-source-reference-map/`
`004_component-id-source-map.csv`。

## 图片位置与权利 / Images And Rights

OBIMD 当前有效权利状态为 `metadata_only_until_verified`。按用户
2026-11-02 的决定，OBIMD 用于个人本地研究，公开仓库不再分发其图片。
10,364 张子字形图片已移到本地忽略区
`external_local_archive/obimd-component-images/`，资产索引中的路径已同步
更新。克隆本仓库的其他人需要自行从 OBIMD 来源获取图片。

OBIMD's effective rights status is `metadata_only_until_verified`. Its
10,364 sub-character images were moved to the ignored local archive; the
public repository no longer redistributes them.

## 2026-11-02 折叠 / Collapse

按[架构重置][reset]第 2 步，原来 2,747 个构件对象目录（约 7 万个文件）
已折叠回上面的登记表。唯一的对象特有内容是视觉观察，已完整写入
`004_obimd-component-visual-observations.csv`。旧目录可从提交
`4a0fb8acf25` 恢复。

The 2,747 generated directories were collapsed into the registers; their
only object-specific content, the visual observations, is preserved in the
observation register.

[reset]: ../../doc/project/007_architecture-reset-and-human-first-knowledge-base/
