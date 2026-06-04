# AI Context Pack Builder / AI 上下文包构建工具

English:
Future context-pack tools will gather source evidence for AI Agent reasoning.

Current tools:

- `build_relationship_graph_context_pack.py`: builds a compact, reviewed-metadata-only relationship graph coverage context pack from generated graph statistics.
- `build_hust_obc_bucket_review_route_pack.py`: builds an AI Agent route pack from HUST-OBC bucket summaries so each review batch points to its manifest, graph files, source checks, and evidence gaps before any draft hypothesis.
- `build_hust_obc_candidate_evidence_pack_request_queue.py`: builds one evidence-pack request row per HUST-OBC promotion candidate, including required evidence sections and draft output paths under `doc/public/user_research/`.

简体中文：
未来上下文包工具会为 AI Agent 推理收集来源证据。

当前工具：

- `build_relationship_graph_context_pack.py`：从已生成的图谱统计构建紧凑的、仅限已复核元数据层面的关系图谱覆盖范围上下文包。
- `build_hust_obc_bucket_review_route_pack.py`：从 HUST-OBC bucket summary 构建 AI Agent 路由包，让每个复核批次在生成草稿假说前先指向对应 manifest、图谱文件、来源核验和证据缺口。
- `build_hust_obc_candidate_evidence_pack_request_queue.py`：为每个 HUST-OBC promotion 候选生成一行 evidence-pack 请求，包含必需证据章节和 `doc/public/user_research/` 下的草稿输出路径。
