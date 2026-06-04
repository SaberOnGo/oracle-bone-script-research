# Statistics And Derived Features / 统计与派生特征

English:
This directory will store generated occurrence, co-occurrence, topic, period, site, and similarity statistics.

Current generated statistics:

- `001_relationship-graph-edge-type-summary.csv`: edge counts by graph file, source ID, and edge type.
- `002_relationship-graph-node-degree-summary.csv`: in-degree, out-degree, source coverage, graph-file coverage, and edge-type counts by graph node.
- `003_ai-agent-relationship-graph-context-pack.json`: compact AI Agent entry context built from relationship graph statistics.
- `004_ai-agent-hust-obc-bucket-review-route-pack.json`: AI Agent route pack for the 16 HUST-OBC promotion-review buckets, linking each batch to manifests, graph files, source checks, and evidence gaps.
- `005_ai-agent-hust-obc-candidate-evidence-pack-request-queue.csv`: per-candidate queue for 1,588 HUST-OBC evidence-pack drafts, including required sections, route files, evidence gaps, and draft output paths under `doc/public/user_research/`.

简体中文：
本目录将保存生成的出现次数、共现、主题、时代、地点和相似度统计。

当前已生成统计：

- `001_relationship-graph-edge-type-summary.csv`：按图谱文件、来源 ID 和边类型汇总边数量。
- `002_relationship-graph-node-degree-summary.csv`：按图谱节点汇总入度、出度、来源覆盖、图谱文件覆盖和边类型计数。
- `003_ai-agent-relationship-graph-context-pack.json`：从关系图谱统计生成的紧凑 AI Agent 入口上下文包。
- `004_ai-agent-hust-obc-bucket-review-route-pack.json`：面向 16 个 HUST-OBC 提升复核 bucket 的 AI Agent 路由包，把每个批次连接到 manifest、图谱文件、来源核验和证据缺口。
- `005_ai-agent-hust-obc-candidate-evidence-pack-request-queue.csv`：面向 1,588 个 HUST-OBC 候选的逐候选 evidence-pack 草稿请求队列，包含必需章节、路由文件、证据缺口，以及 `doc/public/user_research/` 下的草稿输出路径。
