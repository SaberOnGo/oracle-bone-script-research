# Open-Oracle Strategy Review

## English

`src-open-oracle` is adopted as a reviewed project index and strategy reference. It should help this repository discover useful datasets, papers, code repositories, and evaluation tasks, but it is not a primary paleographic authority and should not override institutional catalogues, excavation provenance, published character dictionaries, or specialist scholarship.

Reference source:

- Source ID: `src-open-oracle`
- Project: `Yuliang-Liu/Open-Oracle`
- URL: <https://github.com/Yuliang-Liu/Open-Oracle>
- Reviewed on: 2026-06-04

Useful strategies to borrow:

1. Maintain a project-hub layer that links papers, code, datasets, task definitions, and download locations from one source register.
2. Separate AI task types instead of treating "decipherment" as one black-box problem. Useful task families include recognition, retrieval, radical/component reconstruction, evolution-chain analysis, image/text reasoning, benchmark evaluation, and hypothesis generation.
3. Treat large AI datasets as evidence packages. Each package needs source review, rights review, size handling, checksum records, and a clear statement of whether it is a research corpus, benchmark, or auxiliary model-training source.
4. Use HUST-OBC and EVOBC as high-value candidate datasets for large-scale character images, undeciphered-character classes, and glyph-evolution experiments, while keeping their raw assets under the large-source workflow until source chains and rights are reviewed.
5. Borrow the radical/component reconstruction framing as a way to create agent evidence packs: image evidence, component hypotheses, possible historical forms, supporting evidence, and opposing evidence should be stored separately.
6. Use diffusion or generation-based methods only as clue-generation tools. Generated clues are drafts and must never be stored as confirmed readings.
7. Use benchmark ideas such as OBI-Bench to evaluate where AI agents fail: fine-grained visual perception, inscription context recovery, retrieval quality, and reasoning from incomplete evidence.

Boundaries:

1. Do not copy Open-Oracle content wholesale into this repository.
2. Do not treat Open-Oracle as an official character ID system.
3. Do not bulk download linked datasets into Git. Large or rights-sensitive files must go through `project_registry/006_large-source-register/`.
4. Do not treat AI paper outputs as confirmed philological conclusions. Store them as model/method references or hypotheses until checked against primary evidence and published scholarship.

Implementation consequence:

`src-open-oracle` should stay in the source registry as `adopted_project_index` and `reviewed`. Linked datasets and papers should be registered as separate source records when they become relevant, because each one has its own authority level, rights status, provenance chain, and size policy.

## 简体中文

`src-open-oracle` 在本项目中采纳为“已评审的项目索引和策略参考”。它适合帮助本仓库发现有价值的数据集、论文、代码仓库和评测任务，但它不是甲骨文字形、释读或出土来源的第一权威，不能替代小學堂、《合集材料來源表》、史语所藏品数据库、已出版字书、考古著录和专业学术研究。

参考来源：

- 来源 ID：`src-open-oracle`
- 项目：`Yuliang-Liu/Open-Oracle`
- 地址：<https://github.com/Yuliang-Liu/Open-Oracle>
- 评审日期：2026-06-04

值得借鉴的策略：

1. 保留一个“项目枢纽层”：用来源登记表把论文、代码、数据集、任务定义和下载位置串起来。
2. 把 AI 任务拆开，不把“破译”当作一个黑箱问题。可拆分为识别、检索、构件/偏旁重构、字形演化链分析、图文推理、基准评测和假说生成。
3. 把大型 AI 数据集当作“证据包”管理。每个包都要有来源评审、权利评审、大小处理、校验和记录，并说明它到底是研究语料、评测集，还是辅助训练材料。
4. HUST-OBC 和 EVOBC 可作为大规模字形图片、未释字类别、字形演化实验的重要候选来源，但原始资源必须先走大型资料流程，确认来源链和权利状态后再决定如何导入。
5. 借鉴构件/偏旁重构的思路来设计 agent 证据包：图像证据、构件假说、可能的历史字形、支持证据和反对证据应分开保存。
6. 扩散模型或生成式方法只能作为“线索生成”工具。生成结果属于草稿或假说，不能作为已确认释读保存。
7. 借鉴 OBI-Bench 这类基准评测思路，专门检查 AI agent 在哪里失败：细粒度视觉识别、同版语境恢复、检索质量、以及基于残缺证据推理的能力。

边界规则：

1. 不把 Open-Oracle 的内容整段复制进本仓库。
2. 不把 Open-Oracle 当成官方甲骨文字 ID 系统。
3. 不把其链接的大型数据集直接批量下载并提交到 Git。大型或权利敏感资料必须走 `project_registry/006_large-source-register/`。
4. 不把 AI 论文输出视为已确认的古文字学结论。它们只能作为模型方法参考或待验证假说，必须再与原始证据和已发表研究互证。

实施结论：

`src-open-oracle` 应在来源登记中保持为 `adopted_project_index` 和 `reviewed`。它链接到的具体数据集和论文，如果后续要使用，应分别登记为独立来源，因为每个来源都有自己的权威等级、权利状态、来源链和文件大小处理规则。
