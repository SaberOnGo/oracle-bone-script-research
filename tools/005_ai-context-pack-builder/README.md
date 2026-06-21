# AI Context Pack Builder / AI 上下文包生成器

English:
This directory contains tools that build AI-readable context packs from
reviewed preprocessing routes. The packs help AI Agents open source files,
route summaries, review queues, and outcome scaffold files, but they remain
support data for human research.

简体中文：
本目录保存 AI 上下文包生成工具。它们从已登记的预处理路线中汇总
来源文件、路线摘要、复核队列和 outcome scaffold，帮助 AI Agent
找到下一步证据路线，但仍然只是服务人类研究的辅助资料。

## Human Research Entry Order / 人工研究入口顺序

English:

1. Open the human source, object, or corpus README first.
2. Open the human dossier, review sheet, gallery, or source log next.
3. Use the AI context pack only to locate files and queues.
4. Check provenance, rights status, risk note, checksum, and review status.
5. Record reviewed outcomes only in human-facing review sheets or logs.
6. Do not treat AI context text as reviewed scholarship.

简体中文：

1. 先打开来源、对象或语料目录中的人类 README。
2. 再打开人类档案、复核表、图廊或来源记录。
3. 只把 AI 上下文包用于定位文件、队列和路线。
4. 核查出处、权利状态、风险提示、checksum 和复核状态。
5. 已复核结果只能写入面向人类的复核表或日志。
6. 不得把 AI 上下文文本当作已复核学术成果。

## Current Builder Families / 当前生成器类型

English:

- Source coverage context packs point from summaries to source records.
- Relationship graph context packs route graph edges back to source files.
- Source-processing packs expose gaps, routes, checklists, and scaffolds.
- HUST-OBC, OBIMD, EVOBC, and Xiaoxuetang packs prepare review queues.
- Graph-source packs prepare capture scaffolds for source registration.

简体中文：

- 来源覆盖类 context pack 把统计摘要指回来源记录。
- 关系图谱类 context pack 把图边指回可复核来源文件。
- source-processing 类文件暴露缺口、路线、清单和 scaffold。
- HUST-OBC、OBIMD、EVOBC 与小学堂路线准备复核队列。
- graph-source 路线准备来源登记和下载记录的 capture scaffold。

## Concrete Questions To Check / 具体待查问题

English:

- Which context pack points to the human-readable source trail?
- Which route still opens an empty outcome scaffold?
- Which context pack cites metadata-only rows?
- Which source still needs checksum, manifest, field map, or rights review?
- Which output must not be treated as reviewed scholarship?

简体中文：

- 哪个 context pack 指向可供人阅读的来源链？
- 哪条路线仍然只打开空的 outcome scaffold？
- 哪个 context pack 只引用 metadata-only 行？
- 哪个来源仍缺 checksum、manifest、字段映射或权利复核？
- 哪个输出明确不能当作已复核学术成果？

## Research Boundary / 研究边界

AI context packs are support routes. They are not reviewed scholarship,
not source promotion, not evidence collection, not rights decisions,
not corpus import, and not a decipherment conclusion.

AI 上下文包只是辅助路线。它们不是已复核学术成果，不是来源提升，
不是证据采集，不是权利裁定，不是语料导入，也不是释读结论。

## Regeneration Notes / 再生成说明

English:
Generated context packs must be regenerated from reviewed route files or
registered preprocessing outputs. A generator that creates temporary output
must keep scratch files under ignored work areas and must update validation
or tests when it changes a tracked human-facing entry point.

简体中文：
生成的 context pack 必须来自已登记的路线文件或预处理输出。若生成器
产生临时文件，草稿必须留在已忽略工作区；若它改变被跟踪的人类入口，
必须同步更新校验或测试。
