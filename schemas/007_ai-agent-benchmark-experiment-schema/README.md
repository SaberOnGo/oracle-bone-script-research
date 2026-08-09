# AI Agent Benchmark Experiment v2 / AI Agent 基准实验 v2

## Purpose / 用途

English:
This schema turns the autonomous-candidate strategy into a reproducible
experiment contract. It records frozen cases, family-aware splits, calibrated
probabilities, abstention, counter-evidence, falsification, execution and
model-independent reruns, AI adjudication, leakage review, and recomputable
metrics.

简体中文：
本 schema 把自主候选战略落实为可复跑实验合同。它记录冻结案件、按家族
分割的数据集、校准概率、弃权、反对证据、证伪、执行复跑、模型独立复跑、
AI 裁决、泄漏审计和可复算指标。

This schema supports human-readable research dossiers. It does not replace an
object-local dossier, source evidence, inscription context, or dispute history.

本 schema 服务于人类可读研究档案，不替代对象目录内档案、来源证据、
卜辞上下文或争议史。

Normative companions:

- [autonomous-candidate strategy][strategy];
- [v1 evidence-pack schema][schema-006];
- [source rights and provenance policy][rights-policy];
- [large-source material policy][large-source-policy];
- [large-source register][large-source-register].

规范性配套文件：

- [自主候选战略][strategy]；
- [v1 证据包 schema][schema-006]；
- [来源权利与出处政策][rights-policy]；
- [大型来源资料政策][large-source-policy]；
- [大型来源登记][large-source-register]。

## Version Boundary / 版本边界

Version 1 evidence packs under schema `006` remain unchanged. Version 2 uses a
separate filename suffix:

```text
*_benchmark-experiment-v2.json
```

The v2 validator never discovers v1 evidence-pack JSON files. A v1 pack may be
one frozen evidence snapshot referenced by a v2 case.

`006` 下的 v1 证据包保持不变。v2 使用独立文件后缀，验证器不会扫描 v1
证据包。v1 证据包可以作为 v2 案件引用的冻结证据快照。

## Validator Layers / 验证层次

The validator first evaluates the complete public JSON Schema. It then applies
cross-field gates for case coverage, family isolation, candidate universes,
pretraining eligibility, locked reruns, gold order, scoring, evidence,
human delivery, and candidate delivery.

验证器首先执行完整公开 JSON Schema，再执行跨字段门禁，覆盖案件类型、
家族隔离、候选全集、预训练资格、锁定复跑、gold 时序、评分、证据、
人类交付包和候选交付。

A public-record `PASS` without private gold is accompanied by
`METRICS_NOT_RECOMPUTED`. It confirms schema and cross-field consistency only.
It does not verify metrics, authorize a withheld case, or confirm scholarship.

未提供私有 gold 时，公开记录的 `PASS` 会同时报告
`METRICS_NOT_RECOMPUTED`。这只确认 schema 与跨字段一致，不表示指标已
复核，不授权被扣留案件，也不确认学术结论。

## Research Boundary / 研究边界

Every public experiment record must use:

```text
research_boundary=benchmark_experiment_not_scholarship
```

An AI court may propose:

```text
delivery_status=ai_adjudicated_candidate
```

The field authorizes delivery only after every cross-field delivery gate below
passes. Merely writing the value, passing schema structure, or recomputing
ignored-local diagnostics does not authorize delivery. Even an authorized
candidate is not a confirmed decipherment, publication, or scholarly consensus.

AI 法庭可以提出 `ai_adjudicated_candidate`，但只有下列跨字段交付门禁
全部通过后才授权交付。仅写入该值、只通过结构检查或复算本地诊断指标，
都不构成交付授权。获准交付的候选仍不是已确认释读、发表成果或学界共识。

## Human-First Opening Order / 人类优先打开顺序

1. Open the bilingual human delivery package entry point.
2. Open the linked object-local glyph and inscription dossiers.
3. Review source, rights, plate, catalog, and excavation routes.
4. Read supporting evidence, opposing evidence, and concrete missing items.
5. Open the v1 evidence snapshot and frozen input manifest.
6. Inspect the v2 experiment, probability distribution, and leakage audit.
7. Inspect the external scorer receipt when delivery is proposed.

