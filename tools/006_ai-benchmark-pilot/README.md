# AI Benchmark Diagnostic Pilot / AI 基准诊断试点

## Purpose / 用途

English:

This tool freezes a small, explicit set of files from one real object dossier.
It binds private gold to that freeze, creates a pre-dispatch run receipt, and
locks an externally produced blind Agent report. It can score one retired
ignored-local negative-control diagnostic. It does not run a model, calibrate
probabilities, authorize Gate 3, or claim a decipherment.

简体中文：

本工具从一个真实对象档案中冻结少量、显式列出的文件，并按 schema 007
规则建立 HMAC-SHA-256 gold commitment。它只建立模型运行前的诊断管道，
也可校验并锁定外部生成的盲判 Agent 报告，并对一次性本地负对照诊断
评分。它不运行模型、不校准概率、不授权 Gate 3，也不声称完成释读。

## Boundaries / 边界

- Every output is `diagnostic_only` and
  `pretraining_exposure_unknown`.
- Every output is `benchmark_pilot_not_scholarship`.
- `freeze` and `seal` contain no model prediction. `lock-run` may retain a
  complete Agent distribution but marks it uncalibrated and withheld.
- `score-local` opens ignored-local gold once, retires that diagnostic, and
  always keeps candidate delivery withheld.
- Private gold and all pilot outputs must remain in a Git-ignored path such as
  `.working/` or `doc/public/user_research/generated/`.
- The public commitment contains neither labels nor the HMAC key.
- Answer-bearing metadata fields and allowed-file paths are rejected.
- `freeze` accepts only a registered object directory under `corpus/` whose
  leaf name carries an `obs-`, `src-`, or `coll-` project-object marker.
- Every command creates a new output and refuses to overwrite an old output.

`freeze` 只接受 `corpus/` 下已登记的具体资料对象目录；目录名必须含有
`obs-`、`src-` 或 `coll-` 项目标识。

- 所有输出均标为 `diagnostic_only` 和
  `pretraining_exposure_unknown`。
- 所有输出均标为 `benchmark_pilot_not_scholarship`。
- `freeze` 与 `seal` 不含模型预测；`lock-run` 可保留完整 Agent 分布，
  但必须标为未校准且不交付。
- `score-local` 只打开一次本地忽略区 gold，随后退役该诊断，并始终扣留
  候选交付。
- 私有 gold 和全部试点输出只能放入 `.working/` 或
  `doc/public/user_research/generated/` 等 Git 忽略路径。
- 公开 commitment 不包含标签或 HMAC 密钥。
- 工具拒绝带答案的 metadata 字段和文件路径。
- 每条命令只新建输出；已有输出不会被覆盖。

## Case Selection Triage / 案件选案分诊

The triage command implements only the first strategy step: it creates a
human-readable work order from visible dossier evidence, permitted local
images, checksums, and concrete blockers. Its rank is not a probability and
it does not select a reading or create a benchmark record.

选案命令只实现战略的第一步：根据可见档案证据、获准本地图像、校验和
和具体阻断项生成面向人的工作顺序。排名不是概率，不选择释读，也不生成
基准记录。

```powershell
python tools/006_ai-benchmark-pilot/select_case_triage.py `
  --root . `
  --output .working/case-triage.md `
  --json-output .working/case-triage.json
```

The Markdown report is the primary result. The optional JSON is support only;
both outputs must stay in an ignored path. Open each listed object README and
human dossier before freezing any case for an Agent run.

Markdown 报告是主要结果，JSON 只是辅助；两者都必须留在忽略目录。为 Agent
冻结案件前，必须先打开报告列出的对象 README 和人类档案。

## Freeze Input / 冻结输入

The case metadata JSON has exactly these top-level fields:

```text
case_id, family_id, case_type, split, blind_alias,
evidence_cutoff_at, files
```

`files` maps every explicitly allowed object-relative path to:

```text
source_id, source_ancestor_id, derivative_family_id, rights_status,
allowed_delivery_form, risk_note, large_source_register_ref,
dependency_review_status
```

`--allowed-file` routes and metadata `files` routes must match exactly.
Candidate IDs must be opaque, unique, at least three in number, and include
`unknown_or_other`. The tool hashes the real bytes; it does not copy assets.

`--allowed-file` 路线必须与 metadata 中的 `files` 路线完全一致。候选 ID
必须不带答案、互不重复、至少三个，并包含 `unknown_or_other`。工具对真实
文件字节计算 hash，不复制资产。

```powershell
python tools/006_ai-benchmark-pilot/ai_benchmark_pilot.py freeze `
  --object-dir corpus/path/to/one-object `
  --case-metadata .working/pilot/case-metadata.json `
  --allowed-file 05_human-research-dossier.md `
  --candidate-id candidate-opaque-a `
  --candidate-id candidate-opaque-b `
  --candidate-id unknown_or_other `
  --output .working/pilot/frozen-case.json
```

## Seal Gold / 密封 Gold

The ignored private JSON follows schema 007's commitment binding:

```text
benchmark_id, benchmark_version, gold_key_id,
case_candidate_manifest_sha256, protocol_sha256, labels,
commitment_key_hex
```

