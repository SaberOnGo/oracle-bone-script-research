# 收缩与迁移计划 / Consolidation And Migration Plan

- 状态 / Status: `proposed_plan_awaiting_user_decision`
- 原则 / Principle: 不丢失任何已核对的内容；Git 历史保留一切；工作树
  只保留有用的东西

本计划分六步。每一步都可独立完成、校验、提交。第 1 到 3 步是收缩，
第 4 到 6 步是补核心。收缩先行，因为 50 万文件会拖慢后面的每一步。

Six steps. Steps 1 to 3 shrink the tree; steps 4 to 6 build the missing
core. Shrinking comes first because half a million files slow every later
step.

## 第 1 步：冻结生成器与队列 / Freeze Generators And Queues

- 停止运行 `tools/002_corpus-import/` 下的 `build_*_materials.py`、
  `build_*_dossiers.py`、`build_*_reviews.py` 等批量模板生成器。脚本
  保留在 `tools/` 并在 README 标注 `frozen_do_not_run`。
- 删除 `corpus/009_statistics-and-derived-features/` 中约 200 个
  AI 队列、scaffold、handoff、route pack、assignment plan 文件
  （编号 003 至 089、098 至 212）。保留可由脚本重建的真实统计
  （图边汇总、来源覆盖率）和审计报告（220 至 235）。
- 删除 `doc/public/user_research/002` 到 `010` 的队列目录。它们是
  Agent 工作残留，内容可从 Git 历史恢复。
- 删除根目录未跟踪空目录 `008_source-record-candidates/`。
- 清理 `tmp/` 内 2026-07 的测试日志。

预期效果：`corpus/009` 从 239 文件降到约 40；`user_research` 只剩
`001`、`011` 和新建的 `cases/`。

执行记录（2026-11-02，第 1 步与第 3 步合并完成）：

- 删除 `corpus/009` 队列类文件 195 个。按编号区间删除时误伤的 7 个真实
  统计（`007` 来源覆盖汇总、`186`--`191` 覆盖与 ID 映射审计）已恢复。
- 删除 `doc/public/user_research/002`--`010` 共 119 个空骨架文件，新建
  `cases/index.md` 登记 3 个活跃案件。
- 删除 `tools/005_ai-context-pack-builder/` 全部队列与上下文包生成器，
  删除 `tools/004` 中只生成队列的 36 个脚本；`tools/002`--`004` 其余脚本
  标注冻结。
- 第 3 步提前执行：37,004 行的结构校验脚本重写为约 1,170 行的政策与
  内容门禁校验（G2、G3、G5、G6、G7、G8、G9、G11），运行约 2 分钟；
  32,086 行的骨架测试改为 23 个门禁单元测试，运行不到 1 秒。原因是
  旧校验把每个队列文件写成"必须存在"，不改校验就无法删除任何队列。
- 其余 128 个测试文件中 7 个各有一个方法依赖已删除的函数或队列文件，
  已移除这些方法；其余方法检查真实内容，全部保留并通过。

Execution record (2026-11-02): steps 1 and 3 were completed together,
because the former validator required every queue file to exist.

## 第 2 步：折叠无内容的生成目录 / Collapse Content-Free Directories

按"按需建目录"规则（`02_target-architecture.md` 第 5 节）处理：

| 语料区 | 现状 | 处理 |
| --- | --- | --- |
| 004 EvoBC 演化候选 13,714 目录 | 无本地图，无对象特有事实 | 全部折叠为 `000_evolution-registers/` 中一张 CSV（候选 ID、EvoBC 类号、分期代码、图片路线数、今字标签、状态） |
| 003 OBIMD 构件候选 2,747 目录 | 权利 `metadata_only`，无本地字形图 | 折叠为登记 CSV；有人工视觉观察句的保留观察句到 CSV 列 |
| 002 卜辞 crosswalk 候选 622 目录 | 只有著录号对照 | 折叠进 `000_inscription-registers/` 已有的 crosswalk CSV；10 个 source-record 候选保留并改写 |
| 001 单字 12,584 目录 | 每目录一张本地图 + 一句观察 | 保留目录，但 16 文件合并为 `README.md` + `record.json` + `images/` |
| 007 研究专题 20 目录 | Cambridge Hopkins 主题 | 合并为一个主题登记 CSV + 一份说明 |

