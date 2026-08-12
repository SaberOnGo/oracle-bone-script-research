# AI Benchmark Diagnostic Pilot / AI 基准诊断试点

## Purpose / 用途

English:

This tool freezes a small, explicit set of files from one real object dossier
and creates a schema-007-compatible HMAC-SHA-256 gold commitment. It establishes
diagnostic plumbing before any model run. It does not estimate probabilities,
run an Agent, authorize Gate 3, or claim a decipherment.

简体中文：

本工具从一个真实对象档案中冻结少量、显式列出的文件，并按 schema 007
规则建立 HMAC-SHA-256 gold commitment。它只建立模型运行前的诊断管道，
不估计概率、不运行 Agent、不授权 Gate 3，也不声称完成释读。

## Boundaries / 边界

- Every output is `diagnostic_only` and
  `pretraining_exposure_unknown`.
- Every output is `benchmark_pilot_not_scholarship`.
- No output contains a probability or model prediction.
- Private gold and all pilot outputs must remain in a Git-ignored path such as
  `.working/` or `doc/public/user_research/generated/`.
- The public commitment contains neither labels nor the HMAC key.
- Answer-bearing metadata fields and allowed-file paths are rejected.

- 所有输出均标为 `diagnostic_only` 和
  `pretraining_exposure_unknown`。
- 所有输出均标为 `benchmark_pilot_not_scholarship`。
- 输出不包含概率或模型预测。
- 私有 gold 和全部试点输出只能放入 `.working/` 或
  `doc/public/user_research/generated/` 等 Git 忽略路径。
- 公开 commitment 不包含标签或 HMAC 密钥。
- 工具拒绝带答案的 metadata 字段和文件路径。

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
separators. The key must contain at least 32 bytes. The public file records only
the binding identifiers and HMAC-SHA-256 commitment.

参与 commitment 的消息使用 UTF-8、键排序和紧凑分隔符。密钥至少包含
32 字节。公开文件只记录绑定标识与 HMAC-SHA-256 commitment。

```powershell
python tools/006_ai-benchmark-pilot/ai_benchmark_pilot.py seal `
  --private-gold .working/pilot/private-gold.json `
  --sealed-at 2026-08-12T00:00:00Z `
  --output .working/pilot/public-commitment.json
```

Neither command is a complete benchmark experiment or a Gate 3 pass. A later
experiment still requires the full schema 007 protocol, isolated scoring,
reruns, falsification, leakage review, and delivery gates.

两条命令都不等于完整 benchmark 实验或 Gate 3 通过。后续实验仍须满足
schema 007 的完整协议、隔离评分、复跑、反证、泄漏复核和交付门槛。
