# Statistics Generation Tools / 统计生成工具

English:
Future statistics tools will generate occurrence, co-occurrence, period, topic, site, and grammar-position summaries.

Current tools:

English supplement:
- `build_source_pipeline_gap_matrix.py` writes `132_ai-agent-source-pipeline-gap-matrix.csv`, a 21-row source-level gap matrix derived from the source register and 094 pipeline audit. It is a review navigation file only and keeps rights decisions, source promotion, corpus import, and decipherment claims unset.

简体中文补充：
- `build_source_pipeline_gap_matrix.py` 生成 21 行来源级缺口矩阵 `132_ai-agent-source-pipeline-gap-matrix.csv`，输入为来源登记表和 094 流水线审计。该文件只作为复核导航，不作权利裁定、不提升来源、不导入语料，也不提出释读结论。

English supplement:
- `build_source_engineering_first_wave_source_status.py` creates `122_ai-agent-source-engineering-first-wave-source-status.csv` by rolling up the 119 route results and 121 follow-up tasks per source. The output is a source-engineering navigation surface only and keeps rights, promotion, import, identity, component, evolution, and decipherment decisions pending review.

简体中文补充：
- `build_source_engineering_first_wave_source_status.py` 将 119 路线结果和 121 后续任务按来源汇总为 `122_ai-agent-source-engineering-first-wave-source-status.csv`。该输出只用于来源工程导航，继续保持权利、提升、导入、身份、构件、演化和释读决定待复核。

- `build_relationship_graph_statistics.py`: generates edge-type and node-degree CSV summaries from reviewed relationship graph JSONL files.
- `build_source_coverage_statistics.py`: generates a source-level coverage summary from reviewed source registers, download logs, metadata profiles, asset records, relationship-graph summaries, and the HUST-OBC promotion queue.
- `build_preprocessing_status_audit.py`: generates a repository-wide preprocessing status audit across source registration, download logs, large-source handling, candidate records, graph edges, assets, and review queues. The output is infrastructure status only, not a formal decipherment or identity claim.
- `build_data_quality_audit.py`: checks preprocessing tables and graph-edge files for required-field completeness, duplicate keys, source/download/large-source reference integrity, route-file availability, and candidate-boundary status fields. The output is an engineering-quality audit only.
- `build_source_processing_pipeline_audit.py`: generates one processing-pipeline row per registered source, covering download/access logs, checksum and size presence, field maps, package manifests, metadata profiles, derived records, graph edges, review routes, and next actions.
- `build_source_pipeline_gap_matrix.py`: generates `132_ai-agent-source-pipeline-gap-matrix.csv` from the source register and 094 pipeline audit, classifying per-source preprocessing gaps and review lanes while preserving no-new-rights-decision, not-promoted, not-imported, and no-decipherment-claim boundaries.
- `build_core_corpus_readiness_matrix.py`: generates a core-corpus readiness matrix and manual-review backlog summary across character, undeciphered, component, inscription, asset, bibliography, graph, and research-note entry points. The output is a preprocessing navigation aid only.
- `build_source_engineering_gap_queue.py`: generates 099 source-engineering gap review tasks from the current source pipeline and coverage audits, recording missing metadata profiles, field maps, package manifests, access-boundary follow-up, checksum review, and safe derivative decisions without promoting sources or scholarly claims.
- `build_source_engineering_execution_matrix.py`: generates a source-level execution matrix and summary from the 099 gap queue and 094 source pipeline audit, giving each registered source one metadata-only preprocessing work row without downloading raw material, importing corpus records, clearing rights, or promoting candidate scholarship.
- `build_source_engineering_first_wave_source_status.py`: aggregates the 119 first-wave review results and 121 follow-up queue into 122 source-level status rows, preserving metadata-only, no-new-rights-decision, not-promoted, not-imported, and no-decipherment-claim boundaries.