1. 先打开双语人类交付包入口。
2. 打开其链接的对象目录内字形与卜辞档案。
3. 再核对来源、权利、图版、著录和出土路线。
4. 阅读支持证据、反对证据和具体缺失项。
5. 打开 v1 证据快照和冻结输入清单。
6. 检查 v2 实验、概率分布和泄漏审计。
7. 候选拟交付时，检查外部 scorer receipt。

## Case, Split, And Leakage Rules / 案件、分割与泄漏规则

Every benchmark must contain all four case types:

1. `masked_known_reading`;
2. `historically_disputed`;
3. `null_or_negative_control`;
4. `hard_challenge`.

每个 benchmark 必须同时包含四类案件：隐藏答案已释案、历史争议案、
空白或负对照，以及困难挑战案。

Every case records a non-answer-bearing `blind_alias`, an
`evidence_cutoff_at` timestamp, the frozen input checksum, source snapshots,
training-cutoff evidence, and a reviewed dependency manifest. Each source
snapshot binds `source_ancestor_id`, `derivative_family_id`, and
`snapshot_sha256` so common source and image-derivative ancestry can be audited.

每案都要记录不带答案的 `blind_alias`、`evidence_cutoff_at` 时间截点、
冻结输入 checksum、来源快照、训练截止证据和依赖 manifest。每个来源快照
绑定 `source_ancestor_id`、`derivative_family_id` 和 `snapshot_sha256`，
以审计共同来源和图片派生依赖。

The closed candidate universe must contain at least three unique values and
must include `unknown_or_other`. The unknown option is real probability mass
alongside explicit abstention, not an after-the-fact escape label.

封闭候选全集至少包含三个互异值，且必须包含 `unknown_or_other`。未知项是
与显式弃权并列的真实概率质量，不能在评分后临时补入。

- Split by `family_id`, never by random CSV row.
- One family may appear in only one split.
- A family covers shared objects, bones, inscriptions, glyph variants,
  source ancestors, catalog derivatives, and image-derivative ancestry.
- Gold labels, modern-label leaks, codepoint shortcuts, peer-run outputs, and
  post-unseal outputs are forbidden agent routes.
- `clean_holdout_eligible` requires
  `pretraining_exposure=verified_post_training_cutoff`.
- Unknown exposure remains `pretraining_exposure_unknown` and diagnostic only.
- Retrospective or possibly exposed cases cannot calibrate candidate delivery.

- 必须按 `family_id` 分割，不能随机分割 CSV 行。
- 同一资料家族只能出现在一个 split。
- 家族覆盖共同实物、甲片、卜辞、异体、来源祖先、著录派生和图片派生。
- gold、今字标签捷径、codepoint 捷径、同伴输出和解封后输出禁止进入
  Agent 上下文。
- `clean_holdout_eligible` 要求
  `pretraining_exposure=verified_post_training_cutoff`。
- 暴露未知时必须记为 `pretraining_exposure_unknown`，只能用于诊断。
- 回溯案或可能已暴露案件不得用于校准候选交付。

## Rerun Independence / 复跑独立性

A fresh context on the same base model is only an `execution_rerun` with
`independence_tier=execution_only`. It tests execution repeatability and must
not be counted as model-independent confirmation. Model-independent evidence
uses the separate `model_independent_rerun` role and
`independence_tier=model_independent`. Candidate delivery requires that
explicit model-independent rerun.

同一基础模型即使使用新上下文，也只能标为 `execution_rerun` 和
`independence_tier=execution_only`。它只检验执行复现，不能计作模型独立
确认。模型独立复跑必须另标 `model_independent_rerun` 和
`independence_tier=model_independent`；候选交付必须具备该明确复跑。

Every rerun uses a fresh context, cannot read prior-run outputs, keeps gold
sealed, and records model, retrieval, evidence, and tool ancestry.