The committed message is canonical UTF-8 JSON with sorted keys and compact
separators. The key must contain at least 32 bytes. The public file records
only the binding identifiers and HMAC-SHA-256 commitment. The HMAC message
also includes the tool-derived `frozen_input_sha256`.

`seal` recomputes the frozen case, requires an exact case-label match, and
requires each gold candidate to belong to that case's frozen universe. Gold
cannot be sealed before the case evidence cutoff.

`seal` 会复算冻结案，要求 gold 标签与冻结案件完全对应，并要求每个 gold
候选都属于该案冻结的候选全集。密封时间不得早于证据截止时间。

参与 commitment 的消息使用 UTF-8、键排序和紧凑分隔符。密钥至少包含
32 字节。公开文件只记录绑定标识与 HMAC-SHA-256 commitment。HMAC 消息
还包含工具从冻结案派生的 `frozen_input_sha256`。

```powershell
python tools/006_ai-benchmark-pilot/ai_benchmark_pilot.py seal `
  --frozen-case .working/pilot/frozen-case.json `
  --private-gold .working/pilot/private-gold.json `
  --sealed-at 2026-08-12T00:00:00Z `
  --output .working/pilot/public-commitment.json
```

## Open One Blind Run / 开启一次盲判运行

Create the run-opening receipt after sealing gold and before dispatching the
Agent. It binds the frozen input, candidate manifest, prompt bytes, public
commitment, run identity, role, model identity, and fresh context claim.

必须在 gold 密封之后、Agent 派发之前创建开跑回执。回执绑定冻结输入、
候选 manifest、prompt 字节、公开 commitment、运行身份、角色、模型身份和
全新上下文声明。

```powershell
python tools/006_ai-benchmark-pilot/ai_benchmark_pilot.py open-run `
  --frozen-case .working/pilot/frozen-case.json `
  --public-commitment .working/pilot/public-commitment.json `
  --prompt-manifest .working/pilot/prompt-manifest.md `
  --run-id pilot-run-primary-000001 `
  --role primary `
  --execution-id pilot-execution-000001 `
  --agent-id blind-hypothesis-agent-000001 `
  --model-id diagnostic-model-000001 `
  --model-family diagnostic-family-000001 `
  --context-id fresh-context-000001 `
  --opened-at 2026-08-12T00:01:00Z `
  --output .working/pilot/run-opening.json
```

## Lock One Blind Run / 锁定一次盲判运行

The coordinator writes an ignored prompt manifest before the run. The isolated
Agent returns one JSON prediction containing the full candidate distribution,
an explicit predict or abstain action, supporting and opposing evidence,
falsification checks, and a leakage assessment. The run report records the
exact SHA-256 of both the prompt and raw Agent JSON.

协调器在运行前写入已忽略的 prompt manifest。隔离 Agent 返回一份 JSON
预测，包含完整候选分布、明确预测或弃权动作、正反证、证伪检查和泄漏评估。
运行报告记录 prompt 与原始 Agent JSON 的确切 SHA-256。

```powershell
python tools/006_ai-benchmark-pilot/ai_benchmark_pilot.py lock-run `
  --frozen-case .working/pilot/frozen-case.json `
  --run-opening .working/pilot/run-opening.json `
  --run-report .working/pilot/run-report.json `
  --prompt-manifest .working/pilot/prompt-manifest.md `
  --agent-output .working/pilot/agent-output.json `
  --locked-at 2026-08-12T00:03:00Z `
  --output .working/pilot/locked-run.json
