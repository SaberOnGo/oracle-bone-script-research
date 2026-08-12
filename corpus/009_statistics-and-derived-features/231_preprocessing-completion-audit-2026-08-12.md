# Preprocessing Completion Audit / 资料预处理完成度审计

## Status / 状态

- Audit date / 审计日期: `2026-08-12`
- Audit result / 审计结论: `not_complete`
- Research status / 正式研究状态: `not_started`
- Candidate delivery / 候选交付: `none`

This audit tests the current repository against the nineteen preprocessing
requirements. It supersedes any interpretation that directory counts or
passing structural checks alone prove that the materials are complete.

本审计按十九项预处理要求核对当前仓库。它纠正一种误读：目录数量或结构
校验通过，本身不能证明研究资料已经完整。

The historical closure snapshot remains useful as a record of infrastructure
coverage. Its `2026-08-07` counts are not evidence that every image, text,
catalog, bibliography, or dispute record has been opened and reviewed.

历史闭合快照仍可用于了解基础设施覆盖，但其中 `2026-08-07` 的数量不能
证明每张图像、每篇卜辞、每条著录、每份文献或每项争议已经打开复核。

## Decisive Findings / 决定性发现

### Character images / 单字图像

- Character dossiers checked / 已检查单字档案: `10,996`
- Images found through ordinary Windows paths / 普通路径识别: `1,578`
- Images requiring the Windows long-path prefix / 长路径识别: `9,418`
- Verified local image files / 复核后本地图像总数: `10,996`
- Verified missing image files / 复核后缺失数: `0`

