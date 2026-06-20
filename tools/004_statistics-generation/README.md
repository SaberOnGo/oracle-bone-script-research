# Statistics Generation Tools / 统计生成工具

English:
Future statistics tools will generate occurrence, co-occurrence, period, topic, site, and grammar-position summaries.

Current tools:

English supplement:
- `build_collection_provenance_phase_gap_review_checklist.py` filters the collection-provenance rows from `192_core-corpus-phase-gap-action-queue.csv` and links them to collection staging, the collection-object source map, asset provenance indexes, and the Xiaoxuetang OBM access-boundary follow-up queue, producing `194_collection-provenance-phase-gap-review-checklist.csv`. It is a review entrance for downloaded, linked, and verified collection-provenance gaps only; it does not collect raw images, decide rights, confirm object identity, import corpus rows, or make decipherment claims.
- `build_research_source_phase_gap_review_checklist.py` filters the research-source rows from `192_core-corpus-phase-gap-action-queue.csv` and links them to `185_source-pipeline-missing-evidence-outcome-routes-assignment-checklist.csv`, producing `193_research-source-phase-gap-review-checklist.csv`. It gives later reviewers one compact entrance for the `downloaded`, `unpacked`, `extracted`, `cleaned`, and `verified` research-source phase gaps while preserving no-evidence-collection, no-rights-decision, no-source-promotion, no-corpus-import, and no-decipherment boundaries.
- `build_core_corpus_phase_gap_action_queue.py` expands `135_core-corpus-phase-coverage-matrix.csv` into `192_core-corpus-phase-gap-action-queue.csv`, one row per `missing` or `mixed_or_partial` core-corpus preprocessing phase. The queue preserves phase evidence paths, recommended next actions, and no-claim boundaries so AI Agents can open concrete gaps without treating candidates, route metadata, or drafts as reviewed scholarship.
- `build_source_coverage_statistics.py` now folds `188_object-local-material-coverage-audit.csv` into `007_source-coverage-summary.csv`, adding per-source object-local bundle, local review-image object, route-object, and partial-bundle counts. `build_source_coverage_context_pack.py` carries the same fields into the source coverage context pack so AI Agents can open source routes with both derivative-count and object-local-material coverage visible. These counts are routing infrastructure only; they do not confirm source promotion, rights decisions, identity, component, inscription, evolution, reading, or decipherment claims.
- `build_project_id_source_map_audit.py` generates `190_project-id-source-map-audit.csv` and `191_project-id-source-map-summary.json` from the six CSV maps under `project_registry/002_project-id-to-source-reference-map/`. It checks map-level row counts, canonical-path reachability, source-ID registration, external-reference fields, rights/review statuses, and next preprocessing entry points. This is a route-map integrity audit only: it does not confirm identity, reading, component, evolution, inscription, source promotion, or decipherment claims.
- On Windows, the audit uses long-path-aware path checks so deeply bucketed object-local asset routes are evaluated as repository paths instead of false missing-path issues.

Simplified Chinese supplement:
- `build_collection_provenance_phase_gap_review_checklist.py` 会从 `192_core-corpus-phase-gap-action-queue.csv` 过滤馆藏出处相关行，并连接馆藏 staging、collection-object 来源映射、资产出处索引和小学堂 OBM access-boundary 后续复核队列，生成 `194_collection-provenance-phase-gap-review-checklist.csv`。它只作为 downloaded、linked、verified 馆藏出处缺口的复核入口；不采集原始图片、不裁定权利、不确认对象身份、不导入语料，也不提出释读结论。
- `build_research_source_phase_gap_review_checklist.py` 会从 `192_core-corpus-phase-gap-action-queue.csv` 过滤研究来源相关行，并连接到 `185_source-pipeline-missing-evidence-outcome-routes-assignment-checklist.csv`，生成 `193_research-source-phase-gap-review-checklist.csv`。它为后续复核者提供一个紧凑入口，用于打开 `downloaded`、`unpacked`、`extracted`、`cleaned` 和 `verified` 这五类研究来源阶段缺口，同时保持不采集证据、不裁定权利、不提升来源、不导入语料和不提出释读结论的边界。
- `build_core_corpus_phase_gap_action_queue.py` 会把 `135_core-corpus-phase-coverage-matrix.csv` 中每个 `missing` 或 `mixed_or_partial` 的核心语料预处理阶段展开为 `192_core-corpus-phase-gap-action-queue.csv` 的一行。该队列保留阶段证据路径、建议下一步动作和无结论边界，使 AI Agent 可以打开具体缺口，但不得把候选、路线 metadata 或草稿当成已复核学术成果。
- `build_source_coverage_statistics.py` 现在会把 `188_object-local-material-coverage-audit.csv` 汇入 `007_source-coverage-summary.csv`，为每个来源增加对象内资料包、本地复核图像对象、路线对象和部分缺失包计数。`build_source_coverage_context_pack.py` 会把同样字段带入 source coverage context pack，使 AI Agent 在打开来源路线时同时看到派生计数与对象内资料覆盖情况。这些计数只属于路由基础设施；不确认来源提升、权利决定、身份、构件、卜辞、演化、释读或破译结论。
- `build_project_id_source_map_audit.py` 会从 `project_registry/002_project-id-to-source-reference-map/` 下的六个 CSV 映射表生成 `190_project-id-source-map-audit.csv` 和 `191_project-id-source-map-summary.json`。它检查映射表行数、规范路径是否可到达、来源 ID 是否已登记、外部引用字段、权利/复核状态，以及下一步预处理入口。该流程只做映射完整性审计，不确认身份、释读、构件、演化、卜辞、来源提升或释读结论。
- 在 Windows 上，该审计会使用支持长路径的路径检查，避免把深层 bucket/object-local 资产路由误判为缺失路径。

