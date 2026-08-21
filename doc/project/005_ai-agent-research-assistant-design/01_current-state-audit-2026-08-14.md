# Current State Audit / 当前状态审计

Status: `current_state_audit`

Audit update date: `2026-08-21`

Audited base commit: `b38d90ec6ed`

Follow-up verification date: `2026-08-21`

Historical baseline commit: `7c8b8a29a35` (2026-08-14)

Last verified skeleton receipt before this follow-up: `b38d90ec6ed`

Last verified human-material gate before this follow-up: `b38d90ec6ed`

## Purpose / 目的

This audit binds the autonomous-candidate strategy to the current disk state.
It is an operational audit, not a paleographic conclusion, a decipherment
result, or published scholarship.

本审计把自主候选战略绑定到当前磁盘状态。它是运行审计，不是文字学结论、破译结果
或已发表学术成果。

The normative rules remain in the [autonomous-candidate strategy][strategy].
This file records what is and is not executable at the audited base commit and
the explicitly listed follow-up checks.

规范规则仍在[自主候选战略][strategy]中。本文件只记录该提交上什么已经可运行、什么
仍不可运行。

## Reproducibility receipts / 可复跑凭据

The historical baseline receipts below were run at commit
`7c8b8a29a35` on 2026-08-14. They are retained for comparison and are not
claims that the current commit was rescanned.

## Historical baseline receipts / 历史基线回执

- `python -m unittest discover -s tests -v`: `981 tests OK` in 564 seconds.
- `python tools/validation/check_repository_skeleton.py`: `PASS` in 196
  seconds.
- `check_human_research_material_gate.py --full --strict --summary`:
  `PASS`, 156838 Markdown files, all four debt counts zero.

## Last verified base and working-tree follow-up /
## 最后核验基线与工作树跟进

The last committed audited base is `main` at `b38d90ec6ed`. The receipts in
this section describe that base. The current follow-up is deliberately
recorded as a working-tree change and does not self-embed its future commit
hash. Older sections retain their original commit labels.

最后一个已审计提交是 `main` 的 `b38d90ec6ed`。本节回执描述该基线；当前
跟进明确记录为工作树变更，不把未来提交哈希写入自身。后文保留原始提交标签。

- Full suite: `1040 tests OK` in `645.768` seconds.
- Repository skeleton: `PASS repository skeleton`.
- Full strict human-material gate: exit `0`, `156842` Markdown files,
  and all four debt counts `0`.
- Commit-message check and push: `PASS`; `origin/main` matches HEAD.
- No public v2 experiment record exists; no candidate-delivery channel is
  open. The user-owned `doc/public/user_prompt/1.txt` is untracked,
  unread, and unmodified.
- The working tree adds a ninth Met source-record candidate for object
  `42022` / accession `18.56.71`. It has two checked image bytes and a
  human-first dossier, but no OCR, plate identity, or character linkage.

- 全量测试：`1040 tests OK`，耗时 `645.768` 秒。
- 仓库骨架：`PASS repository skeleton`。
- 严格人类资料门：退出码 `0`，扫描 `156842` 篇 Markdown，四项债务均为 `0`。
- 提交信息检查和推送：`PASS`；`origin/main` 与 HEAD 一致。
- 当前没有公开 v2 实验记录，也没有开启候选交付通道。用户拥有的
  `doc/public/user_prompt/1.txt` 仍未跟踪、未读取、未修改。
- 工作树新增大都会 42022 号、馆藏号 `18.56.71` 的第九个来源记录候选。
  两张图像字节已核验并有优先人类档案，但仍无 OCR、图版身份或单字关联。

Working-tree verification after the claim matrix was added:

- The Met 42022 object suite: `5 tests OK`; both image files match their
  recorded sizes, SHA-256 values, and 4000 x 2667 dimensions. Its claim-gate
  page marks C2 direct observation and C1/C3--C8 blocked or withheld.
- IHP item 503 now has an object-local claim-gate page. It keeps the museum
  phrase `帝令雨` source-reported, marks the private visual route as direct
  observation only, and withholds C4--C8 pending plate, text, and rights work.
  Its focused suite is `8 tests OK`.
- HUST character `obs-char-000963` now has an object-local claim-gate page.
  It binds one checked derivative and five private archive members to C2,
  keeps the near-form comparison as a candidate route, and withholds C1 and
  C4--C8. Its focused suite is `6 tests OK`.
- A live catalog-route review for `obs-char-000963` now records CUHK
  Humanum, a published PDF, and a lexicographic route. Their shared
  `合30173` locator appears with other headwords or contexts, so the HUST
  filename remains route-only; no external snapshot was added.
- HUST `obs-unk-000001` now has an object-local source-member audit and claim
  gate. Its one ZIP member and committed derivative share a checked checksum;
  C2 is direct observation, while identity, context, reading, and delivery
  remain blocked or withheld.
- Met object `42045` now has an object-local crosswalk to its same-object
  source-record candidate. The collection folder keeps one compact image while
  the source record binds both API image bytes; no recto-verso, plate, or text
  claim is added. Its focused Met suite is `14 tests OK`.
- Met object `42022` now has the same object-local handoff pattern. Its source
  record binds both API image bytes, while the collection dossier keeps its
  compact asset and preserves the missing plate, text, and identity checks.
  Its focused Met suite is `11 tests OK`.
- HUST `obs-unk-000002` now has a byte-bound source-member audit and claim
  gate. Its focused source-member suite is `3 tests OK`; its visual note
  remains a direct, neutral observation with no reading or identity claim.
- IHP item `1213` now has an object-local claim gate linked to its official
  page, two private JPEG checks, and source-reported front/reverse text. The
  partial transcription, plate locator, rights, and character linkage remain
  explicitly withheld.
- IHP item `1214` now has an object-local claim gate for six source-reported
  short entries with image placeholders. Its two private JPEGs support direct
  surface observation, while plate mapping, text alignment, rights, and glyph
  linkage remain withheld.
