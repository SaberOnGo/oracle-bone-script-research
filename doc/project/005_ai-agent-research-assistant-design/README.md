# AI Agent Autonomous Candidate Adjudication Strategy / AI Agent 自主候选裁决战略

## Document Status / 文档状态

- Status / 状态: `normative_strategy`
- Effective date / 生效日期: `2026-08-09`
- Scope / 范围: AI hypothesis discovery, falsification, calibration,
  adjudication, and delivery.
- Authority / 权威性: this is the single normative strategy for AI candidate
  adjudication in this repository.

本文件是本仓库关于 AI 假说发现、反证、校准、裁决和交付的唯一规范性
战略。旧规划可以保留历史背景，但不得静默覆盖本文件。

This strategy does not replace [`AGENTS.md`](../../../AGENTS.md), the
human-first archive rule, source and rights policies, or the boundary between
AI hypotheses and confirmed scholarship.

本战略不取代 [`AGENTS.md`](../../../AGENTS.md)、人类档案优先原则、来源
与权利政策，也不取消 AI 假说与已确认学术结论之间的边界。

## 1. Strategic Decision / 战略决策

The project will shift its centre of gravity from producing more directories,
indexes, empty templates, and coverage counts to producing a small number of
falsifiable, counter-evidenced, reproducible candidate discoveries.

项目战略重心从生成更多目录、索引、空模板和覆盖计数，转向产出少量
可证伪、带反证、可复跑的候选发现。

AI agents may independently inspect evidence, form hypotheses, attack those
hypotheses, adjudicate the surviving candidates, and deliver high-confidence
candidates directly to the user. Prior approval by a human specialist is not
a delivery requirement.

AI Agent 可以独立查看证据、形成假说、攻击假说、裁决存活候选，并把
高置信候选直接提交给用户。真人专家预先批准不是候选交付的必要条件。

AI adjudication decides whether a candidate enters the user-facing channel.
It does not decide that the candidate is accepted scholarship. Only an
external scholarly process may establish that later status.

AI 裁决决定候选能否进入面向用户的交付通道，不决定它已被学界接受。
后者只能由外部学术过程形成。

## 2. Mission And User Need / 使命与用户需求

The long-term mission is:

> Use independent AI agents and traceable evidence to discover testable new
> information in oracle bone script, while making every inference open to
> inspection, rerun, refutation, downgrade, and withdrawal.

长期使命是：

> 使用独立 AI Agent 和可追溯证据，发现甲骨文中可检验的新信息，并让
> 每一项推断都能被检查、复跑、反驳、降级和撤回。

The user is not expected to be an oracle-bone specialist or to arbitrate every
technical dispute. The system must carry the burden of specialist-style
inspection and internal review. The user should receive the proposition, its
calibrated probability, the best competing proposition, decisive evidence,
the strongest counterevidence, and the conditions that would overturn it.

用户不需要成为甲骨文学者，也不需要亲自裁决每个技术争议。系统应承担
专家式查看和内部复核的主要负担。用户应收到命题、校准概率、最强替代
命题、决定性证据、最强反证和可推翻条件。

The project remains human-first in presentation. Human-readable research
dossiers are the primary research product. JSON, CSV, manifests, schemas,
indexes, and graph edges remain secondary instruments for search, audit,
statistics, and reruns.

项目在交付形态上仍以人类为先。人类可读研究档案是主要研究产物。
JSON、CSV、manifest、schema、索引和图边仍是检索、审计、统计和复跑的
辅助工具。

## 3. Non-goals / 非目标

The strategy does not authorize the project to:

- turn a model's self-reported confidence into a research probability;
- equate agreement among dependent agents with independent confirmation;
- infer meaning from visual resemblance alone;
- treat modern labels, codepoints, directory names, or benchmark answers as
  hidden evidence;
- promote AI output into `research/` as established scholarship;
- hide disagreement, failed reruns, provenance defects, or rights risks;
- measure progress by file count, object count, or generated templates alone.

本战略不允许项目：

- 把模型自报置信度直接当作研究概率；
- 把存在依赖关系的 Agent 一致意见当作独立确认；
- 只凭图形相似推断字义；
- 把今字标签、码位、目录名或基准答案当作隐藏证据；
- 把 AI 输出直接提升到 `research/` 并写成既定学术结论；
- 隐藏分歧、复跑失败、来源缺陷或权利风险；
- 只用文件数、对象数或模板生成量衡量进展。

## 4. Three Result States / 三层结果状态

### `working_hypothesis`

An exploratory proposition that has not passed the release gate. It may be
useful, but its probability may be uncalibrated or decisive evidence may be
missing. It remains under `doc/public/user_research/`.

尚未通过交付门槛的探索命题。它可能有用，但概率可能尚未校准，或仍缺
决定性证据。它保留在 `doc/public/user_research/`。

### `ai_adjudicated_candidate`

A falsifiable proposition that passed the registered evidence, provenance,
leakage, adversarial, rerun, and probability gates. AI agents may deliver it
to the user without prior human-specialist approval.

通过预登记证据、来源、泄漏、对抗、复跑和概率门槛的可证伪命题。
AI Agent 可以在没有真人专家预先批准的情况下把它提交给用户。

This is a `delivery_status` overlay, not a value for the legacy evidence-pack
`status` or `assignment_status` fields. Legacy v1 packs keep the appropriate
v1 lifecycle `status` and `research_boundary=draft_not_scholarship`. The [v2
benchmark contract][benchmark-v2] records the delivery decision and
independent adjudicator runtime before this overlay can be released. Its
`assignment_status=reserved_candidate_not_assigned` remains until a human
review separately promotes it into the formal character corpus.

这是一个 `delivery_status` 叠加层，不是旧 evidence-pack 的 `status` 或
`assignment_status` 字段值。旧版 v1 证据包继续使用适当的 v1 生命周期
`status`，并保持 `research_boundary=draft_not_scholarship`。v2 基准合同
必须先记录交付决定和独立裁决运行，才可以释放这个叠加状态。只有人工
另行提升到正式单字语料时，
`assignment_status=reserved_candidate_not_assigned` 才改变。

This status always means "high-confidence AI candidate", not "deciphered",
"proved", or "accepted". It is not confirmed scholarship.

该状态始终表示“高置信 AI 候选”，不表示“已经破译”“已经证明”
“已被接受”或“已确认学术结论”。

### `confirmed_scholarship`

A broad label reserved for evidence of wide external scholarly acceptance.
A single publication, peer review, or external opinion is not sufficient.
Repository AI agents cannot assign this status by themselves.

只在有证据表明得到广泛外部学术接受时使用的总括标签。单篇发表、一次
同行评审或一位外部意见都不足以构成该状态。仓库内 AI Agent 不能自行
授予该状态。

The scholarship axis must separately record `published_scholarly_claim`,
`externally_reviewed`, and `accepted_scholarly_consensus`. Publication never
silently promotes a candidate to consensus.

学术状态轴必须分别记录 `published_scholarly_claim`、
`externally_reviewed` 和 `accepted_scholarly_consensus`。发表不能静默把
候选提升为学界共识。

Withdrawal and reopening are lifecycle actions, not a fourth truth level.
Every earlier verdict remains in version history.

撤回和重开属于生命周期动作，不是第四种真值等级。旧裁决必须保留在
版本历史中。

