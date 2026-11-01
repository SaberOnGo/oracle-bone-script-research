# AI Agent 日常工作协议 / AI Agent Operating Protocol

- 状态 / Status: `proposed_normative_protocol`
- 关系 / Relation: 本协议规定当前阶段（知识库建设与盲测校准）的日常
  工作方式。`doc/project/005_*` 的裁决战略规定未来"真实候选交付"阶段
  的门槛，两者不冲突：先按本协议把库建起来，再按 005 交付候选。

This protocol governs day-to-day work in the current stage. The adjudication
strategy in `doc/project/005_*` governs the later delivery stage.

## 1. 每次任务的开场 / Start Of Every Task

1. 读 `AGENTS.md`，再读本目录 `README.md`。
2. 问自己："这次任务结束时，哪一份人读档案、哪一条卜辞记录、哪一条
   有来源的主张或哪一个案件会比现在更完整？"答不出来就不要开始。
3. 打开要改的对象目录，先读现有档案，再查来源登记。
4. 不运行任何批量生成脚本。

## 2. 工作单位 / Unit Of Work

一次提交只做下列之一：

- 完成或推进一份对象档案（单字、实物、来源、文献）；
- 新增或修正一批卜辞释文记录（同一著录分桶内）；
- 新增或修正一组有来源的主张行；
- 推进一个研究案件（新证据、新反证、状态变化）；
- 工具、测试、规则文档的一次明确修改。

提交标题写"做了什么对象的什么事"，例如"补 obs-char-000412 释读史与
三条例句"，不写"Record visual observations for candidates 2829-2832"。

## 3. 写档案的方法 / How To Write A Dossier

按研究者的方式工作，顺序是：

1. 看图：打开本地字形图、拓片、照片，写下直接可见的东西。
2. 查著录：合集号、旧著录号、馆藏号、图版页。
3. 读卜辞：找全部字例所在卜辞，抄录来源释文并标出字位。
4. 读文献：谁释、何时、依据、谁反对；逐条带页码。
5. 比字形：异体、近形、构件、金文、小篆。
6. 写分布：次数、分期、辞例、共现。
7. 列问题：每个空缺写成"打开 X 来源第 N 页能否回答 Y"。

每句话带来源标记。写不出来源的句子，要么删掉，要么以"观察："或
"假说："开头。

## 4. 来源与权利 / Sources And Rights

- 只用登记过的来源（`corpus/006_*/000_source-registers/`）。新来源先
  登记再使用。
- 图片：公有领域或已核实可用的，存入对象 `images/` 并配 `.yaml`；
  其余只记路线、校验和与权利状态。
- 文本：来源释文可引用并标注；项目自己的隶定必须注明依据。
- 不因网页公开就推定可再利用。

## 5. 研究案件的写法 / Writing A Research Case

案件是把知识库证据交给模型推理的地方。流程：

1. 选对象：优先选有多条字例、卜辞全文可得、有近形或同构件字的未释
   字；或有学界争议的已释字。
2. 组证据包：按 `02_target-architecture.md` 第 7 节组装，全部来自
   档案与语料，带来源标记。
3. 独立推理：至少两个不同模型家族各自在新上下文中只看证据包，输出
   候选排序、依据、反证、弃权理由。不告诉它们彼此的答案。
4. 反例搜索：对最强候选，主动找近形竞争字、错误语境对照、相反辞例。
5. 写案件文件：按 `03_object-dossier-standard.md` 第 5 节。状态默认
   `working_hypothesis`。
6. 登记：`doc/public/user_research/cases/index.md` 加一行。

模型自报的"置信度"写进案件时标为 `uncalibrated_score`。只有盲测
（第 6 节）累积足够样本后，才能按 005 的规则讨论概率。

## 6. 盲测校准 / Masked-Known Calibration

- 从已释字档案中抽样，隐去第 2、3 节（隶定与释读史），把其余章节作
  为证据包交给模型。
- 记录：top-1 / top-3 命中、弃权是否恰当、错误类型（近形误判、语境
  误判、过度依赖今字标签等）。
- 结果写入 `doc/public/user_research/cases/calibration/`，每轮一个
  文件，含模型、日期、样本 ID、证据包校验和。
- 盲测同时是知识库的体检：模型因证据不足而失败的案例，说明档案缺
  什么。

## 7. 防走偏的硬规则 / Hard Rules Against Drift

以下任一情况发生，停止并回到第 1 节重新开始：

- 准备新建 10 个以上对象目录；
- 准备写一个 `build_*_dossiers.py`、`*_scaffold*`、`*_queue*`、
  `*_handoff*`、`*_route_pack*` 文件；
- 一份档案里出现第二段"不是释读结论"；
- 一次提交新增文件数超过 200 且不是卜辞语料行；
- 把数据集标签、文件名今字、码位直接写成释读。

这些规则由 `06_quality-gates-and-metrics.md` 中的脚本门禁执行。

Stop and restart from section 1 whenever you are about to create more than
ten object directories, write a generator or queue file, add a second
disclaimer to a dossier, add more than two hundred non-corpus files in one
commit, or write a label as a reading.

## 8. 汇报格式 / Report Format

每次任务结束说明：

- 哪些对象档案 / 卜辞记录 / 主张 / 案件变得更完整，具体到文件；
- 用了哪些来源，权利状态如何；
- 哪些校验跑了、结果如何；哪些没跑；
- 还缺什么，下一个最有价值的来源是什么。

不汇报"新增 N 个目录"或"生成 N 个文件"。
