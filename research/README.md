# Published Scholarship Notes / 已发表学术研究笔记

English:
This directory is for existing scholarship: published papers, monographs,
catalogs, decipherment history, bibliographic notes, scholarly arguments,
and carefully sourced summaries. It is not for user or AI Agent drafts.

简体中文：
本目录用于已有学术研究：已发表论文、专著、著录、释读史、书目笔记、
学术论证和有明确来源的严谨摘要。用户或 AI Agent 草稿不放在这里。

## Human Review Entry Order / 人工复核入口顺序

1. Open the related source object under `corpus/006_*` first.
2. Check the source register row, access note, checksum, and rights note.
3. Open the bibliography or published-scholarship note.
4. Check page, plate, catalog number, URL, and object record.
5. Check proposer, reading process status, disagreement, and dispute.
6. Keep unresolved claims as pending, disputed, or next-source checks.
7. Move no draft from `doc/public/user_research/` without human review.

人工复核时，先打开 `corpus/006_*` 下的来源对象，再核对来源登记、
访问记录、checksum 和权利说明。随后核对书目或已发表研究笔记中的
页码、图版号、著录号、URL、馆藏对象、提出者、释读过程、不同意见
和争议。未经人工复核，不得把 `doc/public/user_research/` 草稿移入
本目录。

## Required Content / 必须记录内容

- bibliographic identity: author, title, venue, year, page, plate, URL,
  catalog number, database name, or object record.
- source trail: source object id, source register row, access route,
  checksum, file size, manifest, field map, derived path, and review status.
- scope: corpus area, object type, inscription, glyph, component, period,
  batch, collection, findspot, or later-script relation supported.
- evidence level: primary object record, catalog, database export,
  peer-reviewed paper, monograph, web note, OCR text, or unreviewed draft.
- citation relation: cites, derives from, summarizes, disputes, or only
  routes to another record.
- reading process status: reported, accepted by cited source, rejected,
  disputed, needs checking, or out of scope.
- proposer and disagreement: who proposed the claim, who disagreed, and
  where the dispute is recorded.
- review status: reviewed source fact, source record only, dispute pending,
  rights pending, or next check pending.

## Concrete Questions To Check / 具体待查问题

- Which source object and register row prove this bibliography item?
- Which page, plate, URL, catalog number, or object record locates it?
- Which corpus object can this source actually support?
- What evidence level is justified by the opened source?
- What is the citation relation to other notes or source records?
- What is the reading process status, and is it merely reported?
- Who is the proposer, and where is the proposal recorded?
- Which disagreement or dispute is documented, and where?
- Which exact source must be opened before promotion into `research/`?

## Boundary / 边界

These notes are not confirmed scholarship until every claim is tied to opened
published evidence and review status. A bibliography row, source route, OCR
text, graph edge, AI draft, or CSV row is not a decipherment conclusion and
not confirmed scholarship.