English supplement:
- `188_object-local-material-coverage-audit.csv` now includes `source_ids` extracted from object packets, including nested source indexes. `094_source-processing-pipeline-audit.csv` and `095_source-processing-pipeline-summary.json` use those IDs to expose source-level object-local material bundle, review-image object, route object, and partial-bundle counts. These are preprocessing navigation signals only: they do not promote candidate objects, decide rights, import corpus records, or make decipherment claims.

Simplified Chinese supplement:
- `188_object-local-material-coverage-audit.csv` 现在会从对象 packet（包括内嵌 source index）抽取 `source_ids`。`094_source-processing-pipeline-audit.csv` 和 `095_source-processing-pipeline-summary.json` 使用这些 ID 按来源显示对象内资料包、复核图像对象、路线对象和部分缺失包计数。这些只是预处理导航信号：不提升候选对象、不裁定权利、不导入语料，也不提出释读结论。

English supplement:
- `build_object_local_material_coverage_audit.py` generates `188_object-local-material-coverage-audit.csv` and `189_object-local-material-coverage-summary.json` across character, component, evolution, inscription-crosswalk, collection-object, source-object, and topic-candidate directories. It audits whether human-readable files, AI-readable packets/indexes, local review images, route galleries, and source material access indexes are co-located inside the same concrete `corpus` object directory, without creating parallel human-only directories or promoting candidate evidence into scholarship.
  The preprocessing status audit also counts 188/189, and the core corpus phase matrix exposes them as relationship-graph/statistics evidence paths so later review can verify object-local human/AI material coverage before semantic promotion.

Simplified Chinese supplement:
- `build_object_local_material_coverage_audit.py` 会跨甲骨字、构件、演化、卜辞 crosswalk、馆藏对象、来源对象和研究主题候选目录生成 `188_object-local-material-coverage-audit.csv` 与 `189_object-local-material-coverage-summary.json`。它检查人类可读文件、AI 可读 packet/index、本地复核图像、路线图和来源资料访问索引是否同处具体 `corpus` 对象目录内；不另建并行人类目录，也不把候选证据提升为学术结论。
  090 预处理状态审计会同步统计 188/189，135 核心语料阶段矩阵会把它们列为关系图/派生统计证据路径，便于后续复核在任何语义提升前先检查对象目录内的人类/AI 资料覆盖。

English supplement:
- `build_character_object_material_coverage_audit.py` generates `186_character-object-material-coverage-audit.csv` and `187_character-object-material-coverage-summary.json` from concrete character object directories. It audits whether each object directory contains co-located human-readable materials (`README.md`, `04_visual-gallery.md`) and AI-readable materials (`01_*packet.json`, `02_visual-source-index.csv`) without creating a parallel human-only directory, collecting new evidence, promoting records, or making decipherment claims.
  It counts object-local `.jpg`, `.jpeg`, and `.png` files under `03_visual-assets/` as committed review images when computing local material coverage.

Simplified Chinese supplement:
- `build_character_object_material_coverage_audit.py` 会从具体字对象目录生成 `186_character-object-material-coverage-audit.csv` 和 `187_character-object-material-coverage-summary.json`。它审计每个对象目录是否同时具备同目录的人类可读资料（`README.md`、`04_visual-gallery.md`）和 AI 可读资料（`01_*packet.json`、`02_visual-source-index.csv`），不创建并行的“人类看的目录”，不采集新证据，不提升记录，也不提出释读结论。
  计算对象内资料覆盖率时，它会把 `03_visual-assets/` 下的 `.jpg`、`.jpeg` 和 `.png` 都计为已提交本地复核图。

English supplement:
- `build_core_corpus_readiness_matrix.py`, `build_core_corpus_phase_coverage_matrix.py`, and `build_preprocessing_status_audit.py` now count `185_source-pipeline-missing-evidence-outcome-routes-assignment-checklist.csv` as the current missing-evidence outcome routes assignment checklist. This is a precheck and navigation surface only; it does not collect evidence, record reviewed outcomes, decide rights, promote sources, import corpus records, or make decipherment claims.

Simplified Chinese supplement:
- `build_core_corpus_readiness_matrix.py`、`build_core_corpus_phase_coverage_matrix.py` 和 `build_preprocessing_status_audit.py` 现在将 `185_source-pipeline-missing-evidence-outcome-routes-assignment-checklist.csv` 计入当前缺失证据 outcome routes assignment checklist。该文件只用于前置检查和导航；不采集证据、不记录已复核 outcome、不裁定权利、不提升来源、不导入语料，也不提出释读结论。

English supplement:
- `build_core_corpus_readiness_matrix.py`, `build_core_corpus_phase_coverage_matrix.py`, and `build_preprocessing_status_audit.py` now count `184_source-pipeline-missing-evidence-outcome-routes-assignment-plan.json` as the current missing-evidence outcome routes assignment plan. This is a planning and navigation surface only; it does not collect evidence, record reviewed outcomes, decide rights, promote sources, import corpus records, or make decipherment claims.

Simplified Chinese supplement:
- `build_core_corpus_readiness_matrix.py`、`build_core_corpus_phase_coverage_matrix.py` 和 `build_preprocessing_status_audit.py` 现在将 `184_source-pipeline-missing-evidence-outcome-routes-assignment-plan.json` 计入当前缺失证据 outcome routes assignment plan。该文件只用于计划和导航；不采集证据、不记录已复核 outcome、不裁定权利、不提升来源、不导入语料，也不提出释读结论。