- The claim evidence gate suite: `4 tests OK`; the matrix is linked from the
  strategy, methods, and AI evidence-pack review skill.
- The full suite: `1069 tests OK` in `686.249` seconds. The triage command
  returned `PASS triage-only case selection (9 rows)`.
- Repository skeleton: `PASS repository skeleton`.
- Full strict human-material gate: exit `0`, `156852` Markdown files, and all
  four debt counts `0`.
- No v2 experiment record or candidate-delivery channel was opened. This
  object remains a source-record candidate with text and catalog blockers.

新增命题矩阵后的工作树验证：

- Met 42022 对象套件：`5 tests OK`；两张图像的大小、SHA-256 和
  `4000 x 2667` 尺寸均与记录一致；命题页把 C2 标为直接观察，C1、
  C3--C8 标为阻断或扣留。
- 史语所 503 号对象现有对象内命题门槛页。它把 `帝令雨` 保持为来源说明，
  把私有图像路线限制为直接观察，并在图版、文字和权利完成前扣留 C4--C8。
  其专项套件为 `8 tests OK`。
- HUST 单字 `obs-char-000963` 现有对象内命题门槛页。它把一张已核验派生图和
  五个私有原包成员绑定到 C2，将近形比较保留为候选路线，并扣留 C1、C4--C8。
  其专项套件为 `6 tests OK`。
- `obs-char-000963` 现有实时著录路线复核，记录香港中文大学 Humanum、已发表
  PDF 和字源字形路线。同一 `合30173` 定位号与其他字头或语境一起出现，故 HUST
  文件名仍是路线候选；没有加入外部快照。
- HUST `obs-unk-000001` 现有对象内来源成员审计和命题门槛页。其唯一 ZIP
  成员与已提交派生图共享已核验 checksum；C2 为直接观察，身份、上下文、
  释读和交付仍被阻断或扣留。
- Met 对象 `42045` 现有对象内交接页，连接同一对象的来源记录候选。
  馆藏目录保留一张紧凑图，来源记录绑定两张 API 图像字节；不新增正反面、
  图版或文字主张。Met 专项套件为 `14 tests OK`。
- Met 对象 `42022` 现有同样的对象内交接页。来源记录绑定两张 API 图像字节，
  馆藏档案保留紧凑资产，并继续明确图版、文字和身份缺口。Met 专项套件为
  `11 tests OK`。
- HUST `obs-unk-000002` 现有字节绑定的来源成员审计和命题门槛页。其专项
  来源成员套件为 `3 tests OK`；图像页仍是直接、中性的观察，不作释读或身份
  主张。
- 史语所 1213 号对象现有对象内命题门槛页，连接官方对象页、两条私有 JPEG
  校验和及正反面来源文字。部分释文、图版定位、权利和单字关联仍明确扣留。
- 史语所 1214 号对象现有对象内命题门槛页，记录六条带图像占位的来源短条目。
  两条私有 JPEG 支持直接表面观察，但图版对应、文字对齐、权利和单字关联仍扣留。
- 命题证据门槛套件：`4 tests OK`；矩阵已由战略、研究方法和 AI
  evidence-pack skill 共同链接。
- 全量测试：`1069 tests OK`，耗时 `686.249` 秒。选案命令返回
  `PASS triage-only case selection (9 rows)`。
- 仓库骨架：`PASS repository skeleton`。
- 严格人类资料门：退出码 `0`，扫描 `156852` 篇 Markdown，四项债务均为 `0`。
- 没有开启 v2 实验记录或候选交付通道。本对象仍是来源记录候选，文字和著录
  缺口仍然阻断正式提升。

## Earlier targeted receipts / 较早定向回执

The following targeted receipts were recorded before the current snapshot.
They remain useful provenance, but are not a replacement for current scans.
- Post-change object-level checks: BL Or. 7694/1595 `7 tests OK`; the related
  source-text reconciliation suite is `5 tests OK`; effective
  BL Or. 7694/1535 `7 tests OK`; effective OBIMD rights `5 tests OK`.
- OBIMD effective-rights propagation: `1 targeted test OK`; every human page
  retaining the legacy value now exposes the effective status and override.
- BL Or. 7694/1595 visual-region review: `3 tests OK`; ten boxes match the
  committed image dimensions and SHA-256 values without text mapping.
- BL Or. 7694/1535v visual-region review: `3 tests OK`; eight boxes match
  the committed CC0 image dimensions and SHA-256 without text mapping.
- Ningxia HYZ 421 source-record regression: `5 tests OK`; the committed
  JPEG matches its recorded size, SHA-256, format, and pixel dimensions.
- Ningxia HYZ 421 visual-region review: `3 tests OK`; eight boxes are bound
  to the committed JPEG and remain unmapped to the displayed source string.
- HUST character visual-comparison follow-up: `15 tests OK` across
  `obs-char-000209`, `obs-char-000412`, and `obs-char-000791`. Fifteen raw
  members are bound to exact ZIP paths, sizes, compressed sizes, SHA-256
  values, and pixel dimensions; no restricted image was newly committed.
- Schwartz Huayuanzhuang East literature dossier: `4 tests OK`; publisher
  metadata, DOI, chapter map, license signal, and HYZ 421 page citation are
  recorded without claiming that the cited pages were opened.
- Liu 2014 *Early China* literature dossier: `4 tests OK`; the abstract's
  Yingcang 885/886 dating argument, citation relationship, copyright status,
  and unresolved BL object crosswalk are recorded.
- Committed British Library image-asset regression: `3 tests OK`; all three
  source bytes match their recorded size, SHA-256, and pixel dimensions.
- AI case-selection triage regression: `4 tests OK`; the report now covers
  seven opened candidates and remains a work-order signal only, not a v2
  record or probability.
- AI diagnostic pilot targeted regression: `48 tests OK`, including corpus
  object scope, leakage, lock, falsification, HMAC, and one-shot scoring gates.
