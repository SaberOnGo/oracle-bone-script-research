# Excavation Sites, Periods, And Batches / 出土地点、时期与批次

English:
This directory stores preprocessing materials for collection provenance,
excavation context, findspot, period, batch, holding institution, and
collection object candidate review.

简体中文：
本目录保存馆藏出处、出土语境、出土地、时期、批次、馆藏机构和馆藏
对象候选的预处理资料。

English:
These records help researchers connect oracle-bone objects, inscriptions,
images, catalog rows, and source packages to their provenance routes. They
are review materials only, not object identity conclusions, not collection
ownership decisions, and not decipherment conclusions.

简体中文：
这些记录帮助研究者把甲骨实物、卜辞、图像、著录行和来源包连接到
出处路线。它们只是复核资料，不是实物身份结论，不是馆藏权属判断，
也不是释读结论。

## Current Registers / 当前登记表

English:

- `000_collection-registers/001_institutional-collection-provenance-staging.csv`
  stores institution-level provenance staging rows.
- `000_collection-registers/002_ihp-museum-oracle-bone-object-staging.csv`
  stores 52 IHP Museum official object-page staging rows.
- `001_public-domain-object-image-assets/` stores committed public-domain
  object images with source-marked metadata.
- `002_collection-object-candidates/` stores object-local collection object
  candidate directories.

简体中文：

- `000_collection-registers/001_institutional-collection-provenance-staging.csv`
  保存机构级馆藏出处暂存行。
- `000_collection-registers/002_ihp-museum-oracle-bone-object-staging.csv`
  保存 52 条史语所博物馆官方对象页暂存行。
- `001_public-domain-object-image-assets/` 保存带来源标注的公版对象图像。
- `002_collection-object-candidates/` 保存对象内馆藏对象候选目录。

## Human Research Entry Order / 人工研究入口顺序

English:
Researchers should inspect collection and provenance materials in this order:

1. Read this README to understand the provenance boundary.
2. Open a concrete `coll-obj-cand-*` directory under the candidate area.
3. Read the object-local README before the AI packet.
4. Check source indexes, visual galleries, and thumbnail route notes.
5. Compare institution, shelfmark, findspot, period, and batch evidence.
6. Fill the human review sheet before recording any reviewed outcome.

简体中文：
研究者查看馆藏和出处资料时，应按以下顺序进行：

1. 先读本 README，确认出处资料边界。
2. 进入候选区下具体的 `coll-obj-cand-*` 目录。
3. 先读对象内 README，再读 AI packet。
4. 检查来源索引、图像 gallery 和 thumbnail route 说明。
5. 核对机构、架藏号、出土地、时期和批次证据。
6. 写入任何复核结果前，先填写人工复核表。

## Object-Local Materials / 对象内资料

English:
Each collection object candidate directory should keep human-readable review
materials and AI-readable support files together. The structured files help
trace source routes, but the object-local human dossier remains primary.

简体中文：
每个馆藏对象候选目录都应同时保存人类可读复核资料和 AI 可读辅助文件。
结构化文件用于追溯来源路线，但对象内人类档案仍是主体。

Expected object-local files:

- `README.md`: human overview, source status, and review boundary.
- `01_collection-object-packet.json`: AI-readable candidate packet.
- `02_collection-source-index.csv`: collection source route table.
- `03_visual-asset-or-thumbnail-route-index.csv`: image or thumbnail route.
- `04_visual-gallery.md`: readable visual or route gallery.
- `05_human-review-sheet.md`: manual review sheet.

## Dossier Questions / 档案待查内容

English:
A complete provenance dossier should collect these review materials:

- holding institution, collection name, object ID, shelfmark, and URL;
- excavation site, findspot, pit, period, batch, and source wording;
- catalog source, page or object record, image path, and thumbnail route;
- rights status, public-domain evidence, risk note, and commit decision;
- linked inscription, oracle-character, plate, bibliography, and source rows;
- object identity uncertainty, disputed provenance, and next source to check.

简体中文：
完整出处档案应补齐以下复核资料：

- 馆藏机构、馆藏名称、对象 ID、架藏号和 URL；
- 出土地点、出土地、坑位、时期、批次和来源原文；
- 著录来源、页码或对象记录、图像路径和缩略图路线；
- 权利状态、公版证据、风险提示和提交决策；
- 关联卜辞、甲骨单字、图版、书目和来源行；
- 实物身份不确定点、出处争议和下一步具体待查来源。

## Concrete Questions To Check / 具体待查问题

English:

- Which holding institution and source page identify this object?
- Which object record or collection shelfmark locates it?
- Is the image public-domain, metadata-only, or pending rights review?
- Which findspot, period, batch, or excavation context is actually stated?
- Which inscription, plate, or oracle-character dossier should link to it?
- Is the thumbnail route enough for review, or is a stronger source needed?
- What source must be checked before any object identity conclusion?

简体中文：

- 哪个馆藏机构和来源页面能定位这个对象？
- 哪条对象记录或馆藏架藏号能定位它？
- 图像是公版、仅 metadata，还是仍待权利复核？
- 来源实际写明了哪些出土地、时期、批次或出土语境？
- 哪个卜辞、图版或甲骨单字档案应与它建立路线？
- thumbnail route 是否足以复核，还是需要更强来源？
- 提出任何实物身份结论前，还必须核查哪个来源？

## Research Boundary / 研究边界

English:
A collection object candidate is not a decipherment conclusion.
It is not an object identity conclusion. It is not an ownership decision or
a confirmed findspot, period, or batch assignment. Keep uncertain facts
marked as candidate, source record, disputed, pending check, or pending
review.

简体中文：
馆藏对象候选不是释读结论，不是实物身份结论，不是权属判断，也不是已
确认的出土地、时期或批次归属。不确定事实必须标为候选、来源记录、
争议、待查或待复核。
