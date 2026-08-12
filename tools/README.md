# Tools / 工具

English:
This directory contains validation, corpus import, graph generation,
statistics, Git, and AI context-pack tools. These tools support human
research dossiers; they do not replace object-local review.

简体中文：
本目录保存校验、语料导入、图谱生成、统计、Git 与 AI 上下文包工具。
这些工具服务于人类研究档案，不能替代对象目录内的人工复核材料。

## Human Review Entry Order / 人工复核入口顺序

English:
Use repository tools in this order:

1. Open the related object-local dossier, review sheet, or source note first.
2. Check source provenance, rights status, risk note, and review status.
3. Run corpus import tools only to build staging or object-local materials.
4. Run graph generation only after opening the cited source rows.
5. Read statistics as review signals, not as research conclusions.
6. Build AI context-pack files only from reviewed routes and warnings.
7. Run validation before committing any docs, schemas, scripts, or outputs.

简体中文：
使用仓库工具时，按以下顺序处理：

1. 先打开相关对象目录内的档案、复核表或来源说明。
2. 核对来源追溯、权利状态、风险提示和复核状态。
3. 语料导入工具只用于生成 staging 或对象内资料。
4. 图谱生成前，必须先打开被引用的来源记录。
5. 统计只能作为复核信号，不能当作研究结论。
6. AI 上下文包只能汇集已标明路线和警示的材料。
7. 提交文档、schema、脚本或输出前，必须运行校验。

## Tool Areas / 工具分区

- `001_corpus-validation/` checks corpus and object-local records.
- `002_corpus-import/` prepares source package, staging index, and
  object-local materials.
- `003_graph-generation/` builds graph generation outputs such as
  character-source and cross-source route edges.
- `004_statistics-generation/` builds statistics for coverage, gaps, and
  review queues.
- `005_ai-context-pack-builder/` builds AI context-pack support files.
- [`006_ai-benchmark-pilot/`][benchmark-pilot] freezes real object files and
  seals ignored diagnostic gold without generating a probability or claim.
- [`validation/`][benchmark-validator] runs repository-wide skeleton, policy,
  evidence-pack, and blinded benchmark-experiment checks.
- `git/` checks commit-message rules before GitHub push.

## Benchmark v2 Validator / Benchmark v2 验证器

The benchmark validator discovers only
`*_benchmark-experiment-v2.json`. It first evaluates the complete public
[schema 007][schema-007], then applies cross-field gates. Those gates cover the
four case types, blind aliases, cutoffs, source and derivative snapshots,
pretraining eligibility, `unknown_or_other`, run independence, scoring,
human delivery, rights, and evidence-family requirements.

benchmark validator 只发现 `*_benchmark-experiment-v2.json`。它先执行完整
公开 [schema 007][schema-007]，再执行跨字段门禁。门禁覆盖四类案件、
盲别名、时间截点、来源与派生快照、预训练资格、`unknown_or_other`、
运行独立性、评分、人类交付、权利和证据家族要求。

Public validation without private gold:

```powershell
python tools/validation/validate_ai_agent_benchmark_experiments.py `
  --path doc/public/user_research/generated/ai-agent-benchmark-experiments
```

When no gold is supplied, a successful run prints
`METRICS_NOT_RECOMPUTED`. This is not metric verification or delivery
authorization.

未提供 gold 时，成功运行会输出 `METRICS_NOT_RECOMPUTED`。这不是指标复核，
也不是交付授权。

An ignored-local gold payload may be supplied only for diagnostic
recomputation. It cannot create the external scoring receipt required for
delivery. Delivery requires a scorer-derived clean holdout, a verified
external isolated scorer, exactly one scoring query, and retirement after that
score.

本地忽略 gold 只能用于诊断复算，不能形成交付所需的外部评分 receipt。交付
要求 scorer 派生的干净留出集、已复核外部隔离评分器、恰好一次评分请求，
并在该次评分后退役。

Same-model reruns count only as execution reruns. Candidate delivery also
requires a separately marked model-independent rerun, a complete bilingual
human delivery package, and at least two reviewed independent evidence
families.

同模型复跑只能计作执行复跑。候选交付还要求单独标记的模型独立复跑、
完整双语人类交付包，以及至少两个经复核的独立证据家族。

Source and evidence records must audit rights status, risk note, allowed
delivery form, large-source register reference, checksum, and dependency
status under the [rights policy] and [large-source policy]. The
[strategy] remains authoritative, and [schema 006][schema-006] remains the v1
draft contract.

来源与证据记录必须依照[权利政策][rights-policy]和
[大型来源政策][large-source-policy]审计权利状态、风险提示、允许交付形式、
大来源登记引用、checksum 和依赖状态。[战略][strategy]保持规范权威，
[schema 006][schema-006]继续作为 v1 草稿合同。

## Concrete Questions To Check / 具体待查问题

- Which object-local dossier or review sheet does this tool support?
- Which source provenance, checksum, manifest, or field map does it cite?
- Does the output stay inside an approved corpus, registry, or ignored area?
- Is the result a staging route, graph route, statistic, or review queue?
- Which human-readable file should be opened before trusting the output?
- Does any output need rights review, large-source registration, or cleanup?
- 哪个对象目录内档案或复核表需要这个工具支持？
- 它引用了哪条来源追溯、checksum、manifest 或字段映射？
- 输出是否留在允许的语料、登记表或已忽略临时区？
- 结果是 staging 路线、图边路线、统计，还是复核队列？
- 信任输出前，应先打开哪一个人类可读文件？
- 是否还有权利复核、大型来源登记或临时产物清理待完成？

## Research Boundary / 研究边界

English:
Tool outputs are preprocessing and review aids. A passed validator, generated
CSV, JSON route, graph edge, statistic, or AI context-pack is not scholarship,
not corpus import approval, not a rights decision, and not a decipherment
conclusion. Even a gate-valid `ai_adjudicated_candidate` remains an AI
candidate, not confirmed scholarship.
This is not a decipherment conclusion.

简体中文：
工具输出只是预处理和复核辅助。通过 validator、生成 CSV、JSON 路线、
图边、统计或 AI 上下文包，都不是学术结论，不是语料导入批准，不是
权利决定，也不是释读结论。即使通过门禁，`ai_adjudicated_candidate`
仍是 AI 候选，不是已确认学术结论。
这不是释读结论。

[benchmark-validator]: validation/validate_ai_agent_benchmark_experiments.py
[benchmark-pilot]: 006_ai-benchmark-pilot/
[strategy]: ../doc/project/005_ai-agent-research-assistant-design/
[schema-006]: ../schemas/006_ai-agent-evidence-pack-schema/
[schema-007]: ../schemas/007_ai-agent-benchmark-experiment-schema/
[rights-policy]: ../doc/project/002_source-rights-and-provenance-policy/
[large-source-policy]: ../doc/project/006_large-source-material-handling/
