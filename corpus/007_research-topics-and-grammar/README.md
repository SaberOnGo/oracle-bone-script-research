# Research Topics And Grammar / 研究主题与语法

English:
This corpus area is the human entry point for topic-label candidates,
controlled-vocabulary routes, Cambridge/Hopkins classified-table groups,
period-count evidence, inscription crosswalk routes, and later
grammar-position review.

简体中文：
本语料区是主题标签候选、受控词表路线、Cambridge/Hopkins 分类表
组别、时期计数证据、卜辞互证路线和后续语法位置复核的人工入口。

It is preprocessing infrastructure. It does not contain confirmed grammar
analysis, accepted inscription-topic assignments, readings, transcriptions,
or decipherment conclusions.

这里是预处理基础设施，不保存已确认语法分析、已接受卜辞主题归属、
读法、释文或释读结论。

## Human Research Entry Order / 人工研究入口顺序

1. Open `000_topic-registers/001_cambridge-hopkins-topic-candidate-index.csv`.
2. Find the matching `obs-topic-cand-*` object directory.
3. Read the object README, human dossier, and review sheet first.
4. Check `05_human-topic-review-sheet.md` for the human review state.
5. Check `02_topic-source-index.csv` for the source and group route.
6. Check `03_period-count-index.csv` for period-count index evidence.
7. Check `04_inscription-crosswalk-route-index.csv` for routed inscriptions.
8. Compare unrouted crosswalk rows before recording follow-up checks.

人工复核时，先看主题候选登记表、对象内 README、人类主题档案和
人工主题复核表，再看来源索引、时期计数索引、卜辞互证路线和
未路由互证行。结构化辅助文件只辅助检索、追溯和复核，不能替代
人工主题档案。

## Current Materials / 当前资料

- `000_topic-registers/001_cambridge-hopkins-topic-candidate-index.csv`
  lists Cambridge/Hopkins classified-table topic candidates.
- `000_topic-registers/002_cambridge-hopkins-topic-crosswalk-link-staging.csv`
  routes topic candidates to inscription crosswalk candidates.
- `000_topic-registers/003_cambridge-hopkins-unrouted-crosswalk-staging.csv`
  records unrouted crosswalk rows that still need human review.
- `001_topic-candidates/`
  contains object-local topic candidate directories.

## Object-Local Topic Materials / 对象内主题资料

Each topic candidate directory should keep these files together:

- `README.md`: human topic candidate overview and boundary.
- `01_topic-candidate-packet.json`: structured candidate support packet.
- `02_topic-source-index.csv`: source, group, and topic route index.
- `03_period-count-index.csv`: period-count index for review.
- `04_inscription-crosswalk-route-index.csv`: inscription crosswalk route.
- `05_human-topic-review-sheet.md`: human topic review sheet.

对象目录内同时放人类可读资料和结构化辅助资料。不要在主题候选目录
旁边另建并行的人类目录。

## Topic Dossier Content / 主题档案内容

A human topic or grammar-position dossier should let a reviewer check:

- topic candidate ID and Cambridge/Hopkins group route;
- source table, source label, and source-period count;
- linked inscription crosswalk candidates and unrouted crosswalk rows;
- inscription context still missing for formal grammar review;
- period, group, and batch fields that remain source hints;
- related characters, components, or formula routes to check later;
- proposer, disagreement, and dispute only when collected from sources;
- missing evidence and next human-gated review action.

人类主题或语法位置档案应让复核者看到：主题候选 ID、
Cambridge/Hopkins 组别路线、来源表、来源标签、来源时期计数、
关联卜辞互证候选、未路由互证行、正式语法复核前仍缺的卜辞语境、
仍只是来源线索的时期、组类与批次字段，以及后续应核查的字形、
构件、辞例路线、提出者、不同意见、争议、缺失证据和下一步人工
门控动作。

## Concrete Questions To Check / 具体待查问题

- Which topic candidate lacks a human topic review sheet?
- Which topic candidate lacks a clear Cambridge/Hopkins source route?
- Which period-count index row is only a source count, not a conclusion?
- Which inscription crosswalk route lacks plate or text evidence?
- Which unrouted crosswalk row should become a review queue item?
- Which topic label needs comparison with full inscription context?
- Which grammar-position question still lacks source-backed examples?
- Which graph edge is only a route and not a grammar conclusion?
- 哪个主题候选还缺人工主题复核表？
- 哪个主题候选还缺清楚的 Cambridge/Hopkins 来源路线？
- 哪个时期计数行只是来源计数，不能当作结论？
- 哪条卜辞互证路线还缺图版或文本证据？
- 哪个未路由互证行应转入复核队列？
- 哪个主题标签需要和完整卜辞上下文比较？
- 哪个语法位置问题还缺有来源支撑的例证？
- 哪条图边只是路线，不能当作语法结论？

## Research Boundary / 研究边界

Topic labels, period counts, crosswalk routes, staging rows, and graph edges
are review routes only. They are not a grammar conclusion, not an
inscription-topic assignment, not a transcription, not a reading, and not a
decipherment conclusion.
They are not an inscription-topic assignment and not a decipherment conclusion.

主题标签、时期计数、互证路线、staging 行和图边都只是复核路线。
它们不是语法结论，不是卜辞主题归属，不是释文，不是读法，也不是
释读结论。

## Regeneration Notes / 再生成说明

When topic routes, crosswalk staging, or review queues change, rerun the
topic material builder and then run repository validation and tests before
committing.

主题路线、互证 staging 或复核队列变化后，应重新运行主题资料生成器，
再运行仓库校验和测试，然后提交。
