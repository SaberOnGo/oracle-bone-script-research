# Oracle Bone Script Research Project Architecture Plan

> Status: discussion draft. This document is only for project planning. Do not implement the directory structure, record schema, database, or scripts until the owner confirms the architecture.

## 1. 项目定位

本项目不是“自动破译甲骨文模型”，而是建设一个可长期积累、可机器检索、可支持 AI Agent 推理与协作的甲骨文开放研究基础设施。

项目的长期目标是推动甲骨文研究的民主化。甲骨文研究长期具有较高资料门槛、专业门槛和工具门槛，普通人即使有热忱和好奇心，也很难进入。本项目希望通过结构化资料、可追溯证据链、知识图谱和 AI Agent 工作流，降低资料门槛、专业信息差和工具门槛，让普通人也能在规范证据框架下进行检索、比对、提问、假说生成和人工复核。

项目希望把资料、方法和证据链转化为更开放、可访问、可复核、可扩展的研究系统。

### 1.1 项目使命与传播表达

这个项目的传播核心可以概括为：

```text
让甲骨文研究从高门槛的专业领域，
变成每一个有热忱、有好奇心的人都可以借助 AI Agent 参与的开放研究。
```

更短的中文表达：

```text
用 AI Agent 推动甲骨文研究民主化。
```

```text
降低甲骨文研究的信息差，让专业知识变得可访问、可检索、可复核。
```

```text
把甲骨文研究从资料门槛、专业门槛和工具门槛中释放出来，
建设一个普通人也能参与的证据化研究平台。
```

对应英文表达：

```text
Democratizing access to oracle bone script research with AI agents.
```

```text
A knowledge base, knowledge graph, and AI agent framework for making oracle bone script research accessible, searchable, and evidence-based.
```

```text
From high-barrier scholarship to evidence-based public research powered by AI agents.
```

关键词：

- 研究民主化：democratization of research
- 知识民主化：democratization of knowledge
- 知识普惠：inclusive access to knowledge
- 学术研究普及化：popularization of scholarly research
- 降低专业研究门槛：lowering barriers to specialist research
- 让专业知识可访问化：making specialist knowledge accessible
- 甲骨文研究可访问化：democratizing access to oracle bone script research

推荐定位：

```text
甲骨文知识库 + 知识图谱 + AI Agent 研究助手 + 开放研究基础设施
```

核心目标：

- 系统整理已释甲骨字、未释甲骨字、字形变体、构件拆分、同版卜辞、出土信息、时代信息、金文/小篆/今文对应、专家释读依据和争议。
- 降低甲骨文研究的信息差和进入门槛，让有热忱、有好奇心的普通人也能借助 AI Agent 参与证据化研究。
- 用结构化资料支持历史学、语言学、考古学、统计学结合的释读推理。
- 让 AI Agent 基于检索出的证据调用工具、统计、知识图谱和大模型，提出候选解释、支持证据、反对证据和待验证假说。

第一阶段不训练模型。优先建设数据结构、资料来源、目录规范和最小可用知识库。

## 2. 总体原则

### 2.1 文件和目录名必须自说明

目录名和文件名应尽量让人类和 AI 只看路径就能判断内容类型。

原则：

- 使用数字前缀保证排序稳定，例如 `001_`、`002_`。
- 使用稳定 ID 保证后续解释变化时路径不必频繁改名。
- 使用英文类别名保证跨平台、脚本、GitHub、数据库工具兼容。
- 目录名和文件名尽量不要依赖现代汉字、隶定字、拼音或英文释义，因为很多古文字无法可靠对应现代文字，且释读结论可能变化。
- 中文释读、隶定字、争议说明放入结构化 metadata 文件中。目录名优先使用本系统 ID 和外部权威资料编号。
- 一个目录中不要直接堆几千个子目录。甲骨单字资料建议每 100 个一个 bucket。

### 2.2 Git 仓库优先保存“可公开、可追溯、可结构化”的资料

公开仓库中应优先保存：

- 数据 schema。
- 索引。
- 研究说明。
- 公开许可资料。
- 图片/拓片/论文的来源引用与 metadata。
- 小尺寸、确定可公开的示例图片。

公开仓库中应谨慎保存：

- 版权不明确的扫描图。
- 论文全文。
- 大规模图片。
- 商业出版物整理文本。

建议后续区分：

- GitHub public repository: 代码、schema、索引、说明文档、可公开数据。
- Local private material folder: 明确不准备提交到 GitHub 的本地私有大图、扫描件、论文 PDF、个人整理材料。
- Generated database: 由结构化文件导入 PostgreSQL/SQLite/Neo4j 等检索系统。

### 2.3 文件系统作为人工维护入口，数据库作为检索和推理入口

建议采用双层设计：

```text
人类维护层：Markdown + YAML + CSV + JSONL + 图片/资料引用
机器检索层：PostgreSQL + graph edges + vector index
```

早期不应直接把全部工作锁死在数据库里。文件系统更适合 Git 版本控制、人工审校、AI 阅读和逐步修订。数据库应由结构化文件生成。