- After the object-scope hardening, the full pilot regression is `49 tests OK`;
  the new case rejects a non-object directory nested under `corpus/`.
- `validate_ai_agent_evidence_packs.py`: `PASS 1 file`.
- `validate_ai_agent_benchmark_experiments.py`: `FAIL no v2 records`.
- Human-material gate regression tests: `7 tests OK`; they cover summary
  failure propagation, the full-scan coverage floor, and debt ceilings.

以上三项全仓库回执属于 2026-08-14 历史基线，不能替代当前主分支的
重新扫描。它们保留了 981 项测试、骨架校验、human-research gate
以及四项债务计数的当时证据。

## Earlier follow-up receipts / 前期跟进回执

The current 2026-08-21 follow-up ran targeted suites after the object and
rights updates. A full skeleton run at commit `4130c2c034f` returned
`PASS repository skeleton`.

The full strict human-material gate at commit `4130c2c034f` returned exit 0
with 156839 scanned Markdown files and all four debt counts at zero.

The full test suite at commit `4130c2c034f` ran 1005 tests in 639.681
seconds and returned `OK`. Its final triage-only case-selection line was
`PASS` for eight rows; it did not open a candidate-delivery channel.

After the human candidate-guide update, the current commit `ea94c2e904c`
ran 1009 tests in 629.329 seconds and returned `OK`. The triage-only check
again returned `PASS` for eight rows.

After these receipts, an eighth inscription source-record candidate was added
for The Met object 42045 / accession 67.43.14. Its two committed image files,
API snapshot, sizes, and SHA-256 values are bound in the object-local dossier.
The candidate still lacks OCR, a plate or Heji identity, and character links;
it is not included in the earlier seven-row triage output.

An earlier full attempt was interrupted after about eight minutes while
reading `check_oracle_character_human_markdown_wrapping`; it produced no PASS
result. The later successful run supersedes that incomplete attempt. The
audit-note edit after the receipt is documentation-only.

2026-08-21 的跟进在对象、权利和自主试点更新后运行了定向测试。完成扫描剪枝后，
`4130c2c034f` 上的全量骨架校验返回 `PASS repository skeleton`。

`4130c2c034f` 上的 full/strict 人类资料门返回退出码 0，扫描 156839 个
Markdown 文件，四项债务计数均为 0。

`4130c2c034f` 上的全量测试运行 1005 项，耗时 639.681 秒，最终为 `OK`。
最后的选案分诊只输出八行 `PASS`，没有开启候选交付通道。

补充人类候选导览后，当前提交 `ea94c2e904c` 上的全量测试运行 1009 项，
耗时 629.329 秒，最终为 `OK`。选案分诊复核再次对八行返回 `PASS`。

更早的一次全量尝试约八分钟后停在读取
`check_oracle_character_human_markdown_wrapping` 的阶段，没有产生 PASS；
后一次成功回执已取代这次未完成尝试。本审计说明的后续修改仅是文档修改。

这些回执之后又加入大都会艺术博物馆 42045 号、馆藏号 67.43.14 的第八个
卜辞来源记录候选。对象目录绑定两张已提交图像、API 快照、大小和 SHA-256；
OCR、图版或合集身份以及单字关联仍缺失。它不在此前七行的选案分诊输出中。

Current targeted receipts include the following:

- AI pilot: `49 tests OK`; case triage: `4 tests OK`; pilot summary:
  `4 tests OK`.
- Fresh AI pilot rerun at commit `faf3ab9cf03`: `49 tests OK` in 88.484
  seconds. This remains a diagnostic pipeline receipt, not a calibration or
  candidate-delivery result.
- Full skeleton at `4130c2c034f`: `PASS repository skeleton`.
- Full strict human-material gate at `4130c2c034f`: `156839` Markdown files;
  all four debt counts were `0`.
- v2 benchmark contract: `68 tests OK`; no real v2 record was found.
- British Library 1595: `7 tests OK`, including the two ignored Wikimedia API
  snapshots bound to the human evidence page; 1535: `7 + 3 tests OK`.
- IHP item 771 source-record candidate: `7 tests OK`, including a new
  image-bound visual observation page.
- IHP item 503 and 1215 source-record candidates now each have a new
  image-bound visual observation page; focused suites have `12` and `13 tests
  OK`, respectively.
- IHP item 1215 also records a dated external-catalog search boundary; no
  independent plate or edition was obtained.
- Ningxia HYZ 421: `5 tests OK`; effective OBIMD rights: `5 + 3 tests OK`.

当前定向回执包括：AI 试点 `49 tests OK`、选案分诊 `4 tests OK`、试点摘要
`4 tests OK`；v2 合同 `68 tests OK`，但没有真实 v2 记录；英国图书馆 1595
为 `6 tests OK`、1535 为 `7 + 3 tests OK`；宁夏 HYZ 421 为 `5 tests OK`；
史语所 771 号来源记录候选为 `7 tests OK`，新增了绑定图像的视觉观察页；
503 和 1215 号来源记录候选分别为 `12` 和 `13 tests OK`，均新增绑定图像的
视觉观察页；
full/strict 人类资料门在 `4130c2c034f` 上扫描 156839 个 Markdown 文件，四项
债务计数均为 0；
OBIMD 有效权利为 `5 + 3 tests OK`。1595 的 OBID 入口、释文检索页和原文
检索页仍只是检索线索；公开页返回需登录的访问边界，没有取得
`Heji 40610` 或 `Yingcang 886` 的精确结果。

`faf3ab9cf03` 上重新运行 AI 试点 `49 tests OK`，用时 88.484 秒。这仍是
诊断流程回执，不是校准结果或候选交付结果。

The v1 pass covers one draft scaffold whose evidence sections remain empty.
It does not show research evidence or autonomous adjudication capability.

v1 通过只覆盖一个仍为空的草稿脚手架，不表示已有研究证据或自主裁决能力。

The v2 failure is intentional evidence of an unopened numerical channel. No
public v2 experiment record currently exists under
`doc/public/user_research/generated/ai-agent-benchmark-experiments/`.

