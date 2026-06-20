# Cambridge/Hopkins Topic Materials Builder / Cambridge/Hopkins 主题材料生成器

English:
`build_cambridge_hopkins_topic_materials.py` converts the Cambridge/Hopkins classified-table summary and inscription crosswalk staging rows into object-local topic candidate materials under `corpus/007_research-topics-and-grammar/`.

简体中文：
`build_cambridge_hopkins_topic_materials.py` 会把 Cambridge/Hopkins 分类表摘要和卜辞 crosswalk staging 行转换为 `corpus/007_research-topics-and-grammar/` 下的对象内主题候选材料。

## Command / 命令

```powershell
python tools/002_corpus-import/build_cambridge_hopkins_topic_materials.py --root .
```

## Outputs / 输出

- `corpus/007_research-topics-and-grammar/000_topic-registers/001_cambridge-hopkins-topic-candidate-index.csv`
- `corpus/007_research-topics-and-grammar/000_topic-registers/002_cambridge-hopkins-topic-crosswalk-link-staging.csv`
- `corpus/007_research-topics-and-grammar/000_topic-registers/003_cambridge-hopkins-unrouted-crosswalk-staging.csv`
- `corpus/007_research-topics-and-grammar/001_topic-candidates/*/README.md`
- `corpus/007_research-topics-and-grammar/001_topic-candidates/*/01_topic-candidate-packet.json`
- `corpus/007_research-topics-and-grammar/001_topic-candidates/*/02_topic-source-index.csv`
- `corpus/007_research-topics-and-grammar/001_topic-candidates/*/03_period-count-index.csv`
- `corpus/007_research-topics-and-grammar/001_topic-candidates/*/04_inscription-crosswalk-route-index.csv`
- `corpus/007_research-topics-and-grammar/001_topic-candidates/*/05_human-topic-review-sheet.md`

## Boundary / 边界

English:
The generated records are source-classification candidates and review routes only. They are not grammar analyses, accepted inscription-topic assignments, transcriptions, readings, or decipherment conclusions.

简体中文：
生成记录只是来源分类候选和复核路线。它们不是语法分析、已接受的卜辞主题归属、释文、读法或破译结论。
