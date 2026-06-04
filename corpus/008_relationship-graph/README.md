# Relationship Graph / 关系图谱

English:
This directory will store graph node and edge files connecting characters, components, inscriptions, sources, places, periods, topics, people, and hypotheses.

Current staged graph files:

- `005_hust-obc-candidate-graph-edges.jsonl`: reviewed metadata-only graph edges derived from HUST-OBC validation class/category metadata. These edges connect project candidate class IDs to HUST-OBC source category rows and OCR label candidate nodes. They are dataset provenance edges, not accepted paleographic readings or confirmed oracle-character identities.
- `006_obimd-component-graph-edges.jsonl`: reviewed metadata-only graph edges derived from OBIMD main-character, sub-character, and glyph-code-point mappings. These edges expose component/glyph relationships for retrieval and later review, but they are not formal component analyses, accepted readings, or committed image assets.
- `007_evobc-evolution-graph-edges.jsonl`: reviewed metadata-only graph edges derived from EVOBC category era/source count summaries. These edges make broad oracle-bone, bronze, seal, Spring and Autumn, Warring States, clerical, and source-token coverage searchable, but they are not accepted paleographic correspondences.

简体中文：
本目录将保存连接甲骨字、构件、卜辞、来源、地点、时代、主题、人物和假说的图谱节点与边。

当前已暂存的图谱文件：

- `005_hust-obc-candidate-graph-edges.jsonl`：从 HUST-OBC validation class/category 元数据派生的、仅限已复核元数据层面的图谱边。该文件连接本项目候选 class ID、HUST-OBC 来源 category 行和 OCR 标签候选节点。这些边是数据集来源关系，不是已接受的古文字释读，也不是已确认的甲骨文字身份关系。
- `006_obimd-component-graph-edges.jsonl`：从 OBIMD main-character、sub-character 和 glyph-code-point 映射派生的、仅限已复核元数据层面的图谱边。该文件把构件/子字与 glyph codepoint 关系暴露给检索和后续复核，但不是正式构件分析、已接受释读或已提交图像资产。
- `007_evobc-evolution-graph-edges.jsonl`：从 EVOBC category 的时代/来源计数摘要派生的、仅限已复核元数据层面的图谱边。该文件让甲骨、金文、篆书、春秋、战国、隶书和来源 token 覆盖情况可检索，但不是已接受的古文字对应关系。
