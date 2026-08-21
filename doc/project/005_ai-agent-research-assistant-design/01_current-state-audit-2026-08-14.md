# Current State Audit / 当前状态审计

Status: `current_state_audit`

Audit update date: `2026-08-21`

Audited base commit: `404e23b4284`

Follow-up verification date: `2026-08-21`

Historical baseline commit: `7c8b8a29a35` (2026-08-14)

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
- Human-material gate regression tests: `3 tests OK`; they cover summary
  failure propagation, the full-scan coverage floor, and debt ceilings.

以上三项全仓库回执属于 2026-08-14 历史基线，不能替代当前主分支的
重新扫描。它们保留了 981 项测试、骨架校验、human-research gate
以及四项债务计数的当时证据。

## Current follow-up receipts / 当前跟进回执

The current 2026-08-21 follow-up ran targeted suites after the object and
rights updates. It did not rerun the repository-wide scans because those
scans are I/O-heavy; their status remains unverified for this commit.

2026-08-21 的跟进只在对象、权利和自主试点更新后运行定向测试，没有重新运行
全仓库 I/O 密集型扫描；这些扫描在当前提交上的状态仍未复核。

Current targeted receipts include the following:

- AI pilot: `49 tests OK`; case triage: `4 tests OK`; pilot summary:
  `4 tests OK`.
- v2 benchmark contract: `68 tests OK`; no real v2 record was found.
- British Library 1595: `6 tests OK`; 1535: `7 + 3 tests OK`.
- Ningxia HYZ 421: `5 tests OK`; effective OBIMD rights: `5 + 3 tests OK`.

当前定向回执包括：AI 试点 `49 tests OK`、选案分诊 `4 tests OK`、试点摘要
`4 tests OK`；v2 合同 `68 tests OK`，但没有真实 v2 记录；英国图书馆 1595
为 `6 tests OK`、1535 为 `7 + 3 tests OK`；宁夏 HYZ 421 为 `5 tests OK`；
OBIMD 有效权利为 `5 + 3 tests OK`。1595 的 OBID 入口、释文检索页和原文
检索页仍只是检索线索；公开页返回需登录的访问边界，没有取得
`Heji 40610` 或 `Yingcang 886` 的精确结果。

The v1 pass covers one draft scaffold whose evidence sections remain empty.
It does not show research evidence or autonomous adjudication capability.

v1 通过只覆盖一个仍为空的草稿脚手架，不表示已有研究证据或自主裁决能力。

The v2 failure is intentional evidence of an unopened numerical channel. No
public v2 experiment record currently exists under
`doc/public/user_research/generated/ai-agent-benchmark-experiments/`.

v2 失败说明数值通道尚未打开。当前没有公开的 v2 实验记录，不能把测试 fixture 或
本地 pilot 记录当作真实基准实验。

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
  prose from transcription and records explicit OCR and plate gaps.
- An IHP item 1215 inscription source-record candidate now records the museum
  short display, three private image checksums, and independent plate/OCR gaps.
- An IHP item 771 inscription source-record candidate now records the
  source-reported proposed divination, two private HTML hashes, three private
  image hashes, and independent plate/text/OCR gaps.
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
- The central inscription source-record map now routes all seven opened
  candidates to their object-local human dossiers.
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
  图版缺口。
- 1215 号对象另有卜辞来源记录候选，记录馆方短文字、三条私有图像校验和，
  并明确独立图版与 OCR 缺口。
- 771 号对象另有卜辞来源记录候选，记录馆方拟译、两份私有 HTML 校验和、三条
  私有图像校验和，并明确独立图版、原文和 OCR 缺口。
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
- 宁夏博物馆 HYZ 421 来源记录候选现保存一张 CC BY-SA 3.0 照片、本地校验和与
  尺寸、来源释文、花园庄东路线及 Schwartz 2019 引用。博物馆权利、图版身份和
  OCR 仍未解决。
- 2026-08-21 重新核对 HYZ 421 的 Commons 结构化字段；对象号、出土地和页面
  显示释文仍是来源报告，未替代博物馆目录或发掘登记。
- The 2026-08-21 HYZ 421 Commons recheck preserves the object, findspot,
  and displayed text as page-level source reports, not museum evidence.
- HYZ 421 候选现有八个区域的视觉复核页和 CSV。区域框与已提交 JPEG 的校验和
  绑定，但没有把区域对应到单字、行序、阅读顺序或页面字符串。
- 中央卜辞来源记录映射表现已把七个已打开候选分别指向对象内人类档案。
- 六个逐项文献档案覆盖 HUST-OBC、OBIMD、EvoBC、Cambridge-Hopkins 著录表、
  Schwartz 的花园庄东专著和 Liu 的《英藏》月食论文。
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

## Autonomous laboratory status / 自主实验室状态

The pilot tool can freeze evidence, seal a private label, create run openings,
lock raw outputs, and perform one local diagnostic score. It does not itself
select cases, invoke a model, create independent contexts, or provide an
external isolated scorer.

The new triage command now supplies the first work-order step for the seven
opened inscription source-record candidates. It ranks visible evidence and
blockers only; it is not model judgment, calibration, or candidate delivery.

The current targeted pilot, triage, and reviewed-summary suites pass 49, 4,
and 4 tests respectively. The v2 validator still finds no real experiment
record, so no calibration or candidate-delivery claim is open.

A reviewed [v4 diagnostic pilot record][pilot-report] exists. Its two runs
used the same model family with fresh contexts, disagreed on the top-ranked
opaque ID, and therefore remained `diagnostic_fail_withheld`.

pilot 工具可以冻结证据、密封私有标签、创建运行开封记录、锁定原始输出，并进行一次
本地诊断评分；但它不会自行选案、调用模型、创建真正独立上下文，也不提供外部隔离评
分器。

新增的选案分诊命令现为七个已打开卜辞来源记录候选提供第一步工作顺序。它只排序可见
证据和阻断项，不是模型判断、校准或候选交付。

当前试点、选案分诊和已复核摘要的定向测试分别通过 49、4、4 项。v2 校验器仍找不
到真实实验记录，因此尚未开启任何校准或候选交付主张。

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
