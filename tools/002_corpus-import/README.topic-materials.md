# Topic Materials Builder / 主题资料生成器

English:
`build_cambridge_hopkins_topic_materials.py` prepares object-local
materials for Cambridge/Hopkins topic candidate review. It turns the
classified-table summary, inscription crosswalk staging rows, and period
count clues into human-readable review folders first, with JSON and CSV as
AI-readable support.

简体中文：
`build_cambridge_hopkins_topic_materials.py` 为 Cambridge/Hopkins 主题候选
复核准备对象内资料。它先把分类表摘要、卜辞 crosswalk staging 行和时期
计数线索整理成人类可读复核文件夹，再提供 JSON 和 CSV 作为 AI 辅助资料。

## Human Review Entry Order / 人工复核顺序

English:

1. Open the topic candidate README in the object-local materials folder.
2. Check the source route and topic source index before using counts.
3. Compare the period count index with the inscription crosswalk route.
4. Trace linked inscriptions and source objects before trusting labels.
5. Use the packet JSON only after the human review route is clear.

简体中文：

1. 先打开对象内资料文件夹中的 topic candidate README。
2. 使用计数前，先核查 source route 和主题来源索引。
3. 对照 period count index 与 inscription crosswalk route。
4. 信任标签前，追溯关联卜辞和来源对象。
5. 人工复核路线清楚后，再使用 packet JSON。

## Current Inputs And Outputs / 当前输入与输出

English:

- Input: Cambridge/Hopkins classified-table summary staging data.
- Input: inscription crosswalk staging rows and unrouted rows.
- Output: topic candidate folders under the research-topics corpus area.
- Output: topic source index, period count index, and route index.
- Output: human topic review sheet plus AI-readable packet JSON.

简体中文：

- 输入：Cambridge/Hopkins 分类表摘要 staging 数据。
- 输入：卜辞 crosswalk staging 行和暂未路由的行。
- 输出：research-topics 语料区下的 topic candidate 文件夹。
- 输出：主题来源索引、时期计数索引和路线索引。
- 输出：人工主题复核表，以及 AI 可读 packet JSON。

## Concrete Questions To Check / 具体待查问题

English:

- Which Cambridge/Hopkins row produced this topic candidate?
- Which source route and source object should be opened next?
- Which inscription crosswalk rows support this route?
- Are the period count values only source clues, not dating results?
- Which linked inscriptions, source rows, or images are still missing?
- Which unresolved rows must remain unrouted until reviewed?

简体中文：

- 这个 topic candidate 来自哪一条 Cambridge/Hopkins 记录？
- 下一步应该打开哪条 source route 和哪个来源对象？
- 哪些 inscription crosswalk 行支持这条路线？
- period count 数值是否只作为来源线索，而不是断代结果？
- 哪些关联卜辞、来源行或图像仍然缺失？
- 哪些未解决行在复核前必须继续保持 unrouted？

## Research Boundary / 研究边界

English:
The generated records are source-classification candidates and review
routes only. They are not grammar analyses, accepted topic assignments,
transcriptions, readings, dating conclusions, or decipherment conclusions.
They are not a decipherment conclusion.
Each unresolved item must stay marked as candidate, source record,
disputed, to-check, or to-review.

简体中文：
生成记录只是来源分类候选和复核路线。它们不是语法分析、已接受的主题
归属、释文、读法、断代结论或破译结论。它们不是释读结论。
所有未解决项目都必须继续标为候选、来源记录、争议、待查或待复核。

## Command / 命令

```powershell
python tools/002_corpus-import/build_cambridge_hopkins_topic_materials.py `
  --root .
```
