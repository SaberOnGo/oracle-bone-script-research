# Statistics Generation Tools / 统计生成工具

English:
Future statistics tools will generate occurrence, co-occurrence, period, topic, site, and grammar-position summaries.

Current tools:

English supplement:
- `build_source_pipeline_gap_matrix.py` writes `132_ai-agent-source-pipeline-gap-matrix.csv`, a 21-row source-level gap matrix derived from the source register and 094 pipeline audit. It is a review navigation file only and keeps rights decisions, source promotion, corpus import, and decipherment claims unset.

简体中文补充：
- `build_source_pipeline_gap_matrix.py` 生成 21 行来源级缺口矩阵 `132_ai-agent-source-pipeline-gap-matrix.csv`，输入为来源登记表和 094 流水线审计。该文件只作为复核导航，不作权利裁定、不提升来源、不导入语料，也不提出释读结论。

English supplement:
- `build_source_engineering_first_wave_source_status.py` creates `122_ai-agent-source-engineering-first-wave-source-status.csv` by rolling up the 119 route results and 121 follow-up tasks per source. The output is a source-engineering navigation surface only and keeps rights, promotion, import, identity, component, evolution, and decipherment decisions pending review.

简体中文补充：
- `build_source_engineering_first_wave_source_status.py` 将 119 路线结果和 121 后续任务按来源汇总为 `122_ai-agent-source-engineering-first-wave-source-status.csv`。该输出只用于来源工程导航，继续保持权利、提升、导入、身份、构件、演化和释读决定待复核。

- `build_relationship_graph_statistics.py`: generates edge-type and node-degree CSV summaries from reviewed relationship graph JSONL files.
- `build_source_coverage_statistics.py`: generates a source-level coverage summary from reviewed source registers, download logs, metadata profiles, asset records, relationship-graph summaries, and the HUST-OBC promotion queue.
- `build_preprocessing_status_audit.py`: generates a repository-wide preprocessing status audit across source registration, download logs, large-source handling, candidate records, graph edges, assets, and review queues. The output is infrastructure status only, not a formal decipherment or identity claim.
- `build_data_quality_audit.py`: checks preprocessing tables and graph-edge files for required-field completeness, duplicate keys, source/download/large-source reference integrity, route-file availability, and candidate-boundary status fields. The output is an engineering-quality audit only.
- `build_source_processing_pipeline_audit.py`: generates one processing-pipeline row per registered source, covering download/access logs, checksum and size presence, field maps, package manifests, metadata profiles, derived records, graph edges, review routes, and next actions.
- `build_source_pipeline_gap_matrix.py`: generates `132_ai-agent-source-pipeline-gap-matrix.csv` from the source register and 094 pipeline audit, classifying per-source preprocessing gaps and review lanes while preserving no-new-rights-decision, not-promoted, not-imported, and no-decipherment-claim boundaries.
- `build_core_corpus_readiness_matrix.py`: generates a core-corpus readiness matrix and manual-review backlog summary across character, undeciphered, component, inscription, asset, bibliography, graph, and research-note entry points. The output is a preprocessing navigation aid only.
- `build_source_engineering_gap_queue.py`: generates 099 source-engineering gap review tasks from the current source pipeline and coverage audits, recording missing metadata profiles, field maps, package manifests, access-boundary follow-up, checksum review, and safe derivative decisions without promoting sources or scholarly claims.
- `build_source_engineering_execution_matrix.py`: generates a source-level execution matrix and summary from the 099 gap queue and 094 source pipeline audit, giving each registered source one metadata-only preprocessing work row without downloading raw material, importing corpus records, clearing rights, or promoting candidate scholarship.
- `build_source_engineering_first_wave_source_status.py`: aggregates the 119 first-wave review results and 121 follow-up queue into 122 source-level status rows, preserving metadata-only, no-new-rights-decision, not-promoted, not-imported, and no-decipherment-claim boundaries.

简体中文补充：
- `build_source_engineering_gap_queue.py`：从当前来源流水线和覆盖率审计生成 099 来源工程缺口复核队列，记录 metadata profile、field map、package manifest、访问边界、checksum 复核和安全派生记录决策等缺口；该输出不提升来源、不导入语料，也不构成学术结论。

简体中文：
未来统计工具会生成出现次数、共现、时代、主题、地点和语法位置统计。

当前工具：

- `build_relationship_graph_statistics.py`：从已复核的 relationship graph JSONL 文件生成边类型和节点度数 CSV 汇总。
- `build_source_coverage_statistics.py`：从已复核的来源登记、下载日志、metadata profile、资产记录、关系图谱汇总和 HUST-OBC promotion queue 生成来源级覆盖统计。
- `build_preprocessing_status_audit.py`：对来源登记、下载日志、大型来源处理、候选记录、图边、资产和复核队列生成仓库级预处理状态盘点；输出只表示基础设施状态，不构成正式释读或身份判断。
- `build_data_quality_audit.py`：检查预处理表和图边文件的必填字段完整性、重复键、来源/下载/大型来源引用完整性、路径可用性和候选边界状态字段；输出仅为资料工程质量审计。
- `build_source_processing_pipeline_audit.py`：为每个已登记来源生成处理流水线记录，覆盖下载/访问日志、checksum 与大小记录、字段映射、包清单、metadata profile、派生记录、图边、复核路线和下一步动作。
- `build_core_corpus_readiness_matrix.py`：围绕单字、未释字、构件、卜辞、资产、书目、关系图和研究笔记入口生成核心语料 readiness 矩阵与人工复核 backlog 摘要；输出仅用于预处理导航。

English supplement:
- build_source_engineering_execution_matrix.py also writes 100_ai-agent-source-engineering-execution-matrix.csv and 101_source-engineering-execution-summary.json as metadata-only source preprocessing work surfaces.

简体中文补充：
- build_source_engineering_execution_matrix.py 同时生成 100_ai-agent-source-engineering-execution-matrix.csv 与 101_source-engineering-execution-summary.json，作为 metadata-only 的来源预处理执行入口。

English supplement:
- `build_source_engineering_lane_summary.py` generates `106_ai-agent-source-engineering-lane-summary.csv` by grouping the 104 next-action checklist and 105 empty result scaffold into six source-engineering review lanes. The output is a metadata-only backlog summary; it does not complete review actions, collect evidence, decide rights, import corpus records, promote sources, or make decipherment claims.

简体中文补充：
- `build_source_engineering_lane_summary.py` 将 104 下一步行动清单和 105 空结果脚手架汇总为六个来源工程复核泳道，并生成 `106_ai-agent-source-engineering-lane-summary.csv`。该输出只是 metadata-only 的 backlog 汇总；它不完成复核动作、不采集证据、不裁定权利、不导入语料、不提升来源，也不提出释读结论。