## 3. 推荐顶层目录结构

以下结构是“实施后”的建议，不应在确认前创建。

```text
oracle-bone-script-research/
  AGENTS.md
  README.md
  README.zh-CN.md
  LICENSE
  .gitignore

  doc/
    project/
      001_project-positioning-and-research-boundaries/
      002_data-rights-and-source-policy/
      003_data-model-and-id-system/
      004_oracle-bone-script-research-methods/
      005_ai-agent-research-assistant-design/
    public/
      user_plan/
      user_research/

  readme/
    README.zh-TW.md
    README.ja.md

  license/
    001_code-license-notes/
    002_data-license-and-rights-policy/
    003_third-party-source-attribution/

  project_registry/
    001_repository-structure-and-naming-rules/
    002_project-id-to-source-reference-map/
    003_external-source-prefixes/
    004_asset-source-and-rights-index/
    005_bilingual-project-glossary/

  schemas/
    001_character-record-schema/
    002_inscription-record-schema/
    003_source-record-schema/
    004_graph-edge-schema/
    005_asset-metadata-schema/

  corpus/
    001_oracle-characters/
    002_oracle-bone-inscriptions/
    003_graphemic-components/
    004_bronze-seal-modern-correspondences/
    005_excavation-sites-periods-and-batches/
    006_research-sources-and-bibliography/
    007_research-topics-and-grammar/
    008_relationship-graph/
    009_statistics-and-derived-features/

  research/
    001_published-scholarship-index/
    002_decipherment-history/
    003_scholarly-arguments-and-disputes/
    004_bibliographic-notes/

  skills/
    001_data-curation-workflow/
    002_source-provenance-review/
    003_ai-agent-evidence-pack-review/

  tools/
    001_data-validation/
    002_data-import/
    003_graph-generation/
    004_statistics-generation/
    005_ai-context-pack-builder/

  tests/
    001_data-schema-validation/
    002_source-reference-validation/
    003_path-naming-validation/

  database/
    001_postgresql-schema/
    002_seed-corpus/
    003_migrations/

  apps/
    001_research-assistant-api/
    002_research-assistant-web/
```

说明：

- `AGENTS.md`: AI Agent 进入本仓库后的强制入口说明，要求先读项目规则、命名规则、来源追溯规则和相关 workflow。
- `README.md`: 英文项目首页。
- `README.zh-CN.md`: 简体中文项目首页。
- `doc/project/`: 项目规则、研究边界、资料政策、AI Agent 推理设计。
- `doc/public/user_plan/`: 用户讨论草案，不一定是最终正式文档位置。
- `doc/public/user_research/`: 普通用户或 AI Agent 的研究草稿、假说、阶段性分析和复核记录。这里的内容可以频繁变化，不等同于已发表学术结论。
- `readme/`: 其他语言 README 或扩展说明。
- `license/`: 代码、数据、图片、论文引用、第三方来源的授权和使用边界说明。
- `project_registry/`: 根目录级项目注册表，集中说明项目结构、命名规则、本项目 ID 与外部来源 ID 的映射、资料引用来源和中英文术语。它是人类和 AI Agent 追溯数据来源的第一入口。
- `schemas/`: 每类结构化文件的字段规范。
- `corpus/`: 人工维护的核心资料。
- `research/`: 已有学术研究、已发表观点、专家释读史、论文索引和严谨文献摘录。这里不同于 `doc/public/user_research/`，不能随意写入未经复核的 AI 假说。
- `skills/`: 面向 AI Agent 和贡献者的可复用工作流说明。
- `tools/`: 后续用于校验、导入、生成统计和构建 AI Agent 上下文包的脚本。
- `tests/`: 数据结构、命名规则、来源引用、导入逻辑和工具行为的测试。
- `database/`: PostgreSQL 等数据库落地结构。
- `apps/`: 后续 Web/API AI Agent 研究助手。

注：用户提到的 `test/`、`tool/` 在正式仓库中建议采用常见复数形式 `tests/`、`tools/`，与参考仓库结构和常见工程习惯一致。如果最终希望严格使用单数目录名，可在实施前统一调整。

### 3.1 `project_registry/` 的职责

`project_registry/` 专门解决两个问题：

1. 下载仓库后，人类或 AI Agent 如何理解这个项目的目录结构。
2. 根据本项目 ID 如何追溯外部数据库、字编、著录、图版、论文和图片来源。

推荐结构：

```text
project_registry/
  001_repository-structure-and-naming-rules/
    001_repository-structure.zh-CN.md
    002_repository-structure.en.md
    003_file-and-directory-naming-rules.zh-CN.md
    004_file-and-directory-naming-rules.en.md

  002_project-id-to-source-reference-map/
    001_oracle-character-id-source-map.csv
    002_oracle-inscription-id-source-map.csv
    003_asset-id-source-map.csv
    004_component-id-source-map.csv

  003_external-source-prefixes/
    001_external-source-prefixes.zh-CN.md
    002_external-source-prefixes.en.md
    003_external-source-prefixes.csv

  004_asset-source-and-rights-index/
    001_asset-source-index.csv
    002_asset-rights-review-log.csv

  005_bilingual-project-glossary/
    001_terms.zh-CN.md
    002_terms.en.md
```

