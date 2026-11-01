# 架构重置：以人类可读知识库为中心 / Architecture Reset: Human-First Knowledge Base

- 状态 / Status: `proposed_architecture_reset_2026-11-01`
- 作者 / Author: Claude Fable 5.1，按用户 2026-11-01 的任务要求写出
- 权威性 / Authority: 用户确认后成为当前阶段的规范性架构。与
  `doc/project/005_*` 的关系：005 规定未来候选交付的门槛；本目录规定
  现在怎样把知识库建起来。两者不冲突，但日常工作以本目录为准。

## 为什么要重置 / Why Reset

项目目标是在 AI 协助下破解甲骨文。实现它需要一座人类可读、来源可
追溯、机器可推理的甲骨文知识库。过去五个月的工作把这个目标偏成了
"批量生成目录"：仓库现有 517,880 个跟踪文件，其中 99.9% 在 `corpus/`，
由模板脚本生成，每个对象目录 16 到 25 个文件，内容是重复的 ID 字段、
边界声明和"待查"固定句。真正带研究信息的内容约 100 个目录，被淹没在
模板中。没有一条卜辞全文，没有一条释读史，没有一条学术关系图边。

用户在 2026-06 至 2026-08 的 prompt 中多次指出同一问题："全是机器索引
说明加复核流程说明"。问题没有解决，因为它是结构性的：生成器、校验
脚本、测试和提交节奏都在奖励"多建目录"。

The project aims to decipher oracle bone script with AI assistance, which
requires a human-readable, traceable, machine-reasonable knowledge base.
Five months of work drifted into bulk directory generation: 517,880 tracked
files, 99.9% template output, zero inscription texts, zero reading
histories, zero scholarly graph edges. The user flagged this repeatedly. It
persisted because generators, validators, tests, and commit cadence all
rewarded directory count.

## 核心决定 / Core Decisions

1. 价值单位改为四种：单字档案、卜辞记录、有来源的主张、研究案件。
   目录数和文件数不再是进展。
2. 一个对象一份人读档案（`README.md`）加一份机读记录
   （`record.json`）加资产目录。现有每目录 7 到 9 份模板 Markdown
   合并为一份。
3. 按需建目录：对象没有至少 3 条有来源的特有事实或一条带出处的
   例句，就只在登记表中占一行，不建目录。
4. 折叠 EvoBC、OBIMD 构件、卜辞 crosswalk 三类无内容生成目录
   （约 30 万文件）为登记 CSV；合并单字目录（约 17 万文件）。Git
   历史保留一切。
5. 补上缺失的核心：卜辞释文语料层。先做《合集》1 至 1000 号试点。
6. 图谱边改为学术关系（出现于、共现、异体、构件、释读提出、释读
   争议、对应后世字形），每条带来源与状态。
7. 100 字深度试点先于任何规模扩展；试点完成后做第一次已释字盲测，
   用结果决定扩展与否。
8. 内容门禁写成脚本：实质内容行比例、单档案规则、禁止固定句、
   禁止批量生成。结构校验之外加内容校验。
9. 005 的法庭与裁决机制保留为交付阶段规则；当前阶段按
   `05_ai-agent-operating-protocol.md` 工作。

## 文档地图 / Document Map

| 文件 | 内容 | 读者 |
| --- | --- | --- |
| [01 现状诊断](01_current-state-diagnosis.md) | 仓库审计事实、规模、内容性质、根因 | 用户、所有 Agent |
| [02 目标架构](02_target-architecture.md) | 价值单位、五层结构、对象模型、图谱边、目录形态、AI 推理层 | 所有 Agent |
| [03 对象档案标准](03_object-dossier-standard.md) | 一份档案必须是什么样；章节；禁止清单 | 写档案的 Agent |
| [04 收缩与迁移计划](04_consolidation-and-migration-plan.md) | 六步计划、来源优先级、风险与决定点 | 用户决策 |
| [05 AI Agent 工作协议](05_ai-agent-operating-protocol.md) | 每次任务怎么做；案件与盲测；防走偏硬规则 | 所有 Agent |
| [06 质量门禁与度量](06_quality-gates-and-metrics.md) | 13 条门禁、仓库度量、成功判据、基线 | 实现校验的 Agent |

## 需要用户决定的事 / Decisions For The User

| 决定 | 建议 |
| --- | --- |
| 批准折叠约 47 万生成文件（历史保留） | 批准 |
| 批准把 005 定位为"交付阶段规则"，日常以 007 为准 | 批准 |
| OBIMD 使用方式 | 已决定：个人研究本地直接使用；公开仓库只放 ID、统计和少量引用 |
| 是否注册殷契文渊账号供 Agent 登录检索 | 建议注册 |
| 是否重写 `.git` 历史以缩小 931 MiB | 暂不 |

## 下一步 / Next Steps

批准后的执行顺序见 `04_consolidation-and-migration-plan.md`：冻结
生成器与队列，折叠无内容目录，重构测试，建卜辞语料试点，100 字深度
试点，重建图谱。每步独立校验、提交、推送。

After approval, follow the six steps in the migration plan: freeze
generators, collapse content-free directories, restructure tests, build the
inscription pilot, run the hundred-character pilot, rebuild the graph.
