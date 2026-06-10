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