## 5. Current-State Diagnosis / 当前状态诊断

The current filesystem is authoritative. The replaceable operational snapshot
is the [2026-08-30 current operating baseline][current-baseline]. The
[2026-08-14 audit][historical-audit] is a historical frozen receipt.

当前磁盘状态具有最高权威。可替换的运行快照是
[2026-08-30 当前运行基线][current-baseline]。[2026-08-14 审计]
[historical-audit]是 historical frozen receipt，仅保留历史回执。

The preprocessing closure dated `2026-08-07` records a broad traceable
archive. Its counts are bound to commit `c58eea95a97`. A later read-only
strategy audit used HEAD `4872a2e8cd9` plus an already dirty working tree on
`2026-08-09`. The later observations are planning signals, not a frozen audit
artifact and not experiment evidence.

`2026-08-07` 的预处理闭合报告记录了广泛的可追溯档案，其计数绑定提交
`c58eea95a97`。后续只读战略审计使用 `4872a2e8cd9` HEAD 和
`2026-08-09` 已经存在未提交修改的工作树。后者只是规划信号，不是冻结
审计产物，也不能作为实验输入。

The normative rules below do not depend on these counts. Gate 1 must create a
versioned audit artifact with commands, tree identity, source routes, and
outputs before any diagnosis is used in an experiment.

以下规范规则不依赖这些计数。任何诊断进入实验前，Gate 1 必须形成带
命令、树身份、来源路线和输出的版本化审计产物。

Material findings include:

- `29,756` object bundles are registered in the closure snapshot.
- `10,996` HUST-derived character objects have a local image and a visual
  note, but their core inscription, catalog, archaeology, variant, component,
  reading-history, and dispute questions remain unresolved.
- `612` inscription candidates have useful collection and catalog identifiers,
  but no local image, transcription, or OCR was present in the audited route.
- the only AI evidence pack was a draft with all nine evidence sections still
  `not_collected`;
- current character-inscription graph promotion remains `0`;
- existing high graph confidence usually describes route integrity, not a
  calibrated probability that a reading is correct.

主要事实包括：

- 闭合快照登记了 `29,756` 个对象包；
- `10,996` 个 HUST 派生单字对象已有本地图像和观察笔记，但卜辞、著录、
  考古、异体、构件、释读史和争议等核心问题仍未解决；
- `612` 个卜辞候选已有可用馆藏与著录标识，但审计路线中没有本地图像、
  释文或 OCR；
- 唯一 AI evidence pack 仍是草稿，九个证据区均为 `not_collected`；
- 当前 character-inscription 图边提升数量仍为 `0`；
- 现有图边的 high confidence 通常只表示路线完整度，不表示释读正确概率。

The historical audit defects now have an explicit disposition:

- The human-material `--summary` control flow and coverage-baseline direction
  are fixed and covered by seven regression tests. The latest full/strict
  receipt scanned 156838 Markdown files with four debt counts at zero.
- The HUST raw package now joins `dl-hust-obc-figshare-raw`, not the API
  metadata record. OBIMD `pkg-file-000008` joins `large-src-000004`; package
  routes and checksums are cross-checked in source-object tests.
- `large-src-000003` remains only the unacquired EVOBC unified raw-image scope;
  its five separate downloaded snapshots are not silently merged into it.
- OBIMD licence statements still conflict. The active override is
  `metadata_only_until_verified`, so public image or derivative reuse remains
  blocked until rights evidence is reconciled.
- No real v2 experiment or external scorer receipt exists. The probability
  channel therefore remains withheld even though structural validators pass.

历史审计缺陷已有明确处置：

- 人类资料门 `--summary` 控制流和覆盖基线方向已修复，并由 7 项回归测试
  覆盖。最新 full/strict 回执扫描 156838 篇 Markdown，四项债务均为 0。
- HUST 原始包现绑定 `dl-hust-obc-figshare-raw`，不再绑定 API 元数据记录。
  OBIMD `pkg-file-000008` 现绑定 `large-src-000004`；来源对象测试会交叉核对
  包路线与 checksum。
- `large-src-000003` 仍只表示尚未取得的 EVOBC 统一原始图像包范围；其 5 个
  独立下载快照不能被静默合并进去。
- OBIMD 许可表述仍有冲突。当前覆盖状态为
  `metadata_only_until_verified`，权利证据解决前仍禁止公开图像或派生件复用。
- 尚无真实 v2 实验或外部评分回执。因此即使结构校验通过，概率通道仍必须扣留。

These findings are repository audits, not paleographic conclusions. They set
the order of implementation work.

这些发现是仓库审计结果，不是文字学结论。它们用于决定实施顺序。

## 6. External Landscape And Differentiation / 外部格局与差异化

The project should reuse strong public work instead of imitating it:

- [HUST-OBC] reports `140,053` images in `1,588` deciphered and `9,411`
  undeciphered categories. It is a major visual candidate pool, but the paper
  warns about duplicated undeciphered categories and source-quality limits.
- [OBIMD] reports `10,077` entries, `93,652` characters, and `21,941`
  sentences with boxes and reading order. It is a strong context substrate,
  not an independent adjudicator.
- [EvoBC] provides a large cross-period visual collection. Its proposed
  evolution routes are candidate evidence, not automatic identity or meaning.
- [IHP] provides institutional rubbing and catalog routes that are valuable
  for object identity and provenance.
- [OBI-Bench] and [PictOBI-20k] expose weaknesses in visual recognition and
  language-prior dependence, but neither is a sufficient probability
  calibration set for genuine decipherment.
- [OracleAgent] demonstrates tool orchestration and retrieval.
- [AlphaOracle] demonstrates a useful morphology, context, and philology
  chain, but its final reports remain hypotheses and its modules do not form
  independent blinded courts.
- a [2026 survey] identifies long-tail data, unavailable materials, noisy
  originals, annotation error, and missing context as persistent barriers.

本项目应复用这些公开成果，而不是简单复制：

- [HUST-OBC] 报告 `140,053` 张图，包含 `1,588` 个已释类和 `9,411` 个
  未释类。它是重要视觉候选池，但论文也提示未释类重复和来源质量问题；
- [OBIMD] 报告 `10,077` 条记录、`93,652` 个字和 `21,941` 个句组，并有
  字框与阅读顺序。它是强上下文底座，不是独立裁判；
- [EvoBC] 提供大规模跨时期图像，其演化路线只是候选证据，不能自动证明
  同字或同义；
- [IHP] 提供机构级拓片和著录路线，适合确认对象身份与来源；
- [OBI-Bench] 和 [PictOBI-20k] 揭示视觉识别弱点和语言先验问题，但都
  不足以单独校准真实释读概率；
- [OracleAgent] 展示了工具编排和检索方式；
- [AlphaOracle] 展示了形体、上下文和文献链，但最终报告仍是假说，且各
  模块不是相互盲隔离的独立法庭；
- [2026 survey] 指出长尾、资料不可得、原图噪声、标注错误和上下文不足
  仍是主要障碍。

The strategic niche is therefore an auditable autonomous hypothesis
laboratory: independent AI experts investigate, falsify, reproduce, calibrate,
and adjudicate candidates on traceable evidence.

因此，本项目的战略差异化是“可审计的自主假说实验室”：独立 AI 专家
在可追溯证据上调查、反证、复现、校准并裁决候选。