v2 失败说明数值通道尚未打开。当前没有公开的 v2 实验记录，不能把测试 fixture 或
本地 pilot 记录当作真实基准实验。

## Latest Xiaoxuetang dossier receipt / 最新小學堂档案回执

Commit `96e1e24d746` adds a human-first Xiaoxuetang database dossier. It
records official portal, oracle-bone, guide, statistics, license, and
technical-report routes; eight ignored snapshot checksums; current count
observations; citation relations; rights wording; and concrete transfer
blockers. It keeps row identity, complete export, proposer, dispute, and
reading history unresolved.

The dossier's focused suite passed `7 tests`. The full skeleton returned
`PASS repository skeleton`. The full strict human-material gate returned exit
0 with `156839` scanned Markdown files and all four debt counts at zero. The
full suite returned `1016 tests in 640.043 seconds, OK`, followed by the
eight-row triage `PASS` line.

The research-note coverage counter was updated from 56 to 65 because the new
dossier adds eight human Markdown files and one subordinate JSON record. This
is a coverage count change, not a claim that the literature corpus is complete.

提交 `96e1e24d746` 新增小學堂数据库人类优先档案，记录官方门户、甲骨文、
入门、统计、版权和技术报告路线、八个已忽略快照的 checksum、当前数量观察、
引用关系、权利文字和具体转移阻断项。行身份、完整导出、提出者、争议和释读史
仍保持待查。

该档案的定向测试为 `7 tests`。全量骨架校验返回 `PASS repository skeleton`。
full/strict 人类资料门退出码为 0，扫描 `156839` 个 Markdown 文件，四项债务
均为 0。全量测试为 `1016 tests in 640.043 seconds, OK`，最后八行选案分诊
仍返回 `PASS`。

由于新增八个 Markdown 和一个辅助 JSON，研究资料计数从 56 更新为 65。这是
覆盖数变化，不是文献资料库已经完整的结论。

## Effective-rights routing receipt / 生效权利路由回执

The current working-tree follow-up propagates the active rights override
into both source-coverage outputs used for AI routing. The historical
`rights_status` value remains visible for provenance, but every affected row
now also carries `effective_rights_status`, the public decision, the override
path, and effective asset counts.

当前工作树跟进已把生效权利覆盖传播到 AI 路由使用的两份来源覆盖输出。历史
`rights_status` 仍保留用于追溯，但受影响的每一行现在同时记录
`effective_rights_status`、公开决定、覆盖表路径和生效资产计数。

For `src-obimd`, the legacy value is still
`licensed_for_repository`, while the effective status is
`metadata_only_until_verified`. The effective public decision is
`metadata_only_no_public_redistribution_until_reconciled`, and the effective
asset count is `metadata_only_until_verified:10364`. The AI context pack
contains the same source-level fields and an effective status summary of
12 metadata-only, 2 public-domain-verified, and 7 source-risk-noted sources.

对 `src-obimd`，历史值仍是 `licensed_for_repository`，但生效状态是
`metadata_only_until_verified`。生效公开决定是
`metadata_only_no_public_redistribution_until_reconciled`，生效资产计数是
`metadata_only_until_verified:10364`。AI 上下文包含有相同的来源级字段，生效
状态汇总为 12 个 metadata-only、2 个 public-domain-verified、7 个
source-risk-noted 来源。

The focused rights-routing suite passed `2 tests`; existing source-coverage
checks passed `5 tests`, and the OBIMD rights check passed `1 test`. The full
skeleton returned `PASS repository skeleton`. The full test suite returned
`1018 tests in 724.594 seconds, OK`. The strict human-material gate returned
exit 0 with `156839` scanned Markdown files and all four debt counts at zero.
Python compilation and `git diff --check` also passed.

生效权利路由定向套件通过 `2 tests`；既有来源覆盖检查通过 `5 tests`，
OBIMD 权利检查通过 `1 test`。全量骨架返回 `PASS repository skeleton`。全量
测试为 `1018 tests in 724.594 seconds, OK`。严格人类资料门退出码为 0，
扫描 `156839` 个 Markdown 文件，四项债务均为 0。Python 编译和
`git diff --check` 也通过。

This receipt does not clear any rights conflict, authorize redistribution, or
promote an asset, graph edge, character, inscription, or reading. Historical
values remain only as traceable source records; agents must use the effective
fields for routing and publication decisions.

本回执不清除任何权利冲突，不授权再分发，也不提升资产、图边、单字、卜辞或
释读状态。历史值只作为可追溯来源记录保留；Agent 必须使用生效字段决定路由和
公开范围。

## Central provenance join receipt / 中央出处闭合回执

The current follow-up found that the two previously reported package-route
errors are already corrected on disk: HUST raw package file
`pkg-file-000001` uses `dl-hust-obc-figshare-raw` and
`large-src-000001`; OBIMD sub-character file `pkg-file-000008` uses
`dl-obimd-subcharacter-images` and `large-src-000004`.

当前跟进确认，先前报告的两处来源包路线错误在磁盘上已经修正：HUST 原始包
`pkg-file-000001` 使用 `dl-hust-obc-figshare-raw` 和
`large-src-000001`；OBIMD 子字符文件 `pkg-file-000008` 使用
`dl-obimd-subcharacter-images` 和 `large-src-000004`。

The existing object-level join only compared object routes with central
tables. A new central gate now checks every package-manifest `download_id`,
source ID, URL, and file size against the download log. If a populated
large-source row has the same URL, the gate also checks its package size and
download checksum. Light-source rows and explicitly unacquired aggregate
scopes remain allowed without inventing a large-source checksum.

原有对象级闭合门只比较对象路线与中央表。新增中央门现在检查每一个来源包清单
行的 `download_id`、来源 ID、URL 和文件大小是否与下载日志一致。若已填充的
大型来源行具有相同 URL，还会检查来源包大小和下载 checksum。light-source 行
以及明确尚未取得的聚合范围仍可不填写大型来源 checksum，不会被误造为已下载。