English supplement:
- `build_core_corpus_readiness_matrix.py`, `build_core_corpus_phase_coverage_matrix.py`, and `build_preprocessing_status_audit.py` now count `183_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-outcome-checklist-outcome-routes-summary.json` as the current missing-evidence assignment outcome source handoff outcome checklist outcome routes summary. This is a routing and status aggregation surface only; it does not collect evidence, record reviewed outcomes, decide rights, promote sources, import corpus records, or make decipherment claims.

Simplified Chinese supplement:
- `build_core_corpus_readiness_matrix.py`、`build_core_corpus_phase_coverage_matrix.py` 和 `build_preprocessing_status_audit.py` 现在将 `183_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-outcome-checklist-outcome-routes-summary.json` 计入当前缺失证据 assignment outcome 来源交接 outcome checklist outcome routes summary。该文件只是路由和状态汇总表面；不采集证据、不记录已复核 outcome、不裁定权利、不提升来源、不导入语料，也不提出释读结论。

English supplement:
- `build_core_corpus_readiness_matrix.py`, `build_core_corpus_phase_coverage_matrix.py`, and `build_preprocessing_status_audit.py` now count `182_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-outcome-checklist-outcome-routes-checklist.csv` as the current missing-evidence assignment outcome source handoff outcome checklist outcome routes checklist. This is a precheck and navigation surface only; it does not collect evidence, record reviewed outcomes, decide rights, promote sources, import corpus records, or make decipherment claims.

Simplified Chinese supplement:
- `build_core_corpus_readiness_matrix.py`、`build_core_corpus_phase_coverage_matrix.py` 和 `build_preprocessing_status_audit.py` 现在将 `182_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-outcome-checklist-outcome-routes-checklist.csv` 计入当前缺失证据 assignment outcome 来源交接 outcome checklist outcome routes checklist。该文件只是前置检查与导航表面；不采集证据、不记录已复核 outcome、不裁定权利、不提升来源、不导入语料，也不提出释读结论。

English supplement:
- `build_core_corpus_readiness_matrix.py`, `build_core_corpus_phase_coverage_matrix.py`, and `build_preprocessing_status_audit.py` now count `181_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-outcome-checklist-outcome-routes.json` as the current missing-evidence assignment outcome source handoff outcome checklist outcome route summary outcome route summary. This is a routing and status aggregation surface only; it does not collect evidence, record reviewed outcomes, decide rights, promote sources, import corpus records, or make decipherment claims.

Simplified Chinese supplement:
- `build_core_corpus_readiness_matrix.py`、`build_core_corpus_phase_coverage_matrix.py` 和 `build_preprocessing_status_audit.py` 现在将 `181_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-outcome-checklist-outcome-routes.json` 计入当前缺失证据 assignment outcome 来源交接 outcome checklist outcome route summary outcome route summary。该文件只是路由和状态汇总表面；不采集证据、不记录已复核 outcome、不裁定权利、不提升来源、不导入语料，也不提出释读结论。

English supplement:
- `build_core_corpus_readiness_matrix.py`, `build_core_corpus_phase_coverage_matrix.py`, and `build_preprocessing_status_audit.py` now count `180_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-outcome-checklist-outcome-route-summary-outcome-scaffold.csv` as the current missing-evidence assignment outcome source handoff outcome checklist outcome route summary outcome scaffold. This is an empty human-gated outcome surface only; it does not collect evidence, record reviewed outcomes, decide rights, promote sources, import corpus records, or make decipherment claims.

Simplified Chinese supplement:
- `build_core_corpus_readiness_matrix.py`、`build_core_corpus_phase_coverage_matrix.py` 和 `build_preprocessing_status_audit.py` 现在将 `180_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-outcome-checklist-outcome-route-summary-outcome-scaffold.csv` 计入当前缺失证据 assignment outcome 来源交接 outcome checklist outcome route summary outcome scaffold。该文件只是空的人工门控 outcome 表面；不采集证据、不记录已复核 outcome、不裁定权利、不提升来源、不导入语料，也不提出释读结论。

English supplement:
- `build_core_corpus_readiness_matrix.py`, `build_core_corpus_phase_coverage_matrix.py`, and `build_preprocessing_status_audit.py` now count `179_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-outcome-checklist-outcome-route-summary.json` as the current missing-evidence assignment outcome source handoff outcome checklist outcome route summary. This is a routing and status aggregation surface only; it does not collect evidence, record reviewed outcomes, decide rights, promote sources, import corpus records, or make decipherment claims.

简体中文补充：
- `build_core_corpus_readiness_matrix.py`、`build_core_corpus_phase_coverage_matrix.py` 和 `build_preprocessing_status_audit.py` 现在将 `179_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-outcome-checklist-outcome-route-summary.json` 计入当前缺失证据 assignment outcome 来源交接 outcome checklist outcome route summary。该文件只是路由和状态汇总表面；不采集证据、不记录已复核 outcome、不裁定权利、不提升来源、不导入语料，也不提出释读结论。

English supplement:
- `build_core_corpus_readiness_matrix.py`, `build_core_corpus_phase_coverage_matrix.py`, and `build_preprocessing_status_audit.py` now count `178_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-outcome-checklist-outcome-scaffold.csv` as the current missing-evidence assignment outcome source handoff outcome checklist outcome scaffold. This is an empty human-gated outcome surface only; it does not collect evidence, record reviewed outcomes, decide rights, promote sources, import corpus records, or make decipherment claims.

