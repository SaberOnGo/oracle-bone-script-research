# Oracle Characters / 甲骨单字

English:
This area stores oracle-character and undeciphered-character candidate
folders. Each concrete object folder should work like a small archaeological
and paleographic dossier, not like a packet of images plus JSON only.

简体中文：
本区保存甲骨单字和未释字候选目录。每个具体对象目录都应像一个
小型考古和文字学档案夹，而不是只有图片和 JSON 的资料包。

## Current Stage / 当前阶段

English:
The current stage is preprocessing before formal oracle-bone research.
Object-local materials gather glyph image routes, source evidence, visual
review pages, human research dossier files, review sheets, and AI support
indexes. They are preparation records, not accepted scholarship.

简体中文：
当前仍处在正式甲骨文研究开始前的资料整理与预处理阶段。对象内
资料汇集字形图片路线、来源证据、图像复核页、人类研究档案、
复核表和 AI 辅助索引。它们是准备记录，不是已接受的学术结论。

## Human Research Entry Order / 人工研究入口顺序

1. Open the concrete `obs-char-*` or `obs-unk-*` object directory.
2. Read the object-local `README.md` before opening the JSON packet.
3. Inspect `04_visual-gallery.md` and local glyph image routes.
4. Read `05_human-research-dossier.md` for dossier coverage.
5. Use `06_human-review-sheet.md` to record pending human checks.
6. Use `07_research-dossier-index.json` only as an AI support index.
7. Follow source IDs back to `project_registry/` and source objects.
8. Keep every unchecked reading, component, or correspondence as candidate.

人工阅读时，先进入具体 `obs-char-*` 或 `obs-unk-*` 对象目录，
先读对象内 `README.md`，再看 JSON packet。随后检查
`04_visual-gallery.md`、字形图片路线、`05_human-research-dossier.md`
和 `06_human-review-sheet.md`。`07_research-dossier-index.json`
只作为 AI 辅助索引使用，不能替代人类档案。

## Dossier Contents / 档案内容

English:
A usable character folder should expose or explicitly mark these items:

- glyph image and visual source route;
- glyph observation and visual review status;
- variant, similar-form, and component candidate routes;
- inscription context and full-text or OCR route;
- plate, catalog number, Heji or OBM route, and page reference;
- findspot, collection, period, group, and batch route;
- source evidence, rights status, checksum, and risk note;
- later-script, bronze, seal, and modern-form candidate routes;
- decipherment history, proposer, disagreement, and bibliography route;
- concrete missing questions and next sources to check.

简体中文：
可用的单字目录应展示或明确标出下列项目：

- 字形图片和图像来源路线；
- 字形观察和图像复核状态；
- 异体、近形和构件候选路线；
- 所在卜辞、卜辞上下文、全文或 OCR 路线；
- 图版号、著录号、合集或 OBM 路线、页码线索；
- 出土地、馆藏、时期、组类和批次路线；
- 来源证据、权利状态、checksum 和风险提示；
- 金文、小篆、后世字形和今字候选路线；
- 释读史、提出者、不同意见和文献路线；
- 具体缺失项和下一步待查来源。

## Existing Local Materials / 已有对象内资料

English:
Prepared HUST-OBC `obs-char-*` and `obs-unk-*` folders keep human-readable
and AI-readable materials together in the same object directory. The common
files include:

- `README.md`;
- `01_*packet.json`;
- `02_visual-source-index.csv`;
- `03_visual-assets/`;
- `04_visual-gallery.md`;
- `05_human-research-dossier.md`;
- `06_human-review-sheet.md`;
- `07_research-dossier-index.json`.

简体中文：
已准备的 HUST-OBC `obs-char-*` 和 `obs-unk-*` 目录，会把人类可读
资料和 AI 可读辅助资料放在同一对象目录内。常见文件包括
README、候选 packet、图像来源索引、图像目录、图像 gallery、
人类研究档案、人工复核表和 AI 辅助索引。

