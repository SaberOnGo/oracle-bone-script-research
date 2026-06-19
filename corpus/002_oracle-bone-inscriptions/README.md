# Oracle Bone Inscriptions / 甲骨卜辞

English:
This directory will store full inscription records, context, character sequence indexes, topics, excavation context, and source references.

Current registers:

- `000_inscription-registers/001_all-inscriptions-index.csv`: accepted project inscription records.
- `000_inscription-registers/002_cambridge-hopkins-crosswalk-staging.csv`: Cambridge Hopkins finding-list staging crosswalk with 612 visible `y/c/h/j` reference rows.
- `000_inscription-registers/003_cambridge-hopkins-classified-summary.csv`: Cambridge Hopkins classified table summary with 20 topic groups, official period totals, ancestor subgroups, and grand total.
- `../009_statistics-and-derived-features/098_ai-agent-cambridge-hopkins-inscription-crosswalk-review-queue.csv`: metadata-only per-row review queue for the 612 Cambridge/Hopkins crosswalk candidates.

The Cambridge staging rows are institutional crosswalk metadata. They preserve Yingguo, Cambridge University Library, Chalfant, and Heji references, but must be checked against object records, Heji/OBM records, and source images before becoming formal `obi-*` inscription records.

The 098 review queue is a preprocessing route only. It prioritizes rows with missing CUL, Chalfant, or Heji references and records that image evidence, text transcription, collection-object matching, and formal `obi-*` assignment are not collected.

简体中文补充：
`../009_statistics-and-derived-features/098_ai-agent-cambridge-hopkins-inscription-crosswalk-review-queue.csv` 是 612 条 Cambridge/Hopkins crosswalk 候选的逐行 metadata-only 复核队列；它只安排缺失 CUL、Chalfant、Heji 引用和后续图像/对象/OBM 复核，不生成正式 `obi-*` 卜辞记录，也不记录释读结论。

简体中文：
本目录将保存卜辞全文记录、上下文、字序索引、主题、出土信息和来源引用。

当前索引：

- `000_inscription-registers/001_all-inscriptions-index.csv`：正式本项目卜辞记录。
- `000_inscription-registers/002_cambridge-hopkins-crosswalk-staging.csv`：Cambridge Hopkins finding list 暂存 crosswalk，包含 612 条可见 `y/c/h/j` 编号行。
- `000_inscription-registers/003_cambridge-hopkins-classified-summary.csv`：Cambridge Hopkins 分期分类汇总，包含 20 个主题组、官方分期合计、祖类补充组和总计。

Cambridge 暂存行是机构清单 crosswalk metadata。它们保留《英国所藏甲骨集》、Cambridge University Library、Chalfant 和《甲骨文合集》编号，但进入正式 `obi-*` 卜辞记录前，必须再和馆藏对象记录、《合集》/OBM 记录及原始图像交叉复核。