简体中文补充：
- `build_core_corpus_readiness_matrix.py`、`build_core_corpus_phase_coverage_matrix.py` 和 `build_preprocessing_status_audit.py` 现在将 `178_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-outcome-checklist-outcome-scaffold.csv` 计入当前缺失证据 assignment outcome 来源交接 outcome checklist outcome scaffold。该文件只是空的人工门控 outcome 表面；不采集证据、不记录已复核 outcome、不裁定权利、不提升来源、不导入语料，也不提出释读结论。

English supplement:
- `build_core_corpus_readiness_matrix.py`, `build_core_corpus_phase_coverage_matrix.py`, and `build_preprocessing_status_audit.py` now count `177_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-outcome-checklist-route-summary.json` as the current missing-evidence assignment outcome source handoff outcome checklist route summary. This is a routing and status aggregation surface only; it does not collect evidence, record reviewed outcomes, decide rights, promote sources, import corpus records, or make decipherment claims.

简体中文补充：
- `build_core_corpus_readiness_matrix.py`、`build_core_corpus_phase_coverage_matrix.py` 和 `build_preprocessing_status_audit.py` 现在把 `177_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-outcome-checklist-route-summary.json` 计入当前缺失证据 assignment outcome 来源交接 outcome checklist route summary。该文件只作为路线和状态汇总入口；不采集证据、不记录已复核 outcome、不裁定权利、不提升来源、不导入语料，也不提出释读结论。
English supplement:
- `build_core_corpus_readiness_matrix.py`, `build_core_corpus_phase_coverage_matrix.py`, and `build_preprocessing_status_audit.py` now count `176_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-outcome-checklist.csv` as the current missing-evidence assignment outcome source handoff outcome precheck checklist. This is a human-gated preprocessing checklist only; it does not collect evidence, record reviewed outcomes, decide rights, promote sources, import corpus records, or make decipherment claims.

简体中文补充：
- `build_core_corpus_readiness_matrix.py`、`build_core_corpus_phase_coverage_matrix.py` 和 `build_preprocessing_status_audit.py` 现在把 `176_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-outcome-checklist.csv` 计入当前缺失证据 assignment outcome 来源交接 outcome 前置检查清单。该文件只是人工门控的预处理检查入口；不采集证据、不记录已复核 outcome、不裁定权利、不提升来源、不导入语料，也不提出释读结论。

English supplement:
- `build_core_corpus_readiness_matrix.py`, `build_core_corpus_phase_coverage_matrix.py`, and `build_preprocessing_status_audit.py` now count `175_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-outcome-route-summary.json` as the current missing-evidence assignment outcome source handoff outcome route summary. This is a routing and status aggregation surface only; it does not collect evidence, record reviewed outcomes, decide rights, promote sources, import corpus records, or make decipherment claims.

简体中文补充：
- `build_core_corpus_readiness_matrix.py`、`build_core_corpus_phase_coverage_matrix.py` 和 `build_preprocessing_status_audit.py` 现在把 `175_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-outcome-route-summary.json` 计入当前缺失证据 assignment outcome 来源交接 outcome route summary。该文件只作为路线和状态汇总入口；不采集证据、不记录已复核 outcome、不裁定权利、不提升来源、不导入语料，也不提出释读结论。

English supplement:
- `build_core_corpus_readiness_matrix.py`, `build_core_corpus_phase_coverage_matrix.py`, and `build_preprocessing_status_audit.py` now count `174_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-outcome-scaffold.csv` as the current missing-evidence assignment outcome source handoff outcome scaffold. This is an empty human-gated outcome surface only; it does not collect evidence, record reviewed outcomes, decide rights, promote sources, import corpus records, or make decipherment claims.

简体中文补充：
- `build_core_corpus_readiness_matrix.py`、`build_core_corpus_phase_coverage_matrix.py` 和 `build_preprocessing_status_audit.py` 现在把 `174_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-outcome-scaffold.csv` 计入当前缺失证据 assignment outcome 来源交接 outcome scaffold。该文件只是空的人工门控 outcome 表面；不采集证据、不记录已复核 outcome、不裁定权利、不提升来源、不导入语料，也不提出释读结论。

English supplement:
- `build_core_corpus_readiness_matrix.py`, `build_core_corpus_phase_coverage_matrix.py`, and `build_preprocessing_status_audit.py` now count `173_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-route-summary.json` as the current missing-evidence assignment outcome source handoff route summary. This is a routing and status aggregation surface only; it does not collect evidence, record reviewed outcomes, decide rights, promote sources, import corpus records, or make decipherment claims.

简体中文补充：
- `build_core_corpus_readiness_matrix.py`、`build_core_corpus_phase_coverage_matrix.py` 和 `build_preprocessing_status_audit.py` 现在把 `173_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-route-summary.json` 计入当前缺失证据 assignment outcome 来源交接路线汇总。该文件只作为路线和状态汇总入口；不采集证据、不记录已复核 outcome、不裁定权利、不提升来源、不导入语料，也不提出释读结论。

English supplement:
- `build_core_corpus_readiness_matrix.py`, `build_core_corpus_phase_coverage_matrix.py`, and `build_preprocessing_status_audit.py` now count `172_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-checklist.csv` as the current missing-evidence assignment outcome source handoff checklist. This is a precheck and navigation surface only; it does not collect evidence, record reviewed outcomes, decide rights, promote sources, import corpus records, or make decipherment claims.

简体中文补充：
- `build_core_corpus_readiness_matrix.py`、`build_core_corpus_phase_coverage_matrix.py` 和 `build_preprocessing_status_audit.py` 现在把 `172_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-checklist.csv` 计入当前缺失证据 assignment outcome 来源交接检查清单。该文件只作为前置检查和导航入口；不采集证据、不记录已复核 outcome、不裁定权利、不提升来源、不导入语料，也不提出释读结论。