简体中文补充：
- `build_source_engineering_gap_queue.py`：从当前来源流水线和覆盖率审计生成 099 来源工程缺口复核队列，记录 metadata profile、field map、package manifest、访问边界、checksum 复核和安全派生记录决策等缺口；该输出不提升来源、不导入语料，也不构成学术结论。

简体中文：
未来统计工具会生成出现次数、共现、时代、主题、地点和语法位置统计。

当前工具：

- `build_relationship_graph_statistics.py`：从已复核的 relationship graph JSONL 文件生成边类型和节点度数 CSV 汇总。
- `build_source_coverage_statistics.py`：从已复核的来源登记、下载日志、metadata profile、资产记录、关系图谱汇总和 HUST-OBC promotion queue 生成来源级覆盖统计。
- `build_preprocessing_status_audit.py`：对来源登记、下载日志、大型来源处理、候选记录、图边、资产和复核队列生成仓库级预处理状态盘点；输出只表示基础设施状态，不构成正式释读或身份判断。
- `build_data_quality_audit.py`：检查预处理表和图边文件的必填字段完整性、重复键、来源/下载/大型来源引用完整性、路径可用性和候选边界状态字段；输出仅为资料工程质量审计。
- `build_source_processing_pipeline_audit.py`：为每个已登记来源生成处理流水线记录，覆盖下载/访问日志、checksum 与大小记录、字段映射、包清单、metadata profile、派生记录、图边、复核路线和下一步动作。
- `build_core_corpus_readiness_matrix.py`：围绕单字、未释字、构件、卜辞、资产、书目、关系图和研究笔记入口生成核心语料 readiness 矩阵与人工复核 backlog 摘要；输出仅用于预处理导航。

English supplement:
- build_source_engineering_execution_matrix.py also writes 100_ai-agent-source-engineering-execution-matrix.csv and 101_source-engineering-execution-summary.json as metadata-only source preprocessing work surfaces.

简体中文补充：
- build_source_engineering_execution_matrix.py 同时生成 100_ai-agent-source-engineering-execution-matrix.csv 与 101_source-engineering-execution-summary.json，作为 metadata-only 的来源预处理执行入口。

English supplement:
- `build_source_engineering_lane_summary.py` generates `106_ai-agent-source-engineering-lane-summary.csv` by grouping the 104 next-action checklist and 105 empty result scaffold into six source-engineering review lanes. The output is a metadata-only backlog summary; it does not complete review actions, collect evidence, decide rights, import corpus records, promote sources, or make decipherment claims.

简体中文补充：
- `build_source_engineering_lane_summary.py` 将 104 下一步行动清单和 105 空结果脚手架汇总为六个来源工程复核泳道，并生成 `106_ai-agent-source-engineering-lane-summary.csv`。该输出只是 metadata-only 的 backlog 汇总；它不完成复核动作、不采集证据、不裁定权利、不导入语料、不提升来源，也不提出释读结论。

English supplement:
- `build_source_pipeline_evidence_ledger.py` generates `134_ai-agent-source-pipeline-evidence-ledger.csv` from the 094 source-processing audit and 133 source-pipeline checklist. It records existing download, checksum, package-manifest, metadata-profile, candidate, and graph evidence counts per source, while keeping reviewed evidence paths and outcomes empty.

简体中文补充：
- `build_source_pipeline_evidence_ledger.py` 基于 094 来源处理流水线审计和 133 来源流水线清单生成 `134_ai-agent-source-pipeline-evidence-ledger.csv`。它按来源记录现有下载、checksum、包清单、metadata profile、候选记录和图边证据计数，同时保持已复核证据路径和 outcome 为空。

English supplement:
- `build_core_corpus_phase_coverage_matrix.py` generates `135_core-corpus-phase-coverage-matrix.csv` from the 090 preprocessing audit, 096 readiness matrix, and 134 source evidence ledger. It maps each core corpus area to preprocessing phase statuses and next evidence paths without importing records or making scholarship claims.
- `build_source_pipeline_phase_coverage_matrix.py` generates `136_source-pipeline-phase-coverage-matrix.csv` from the 134 source evidence ledger. It assigns every registered source phase statuses, missing/review-needed phases, and next review steps while preserving no-rights-decision, not-promoted, not-imported, and no-decipherment-claim boundaries.

