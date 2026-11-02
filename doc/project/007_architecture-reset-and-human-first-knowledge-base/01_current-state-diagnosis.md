# 现状诊断 / Current-State Diagnosis

- 状态 / Status: `diagnosis_2026-11-01`
- 检查对象 / Inspected: 工作树 HEAD `6bf9a9dee42`，1657 次提交
- 方法 / Method: `git ls-files` 统计、目录抽样阅读、prompt 历史对照

本文件只记录仓库审计事实，不涉及任何甲骨文释读判断。

This file records repository audit facts only. It makes no paleographic
claim.

## 1. 一句话结论 / One-Line Verdict

仓库把"目录数量"当成了进展，用模板生成器批量制造了约 50 万个几乎
相同的文件；真正带有研究信息的内容不到总量的千分之一，且被淹没在
模板里。用户 2026-06 至 2026-08 多次纠正的"机器索引说明 + 复核流程
说明"问题，至今没有在结构上解决。

The repository has treated directory count as progress. Template generators
produced roughly half a million near-identical files. Content that carries
real research information is well under one part in a thousand and is buried
inside boilerplate. The problem the user corrected repeatedly between June
and August 2026 has not been fixed structurally.

## 2. 规模事实 / Scale Facts

| 项目 / Item | 数值 / Value |
| --- | --- |
| Git 跟踪文件总数 / tracked files | 517,880 |
| 其中 `corpus/` | 517,182 (99.9%) |
| Markdown 文件 / `.md` | 255,149 |
| JSON/CSV/YAML/JSONL | 240,659 |
| 图片 / images | 21,372 |
| `.git` 目录大小 / size | 931 MiB |
| 测试文件 / 用例 | 131 files / 1,238 tests |
| 提交者 / committers | Codex 1,656; 用户 1 |

各语料区的对象目录数与文件数：

| 语料区 / Area | 对象目录 / dirs | 文件 / files | 每目录文件 |
| --- | --- | --- | --- |
| 001 甲骨单字（HUST 派生）与码位对照 | 12,584 | 210,916 | ~16 |
| 004 字形演化（EvoBC 派生） | 13,714 | 219,565 | ~16 |
| 003 构件候选（OBIMD 派生） | 2,747 | 70,205 | ~25 |
| 002 卜辞 crosswalk 候选 | 622 | 14,256 | ~22 |
| 005 馆藏实物候选 | 58 | 1,113 | ~19 |
| 006 来源对象 | 21 | 540 | ~25 |
| 007 研究专题 | 20 | 323 | ~16 |

`not_collected` 占位值在结构化文件中出现 137,205 次。

对 3,000 个随机 `corpus/` Markdown 的抽样显示：79.8% 的非空行是在 2%
以上文件中逐字重复的模板行，7.1% 是 ID 与状态字段行，只有 13.2% 可能
含有对象特有内容（含被折断的路径片段）。方法与分区数据见
`06_quality-gates-and-metrics.md` 第 6 节。

A sample of 3,000 random corpus Markdown files shows 79.8% verbatim
template lines, 7.1% ID and status field lines, and 13.2% possibly
object-specific lines.

## 3. 文件内容性质 / What The Files Contain

抽读 `corpus/001`、`003`、`004` 任意对象目录，每个目录的 16 至 25 个
文件由同一组脚本生成，内容结构如下：

- 7 至 9 个 Markdown：图像页、人类研究档案、复核单（两份同名重复）、
  上下文档案、考古文字复核、准备度复核、视觉观察、README。
- 每个 Markdown 开头和结尾各有 2 至 4 段"本文件不是释读结论"的边界
  声明，全仓库重复数十万次。
- 正文主体是 `project id`、`external id`、`review status`、`rights
  status` 等字段的反复罗列，同一组字段在同一目录内平均出现 6 遍。
- 唯一的对象特有信息通常只有：一张来源图片的路径与校验和，以及一句
  机器写的视觉描述（例如"狭长直立形，外侧闭合轮廓"）。