Shared ancestry must be explicit. AlphaOracle, PictOBI, HUST-OBC, EvoBC,
and OBIMD may reuse the same images, labels, or transcriptions. Agreement
among them is not automatically independent evidence.

来源共同祖先必须显式记录。AlphaOracle、PictOBI、HUST-OBC、EvoBC 和
OBIMD 可能复用相同图像、标签或释文；它们的一致意见不自动构成独立
证据。

## 7. Three Research Planes / 三层研究平面

### Evidence archive / 证据档案层

Object-local human dossiers hold images, observations, inscriptions, context,
catalog trails, find spots, collections, periods, groups, literature,
disputes, rights, provenance, and concrete missing questions.

对象内人类档案保存图像、观察、卜辞、上下文、著录链、出土地、馆藏、
时期、组类、文献、争议、权利、来源和具体缺失问题。

### Candidate discovery laboratory / 候选发现实验层

Agents open frozen evidence views, perform independent analyses, record
alternatives and falsifiers, and produce versioned case files.

Agent 打开冻结证据视图，进行独立分析，记录替代解释和反证条件，并形成
版本化案件档案。

### Experiment and calibration layer / 实验与校准层

Hidden-answer benchmarks, leakage controls, reruns, metrics, and threshold
registrations determine whether a numerical probability may be shown.

隐藏答案基准、泄漏控制、复跑、指标和阈值预登记共同决定是否允许显示
数值概率。

No plane may replace another. A machine experiment without a readable dossier
is not a research delivery. A readable argument without reproducible evidence
and calibration cannot enter the high-confidence channel.

三层互不替代。没有可读档案的机器实验不是研究交付；没有可复现证据和
校准的人类可读论证，也不能进入高置信通道。

## 8. Six Linked Research Graphs / 六类关联研究图

The laboratory needs six linked graphs:

1. provenance dependency: downloads, packages, derivatives, citations, and
   common ancestors;
2. object and inscription: bone, fragment, plate, catalog number, occurrence,
   sentence, collection, find spot, period, and group;
3. glyph: image, shape, component, near-form, variant, and damage relation;
4. context: neighbouring signs, syntax slot, topic, formula, co-occurrence,
   negative occurrence, and distribution;
5. scholarship: claim, proposer, date, citation, supporting argument,
   objection, dispute, and supersession;
6. experiment lineage: evidence snapshot, model, prompt, tool, seed, run,
   verdict, calibration cohort, rerun, and withdrawal.

实验室需要六类互联图：

1. 来源依赖图：下载、包、派生物、引用和共同祖先；
2. 对象与卜辞图：原骨、残片、图版、著录号、字例、句组、馆藏、
   出土地、时期和组类；
3. 字形图：图像、形态、构件、近形、异体和残损关系；
4. 语境图：邻字、句法位置、主题、辞例、共现、负出现和分布；
5. 学术主张图：主张、提出者、日期、引文、论据、反对意见、争议和取代；
6. 实验谱系图：证据快照、模型、提示词、工具、seed、运行、裁决、
   校准群、复跑和撤回。

`route_integrity_confidence` and `hypothesis_probability` must be separate.
The former says how trustworthy a route or mapping is. The latter is allowed
only after task-specific calibration.

`route_integrity_confidence` 与 `hypothesis_probability` 必须分开。前者
表示路线或映射可信程度，后者只有在任务级校准后才允许出现。

## 8.1 Network Search And Evidence Routing / 网络搜索与证据路由

The network is an evidence-routing instrument, not a popularity ranking. Its
purpose is to find the next source that can most sharply support or falsify a
registered proposition.

网络是证据路由工具，不是网页热度排名。它的目的，是找到最可能明确支持
或推翻已登记命题的下一项来源。

Every search starts from an object-local dossier and a claim card. Before an
agent queries the web, it records the stable project ID, external aliases,
traditional and simplified forms, catalog abbreviations, and known false
aliases. Search-engine wording is never silently promoted to evidence.

每次搜索都从对象目录内档案和命题卡开始。Agent 查询网络前，先记录稳定的
项目 ID、外部别名、繁简字形、著录缩写和已知错误别名。搜索引擎生成的词语
不得被静默提升为证据。

### Layered search order / 分层搜索顺序

Search proceeds in layers, with each layer answering a different question:

搜索按层进行，每层只回答一种不同问题：

1. institutional catalogues and museum records for object identity,
   collection, accession, findspot, and rights;
2. source-edition plates, rubbings, photographs, and facsimiles for visible
   material and plate-level identity;
3. inscription and context databases for sentence scope, neighbours, order,
   and occurrence routes;
4. published scholarship for proposers, dates, arguments, corrections,
   competing readings, and dispute history;
5. bronze, seal, and later-form sources for diachronic comparison only after
   the earlier layers are open;
6. package, checksum, rights, and dependency records before any derivative is
   counted or delivered.

1. 机构著录和博物馆记录：核对对象身份、馆藏、登录号、出土地和权利；
2. 底本图版、拓片、照片和摹本：查看实物及图版级身份；
3. 卜辞和上下文数据库：恢复句子范围、邻字、顺序和字例路线；
4. 已发表研究：记录提出者、日期、论证、订正、不同释读和争议史；
5. 金文、小篆和后世字形：只有前几层打开后才用于历时比较；
6. 包、校验和、权利和依赖记录：在计算或交付任何派生物前完成核对。

### Search receipts / 搜索回执

Each query is a reproducible source event. Its receipt records the exact
query, site or endpoint, timestamp, response URL, status code, content type,
access or download path, size, checksum, rights signal, extraction method,
and the concrete unresolved question left by the result.

每次查询都是可复跑的来源事件。回执记录准确查询词、网站或接口、时间、响应
URL、状态码、内容类型、访问或下载路径、大小、校验和、权利信号、抽取方法，
以及该结果留下的具体未决问题。

A result that returns only a label, a search hit, or a platform identifier is
a route record. It is not a plate, a transcription, an identity decision, or
a reading. HTTP errors and authentication walls are access boundaries, not
negative evidence.

只返回标签、搜索命中或平台 ID 的结果只是路线记录，不是图版、释文、身份
裁决或释读。HTTP 错误和登录墙是访问边界，不是反面证据。

### Graph rules / 图谱规则

The graph stores objects, occurrences, pages, editions, claims, agents, and
runs as distinct nodes. Edges are typed at minimum as `supports`,
`contradicts`, `derives_from`, `duplicates`, `cites`, `co_occurs`,
`same_object_candidate`, or `source_missing`.

图谱把对象、字例、页面、版本、命题、Agent 和运行作为不同节点。边至少要
区分 `supports`、`contradicts`、`derives_from`、`duplicates`、`cites`、
`co_occurs`、`same_object_candidate` 和 `source_missing`。

Every edge carries a source locator, checksum or snapshot identity when
available, rights state, review status, time, and provenance family. A graph
edge without a source locator remains a routing hint and cannot support a
candidate.

每条边都要带来源定位；若有条件，还要带校验和或快照身份、权利状态、复核
状态、时间和来源家族。没有来源定位的图边只能作路由提示，不能支持候选。

