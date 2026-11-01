# 目标架构 / Target Architecture

- 状态 / Status: `proposed_normative_architecture`
- 适用范围 / Scope: 仓库全部研究资料的组织方式、价值单位、分层和
  目录形态

## 1. 使命与价值单位 / Mission And Unit Of Value

使命不变：在 AI 协助下破解未释甲骨文。实现路径是建一座人类可读、
来源可追溯、机器可推理的甲骨文知识库，再让强推理模型在知识库证据上
提出和检验假说。

The mission is unchanged: decipher undeciphered oracle bone graphs with AI
assistance, by building a human-readable, source-traceable, machine-
reasonable knowledge base and letting strong reasoning models form and test
hypotheses on its evidence.

从本架构起，仓库的价值单位只有四种，其余一切都是辅助：

| 价值单位 / Unit | 定义 / Definition |
| --- | --- |
| 单字档案 | 一个甲骨字（已释或未释）的全部已知研究资料，一份文件 |
| 卜辞记录 | 一条有著录号、全文、来源、分期的卜辞文本 |
| 有来源的主张 | 一条"谁、何时、在哪、主张什么、依据什么"的学术记录 |
| 研究案件 | 一个明确命题及其证据、反证和当前裁决状态 |

目录数、文件数、字段数、索引行数、图边数、队列长度都不是进展。

From now on the repository has four units of value: a character dossier, an
inscription record, a sourced claim, and a research case. Counts of
directories, files, fields, index rows, graph edges, or queues are not
progress.

## 2. 五层结构 / Five Layers

```text
L4  研究案件层   doc/public/user_research/cases/  假说、证据、反证、裁决
L3  学术主张层   research/                         释读史、文献、争议
L2  关系图谱层   corpus/008 + 009                  学术关系边与统计
L1  知识对象层   corpus/001-007                    单字、卜辞、实物、来源
L0  来源与权利层 project_registry/ + corpus/006   登记、权利、校验和
```

- L0 回答"这条资料从哪来、能不能用"。
- L1 回答"关于这个字 / 这片甲骨 / 这条卜辞，我们知道什么"。
- L2 回答"它和别的对象有什么关系、分布如何"。
- L3 回答"学者们说过什么、争在哪里"。
- L4 回答"我们现在提出什么命题、证据够不够、结论是什么状态"。

每层只能引用它下面的层。L4 的案件引用 L1 到 L3 的具体文件；L2 的边
必须指向 L1 的记录和 L0 的来源行。任何一层都不能用模板代替内容。

Each layer may cite only the layers below it. A case cites dossiers, claims
and edges; an edge points to records and source rows. No layer may
substitute templates for content.

## 3. 知识对象模型 / Knowledge Object Model

### 3.1 对象类型

| 对象 / Object | ID 前缀 | 身份锚点 / Identity anchor |
| --- | --- | --- |
| 甲骨字（已释候选） | `obs-char-` | 外部字头号（小学堂 / HUST 类号） |
| 甲骨字（未释候选） | `obs-unk-` | 外部未释类号 |
| 甲骨实物 | `obs-bone-` | 馆藏号 + 著录号（合集号优先） |
| 卜辞 | `obs-insc-` | 著录号 + 片内序号（如 合 14496.1） |
| 构件 | `obs-comp-` | 项目内编号，锚定到字例 |
| 来源 | `src-` | 机构或数据集 |
| 文献 | `lit-` | DOI / ISBN / 书目 |
| 主张 | `claim-` | 文献 + 页码 + 命题 |
| 案件 | `case-` | 命题文本 |

现有 `obs-insc-cw-cand-`、`obs-insc-src-cand-`、`coll-obj-cand-`、
`obs-evo-cand-`、`obs-comp-cand-` 等候选前缀继续有效，但新建对象只
在有实质内容时才建目录（见第 5 节）。

### 3.2 核心关系（图谱边类型）

图谱必须能回答研究者的问题，因此边类型改为学术关系：

```text
occurs_in         字 -> 卜辞 (位置序号, 是否残缺)
co_occurs         字 <-> 字 (同条卜辞, 距离)
variant_of        字 -> 字 (异体 / 同字异写, 依据)
near_form_of      字 -> 字 (近形, 区别特征)
component_of      构件 -> 字 (位置, 依据)
same_bone         卜辞 <-> 卜辞 (同版)
same_pit          实物 <-> 实物 (同坑 / 同批)
dated_to          实物 / 卜辞 -> 分期 / 组类 (依据: 五期 / 组类)
inscribed_on      卜辞 -> 实物
held_by           实物 -> 馆藏
published_in      实物 / 卜辞 -> 著录 (卷, 页, 图版号)
reading_proposed  字 -> 释读 (学者, 年份, 文献, 页)
reading_disputed  释读 -> 释读 (反对者, 文献)
corresponds_to    字 -> 金文 / 小篆 / 楷书 (依据, 状态)
derives_from      任意 -> 来源 (来源行, 校验和)
```

每条边必备字段：`source_ref`（来源行或文献定位）、`status`
（`source_reported` / `candidate` / `disputed` / `accepted_by_source`）、
`note`。没有 `source_ref` 的边不得写入图谱。