- 其余研究栏目（异体、构件、卜辞、著录、出土、释读史、争议、金文）
  全部是"待查：需核对……"的固定句。

因此，用户要求的"打开一个字的目录就能了解该字的全部人类资料"在
10,407 个单字目录中一个都没有实现（001 区另有约 2,177 个码位对照目录，
2026-11-02 复核时更正）。EvoBC 的 13,714 个演化目录连本地
图片都没有，只有外部图片路线编号。

Reading any object directory in `corpus/001`, `003`, or `004` shows 16 to 25
files from one generator. Each Markdown file opens and closes with two to
four boundary disclaimers, repeats the same ID and status fields about six
times per directory, and carries at most one object-specific sentence: a
machine-written visual description of a single source image. Every research
section (variants, components, inscriptions, catalog, findspot, reading
history, disputes, bronze forms) is a fixed "pending" sentence. The user's
requirement that one directory tell a researcher everything known about a
character is met by none of the 12,584 character directories.

## 4. 真正有研究价值的内容 / Where Real Content Exists

以下内容是人工加 AI 逐条核对来源后写成的，值得保留并作为新架构的
样板：

- 3 个活跃案件：`HYZ421`（花东 421 释义争议）、`H2`（OBIMD H2 与
  合集 2 身份）、`obs-unk-005708`（HUST 未释类 50 成员混组问题）。
  位置见 `doc/project/005_*/04_current-operating-baseline-2026-08-30-ihp-anchor.md`。
- 10 个卜辞来源记录候选（史语所 503/771/1215/1222、大英图书馆
  Or.7694/1535 与 1595、大都会 42022/42045、花东 421、OBIMD H2），在
  `corpus/002_oracle-bone-inscriptions/008_source-record-candidates/`。
- 58 个馆藏实物候选（史语所博物馆 52 件、Smithsonian、Penn、Met、
  Cambridge、British Museum），在 `corpus/005_*/002_collection-object-candidates/`。
- 21 个来源对象档案（小学堂、史语所、殷契文渊、HUST-OBC、OBIMD、
  EvoBC、各博物馆），在 `corpus/006_*/001_source-objects/`。
- 9 篇文献档案（HUST-OBC、OBIMD、EvoBC 数据论文，Cambridge Hopkins
  目录，Schwartz 花东专著，Liu 2014 月食，小学堂数据库说明等），在
  `research/001_published-scholarship-index/`。
- 来源登记表、权利冲突复核（OBIMD）、大来源登记、ID 映射表。

这些加起来约 100 个目录、数千行有来源的文字。这是仓库的实际资产。

Roughly one hundred directories hold sourced, individually checked writing:
three active cases, ten inscription source-record candidates, 58 collection
object candidates, 21 source-object dossiers, nine literature dossiers, and
the registries. This is the repository's real asset base.

## 5. 结构性缺失 / Structural Gaps

### 5.1 没有卜辞全文语料

破译依赖语境：同版卜辞、邻字、辞例、句法位置、共现统计、分期分组。
仓库中没有一条可逐行定位的卜辞释文。622 个卜辞候选只有著录号
crosswalk，没有全文、OCR 或图版。没有卜辞文本，就不可能做任何"某字
出现于哪些卜辞、与哪些字共现"的分析，知识图谱也无法回答研究问题。

No line-addressable inscription transcription exists in the repository.
Without inscription text, no contextual, co-occurrence, or distributional
analysis is possible, and the knowledge graph cannot answer any research
question.

### 5.2 图谱是"路线边"，不是"研究关系边"

现有 14 个图边文件的边类型是 `CHARACTER_HAS_LOCAL_GLYPH_ASSET_CANDIDATE`、
`CHARACTER_HAS_HUST_OBC_CODEPOINT_LOOKUP_ROUTE` 一类的文件路线关系。
没有 `occurs_in`（字出现于卜辞某位）、`co_occurs`、`variant_of`、
`component_of`、`reading_proposed_by`、`disputed_by`、`same_bone`、
`same_pit` 等学术关系。图谱对研究者没有用处。