Support is counted by independent source family, not by edge, row, prompt,
or agent count. The provenance graph collapses mirrors, copied images,
derived OCR, shared transcriptions, and same-platform aliases before support
is aggregated. Unknown ancestry is treated as dependent or unresolved, never
as independent confirmation.

支持按独立来源家族计数，不按图边、数据行、提示词或 Agent 数量计数。合并
支持前，来源图必须折叠镜像、复制图像、派生 OCR、共享释文和同平台别名。
祖先关系未知时记为依赖或未决，不能当作独立确认。

Node degree, PageRank, or community size is useful for routing and duplicate
discovery only. A high-degree source hub does not receive extra evidential
weight, and a disconnected node is not evidence against a proposition.

节点度数、PageRank 或社区大小只能用于路由和发现重复。高连接来源枢纽不因
此增加证据权重；孤立节点也不能被解释为反对命题的证据。

### Network analyses / 网络分析

The network analyst runs five bounded diagnostics before a court sees a
candidate:

网络分析 Agent 在法庭查看候选前执行五项有边界的诊断：

1. provenance components and communities to separate source families and
   identify shared ancestors;
2. duplicate and near-duplicate checks using checksums, image fingerprints,
   OCR overlap, citation inheritance, and platform identifiers;
3. temporal slices to expose future-literature, benchmark, and training
   leakage;
4. coverage-aware negative checks so an unindexed or inaccessible item is not
   mistaken for a true absence;
5. bridge and bottleneck checks to find the single next source that could
   split competing identity or reading explanations.

1. 用来源连通分量和社区拆分来源家族并识别共同祖先；
2. 用校验和、图像指纹、OCR 重叠、引文继承和平台 ID 查重及近重复；
3. 用时间切片发现未来文献、基准泄漏和训练泄漏；
4. 做覆盖率感知的反面检查，不能把未编目或不可访问误当成真实缺失；
5. 检查桥接点和瓶颈，寻找能区分身份或释读竞争解释的下一来源。

The next-source priority is an information-gain heuristic, not a research
probability:

下一来源优先级是信息增益启发式，不是研究概率：

```text
priority = impact * falsification_power * independence_gain
           * access_likelihood / cost
```

The factors are qualitative until a task-specific study validates them. The
highest priority usually belongs to a source that can attack the strongest
remaining assumption, not to the source with the most rows or images.

在任务级研究验证前，上述因子只能作定性判断。最高优先级通常属于能攻击
最强剩余假设的来源，而不是行数或图片最多的来源。

### Handoff and stopping / 交接与停止

The network agent delivers a human-readable route note containing the query
history, family map, support and contradiction edges, access boundaries, and
one concrete next-source question. JSON, CSV, and graph files sit beside that
note as audit support.

网络 Agent 交付人类可读的路由说明，包含查询历史、来源家族图、支持与反证
边、访问边界和一个具体下一来源问题。JSON、CSV 和图文件只作为该说明旁边
的审计辅助资料。

Two blinded research courts receive family-labelled evidence slices, not a
network popularity score. The final AI adjudicator may deliver a candidate
without prior human-specialist approval, but only after the same calibration,
rights, leakage, and falsification gates in this strategy pass.

两个盲隔离研究法庭接收标明来源家族的证据切片，不接收网络热度分数。最终
AI 裁判可以在没有真人专家预先批准时交付候选，但仍必须通过本战略规定的
校准、权利、泄漏和反证门槛。

If one high-value route produces only metadata, the case remains open but the
claim remains withheld. If a second search adds no independent edge, the
system stops crawling and changes the research question or records abstention.
Endless inventory growth is not network progress.

如果一条高价值路线仍只产生 metadata，案件可以保留，但命题必须扣留。如果
第二次搜索没有增加独立图边，系统停止爬取，转向新的研究问题或记录弃权。
无止境增加清单不算网络进展。

## 9. Independent Agent Courts / 独立 Agent 法庭

Each candidate is examined by two blinded research courts and one calibration
and adjudication court. The unit of independence is an evidence family, not
the number of prompts or model personas.

每个候选由两个相互盲隔离的研究法庭和一个校准裁决法庭处理。独立性的
单位是证据家族，不是提示词或角色数量。

Independence has separate axes: evidence, execution context, model family,
training knowledge, retrieval corpus, and tool lineage. Every run records all
six. Multiple prompts or fresh contexts on the same base model provide
execution reruns, not model-independent confirmation. Unknown training
overlap is recorded as dependence, not assumed away.

独立性分为证据、执行上下文、模型家族、训练知识、检索语料和工具谱系
六个轴。每次运行都要记录六轴。同一基础模型的多个提示词或新上下文只是
执行复跑，不构成模型独立确认。训练重叠未知时应记为依赖，不能假定独立。

Recommended specialist roles are:

- artifact and image inspection;
- glyph morphology, damage, near-form, and component comparison;
- inscription context, grammar, formula, and co-occurrence;
- archaeology, period, group, find spot, and collection;
- diachronic bronze, seal, and later-form correspondence;
- literature, reading history, proposer, and dispute review;
- network statistics and negative-distribution analysis;
- provenance dependency and rights audit;
- label, benchmark, and training-leakage audit;
- strongest alternative explanation and adversarial falsification;
- calibration and final adjudication.

建议专家角色包括：

- 实物与图像查看；
- 字形、残损、近形和构件比较；
- 卜辞上下文、语法、辞例和共现分析；
- 考古时期、组类、出土地和馆藏分析；
- 金文、小篆和后世字形历时对应；
- 文献、释读史、提出者和争议审查；
- 网络统计与负分布分析；
- 来源依赖和权利审计；
- 标签、基准和训练泄漏审计；
- 最强替代解释与对抗反证；
- 概率校准与最终裁决。

Agents submit sealed initial judgments before seeing other agents' answers.
They then receive only the minimum material needed for cross-examination.
No agent may count its own derivative output as new evidence.

各 Agent 在看到其他 Agent 答案前提交密封初判。随后只取得交叉质询所需
的最少材料。任何 Agent 都不得把自己的派生输出再次计为新证据。

The final adjudicator does not use majority vote. It folds dependent sources,
models, retrieval corpora, and tools, weighs task-calibrated evidence, records
unresolved disagreement, and may abstain.

最终裁判不采用简单多数票。它合并依赖来源、模型、检索语料和工具，按
任务校准证据加权，记录未解决分歧，并可以弃权。

## 9.1 Independent Adjudicator Contract / 独立裁决 Agent 合同

The final adjudicator is a separate decision run, not a summarizer of the
research courts and not a counter of votes. It may reject every court's
ranking. Its output is a decision about the registered case, not a new source
of paleographic evidence.

最终裁决 Agent 是独立的决策运行，不是研究法庭的摘要器，也不是计票器。
它可以否定所有法庭的排序。它的输出只是对已登记案件的裁决，不是新的
古文字证据来源。

Before it receives court reports, the coordinator freezes the claim, the
candidate universe, the evidence snapshot, the rights state, and the
falsification plan. The adjudicator must use a fresh context, keep gold
sealed, and have `prior_run_output_access=none`.

在裁决 Agent 收到法庭报告前，协调器先冻结命题、候选全集、证据快照、
权利状态和反证计划。裁决 Agent 必须使用全新上下文、保持 gold 封存，
并把 `prior_run_output_access=none` 写入记录。