单字目录合并脚本的规则：读取现有 16 个文件，抽出所有非模板行（图片
路径、校验和、来源行、观察句、文件名著录线索），按新标准章节重排，
省略空章节，写出一份 `README.md`；所有 JSON 合并为一个
`record.json`。合并后由脚本比对：旧文件中每条非模板行都能在新文件中
找到，否则报错。

预期效果：跟踪文件从 518k 降到约 45k；`corpus/001` 从 211k 降到约
38k。

Expected result: tracked files drop from 518k to about 45k.

执行记录（2026-11-02，第 2a 步）：

- 折叠 190 个分桶、共 329,575 个文件：EvoBC 13,714 目录、OBIMD 构件
  2,747 目录、Cambridge 对照 612 目录、码位对照 16 个分桶、主题 20 目录。
  各对象 ID 仍可经 `project_registry/002_*` 映射到登记表中的一行。
- 构件目录中唯一的对象特有内容是视觉观察，2,743 条已写入
  `004_obimd-component-visual-observations.csv`（描述性观察与像素画像）。
- OBIMD 10,364 张子字形图片按用户决定移到本地忽略区
  `external_local_archive/obimd-component-images/`，公开仓库不再分发；
  资产索引、技术画像、视觉画像、资产 ID 映射中的路径已同步更新。
- 跟踪文件由 517,880 降到约 187,800。
- 单字合并（第 2b 步）尚未执行：实际单字目录为 10,407 个
  （999 个已释候选、9,408 个未释候选），每个目录一张本地图片；其中
  10 个有额外复核文件的目录留给第 5 步人工整理。

Execution record (step 2a): 329,575 files in 190 buckets were collapsed into
registers; OBIMD images moved to the ignored archive; tracked files dropped
to about 187,800. Character merging (step 2b) has not run yet.

## 第 3 步：重构测试 / Restructure Tests

- 按对象编写的测试（`test_obs_char_000963_*`、`test_ihp_*_1216_1217`
  等约 60 个文件）改写为数据驱动的通用测试：遍历所有对象目录，检查
  档案标准、来源标记、机读与人读互检、禁止模式。
- 保留仓库骨架、提交信息、权利覆盖、大来源登记、schema 校验测试。
- 目标：全量测试一次运行在 5 分钟内结束。

`.git` 931 MiB 的历史体积是否用 `git filter-repo` 重写，由用户单独
决定；本计划不建议现在做，因为会改写全部提交哈希并影响已推送的
远端。

## 第 4 步：建立卜辞释文语料 / Build The Inscription Text Layer

这是最重要的一步。来源按"权利可行性 × 文本质量"排序：