```

`lock-run` recomputes frozen hashes and verifies every report identity field
against the opening receipt. It checks the candidate universe, distribution,
frozen evidence, counterevidence, falsification, and leakage consistency. A
prediction needs support for its selected candidate; a triggered falsifier
for that candidate requires abstention. The time chain must satisfy
`sealed < opened < started < completed < locked`. Its output always uses
`probability_status=uncalibrated_agent_distribution`,
`calibration_status=not_calibrated`, and `delivery_status=withheld`.

`lock-run` 会复算冻结 hash，并把报告的每个运行身份字段与开跑回执核对。
它还核验候选全集、分布、冻结证据、反证、证伪和泄漏记录的一致性。
做出预测时，所选候选必须有支持证据；该候选的反证一旦触发，必须弃权。
时间链必须满足 `sealed < opened < started < completed < locked`。输出始终
标为未校准 Agent 分布、未校准且不交付。

## Lock One Adjudication / 锁定一次裁决

`lock-adjudication` binds an externally produced final-adjudicator report to
all locked runs. It requires a fresh context, sealed gold, new agent and
execution identities, a model and model family not used by the research runs,
the frozen evidence hash, and retrieval and tool-manifest hashes. It does not
run a model or read private gold.

`lock-adjudication` 把外部生成的最终裁决报告绑定到全部锁定运行。它要求
全新上下文、封存 gold、新的 Agent 和执行身份、未用于研究运行的模型及
模型家族、冻结证据 hash，以及检索快照和工具 manifest 的 hash。它不运行
模型，也不读取私有 gold。

The adjudicator JSON must contain exactly these fields:

```text
case_id, decision, selected_candidate_id, abstention_reason_code,
best_alternative_candidate_id, disagreement_resolution, evidence_blockers,
hard_opposition, ood_status, falsification_summary, probability_status,
delivery_status, rationale, next_source_question
```

`probability_status` must be `not_generated` and `delivery_status` must be
`withheld`. The command writes a JSON binding and a bilingual Markdown memo;
the Markdown memo is the human-facing result. Both outputs must stay ignored.

裁决 JSON 必须严格包含上述字段。`probability_status` 必须为
`not_generated`，`delivery_status` 必须为 `withheld`。命令同时写入 JSON
绑定和双语 Markdown 说明，Markdown 说明是面向人的结果；两个输出都必须
位于 Git 忽略区。

```powershell
python tools/006_ai-benchmark-pilot/ai_benchmark_pilot.py `
  lock-adjudication `
  --frozen-case .working/pilot/frozen-case.json `
  --public-commitment .working/pilot/public-commitment.json `
  --locked-run .working/pilot/locked-run-primary.json `
  --locked-run .working/pilot/locked-run-rerun.json `
  --adjudicator-output .working/pilot/adjudicator-output.json `
  --retrieval-snapshot .working/pilot/retrieval-snapshot.json `
  --tool-manifest .working/pilot/tool-manifest.json `
  --adjudicator-id adjudicator-agent-000001 `
  --execution-id adjudicator-execution-000001 `
  --model-id adjudicator-model-000001 `
  --model-family adjudicator-family-000001 `
  --context-id adjudicator-context-000001 `
  --training-knowledge documented `
  --locked-at 2026-08-12T00:05:00Z `
  --output .working/pilot/locked-adjudication.json `
  --human-output .working/pilot/adjudication-memo.md
```

This remains a diagnostic receipt. It always keeps probability and candidate
delivery withheld; a complete v2 experiment still needs calibration, external
one-shot scoring, and the full human delivery package.

这仍然只是诊断回执。它始终扣留概率和候选交付；完整 v2 实验仍须具备
校准、外部一次性评分和完整人类交付包。

## Score One Local Diagnostic / 评分一次本地诊断

`score-local` only supports a frozen `null_or_negative_control`. It requires
at least two unique locked runs. Before reading private gold once, it
recomputes the frozen case, checks every locked report and prediction, and
binds each run to the same candidate manifest, protocol, and public
commitment.

`score-local` 只支持已冻结的 `null_or_negative_control`，并要求至少两次
互异的锁定运行。工具只读取一次私有 gold；读取前会复算冻结案，核验每份
锁定报告与预测，并要求所有运行绑定同一候选 manifest、协议和公开
commitment。

```powershell
python tools/006_ai-benchmark-pilot/ai_benchmark_pilot.py score-local `
  --frozen-case .working/pilot/frozen-case.json `
  --public-commitment .working/pilot/public-commitment.json `
  --private-gold .working/pilot/private-gold.json `
  --locked-run .working/pilot/locked-run-primary.json `
  --locked-run .working/pilot/locked-run-rerun.json `
  --scored-at 2026-08-12T00:04:00Z `
  --output .working/pilot/local-score-receipt.json
```

The receipt reports `pipeline_diagnostic_pass` only when every run abstains,
selects no candidate, ranks the sealed null label first, and records
`indeterminate` leakage with `pretraining_exposure_unknown`. Every other
well-formed result is `diagnostic_fail_withheld`. Either result retires this
local evaluation after its single query. Neither result generates a research
probability, authorizes Gate 3, or permits candidate delivery.

仅当每次运行都弃权、不选择候选、把密封的空标签排在首位，并以
`pretraining_exposure_unknown` 记录 `indeterminate` 泄漏时，回执才写为
`pipeline_diagnostic_pass`。其他格式有效的结果均写为
`diagnostic_fail_withheld`。无论哪种结果，该本地评估都在一次查询后退役，
且不生成研究概率、不授权 Gate 3、不允许候选交付。

## Residual Limits / 剩余限制

The local commitment is neither externally signed nor independently
timestamped. An operator who controls the ignored files and HMAC key could
forge a new local chain. Model IDs, fresh-context claims, and execution
isolation are coordinator assertions; this tool cannot prove model
independence or absence of pretraining exposure. It verifies file bindings
and contract consistency, not scholarly truth or probability calibration.

本地 commitment 没有外部签名或独立时间戳。能控制忽略文件和 HMAC 密钥的
操作者仍可伪造新的本地链。模型 ID、全新上下文和执行隔离由协调器声明；
本工具不能证明模型独立，也不能排除预训练暴露。它只核验文件绑定与合同
一致性，不证明学术真实性或概率校准。

None of these commands is a complete benchmark experiment or a Gate 3 pass.
A later experiment still requires the full schema 007 protocol, isolated
scoring, reruns, falsification, leakage review, and delivery gates.

这些命令都不等于完整 benchmark 实验或 Gate 3 通过。后续实验仍须满足
schema 007 的完整协议、隔离评分、复跑、反证、泄漏复核和交付门槛。
