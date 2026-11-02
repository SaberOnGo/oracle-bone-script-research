# Scholarly Graph Tools / 学术关系图谱工具

简体中文：
`build_scholarly_graph.py` 生成架构重置第 6 步的学术关系图谱。边类型、
数量和权利处理见 `corpus/008_relationship-graph/README.md`。

English:
`build_scholarly_graph.py` builds the scholarly relationship graph for step 6
of the architecture reset.

## 输入 / Inputs

- 单字档案 `record.json`：官方标签、跨来源同字候选、文件名著录线索。
- 本地 OBIMD 标注 `external_local_archive/source_packages/obimd/data.json`，
  经 `tools/008_inscription-text-layer/` 解析。

## 输出 / Outputs

- `corpus/008_relationship-graph/100_scholarly-graph/000_edge-summary.csv`
- `corpus/008_relationship-graph/100_scholarly-graph/001_character-identity-edges.jsonl`
- `corpus/008_relationship-graph/100_scholarly-graph/002_glyph-cooccurrence-edges.jsonl`
- 本地：`external_local_archive/derived/graph/occurs_in.jsonl`

## 运行 / Run

```powershell
python tools/009_scholarly-graph/build_scholarly_graph.py --min-cooccur 5
```

先运行 `tools/008_inscription-text-layer/` 的两个脚本，再运行本脚本。

Run the two inscription-layer scripts first, then this one.