The adjudicator declares its model family, model ID, retrieval snapshot, tool
manifest, training-knowledge status, context ID, input run IDs, and output
lock hash. Its evidence snapshot must equal the frozen protocol snapshot. A
model family already used by a research court may issue a diagnostic review,
but it cannot authorize candidate delivery as the only adjudicator family.

裁决 Agent 必须声明模型家族、模型 ID、检索快照、工具 manifest、训练知识
状态、上下文 ID、输入运行 ID 和输出锁定 hash。其证据快照必须等于冻结的
协议快照。研究法庭已经使用过的模型家族可以做诊断复核，但不能作为唯一
裁决家族授权候选交付。

### Adjudicator packet / 裁决包

The packet is human-readable first and contains the exact proposition, opaque
candidate aliases including `unknown_or_other`, the source-family map, the
support and opposition ledger, all falsification outcomes, calibration
pointer, rights and leakage status, and every locked rerun receipt.

裁决包以人类可读内容为先，包含精确命题、包括 `unknown_or_other` 在内的
不泄漏答案的候选别名、来源家族图、支持与反对证据账、全部反证结果、
校准指针、权利与泄漏状态以及每次锁定复跑回执。

The initial comparison presents court reports under opaque court IDs. It
does not expose a popularity score or model prestige. Dependency metadata is
shown as an audit fact, while a court's agreement is never counted as a new
evidence family.

初次比较时，法庭报告只显示不透明的法庭 ID。不显示热度分数或模型声望。
依赖 metadata 作为审计事实提供，但法庭之间的一致意见绝不计作新的证据
家族。

The adjudicator may re-read registered evidence, but may not add an
unregistered file, repair a missing source silently, change a candidate alias,
or waive a rights, leakage, provenance, or claim-evidence blocker.

裁决 Agent 可以重读已登记证据，但不得添加未登记文件、静默修补缺失来源、
改变候选别名，也不得豁免权利、泄漏、出处或命题证据阻断项。

### Required decision memo / 必需裁决说明

The memo records one decision for every test case: selected candidate or
explicit abstention, calibrated interval or cleared probability, the best
alternative, disagreement resolution, hard opposition, evidence blockers,
one concrete next-source question, and the exact reason for delivery or
withholding.

裁决说明为每个测试案件记录一项决定：选定候选或明确弃权、校准区间或已
清除的概率、最佳替代命题、分歧处理、致命反证、证据阻断项、一个具体的
下一来源问题，以及交付或扣留的确切理由。

The adjudicator cannot raise a probability above the registered calibration
support, turn a route hint into evidence, or replace an unresolved hard
counterexample with a confidence statement. If the independent model or
source condition is missing, the valid output is diagnostic review or
withholding, not a candidate.

裁决 Agent 不能把概率提高到预登记校准支持之上，不能把路线提示变成证据，
也不能用置信度表述替代未解决的致命反例。如果独立模型或来源条件缺失，
有效输出只能是诊断复核或扣留，而不是候选。

The v2 record must bind `adjudicator_id`, `execution_id`, `model_id`,
`model_family`, `context_id`, `input_run_ids`,
`evidence_snapshot_sha256`, `tool_manifest_sha256`, `gold_access`,
`prior_run_output_access`, and `output_lock_sha256`. A missing binding is an
execution defect and blocks `ai_adjudicated_candidate`.

v2 记录必须绑定 `adjudicator_id`、`execution_id`、`model_id`、
`model_family`、`context_id`、`input_run_ids`、
`evidence_snapshot_sha256`、`tool_manifest_sha256`、`gold_access`、
`prior_run_output_access` 和 `output_lock_sha256`。缺少绑定属于执行缺陷，
必须阻止 `ai_adjudicated_candidate`。

Human-specialist approval is not a prerequisite for this contract. The
independent AI adjudicator, sealed evidence, calibrated lower bound, and
reversible audit trail are the required safeguards. External scholarship
may later disagree, and such disagreement must reopen rather than silently
rewrite the AI verdict.

本合同不把真人专家批准设为前置条件。必需的安全措施是独立 AI 裁决、封存
证据、校准下界和可逆审计链。外部学术研究以后可以提出不同意见；这类
分歧必须触发重开，不能静默改写 AI 裁决。

## 10. End-to-End Research Loop / 端到端研究循环

1. Select a case for expected information gain and falsifiability, not a
   weekly quota.
2. Freeze the object, source, rights, software, and evidence snapshot.
3. Register the exact proposition, alternatives, and overturning conditions.
4. Blind modern labels, codepoints, answer-bearing paths, and later literature.
5. Give dependency-labelled evidence views to the two research courts.
6. Collect sealed rankings, probabilities or scores, evidence, and objections.
7. Run adversarial searches for near-form, context, period, and source
   counterexamples.
8. Fold common source ancestry and run leakage and rights audits.
9. Rerun with fixed manifests, fresh contexts, and declared independence axes.
10. Apply the registered calibration model and release gate.
11. Deliver an `ai_adjudicated_candidate` or an explicit abstention.
12. Reopen, downgrade, or withdraw when material new evidence arrives.

1. 按预期信息增益和可证伪性选案，不设每周配额；
2. 冻结对象、来源、权利、软件和证据快照；
3. 预登记精确命题、替代命题和可推翻条件；
4. 隐藏今字标签、码位、带答案路径和目标年代之后的文献；
5. 向两个研究法庭提供标明依赖关系的证据视图；
6. 收集密封排序、概率或分数、证据和异议；
7. 主动搜索近形、语境、时期和来源反例；
8. 合并共同来源祖先，执行泄漏和权利审计；
9. 使用固定 manifest、新上下文和已声明的独立性轴复跑；
10. 应用预登记校准模型和交付门槛；
11. 交付 `ai_adjudicated_candidate`，或明确弃权；
12. 出现重要新证据时重开、降级或撤回。

## 11. Probability Policy / 概率政策

A model statement such as "92% confident" is an uncalibrated score. It must
not be displayed as a probability of decipherment.

模型说“有 92% 把握”只是未校准分数，不能显示为破译概率。

The case model should distinguish at least:

- probability of object and image identity;
- probability of a same-sign, variant, near-form, or component relation;
- probability of a reading or phonological candidate;
- probability of the semantic or grammatical function in this inscription;
- probability of a cross-period correspondence;
- probability of the complete proposition submitted to the user.

案件至少应区分：

- 对象与图像身份概率；
- 同字、异体、近形或构件关系概率；
- 读音或隶定候选概率；
- 该卜辞中语义或语法功能概率；
- 跨时期对应概率；
- 最终提交给用户的完整命题概率。

These values are not multiplied mechanically. A registered meta-calibrator
must learn their relationship from hidden known-answer cases in the same task
family.

这些数值不能机械相乘。预登记的综合校准器应在同任务族的隐藏已知答案
案例上学习它们之间的关系。

Empirical calibration may draw on generation-based [LLM calibration] and
[conformal shift] methods. Their assumptions and failure modes must be stated.
Neither method repairs answer leakage, dependent evidence, or an invalid
benchmark.

经验校准可以参考基于模型生成的 [LLM calibration] 和 [conformal shift]
方法，但必须写清假设和失效条件。任何方法都不能修复答案泄漏、依赖证据
或无效基准。