Existing graph edges describe file routes, not scholarly relations.

### 5.3 已释字没有释读史与例句

1,588 个 HUST 已释类目录里，没有一个记录"谁在哪年提出此释读、依据
是什么、谁反对、现在学界怎么看"，也没有一条带出处的卜辞例句。
这恰恰是"已释字"之所以是已释字的全部理由。

None of the 1,588 deciphered-class directories records who proposed the
reading, when, on what grounds, who disagreed, or one sourced example
sentence.

### 5.4 字形在文档中被今字和乱码替代

HUST 来源文件名里的隶定字和扩展区 Unicode（如 `𠂤歷間`、`？`）被原样
抄进 Markdown。读者看到的是乱码或现代字，不是甲骨字形。字形只能
以图呈现；今字只能是带状态的"候选对应"字段。

Glyphs appear as liding characters and extension-block Unicode copied from
source filenames, not as images.

### 5.5 治理文档超过了研究内容

`doc/project/005_*/README.md` 有 1,289 行，定义了双盲法庭、独立裁决
Agent、HMAC 答案承诺、校准阈值预登记等机制。这些机制针对的是 Gate 5
"真实候选交付"阶段；而当前 Gate 2 到 6 全部 `BLOCKED` 或 `CLOSED`。
日常工作需要的是"怎样把一个字的档案写出来"，而这份文档没有回答。

The 1,289-line adjudication strategy governs a delivery stage that every
gate snapshot marks as blocked or closed. It does not tell an agent how to
write one character dossier, which is the work actually needed now.

### 5.6 工程负担阻碍迭代

- 50 万文件使 `git status`、`du`、`ls -R`、全文搜索在本机需要数分钟。
- 1,238 个测试里大量按单个对象编写（`test_obs_char_000963_*`），任何
  档案格式调整都会连锁失败；`tmp/` 中保留了分批运行全量测试的日志，
  说明全量测试已经不能一次跑完。
- `corpus/009` 有 239 个文件，其中约 200 个是 AI 队列、scaffold、
  handoff、route pack；`doc/public/user_research/002` 到 `010` 也是同
  类队列。这些是 Agent 的工作台残留物，不是研究资料。

Half a million files slow every repository operation. Per-object tests make
format changes cascade. About two hundred AI queue and scaffold files in
`corpus/009` and `doc/public/user_research/` are agent workbench residue.

### 5.7 零散问题

- `corpus/001/.../035_undeciphered-001900_*` 和 `063_*oracle-characters-
  candidates` 是重复或拼写不一致的分桶目录。
- 根目录下存在未跟踪空目录 `008_source-record-candidates/`，应删除。
- `apps/`、`database/` 只有 README 占位，当前阶段无内容。
- `doc/public/user_prompt/` 内三个中文文件名在 Git 中以转义字节显示，
  与 ASCII 路径规则冲突。
- 80 字符换行规则被机械应用，在多处把文件路径从中间折断，使路径
  无法复制和点击。

## 6. 根因 / Root Causes

1. 把"每个对象必须同时有人类档案和 AI 文件"理解成"每个对象先建满
   一套模板"，而不是"有内容才建目录"。
2. 用生成器批量生产"人类可读"文件，而人类可读与否取决于内容，不取决
   于文件后缀。
3. 没有可度量的内容门禁，校验脚本只检查结构、路径和字段存在。
4. 治理设计先于研究实践，用门槛和合同代替了样板档案。
5. 提交节奏按"每批 4 个候选写一次视觉观察"推进，1,600 多次提交
   没有一次要求回答"研究者能用这个目录做什么"。

Root causes: "every object needs human and AI files" was read as "every
object gets a full template set"; readability was equated with file type;
validators checked structure but never content; governance preceded
practice; and commit cadence rewarded batch size over usefulness.
