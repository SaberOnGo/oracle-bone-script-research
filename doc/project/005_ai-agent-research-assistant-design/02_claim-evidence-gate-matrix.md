# Claim Evidence Gate Matrix / 命题证据门槛矩阵

## Status And Authority / 状态与权威

This document is a normative companion to the autonomous-candidate
strategy. It specifies which evidence is mandatory for each kind of
research proposition and when an AI adjudicator must abstain or withhold.

本文件是自主候选战略的规范配套。它规定不同研究命题必须具备哪些证据，
以及 AI 裁决器何时必须弃权或扣留。

It does not create a decipherment result, promote a corpus record, or replace
the object-local human dossier. A passing structure check is never evidence
of a true reading.

本文件不生成释读结果，不提升正式语料记录，也不替代对象目录内的人类档案。
结构校验通过从来不等于释读正确。

The matrix is effective with the [autonomous-candidate strategy][strategy].
The AI may apply it without a human specialist acting as a blocking reviewer,
but a released item remains an AI candidate and not confirmed scholarship.

本矩阵与[自主候选战略][strategy]同时生效。AI 可以自主应用本矩阵，不把
真人专家设为交付前置阻塞者；但交付内容仍是 AI 候选，不是已确认学术结论。

## Human-First Opening Order / 人类优先打开顺序

1. Open the object-local human dossier and the visible object, image, or
   authorized surrogate.
2. Open the source, catalog, plate, excavation, rights, and literature routes.
3. Record direct observations separately from source-reported labels.
4. Apply the claim row below before writing a hypothesis or probability.
5. Record every missing mandatory item as a concrete next-source question.
6. Open JSON, CSV, graph, or benchmark files only as support for the human
   record.

1. 先打开对象目录内人类档案，以及可见实物、图像或获准替代物。
2. 再打开来源、著录、图版、出土、权利和文献路线。
3. 把直接观察与来源报告的标签分开记录。
4. 在写假说或概率前，先应用下列命题行。
5. 每个缺失的必需项都写成具体的下一来源待查问题。
6. 最后才打开 JSON、CSV、图边或基准文件作为辅助。

## Evidence States And Independence / 证据状态与独立性

Use one state for every evidence item:

- `route_only`: an access or catalog route exists, but the item was not
  opened or verified.
- `source_reported`: a provider, catalog, paper, or database states it.
- `direct_checked`: the permitted object, image, text, or snapshot was opened
  and its locator and checksum were recorded.
- `independently_corroborated`: two evidence families agree after shared
  ancestry, labels, and derivative reuse are audited.
- `calibrated_support`: the proposition also passed the registered task
  calibration and leakage gates.

每个证据项使用一种状态：

- `route_only`：只有访问或著录路线，没有打开或核验资料本身。
- `source_reported`：由机构、著录、论文或数据库明确报告。
- `direct_checked`：已打开获准实物、图像、文本或快照，并记录定位与
  checksum。
- `independently_corroborated`：两个证据家族在审计共同祖先、标签和派生
  重用后仍相互支持。
- `calibrated_support`：命题还通过了预登记校准和泄漏门槛。

`source_reported` is not the same as `direct_checked`. Two files derived from
one ZIP, one database row, or one modern label are one evidence family, not
two independent witnesses.

`source_reported` 不等于 `direct_checked`。同一个 ZIP、同一数据库行或同一
现代标签派生出的两份文件仍属于一个证据家族，不能当作两个独立见证。

The following decisions are mandatory:

- `route_only` or missing mandatory evidence: `blocked`.
- Complete direct evidence without calibration: `candidate_route` or
  `uncalibrated_score`; never a release probability.
- Independent evidence with unresolved hard opposition: `withhold`.
- All applicable rows plus the strategy gates: `ai_adjudicated_candidate`.
- No row permits `confirmed_scholarship` or automatic corpus promotion.

下列决定是强制的：