| 优先 | 来源 | 内容 | 权利判断（待核实） | 路线 |
| --- | --- | --- | --- | --- |
| 1 | OBIMD（Scientific Data 2026） | 21,941 句，带字框与阅读顺序 | 用户决定（2026-11-01）：个人非商业研究直接使用，不致信作者；公开仓库不再分发原始数据 | 原始包放本地忽略归档，Agent 本地解析与统计；Git 只提交 OBIMD 条目 ID、统计结果和档案内带出处的少量例句引用 |
| 2 | 小学堂《合集材料来源表》 | 合集号 -> 著录、分期、出土 | 官方学术数据库，metadata | 已有 302 行缩略语 staging；继续抽取 |
| 3 | 殷契文渊 | 著录、拓片、释文检索 | 需注册登录；详情接口 406 | 用户注册账号；Agent 在登录态下按条取回，只存 metadata 与引用 |
| 4 | 早期著录（公有领域候选） | 《铁云藏龟》1903、《殷虚书契》前编 1913 / 后编 1916、《殷虚文字甲编》1948 等 | 罗振玉卒 1940、董作宾卒 1963；按作者卒后 50 年规则原书应已进入公有领域，但扫描件的馆方条款需逐一核实 | 可本地保存拓片图并公开，是字形图与卜辞图版的合法主渠道 |
| 5 | Cambridge Hopkins finding list | 著录 crosswalk | 已登记 | 已有 |
| 6 | 已出版释文（《合集释文》《摹释总集》《花东》Schwartz 译注） | 高质量释文 | 版权保护 | 只记录引用与页码；项目隶定由 Agent 逐条核对后自行写出并标注依据 |

实施顺序：先做《合集》第 1 至 1000 号的释文语料试点（约千条），
形成 `inscriptions.jsonl` 与渲染表，验证字位到字 ID 的链接；再扩展。

The inscription text layer is the most important step. Priority sources are
ranked by rights feasibility and text quality. Start with a thousand-entry
pilot on Heji 1 to 1000.

## 第 5 步：100 字深度试点 / One-Hundred-Character Deep Pilot

从已释字中选 100 个：高频、有多条卜辞例句、有金文对应、释读史清楚。
为每个字按 `03_object-dossier-standard.md` 写出完整档案。目标是：

- 100 份档案全部有第 1 至 4 节和第 10 节；
- 至少 60 份有释读史（提出者、年份、文献、页码）；
- 至少 80 份有 3 条以上带出处的卜辞例句；
- 每份档案的实质内容行占比 ≥ 70%。

试点完成后，用这 100 字做第一次盲测（隐去释读，只给证据包），记录
模型命中率、弃权率、错误类型。盲测结果决定是否扩展到 1,588 字。

试点同时产出：合并后的档案样例（真实内容，不是空模板）、释读史
来源清单、例句抽取工具、字位链接工具。

A hundred-character deep pilot produces real exemplar dossiers, the first
masked-known blind test, and the tooling for scaling.

## 第 6 步：重建图谱与统计 / Rebuild Graph And Statistics

- 从卜辞语料生成 `occurs_in`、`co_occurs`、`same_bone`、`dated_to`。
- 从单字档案生成 `variant_of`、`near_form_of`、`component_of`、
  `corresponds_to`、`reading_proposed`、`reading_disputed`。
- 统计：每字出现次数、分期分布、辞例类型分布、高频共现字、
  同构件字簇。
- 所有边带 `source_ref` 与 `status`；旧路线边移出图谱目录。

此时知识库才第一次能回答"某字出现 N 次、全在某期、常与某字共现"这类
问题，AI 推理层才有可用输入。

## 风险与决定点 / Risks And Decision Points

| 决定 | 影响 | 建议 |
| --- | --- | --- |
| 折叠 004 / 003 / 002 生成目录 | 删除约 30 万文件（历史保留） | 执行 |
| 合并 001 单字目录 16 -> 3 文件 | 删除约 17 万文件；需合并脚本与互检 | 执行 |
| 删除 009 队列与 user_research 队列 | 删除约 250 文件 | 执行 |
| 重写 .git 历史 | 改哈希，影响远端 | 暂不执行 |
| OBIMD 使用方式 | 本地使用，公开仓库不再分发 | 已决定：个人研究直接使用 |
| 注册殷契文渊账号 | 外部账号 | 用户决定 |
| 公有领域著录扫描来源 | 需逐一核实馆方条款 | 先核实再下载 |

Every deletion is reversible from Git history. OBIMD is used locally for
personal non-commercial research without contacting the authors; the public
repository carries only IDs, statistics, and short cited examples.
Registering a Yinqi Wenyuan account remains the user's decision.