每次复跑都要使用新上下文，不得读取先前运行输出，保持 gold 封存，并记录
模型、检索、证据和工具谱系。

## Probability And Delivery Gate / 概率与交付门

The numeric probability is a calibrated task probability, not an LLM
self-score. The threshold must be preregistered from a calibration split.
The record stores the confidence level, effective sample requirement, target
selective precision, threshold support status, and OOD tests.

数值概率是任务级校准概率，不是 LLM 自评分。阈值必须由 calibration split
预注册，并记录置信水平、有效样本要求、目标选择性精确率、阈值支持状态和
OOD 检查。

`ai_adjudicated_candidate` is allowed only when all of these hold:

- the calibrated lower bound reaches the registered threshold;
- `threshold_status=scorer_derived_supported`;
- calibration uses a verified external isolated-scorer artifact;
- the case is `clean_holdout_eligible` and inside the calibration domain;
- required evidence blockers are empty;
- no hard opposition remains;
- every locked run agrees with the delivered prediction;
- a model-independent rerun and completed locked adjudication exist;
- no suspected, confirmed, indeterminate, or pretraining leakage remains;
- external scoring is valid and the holdout is retired after one score;
- the human delivery package and its rights and content reviews are complete;
- at least two reviewed, deliverable, independent evidence families support it.

只有校准下界达到预注册阈值、阈值为 scorer 派生支持、外部隔离评分产物
已复核、案件为合格干净留出且位于校准域、强制证据阻断项为空、没有硬性
反证、全部锁定运行结论一致、模型独立复跑与锁定裁决完整、泄漏已排除、
一次外部评分后留出集已退役、人类交付包完整，且至少两个经依赖与权利复核
的独立证据家族支持时，才允许交付 `ai_adjudicated_candidate`。

Out-of-domain cases must abstain and clear the numeric probability. A
structure pass cannot override any delivery blocker.

域外案件必须弃权并清空数值概率。结构通过不能覆盖任何交付阻断项。

## Sealed Gold / 密封 gold

The public record stores only an HMAC-SHA-256 commitment. The committed
message is canonical UTF-8 JSON with sorted keys and compact separators. It
binds `benchmark_id`, `benchmark_version`, `gold_key_id`,
`case_candidate_manifest_sha256`, `protocol_sha256`, and `labels`.

公开记录只保存 HMAC-SHA-256 commitment。参与 commitment 的消息使用
UTF-8、键排序和紧凑分隔符，并绑定 `benchmark_id`、
`benchmark_version`、`gold_key_id`、`case_candidate_manifest_sha256`、
`protocol_sha256` 和 `labels`。

A naked hash of a low-entropy answer is not accepted. Gold must be sealed
before the first run. Agents and adjudicators keep `gold_access` as
`sealed_unavailable`. The private payload belongs under `.working/` or
`local_private_data/` and must never be committed. A record backed by local
ignored gold uses `storage_class=ignored_local_diagnostic`; it supports
diagnostics only and can never authorize candidate delivery.

不得使用可枚举低熵答案的裸 hash。gold 必须在首次运行前密封。Agent 和
裁决者的 `gold_access` 必须保持 `sealed_unavailable`。私有 payload 只能
放在 `.working/` 或 `local_private_data/`，不得提交。由本地忽略 gold 支持
的记录必须标为 `storage_class=ignored_local_diagnostic`，只能用于诊断，
永远不能授权候选交付。

Delivery uses `storage_class=external_isolated_scorer`. The scorer receives the
locked request only once, records a verified receipt, and changes the gold and
evaluation states to `scorer_only_unsealed_retired` and
`retired_after_single_scoring`. Any later use is diagnostic reuse only.

交付必须使用 `storage_class=external_isolated_scorer`。评分器只接收一次
锁定请求，形成已复核 receipt，并把 gold 与 evaluation 分别改为
`scorer_only_unsealed_retired` 和 `retired_after_single_scoring`。之后任何
复用都只能用于诊断。

## Metrics / 指标

The isolated scorer recomputes:

