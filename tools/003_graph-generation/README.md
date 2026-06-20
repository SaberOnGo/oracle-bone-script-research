# Graph Generation Tools / 图谱生成工具

English:
Future graph generation tools will produce graph nodes and edges from structured records.

Current tools:

- `build_hust_obc_candidate_graph_edges.py`: builds reviewed metadata-only JSONL edges from the HUST-OBC validation class staging table and source category staging table.
- `build_obimd_component_graph_edges.py`: builds reviewed metadata-only JSONL edges from OBIMD main-character, sub-character, and glyph-code-point staging tables.
- `build_evobc_evolution_graph_edges.py`: builds reviewed metadata-only JSONL edges from EVOBC evolution category era/source count summaries.
- `build_cambridge_hopkins_inscription_graph_edges.py`: builds reviewed metadata-only JSONL edges from Cambridge/Hopkins inscription crosswalk staging rows to source, download, period, classification-group, and external catalog-reference nodes.
- `build_character_asset_graph_edges.py`: builds candidate JSONL edges from the asset source index so project-local character candidates can point to co-located local glyph image assets without making decipherment or component claims.
- `build_component_asset_graph_edges.py`: builds candidate JSONL edges from the asset source index so OBIMD component candidates can point to co-located local subcharacter image assets without confirming component forms or assignments.
- `build_cross_source_id_graph_edges.py`: builds candidate JSONL lookup-route edges from HUST/OBIMD/EVOBC codepoint crosswalk staging rows to HUST category, OBIMD candidate main-character, and EVOBC candidate evolution-category nodes without confirming identity, readings, components, or evolution chains.
- `build_character_asset_graph_edges.py`：从资产来源登记表生成候选 JSONL 图谱边，让本项目字形候选能指向同一具体字目录中的本地图像资产；不提出释读、字形身份或构件结论。
- `build_cross_source_id_graph_edges.py`：从 HUST/OBIMD/EVOBC codepoint crosswalk 暂存表生成候选 JSONL 查找路线边，连接 HUST 分类、OBIMD 候选主字和 EVOBC 候选演化分类节点；不确认同字关系、释读、构件或演化链。

简体中文：
未来图谱生成工具会从结构化记录生成图谱节点和边。

当前工具：

- `build_hust_obc_candidate_graph_edges.py`：从 HUST-OBC validation class 暂存表和 source category 暂存表生成仅限已复核元数据层面的 JSONL 图谱边。
- `build_obimd_component_graph_edges.py`：从 OBIMD main-character、sub-character 和 glyph-code-point 暂存表生成仅限已复核元数据层面的 JSONL 图谱边。
- `build_evobc_evolution_graph_edges.py`：从 EVOBC evolution category 的时代/来源计数摘要生成仅限已复核元数据层面的 JSONL 图谱边。
- `build_cambridge_hopkins_inscription_graph_edges.py`：从 Cambridge/Hopkins 卜辞 crosswalk staging 行生成仅限已复核 metadata 层面的 JSONL 图谱边，连接来源、下载记录、时期、分类组和外部著录号节点。
- `build_character_asset_graph_edges.py`：从资产来源登记表生成候选 JSONL 图谱边，让本项目字形候选能指向同一具体字目录中的本地图像资产；不提出释读、字形身份或构件结论。
- `build_cross_source_id_graph_edges.py`：从 HUST/OBIMD/EVOBC codepoint crosswalk 暂存表生成候选 JSONL 查找路线边，连接 HUST 分类、OBIMD 候选主字和 EVOBC 候选演化分类节点；不确认同字关系、释读、构件或演化链。
