# Graphemic Components / 字形构件

English:
This directory is the working corpus for graphemic component records,
component variants, and character-component relationships.

简体中文：
本目录保存字形构件记录、构件异体、以及单字与构件关系的预处理资料。

English:
The current OBIMD rows are component candidate materials. They preserve
source hierarchy, glyph-codepoint evidence, local images, and review routes,
but they are not confirmed component forms or component assignments.

简体中文：
当前 OBIMD 行是构件候选资料。它们保存来源层级、glyph-codepoint
证据、本地图像和复核路线，但不是已确认的构件字形或构件归属。

## Current Registers / 当前登记表

English:

- `000_component-registers/001_all-components-index.csv` stores accepted
  project component records.
- `000_component-registers/002_obimd-subcharacter-main-staging.csv` stores
  OBIMD subcharacter to main-character staging rows.
- `000_component-registers/003_obimd-subcharacter-glyph-staging.csv` stores
  OBIMD subcharacter to glyph-codepoint staging rows.

简体中文：

- `000_component-registers/001_all-components-index.csv` 保存项目构件记录。
- `000_component-registers/002_obimd-subcharacter-main-staging.csv` 保存
  OBIMD subcharacter 到 main-character 的暂存行。
- `000_component-registers/003_obimd-subcharacter-glyph-staging.csv` 保存
  OBIMD subcharacter 到 glyph-codepoint 的暂存行。

## Human Research Entry Order / 人工研究入口顺序

English:
Researchers should inspect each `obs-comp-cand-*` directory in this order:

1. Read `README.md` for the candidate scope and review status.
2. Inspect `05_component-visual-assets/` for local source-marked images.
3. Compare `04_glyph-codepoint-gallery.md` with the visual gallery.
4. Check `09_component-visual-route-index.csv` for source route evidence.
5. Fill `08_human-visual-review-sheet.md` during manual review.
6. Promote relationships only after source, image, and context review.

简体中文：
研究者查看每个 `obs-comp-cand-*` 目录时，应按以下顺序进行：

1. 先读 `README.md`，确认候选范围和复核状态。
2. 查看 `05_component-visual-assets/` 中的本地来源标注图像。
3. 对照 `04_glyph-codepoint-gallery.md` 与 visual gallery。
4. 检查 `09_component-visual-route-index.csv` 的来源路线证据。
5. 人工复核时填写 `08_human-visual-review-sheet.md`。
6. 来源、图像、上下文均复核后，才可提升为正式关系。

## Object-Local Materials / 对象内资料

English:
Each candidate directory should keep human-readable and AI-readable support
files together, so a scholar can study the object without opening a parallel
human directory.

简体中文：
每个候选目录都应同时保存人类可读资料和 AI 可读辅助资料。研究者打开
对象目录后，应能直接复核该构件候选，而不是只看到索引文件。

Expected object-local files:

- `README.md`: human overview, source status, and review boundary.
- `01_candidate-component-packet.json`: structured support packet for the
  human component dossier.
- `02_component-source-index.csv`: source table and package route.
- `03_glyph-codepoint-index.csv`: glyph-codepoint relationship table.
- `04_glyph-codepoint-gallery.md`: readable glyph-codepoint gallery.
- `05_component-visual-assets/`: local image derivatives.
- `06_component-visual-index.csv`: image asset index.
- `07_component-visual-gallery.md`: readable visual gallery.
- `08_human-visual-review-sheet.md`: manual review sheet.
- `09_component-visual-route-index.csv`: component visual route table.
- `10_component-visual-route-gallery.md`: readable route gallery.

## Dossier Questions / 档案待查内容

English:
A complete component dossier should collect the following review evidence:

- visual form, stroke grouping, and uncertain visual details;
- source PNG path, source zip member, checksum, size, and rights status;
- glyph-codepoint route, source package record, and extraction note;
- candidate relationship to oracle characters, variants, and similar-form
  groups;
- inscription or plate evidence where the candidate occurs in context;
- bibliographic, database, or webpage routes used for later verification;
- current review status, reviewer notes, and concrete next source to check.

简体中文：
完整构件档案应补齐以下复核证据：

- 字形观察、笔画组合、以及不确定视觉细节；
- 来源 PNG 路径、来源 zip member、checksum、大小和权利状态；
- glyph-codepoint 路线、来源包记录和抽取说明；
- 与甲骨单字、异体、近形组之间的候选关系；
- 候选构件出现在卜辞或图版上下文中的证据；
- 可供追溯的书目、数据库或网页路线；
- 当前复核状态、复核者记录、以及下一步具体待查来源。

## Concrete Questions To Check / 具体待查问题

English:

- Which OBIMD source package and zip member produced this visual asset?
- Does the checksum match the registered extraction manifest?
- Does the image show a reusable component shape, or only a cropped glyph?
- Which oracle-character directories cite this component candidate?
- Are related variant or similar-form links supported by visible evidence?
- Which inscription, plate, or catalog record should be checked next?
- Is the rights status suitable for committing the derived local image?

简体中文：

- 该视觉资产来自哪一个 OBIMD 来源包和 zip member？
- checksum 是否与已登记的抽取 manifest 一致？
- 图像显示的是可复用字形构件，还是只是一处截取字形？
- 哪些甲骨单字目录引用了这个构件候选？
- 异体或近形关系是否有可见图像证据支持？
- 下一步应核查哪条卜辞、图版或著录记录？
- 权利状态是否允许把该派生本地图像提交到仓库？

## Research Boundary / 研究边界

English:
These records are preprocessing evidence. A component candidate is
not a decipherment conclusion. It is not a confirmed component form or a
component assignment. It must remain marked as candidate, source record,
disputed, pending check, or pending review until human evidence review is
complete.

简体中文：
这些记录只是预处理证据。构件候选不是释读结论，不是已确认构件字形，
也不是已确认构件归属。人工证据复核完成前，必须标为候选、来源记录、
争议、待查或待复核。