现有 `CHARACTER_HAS_*_ROUTE` 类文件路线边降级为工具内部索引，不再
算作图谱内容。

Edge types become scholarly relations. Every edge carries a source
reference, a status, and a note; route edges are demoted to tool indexes.

## 4. 单字档案的形态 / Shape Of A Character Dossier

一个单字目录只有三样东西：

```text
001_obs-char-000001_hust-obc-cat-0001_oracle-character/
  README.md        单字档案（人读；全部已知资料，一份）
  record.json      机读记录（字段化同一内容 + 图边 + 来源行）
  images/          字形图片、拓片裁片、摹本（每张配 .yaml 来源）
```

`README.md` 的章节顺序固定为研究者的阅读顺序：

1. 字形（图）与字形观察
2. 隶定与今字候选（带状态与依据）
3. 释读史（谁、何时、文献、依据、反对意见、当前共识状态）
4. 卜辞例句（著录号、全文、该字位置、分期、出处）
5. 分布（出现次数、分期分组、辞例类型、共现字）
6. 异体、近形、构件
7. 金文、小篆、后世字形对应
8. 实物、出土、馆藏
9. 争议与未决问题
10. 来源与权利
11. 具体待查项（每项是一个可执行的问题，不是"待查"二字）

这些章节如果没有内容，就不出现；不写"待查：需核对……"的空句。
档案开头只允许一行状态：`状态：已释候选 | 复核：部分 | 更新：日期`。
仓库级边界声明写在 `corpus/README.md`，对象档案不重复。

A character directory holds one `README.md`, one `record.json`, and an
`images/` folder. Sections that have no content are omitted. One status line
replaces repeated disclaimers.

卜辞记录、实物档案、来源档案、文献档案采用同样的"一份人读 + 一份
机读 + 资产"形态，章节见 `03_object-dossier-standard.md`。

## 5. 按需建目录 / Directories On Demand

对象只有在满足下列条件之一时才拥有自己的目录：

- 有至少一张本地可见图片，且有至少 3 条对象特有的、带来源的事实；
- 或有至少一条带全文和出处的卜辞例句；
- 或是活跃研究案件的对象。

不满足条件的对象只存在于语料区的登记表（CSV / JSONL）和图片库中。
登记表一行即是它的全部记录。研究者要找它时，查表，不查目录。

An object gets a directory only when it has a visible image plus at least
three sourced object-specific facts, or one sourced example sentence, or an
active case. Otherwise it lives as one row in the area register.

## 6. 卜辞语料层 / Inscription Text Layer

这是当前缺失的核心。目标形态：

```text
corpus/002_oracle-bone-inscriptions/
  000_inscription-registers/            索引、crosswalk、分期对照
  010_inscription-texts/                卜辞释文语料（新建）
    heji-00001-01000/
      inscriptions.jsonl                 每行一条卜辞：著录号、片内序号、
                                         释文、分期、组类、来源、权利
      inscriptions.md                    由 jsonl 渲染的人读对照表
    heji-01001-02000/ ...
  020_bone-dossiers/                     有实质内容的甲骨实物目录
```

释文字段：`catalog_id`、`sub_no`、`text_source_form`（来源原文）、
`text_normalized`（规范化隶定）、`glyph_positions`（字位 -> 字 ID 或
未释标记）、`period`、`group`、`topic`、`source_ref`、`rights_status`、
`text_quality`。

来源优先级与权利判断见 `04_consolidation-and-migration-plan.md`。

The inscription text layer is the missing core. It is stored as JSONL per
catalog bucket, rendered to a human-readable table, with per-glyph position
links to character IDs.

## 7. AI 推理层如何用这座库 / How The AI Layer Uses It

模型不替代知识库，模型在知识库上推理。标准输入是一个"证据包"：

```text
未释字 X 的证据包
  字形图片（全部字例裁片）
  每条出现卜辞的全文、字位、分期、组类、主题
  共现字统计、位置统计、分期分布
  近形字、同构件字及其释读
  同版 / 同坑其他卜辞
  已有学者意见（若有）
  金文 / 小篆中的可比形
```

输出是一份人读案件文件：命题、候选解释排序、每个候选的支持证据与
反证、可推翻条件、下一个最有价值的待查来源。案件标准见
`05_ai-agent-operating-protocol.md`。

校准方法：先用已释字做盲测（隐去释读，只给证据包），统计模型命中率
与弃权质量。这既检验模型，也检验知识库是否够用。只有证据包能让模型
"重新发现"大多数已释字时，才有理由相信它对未释字的判断。

Calibrate by masking known readings and checking whether the evidence pack
alone lets the model rediscover them. This tests the model and the knowledge
base at once.

## 8. 不做的事 / Non-Goals For This Stage

- 不训练模型，不建向量索引，不建 Web 应用，不建数据库服务。
- 不批量生成任何对象目录、模板、队列、scaffold。
- 不把数据集标签、文件名里的今字、码位当作释读。
- 不在校准完成前显示任何"破译概率"。

No model training, vector index, web app, or database service; no batch
generation; no labels-as-readings; no probability display before
calibration.