The real-register join test and a synthetic mismatch regression both pass.
The object-route join test passes as well. This is provenance validation only;
it does not establish object identity, rights clearance, or any decipherment.

真实登记表闭合测试和合成错误回归测试均通过，对象路线闭合测试也通过。这只是
来源追溯校验，不建立对象身份、权利清理或任何释读结论。

After this gate was added, the full skeleton returned `PASS repository
skeleton`, the full test suite returned `1020 tests in 609.027 seconds, OK`,
and the strict human-material gate returned `156839` scanned Markdown files
with all four debt counts at zero. These receipts cover the current working
tree before the next commit.

加入此门禁后，全量骨架返回 `PASS repository skeleton`，全量测试返回
`1020 tests in 609.027 seconds, OK`，严格人类资料门扫描 `156839` 个
Markdown 文件，四项债务均为 0。这些回执对应下一次提交前的当前工作树。

## Human archive progress / 人类档案进展

- Thirty IHP collection-object directories contain live-source evidence
  dossiers with page routes, catalog facts, image checksums, and concrete gaps.
- The current wave includes items 770, 771, and 772. Their source-reported
  descriptions remain explicitly separate from independent readings.
- Item 508 now has the same source-only treatment, with private image hashes
  and no committed image derivative.
- Item 503 now has the same source-only treatment, with private image hashes
  and no committed image derivative.
- An IHP item 503 inscription source-record candidate now separates museum
  prose from transcription, records explicit OCR and plate gaps, and links a
  bounded visual observation page to the parent evidence.
- An IHP item 1215 inscription source-record candidate now records the museum
  short display, three private image checksums, independent plate/OCR gaps,
  and a bounded visual observation page linked to the parent evidence.
- An IHP item 771 inscription source-record candidate now records the
  source-reported proposed divination, two private HTML hashes, three private
  image hashes, independent plate/text/OCR gaps, and a bounded visual
  observation page linked to the parent collection-object evidence.
- A British Library Or. 7694/1595 recto-verso source-record candidate now
  records the two CC0 image routes, local checksums, page-displayed eclipse
  strings, and independent catalog, text, and character-link gaps.
- The Or. 7694/1595 and Or. 7694/1535v objects now also contain three
  unchanged CC0 source images, linked from their human dossiers and bound to
  the recorded checksums.
- The same candidate now has a British Library catalogue page recording
  source-reported shelfmark, title, collection, date range, extent, and the
  catalogue's `Images currently unavailable` notice. Item-level JSON, IIIF,
  and catalogue-image retrieval remain unresolved.
- A related-route review now records Google Arts & Culture as a same-family
  aggregation and Sketchfab as a CC Attribution route with an explicit NoAI
  restriction. Neither route adds image bytes or independent text evidence.
- The Or. 7694/1535v candidate now records a targeted negative search: the
  generic Google Arts page lists other BL source IDs but not 1535. It remains
  a route note, not evidence that no image exists.
- The Or. 7694/1535v candidate now has the same bounded catalogue treatment;
  its Heji 39498v, Yingcang 1117v, item-level JSON, IIIF, and image links
  remain separate checks.
- A Ningxia Museum HYZ 421 source-record candidate now preserves one
  CC BY-SA 3.0 photograph, its local checksum and dimensions, the source
  inscription string, the Huayuanzhuang East route, and the Schwartz 2019
  citation. Museum rights, plate identity, and OCR remain unresolved.
- The HYZ 421 candidate now has an eight-region visual review page and CSV.
  The boxes are checksum-bound to the committed JPEG, but none is mapped to
  a character, line, reading order, or displayed source string.
- A British Library Or. 7694/1535v source-record candidate now records one
  CC0 image route, local checksums, direct visual observations, and concrete
  catalog, text, and character-link gaps.
- The central inscription source-record map now routes all eight opened
  candidates to their object-local human dossiers.
- A later follow-up adds a Met 42045 source-record candidate with two
  public-domain image files and a bounded human dossier; it remains outside
  the seven-row triage snapshot and has no OCR or character assignment.
- Item 506 now has a source-only treatment with English/Chinese catalog
  differences, private image hashes, and no committed image derivative.
- Six item-level literature dossiers cover HUST-OBC, OBIMD, EvoBC, the
  Cambridge-Hopkins finding list, the Schwartz Huayuanzhuang East book, and
  Liu's Yingcang eclipse article.
- Candidate graph edges now include character-to-component candidates,
  character-to-inscription source-record candidates, variants, local assets,
  and EvoBC correspondence candidates.
- The graph schema now separates route-integrity confidence from any future
  calibrated hypothesis probability; existing `confidence_level` remains
  route metadata only.
- Six HUST character dossiers now include object-specific opened-evidence
  synthesis with direct observation, filename candidates, counterevidence,
  rights boundaries, and concrete next checks.
- The six-object HUST visual batch now has human-readable multi-instance
  comparisons for `000209`, `000412`, `000621`, `000791`, `000852`, and
  `000963`. These are bounded visual records, not accepted glyph identities.
- The British Library Or. 7694/1595 candidate now has a human-readable
  source-text and image-side reconciliation page preserving both displayed
  strings without creating OCR or a project transcription.
- The same candidate now has a ten-region visual review page and CSV. The
  boxes are checksum-bound to the two CC0 images, but no region is mapped to
  a character, line, reading order, or source string.
- Its human evidence page now records the ignored recto and verso Wikimedia
  API snapshots, their byte sizes, SHA-256 values, and local-only status.
- The related Or. 7694/1535v candidate now has an eight-region visual review
  page and CSV bound to its CC0 image, without mapping any region to text.
- Its literature page now records a named astronomical-date dispute: the
  British Library/Scroll route reports 1192 BC, while Liu's *Early China*
  abstract records a 1166 BCE argument for Yingcang 885/886. Both remain
  source routes; neither date is adopted by this project.
