# Graph Generation Tools / 图谱生成工具

English:
Future graph generation tools will produce graph nodes and edges from structured records.

Current tools:

- `build_hust_obc_candidate_graph_edges.py`: builds reviewed metadata-only JSONL edges from the HUST-OBC validation class staging table and source category staging table.
- `build_obimd_component_graph_edges.py`: builds reviewed metadata-only JSONL edges from OBIMD main-character, sub-character, and glyph-code-point staging tables.
- `build_evobc_evolution_graph_edges.py`: builds reviewed metadata-only JSONL edges from EVOBC evolution category era/source count summaries.
- `build_cambridge_hopkins_inscription_graph_edges.py`: builds reviewed metadata-only JSONL edges from Cambridge/Hopkins inscription crosswalk staging rows to source, download, period, classification-group, and external catalog-reference nodes.

简体中文：
未来图谱生成工具会从结构化记录生成图谱节点和边。

当前工具：

- `build_hust_obc_candidate_graph_edges.py`：从 HUST-OBC validation class 暂存表和 source category 暂存表生成仅限已复核元数据层面的 JSONL 图谱边。
- `build_obimd_component_graph_edges.py`：从 OBIMD main-character、sub-character 和 glyph-code-point 暂存表生成仅限已复核元数据层面的 JSONL 图谱边。
- `build_evobc_evolution_graph_edges.py`：从 EVOBC evolution category 的时代/来源计数摘要生成仅限已复核元数据层面的 JSONL 图谱边。
- `build_cambridge_hopkins_inscription_graph_edges.py`：从 Cambridge/Hopkins 卜辞 crosswalk staging 行生成仅限已复核 metadata 层面的 JSONL 图谱边，连接来源、下载记录、时期、分类组和外部著录号节点。