Before calibration is adequate, the field is `uncalibrated_score`, and the
case cannot enter the high-confidence channel. Each task-domain protocol must
pre-register:

- the calibration population and domain card;
- the loss, candidate universe, and abstention semantics;
- the calibration method and independent family-cluster unit;
- a one-sided confidence level, normally `95%`;
- a power-based `minimum_effective_cases` requirement;
- the target selective precision and threshold-search rule;
- the OOD tests and mandatory withholding outcome.

在校准充分前，字段只能叫 `uncalibrated_score`，案件不能进入高置信通道。
每个任务域协议必须预登记：

- 校准总体和适用域说明；
- 损失函数、候选全集和弃权语义；
- 校准方法和独立家族聚类单位；
- 单侧置信水平，通常为 `95%`；
- 按统计功效确定的 `minimum_effective_cases`；
- 目标选择性精确率和阈值搜索规则；
- OOD 检查和强制扣留结果。

`XX%` is not chosen by intuition. It is the registered threshold whose
one-sided lower confidence bound for selective precision meets the target on
the calibration split, with the minimum effective cases satisfied. The final
test is opened once. If no threshold qualifies, the entire high-confidence
channel is withheld.

`XX%` 不能凭直觉指定。它必须是在 calibration split 上满足最小有效案例
数，并使选择性精确率单侧置信下界达到目标的预登记阈值。最终测试集只
开启一次。没有任何阈值达标时，整个高置信通道都必须扣留。

The live case also needs a cross-fitted probability interval whose lower bound
exceeds the registered task threshold. Values such as `0.90` or `0.97` may be
precision targets, but they are not granted before the benchmark supports
them. Runner-up odds are only a diagnostic for a declared closed candidate
universe with explicit unknown mass; they are never a stand-alone release
gate.

真实案件还要有交叉拟合的概率区间，其下界必须超过预登记任务阈值。
`0.90` 或 `0.97` 可以作为精确率目标，但在基准支持前并不成立。第一与
第二候选优势只适用于已声明封闭、并显式包含未知质量的候选全集，且不能
单独作为交付门槛。

Calibration on known readings does not automatically transfer to unknown,
rare, damaged, disputed, or hapax cases. The domain card compares frequency,
damage, period, source family, context availability, claim type, and label
exposure. A case outside support becomes `out_of_calibration_domain`; it may
retain a score but must not display a discovery probability or be released.

已释字上的校准不能自动外推到未释字、罕见字、残损字、争议字或孤例。
适用域说明要比较频率、残损、时期、来源家族、上下文可得性、命题类型和
标签暴露。超出支持域的案件标为 `out_of_calibration_domain`；它可以保留
分数，但不能显示发现概率，也不能交付。

Release also requires:

- at least two independent evidence families;
- complete provenance and source-dependency review;
- no unresolved hard counterexample;
- no critical label, train-test, time, or derivative leakage;
- consistent reruns with their dependence axes declared;
- a rights status that permits the proposed delivery form;
- an explicit alternative and an explicit abstention option.

交付还要求：

- 至少两个独立证据家族；
- 来源与来源依赖复核完整；
- 没有未解决的致命反例；
- 没有关键标签、训练测试、时间或派生泄漏；
- 已声明依赖轴的复跑结果一致；
- 权利状态允许计划中的交付形态；
- 明确列出替代命题和弃权选项。

Two evidence families are necessary, not sufficient. Claim-specific blockers
also apply:

The complete claim-by-claim mandatory-evidence and blocking matrix is the
[claim evidence gate matrix][claim-evidence-matrix]. It is normative for
human dossiers and AI adjudication; the lists below are its short summary.

完整的逐命题必需证据与阻断矩阵见[命题证据门槛矩阵][claim-evidence-matrix]。
它同时约束人类档案和 AI 裁决；下列内容只是该矩阵的简要摘要。

- object identity requires visible material or an authorized surrogate,
  stable catalog identity, and a checksum-bound source trail;
- glyph or variant relation requires damage-aware comparable forms,
  near-form alternatives, and non-label-derived support;
- reading, semantic, or grammatical claims require the full available
  inscription, exact occurrence, neighbours, grammar, archaeology or catalog
  context, reading history, and positive and negative evidence;
- diachronic claims require period-provenanced forms and a bridge beyond later
  visual resemblance;
- a complete decipherment proposition requires every applicable minimum item
  in the repository research-methods policy.

两个证据家族只是必要条件，不是充分条件。还要应用命题级阻断矩阵：

- 对象身份要求可见实物或获准替代物、稳定著录身份和 checksum 绑定的
  来源链；
- 同字或异体关系要求考虑残损的可比字形、近形替代和非标签派生支持；
- 读音、语义或语法主张要求全部可得卜辞、精确字例、邻字、语法、考古
  或著录上下文、释读史以及正反证；
- 历时主张要求有时期来源的字形，以及超越后世视觉相似的桥梁；
- 完整释读命题要求满足仓库研究方法政策中全部适用的最小证据项。

A missing mandatory item blocks delivery. Missing non-mandatory evidence may
remain only when the verdict states its effect and a concrete next source.

任何必需项缺失都会阻止交付。非必需证据可以缺失，但裁决书必须说明其
影响和下一项具体来源。

## 12. Benchmark And Leakage Control / 基准与泄漏控制

The benchmark must contain four case types:

1. masked known readings for retrospective discovery;
2. historically disputed cases with dated evidence cutoffs;
3. null and negative controls where abstention is correct;
4. hard challenge cases involving damage, rare forms, proper names, or
   misleading context.

基准必须包含四类案件：

1. 隐藏答案的已释字，用于回溯式重新发现；
2. 设置文献时间截点的历史争议案；
3. 正确答案应为弃权的空白与负对照；
4. 涉及残损、罕见形、专名或误导语境的困难挑战案。

Splits must be made by family, not random rows. Family keys include glyph,
variant cluster, bone or fragment, inscription, source ancestor, catalog
derivative, and image-derivative lineage.

数据切分必须按家族完成，不能随机切行。家族键包括字形、异体簇、原骨或
残片、卜辞、来源祖先、著录派生链和图像派生链。

Each benchmark case needs a blind alias, allowed-evidence snapshot, source
checksums, time cutoff, forbidden-leakage list, and a keyed gold commitment.
A plain hash is forbidden for low-entropy answers. Use HMAC-SHA-256 or an
equivalent commitment with a scorer-only secret stored outside Git.

每个基准案件都要保存盲别名、允许证据快照、来源 checksum、时间截点、
禁止泄漏清单和带密钥的答案承诺。低熵答案禁止使用裸 hash。应使用
HMAC-SHA-256 或同等承诺，评分器专用密钥放在 Git 之外。

Predictions and adjudication are locked before an isolated scorer opens gold.
After opening, the case is retired from final holdout use; later runs are
diagnostic only, and a new sealed holdout must replace it.

预测和裁决必须先锁定，再由隔离评分器开启答案。答案开启后，该案例退出
最终留出集；后续运行只能作为诊断，并由新的封存留出案替换。

Prompt masking cannot remove answers already present in model weights.
Every case records training-cutoff evidence or `pretraining_exposure=unknown`.
Retrospective known-answer cases with unknown exposure test the workflow but
cannot calibrate new-discovery probability. Only an auditable clean holdout,
such as private post-cutoff material, may support that claim.