## Concrete Questions To Check / 具体待查问题

- Which character folder has an image but lacks a human research dossier?
- 哪个单字目录有图片，却还缺人类研究档案？
- Which glyph image lacks source evidence, checksum, rights status, or risk?
- 哪张字形图片缺来源证据、checksum、权利状态或风险提示？
- Which candidate lacks glyph observation, variant, or similar-form notes?
- 哪个候选还缺字形观察、异体或近形说明？
- Which candidate lacks inscription context, plate number, or catalog route?
- 哪个候选还缺卜辞上下文、图版号或著录路线？
- Which candidate lacks findspot, collection, period, group, or batch route?
- 哪个候选还缺出土地、馆藏、时期、组类或批次路线？
- Which component, later-script, or modern-form route is only a candidate?
- 哪条构件、后世字形或今字路线仍只是候选线索？
- Which bibliography item records decipherment history or disagreement?
- 哪条文献记录涉及释读史、提出者或不同意见？
- Which JSON or graph edge is only an index and not a research conclusion?
- 哪个 JSON 或图边只是索引，不能当成人类研究结论？

## Research Boundary / 研究边界

English:
Dataset labels, graph edges, codepoint matches, component routes,
later-script routes, and object IDs are routing evidence only. They are not
accepted readings, component assignments, inscription identities,
correspondence claims, or a decipherment conclusion. In short, every
unchecked route is not a decipherment conclusion.

简体中文：
数据集标签、图边、codepoint 匹配、构件路线、后世字形路线和对象
ID 都只是检索与复核线索。它们不是已接受释读、构件归属、卜辞
身份、字形对应主张，也不是释读结论。

## 2026-11-02 折叠 / Collapse

按架构重置第 2 步，16 个码位对照分桶（`obs-xwalk-cand-*`）已折叠回
`000_character-registers/011_hust-obimd-evobc-codepoint-crosswalk-staging.csv`，
每个 ID 对应其中一行。单字与未释字目录将在下一步合并为一份档案。旧目录
可从提交 `4a0fb8acf25` 恢复。

The 16 codepoint-crosswalk buckets were collapsed into register `011`.
Character directories will be merged into single dossiers in the next step.

## 2026-11-02 单字档案合并 / Character Dossier Merge

简体中文：
按架构重置第 2b 步，10,986 个单字目录各自合并为一份人读档案
`README.md`、一份机读记录 `record.json` 和一个 `images/` 目录。档案章节
按研究者阅读顺序排列，只写有来源的内容，没有内容的章节直接省略。
档案标准见 `doc/project/007_architecture-reset-and-human-first-knowledge-base/`
`03_object-dossier-standard.md`。

另有 10 个目录含人工复核记录（多字例比较、证据门槛、史语所回执等），
暂按原格式保留，将在第 5 步深度试点中人工整理：
`obs-char-000101`、`000209`、`000412`、`000621`、`000791`、`000852`、
`000963`，以及 `obs-unk-000001`、`000002`、`005708`。

合并时统计到的事实（均为数据集层面，不是释读结论）：

| 项目 | 数量 |
| --- | --- |
| 已释字候选档案 | 1,581 |
| 未释字候选档案 | 9,405 |
| 来源只有 1 张样本的未释类（孤例） | 6,207 |
| 来源样本 20 张以上的未释类 | 2,331 |
| 文件名带合集号线索的档案 | 725 |
| 文件名带旧著录线索的档案 | 1,054 |
| 只有算法像素画像、尚无人工观察的档案 | 4,405 |
| 数据集标签落在 Unicode 部首区的已释类 | 8 |

English summary:
10,986 character directories were merged into one dossier each. Ten
directories with manual review records stay in their former layout for step
5. About two thirds of the HUST undeciphered classes have a single sample,
so their study will depend on inscription context more than on form
comparison.