- 必需证据为 `route_only` 或缺失：`blocked`。
- 直接证据齐全但尚未校准：`candidate_route` 或 `uncalibrated_score`，
  不能作为交付概率。
- 有独立证据但存在未解决的致命反证：`withhold`。
- 所有适用行和战略门槛均通过：`ai_adjudicated_candidate`。
- 任何一行都不能产生 `confirmed_scholarship` 或自动提升正式语料。

## Claim Rows / 命题行

### C1 Object Identity / 对象身份

**Question / 命题：** Is this the named bone, fragment, museum object, or
catalog item?

**Required / 必需：**

- stable institution or catalog identity;
- visible object, permitted image, or authorized surrogate;
- checksum-bound asset or snapshot route;
- source, rights, and derivative-ancestry record;
- an explicit alternative identity and a failed-identity check.

**阻断：** 只有网页入口、现代数据库 ID、文件名或来源自报时，身份命题
必须扣留；不能把 `source_reported` 写成已核实对象身份。

### C2 Direct Glyph Observation / 直接字形观察

**Question / 命题：** What is visibly present in the selected glyph region?

**Required / 必需：**

- a checksum-bound image or authorized visual surrogate;
- locator, crop or region route, dimensions, and image quality notes;
- neutral observations of strokes, placement, damage, cracks, and occlusion;
- an explicit distinction between visible marks and inferred components.

**阻断：** 没有可打开图像、区域定位或质量说明时，只能记为路线候选；
不能用 Unicode、今字或模型标签替代直接观察。

### C3 Same-Sign, Variant, Near-Form, Or Component /
### 同字、异体、近形或构件关系

**Question / 命题：** Do two visible records plausibly share a sign, variant,
near-form, or component relation?

**Required / 必需：**

- C1 and C2 for every compared object;
- at least two genuinely independent evidence families;
- damage-aware aligned comparisons and a near-form alternative set;
- source-file, not modern-label, support for each proposed link;
- a counterexample search and a rule for splitting the cluster.

**阻断：** 只有 codepoint、今字、目录同名或同一数据集的重复派生时，关系
只能是 `candidate_relation`，不得写成同字、异体或构件事实。

### C4 Inscription Occurrence And Context / 卜辞字例与上下文

**Question / 命题：** Where does the sign occur, and what context is actually
available?

**Required / 必需：**

- exact occurrence, plate or image locator, and catalog/source identifier;
- the full available inscription or an explicit bounded absence statement;
- neighbouring signs, line/order information, and text-quality status;
- period, batch, excavation, collection, or a concrete missing-source query;
- image/text provenance and a review state for OCR or transcription.

**阻断：** 只有字符 crosswalk、句组 ID、文件名或摘要时，不得声称已有卜辞
全文、图版、合集号、行序或出土地。

### C5 Reading Or Phonological Candidate / 读音或隶定候选

**Question / 命题：** Does a visible occurrence support a proposed reading or
phonological value?

**Required / 必需：**

- C4 with the complete available context and exact occurrence;
- neighbouring signs and grammar position;
- dated reading history, proposer, alternate readings, and disagreement;
- positive and negative evidence from independent source families;
- a preregistered falsification test and an explicit `unknown_or_other`.

**阻断：** 缺少逐行文本、读法史、提出者、反例或邻字时，AI 必须弃权；
模型语言先验不能补足这些缺口。

### C6 Semantic Or Grammatical Function / 语义或语法功能

**Question / 命题：** Does the sign have a proposed meaning or grammatical
function in this inscription?

**Required / 必需：**

- C5, not merely a shape or codepoint match;
- complete available sentence context and comparable occurrences;
- grammar analysis tied to a source text, not an OCR guess alone;
- archaeological, period, or catalog context when the claim depends on it;
- competing meanings, disconfirming examples, and a reopening condition.

**阻断：** 任一必需上下文或争议史缺失时，不能交付语义或语法概率；只能
交付资料路线或明确弃权。

