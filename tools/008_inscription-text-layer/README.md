# Inscription Text Layer Tools / 卜辞释文层工具

简体中文：
这两个脚本从已登记的 OBIMD 标注文件重建卜辞释文层，并把例句和分布写进
单字档案。它们是架构重置第 4 步的实现，见
`doc/project/007_architecture-reset-and-human-first-knowledge-base/`。

English:
These scripts rebuild the inscription text layer from the registered OBIMD
annotation file and attach examples and distribution to character dossiers.

## 输入 / Inputs

- `external_local_archive/source_packages/obimd/data.json`：OBIMD 原始标注，
  登记为 `large-src-000002` / `pkg-file-000005`，本地保存，不进 Git。
- `corpus/001_oracle-characters/000_character-registers/006_obimd-main-character-staging.csv`：
  主字形 UID 到隶定字的对照。
- 单字档案 `record.json` 中的 `cross_source_codepoint.obimd_main_uids`，
  由 HUST-OBC 官方标签与 OBIMD 隶定字对照得到。

## 输出 / Outputs

| 位置 | 内容 | 是否公开 |
| --- | --- | --- |
| `external_local_archive/derived/obimd-inscriptions/inscriptions.jsonl` | 21,941 个句组的完整释文、字框和阅读顺序 | 否，本地研究用 |
| `external_local_archive/derived/obimd-inscriptions/plates-*.md` | 按千片分卷的人读释文表 | 否 |
| `corpus/002_oracle-bone-inscriptions/010_inscription-texts/001_obimd-plate-index.csv` | 每片甲骨的句组数、字数、未识别字数 | 是，只有统计 |
| `corpus/002_oracle-bone-inscriptions/010_inscription-texts/002_obimd-glyph-occurrence-stats.csv` | 每个字形的出现次数、片数、句组类别、高频共现字 | 是，只有统计 |
| 单字档案第 4、5 节 | 每字最多 2 条例句、其余片号、分布 | 是，少量引用 |

## 权利 / Rights

OBIMD 当前有效权利状态为 `metadata_only_until_verified`。按用户
2026-11-02 的决定，OBIMD 只在本地用于个人研究；公开仓库只放编号、统计和
每字最多 2 条带出处的例句。不要把 `inscriptions.jsonl` 或分卷释文提交到
Git。

OBIMD stays local for personal research. The public repository carries only
identifiers, statistics, and at most two cited examples per dossier.

## 运行 / Run

```powershell
python tools/008_inscription-text-layer/build_obimd_inscription_text_layer.py
python tools/008_inscription-text-layer/attach_obimd_evidence_to_dossiers.py
```

## 已知限制 / Known Limits

- OBIMD 片号 `H` 后的数字推定为《合集》号，尚未逐片核对（见案件
  `case-h2-heji2`）。
- OBIMD 没有分期和组类字段。
- 23,927 个字例没有字形标签，显示为 □；688 个字形没有标准 Unicode 码位，
  显示为 ◇，原码位保留在本地 `inscriptions.jsonl`。
- 例句中的字是 OBIMD 的隶定，不是本项目的复核释读。
