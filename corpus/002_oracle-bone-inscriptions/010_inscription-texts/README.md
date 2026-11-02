# Inscription Texts / 卜辞释文层

简体中文：
本目录是卜辞释文层的公开部分。完整释文来自 OBIMD，只保存在本地忽略区
`external_local_archive/derived/obimd-inscriptions/`，这里只放统计表。
生成方法见 `tools/008_inscription-text-layer/README.md`。

English:
This directory is the public part of the inscription text layer. The full
OBIMD transcriptions stay in the ignored local archive; only statistics are
committed here.

## 规模 / Scale

| 项目 | 数量 |
| --- | --- |
| OBIMD 甲骨片 | 10,077 |
| 句组 | 21,941（卜辞句 17,150，兆序 3,785，验辞 407，未定 599） |
| 字例 | 115,319 |
| 无字形标签的字例（□） | 23,927 |
| 出现过的字形 | 1,730，其中 688 个没有标准 Unicode 码位 |

## 文件 / Files

- `001_obimd-plate-index.csv`：每片甲骨的句组数、字例数、未识别字数和句组
  类别。`heji_number_candidate` 只是从片号推出的候选《合集》号。
- `002_obimd-glyph-occurrence-stats.csv`：每个字形的出现次数、所在片数、
  各类句组中的次数，以及同一句组中最常一起出现的 8 个字。

## 用法提醒 / Caution

统计只说明 OBIMD 标注里的分布，不说明释读正确。字形相同与否、分期分组、
辞例类型都要回到拓片和著录核对。

These statistics describe OBIMD annotations; they do not validate readings.