- The OBIMD object package-route index now displays the active
  `metadata_only_until_verified` status; the central historical manifest value
  remains traceable under the active rights override.
- Rights remain source-specific. `metadata_only_until_verified` still blocks
  public image reuse where permission is unresolved.

- 三十个史语所馆藏对象目录已有现场来源证据档案，记录页面路线、著录事实、图像校验
  和具体缺口。
- 当前批次新增 770、771、772 号对象；其来源描述与独立释读明确分开。
- 508 号对象也采用同一来源限定，仅保留私有图像校验，不提交图像派生件。
- 503 号对象也采用同一来源限定，仅保留私有图像校验，不提交图像派生件。
- 503 号对象另有卜辞来源记录候选，明确区分馆方说明与摹写，并记录 OCR 和
  图版缺口；新增绑定高清图像的视觉观察页，但不建立拼合、字形或释读结论。
- 1215 号对象另有卜辞来源记录候选，记录馆方短文字、三条私有图像校验和，
  并明确独立图版与 OCR 缺口；新增绑定三张图像的视觉观察页，但不建立拼合、
  字形或释读结论。
- 1215 号对象另记录 2026-08-21 的外部著录检索边界；没有取得独立图版或版本，
  也不把无关的 `R044587` 检索结果加入来源图谱。
- 771 号对象另有卜辞来源记录候选，记录馆方拟译、两份私有 HTML 校验和、三条
  私有图像校验和，并明确独立图版、原文和 OCR 缺口；新增绑定高清图像的
  视觉观察页，但不建立拼合、字形或释读结论。
- 2026-08-21 重新打开 503、771 和 1215 的史语所官方页面。503 页面仍显示
  `帝令雨`；771 的官方展览页仍显示 `I 5867+8202` 的先写后刻说明；1215
  页面仍显示 `帚（婦）井示。韋。`。三者都只是来源页面复核，没有新字节快照、
  可逐行版本或项目释读。
- The 2026-08-21 recheck reopened the official IHP pages for items 503, 771,
  and 1215. Item 503 still displays `帝令雨`; the item 771 exhibition page
  still reports the pre-writing and engraving description for `I 5867+8202`;
  item 1215 still displays `帚（婦）井示。韋。`. These are source-page
  checks only: no new byte snapshot, line-addressable edition, or project
  reading was created.
- 大英图书馆 Or. 7694/1595 正反面来源记录候选保存两条 CC0 图像路线、
  本地校验和、页面月食文字，以及独立著录、文字和单字关联缺口。
- 同一候选现增加大英图书馆馆藏页，记录来源报告的馆藏号、题名、馆藏区域、
  年代范围、范围字段和 `Images currently unavailable` 提示。逐项 JSON、
  IIIF 和馆藏图像仍未取得。
- 2026-08-21 的官方检索结果另报告：该对象的全部或部分刻辞可能在二十世纪
  添加。该句保留为馆藏来源警示，不是本项目真伪判断；后续释读、年代和图版
  使用均被此警示阻断，直到对象历史和实物路线完成对照。
- The 2026-08-21 live catalogue result also reports a possible twentieth-century
  addition to all or part of the inscription. It remains a source warning,
  not a project authenticity judgment, and blocks later reading, dating, or
  plate use until the object history and physical routes are reconciled.
- Or. 7694/1535v 候选现采用同样的限定馆藏处理；其 Heji 39498v、
  Yingcang 1117v、逐项 JSON、IIIF 和图像路线仍需分别核验。
- 2026-08-21 再次核对 Or. 7694/1535v 官方检索结果；仍为
  `Images currently unavailable`，不能把该负面访问结果写成“没有图像”。
- The 2026-08-21 recheck of the Or. 7694/1535v catalogue still reports
  `Images currently unavailable`; this access result is not evidence that no
  image exists.
- The same recheck records a visible hierarchy gap: `Or 7694/1534` is
  followed by `Or 7694/1537`, while `1535` and `1536` are not shown in that
  rendering. This is a route discrepancy only; item identity remains open.
- 同次复核还记录可见层级间隔：`Or 7694/1534` 后接 `Or 7694/1537`，
  页面呈现中未见 `1535` 与 `1536`。这只是路线差异，逐项身份仍待查。
- 宁夏博物馆 HYZ 421 来源记录候选现保存一张 CC BY-SA 3.0 照片、本地校验和与
  尺寸、来源释文、花园庄东路线及 Schwartz 2019 引用。博物馆权利、图版身份和
  OCR 仍未解决。
- 2026-08-21 重新核对 HYZ 421 的 Commons 结构化字段；对象号、出土地和页面
  显示释文仍是来源报告，未替代博物馆目录或发掘登记。
- The 2026-08-21 HYZ 421 Commons recheck preserves the object, findspot,
  and displayed text as page-level source reports, not museum evidence.
- HYZ 421 候选现有八个区域的视觉复核页和 CSV。区域框与已提交 JPEG 的校验和
  绑定，但没有把区域对应到单字、行序、阅读顺序或页面字符串。
- 中央卜辞来源记录映射表现已把八个已打开候选分别指向对象内人类档案。
- 后续又加入大都会 42045 号来源记录候选，含两张公开领域图像和受限的人类
  档案；它不属于七行分诊快照，仍没有 OCR 或单字分配。
- 六个逐项文献档案覆盖 HUST-OBC、OBIMD、EvoBC、Cambridge-Hopkins 著录表、
  Schwartz 的花园庄东专著和 Liu 的《英藏》月食论文。
- Or. 7694/1595 的争议档案另补记史语所官方书目中的董作宾 1950 年〈殷代月食考〉；
  本次只取得书目页和全文路线，未取得全文，因此没有把论文观点用于本对象年代或
  释读。
- The Or. 7694/1595 dispute file also records the official IHP bibliography
  route for Tung Tso-pin's 1950 lunar-eclipse article. Only the bibliography
  page and full-text route were obtained; the article was not opened, so no
  date or reading from it is applied to this object.
