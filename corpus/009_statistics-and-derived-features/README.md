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
- `011_ai-agent-source-route-review-results.csv`: reviewed metadata-only source-route results for graph-derived HUST-OBC, EVOBC, and OBIMD routes, confirming route files, derived counts, rights/risk boundaries, size/commit-policy boundaries, and next cross-source review actions without promoting raw assets, dataset labels, graph edges, or staging rows into scholarship.
- `012_ai-agent-graph-source-cross-review-queue.csv`: three metadata-only cross-source review tasks for the first HUST-OBC, EVOBC, and OBIMD graph-derived routes, pointing agents to the required registers, staging rows, graph files, and review logs before any evidence-pack draft or source promotion.
- `013_ai-agent-graph-source-cross-review-log-scaffold.csv`: empty log scaffold for the 012 cross-source review tasks, keeping source register, download log, package manifest, metadata profile, graph-edge, staging-row, counter-source, rights/risk, review-log, evidence-pack, and promotion-decision sections uncollected until source-marked review.
- `014_ai-agent-graph-source-cross-review-log-draft-manifest.csv`: manifest for three empty Markdown cross-source review log drafts under `doc/public/user_research/002_cross-source-review-queues/`, keeping every evidence section `not_collected` and every promotion decision `not_decided`.
- `015_ai-agent-graph-source-cross-review-log-results.csv`: metadata-only cross-source review log results for the three draft logs, confirming local route-file availability, registered counter sources, metadata/profile/download/package rows, graph-edge route counts, and staging-row refs without promoting any dataset labels, graph edges, component assignments, evolution chains, or decipherment conclusions.
- `016_ai-agent-graph-source-evidence-collection-task-queue.csv`: per-source, per-section evidence-collection task queue derived from the 015 results, routing future agents to source register, download log, package manifest, metadata profile, graph-edge, staging-row, counter-source, rights/risk, and review-log checks while keeping all evidence uncollected.
- `017_ai-agent-graph-source-evidence-collection-note-draft-manifest.csv`: manifest for three empty source-register evidence-collection note drafts under `doc/public/user_research/003_evidence-collection-tasks/`, linked to 016 task rows and kept `not_collected`, `not_promoted`, and outside scholarship.
- `018_ai-agent-graph-source-download-log-note-draft-manifest.csv`: manifest for three empty download-log evidence-collection note drafts under `doc/public/user_research/003_evidence-collection-tasks/`, routing agents to the large-source download log without recording collected evidence, checksums, rights decisions, or source promotion.
- `019_ai-agent-graph-source-package-manifest-note-draft-manifest.csv`: manifest for three empty package-manifest evidence-collection note drafts under `doc/public/user_research/003_evidence-collection-tasks/`, routing agents to source package file manifests without recording file-size conclusions, checksum review, rights decisions, or source promotion.
- `020_ai-agent-graph-source-metadata-profile-note-draft-manifest.csv`: manifest for three empty metadata-profile evidence-collection note drafts under `doc/public/user_research/003_evidence-collection-tasks/`, routing agents to downloaded metadata profile rows without recording collected metrics, rights decisions, source promotion, or decipherment conclusions.
- `021_ai-agent-graph-source-graph-edges-note-draft-manifest.csv`: manifest for three empty graph-edge evidence-collection note drafts under `doc/public/user_research/003_evidence-collection-tasks/`, routing agents to relationship graph JSONL files without recording collected edge evidence, component assignments, evolution-chain claims, or decipherment conclusions.

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
- `011_ai-agent-source-route-review-results.csv`：面向 graph-derived HUST-OBC、EVOBC、OBIMD 路由的 metadata-only 来源路由复核结果，确认 route files、派生计数、权利/风险边界、尺寸/提交策略边界和下一步交叉来源复核动作，不把原始资产、数据集标签、图谱边或 staging rows 提升为学术结论。
- `012_ai-agent-graph-source-cross-review-queue.csv`：面向首个 HUST-OBC、EVOBC、OBIMD graph-derived 路由的三条 metadata-only 交叉来源复核任务，指向必需登记表、staging 行、图谱文件和复核日志，在任何 evidence-pack 草稿或来源提升前保持准备阶段边界。
- `013_ai-agent-graph-source-cross-review-log-scaffold.csv`：面向 012 交叉来源复核任务的空白日志骨架，把来源登记、下载日志、包 manifest、metadata profile、图谱边、staging 行、反查来源、权利/风险、复核日志、evidence-pack 和提升决定章节保持为未收集状态，等待带来源标记的复核。
- `014_ai-agent-graph-source-cross-review-log-draft-manifest.csv`：记录 `doc/public/user_research/002_cross-source-review-queues/` 下三份空白 Markdown 交叉来源复核日志草稿，所有证据章节保持 `not_collected`，所有提升决定保持 `not_decided`。
- `015_ai-agent-graph-source-cross-review-log-results.csv`：面向三份草稿日志的 metadata-only 交叉来源复核日志结果，确认本地 route file 可用性、已登记反查来源、metadata/profile/download/package 行、图谱边路由计数和 staging row 引用，但不提升任何数据集标签、图谱边、构件判定、演化链或释读结论。
- `016_ai-agent-graph-source-evidence-collection-task-queue.csv`：从 015 结果派生的逐来源、逐章节证据收集任务队列，把后续 agent 路由到来源登记、下载日志、package manifest、metadata profile、图谱边、staging 行、反查来源、权利/风险和复核日志检查，同时保持所有证据为未收集状态。
- `017_ai-agent-graph-source-evidence-collection-note-draft-manifest.csv`：记录 `doc/public/user_research/003_evidence-collection-tasks/` 下三份空白来源登记证据收集记录草稿，与 016 任务行相连，并保持 `not_collected`、`not_promoted`、非学术结论边界。
- `018_ai-agent-graph-source-download-log-note-draft-manifest.csv`：记录 `doc/public/user_research/003_evidence-collection-tasks/` 下三份空白下载日志证据收集记录草稿，把 agent 路由到大型来源下载日志，但不记录已收集证据、checksum、权利决定或来源提升。
- `019_ai-agent-graph-source-package-manifest-note-draft-manifest.csv`：记录 `doc/public/user_research/003_evidence-collection-tasks/` 下三份空白 package manifest 证据收集记录草稿，把 agent 路由到来源包文件 manifest，但不记录文件大小结论、checksum 复核、权利决定或来源提升。
- `020_ai-agent-graph-source-metadata-profile-note-draft-manifest.csv`：记录 `doc/public/user_research/003_evidence-collection-tasks/` 下三份空白 metadata profile 证据收集记录草稿，把 agent 路由到已下载 metadata profile 行，但不记录已收集指标、权利决定、来源提升或释读结论。
- `021_ai-agent-graph-source-graph-edges-note-draft-manifest.csv`：记录 `doc/public/user_research/003_evidence-collection-tasks/` 下三份空白 graph-edge 证据收集记录草稿，把 agent 路由到关系图谱 JSONL 文件，但不记录已收集图谱边证据、构件判定、演化链声明或释读结论。
