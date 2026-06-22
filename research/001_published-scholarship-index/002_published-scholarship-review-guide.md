# Published Scholarship Review Guide / 已发表研究复核指南

English:
Use this guide before rewriting any bibliography item, paper note, database
description, web page note, or catalog note into `research/`. It is a human
review checklist for preprocessing only. It does not approve a reading,
component assignment, inscription identity, correspondence, or rights decision.

简体中文：
把任何书目条目、论文笔记、数据库说明、网页记录或著录说明改写进入
`research/` 前，先用本指南复核。这里是预处理阶段的人类复核清单，
不是释读批准、构件归属、卜辞身份、字形对应或权利决定。

## Review Order / 复核顺序

1. Open the source object directory under `corpus/006_research-sources-and-
   bibliography/001_source-objects/`.
2. Read `README.md`, `06_human-source-review-sheet.md`, and
   `07_material-access-index.md` before any CSV, JSON, or graph edge.
3. Check the source register, download log, checksum, package manifest,
   field map, metadata profile, rights status, risk note, and review status.
4. Compare any user or AI draft under `doc/public/user_research/` with the
   source object and the source register before promotion.
5. Record only sourced, reviewed bibliographic facts in `research/`.
6. Leave unresolved material as concrete next checks.

中文复核顺序：

1. 先打开 `corpus/006_research-sources-and-bibliography/001_source-
   objects/` 下的具体来源对象目录。
2. 先读 `README.md`、`06_human-source-review-sheet.md` 和
   `07_material-access-index.md`，再读 CSV、JSON 或图边。
3. 核对来源登记、下载记录、checksum、manifest、字段映射、
   metadata profile、权利状态、风险提示和复核状态。
4. `doc/public/user_research/` 下的用户或 AI 草稿，必须先和来源对象、
   来源登记互核，才能改写进入 `research/`。
5. `research/` 只记录有来源、已复核的书目信息。
6. 未解决内容写成具体下一步待查问题。

## Required Content / 必须记录内容

Each published-scholarship or bibliography note should preserve these items
when they are known:

- bibliographic identity: author, title, venue, year, URL, catalog number,
  database name, page, plate, or object record;
- source trail: source object id, source register row, download or access
  route, checksum, file size, manifest, and derived path;
- scope: which corpus area, object type, inscription, glyph, component,
  period, batch, or later-script route the source can support;
- evidence level: primary object record, catalog, database export, peer
  reviewed paper, book, web note, OCR text, or unreviewed draft;
- citation relation: cites, derives from, summarizes, disputes, or only
  routes to another record;
- reading process status: whether a decipherment or interpretation process is
  merely reported, needs checking, disputed, or out of scope;
- proposer and disagreement: who proposed the claim, who disagreed, and where
  the dispute is recorded;
- review status: reviewed source fact, candidate route, source record only,
  dispute pending, rights pending, or next check pending.

中文记录项：

- 书目身份：作者、题名、刊物或出版项、年份、URL、著录号、数据库名、
  页码、图版号或馆藏对象记录。
- 来源链：source object id、来源登记行、访问或下载路线、checksum、
  文件大小、manifest 和派生路径。
- 适用范围：该资料能支持哪个语料区、对象类型、卜辞、字形、构件、
  时期、批次或后世字形路线。
- 证据等级：实物记录、著录、数据库导出、同行评议论文、图书、网页
  说明、OCR 文本或未复核草稿。
- 引用关系：引用、派生、摘要、争议，或仅指向另一条记录。
- 释读过程状态：某项释读或解释过程只是被报道、待查、有争议，还是
  不属于本次复核范围。
- 提出者和争议：谁提出，谁不同意，争议记录在哪里。
- 复核状态：已复核来源事实、候选路线、仅来源记录、争议待查、权利
  待查或下一步待查。

## Concrete Next Checks / 具体待查问题

Use questions like these instead of empty placeholders:

- Which source object and register row prove this bibliography item?
- Which page, plate, URL, catalog number, or object record locates it?
- Which checksum, file size, manifest, or field map supports the route?
- Which corpus object can this source actually support?
- What evidence level is justified by the opened source?
- Who is the proposer, and where is the proposal recorded?
- Which disagreement or dispute is documented, and where?
- Which user or AI draft must stay outside `research/` until reviewed?
- What exact source must be opened before any note can be promoted?

中文问题示例：

- 哪个 source object 和登记行能证明这条书目？
- 哪个页码、图版号、URL、著录号或馆藏记录能定位资料？
- 哪个 checksum、文件大小、manifest 或字段映射支持该路线？
- 这条资料实际能支持哪个语料对象？
- 已打开来源能支持什么证据等级？
- 提出者是谁，提出记录在哪里？
- 哪个不同意见或争议已有文献记录，位置在哪里？
- 哪条用户或 AI 草稿在复核前必须留在 `doc/public/user_research/`？
- 在提升为研究笔记前，下一步必须打开哪一个具体来源？

## Boundary / 边界

This guide is not scholarship. A note may move into `research/` only after a
human reviewer rewrites it from opened source evidence and marks unresolved
items as pending. Source metadata, graph edges, AI drafts, OCR text, and CSV
rows must not be written as confirmed readings.

本指南不是学术结论。只有人工复核者打开来源证据并改写后，笔记才可进入
`research/`；未解决内容必须标为待查。来源 metadata、图边、AI 草稿、
OCR 文本和 CSV 行不得写成已确认释读。