### C7 Diachronic Correspondence / 历时字形对应

**Question / 命题：** Does a later bronze, seal, or modern form correspond to
the earlier record?

**Required / 必需：**

- period-provenanced forms on both sides;
- a bridge argument beyond visual resemblance;
- source and edition history for every form;
- near-form and counterexample comparisons;
- explicit separation of dataset co-membership from paleographic proof.

**阻断：** EvoBC、金文、小篆或 Unicode 同码路线本身只能产生对应候选，
不能自动产生演化事实、读音或意义。

### C8 Complete Proposition And User Delivery /
### 完整命题与用户交付

**Question / 命题：** Is the complete proposition ready for the user-facing
candidate channel?

**Required / 必需：**

- every applicable row C1--C7 is non-blocked;
- two reviewed independent evidence families and complete provenance;
- no hard counterexample, rights block, or leakage;
- calibrated task probability with a registered lower-bound threshold;
- clean in-domain holdout, model-independent rerun, locked adjudication,
  external one-shot scoring, and retired holdout;
- bilingual human delivery dossier with alternatives and abstention.

**阻断：** 任一条件缺失，`delivery_status` 必须是 `withheld` 或
`abstain`; 不得写 `ai_adjudicated_candidate`。即使全部通过，也只能称
AI 候选，不是已确认释读或学界共识。

## Recording Contract / 记录合同

Every human dossier records, for each applicable claim:

- `claim_id` (`C1`--`C8`);
- evidence item IDs and their state;
- independent family IDs and shared-ancestor notes;
- mandatory blockers, impact, and one concrete next-source question;
- alternative proposition, falsification condition, and abstention reason;
- AI delivery state and the linked versioned adjudication record.

每份人类档案都要逐项记录适用命题：

- `claim_id`（`C1`--`C8`）；
- 证据项 ID 及其状态；
- 独立证据家族 ID 和共同祖先说明；
- 必需阻断项、影响和一个具体下一来源待查问题；
- 替代命题、证伪条件和弃权原因；
- AI 交付状态及其版本化裁决记录链接。

For v1 evidence packs, map these rows to the existing sections rather than
adding a second hidden schema. `full_inscription_context`,
`neighboring_characters`, `component_breakdown_and_variant_notes`,
`excavation_period_and_catalog_provenance`, `supporting_evidence`, and
`opposing_evidence` must remain human-readable evidence sections. A v1
`status` or a schema `PASS` cannot override this matrix.

对于 v1 evidence pack，应把这些命题行映射到现有章节，不要再建立隐藏的
第二套 schema。`full_inscription_context`、`neighboring_characters`、
`component_breakdown_and_variant_notes`、
`excavation_period_and_catalog_provenance`、`supporting_evidence` 和
`opposing_evidence` 必须保持为人类可读证据章节。v1 `status` 或 schema
`PASS` 都不能覆盖本矩阵。

## Reopening And Withdrawal / 重开与撤回

Reopen the claim when a source identity changes, a right is withdrawn, a new
near-form appears, a counterexample is found, a dependency is discovered, or
the calibration domain changes. Preserve the earlier dossier and receipt;
append a new decision instead of editing history.

当来源身份变化、权利撤回、出现新的近形、发现反例、发现共同依赖，或校准
适用域变化时，必须重开命题。保留旧档案和回执；追加新决定，不改写历史。

The final labels remain `candidate`, `withheld`, `abstained`, `withdrawn`, or
`confirmed_scholarship` only when an external scholarly process supports that
separate status. AI autonomy removes a human delivery prerequisite; it does
not remove evidence, provenance, or falsification requirements.

最终标签仍只能是 `candidate`、`withheld`、`abstained` 或 `withdrawn`；
`confirmed_scholarship` 只能在独立的外部学术过程支持时使用。AI 自主裁决
取消了真人交付前置条件，但没有取消证据、出处和证伪要求。

[strategy]: README.md
