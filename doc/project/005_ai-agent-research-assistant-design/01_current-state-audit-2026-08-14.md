# Current State Audit / 当前状态审计

Status: `current_state_audit`

Snapshot date: `2026-08-14`

Snapshot commit: `8408aaa79d0`

## Purpose / 目的

This audit binds the autonomous-candidate strategy to the current disk state.
It is an operational audit, not a paleographic conclusion, a decipherment
result, or published scholarship.

本审计把自主候选战略绑定到当前磁盘状态。它是运行审计，不是文字学结论、破译结果
或已发表学术成果。

The normative rules remain in the [autonomous-candidate strategy][strategy].
This file records what is and is not executable at the snapshot commit.

规范规则仍在[自主候选战略][strategy]中。本文件只记录该提交上什么已经可运行、什么
仍不可运行。

## Reproducibility receipts / 可复跑凭据

The following commands were run from the repository root:

- `python -m unittest discover -s tests -v`: `899 tests OK`.
- `python tools/validation/check_repository_skeleton.py`: `PASS`.
- `validate_ai_agent_evidence_packs.py`: `PASS 1 file`.
- `validate_ai_agent_benchmark_experiments.py`: `FAIL no v2 records`.

以上命令均从仓库根目录执行：全量测试为 `899 tests OK`，骨架校验为 `PASS`，v1
证据包校验为 `PASS 1 file`，v2 实验校验为 `FAIL no v2 records`。

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
- Item 506 now has a source-only treatment with English/Chinese catalog
  differences, private image hashes, and no committed image derivative.
- Four item-level literature dossiers cover HUST-OBC, OBIMD, EvoBC, and the
  Cambridge-Hopkins finding list.
- Candidate graph edges now include character-to-component candidates,
  character-to-inscription source-record candidates, variants, local assets,
  and EvoBC correspondence candidates.
- Rights remain source-specific. `metadata_only_until_verified` still blocks
  public image reuse where permission is unresolved.

- 三十个史语所馆藏对象目录已有现场来源证据档案，记录页面路线、著录事实、图像校验
  和具体缺口。
- 当前批次新增 770、771、772 号对象；其来源描述与独立释读明确分开。
- 508 号对象也采用同一来源限定，仅保留私有图像校验，不提交图像派生件。
- 503 号对象也采用同一来源限定，仅保留私有图像校验，不提交图像派生件。
- 四个逐项文献档案覆盖 HUST-OBC、OBIMD、EvoBC 和 Cambridge-Hopkins 著录表。
- 候选图谱已包括单字—构件、单字—卜辞来源记录、异体、本地图像资产和 EvoBC 演化候
  选关系。
- 权利仍按来源分别处理；权利未解决时，`metadata_only_until_verified` 继续阻止
  公开图像再利用。

These are archive and route improvements. They do not promote an object,
character, inscription, component, or evolution edge into a confirmed claim.

这些是档案和路线改进，不把对象、单字、卜辞、构件或演化边提升为已确认结论。

## Autonomous laboratory status / 自主实验室状态

The pilot tool can freeze evidence, seal a private label, create run openings,
lock raw outputs, and perform one local diagnostic score. It does not itself
select cases, invoke a model, create independent contexts, or provide an
external isolated scorer.

A reviewed [v4 diagnostic pilot record][pilot-report] exists. Its two runs
used the same model family with fresh contexts, disagreed on the top-ranked
opaque ID, and therefore remained `diagnostic_fail_withheld`.

pilot 工具可以冻结证据、密封私有标签、创建运行开封记录、锁定原始输出，并进行一次
本地诊断评分；但它不会自行选案、调用模型、创建真正独立上下文，也不提供外部隔离评
分器。

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
| 10 literature | partial | four dossiers; broad corpus absent |
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
