# Authoritative Source Expansion Notes

## English

This note records the second source-expansion pass for the first-stage corpus. The selection rule remains strict: adopt institutional, museum, library, professional database, and peer-reviewed research sources; do not mix in general news, entertainment pages, unsourced popular articles, or casual hobbyist material.

Reviewed and adopted in this pass:

1. `src-obid-ancientbooks`: useful as a professional discovery source for inscription browsing, transcription search, original-text search, and oracle dictionary lookup. It is not treated as unrestricted public data because it is hosted on a commercial platform and access/redistribution terms require caution.
2. `src-tsinghua-oracle-bones`: useful as an official university-library collection reference. It records the scale and provenance of Tsinghua University Library's oracle-bone holdings and helps map institutional custody history.
3. `src-cambridge-hopkins`: useful as a collection finding list and crosswalk. Its references to Cambridge University Library numbers, Chalfant, Heji, and `Yingguo suo cang jiagu ji` make it valuable for external ID mapping.
4. `src-british-museum-oracle-bone`: useful as a museum-object reference pattern. It is not corpus-scale, but it gives a clean example of museum number, registration number, period, material, acquisition, and department metadata.
5. `src-smithsonian-nmaa-oracle-bone`: useful as a public-domain sample source because the official object page provides accession/EDAN identifiers, provenance notes, IIIF access, and a CC0 rights statement.

Reviewed AI/research datasets:

1. `src-hust-obc`: now reviewed at the metadata level. It is important for the project's 1500+ deciphered and undeciphered-character goal because it reports 1,588 deciphered classes and 9,411 undeciphered classes. It remains a large-source candidate, not a primary paleographic authority.
2. `src-obimd`: now reviewed at the metadata level. It is important for inscription-level, character-level, sentence-level, and reading-order work. The rights note must preserve the difference between the Hugging Face CC-BY statement and narrower wording in the GitHub README.
3. `src-evobc`: added as a candidate evolution-chain dataset source. It is useful for later glyph-evolution experiments, but its source texts, source websites, and image rights need separate review before raw import.
4. `src-gbedobc`: reviewed as a graph/evolution experiment source, not as a primary corpus authority.
5. `src-oracle-mnist`: reviewed as a benchmark-only source because its ten classes are too narrow for corpus construction.

Explicit exclusions and caution:

- General news and blog summaries found during search were not adopted as formal corpus sources.
- `GuoXueDaShi` remains excluded as a formal primary source at this stage because the project policy rejects unaudited hobbyist or enthusiast collections. If a peer-reviewed dataset includes a GuoXueDaShi-derived split, that split must be marked as dataset-internal evidence, not as a primary source.
- The National Library of China `甲骨世界` source remains a candidate until a stable official endpoint is confirmed. Official NLC notes may be logged as evidence for scope, but third-party summaries must not become source authority.

## 简体中文

本说明记录第一阶段语料的第二轮来源扩展。筛选规则仍然严格：采纳机构、博物馆、图书馆、专业数据库和同行评审研究来源；一般新闻、娱乐网站、无来源科普文章和随意整理的民间材料不进入正式语料。

本轮已评审并采纳：

1. `src-obid-ancientbooks`：适合作为专业发现源，用于卜辞浏览、释文检索、原文检索和甲骨字典查询。但它托管在商业平台上，因此不视为无限制公开数据，访问与再分发权利需要保留风险提示。
2. `src-tsinghua-oracle-bones`：适合作为大学图书馆官方馆藏来源。它记录清华大学图书馆甲骨藏品规模和来源脉络，有助于建立机构馆藏史。
3. `src-cambridge-hopkins`：适合作为馆藏清单和外部编号 crosswalk。它把剑桥馆藏号、Chalfant、《合集》和《英国所藏甲骨集》等编号联系起来，对外部 ID 映射很有价值。
4. `src-british-museum-oracle-bone`：适合作为博物馆单件藏品记录范式。它不是大规模语料来源，但能提供博物馆号、登记号、时代、材质、入藏和部门等 metadata 示例。
5. `src-smithsonian-nmaa-oracle-bone`：适合作为公版样例来源，因为官方藏品页提供登录号、EDAN ID、来源说明、IIIF 入口和 CC0 权利声明。

本轮已评审的 AI/研究数据集：

1. `src-hust-obc`：已完成 metadata 层面的评审。它对本项目 1500+ 已释字和未释字目标很重要，因为其报告 1,588 个已释类别和 9,411 个未释类别。但它仍是大型来源候选，不是古文字学一手权威。
2. `src-obimd`：已完成 metadata 层面的评审。它对卜辞级、字符级、句级和阅读顺序资料很重要。权利说明必须保留 Hugging Face 的 CC-BY 说明与 GitHub README 中较窄学术用途措辞之间的差异。
3. `src-evobc`：新增为候选字形演化链数据集来源。它适合后续字形演化实验，但原始导入前必须分别评审来源文本、来源网站和图片权利。
4. `src-gbedobc`：作为图结构/字形演化实验来源评审通过，但不作为一手语料权威。
5. `src-oracle-mnist`：仅作为 benchmark 来源评审通过，因为它只有十个类别，不适合构建大规模研究语料。

明确排除和注意：

- 搜索过程中出现的一般新闻、博客汇总和工具导航页未作为正式语料来源采纳。
- `GuoXueDaShi` 在本阶段仍不作为正式一手来源采纳，因为项目政策排除未经审计的爱好者/民间整理集合。如果同行评审数据集中包含来自 GuoXueDaShi 的拆分，该拆分只能标记为数据集内部证据，不能上升为一手来源。
- 中国国家图书馆 `甲骨世界` 来源在确认稳定官方入口前仍保留为候选来源。国图官方说明可作为范围证据登记，但第三方介绍不能成为来源权威。