简体中文补充：
- `build_core_corpus_phase_coverage_matrix.py` 基于 090 预处理审计、096 readiness 矩阵和 134 来源证据账本生成 `135_core-corpus-phase-coverage-matrix.csv`。它把每类核心语料映射到预处理阶段状态和下一步证据路径，不导入记录，也不提出学术结论。
- `build_source_pipeline_phase_coverage_matrix.py` 基于 134 来源证据账本生成 `136_source-pipeline-phase-coverage-matrix.csv`。它为每个已登记来源标注阶段状态、缺失/待复核阶段和下一步复核步骤，同时保持不作权利裁定、不提升来源、不导入语料和不提出释读结论的边界。

English supplement:
- `build_source_pipeline_phase_action_queue.py` generates `137_source-pipeline-phase-action-queue.csv` from the 136 source phase matrix. It expands missing or review-needed source phases into 77 human-review action rows without collecting evidence, deciding rights, promoting sources, importing corpus records, or making decipherment claims.
- `build_source_pipeline_phase_action_result_scaffold.py` generates `138_source-pipeline-phase-action-result-scaffold.csv` from the 137 action queue. It reserves reviewed-outcome fields for all 77 actions while keeping evidence, rights decisions, source promotion, corpus import, and decipherment claims empty.
- `build_source_pipeline_phase_action_route_summary.py` generates `139_source-pipeline-phase-action-route-summary.json` from the 138 result scaffold. It groups all 77 source-phase review routes by source, phase, and lane for navigation only, without recording reviewed outcomes.
- `build_source_pipeline_phase_action_source_summary.py` generates `140_source-pipeline-phase-action-source-summary.csv` from the 139 route summary. It compresses the 77 routes into 21 source-level review entry rows while keeping outcomes, rights decisions, promotion, imports, and decipherment claims empty.
- `build_source_pipeline_phase_action_file_checklist.py` generates `141_source-pipeline-phase-action-file-checklist.csv` from the 140 source summary. It expands each source-level entry into the 10 source register, manifest, field-map, download-log, and audit files that must be opened for review, without deciding any reviewed outcome.
- `build_source_pipeline_phase_action_evidence_presence_matrix.py` generates `142_source-pipeline-phase-action-evidence-presence-matrix.csv` from the 141 file checklist. It checks whether each review file currently contains source-matched rows, including large-source register matches through package-manifest package IDs, without collecting new evidence or deciding review outcomes.
- `build_source_pipeline_phase_action_evidence_gap_summary.py` generates `143_source-pipeline-phase-action-evidence-gap-summary.csv` from the 142 evidence presence matrix. It rolls up present and missing source-file evidence roles per source into a 21-row next-action summary, without completing human review or promoting any source.
- `build_source_pipeline_phase_action_missing_evidence_action_queue.py` generates `144_source-pipeline-phase-action-missing-evidence-action-queue.csv` from the 142 evidence presence matrix. It expands the 47 missing source-file evidence roles into human-review tasks, without collecting new evidence, deciding rights, promoting sources, importing corpus records, or making decipherment claims.
- `build_source_pipeline_phase_action_missing_evidence_result_scaffold.py` generates `145_source-pipeline-phase-action-missing-evidence-result-scaffold.csv` from the 144 missing-evidence action queue. It reserves empty reviewed-outcome fields for all 47 missing-evidence actions while keeping evidence collection, rights decisions, source promotion, corpus import, and decipherment claims unset.
- `build_source_pipeline_phase_action_missing_evidence_route_summary.py` generates `146_source-pipeline-phase-action-missing-evidence-route-summary.json` from the 145 result scaffold. It groups the 47 missing-evidence routes by source and missing evidence role for navigation only, without recording reviewed outcomes.