提示词遮蔽不能移除模型权重中已经存在的答案。每案必须记录训练截止证据，
或标记 `pretraining_exposure=unknown`。预训练暴露未知的回溯已知答案案只能
测试工作流，不能校准新发现概率。只有可审计的干净留出集，例如训练截止
后的私有材料，才可以支持该概率主张。

Required metrics are top-1 and top-k accuracy, Brier score, log loss,
expected calibration error with intervals, reliability curves, coverage-risk,
abstention quality, falsification survival, and rerun agreement.

必需指标包括 top-1、top-k、Brier score、log loss、带区间的 ECE、
可靠性曲线、coverage-risk、弃权质量、反证存活率和复跑一致率。

## 13. Falsification And Reopening / 反证与重开

Every case must pre-register what would count against it. Minimum attacks are:

- the strongest near-form competitor;
- a context swap and a wrong-context control;
- removal of the strongest source family;
- image masking, damage sensitivity, and derivative duplication checks;
- period, group, findspot, and formula counterexamples;
- later-form similarity without contextual support;
- literature that proposes a materially different explanation;
- an attempt to explain the same evidence with an unknown or null answer.

每案必须预登记什么证据会反对它。最低攻击集包括：

- 最强近形竞争字；
- 语境交换和错误语境对照；
- 移除最强来源家族；
- 图像遮挡、残损敏感性和派生重复检查；
- 时期、组类、出土地和辞例反例；
- 只有后世字形相似而缺少语境支持的情况；
- 提出实质不同解释的文献；
- 用未知或空答案解释同一证据的尝试。

A single hard provenance, identity, leakage, or rights defect may withhold a
candidate even when other scores are high. Negative results are retained as
research assets.

即使其他分数很高，一个致命来源、身份、泄漏或权利缺陷也可以扣留候选。
负结果必须作为研究资产保留。

## 14. Human-Readable Delivery Package / 人类可读交付包

Every user-facing candidate directory must lead with a readable verdict and
keep machine files beside it as support. It must contain:

- the exact proposition in plain Chinese and English;
- the result state and calibrated probability with interval;
- ranked alternatives and abstention probability;
- the visible glyph, rubbing, plate, and occurrence context;
- catalog numbers, collection, find spot, period, group, and source trail;
- the reasoning chain by morphology, context, archaeology, and literature;
- independent support families and their dependency graph;
- the strongest counterevidence and all unresolved disagreements;
- each court's sealed initial judgment and cross-examination record;
- falsification tests, ablations, negative controls, and rerun outcomes;
- model, prompt, tool, version, seed, input checksum, and case manifest;
- calibration cohort, threshold source, metrics, and leakage audit;
- exact conditions for downgrade, withdrawal, or reopening;
- concrete missing evidence and the next highest-value source to open.

每个面向用户的候选目录都必须以可读裁决书为入口，机器文件只在同目录
提供辅助。内容必须包括：

- 用清楚中文和英文写出的精确命题；
- 结果状态、带区间的校准概率；
- 排序后的替代命题与弃权概率；
- 可见字形、拓片、图版和字例上下文；
- 著录号、馆藏、出土地、时期、组类和来源链；
- 形体、语境、考古和文献四类推理链；
- 独立支持证据家族及其依赖图；
- 最强反证和全部未解决分歧；
- 各法庭密封初判和交叉质询记录；
- 反证测试、消融、负对照和复跑结果；
- 模型、提示词、工具、版本、seed、输入 checksum 和案件 manifest；
- 校准群、阈值来源、指标和泄漏审计；
- 降级、撤回或重开的精确条件；
- 具体缺失证据和下一项最高价值待查来源。

Large raw materials remain in ignored or external archives according to
repository policy. The delivery package records their checksums, rights,
manifests, extraction routes, and reproducible derivatives.

大型原始资料继续按仓库政策保存在忽略区或外部归档。交付包记录其
checksum、权利、manifest、抽取路线和可复核派生物。

## 15. Source Roles / 来源角色

Source value depends on the proposition being tested:

- IHP and museum object pages are preferred for artifact identity,
  collection, catalog, and stable institutional provenance.
- HUST-OBC is preferred for broad visual candidate discovery, with duplicate
  category and label-leakage caution.
- OBIMD is preferred for bounding boxes, sentence groups, reading order, and
  contextual recovery, subject to its rights and dependency review.
- EvoBC is preferred for generating diachronic comparison candidates, not for
  proving an evolution chain by itself.
- Xiaoxuetang and other databases are discovery and crosswalk routes whose
  underlying sources must be opened before a claim is counted independently.
- published scholarship supplies dated claims, proposers, arguments,
  objections, and disputes; a citation is not the same as agreement.

来源价值取决于正在检验的命题：

- IHP 和博物馆对象页优先用于实物身份、馆藏、著录和稳定机构来源；
- HUST-OBC 优先用于广泛视觉候选发现，但要警惕重复类别和标签泄漏；
- OBIMD 优先用于字框、句组、阅读顺序和上下文恢复，但要先解决权利与
  依赖复核；
- EvoBC 优先用于生成历时候选，不能单独证明演化链；
- 小学堂等数据库用于发现和 crosswalk，必须打开其底层来源后才能作为
  独立证据计数；
- 已发表研究用于记录有日期的主张、提出者、论据、反对和争议，引用不
  等于赞同。

## 16. Gate-Based Roadmap / 门槛式路线图

The roadmap has no weekly quota and no artificial deadline. A stage ends only
when its exit evidence exists.

路线图不设每周配额，也不设置人为时间限制。只有出现可核验的退出证据，
阶段才算完成。

### Gate 0: Strategic authority / 战略权威

- establish this document as the single normative strategy;
- mark earlier architecture plans as historical drafts;
- connect the preprocessing closure to the new execution baseline.

Exit: one unambiguous strategy, readable in both languages.

退出条件：只有一份明确、中英可读的规范性战略。

### Gate 1: Truth and provenance integrity / 事实与来源完整性

- repair validators that can falsely pass;
- correct baseline direction and add deletion and growth regressions;
- reconcile rights statements without inventing a licence;
- repair package-to-download routes and missing manifest coverage;
- build source-ancestor and derivative dependency records;
- split route confidence from hypothesis probability.

Exit: no known critical provenance or false-pass defect can reach an
experiment.

退出条件：已知关键来源缺陷或假通过缺陷都不能进入实验。

### Gate 2: Blind benchmark and calibration / 盲测基准与校准

- create sealed known-answer, disputed, null, and challenge sets;
- enforce family, source, time, and derivative separation;
- separate clean holdouts from pretraining-exposure-unknown diagnostics;
- define calibration domains and mandatory OOD withholding;
- implement probability, abstention, calibration, and risk metrics;
- pre-register task-specific release thresholds.

Exit: an auditable clean holdout supports the claimed probability semantics
inside a declared domain. Otherwise the numerical channel remains withheld.

退出条件：可审计干净留出集只在已声明适用域内支持所称概率。否则数值
通道继续扣留。

### Gate 3: Autonomous laboratory MVP / 自主实验室最小闭环

- run two blinded courts, adversarial review, provenance review, rerun, and
  final adjudication;
- bind a fresh final adjudicator runtime outside the research-court model
  families, with sealed gold and complete locked-run inputs;