- multiclass Brier mean;
- natural-log loss with a preregistered probability floor;
- top-1 equal-width ECE with a fixed bin count;
- coverage and covered top-1 error risk.

隔离 scorer 复算多类 Brier 均值、自然对数 log loss、固定分箱 top-1 ECE、
coverage 和已覆盖案件的 top-1 错误风险。

Without private gold, the validator must report
`METRICS_NOT_RECOMPUTED`. A public-record pass is not metric verification.
Supplying ignored-local gold recomputes diagnostics but does not create the
external scoring receipt or a delivery-eligible calibration artifact.

未提供私有 gold 时，验证器必须报告 `METRICS_NOT_RECOMPUTED`。公开记录
通过不等于指标已经复核。提供本地忽略 gold 只能复算诊断指标，不能形成
外部评分 receipt 或可用于交付的校准产物。

Only clean-holdout metrics derived and verified by the external isolated
scorer may set `threshold_status=scorer_derived_supported`.

只有外部隔离评分器从干净留出集派生并复核的指标，才可以把
`threshold_status` 设为 `scorer_derived_supported`。

## Human Delivery And Source Audit / 人类交付与来源审计

Candidate delivery requires a bilingual `human_delivery_package` with a
complete status, checksum, object dossiers, inscription contexts, source
evidence, adjudication memo, dependency graph, and claim-evidence matrix.
Rights and content reviews must be complete, and no missing item may be
blocking.

候选交付要求双语 `human_delivery_package` 完整并带 checksum，且包含对象
档案、卜辞上下文、来源证据、裁决说明、依赖图和主张证据矩阵。权利与内容
复核必须完成，也不能存在 blocking 缺失项。

Every source snapshot and evidence item records source ancestry, derivative
family, checksum, `rights_status`, `allowed_delivery_form`, `risk_note`,
`large_source_register_ref`, and `dependency_review_status`. Evidence with a
rights conflict, unknown rights, withheld delivery form, or incomplete
dependency review cannot count toward the two-family delivery minimum.

每个来源快照和证据项都记录来源祖先、派生家族、checksum、
`rights_status`、`allowed_delivery_form`、`risk_note`、
`large_source_register_ref` 和 `dependency_review_status`。权利冲突或未知、
交付形式为 withhold，或依赖复核未完成的证据，不能计入两个独立证据家族
的交付下限。

## Storage / 存储

Active experiment runs belong in the ignored directory:

```text
doc/public/user_research/generated/ai-agent-benchmark-experiments/
```

Commit the schema, validator, protocol description, and later a human-readable
redacted result summary. Do not commit raw gold, model scratch data, or
unreviewed generated runs.

进行中的实验放在上述忽略目录。Git 中只提交 schema、验证器、协议说明和
以后形成的人类可读脱敏结果摘要；不得提交 raw gold、模型草稿或未复核
生成结果。

## Validation / 校验

Public schema and cross-field validation without gold:

```powershell
python tools/validation/validate_ai_agent_benchmark_experiments.py `
  --path doc/public/user_research/generated/ai-agent-benchmark-experiments
```

Local ignored-gold diagnostic recomputation:

```powershell
python tools/validation/validate_ai_agent_benchmark_experiments.py `
  --path .working/example_benchmark-experiment-v2.json `
  --gold-path local_private_data/example-private-gold.json
```

The second command is diagnostic even if metrics match. It cannot substitute
for the external isolated scorer, its verified receipt, or one-shot holdout
retirement. Passing either command does not authorize candidate delivery and
does not confirm an oracle-bone reading.

第二条命令即使指标一致也仍是诊断，不能替代外部隔离评分器、已复核
receipt 或一次评分后的留出集退役。任一命令通过都不授权候选交付，也不
表示甲骨文字释读已确认。

[strategy]: ../../doc/project/005_ai-agent-research-assistant-design/
[schema-006]: ../006_ai-agent-evidence-pack-schema/
[rights-policy]: ../../doc/project/002_source-rights-and-provenance-policy/
[large-source-policy]: ../../doc/project/006_large-source-material-handling/
[large-source-register]: ../../project_registry/006_large-source-register/