简体中文补充：
- `build_source_pipeline_phase_action_queue.py` 基于 136 来源阶段矩阵生成 `137_source-pipeline-phase-action-queue.csv`。它把缺失或待复核的来源阶段展开为 77 行人工复核动作；不采集新证据、不裁定权利、不提升来源、不导入语料，也不提出释读结论。
- `build_source_pipeline_phase_action_result_scaffold.py` 基于 137 动作队列生成 `138_source-pipeline-phase-action-result-scaffold.csv`。它为 77 条动作预留复核 outcome 字段，但证据、权利裁定、来源提升、语料导入和释读结论仍保持为空。
- `build_source_pipeline_phase_action_route_summary.py` 基于 138 结果脚手架生成 `139_source-pipeline-phase-action-route-summary.json`。它按来源、阶段和 lane 汇总 77 条来源阶段复核路线，仅作导航，不记录已复核 outcome。
- `build_source_pipeline_phase_action_source_summary.py` 基于 139 路线汇总生成 `140_source-pipeline-phase-action-source-summary.csv`。它把 77 条路线压缩成 21 行来源级复核入口，同时保持 outcome、权利裁定、来源提升、语料导入和释读结论为空。
- `build_source_pipeline_phase_action_file_checklist.py` 基于 140 来源汇总生成 `141_source-pipeline-phase-action-file-checklist.csv`。它把每个来源级入口展开为复核时需要打开的 10 个 source register、manifest、field-map、download-log 和 audit 文件；不裁定任何已复核 outcome。
- `build_source_pipeline_phase_action_evidence_presence_matrix.py` 基于 141 文件清单生成 `142_source-pipeline-phase-action-evidence-presence-matrix.csv`。它检查每个复核文件当前是否含有与来源匹配的行，其中 large-source register 通过 package manifest 的 package ID 间接匹配；不采集新证据，也不裁定复核 outcome。
- `build_source_pipeline_phase_action_evidence_gap_summary.py` 基于 142 evidence presence 矩阵生成 `143_source-pipeline-phase-action-evidence-gap-summary.csv`。它按来源把已有和缺失的 source-file evidence role 汇总成 21 行下一步动作摘要；不完成人工复核，也不提升任何来源。
- `build_source_pipeline_phase_action_missing_evidence_action_queue.py` 基于 142 evidence presence 矩阵生成 `144_source-pipeline-phase-action-missing-evidence-action-queue.csv`。它把 47 个缺失 source-file evidence role 展开为人工复核任务；不采集新证据、不裁定权利、不提升来源、不导入语料，也不提出释读结论。
- `build_source_pipeline_phase_action_missing_evidence_result_scaffold.py` 基于 144 缺失证据动作队列生成 `145_source-pipeline-phase-action-missing-evidence-result-scaffold.csv`。它为 47 个缺失证据动作预留空白的已复核 outcome 字段，同时保持证据采集、权利裁定、来源提升、语料导入和释读结论均未设置。
- `build_source_pipeline_phase_action_missing_evidence_route_summary.py` 基于 145 结果脚手架生成 `146_source-pipeline-phase-action-missing-evidence-route-summary.json`。它按来源和缺失证据角色汇总 47 条缺失证据路线，仅用于导航，不记录已复核 outcome。
- `build_source_pipeline_phase_action_missing_evidence_source_summary.py` generates `147_source-pipeline-phase-action-missing-evidence-source-summary.csv` from the 146 route summary. It compresses the 47 missing-evidence routes into 18 source-level review entries while keeping reviewed outcomes, rights decisions, source promotion, corpus import, and decipherment claims empty.
- `build_source_pipeline_phase_action_missing_evidence_review_drafts.py` generates `148_source-pipeline-phase-action-missing-evidence-review-draft-manifest.csv` and 18 Markdown drafts from the 147 source summary. The drafts are human-review work surfaces only and keep evidence, rights decisions, source promotion, corpus import, and decipherment claims empty.
- `build_source_pipeline_phase_action_missing_evidence_review_result_scaffold.py` generates `149_source-pipeline-phase-action-missing-evidence-result-scaffold.csv` from the 148 draft manifest. It provides empty source-level outcome fields for human reviewers while keeping evidence, rights decisions, source promotion, corpus import, identity, component, evolution, and decipherment claims unset.
- `build_source_pipeline_phase_action_missing_evidence_review_checklist.py` generates `150_source-pipeline-phase-action-missing-evidence-review-checklist.csv` from the 149 result scaffold. It turns each source-level missing-evidence scaffold into a human-gated checklist of route files and role-specific checks without collecting evidence or setting reviewed outcomes.
- `build_source_pipeline_phase_action_missing_evidence_review_route_pack.py` generates `151_source-pipeline-phase-action-missing-evidence-review-route-pack.json` from the 150 review checklist. It bundles checklist rows, route IDs, files to open, and status counts for navigation only, without collecting evidence or setting reviewed outcomes.
- `build_source_pipeline_phase_action_missing_evidence_review_handoff_scaffold.py` generates `152_source-pipeline-phase-action-missing-evidence-review-handoff-scaffold.json` from the 151 route pack. It wraps each route as a planned human handoff without assigning owners, collecting evidence, deciding rights, importing corpus rows, or making scholarly claims.
- `build_source_pipeline_phase_action_missing_evidence_review_handoff_checklist.py` generates `153_source-pipeline-phase-action-missing-evidence-review-handoff-checklist.csv` from the 152 handoff scaffold. It gives each planned handoff a precheck checklist for opening source files and confirming empty outcome fields before any later reviewed outcome is recorded.
- `build_source_pipeline_phase_action_missing_evidence_review_handoff_route_summary.py` generates `154_source-pipeline-phase-action-missing-evidence-review-handoff-route-summary.json` from the 153 handoff checklist. It summarizes the planned handoff routes by source and pipeline gap status for navigation only, without collecting evidence or recording outcomes.
- `build_source_pipeline_phase_action_missing_evidence_review_outcome_scaffold.py` generates `155_source-pipeline-phase-action-missing-evidence-review-outcome-scaffold.csv` from the 154 handoff route summary. It creates the human-fillable outcome surface for missing-evidence source review while keeping evidence, rights decisions, source promotion, corpus import, and decipherment claims unset.
- `build_source_pipeline_phase_action_missing_evidence_review_outcome_route_pack.py` generates `156_source-pipeline-phase-action-missing-evidence-review-outcome-route-pack.json` from the 155 outcome scaffold. It indexes the human-gated outcome rows for navigation only and does not collect evidence or record reviewed outcomes.