`002_project-id-to-source-reference-map/` 是核心。它应允许通过 `obs-char-000001`、`obi-000001`、`asset-000001` 等本项目 ID 找到：

- 首选外部 ID。
- 全部外部 ID。
- 来源数据库或著录系统。
- 图版号、旧著录号、馆藏号。
- 对应目录路径。
- 资料权利状态。
- 最后复核时间。

示例字段：

```csv
project_id,record_type,canonical_path,primary_external_ref_id,all_external_ref_ids,source_ids,rights_status,review_status,updated_at
obs-char-000001,oracle_character,corpus/001_oracle-characters/001_000001-000100_obs-char-bucket_oracle-characters/001_obs-char-000001_xxt-jgw-0001_oracle-character,xxt-jgw-0001,"xxt-jgw-0001;unicode-u99ac","src-xiaoxuetang-jiaguwen;src-unicode",metadata_only_until_verified,draft,2026-06-04
```

这样文件名/目录名可以保持短而自说明，完整引用来源则集中保存在 `project_registry/` 与各资料包 metadata 中。

### 3.2 `doc/public/user_research/` 与根目录 `research/` 的区别

`doc/public/user_research/`：

- 存放普通用户、贡献者或 AI Agent 的研究草稿。
- 可以包含未成熟假说、检索记录、对比笔记、AI 输出、人工复核意见。
- 可以频繁修改，甚至每天变化。
- 必须明确标记为草稿、假说、待复核或已复核。
- 不应被当作正式学术结论引用。

`research/`：

- 存放已有学术研究、已发表论文/专著观点、专家释读史、严谨文献索引和来源笔记。
- 更接近“已发表研究资料库”。
- 写入前应有明确来源、引用、出处、页码或数据库链接。
- 不应混入未经复核的 AI Agent 草稿。
- 版权不明确的论文和图书不直接存全文，优先存书目信息、摘要、引用位置和合法链接。

## 4. 甲骨单字资料库目录设计

### 4.1 全局目录

建议把所有甲骨单字资料放在：

```text
corpus/001_oracle-characters/
```

下面按每 100 个甲骨字分桶：

```text
corpus/001_oracle-characters/
  000_character-registers/
    001_all-oracle-characters-index.csv
    002_deciphered-oracle-characters-index.csv
    003_undeciphered-oracle-characters-index.csv
    004_character-id-assignment-log.md
    005_external-reference-prefixes-and-source-map.md

  001_000001-000100_obs-char-bucket_oracle-characters/
  002_000101-000200_obs-char-bucket_oracle-characters/
  003_000201-000300_obs-char-bucket_oracle-characters/
  ...
  015_001401-001500_obs-char-bucket_oracle-characters/
  016_001501-001600_obs-char-bucket_oracle-characters/
```

推荐使用“本系统稳定 ID + 外部来源 ID”的组合方式。

`obs` = oracle bone script。

基础格式：

```text
obs-char-000001_xxt-jgw-0001
```

含义：

- `obs-char-000001`: 本项目内部稳定编号，由本项目分配。
- `xxt-jgw-0001`: 首选外部来源编号，用于追溯到现有权威或常用资料系统。

不要只使用 `obs-char-000001`，因为它只能在本项目内部定位，不能直接证明该资料来自哪一个现有数据库、字编、著录或图版来源。也不要只使用外部编号，因为不同字编、数据库、论文和图版系统可能有不同编号，且同一字可能需要对应多个来源。

因此推荐规则是：

```text
数字前缀_本项目ID_首选外部ID_简短类型说明
```

完整外部引用列表放在 metadata 中。

对于有大量子目录的资料，应使用分桶目录：

```text
数字前缀_区段_本项目ID类型-bucket_资料类型
```

例如：

```text
001_000001-000100_obs-char-bucket_oracle-characters/
```

原因：

- 不依赖某一本字编的编号。
- 不依赖当前是否已释读。
- 不依赖现代汉字是否有 Unicode。
- 后续释读变化时 ID 不变。
- 可以通过外部来源 ID 快速追溯数据、图片、释读、卜辞和著录来源，类似论文引用。
- 方便人类和 AI 判断资料可靠性，并回应“数据从哪里来”的质疑。

### 4.1.1 外部编号与来源追溯策略

目前不应假设甲骨单字存在一个全学界、跨全部资料系统唯一公认的 ID。更稳妥的做法是记录多个外部来源编号。

可优先参考的外部编号类型：

```text
xxt-jgw-0001       小學堂甲骨文字號，基于《甲骨文編》顺序
jgwbian-0001       《甲骨文編》相关编号或页码
jgwzibian-0001     《甲骨文字編》相关编号或页码
jgwzgl-0001        《甲骨文字詁林》相关编号或页码
heji-010308        《甲骨文合集》图版号，主要用于卜辞/字形出处，不等同于单字 ID
oldcat-tie-001-002 旧著录号，例如《鐵雲藏龜》相关编号
chardb-cid-08171   汉字古今字资料库/字形演变页的现代字或字头链接 ID
unicode-u9aa8      可对应现代汉字时的 Unicode 编码
```