English supplement:
- `build_core_corpus_readiness_matrix.py`, `build_core_corpus_phase_coverage_matrix.py`, and `build_preprocessing_status_audit.py` now count `169_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-checklist.csv` as the current missing-evidence assignment outcome source checklist. This is a human-gated preprocessing checklist only; it does not collect evidence, record reviewed outcomes, decide rights, promote sources, import corpus records, or make decipherment claims.

简体中文补充：
- `build_core_corpus_readiness_matrix.py`、`build_core_corpus_phase_coverage_matrix.py` 和 `build_preprocessing_status_audit.py` 现在把 `169_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-checklist.csv` 计入当前缺失证据 assignment outcome 来源清单。该文件只是人工门控预处理清单；不采集证据、不记录已复核 outcome、不裁定权利、不提升来源、不导入语料，也不提出释读结论。
English supplement:
- `build_source_pipeline_phase_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_summary.py`, `build_core_corpus_readiness_matrix.py`, `build_core_corpus_phase_coverage_matrix.py`, and `build_preprocessing_status_audit.py` now count `168_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-summary.csv` as the current missing-evidence assignment outcome source summary. This is source-level routing only; it does not collect evidence, record reviewed outcomes, decide rights, promote sources, import corpus records, or make decipherment claims.

简体中文补充：
- `build_source_pipeline_phase_action_missing_evidence_review_outcome_wave_handoff_assignment_outcome_source_summary.py`、`build_core_corpus_readiness_matrix.py`、`build_core_corpus_phase_coverage_matrix.py` 和 `build_preprocessing_status_audit.py` 现在把 `168_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-summary.csv` 计入当前缺失证据 assignment outcome 来源级汇总。该文件只做来源级路线汇总；不采集证据、不记录已复核 outcome、不裁定权利、不提升来源、不导入语料，也不提出释读结论。
English supplement:
- `build_core_corpus_readiness_matrix.py`, `build_core_corpus_phase_coverage_matrix.py`, and `build_preprocessing_status_audit.py` now count `167_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-route-summary.json` as the current missing-evidence assignment outcome route summary. This is routing and status aggregation only; it does not collect evidence, record reviewed outcomes, decide rights, promote sources, import corpus records, or make decipherment claims.

简体中文补充：
- `build_core_corpus_readiness_matrix.py`、`build_core_corpus_phase_coverage_matrix.py` 和 `build_preprocessing_status_audit.py` 现在把 `167_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-route-summary.json` 计入当前缺失证据 assignment outcome 路线汇总。该文件只做路线和状态汇总；不采集证据、不记录已复核 outcome、不裁定权利、不提升来源、不导入语料，也不提出释读结论。
English supplement:
- `build_core_corpus_readiness_matrix.py`, `build_core_corpus_phase_coverage_matrix.py`, and `build_preprocessing_status_audit.py` now count `166_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-scaffold.csv` as the current missing-evidence assignment outcome scaffold. This is an empty human-gated preprocessing surface only; it does not collect evidence, record reviewed outcomes, decide rights, promote sources, import corpus records, or make decipherment claims.

简体中文补充：
- `build_core_corpus_readiness_matrix.py`、`build_core_corpus_phase_coverage_matrix.py` 和 `build_preprocessing_status_audit.py` 现在把 `166_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-scaffold.csv` 计入当前缺失证据 assignment outcome scaffold。该文件只是空的人工门控预处理界面；不采集证据、不记录已复核 outcome、不裁定权利、不提升来源、不导入语料，也不提出释读结论。

English supplement:
- `build_core_corpus_readiness_matrix.py`, `build_core_corpus_phase_coverage_matrix.py`, and `build_preprocessing_status_audit.py` now count `165_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-checklist.csv` as the current missing-evidence outcome-review assignment precheck entry. This is preprocessing navigation only; it does not collect evidence, record reviewed outcomes, decide rights, promote sources, import corpus records, or make decipherment claims.

简体中文补充：
- `build_core_corpus_readiness_matrix.py`、`build_core_corpus_phase_coverage_matrix.py` 和 `build_preprocessing_status_audit.py` 现在把 `165_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-checklist.csv` 计入当前缺失证据 outcome 复核分派前置检查入口。该入口仅用于预处理导航；不采集证据、不记录已复核 outcome、不裁定权利、不提升来源、不导入语料，也不提出释读结论。

English supplement:
- `build_core_corpus_readiness_matrix.py`, `build_core_corpus_phase_coverage_matrix.py`, and `build_preprocessing_status_audit.py` now count `164_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-plan.json` as the current missing-evidence outcome-review handoff assignment entry. This is preprocessing navigation only; it does not collect evidence, record reviewed outcomes, decide rights, promote sources, import corpus records, or make decipherment claims.