简体中文补充：
- `build_source_pipeline_phase_action_missing_evidence_source_summary.py` 基于 146 route summary 生成 `147_source-pipeline-phase-action-missing-evidence-source-summary.csv`。它把 47 条缺失证据 route 压缩成 18 行来源级复核入口，同时保持已复核 outcome、权利裁定、来源提升、语料导入和释读结论为空。
- `build_source_pipeline_phase_action_missing_evidence_review_drafts.py` 基于 147 来源汇总生成 `148_source-pipeline-phase-action-missing-evidence-review-draft-manifest.csv` 和 18 个 Markdown 草稿。这些草稿只作为人工复核工作界面，证据、权利裁定、来源提升、语料导入和释读结论仍保持为空。
- `build_source_pipeline_phase_action_missing_evidence_review_result_scaffold.py` 基于 148 草稿 manifest 生成 `149_source-pipeline-phase-action-missing-evidence-result-scaffold.csv`。它为人工复核预留空白的来源级 outcome 字段，同时保持证据、权利裁定、来源提升、语料导入、身份、构件、演化和释读结论均未设置。
- `build_source_pipeline_phase_action_missing_evidence_review_checklist.py` 基于 149 结果脚手架生成 `150_source-pipeline-phase-action-missing-evidence-review-checklist.csv`。它把每个来源级缺失证据脚手架转换为人工门控的路线文件和角色专项检查清单，不采集证据，也不填写已复核 outcome。
- `build_source_pipeline_phase_action_missing_evidence_review_route_pack.py` 基于 150 复核清单生成 `151_source-pipeline-phase-action-missing-evidence-review-route-pack.json`。它把清单行、route ID、待打开文件和状态计数打包为仅用于导航的 JSON，不采集证据，也不填写已复核 outcome。
- `build_source_pipeline_phase_action_missing_evidence_review_handoff_scaffold.py` 基于 151 route pack 生成 `152_source-pipeline-phase-action-missing-evidence-review-handoff-scaffold.json`。它把每条 route 包装成人工交接计划，不分配负责人、不采集证据、不裁定权利、不导入语料，也不提出学术结论。
- `build_source_pipeline_phase_action_missing_evidence_review_handoff_checklist.py` 基于 152 handoff scaffold 生成 `153_source-pipeline-phase-action-missing-evidence-review-handoff-checklist.csv`。它为每个计划中的交接项提供前置复核清单，用于打开来源文件并确认 outcome 字段仍为空，之后才可在后续已复核流程中记录结果。
- `build_source_pipeline_phase_action_missing_evidence_review_handoff_route_summary.py` 基于 153 handoff checklist 生成 `154_source-pipeline-phase-action-missing-evidence-review-handoff-route-summary.json`。它按来源和 pipeline gap status 汇总计划中的交接路线，仅用于导航，不采集证据，也不记录 outcome。
- `build_source_pipeline_phase_action_missing_evidence_review_outcome_scaffold.py` 基于 154 handoff route summary 生成 `155_source-pipeline-phase-action-missing-evidence-review-outcome-scaffold.csv`。它为 missing-evidence 来源复核建立人工可填写 outcome 表面，同时保持证据、权利决定、来源提升、语料导入和释读结论均未设置。
- `build_source_pipeline_phase_action_missing_evidence_review_outcome_route_pack.py` 基于 155 outcome scaffold 生成 `156_source-pipeline-phase-action-missing-evidence-review-outcome-route-pack.json`。它仅为人工闸口 outcome 行建立导航索引，不采集证据，也不记录已复核 outcome。
English supplement:
- `build_source_pipeline_phase_action_missing_evidence_review_outcome_handoff_scaffold.py` generates `157_source-pipeline-phase-action-missing-evidence-review-outcome-handoff-scaffold.json` from the 156 route pack. It wraps the 18 outcome routes as planned handoffs only and does not assign reviewers, collect evidence, decide rights, promote sources, import corpus rows, or make decipherment claims.
- `build_source_pipeline_phase_action_missing_evidence_review_outcome_handoff_checklist.py` generates `158_source-pipeline-phase-action-missing-evidence-review-outcome-handoff-checklist.csv` from the 157 handoff scaffold. It gives each planned handoff a precheck checklist for opening outcome route files and confirming empty reviewed-outcome fields before any later human-gated outcome is recorded.

简体中文补充：
- `build_source_pipeline_phase_action_missing_evidence_review_outcome_handoff_scaffold.py` 基于 156 route pack 生成 `157_source-pipeline-phase-action-missing-evidence-review-outcome-handoff-scaffold.json`。它只把 18 条 outcome route 包装为计划中的 handoff，不分配复核者、不采集证据、不裁定权利、不提升来源、不导入语料，也不提出释读结论。
- `build_source_pipeline_phase_action_missing_evidence_review_outcome_handoff_checklist.py` 基于 157 handoff scaffold 生成 `158_source-pipeline-phase-action-missing-evidence-review-outcome-handoff-checklist.csv`。它为每个计划中的 handoff 提供前置检查清单，用于打开 outcome route 文件并确认 reviewed-outcome 字段仍为空，之后才可在人工闸口流程中记录 outcome。
