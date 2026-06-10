# Statistics And Derived Features / 统计与派生特征

English:
This directory will store generated occurrence, co-occurrence, topic, period, site, and similarity statistics.

Current generated statistics:

- `001_relationship-graph-edge-type-summary.csv`: edge counts by graph file, source ID, and edge type.
- `002_relationship-graph-node-degree-summary.csv`: in-degree, out-degree, source coverage, graph-file coverage, and edge-type counts by graph node.
- `003_ai-agent-relationship-graph-context-pack.json`: compact AI Agent entry context built from relationship graph statistics.
- `004_ai-agent-hust-obc-bucket-review-route-pack.json`: AI Agent route pack for the 16 HUST-OBC promotion-review buckets, linking each batch to manifests, graph files, source checks, and evidence gaps.
- `005_ai-agent-hust-obc-candidate-evidence-pack-request-queue.csv`: per-candidate queue for 1,588 HUST-OBC evidence-pack drafts, including required sections, route files, evidence gaps, and draft output paths under `doc/public/user_research/`.
- `006_ai-agent-public-domain-asset-context-pack.json`: AI Agent routing context for committed public-domain image assets, rights review, technical metadata, and safe visual preprocessing metadata.
- `007_source-coverage-summary.csv`: source-level coverage summary for download plans/logs, metadata profiles, committed public assets, relationship-graph derivatives, and HUST-OBC promotion-review candidates.
- `008_ai-agent-source-coverage-context-pack.json`: AI Agent source-routing context pack built from the coverage summary, preserving source, rights, access, graph, asset, and candidate-queue boundaries before evidence collection.
- `009_ai-agent-source-route-review-queue.csv`: per-source AI Agent review queue that prioritizes candidate, graph, public-asset, access-limited, metadata-profile, and download-log checks while keeping the work routing-only.
- `010_ai-agent-source-route-review-result-scaffold.csv`: empty per-source route-review result scaffold, reserving not-collected review sections for source register, route file, rights/risk, size/checksum, promotion decision, evidence gap, and next artifact checks.
- `011_ai-agent-source-route-review-results.csv`: first reviewed metadata-only source-route result for HUST-OBC, confirming route files, derived counts, rights/risk boundary, raw-package size boundary, and next cross-source review action without promoting raw assets or making decipherment claims.

简体中文：
本目录将保存生成的出现次数、共现、主题、时代、地点和相似度统计。

当前已生成统计：

- `001_relationship-graph-edge-type-summary.csv`：按图谱文件、来源 ID 和边类型汇总边数量。
- `002_relationship-graph-node-degree-summary.csv`：按图谱节点汇总入度、出度、来源覆盖、图谱文件覆盖和边类型计数。
- `003_ai-agent-relationship-graph-context-pack.json`：从关系图谱统计生成的紧凑 AI Agent 入口上下文包。
- `004_ai-agent-hust-obc-bucket-review-route-pack.json`：面向 16 个 HUST-OBC 提升复核 bucket 的 AI Agent 路由包，把每个批次连接到 manifest、图谱文件、来源核验和证据缺口。
- `005_ai-agent-hust-obc-candidate-evidence-pack-request-queue.csv`：面向 1,588 个 HUST-OBC 候选的逐候选 evidence-pack 草稿请求队列，包含必需章节、路由文件、证据缺口，以及 `doc/public/user_research/` 下的草稿输出路径。
- `006_ai-agent-public-domain-asset-context-pack.json`：面向已提交公共领域图像资产的 AI Agent 路由上下文，包含权利复核、技术 metadata 和安全视觉预处理 metadata。
- `007_source-coverage-summary.csv`：来源级覆盖统计，汇总下载计划/日志、metadata profile、已提交公共领域资产、关系图谱派生记录和 HUST-OBC promotion-review 候选覆盖。
- `008_ai-agent-source-coverage-context-pack.json`：从 coverage summary 生成的 AI Agent 来源路由上下文包，在收集证据前保持来源、权利、访问、图谱、资产和候选队列边界。
- `009_ai-agent-source-route-review-queue.csv`：逐来源 AI Agent 复核队列，优先安排候选、图谱、公共领域资产、访问受限、metadata profile 和下载日志检查，并保持仅限路由的工作边界。
- `010_ai-agent-source-route-review-result-scaffold.csv`：逐来源 route-review 空白结果骨架，为来源登记、route file、权利/风险、大小/checksum、提升决定、证据缺口和下一产物检查预留 not-collected 章节。
- `011_ai-agent-source-route-review-results.csv`：首条 HUST-OBC metadata-only 来源路由复核结果，确认 route files、派生计数、权利/风险边界、原始包尺寸边界和下一步交叉来源复核动作，不提升原始资产，也不提出释读结论。
