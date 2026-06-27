# obs-unk-008571 单字考古文字上下文档案

本文件是单字对象目录内的人类可读上下文档案。它把已经存在的图片入口、来源路线、图边线索和待查问题集中到同一目录，供甲骨文学、考古学和人类研究者继续核查。

This dossier is a human-readable context entrance for the same object
directory. JSON and CSV files remain support tools for search, tracing,
comparison, and audit.

边界提示：本文件只整理预处理阶段证据路线，不是释读结论，不是构件归属结论，不是卜辞身份确认，也不是后世字形对应结论。

## 1. 对象身份与复核状态

- 项目 ID: `obs-unk-008571`
- 首选外部 ID: `hust-obc-und-YH-008571`
- 来源 ID: `src-hust-obc`
- packet 文件: `01_undeciphered-candidate-packet.json`
- 记录类型: `oracle_character_undeciphered_candidate_packet`
- 释读状态: `undeciphered_dataset_candidate_not_accepted_character`
- 复核状态: `reviewed_metadata_only`
- 权利状态: `source_marked_risk_noted`

## 2. 字形图片与观察入口

- 图像索引: `02_visual-source-index.csv`
- 图像页: `04_visual-gallery.md`
- 索引行数: `1`
- 来源图像路线数: `1`
- 本地复核图像数: `1`
- 首个来源图像名: `H_？_60C10_0.png`
- 首个本地图像名: `001_asset-010162_hust-obc-und-YH-008571_glyph.jpg`
- 图像权利状态: `source_marked_risk_noted`
- 图像复核状态: `needs_human_visual_review`

观察记录应从实物图像、拓片或照片路线开始；每条笔画、残缺、疑似描摹差异或不确定痕迹都需要绑定到具体图像或来源行。

## 3. 异体、近形与构件线索

- 异体路线: 待查：需连接已复核的异体、同版异写或来源分组记录
- 近形路线: 待查：需核对近形字、误分组和图像相似路线
- 构件线索: 待查：只可记录候选构件路线，不能写成构件归属
- 当前图边数: `1`
- 图边类型: CHARACTER_HAS_LOCAL_GLYPH_ASSET_CANDIDATE

## 4. 卜辞、图版与著录路线

- 卜辞出现: 待查：需核对卜辞编号、全文或 OCR、上下文和字位
- 图版与页码: 待查：需核对图版号、页码、著录来源和影像路线
- 合集或旧著录号: 待查：需核对合集号、旧著录号和目录互证记录
- 现有 route 文件: 待查：需核对对象目录内索引、来源路线或统计图边记录
- 图边 route 文件: 待查：需核对对象目录内索引、来源路线或统计图边记录

### Graph Evidence Routes

These graph rows are evidence routes for human review. They do not confirm a
reading, component assignment, inscription identity, or later-script
correspondence.

#### Graph Evidence Route 1

- edge type: `CHARACTER_HAS_LOCAL_GLYPH_ASSET_CANDIDATE`
- target node: `asset-010162`
- graph file: `009_character-asset-graph-edges.jsonl`
- review status: `needs_human_visual_review`
- source ids: src-hust-obc
- route files: 待查：需核对对象目录内索引、来源路线或统计图边记录
- evidence note: Local visual asset edge from asset source registry; the
  linked glyph image is a preparation-stage candidate and not decipherment
  evidence, not a confirmed glyph identity, and not a component conclusion.

## 5. 出土地、馆藏、时期与组类

- 出土地: 待查：需从来源著录、馆藏对象或考古批次记录追溯
- 馆藏: 待查：需核对馆藏号、对象记录和公开数据库路线
- 时期与组类: 待查：需记录来源中的分期、组类和批次，不作新判断
- 来源包: `large-src-000001`
- 下载或访问记录: dl-hust-obc-figshare-raw
- 来源 metadata: 待查：需核对对象目录内索引、来源路线或统计图边记录

## 6. 来源证据、权利与风险

- 来源追溯: 待查：需核对对象目录内索引、来源路线或统计图边记录
- checksum 与 manifest: 待查：需打开来源登记、下载日志和来源包清单
- 权利风险: `Figshare package metadata reports CC BY 4.0; Scientific Data
  article page uses CC BY-NC-ND 4.0. Raw package is 607933810 bytes and must
  not be committed to regular Git.`
- 公开提交边界: 元数据和小型派生图像需保留权利状态与风险提示

## 7. 释读史、争议与后世字形

Dataset labels below are not an accepted reading, not the glyph itself, and
not a decipherment conclusion.

- 来源标签状态: 待查：需核对对象 packet、来源路线或图边记录
- 来源标签文字: 待查：需核对对象 packet、来源路线或图边记录
- 来源标签 codepoint: 待查：需核对对象 packet、来源路线或图边记录
- 跨来源状态: 待查：需核对对象目录内索引、来源路线或统计图边记录
- 后世字形路线: 待查：金文、小篆、今字路线只能作为候选线索
- 释读史与争议: 待查：需记录提出者、文献来源和不同意见

## 8. 具体待查问题

- 需要核对哪些卜辞、图版、著录号或合集号？
- 哪些全文、OCR 或图版影像能补足该字所在上下文？
- 哪些字形观察能绑定到具体图像、拓片、照片或来源行？
- 哪些异体、近形或构件候选仍只是复核路线？
- 哪些馆藏、出土地、时期、组类或批次记录与本对象有关？
- 哪些文献讨论了释读史、提出者、不同意见或争议？
- 哪些金文、小篆、今字或字形演化路线仍只是候选？
- 需要打开哪些来源、checksum、manifest 或权利记录？

## 9. 本目录应先打开的文件

- `README.md`
- `04_visual-gallery.md`
- `05_human-research-dossier.md`
- `06_human-review-sheet.md`
- `08_character-context-evidence-dossier.md`
- `01_*packet.json`
- `02_visual-source-index.csv`
- `07_research-dossier-index.json`
- `09_character-context-evidence-index.json`

## 10. 复核边界

本档案记录可打开、可追溯、可继续核查的资料路线。任何读音、今字、构件、卜辞身份或演化对应，都必须在正式研究阶段另行人工复核后才能写成学术说明。