- save complete human and machine case records;
- prove that abstention, withholding, reopening, and withdrawal work.

最终裁决必须绑定全新运行，其模型家族不得属于研究法庭，并保持 gold
封存、完整绑定所有锁定运行输入。

Exit: at least one eligible holdout and one negative control are reproduced
end to end with no known route leakage and explicit pretraining status.

退出条件：至少一个合格留出案和一个负对照端到端复现，没有已知路线
泄漏，并明确记录预训练暴露状态。

### Gate 4: Deep pilot cases / 少量深度试点

- choose cases with visible evidence, recoverable context, useful source
  intersections, and strong negative controls;
- prefer a few complete cases over thousands of shallow packets;
- publish failure cases and calibration drift beside successes.

Exit: dependency-labelled reruns and counterevidence review support stable
operation.

退出条件：标明依赖关系的复跑与反证复核证明系统可以稳定运行。

### Gate 5: Live candidate discovery / 真实候选发现

- open previously unknown or unresolved cases;
- release only in-domain candidates that pass every registered gate;
- send qualifying candidates directly to the user;
- retain all other outcomes as hypotheses, abstentions, or negative findings.

Exit: each delivered candidate is reproducible, dependency-labelled, and
auditable.

退出条件：每个已交付候选都能复现、标明依赖并接受审计。

### Gate 6: Expansion and external scrutiny / 扩展与外部检验

- expand source families and task families only when calibration holds;
- compare with new scholarship and tools without leaking future answers;
- optionally seek external scholarly review or publication;
- never make external review a blocker for user delivery.

Exit: expansion does not degrade calibration, provenance, or readability.

退出条件：扩展不降低校准、来源或人类可读质量。

## 17. Success Metrics / 成功指标

File and directory counts are operational diagnostics, not success metrics.
The strategic dashboard should report:

- proportion of cases with opened images, contexts, catalogs, and sources;
- proportion of evidence grouped into independent source families;
- unresolved identity, rights, and provenance blockers;
- retrieval recall on sealed evidence routes;
- top-1, top-k, Brier, log loss, ECE, and reliability intervals;
- coverage-risk and abstention quality;
- survival after falsification and source ablation;
- rerun agreement by independence tier and adjudicator stability;
- high-confidence error rate and calibration drift;
- number of user-delivered candidates that meet every gate;
- time and evidence needed to reopen or withdraw an incorrect candidate.

文件数和目录数只是运行诊断，不是成功指标。战略看板应报告：

- 已打开图像、上下文、著录和来源的案件比例；
- 已归并到独立来源家族的证据比例；
- 未解决身份、权利和来源阻断；
- 封存证据路线上的检索召回率；
- top-1、top-k、Brier、log loss、ECE 和可靠性区间；
- coverage-risk 与弃权质量；
- 经反证与来源消融后的存活率；
- 分独立等级的复跑一致率和裁判稳定性；
- 高置信错误率与校准漂移；
- 满足全部门槛并提交给用户的候选数量；
- 错误候选被重开或撤回所需的时间与证据。

No target requires a candidate to be produced. A well-supported abstention is
better than an uncalibrated discovery claim.

任何指标都不得强迫系统产出候选。证据充分的弃权优于未经校准的发现
主张。

## 18. Immediate Implementation Order / 立即实施顺序

Use the [current operating baseline][current-baseline] to select a few
decisive propositions. Open their next falsifying source while independently
preparing a family-isolated known-answer cohort, negative control, leakage
audit, and external scoring route. Do not wait for bulk coverage and do not
open the live delivery channel before the calibration gates pass.

按[当前运行基线][current-baseline]选择少量决定性命题，打开其下一项可证伪
来源；同时独立准备来源家族隔离的已知答案群、负对照、泄漏审计和外部
评分路线。不得等待批量覆盖，也不得在校准门槛通过前开放真实交付通道。

Model training, a web application, mass evidence-pack generation, and broad
schema migration are explicitly deferred until the benchmark and laboratory
gates justify them.

模型训练、Web 应用、批量 evidence pack 和大范围 schema 迁移，明确延后
到基准与实验室门槛证明其必要性之后。

This sequence does not grant standing permission for unrelated repository,
external-service, or publication changes. Each implementation remains within
the user's active task authorization.

本顺序不构成对无关仓库修改、外部服务操作或发表行为的长期授权。每项
实施仍须处于用户当前任务授权范围内。

## 19. Repository Boundaries And Links / 仓库边界与链接

The current operating baseline is an operational companion, not a second
normative strategy. Older audits remain historical receipts.

当前运行基线是运行配套文件，不是第二份规范性战略。旧审计保留为历史
回执。

Normative companion policies:

- [project positioning](../001_project-positioning-and-research-boundaries/)
- [source rights and provenance](../002_source-rights-and-provenance-policy/)
- [research methods](../004_oracle-bone-script-research-methods/)
- [evidence-pack schema](../../../schemas/006_ai-agent-evidence-pack-schema/)
- [benchmark experiment v2 schema][benchmark-v2]
- [evidence-pack review skill](../../../skills/ai-agent-evidence-pack-review/)
- [English root README](../../../README.md)
- [Chinese root README](../../../README.zh-CN.md)

The historical preprocessing snapshot is file
`230_preformal-research-preprocessing-closure.md` under the
[statistics directory](../../../corpus/009_statistics-and-derived-features/).

Source-object evidence dossiers are under the
[source corpus](../../../corpus/006_research-sources-and-bibliography/).
Priority source IDs include `src-ihp-oracle-rubbings`, `src-hust-obc`,
`src-obimd`, and `src-evobc`.

AI and user hypotheses remain under `doc/public/user_research/`. Published
scholarship notes remain under `research/`. An `ai_adjudicated_candidate`
does not move automatically between those areas.

AI 与用户假说继续放在 `doc/public/user_research/`，已发表研究笔记继续放在
`research/`。`ai_adjudicated_candidate` 不会自动跨越这两个研究区。

[benchmark-v2]: ../../../schemas/007_ai-agent-benchmark-experiment-schema/
[current-baseline]: 03_current-operating-baseline-2026-08-30.md
[historical-audit]: 01_current-state-audit-2026-08-14.md

## 20. Source Notes / 来源说明

The online sources below were checked for strategic comparison on
`2026-08-09`. They support system and dataset descriptions, not a new oracle-
bone reading.

以下网络来源于 `2026-08-09` 用于战略比较，只支持系统和数据集说明，不
支持任何新的甲骨释读。

[HUST-OBC]: https://www.nature.com/articles/s41597-024-03807-x
[OBIMD]: https://www.nature.com/articles/s41597-026-06967-0
[EvoBC]: https://arxiv.org/abs/2401.12467
[IHP]: https://dap.ihp.sinica.edu.tw/database/3/
[OBI-Bench]: https://arxiv.org/html/2412.01175
[PictOBI-20k]: https://arxiv.org/abs/2509.05773
[OracleAgent]: https://arxiv.org/html/2510.26114
[AlphaOracle]: https://arxiv.org/html/2607.17849
[2026 survey]: https://www.nature.com/articles/s40494-026-02511-w
[LLM calibration]: https://arxiv.org/abs/2403.05973
[conformal shift]: https://arxiv.org/abs/1904.06019
[claim-evidence-matrix]: 02_claim-evidence-gate-matrix.md