- 候选图谱已包括单字—构件、单字—卜辞来源记录、异体、本地图像资产和 EvoBC 演化候
  选关系。
- 图谱 schema 现已把路线完整性置信度与未来的校准假说概率分开；现有
  `confidence_level` 仍只表示路线 metadata。
- 六个 HUST 单字档案现已加入对象特异的已打开证据综合，包含直接观察、文件名候选、
  反证、权利边界和具体下一步。
- 大英图书馆 Or. 7694/1595 候选现已加入来源文字与正反面图像对照页，保留两面显示
  字符串，不生成 OCR 或项目摹写。
- 同一候选现有十个区域的视觉复核页和 CSV。区域框与两张 CC0 图像的校验和绑定，
  但没有把区域对应到单字、行序、阅读顺序或页面字符串。
- 相关的 Or. 7694/1535v 候选现有八个区域的视觉复核页和 CSV，区域框与 CC0
  图像绑定，但没有把任何区域对应到文字。
- 该候选的文献页现记录了有名有据的年代争议：大英图书馆/Scroll 路线报告公元前
  1192 年，Liu 的 *Early China* 摘要为《英藏》885/886 记录公元前 1166 年的
  论证。两者仍是来源路线，本项目不采用任何一个年代。
- OBIMD 来源对象的来源包路线现显示生效的
  `metadata_only_until_verified`；中央历史 manifest 值仍由有效权利覆盖记录追溯。
- Or. 7694/1595 与 Or. 7694/1535v 对象现保存三张未改动的 CC0 来源图像；
  人类档案链接和校验和均已绑定，页面文字和著录仍分别待复核。
- 相关路线复核现把 Google Arts & Culture 标为同源聚合路线，把 Sketchfab
  标为带明确 NoAI 限制的 CC Attribution 路线；两者没有新增图像字节或独立文字证据。
- Or. 7694/1535v 候选现记录精确标识的负面路线检索：通用 Google Arts 页面
  列出其他大英图书馆来源号，但没有 1535；这只是路线记录，不证明其他地方没有图像。
- Or. 7694/1595 候选现记录 OBID 数据库入口、H/Y 类属和 2026-08-21
  检索边界；没有把数据库首页或未取得的查询结果当成第二见证。
- 权利仍按来源分别处理；权利未解决时，`metadata_only_until_verified` 继续阻止
  公开图像再利用。
- 大型来源登记入口现明确：OBIMD 的历史 `licensed_for_repository` 值不是
  生效授权；复核者必须先读取有效权利覆盖表。
- The large-source entry now states that OBIMD's historical
  `licensed_for_repository` value is not an effective grant; reviewers must
  read the active rights override first.

These are archive and route improvements. They do not promote an object,
character, inscription, component, or evolution edge into a confirmed claim.

这些是档案和路线改进，不把对象、单字、卜辞、构件或演化边提升为已确认结论。

## Earlier HEAD receipt / 较早主分支回执

The object-repair baseline is `6078f7ae9c4`. Its preceding commits
`bf243ee38b9` and `274d7a46b6f` added the Met 42045 two-view page and the
Or. 7694/1595 astronomical-date dispute matrix. The baseline repaired the
direct image link in the obs-char-000621 multi-instance dossier. These
remain source-record or dispute aids; none creates OCR, a transcription, or
a decipherment claim. This receipt is refreshed by a later audit commit;
the audit page intentionally does not self-embed its own commit hash.

对象修复基线为 `6078f7ae9c4`。此前的
`bf243ee38b9`、`274d7a46b6f` 分别为 Met 42045 增加双图人类证据页，
为 Or. 7694/1595 增加月食年代争议矩阵。该基线修复了
obs-char-000621 多实例档案中的直接图像链接。这些都只是来源记录或争议
辅助，没有生成 OCR、摹写或破译主张。本回执由后续审计提交刷新，
审计页不把自身提交哈希写入正文，以避免自指过时。

Earlier receipts bound to that follow-up were:

- Met 42045 two-view suite: `4 tests OK`.
- Or. 7694/1595 date-dispute suite: `4 tests OK`.
- obs-char-000621 multi-instance suite: `4 tests OK`.
- Full suite in the refreshed working tree: `1040 tests OK` in `645.768`
  seconds.
- Repository skeleton: `PASS repository skeleton`.
- Full strict human-material gate: exit `0`, `156842` Markdown files,
  and all four debt counts `0`.
- Commit-message format: `PASS` before the audit refresh was pushed.
- Remote branch verification: `PASS` after the audit refresh was pushed.

该次较早跟进绑定的回执如下：

- Met 42045 双图套件：`4 tests OK`。
- Or. 7694/1595 年代争议套件：`4 tests OK`。
- obs-char-000621 多实例套件：`4 tests OK`。
- 刷新后工作树全量测试：`1040 tests OK`，耗时 `645.768` 秒。
- 仓库骨架：`PASS repository skeleton`。
- 严格人类资料门：退出码 `0`，`156842` 篇 Markdown，四项债务均为 `0`。
- 提交信息格式：审计刷新推送前为 `PASS`。
- 远端分支核验：审计刷新推送后为 `PASS`。

The user-owned untracked file `doc/public/user_prompt/1.txt` remains outside
the commits and was not read or modified. No AI v2 experiment record was
created by this follow-up, and no candidate-delivery channel was opened.

用户拥有的未跟踪文件 `doc/public/user_prompt/1.txt` 仍未进入提交，且未被读取
或修改。本次没有创建 AI v2 实验记录，也没有开启候选交付通道。

## Autonomous laboratory status / 自主实验室状态

The pilot tool can freeze evidence, seal a private label, create run openings,
lock raw outputs, and perform one local diagnostic score. It does not itself
select cases, invoke a model, create independent contexts, or provide an
external isolated scorer.

The new triage command now supplies the first work-order step for the nine
opened inscription source-record candidates. It ranks visible evidence and
blockers only; it is not model judgment, calibration, or candidate delivery.

