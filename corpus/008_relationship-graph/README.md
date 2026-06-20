# Relationship Graph / 关系图谱

English:
This directory stores graph edge files connecting candidate characters, components, inscriptions, sources, periods, topics, and assets. The files are preprocessing and retrieval infrastructure only.

简体中文：
本目录保存连接候选单字、构件、卜辞、来源、时期、主题和资产的图边文件。这些文件只是预处理和检索基础设施。

## Current Graph Files / 当前图边文件

- `005_hust-obc-candidate-graph-edges.jsonl`: HUST-OBC validation class/category metadata edges.
- `006_obimd-component-graph-edges.jsonl`: OBIMD main-character, sub-character, and glyph-codepoint metadata edges.
- `007_evobc-evolution-graph-edges.jsonl`: EVOBC category, era, and source-token metadata edges.
- `008_cambridge-hopkins-inscription-crosswalk-graph-edges.jsonl`: Cambridge/Hopkins inscription crosswalk metadata edges.
- `009_character-asset-graph-edges.jsonl`: character candidate to local glyph-image asset route edges.
- `010_cross-source-id-graph-edges.jsonl`: HUST/OBIMD/EVOBC codepoint lookup-route edges.
- `011_component-asset-graph-edges.jsonl`: component candidate to local component-image asset route edges.
- `012_cambridge-hopkins-topic-candidate-graph-edges.jsonl`: Cambridge/Hopkins topic candidate to source, download, classification-group, inscription-crosswalk route, and unrouted crosswalk review-bucket edges.

## Boundary / 边界

English:
Graph edges are routing evidence and review scaffolding. They do not confirm readings, component assignments, inscription identities, topic assignments, grammar analyses, paleographic correspondences, transcriptions, or decipherment conclusions.

简体中文：
图边只是证据路由和复核脚手架。它们不确认读法、构件归属、卜辞身份、主题归属、语法分析、古文字对应、释文或破译结论。