简体中文补充：
- `build_core_corpus_readiness_matrix.py`、`build_core_corpus_phase_coverage_matrix.py` 和 `build_preprocessing_status_audit.py` 现在把 `164_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-plan.json` 计入当前缺失证据 outcome 复核交接分派入口。该入口仅用于预处理导航；不采集证据、不记录已复核 outcome、不裁定权利、不提升来源、不导入语料，也不提出释读结论。

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
- `build_source_processing_pipeline_audit.py`: generates one processing-pipeline row per registered source, covering download/access logs, checksum and size presence, field maps, package manifests, metadata profiles, derived records, graph edges, review routes, downstream phase-action counts, missing-evidence action counts, assignment checklist coverage, and next actions.
  The downstream counts are preprocessing navigation signals only; they do not record reviewed outcomes, rights decisions, source promotion, corpus import, or decipherment claims.
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
- `build_source_pipeline_phase_action_queue.py` generates `137_source-pipeline-phase-action-queue.csv` from the 136 source phase matrix. It expands missing or review-needed source phases into 62 human-review action rows without collecting evidence, deciding rights, promoting sources, importing corpus records, or making decipherment claims.
- `build_source_pipeline_phase_action_result_scaffold.py` generates `138_source-pipeline-phase-action-result-scaffold.csv` from the 137 action queue. It reserves reviewed-outcome fields for all 62 actions while keeping evidence, rights decisions, source promotion, corpus import, and decipherment claims empty.
- `build_source_pipeline_phase_action_route_summary.py` generates `139_source-pipeline-phase-action-route-summary.json` from the 138 result scaffold. It groups all 62 source-phase review routes by source, phase, and lane for navigation only, without recording reviewed outcomes.
- `build_source_pipeline_phase_action_source_summary.py` generates `140_source-pipeline-phase-action-source-summary.csv` from the 139 route summary. It compresses the 62 routes into 21 source-level review entry rows while keeping outcomes, rights decisions, promotion, imports, and decipherment claims empty.
- `build_source_pipeline_phase_action_file_checklist.py` generates `141_source-pipeline-phase-action-file-checklist.csv` from the 140 source summary. It expands each source-level entry into the 10 source register, manifest, field-map, download-log, and audit files that must be opened for review, without deciding any reviewed outcome.
- `build_source_pipeline_phase_action_evidence_presence_matrix.py` generates `142_source-pipeline-phase-action-evidence-presence-matrix.csv` from the 141 file checklist. It checks whether each review file currently contains source-matched rows, including large-source register matches through package-manifest package IDs, without collecting new evidence or deciding review outcomes.
- `build_source_pipeline_phase_action_evidence_gap_summary.py` generates `143_source-pipeline-phase-action-evidence-gap-summary.csv` from the 142 evidence presence matrix. It rolls up present and missing source-file evidence roles per source into a 21-row next-action summary, without completing human review or promoting any source.
- `build_source_pipeline_phase_action_missing_evidence_action_queue.py` generates `144_source-pipeline-phase-action-missing-evidence-action-queue.csv` from the 142 evidence presence matrix. It expands the 47 missing source-file evidence roles into human-review tasks, without collecting new evidence, deciding rights, promoting sources, importing corpus records, or making decipherment claims.
- `build_source_pipeline_phase_action_missing_evidence_result_scaffold.py` generates `145_source-pipeline-phase-action-missing-evidence-result-scaffold.csv` from the 144 missing-evidence action queue. It reserves empty reviewed-outcome fields for all 47 missing-evidence actions while keeping evidence collection, rights decisions, source promotion, corpus import, and decipherment claims unset.
- `build_source_pipeline_phase_action_missing_evidence_route_summary.py` generates `146_source-pipeline-phase-action-missing-evidence-route-summary.json` from the 145 result scaffold. It groups the 47 missing-evidence routes by source and missing evidence role for navigation only, without recording reviewed outcomes.

简体中文补充：
- `build_source_pipeline_phase_action_queue.py` 基于 136 来源阶段矩阵生成 `137_source-pipeline-phase-action-queue.csv`。它把缺失或待复核的来源阶段展开为 62 行人工复核动作；不采集新证据、不裁定权利、不提升来源、不导入语料，也不提出释读结论。
- `build_source_pipeline_phase_action_result_scaffold.py` 基于 137 动作队列生成 `138_source-pipeline-phase-action-result-scaffold.csv`。它为 62 条动作预留复核 outcome 字段，但证据、权利裁定、来源提升、语料导入和释读结论仍保持为空。
- `build_source_pipeline_phase_action_route_summary.py` 基于 138 结果脚手架生成 `139_source-pipeline-phase-action-route-summary.json`。它按来源、阶段和 lane 汇总 62 条来源阶段复核路线，仅作导航，不记录已复核 outcome。
- `build_source_pipeline_phase_action_source_summary.py` 基于 139 路线汇总生成 `140_source-pipeline-phase-action-source-summary.csv`。它把 62 条路线压缩成 21 行来源级复核入口，同时保持 outcome、权利裁定、来源提升、语料导入和释读结论为空。
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
English supplement:
- `build_source_pipeline_phase_action_missing_evidence_review_outcome_handoff_route_summary.py` generates `159_source-pipeline-phase-action-missing-evidence-review-outcome-handoff-route-summary.json` from the 158 outcome handoff checklist. It indexes the 18 planned outcome handoff checklist rows for routing only, without collecting evidence, recording reviewed outcomes, deciding rights, promoting sources, importing corpus records, or making decipherment claims.

简体中文补充：
- `build_source_pipeline_phase_action_missing_evidence_review_outcome_handoff_route_summary.py` 基于 158 outcome handoff checklist 生成 `159_source-pipeline-phase-action-missing-evidence-review-outcome-handoff-route-summary.json`。它只为 18 条计划中的 outcome handoff checklist 行建立路由索引，不采集证据、不记录已复核 outcome、不裁定权利、不提升来源、不导入语料，也不提出释读结论。
English supplement:
- `build_source_pipeline_phase_action_missing_evidence_review_outcome_assignment_plan.py` generates `160_source-pipeline-phase-action-missing-evidence-review-outcome-assignment-plan.json` from the 159 outcome handoff route summary. It groups the 18 planned source outcome-review routes into five gap-status waves for navigation only, without assigning reviewers, collecting evidence, recording reviewed outcomes, deciding rights, promoting sources, importing corpus records, or making decipherment claims.