The first audit pass incorrectly classified `9,418` long paths as missing.
An independent Agent reproduced the paths with the Windows `\\?\` prefix and
found every file. The repository now has a validator that distinguishes a
real local image, a missing local route, and a path outside the repository.

首轮审计把 `9,418` 条 Windows 长路径误判为缺失。独立 Agent 使用
Windows `\\?\` 前缀复核后确认全部文件存在。仓库现已增加真值门禁，
分别识别真实本地图像、缺失的本地路线和仓库外路径。

This correction is itself part of the audit evidence: a single path API or
single Agent count is not enough for candidate adjudication.

这一纠错也是审计证据的一部分：单一文件 API 或单个 Agent 的统计，不能
作为候选裁决的充分依据。

### Character research depth / 单字研究深度

All `10,996` character dossiers have object-local human and machine entrances.
However, the inspected core fields for inscription occurrence, full text or
OCR, plate and catalog, Heji number, findspot, collection, period, group,
variant, near form, component, bibliography, reading history, and dispute are
still generic pending questions across the collection.

全部 `10,996` 份单字档案已共置人类入口和机器辅助入口。但本次检查的
卜辞出现、全文或 OCR、图版著录、合集号、出土地、馆藏、时期组类、
异体、近形、构件、书目、释读史和争议等核心字段，仍普遍只是同类待查
问题，尚未成为对象特异的已打开证据。

### Inscription and plate evidence / 卜辞与图版证据

- Inscription crosswalk dossiers / 卜辞交叉候选档案: `612`
- Confirmed catalog identities / 已确认著录身份: `0`
- Dossiers with opened plate, OCR, or full text / 已打开图版或全文: `0`
- Independent plate object directories / 独立图版对象目录: `0`

These folders are useful crosswalk routes, but they are not yet inscription
and plate archives of the depth required for direct philological research.

这些目录是有用的交叉检索路线，但尚未达到可直接进行文字学研究的卜辞与
图版档案深度。

### Literature evidence / 文献证据

The source-object area records twenty-one databases, repositories, museums,
and collection routes. The formal `research/` area still contains guides and
indexes rather than item-level paper, monograph, catalog, reading-history, and
dispute dossiers. Source engineering does not substitute for literature work.

来源对象区已经记录二十一个数据库、仓库、博物馆和馆藏路线。正式
`research/` 区仍以指南和索引为主，尚未形成逐篇论文、专著、著录、
释读史和争议档案。来源工程不能替代文献整理。

### Source processing / 来源处理

- Registered source objects / 已登记来源对象: `21`
- Final source review status / 最终来源复核状态:
  `pending_human_review` for `21/21`
- Sources with evidence and derivatives pending review / 已有证据与派生物:
  `4/21`
- Sources with material evidence gaps / 仍有实质证据缺口: `17/21`

The four comparatively strong routes are HUST-OBC, OBIMD, EvoBC, and the
Cambridge-Hopkins crosswalk. Several Sinica, Xiaoxuetang, and museum routes
remain access pages, restricted snapshots, or failed downloads rather than
opened source packages.

相对较强的四条路线是 HUST-OBC、OBIMD、EvoBC 和 Cambridge-Hopkins
交叉表。若干史语所、小学堂和博物馆路线仍只是入口页、受限页面快照或
下载失败记录，不是已经打开的来源资料包。

### Graph and AI laboratory / 图谱与 AI 实验室

The relationship graph contains `141,589` routing edges. It still has no
reviewed formal `character-component` or `character-inscription` relation.
EvoBC evolution edges remain dataset routes, not verified evolution claims.

关系图已有 `141,589` 条路线边，但仍没有经复核的正式
`character-component` 或 `character-inscription` 关系。EvoBC 演化边仍
是数据集路线，不是已验证的字形演化结论。

The v2 benchmark schema and validator exist, but the repository has no real v2
experiment record, frozen pilot case, sealed diagnostic gold, Agent court run,
model-independent rerun, or isolated scorer receipt. The only live candidate
decision is a justified `abstain_withhold_candidate` record.

v2 基准 schema 和校验器已经存在，但仓库中没有真实 v2 实验记录、冻结
试点案、密封诊断 gold、Agent 法庭运行、模型独立复跑或隔离评分 receipt。
目前唯一真实候选裁决是有依据的 `abstain_withhold_candidate`。

## Nineteen-Requirement Verdict / 十九项要求判定

1. Human-first positioning: `established`, but material depth is incomplete.
2. Evidence-first workflow: `established`, but many routes are unopened.
3. Structured-data subordination: `established in policy`; continue auditing.
4. Research boundary: `established`; no new decipherment claim was made.
5. Required reading and live-disk authority: `established`.
6. Object-local co-location: `established for audited object families`.
7. Research-ready character folders: `partial`.
8. Required character evidence: `not complete`.
9. Required inscription and plate evidence: `not complete`.
10. Item-level literature and dispute evidence: `not complete`.
11. Breadth of source types: `partial`; several named classes remain routes.
12. Priority sources: `partial`; access and rights blockers remain.
13. Parsing, cleaning, linking, and human extraction: `partial`.
14. Source provenance fields: `broadly present`, final review incomplete.
15. Required graph relations and statistics: `partial`.
16. Large-file handling: `established for audited HUST and OBIMD packages`.
17. Chinese, line width, and concrete missing questions: `partial`.
18. Validation, commit, and push process: `established as a workflow`.
19. Human-readable, traceable research infrastructure: `partial`, not closed.

1. 人类优先定位：`已建立`，但资料深度尚未完成。
2. 证据优先流程：`已建立`，但大量路线尚未打开。
3. 结构化资料从属：`政策已建立`，仍须持续审计实际内容。
4. 研究边界：`已建立`；本审计未提出新释读结论。
5. 必读与磁盘真值：`已建立`。
6. 对象内共置：`已在已审计对象族建立`。
7. 可直接研究的单字档案夹：`部分完成`。
8. 单字所需证据：`未完成`。
9. 卜辞与图版所需证据：`未完成`。
10. 逐项文献、释读史和争议证据：`未完成`。
11. 来源类型广度：`部分完成`；若干类型仍只是路线。
12. 重点来源：`部分完成`；仍有访问和权利阻断。
13. 解析、清洗、关联和人类内容抽取：`部分完成`。
14. 来源追溯字段：`广泛存在`，但最终复核未完成。
15. 所需图关系与统计：`部分完成`。
16. 大文件处理：`已在审计过的 HUST 与 OBIMD 原包建立`。
17. 中文、行宽和具体待查问题：`部分完成`。
18. 校验、提交和推送流程：`已建立工作流`。
19. 人类可读、可追溯研究基础设施：`部分完成，尚未闭合`。

## Next Evidence Gates / 下一证据门槛

1. Keep the new long-path-aware image truth validator in the release gate.
2. Complete a small, rights-safe character batch with opened images,
   object-specific observations, catalog routes, and inscription context.
3. Open at least one real plate and inscription dossier end to end.
4. Create item-level literature dossiers with citation and disagreement trails.
5. Resolve source evidence and rights gaps before source status promotion.
6. Run one diagnostic known-answer case and one negative control through a
   frozen, sealed, independently rerun AI court; withhold probability when
   pretraining exposure is unknown.

1. 把新的长路径感知图像真值门禁保留在发布校验中。
2. 选择一个权利安全的小批单字，打开真实图像，补对象特异观察、著录路线
   和卜辞上下文。
3. 至少把一个真实图版与卜辞档案端到端打开。
4. 建立逐项文献档案，记录引用关系和不同意见。
5. 来源状态提升前，先解决来源证据和权利缺口。
6. 用冻结、密封、独立复跑的 AI 法庭完成一个已知答案诊断案和一个负对照；
   预训练暴露未知时不得显示研究概率。

## Boundary / 边界

This is a completion audit, not a decipherment result, a rights clearance, or
confirmed scholarship. `not_complete` is an instruction to keep collecting
and opening evidence, not permission to invent missing material.

本文件是完成度审计，不是释读结果、权利清理或已确认学术成果。
`not_complete` 表示应继续收集和打开证据，不允许编造缺失资料。