说明：

- 单字目录的首选外部编号建议优先采用稳定、可检索、覆盖面较广的字头/字形数据库编号。
- 卜辞、拓片、出土资料和图片资产应优先记录 `heji-*`、旧著录号、馆藏号、图版号等来源编号。
- 一个字可能对应多个外部编号，目录名只放一个首选外部编号，完整编号列表写入 metadata。
- 对未释字或暂时无法对应外部编号的字，可暂用 `extid-unassigned`，但必须在 metadata 中记录来源图版、图片、卜辞或采集批次。

参考依据：

- 小學堂甲骨文資料庫支持按字號、字形、頁碼、合集號、舊著錄、類組等条件检索。
- 小學堂说明中提到，甲骨文字號是该字在《甲骨文編》中的顺序。
- 《甲骨文合集》图版编号是以一片甲骨实物为一号，适合追溯卜辞、图版和字形出处。

参考链接：

- [小學堂甲骨文資料庫](https://xiaoxue.iis.sinica.edu.tw/jiaguwen)
- [小學堂甲骨文資料庫簡介](https://xiaoxue.iis.sinica.edu.tw/jiaguwen/About/About)
- [漢字古今字資料庫使用簡介](https://xiaoxue.iis.sinica.edu.tw/CCDB/Content/Files/ccdb-Get_Started.pdf)
- [甲骨文合集材料來源表](https://xiaoxue.iis.sinica.edu.tw/obm)
- [甲骨文合集材料來源表凡例](https://xiaoxue.iis.sinica.edu.tw/obm/Home/Example)

### 4.2 单字目录命名

推荐格式：

```text
001_obs-char-000001_xxt-jgw-0001_oracle-character/
002_obs-char-000002_xxt-jgw-0003_oracle-character/
100_obs-char-000100_extid-unassigned_oracle-character/
```

不推荐目录名包含现代汉字、隶定字、拼音或英文释义。

原因：

- 许多甲骨字没有可靠现代汉字对应。
- 同一甲骨字可能有多个隶定、释读或争议读法。
- 目录名一旦使用释读结果，后续释读修订会导致路径不稳定。
- 文件路径应像论文引用一样优先提供“可追溯来源编号”，而不是把释读结论写进路径。

建议默认使用 ASCII 路径，把中文信息、释读、隶定、来源编号放入 metadata：

```yaml
oracle_character_id: obs-char-000001
primary_external_ref_id: xxt-jgw-0001
decipherment_status: deciphered
modern_character: 馬
liding_character: 馬
pinyin: ma
primary_english_label: horse
external_references:
  - external_ref_id: xxt-jgw-0001
    source_id: src-xiaoxuetang-jiaguwen
    id_type: jiaguwen_zihao
    external_value: "1"
    source_basis: "《甲骨文編》顺序"
    url: "https://xiaoxue.iis.sinica.edu.tw/jiaguwen?kaiOrder=1"
  - external_ref_id: unicode-u99ac
    source_id: src-unicode
    id_type: unicode
    external_value: "U+99AC"
```

这样可以避免脚本、URL、命令行和跨平台同步时出现编码问题。

### 4.2.1 图片、拓片、摹本和资料文件命名

图片、拓片、摹本、截图和下载资料也应尽量在文件名中带有来源编号，方便离线下载后仍能追溯来源。

推荐格式：

```text
001_asset-000001_xxt-jgw-0001_glyph-image.png
002_asset-000002_heji-010308_rubbing-image.jpg
003_asset-000003_oldcat-tie-001-002_source-note.md
```

命名原则：

- `asset-000001`: 本项目内部资产编号。
- `xxt-jgw-0001`: 字头/字形数据库外部编号。
- `heji-010308`: 《甲骨文合集》图版号或卜辞出处编号。
- `oldcat-tie-001-002`: 旧著录来源编号。
- 文件名只放最关键的 1 个首选外部追溯 ID 和极短类型说明。完整来源、版权、下载 URL、截图范围、图版位置、其他外部 ID 放入 asset metadata 和 `project_registry/`。

推荐每个图片目录都保留资产索引：

```text
001_oracle-glyph-image-assets/
  000_asset-index.csv
  001_asset-000001_xxt-jgw-0001_glyph-image.png
  001_asset-000001_xxt-jgw-0001_glyph-image.yaml
```

对应 metadata 示例：

```yaml
asset_id: asset-000001
asset_type: oracle_glyph_image
related_oracle_character_id: obs-char-000001
related_external_ref_ids:
  - xxt-jgw-0001
  - heji-010308
source_id: src-xiaoxuetang-jiaguwen
source_url: "https://xiaoxue.iis.sinica.edu.tw/jiaguwen?kaiOrder=1"
source_catalog_refs:
  - source_id: src-jiaguwen-heji
    id_type: heji_plate_number
    value: "10308"
rights_status: metadata_only_until_verified
local_file: 001_asset-000001_xxt-jgw-0001_glyph-image.png
review_status: draft
```

### 4.3 单字目录内部结构

推荐每个甲骨字目录内部结构：

```text
001_obs-char-000001_xxt-jgw-0001_oracle-character/
  00_README.zh-CN.md
  01_core-character-record.yaml
  02_decipherment-status-and-readings.yaml
  03_component-breakdown.yaml

  04_oracle-glyph-forms-and-variants/
    001_oracle-glyph-variant-index.csv
    002_oracle-glyph-image-assets/
    003_rubbing-and-hand-copy-assets/
    004_variant-chain-notes.zh-CN.md

  05_inscription-contexts/
    001_occurrence-index.csv
    002_full-inscription-contexts.zh-CN.md
    003_same-inscription-neighbor-characters.csv
    004_grammar-position-notes.zh-CN.md

  06_cooccurrence-and-statistics/
    001_character-cooccurrence-summary.csv
    002_topic-distribution-summary.csv
    003_period-distribution-summary.csv
    004_site-distribution-summary.csv

  07_bronze-seal-modern-correspondence/
    001_bronze-script-correspondence.yaml
    002_seal-script-correspondence.yaml
    003_modern-character-correspondence.yaml
    004_graphic-evolution-notes.zh-CN.md

  08_excavation-and-source-provenance/
    001_excavation-context.yaml
    002_source-bibliography.yaml
    003_rubbing-copy-source-notes.zh-CN.md
    004_collection-and-catalog-references.csv

  09_expert-decipherment-evidence/
    001_main-decipherment-evidence.zh-CN.md
    002_expert-opinions-and-disputes.zh-CN.md
    003_supporting-and-opposing-evidence.zh-CN.md
    004_research-history-timeline.csv

  10_ai-research-hypotheses/
    001_machine-readable-evidence-pack.json
    002_ai-generated-hypotheses.zh-CN.md
    003_human-review-log.md
```

这套结构覆盖：

- 甲骨字图像。
- 拓片/摹本来源。
- 已释读字。
- 隶定字。
- 构件拆分。
- 字形变体。
- 所在卜辞全文。
- 出土批次/坑位/著录来源。
- 同版其他字。
- 金文/铭文/小篆/今文字形演变。
- 专家释读过程与争议。
- 共现统计。
- 语法位置。
- AI Agent 假说与人工复核。

### 4.4 单字核心记录字段

`01_core-character-record.yaml` 建议字段：

```yaml
oracle_character_id: obs-char-000001
record_type: oracle_character
preferred_directory_name: 001_obs-char-000001_xxt-jgw-0001_oracle-character
primary_external_ref_id: xxt-jgw-0001
decipherment_status: deciphered

modern_character: 馬
liding_character: 馬
pinyin: ma
primary_english_label: horse

confidence_level: high
character_family_id: obs-family-000001
component_ids:
  - obs-comp-000001

main_periods:
  - period-001
main_sites:
  - site-001

primary_sources:
  - src-jiaguwen-heji
  - src-jiaguwenzibian

external_references:
  - external_ref_id: xxt-jgw-0001
    source_id: src-xiaoxuetang-jiaguwen
    id_type: jiaguwen_zihao
    external_value: "1"
    source_basis: "《甲骨文編》顺序"
    url: "https://xiaoxue.iis.sinica.edu.tw/jiaguwen?kaiOrder=1"
  - external_ref_id: heji-010308
    source_id: src-jiaguwen-heji
    id_type: heji_plate_number
    external_value: "10308"
    note: "该编号用于具体图版/卜辞出处，不等同于单字主 ID。"

created_at: 2026-06-04
updated_at: 2026-06-04
review_status: draft
```

`02_decipherment-status-and-readings.yaml` 建议字段：

```yaml
oracle_character_id: obs-char-000001
decipherment_status: deciphered
accepted_readings:
  - reading_id: reading-000001
    modern_character: 馬
    liding_character: 馬
    confidence_level: high
    accepted_by:
      - source_id: src-example-001
    evidence_summary: "字形、语境、后世文字演变链均支持释为馬。"

alternative_readings: []
controversy_level: low
needs_human_review: false
```

`03_component-breakdown.yaml` 建议字段：

```yaml
oracle_character_id: obs-char-000001
breakdown_level: reviewed
components:
  - component_id: obs-comp-000001
    component_label: horse-body
    position: whole
    confidence_level: medium
component_notes: "此字整体象形，暂不强拆为左右/上下构件。"
```

## 5. 卜辞资料库目录设计

甲骨文破译不能只存单字，必须保存上下文。

推荐目录：

```text
corpus/002_oracle-bone-inscriptions/
  000_inscription-registers/
    001_all-inscriptions-index.csv
    002_inscription-source-index.csv
    003_inscription-topic-index.csv

  001_obi-000001-000100_oracle-bone-inscriptions/
  002_obi-000101-000200_oracle-bone-inscriptions/
```

`obi` = oracle bone inscription。

单条卜辞目录：

```text
obi-000001_heji-00001_oracle-bone-inscription/
  00_README.zh-CN.md
  01_core-inscription-record.yaml
  02_transcription-and-translation.zh-CN.md
  03_character-sequence.csv
  04_topics-people-places-events.yaml
  05_excavation-and-catalog-provenance.yaml
  06_image-and-rubbing-assets/
  07_related-character-occurrences.csv
  08_research-notes.zh-CN.md
```

卜辞核心字段：

```yaml
inscription_id: obi-000001
record_type: oracle_bone_inscription
catalog_numbers:
  heji: "00001"
period_id: period-001
site_id: site-001
pit_or_batch_id: batch-001

topics:
  - ritual
  - warfare

people:
  - person-king-wu-ding

places:
  - place-example-001

transcription_status: reviewed
source_ids:
  - src-jiaguwen-heji
```

## 6. 构件资料库目录设计

构件是破译推理的核心之一，不能只作为单字字段存在。

推荐目录：

```text
corpus/003_graphemic-components/
  000_component-registers/
    001_all-components-index.csv
    002_component-family-index.csv

  001_obs-comp-000001-000100_graphemic-components/
```

单个构件目录：

```text
obs-comp-000001_person-form_graphemic-component/
  00_README.zh-CN.md
  01_core-component-record.yaml
  02_component-forms-and-variants/
  03_characters-containing-this-component.csv
  04_semantic-and-phonetic-function-notes.zh-CN.md
  05_research-source-evidence.yaml
```

构件需要记录：

- 构件 ID。
- 构件名称。
- 字形变体。
- 在哪些甲骨字中出现。
- 位置关系：左、右、上、下、内、外、整体、附加。
- 可能的语义功能。
- 可能的声符功能。
- 相关金文/小篆形体。
- 释读争议。

## 7. 金文、小篆、今文对应资料库

推荐目录：

```text
corpus/004_bronze-seal-modern-correspondences/
  000_correspondence-registers/
    001_all-correspondences-index.csv
    002_oracle-to-bronze-index.csv
    003_oracle-to-seal-index.csv
    004_oracle-to-modern-index.csv

  001_bronze-script-forms/
  002_seal-script-forms/
  003_modern-character-forms/
  004_graphic-evolution-chains/
```

字形演变链示例：

```text
evolution-chain-000001_xxt-jgw-0001/
  00_README.zh-CN.md
  01_evolution-chain-record.yaml
  02_oracle-bone-script-forms/
  03_bronze-script-forms/
  04_warring-states-script-forms/
  05_seal-script-forms/
  06_clerical-and-regular-script-forms/
  07_evidence-and-dispute-notes.zh-CN.md
```

这个部分支持：

```text
甲骨文 -> 金文 -> 战国文字 -> 小篆 -> 隶书 -> 楷书
```

## 8. 出土地点、时代、批次资料库

推荐目录：

```text
corpus/005_excavation-sites-periods-and-batches/
  001_periods/
  002_excavation-sites/
  003_pits-and-batches/
  004_collection-history/
```

应记录：

- 分期：一期、二期、三期、四期、五期。
- 出土地点。
- 坑位。
- 同坑材料。
- 著录来源。
- 收藏单位。
- 相关骨片是否可能同版、同组、同坑。

这是处理“同坑材料”和“出土关系推理”的基础。

## 9. 研究来源与文献资料库

推荐目录：

```text
corpus/006_research-sources-and-bibliography/
  000_source-registers/
    001_all-sources-index.csv
    002_primary-catalogs-index.csv
    003_secondary-research-index.csv
    004_image-source-index.csv

  001_primary-catalogs/
  002_character-dictionaries/
  003_decipherment-studies/
  004_papers-and-monographs/
  005_online-databases/
```

重点来源类型：

- 《甲骨文合集》
- 《甲骨文字编》
- 《甲骨文字诂林》
- 金文资料。
- 出土记录。
- 专家论文。
- 博物馆公开资料。
- 在线数据库。

每个 source 需要记录：

```yaml
source_id: src-jiaguwen-heji
source_type: primary_catalog
title_zh: 甲骨文合集
title_en: Collection of Oracle Bone Inscriptions
rights_status: unknown_or_restricted
reuse_policy: metadata_only_until_verified
citation_format: ""
notes: ""
```

## 10. 关系图谱设计

关系图谱应把“字、构件、卜辞、地点、时代、主题、人物、文献、释读观点”连接起来。

推荐目录：

```text
corpus/008_relationship-graph/
  001_graph-node-types.md
  002_graph-edge-types.md
  003_graph-nodes.jsonl
  004_graph-edges.jsonl
  005_graph-validation-rules.md
```

### 10.1 核心节点类型

```text
OracleCharacter
OracleGlyphForm
Inscription
GraphemicComponent
BronzeScriptForm
SealScriptForm
ModernCharacter
Reading
Source
Expert
ExcavationSite
ExcavationBatch
Period
Topic
Person
Place
Event
Hypothesis
```

### 10.2 核心关系类型

```text
OracleCharacter CONTAINS_COMPONENT GraphemicComponent
OracleCharacter HAS_VARIANT OracleGlyphForm
OracleCharacter OCCURS_IN Inscription
OracleCharacter COOCCURS_WITH OracleCharacter
OracleCharacter HAS_READING Reading
OracleCharacter HAS_ACCEPTED_READING Reading
OracleCharacter HAS_DISPUTED_READING Reading
OracleCharacter CORRESPONDS_TO BronzeScriptForm
OracleCharacter CORRESPONDS_TO SealScriptForm
OracleCharacter CORRESPONDS_TO ModernCharacter
OracleCharacter APPEARS_IN_PERIOD Period
OracleCharacter FOUND_AT ExcavationSite
OracleCharacter ASSOCIATED_WITH_TOPIC Topic
OracleCharacter SUPPORTED_BY Source

Inscription HAS_CHARACTER OracleCharacter
Inscription HAS_TOPIC Topic
Inscription MENTIONS_PERSON Person
Inscription MENTIONS_PLACE Place
Inscription FROM_BATCH ExcavationBatch
Inscription DATED_TO Period

Reading PROPOSED_BY Expert
Reading SUPPORTED_BY Source
Reading DISPUTED_BY Source
Hypothesis SUPPORTED_BY Evidence
Hypothesis OPPOSED_BY Evidence
```

### 10.3 关系边字段

`004_graph-edges.jsonl` 每行建议：

```json
{
  "edge_id": "edge-000000001",
  "source_node_id": "obs-char-000001",
  "edge_type": "CONTAINS_COMPONENT",
  "target_node_id": "obs-comp-000001",
  "confidence_level": "medium",
  "source_ids": ["src-example-001"],
  "evidence_note": "构件拆分来自某字编及人工复核。",
  "created_at": "2026-06-04",
  "review_status": "draft"
}
```

## 11. 统计和派生资料设计

推荐目录：

```text
corpus/009_statistics-and-derived-features/
  001_character-occurrence-statistics/
  002_character-cooccurrence-statistics/
  003_topic-distribution-statistics/
  004_period-distribution-statistics/
  005_site-distribution-statistics/
  006_graph-centrality-statistics/
  007_visual-similarity-features/
```

早期应优先做：

- 字出现次数。
- 字与字共现。
- 字在不同主题中的分布。
- 字在不同时期中的分布。
- 字在不同出土地点中的分布。
- 字在句法位置中的分布。

图像相似向量可以后置。

阶段建议：

- 1 万张图片以内：人工 metadata + 普通图片索引。
- 10 万张图片以上：加入 DINOv2 或 CLIP 类图像向量。
- 100 万张图片以上：再考虑训练甲骨文字形 embedding。

## 12. AI Agent 研究助手设计

AI Agent 不直接“凭记忆猜字”。它应先检索证据、调用工具、组织上下文，再进行推理。

AI Agent 的角色不是取代专家，也不是给出不可质疑的结论，而是帮助普通研究者和专业研究者共同完成资料检索、证据整理、交叉比对、统计分析、假说生成和复核记录。它应让研究过程更透明，而不是制造新的黑箱。

推荐流程：

```text
未知字图片/ID
  -> 找到单字资料包
  -> 检索字形变体
  -> 检索同版卜辞
  -> 检索周边字
  -> 检索共现统计
  -> 检索同坑材料
  -> 检索时代和主题
  -> 检索金文/小篆/今文对应
  -> 检索专家释读争议
  -> 生成 AI Agent evidence pack
  -> AI Agent 调用大模型提出候选解释
  -> 人工复核并写入研究日志
```

AI Agent 输出应固定包含：

- 候选释读。
- 置信度。
- 支持证据。
- 反对证据。
- 需要补充的数据。
- 可验证预测。
- 与已有专家观点的关系。
- 是否只是字形相似，还是语境、出土、语法、历史背景共同支持。

## 13. 数据录入优先级

### 13.1 MVP 阶段

建议第一批只做 20-50 个甲骨字样例，不要一开始录入 1500 个。

目标是验证：

- 目录结构是否可维护。
- 字符 ID 是否稳定。
- 单字资料包是否过重。
- 卜辞上下文是否能关联。
- 构件拆分是否能查询。
- 金文/小篆对应是否能表达。
- 释读依据和争议是否能被 AI Agent 正确引用。

### 13.2 第一正式阶段

整理：

- 1400+ 或 1500+ 已释字基本记录。
- 每字至少一个核心 metadata。
- 每字至少一个来源引用。
- 每字至少一个释读状态。
- 基础构件拆分。
- 基础金文/小篆/今文对应。

### 13.3 第二正式阶段

整理：

- 《甲骨文合集》卜辞索引。
- 每字出现在哪些卜辞。
- 卜辞全文。
- 同版其他字。
- 出土地点、批次、时代。
- 主题分类：祭祀、战争、农业、天象、疾病、田猎、王事等。

### 13.4 第三正式阶段

整理：

- 专家释读过程。
- 争议说法。
- 支持证据和反对证据。
- 字族和变体链条。
- 共现统计。
- AI Agent evidence pack。

## 14. 建议先确认的关键问题

实施前建议先确认这些架构决策：

1. 单字目录是否采用 `001_obs-char-000001_xxt-jgw-0001_oracle-character` 这种“数字前缀 + 本系统 ID + 首选外部来源 ID + 简短类型”的组合。
2. 单字分桶是否固定每 100 个一个目录。
3. 目录名是否默认 ASCII，且避免使用现代汉字、隶定字、拼音或英文释义作为路径依据。
4. GitHub 是否只存公开可分发资料，版权不明确资料只存引用。
5. 文件系统是否作为 source of truth，数据库由文件生成。
6. 第一批 MVP 是否只录入 20-50 个样例字。
7. 是否优先用 PostgreSQL，图谱先用 edges 表表达，而不是一开始引入 Neo4j。
8. 是否把 AI Agent 假说与人工确认严格分开，避免模型输出污染正式资料。
9. 根目录是否采用 `project_registry/` 作为项目结构、命名规则、本项目 ID 到外部来源引用的总入口。
10. 是否明确区分 `doc/public/user_research/` 的用户/AI Agent 草稿研究与根目录 `research/` 的已发表学术研究。
11. 正式目录是否采用 `tools/`、`tests/` 复数形式，而不是 `tool/`、`test/` 单数形式。

## 15. 推荐实施阶段

确认架构后，建议按阶段实施。

### Phase 0: 项目基础规则

创建：

- `AGENTS.md`
- `README.md`
- `README.zh-CN.md`
- `LICENSE`
- `doc/project/001_project-positioning-and-research-boundaries/`
- `doc/project/002_source-rights-and-provenance-policy/`
- `doc/project/003_record-model-and-id-system/`
- `doc/public/user_research/`
- `project_registry/001_repository-structure-and-naming-rules/`
- `project_registry/002_project-id-to-source-reference-map/`
- `project_registry/003_external-source-prefixes/`
- `license/`
- `readme/`
- `research/`
- `skills/`
- `schemas/`
- `.gitignore`

产出：

- 项目定位文档。
- `AGENTS.md` AI Agent 强制入口规则。
- 中英文 README。
- 数据授权边界文档。
- ID 命名规范。
- 本项目 ID 到外部来源 ID 的映射规范。
- `doc/public/user_research/` 与 `research/` 的写入边界。
- 基础 schema。

### Phase 1: 文件系统资料包 MVP

创建：

- `corpus/001_oracle-characters/`
- `corpus/002_oracle-bone-inscriptions/`
- `corpus/003_graphemic-components/`

产出：

- 20-50 个单字样例资料包。
- 5-10 条卜辞样例资料包。
- 20 个构件样例资料包。
- 基础索引 CSV。

### Phase 2: 校验工具

创建：

- `tools/001_corpus-validation/`

产出：

- 校验 ID 是否重复。
- 校验目录名和 metadata 是否一致。
- 校验 source_id 是否存在。
- 校验 edge 是否指向存在节点。

### Phase 3: PostgreSQL 导入

创建：

- `database/001_postgresql-schema/`
- `tools/002_corpus-import/`

产出：

- 结构化文件导入 PostgreSQL。
- 基础查询：按字、构件、卜辞、主题、时代、来源检索。

### Phase 4: 关系图谱与统计

创建：

- `corpus/008_relationship-graph/`
- `corpus/009_statistics-and-derived-features/`
- `tools/003_graph-generation/`
- `tools/004_statistics-generation/`

产出：

- graph edges。
- 共现统计。
- 主题分布。
- 时代分布。
- 地点分布。

### Phase 5: AI Agent 研究助手

创建：

- `tools/005_ai-context-pack-builder/`
- `apps/001_research-assistant-api/`
- `apps/002_research-assistant-web/`

产出：

- 给单个字生成 evidence pack。
- AI Agent 输出候选释读、证据、反证和待验证问题。
- 人工复核日志。

## 16. 不建议现在做的事

当前阶段不建议：

- 训练自己的甲骨文模型。
- 一开始收集百万级图片。
- 直接把所有扫描图提交到 GitHub。
- 只做图像相似检索，不做语境和出土关系。
- 把 AI Agent 输出直接写成正式释读结论。
- 一开始建立过重的 Web 平台。
- 一开始引入太多数据库系统。

## 17. 本草案的建议结论

推荐先采用：

```text
文件系统 source of truth
+ YAML/CSV/JSONL 结构化数据
+ 每 100 个甲骨字一个 bucket
+ 本系统稳定 ID + 外部来源 ID
+ PostgreSQL 作为后续查询数据库
+ graph edges 作为第一版知识图谱表达
+ AI Agent evidence pack 作为工具调用和大模型推理入口
```

下一步不是立即实施，而是先确认第 14 节的关键问题。确认后再创建正式目录、schema、样例数据和校验工具。