简体中文补充：
- `build_source_pipeline_phase_action_missing_evidence_review_outcome_assignment_plan.py` 基于 159 outcome handoff route summary 生成 `160_source-pipeline-phase-action-missing-evidence-review-outcome-assignment-plan.json`。它只把 18 条计划中的来源 outcome-review 路由按五类 gap status 分组为复核 wave，用于导航；不分配复核者、不采集证据、不记录已复核 outcome、不裁定权利、不提升来源、不导入语料，也不提出释读结论。
English supplement:
- `build_source_pipeline_phase_action_missing_evidence_review_outcome_wave_handoff_scaffold.py` generates `161_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-scaffold.json` from the 160 assignment plan. It opens the planned outcome-review waves as handoff rows for navigation only, without assigning owners, collecting evidence, recording reviewed outcomes, deciding rights, promoting sources, importing corpus records, or making decipherment claims.

简体中文补充：
- `build_source_pipeline_phase_action_missing_evidence_review_outcome_wave_handoff_scaffold.py` 基于 160 assignment plan 生成 `161_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-scaffold.json`。它只把计划中的 outcome-review wave 展开为交接行用于导航；不分配 owner、不采集证据、不记录已复核 outcome、不裁定权利、不提升来源、不导入语料，也不提出释读结论。
English supplement:
- `build_core_corpus_readiness_matrix.py`, `build_core_corpus_phase_coverage_matrix.py`, and `build_preprocessing_status_audit.py` now count `162_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-checklist.csv` as the current missing-evidence outcome-review precheck entry. This remains preprocessing navigation only: no evidence collection, reviewed outcome, rights decision, source promotion, corpus import, or decipherment claim is recorded.

Simplified Chinese supplement:
- `build_core_corpus_readiness_matrix.py`、`build_core_corpus_phase_coverage_matrix.py` 和 `build_preprocessing_status_audit.py` 现在把 `162_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-checklist.csv` 计为当前 missing-evidence outcome-review 的 precheck 入口。该输出仍然只是预处理导航；不采集证据，不记录已复核 outcome，不裁定权利，不提升来源，不导入语料，也不提出释读结论。
English supplement:
- `build_core_corpus_readiness_matrix.py`, `build_core_corpus_phase_coverage_matrix.py`, and `build_preprocessing_status_audit.py` now count `163_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-route-summary.json` as the current missing-evidence outcome-review routing entry. This is still preprocessing navigation only and does not record evidence, outcomes, rights decisions, source promotion, corpus import, or decipherment claims.

Simplified Chinese supplement:
- `build_core_corpus_readiness_matrix.py`、`build_core_corpus_phase_coverage_matrix.py` 和 `build_preprocessing_status_audit.py` 现在把 `163_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-route-summary.json` 计为当前 missing-evidence outcome-review 的路由入口。该输出仍然只是预处理导航，不记录证据、outcome、权利裁定、来源提升、语料导入或释读结论。
English supplement:
- `build_core_corpus_readiness_matrix.py`, `build_core_corpus_phase_coverage_matrix.py`, and `build_preprocessing_status_audit.py` now count `170_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-route-pack.json` as the current assignment outcome source routing entry. This remains preprocessing navigation only: it does not collect evidence, record reviewed outcomes, decide rights, promote sources, import corpus records, or make decipherment claims.

Simplified Chinese supplement:
- `build_core_corpus_readiness_matrix.py`、`build_core_corpus_phase_coverage_matrix.py` 和 `build_preprocessing_status_audit.py` 现在把 `170_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-route-pack.json` 计为当前 assignment outcome source 的 route 入口。该入口仍然只用于预处理导航：不采集证据、不记录已复核 outcome、不裁定权利、不提升来源、不导入语料，也不提出释读结论。

English supplement:
- `build_core_corpus_readiness_matrix.py`, `build_core_corpus_phase_coverage_matrix.py`, and `build_preprocessing_status_audit.py` now count `171_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-scaffold.json` as the current assignment outcome source handoff entry. This remains preprocessing navigation only: it does not collect evidence, record reviewed outcomes, decide rights, promote sources, import corpus records, or make decipherment claims.

English supplement:
- `build_inscription_plate_crosswalk_phase_gap_review_checklist.py` generates `195_inscription-plate-crosswalk-phase-gap-review-checklist.csv` from the core corpus phase gap queue and current Cambridge/Hopkins inscription crosswalk staging, review queue, project inscription source map, and object-local candidate packet routes. The checklist is preprocessing navigation only: it does not collect new evidence, decide rights, promote sources, import formal inscription records, confirm inscription identity, or make decipherment claims.

Simplified Chinese supplement:
- `build_inscription_plate_crosswalk_phase_gap_review_checklist.py` 基于 core corpus phase gap queue 和当前 Cambridge/Hopkins inscription crosswalk staging、review queue、project inscription source map 以及对象目录内的 candidate packet 路线，生成 `195_inscription-plate-crosswalk-phase-gap-review-checklist.csv`。该清单只作为预处理导航入口：不采集新证据、不裁定权利、不提升来源、不导入正式卜辞记录、不确认卜辞身份，也不提出释读结论。

English supplement:
- `build_shape_component_evolution_verification_gap_review_checklist.py` generates `196_shape-component-evolution-verification-gap-review-checklist.csv` from the verified-missing codepoint, component, and evolution/correspondence rows in the core corpus phase gap queue. It links the rows to current HUST/OBIMD/EVOBC staging tables, project ID maps, graph edges, object-local candidate packets, and review routes while keeping every result candidate-only and unverified.