The earlier targeted pilot, triage, and reviewed-summary suites passed 49, 4,
and 4 tests respectively. The current object suite adds five bounded tests;
the v2 validator still finds no real experiment record.

A reviewed [v4 diagnostic pilot record][pilot-report] exists. Its two runs
used the same model family with fresh contexts, disagreed on the top-ranked
opaque ID, and therefore remained `diagnostic_fail_withheld`.

pilot 工具可以冻结证据、密封私有标签、创建运行开封记录、锁定原始输出，并进行一次
本地诊断评分；但它不会自行选案、调用模型、创建真正独立上下文，也不提供外部隔离评
分器。

新增的选案分诊命令现为九个已打开卜辞来源记录候选提供第一步工作顺序。它只排序可见
证据和阻断项，不是模型判断、校准或候选交付。

此前试点、选案分诊和已复核摘要的定向测试分别通过 49、4、4 项。当前对象套件
新增五项边界测试；v2 校验器仍找不到真实实验记录。

已有一份已复核的 v4 诊断记录。两次运行使用同一模型族但不同上下文，
对不透明 ID 的首位排序不一致，因此结果保持 `diagnostic_fail_withheld`。

The existing diagnostic pilot is withheld and uncalibrated. It is a pipeline
exercise, not a clean holdout, not Gate 3, and not an AI-adjudicated candidate.
Unknown pretraining exposure remains a permanent blocker for probability
calibration on that case.

现有诊断试点是扣留且未校准的。它只是流程演练，不是干净留出集、不是 Gate 3，也不是
AI 裁决候选。该案的预训练暴露未知，因此不能进入概率校准。

## Blocking conditions / 当前阻断条件

1. There is no real v2 benchmark record with sealed gold, family splits,
   locked runs, and recomputed metrics.
2. There is no verified calibration cohort or declared OOD support domain for
   unknown-character discovery.
3. There is no cryptographically independent model run or external scorer
   receipt for a user-facing candidate.
4. Many inscription and plate routes still lack permitted images, OCR, or a
   line-addressable transcription.
5. Source rights and derivative ancestry remain unresolved for several major
   datasets.

1. 尚无包含密封答案、家族分割、锁定运行和重算指标的真实 v2 基准记录。
2. 尚无可核验校准群，也没有针对未释字发现声明适用域的 OOD 支持范围。
3. 尚无密码学独立的模型复跑或外部评分回执，不能交付用户候选。
4. 多数卜辞与图版路线仍缺获准图像、OCR 或可定位的逐行释文。
5. 多个主要数据集的来源权利和派生祖先链仍未解决。

## Next strategic order / 下一战略顺序

The next work must deepen a few object and inscription dossiers, then create a
real sealed benchmark record from permitted evidence. It must not expand file
counts merely to make the v2 validator pass.

下一步应先深化少量对象和卜辞档案，再用获准证据创建真实密封基准记录；不能为了让
v2 校验器通过而单纯增加文件数量。

Until the blocking conditions are cleared, every numerical output remains an
`uncalibrated_score`, and every live unknown-character case must abstain or be
withheld. The user may receive a candidate only after the strategy's registered
calibration, leakage, falsification, rerun, rights, and delivery gates pass.

在阻断条件清除前，所有数值输出都只能叫 `uncalibrated_score`，真实未释字案件必须
弃权或扣留。只有在战略登记的校准、泄漏、反证、复跑、权利和交付门槛全部通过后，用户
才可收到候选。

## Requirement coverage audit / 19 项要求覆盖审计

This section is an execution control, not a claim that the project is
finished. `implemented` means the rule and a current check exist;
`partial` means human evidence exists only for a bounded subset;
`blocked` means the missing evidence prevents the next promotion gate.

本节是执行控制，不是完成声明。`implemented` 表示规则和当前校验均
存在；`partial` 表示只完成了有限对象的人类证据；`blocked` 表示缺失
证据阻断下一道提升门槛。

| Requirement | Status | Current evidence or blocker |
| --- | --- | --- |
| 1 human-first positioning | implemented | root README and strategy |
| 2 workflow | partial | dossiers exist; many routes remain |
| 3 no template substitution | implemented | human gate and v2 no-record stop |
| 4 no unreviewed scholarship | implemented | candidate and no-claim fields |
| 5 required reading | implemented | AGENTS and repository reading rules |
| 6 co-located archives | implemented | object-local human + support |
| 7 character depth | partial | six visual dossiers; bulk gaps |
| 8 character fields | partial | filename and visual samples |
| 9 inscription/plate | blocked | OCR and plate locators missing |
| 10 literature | partial | six dossiers; broad corpus absent |
| 11 source range | partial | routes; access gaps remain |
| 12 priority-source handling | partial | HUST, OBIMD, EvoBC and IHP samples |
| 13 processing | partial | manifests; review gaps remain |
| 14 provenance/rights | partial | hashes; conflicts block reuse |
| 15 graph/statistics | partial | candidates; review incomplete |
| 16 large files | implemented | ignored archives + manifests |
| 17 doc quality | partial | gates pass; legacy repair queue |
| 18 validation/push | implemented | tests, gate, commit, push |
| 19 completion standard | blocked | no valid v2/calibrated gate |

The next work order follows the blocked rows, not the number of files:

1. Add a few inscription records with permitted image or text evidence and
   line-addressable provenance.
2. Reconcile rights and derivative ancestry before any public image use.
3. Build a family-isolated known-answer cohort and an external scoring route.
4. Run v2 only after the cohort, leakage audit, independent rerun, and score
   receipt are real; otherwise keep all unknown cases withheld.

下一步按阻断项排序，而不是按文件数量排序：先补少量可定位的卜辞
资料，再解决权利与派生祖先链，随后建立隔离校准集和外部评分路线。
在这些条件真实存在前，未知字案例继续扣留，不能进入用户候选通道。

[pilot-report]: ../../public/user_research/011_ai-diagnostic-pilot-2026-08-13
[strategy]: README.md
