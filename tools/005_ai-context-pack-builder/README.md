# AI Context Pack Builder / AI 上下文包构建工具

English:
Future context-pack tools will gather source evidence for AI Agent reasoning.

Current tools:

- `build_relationship_graph_context_pack.py`: builds a compact, reviewed-metadata-only relationship graph coverage context pack from generated graph statistics.
- `build_hust_obc_bucket_review_route_pack.py`: builds an AI Agent route pack from HUST-OBC bucket summaries so each review batch points to its manifest, graph files, source checks, and evidence gaps before any draft hypothesis.
- `build_hust_obc_candidate_evidence_pack_request_queue.py`: builds one evidence-pack request row per HUST-OBC promotion candidate, including required evidence sections and draft output paths under `doc/public/user_research/`.
- `build_hust_obc_evidence_pack_draft.py`: builds one empty, schema-aligned evidence-pack draft from a single request queue row. It does not batch-create all drafts and does not make decipherment claims.
- `build_source_coverage_context_pack.py`: builds a source-level AI Agent routing context pack from the reviewed coverage summary so agents can choose the right register, download log, metadata profile, asset record, graph derivative, or candidate queue before collecting evidence.
- `build_source_route_review_queue.py`: builds one source-route review task per source from the source coverage context pack, preserving routing-only boundaries before any evidence collection or source promotion.
- `build_source_route_review_result_scaffold.py`: builds one empty source-route review result scaffold per route task, with all review sections marked not collected until an agent opens the cited route files.
- `build_source_route_review_results.py`: builds reviewed metadata-only source-route results for graph-derived HUST-OBC, EVOBC, and OBIMD routes from queue, scaffold, source register, metadata profile, download log, package manifest, candidate/evidence queues when applicable, and graph-edge counts.
- `build_graph_source_cross_review_queue.py`: builds three metadata-only cross-source review tasks from the reviewed HUST-OBC, EVOBC, and OBIMD source-route results, linking each first candidate or staging row to required route files and non-promotion cautions.
- `build_graph_source_cross_review_log_scaffold.py`: builds an empty log scaffold from the graph-source cross-review queue, reserving not-collected review sections for source registers, route files, counter-source lookups, rights/risk checks, evidence-pack status, and promotion decisions.
- `build_graph_source_cross_review_log_drafts.py`: builds three empty Markdown cross-source review log drafts from the scaffold, plus a draft manifest, with every evidence section left `not_collected`.
- `build_graph_source_cross_review_log_results.py`: builds metadata-only cross-source review log results from the draft manifest and local route files, confirming availability and staging refs without source promotion or decipherment claims.
- `build_graph_source_evidence_collection_task_queue.py`: builds a not-started evidence-collection task queue from the 015 results, splitting each reviewed route into source-register, download-log, package-manifest, metadata-profile, graph-edge, staging-row, counter-source, rights/risk, and review-log tasks.
- `build_graph_source_evidence_collection_note_drafts.py`: builds three empty evidence-collection note drafts for a selected 016 task section, plus a manifest, with all evidence still `not_collected`.
- `build_graph_source_evidence_collection_route_pack.py`: builds a graph-source evidence-collection route pack from the 017-025 note draft manifests, indexing all not-collected note drafts and route files without turning them into evidence or conclusions.
- `build_graph_source_evidence_collection_result_scaffold.py`: builds an empty graph-source evidence-collection result scaffold from the 026 route pack, preserving route links while every result section remains not collected.
- `build_graph_source_evidence_collection_review_queue.py`: builds a graph-source evidence-collection review queue from the 027 scaffold, routing future agents to the result row, note draft, route pack, manifest, and route files before any evidence is recorded.
- `build_graph_source_evidence_collection_review_route_summary.py`: builds a graph-source evidence-collection review route summary from the 028 queue, grouping review tasks by source and target evidence section while keeping the output routing-only.
- `build_graph_source_evidence_collection_assignment_plan.py`: builds a graph-source evidence-collection assignment plan from the 028 queue and 029 route summary, ordering 27 planned-not-assigned review tasks into 9 source-balanced waves without collecting evidence.
- `build_graph_source_evidence_collection_wave_handoff_scaffold.py`: builds the first `source_register` wave handoff scaffold from the 030 plan, listing the three handoff rows and route files while leaving evidence, owners, rights decisions, source promotion, and decipherment claims unset.
- `build_graph_source_evidence_collection_source_register_capture_scaffold.py`: builds an empty first-wave source-register evidence capture scaffold from 031, reserving fields for later source-register provenance capture without filling evidence values or making rights, promotion, or decipherment decisions.
- `build_graph_source_source_register_capture_review_checklist.py`: builds a not-started review checklist from 032 so agents must verify the capture row, source-register row, external reference, rights/risk fields, and non-promotion boundaries before recording evidence.
- `build_graph_source_download_log_wave_handoff_scaffold.py`: builds the second `download_log` wave handoff scaffold from the 030 plan, listing the three handoff rows and route files while leaving downloads, checksums, size/access conclusions, rights decisions, source promotion, and decipherment claims unset.
- `build_graph_source_download_log_capture_scaffold.py`: builds an empty download-log evidence capture scaffold from 034, reserving fields for later download status, URL, size, checksum, local temp path, and risk-note capture without filling evidence values or making rights, access, size, checksum, promotion, or decipherment decisions.
- `build_graph_source_download_log_capture_review_checklist.py`: builds a not-started review checklist from 035 so agents must verify the download log row, source/download IDs, URL, status, size, checksum, temp path, risk note, and non-inference boundaries before recording evidence.
- `build_graph_source_package_manifest_wave_handoff_scaffold.py`: builds the third `package_manifest` wave handoff scaffold from the 030 plan, listing the three handoff rows and route files while leaving file-size, checksum, storage-boundary, rights, promotion, and decipherment decisions unset.
- `build_graph_source_package_manifest_capture_scaffold.py`: builds an empty package-manifest evidence capture scaffold from 037, reserving fields for later package file, source package, file name, source URL, size, checksum, commit-policy, handling-strategy, rights, and review-status capture without filling evidence values or making file-size, checksum, storage, rights, promotion, or decipherment decisions.
- `build_graph_source_package_manifest_capture_review_checklist.py`: builds a not-started review checklist from 038 so agents must verify package manifest row, package/source package IDs, file metadata, size/download ID, checksum boundary, commit policy, handling strategy, rights/review status, and non-promotion boundaries before recording evidence.
- `build_hust_obimd_evobc_codepoint_crosswalk_context_pack.py`: builds a metadata-only AI Agent route context pack from the HUST/OBIMD/EVOBC codepoint crosswalk, summarizing match coverage, sample rows, source routes, and cautions without claiming oracle-character identity, readings, components, evolution chains, or decipherment conclusions.
- `build_hust_obimd_evobc_codepoint_crosswalk_review_queue.py`: builds a metadata-only review queue for the 134 HUST/OBIMD/EVOBC codepoint crosswalk rows that have OBIMD or EVOBC matches, prioritizing three-source matches before single-source matches while preserving no-identity and no-decipherment boundaries.
- `build_hust_obimd_evobc_codepoint_crosswalk_review_log_drafts.py`: builds 15 empty Markdown review-log drafts for the first-priority three-source codepoint matches, plus a manifest, with every evidence section left `not_collected` and no identity, reading, component, evolution-chain, or decipherment claim.

