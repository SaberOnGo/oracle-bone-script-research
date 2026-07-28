# Authoritative Source Expansion Notes / 权威来源扩展说明

## English

This note records the second source-expansion pass for the first-stage corpus.
The selection rule remains strict: adopt institutional, museum, library,
professional database, and peer-reviewed research sources. Do not mix in
general news, entertainment pages, unsourced popular articles, or casual
hobbyist material.

Reviewed and adopted in this pass:

1. `src-obid-ancientbooks`: professional discovery for inscription browsing,
   transcription search, original-text search, and oracle dictionary lookup.
   Commercial hosting means access and redistribution terms need caution.
2. `src-tsinghua-oracle-bones`: official university-library collection
   reference for holdings scale, custody, and provenance.
3. `src-cambridge-hopkins`: collection finding list and crosswalk for Cambridge,
   Chalfant, Heji, and `Yingguo suo cang jiagu ji` identifiers.
4. `src-british-museum-oracle-bone`: museum-object metadata pattern for
   registration number, period, material, acquisition, and department.
5. `src-smithsonian-nmaa-oracle-bone`: public-domain sample with accession,
   EDAN, provenance, IIIF access, and a CC0 rights statement.

Reviewed AI/research datasets:

1. `src-hust-obc`: metadata-level review completed. It reports 1,588
   deciphered and 9,411 undeciphered classes, but remains a large-source
   candidate rather than primary paleographic authority.
2. `src-obimd`: metadata-level review completed. Preserve the difference
   between the Hugging Face CC-BY statement and narrower GitHub wording.
3. `src-evobc`: candidate evolution dataset; source texts, websites, and
   image rights need separate review before raw import.
4. `src-gbedobc`: graph/evolution experiment source, not primary authority.
5. `src-oracle-mnist`: benchmark-only source because its ten classes are
   too narrow for corpus construction.

Explicit exclusions and caution:

- General news, blog summaries, and tool-navigation pages were not adopted.
- `GuoXueDaShi` remains excluded as a formal primary source. A peer-reviewed
  dataset split derived from it must be marked dataset-internal evidence.
- The National Library of China `甲骨世界` source remains a candidate until
  a stable official endpoint is confirmed. Third-party summaries are not
  source authority.

## 简体中文

本说明记录第一阶段语料的第二轮来源扩展。筛选规则仍然严格：采用机构、博物馆、
图书馆、专业数据库和同行评审研究来源；一般新闻、娱乐网站、无来源科普文章和
未经审计的民间整理，不进入正式语料。

本轮已评估并采纳的来源：

1. `src-obid-ancientbooks`：用于卜辞浏览、释文检索、原文检索和甲骨字典查询的
   专业发现源。因托管在商业平台，访问和再分发条款仍需谨慎。
2. `src-tsinghua-oracle-bones`：大学图书馆官方馆藏来源，用于记录馆藏规模、
   保管机构和来源脉络。
3. `src-cambridge-hopkins`：馆藏清单和外部编号 crosswalk，可关联 Cambridge、
   Chalfant、合集和《英国所藏甲骨集》编号。
4. `src-british-museum-oracle-bone`：博物馆单件藏品记录范式，可参考登记号、
   时期、材质、入藏和部门字段。
5. `src-smithsonian-nmaa-oracle-bone`：公版样例，含 accession、EDAN、来源说明、
   IIIF 入口和 CC0 权利声明。

本轮已评估的 AI/研究数据集：

1. `src-hust-obc`：已完成 metadata 层面复核，报告 1,588 个已释类别和 9,411 个
   未释类别，但仍是大型来源候选，不是文字学一手权威。
2. `src-obimd`：已完成 metadata 层面复核，必须区分 Hugging Face 的 CC-BY 声明
   与 GitHub README 中更窄的学术使用措辞。
3. `src-evobc`：字形演化候选数据集；原始文本、来源网站和图像权利仍需单独复核。
4. `src-gbedobc`：图结构和字形演化实验来源，不作为一手语料权威。
5. `src-oracle-mnist`：仅作 benchmark，因为只有十个类别，不适合构建大语料。

明确排除和注意事项：

- 搜索得到的一般新闻、博客汇总和工具导航页未采纳为正式来源。
- `GuoXueDaShi` 当前不作为正式一手来源；若同行评审数据集含其派生拆分，必须标为
  数据集内部证据，不能提升为一手来源。
- 中国国家图书馆的 `甲骨世界` 在确认稳定官方入口前仍列为候选来源。第三方介绍
  只能作为范围记录，不能成为来源权威。