Simplified Chinese supplement:
- `build_shape_component_evolution_verification_gap_review_checklist.py` 基于 core corpus phase gap queue 中 codepoint、component 和 evolution/correspondence 的 verified missing 行，生成 `196_shape-component-evolution-verification-gap-review-checklist.csv`。该清单连接当前 HUST/OBIMD/EVOBC 暂存表、项目 ID 映射、图边、对象目录内 candidate packet 和复核路线；所有结果仍保持候选和未验证状态。

Simplified Chinese supplement:
- `build_core_corpus_readiness_matrix.py`、`build_core_corpus_phase_coverage_matrix.py` 和 `build_preprocessing_status_audit.py` 现在把 `171_source-pipeline-phase-action-missing-evidence-review-outcome-wave-handoff-assignment-outcome-source-handoff-scaffold.json` 计为当前 assignment outcome source 的 handoff 入口。该入口仍然只用于预处理导航：不采集证据、不记录已复核 outcome、不裁定权利、不提升来源、不导入语料，也不提出释读结论。
English supplement:
- `build_published_research_note_phase_gap_review_checklist.py` generates `197_published-research-note-phase-gap-review-checklist.csv` from the published_research_notes rows in the core corpus phase gap queue. It routes reviewers to `research/`, `doc/public/user_research/`, and the source register index while keeping user/AI drafts outside `research/` until human review rewrites them as source-marked scholarship notes.

Simplified Chinese supplement:
- `build_published_research_note_phase_gap_review_checklist.py` 基于 core corpus phase gap queue 中的 published_research_notes 行生成 `197_published-research-note-phase-gap-review-checklist.csv`。该清单把复核者路由到 `research/`、`doc/public/user_research/` 和来源登记索引，同时保持用户/AI 草稿不进入 `research/`，除非经过人工复核并改写为带来源标记的学术笔记。

English supplement:
- `build_character_candidate_phase_gap_review_checklist.py` generates `198_character-candidate-phase-gap-review-checklist.csv` from the high-priority oracle_characters and undeciphered_oracle_character_candidates rows in the core corpus phase gap queue. It routes reviewers to HUST-OBC promotion queues, undeciphered-candidate indexes, evidence-readiness rows, and character object-local material audits while keeping every row candidate-only and unpromoted.
- `build_core_corpus_phase_gap_review_index.py` generates `199_core-corpus-phase-gap-review-index.csv` by joining every row in `192_core-corpus-phase-gap-action-queue.csv` to exactly one specialized review checklist row from `193` through `198`. The index is a navigation and coverage surface only: it does not collect evidence, record reviewed outcomes, decide rights, promote sources or candidates, import formal corpus records, or make decipherment claims.
- `build_core_corpus_phase_gap_review_route_pack.py` generates `200_core-corpus-phase-gap-review-route-pack.json` from the `199` review index. It groups all 20 routed gaps by corpus area and specialized checklist family so later reviewers can open the aggregate index and the correct specialized row without recording any reviewed outcome.
- `build_core_corpus_phase_gap_review_handoff_scaffold.py` generates `201_core-corpus-phase-gap-review-handoff-scaffold.json` from the `200` route pack. It wraps all 20 routed gaps as precheck-only handoff rows with empty reviewed outcome fields, preserving the no evidence collection, no rights decision, no promotion, no corpus import, and no decipherment-claim boundaries.
- `build_core_corpus_phase_gap_review_handoff_checklist.py` generates `202_core-corpus-phase-gap-review-handoff-checklist.csv` from the `201` handoff scaffold. It gives each planned handoff one CSV precheck row for opening the scaffold, route pack, review index, specialized checklist row, and empty reviewed outcome fields before any later human-gated review.

Simplified Chinese supplement:
- `build_character_candidate_phase_gap_review_checklist.py` 基于 core corpus phase gap queue 中高优先级的 oracle_characters 与 undeciphered_oracle_character_candidates 行生成 `198_character-candidate-phase-gap-review-checklist.csv`。该清单把复核者路由到 HUST-OBC 提升复核队列、未释字候选索引、证据就绪清单和单字对象内资料覆盖审计，同时保持所有记录为候选、未提升状态。
- `build_core_corpus_phase_gap_review_index.py` 会把 `192_core-corpus-phase-gap-action-queue.csv` 的每一行连接到 `193` 至 `198` 中唯一的专项复核清单行，生成 `199_core-corpus-phase-gap-review-index.csv`。该索引只作为导航与覆盖率入口：不采集证据、不记录已复核 outcome、不裁定权利、不提升来源或候选、不导入正式语料，也不提出释读结论。
- `build_core_corpus_phase_gap_review_route_pack.py` 基于 `199` 复核索引生成 `200_core-corpus-phase-gap-review-route-pack.json`。它按 corpus area 和专项清单 family 汇总 20 条已路由缺口，使后续复核者可以打开汇总索引和正确的专项行，但不记录任何已复核 outcome。
- `build_core_corpus_phase_gap_review_handoff_scaffold.py` 基于 `200` route pack 生成 `201_core-corpus-phase-gap-review-handoff-scaffold.json`。它把 20 条已路由缺口包装为仅限 precheck 的 handoff 行，并保持 reviewed outcome 字段为空，同时保留不采集证据、不裁定权利、不提升、不导入语料和不提出释读结论的边界。
- `build_core_corpus_phase_gap_review_handoff_checklist.py` 基于 `201` handoff scaffold 生成 `202_core-corpus-phase-gap-review-handoff-checklist.csv`。它为每个计划中的 handoff 提供一行 CSV 前置检查入口，用于打开 scaffold、route pack、review index、专项复核清单行，并确认 reviewed outcome 字段仍为空，然后才进入后续人工门控复核。
