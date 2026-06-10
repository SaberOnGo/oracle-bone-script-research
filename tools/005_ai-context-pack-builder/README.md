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
- `build_graph_source_evidence_collection_note_drafts.py`: builds three empty source-register evidence-collection note drafts from the 016 task queue, plus a manifest, with all evidence still `not_collected`.

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
- `build_graph_source_evidence_collection_note_drafts.py`：从 016 任务队列生成三份空白来源登记证据收集记录草稿和一份 manifest，所有证据仍保持 `not_collected`。