简体中文：
未来上下文包工具会为 AI Agent 推理收集来源证据。

当前工具：

- `build_relationship_graph_context_pack.py`：从已生成的图谱统计构建紧凑的、仅限已复核元数据层面的关系图谱覆盖范围上下文包。
- `build_hust_obc_bucket_review_route_pack.py`：从 HUST-OBC bucket summary 构建 AI Agent 路由包，让每个复核批次在生成草稿假说前先指向对应 manifest、图谱文件、来源核验和证据缺口。
- `build_hust_obc_candidate_evidence_pack_request_queue.py`：为每个 HUST-OBC promotion 候选生成一行 evidence-pack 请求，包含必需证据章节和 `doc/public/user_research/` 下的草稿输出路径。
- `build_hust_obc_evidence_pack_draft.py`：从单条 request queue 记录生成一个空白、符合 schema 的 evidence-pack 草稿。它不会批量创建全部草稿，也不会提出释读结论。
- `build_source_coverage_context_pack.py`：从已复核 coverage summary 构建来源级 AI Agent 路由上下文包，让 agent 在收集证据前先选择正确的来源登记、下载日志、metadata profile、资产记录、图谱派生或候选队列。
- `build_source_route_review_queue.py`：从来源覆盖上下文包为每个 source 生成一条 source-route 复核任务，在收集证据或提升来源派生记录前保持仅限路由的边界。
- `build_source_route_review_result_scaffold.py`：为每条来源路由任务生成一个空白 source-route 复核结果骨架，在 agent 打开被引用 route files 前，所有复核章节都保持 not collected。
- `build_source_route_review_results.py`：从 queue、scaffold、来源登记、metadata profile、下载日志、包 manifest、适用时的候选/evidence 队列和图谱边计数，为 graph-derived HUST-OBC、EVOBC、OBIMD 路由生成已复核 metadata-only 来源路由结果。
- `build_graph_source_cross_review_queue.py`：从已复核的 HUST-OBC、EVOBC、OBIMD source-route 结果生成三条 metadata-only 交叉来源复核任务，把每个首个候选或 staging 行连接到必需 route files 和禁止提升为结论的 caution。
- `build_graph_source_cross_review_log_scaffold.py`：从 graph-source cross-review queue 生成空白日志骨架，为来源登记、route files、反查来源、权利/风险检查、evidence-pack 状态和提升决定预留 not-collected 复核章节。
- `build_graph_source_cross_review_log_drafts.py`：从 scaffold 生成三份空白 Markdown 交叉来源复核日志草稿和一份草稿 manifest，所有证据章节保持 `not_collected`。
- `build_graph_source_cross_review_log_results.py`：从 draft manifest 和本地 route files 生成 metadata-only 交叉来源复核日志结果，只确认可用性和 staging 引用，不提升来源记录或提出释读结论。
- `build_graph_source_evidence_collection_task_queue.py`：从 015 结果生成未开始的证据收集任务队列，把每条已复核路由拆成来源登记、下载日志、package manifest、metadata profile、图谱边、staging 行、反查来源、权利/风险和复核日志任务。
- `build_graph_source_evidence_collection_note_drafts.py`：从 016 任务队列为指定任务章节生成三份空白证据收集记录草稿和一份 manifest，所有证据仍保持 `not_collected`。
- `build_graph_source_evidence_collection_route_pack.py`：从 017-025 证据收集记录草稿 manifest 构建 graph-source evidence-collection route pack，索引所有未收集草稿和 route files，但不把它们提升为证据或结论。
- `build_graph_source_evidence_collection_result_scaffold.py`：从 026 route pack 生成空白 graph-source evidence-collection result scaffold，保留路由链接，同时让所有结果章节保持未收集状态。
- `build_graph_source_evidence_collection_review_queue.py`：从 027 scaffold 生成 graph-source evidence-collection review queue，把后续 agent 路由到结果行、note draft、route pack、manifest 和 route files，在记录任何证据前保持准备阶段边界。
- `build_graph_source_evidence_collection_review_route_summary.py`：从 028 队列生成 graph-source evidence-collection review route summary，按来源和目标证据章节汇总复核任务，同时保持仅限路由的输出边界。
- `build_graph_source_evidence_collection_assignment_plan.py`：从 028 队列和 029 路由摘要生成 graph-source evidence-collection assignment plan，把 27 条 planned-not-assigned 复核任务排成 9 个来源均衡 wave，但不收集证据。
- `build_graph_source_evidence_collection_wave_handoff_scaffold.py`：从 030 计划生成第一波 `source_register` 交接脚手架，列出三条交接行和 route files，同时让证据、owner、权利决定、来源提升和释读声明保持未设置状态。
- `build_graph_source_evidence_collection_source_register_capture_scaffold.py`：从 031 生成空白的首波来源登记证据捕获骨架，为后续来源登记出处捕获预留字段，但不填入证据值，也不作权利、提升或释读决定。
- `build_graph_source_source_register_capture_review_checklist.py`：从 032 生成未开始的复核 checklist，要求 agent 在记录证据前核对 capture row、来源登记行、外部引用、权利/风险字段和禁止提升边界。
- `build_graph_source_download_log_wave_handoff_scaffold.py`：从 030 计划生成第二波 `download_log` 交接脚手架，列出三条交接行和 route files，同时让下载、checksum、大小/访问结论、权利决定、来源提升和释读声明保持未设置状态。
- `build_graph_source_download_log_capture_scaffold.py`：从 034 生成空白下载日志证据捕获骨架，为后续下载状态、URL、大小、checksum、本地临时路径和风险说明捕获预留字段，但不填入证据值，也不作权利、访问、大小、checksum、提升或释读决定。
- `build_graph_source_download_log_capture_review_checklist.py`：从 035 生成未开始的复核 checklist，要求 agent 在记录证据前核对下载日志行、source/download ID、URL、状态、大小、checksum、临时路径、风险说明和禁止推断边界。
- `build_graph_source_package_manifest_wave_handoff_scaffold.py`：从 030 计划生成第三波 `package_manifest` 交接脚手架，列出三条交接行和 route files，同时让文件大小、checksum、存储边界、权利、提升和释读决定保持未设置状态。
- `build_graph_source_package_manifest_capture_scaffold.py`：从 037 生成空白 package manifest 证据捕获骨架，为后续 package file、source package、文件名、来源 URL、大小、checksum、提交策略、处理策略、权利和复核状态捕获预留字段，但不填入证据值，也不作文件大小、checksum、存储、权利、提升或释读决定。
- `build_graph_source_package_manifest_capture_review_checklist.py`：从 038 生成未开始的复核 checklist，要求 agent 在记录证据前核对 package manifest 行、package/source package ID、文件 metadata、大小/download ID、checksum 边界、提交策略、处理策略、权利/复核状态和禁止提升边界。
- `build_hust_obimd_evobc_codepoint_crosswalk_context_pack.py`：从 HUST/OBIMD/EVOBC codepoint crosswalk 生成 metadata-only AI Agent 路由上下文包，汇总命中覆盖、样例行、来源路由和 caution，但不声明甲骨字身份、释读、构件、演化链或破译结论。
- `build_hust_obimd_evobc_codepoint_crosswalk_review_queue.py`：为 HUST/OBIMD/EVOBC codepoint crosswalk 中 134 条命中 OBIMD 或 EVOBC 的行生成 metadata-only 复核队列，优先三源命中，再处理单源命中，同时保持不确认身份、不作释读的边界。
- `build_hust_obimd_evobc_codepoint_crosswalk_review_log_drafts.py`：为第一优先级的 15 条三源 codepoint 命中生成空白 Markdown 复核日志草稿和 manifest；所有证据章节保持 `not_collected`，不提出身份、释读、构件、演化链或破译结论。
