# Bronze, Seal, And Modern Correspondences / 金文、小篆与今字对应

English:
This directory stores preprocessing materials for cross-period character-form
comparison. It covers oracle bone script, bronze script, seal script,
later-script labels, modern codepoint routes, and EVOBC
evolution/correspondence candidate records.

简体中文：
本目录保存跨时期字形比较的预处理资料，范围包括甲骨文、金文、小篆、
后续文字阶段标签、今字 codepoint 路线，以及 EVOBC 字形演化和对应
候选记录。

English:
These files are evidence routes for later human review. They are not accepted
paleographic correspondences, not evolution-chain conclusions, not modern
character identity confirmations, and not decipherment conclusions.

简体中文：
这些文件只是供后续人工复核的证据路线。它们不是已接受的古文字对应，
不是字形演化链结论，不是今字身份确认，也不是释读结论。

## Current Registers / 当前登记表

English:

- `000_evolution-registers/001_evobc-evolution-category-staging.csv`
  stores 13,714 EVOBC dataset category rows.
- `000_evolution-registers/002_evobc-era-source-codebook-staging.csv`
  stores EVOBC era and source codebook rows.
- `001_*_obs-evo-cand-bucket_evolution-candidates/` stores object-local
  EVOBC evolution/correspondence candidate directories.

简体中文：

- `000_evolution-registers/001_evobc-evolution-category-staging.csv`
  保存 13,714 条 EVOBC 数据集类别行。
- `000_evolution-registers/002_evobc-era-source-codebook-staging.csv`
  保存 EVOBC 时期和来源代码表行。
- `001_*_obs-evo-cand-bucket_evolution-candidates/` 保存对象内 EVOBC
  字形演化和对应候选目录。

## Human Research Entry Order / 人工研究入口顺序

English:
Researchers should inspect each `obs-evo-cand-*` directory in this order:

1. Read `README.md` for candidate scope and review status.
2. Open `02_evolution-source-index.csv` to identify the dataset route.
3. Check `03_era-source-code-index.csv` for era and source-code context.
4. Read `05_image-reference-route-gallery.md` for image-reference routes.
5. Fill `04_human-review-sheet.md` before any correspondence claim.
6. Compare against stronger sources before promoting any relationship.

简体中文：
研究者查看每个 `obs-evo-cand-*` 目录时，应按以下顺序进行：

1. 先读 `README.md`，确认候选范围和复核状态。
2. 打开 `02_evolution-source-index.csv`，定位数据集来源路线。
3. 检查 `03_era-source-code-index.csv` 的时期和来源代码语境。
4. 阅读 `05_image-reference-route-gallery.md` 的图像引用路线。
5. 在提出任何对应关系前，先填写 `04_human-review-sheet.md`。
6. 关系提升前，必须与更强来源证据交叉复核。

## Object-Local Materials / 对象内资料

English:
Each concrete candidate directory should keep human-readable review material
and AI-readable support files together. The JSON and CSV files help search,
trace, compare, and audit the human dossier, but they do not replace it.

简体中文：
每个具体候选目录都应同时保存人类可读复核资料和 AI 可读辅助文件。
JSON 与 CSV 只用于检索、追溯、比较和审计人类档案，不能替代档案。

Expected object-local files:

- `README.md`: human overview, source status, and boundary.
- `01_candidate-evolution-packet.json`: AI-readable candidate packet.
- `02_evolution-source-index.csv`: EVOBC source route table.
- `03_era-source-code-index.csv`: era and source code table.
- `04_human-review-sheet.md`: manual review sheet.
- `05_image-reference-route-gallery.md`: readable image route gallery.
- `06_image-reference-route-index.csv`: image-reference route table.

## Dossier Questions / 档案待查内容

English:
A complete evolution/correspondence dossier should collect these materials:

- source dataset row, EVOBC category ID, and project-local candidate ID;
- image route, source code, era label, and source package evidence;
- oracle-bone, bronze script, seal script, and later-script comparanda;
- modern codepoint route and whether it is only a dataset clue;
- related oracle-character, component, variant, and similar-form routes;
- bibliography, database, or web source route for later verification;
- review status, disputed points, and the next source to check.

简体中文：
完整的字形演化和对应候选档案应补齐以下资料：

- 来源数据集行、EVOBC 类别 ID 和本项目候选 ID；
- 图像路线、来源代码、时期标签和来源包证据；
- 甲骨文、金文、小篆和后续文字阶段的可比材料；
- 今字 codepoint 路线，以及它是否只是数据集线索；
- 相关甲骨单字、构件、异体和近形路线；
- 供后续复核的书目、数据库或网页来源路线；
- 复核状态、争议点和下一步具体待查来源。

## Concrete Questions To Check / 具体待查问题

English:

- Which EVOBC row and source code created this candidate route?
- Does the candidate have visible image evidence, or only a dataset label?
- Which bronze script, seal script, or later-script forms should be checked?
- Which oracle-character or component dossier should be opened next?
- Is the modern codepoint route a comparison clue or an unreviewed identity?
- Which source package, bibliography item, or webpage should verify it?
- What evidence is missing before any formal correspondence claim?

简体中文：

- 这条候选路线来自哪条 EVOBC 行和哪个来源代码？
- 该候选是否有可见图像证据，还是只有数据集标签？
- 下一步应核查哪些金文、小篆或后续文字阶段字形？
- 应打开哪个甲骨单字或构件档案继续比较？
- 今字 codepoint 路线是比较线索，还是未经复核的身份判断？
- 应由哪个来源包、文献项目或网页记录来验证它？
- 提出正式对应关系前，还缺少哪些证据？

## Research Boundary / 研究边界

English:
An EVOBC evolution/correspondence candidate is not a decipherment conclusion.
It is not an accepted paleographic correspondence, not an evolution-chain
assignment, and not a modern-character identity confirmation. Keep every
unreviewed item marked as candidate, source record, disputed, pending check,
or pending review.

简体中文：
EVOBC 字形演化和对应候选不是释读结论，不是已接受的古文字对应，
不是字形演化链归属，也不是今字身份确认。所有未经复核的项目都必须
标为候选、来源记录、争议、待查或待复核。
