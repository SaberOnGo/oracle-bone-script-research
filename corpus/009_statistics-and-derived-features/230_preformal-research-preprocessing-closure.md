# Preformal Research Preprocessing Closure / 正式研究前资料整理闭合

## Purpose / 用途

This report records the current preprocessing boundary before formal oracle-
bone research. It is a human opening guide, not a new corpus record, a rights
decision, a decipherment result, or a claim that any candidate relation is
accepted scholarship.

本报告记录正式甲骨文研究开始前的资料整理边界。它是给人阅读的开包
指南，不是新的语料记录、权利决定、释读结果，也不把任何候选关系写成
已接受的学术结论。

Human-readable object dossiers remain primary. JSON, CSV, graph edges,
manifests, and route indexes remain secondary support for tracing, comparison,
statistics, and validation.

对象内人类可读档案仍是主体。JSON、CSV、图边、manifest 和路线索引只
用于追溯、比较、统计和校验，不能替代对象档案。

## Snapshot / 快照

- Snapshot date / 快照日期: `2026-08-07`
- Repository commit / 仓库提交: `c58eea95a97`
- Human archive status / 人类档案状态:
  `preprocessing_ready_for_human_review`
- Formal research status / 正式研究状态: `not_started`
- Source promotion / 来源提升: `not_promoted`
- Formal corpus import / 正式语料导入: `not_imported`
- Decipherment claims / 释读结论: `no_claim`

## Human Archive Coverage / 人类档案覆盖

- Deciphered oracle-character candidates: `1,588` object dossiers.
  Each has a local image, source route, human dossier, context dossier,
  archaeology/paleography review, readiness review, and visual note.
- Undeciphered oracle-character candidates: `9,408` non-empty object dossiers.
  Two empty duplicate directories remain outside the tracked archive and are
  not counted as records.
- OBIMD component candidates: `2,747` object dossiers. Each has a component
  dossier, visual gallery, context evidence, readiness review, and visual note.
- Cambridge/Hopkins inscription candidates: `612` object dossiers. Each has a
  human inscription dossier, plate/text gallery, OCR-quality review, context
  review, linkage review, and preformal opening check.
- EVOBC evolution/correspondence candidates: `13,714` object dossiers. Each
  has a human evolution dossier, image-route gallery, cross-period review,
  fact matrix, label-caution review, and readiness review.
- Collection-object candidates: `58` object dossiers with collection,
  findspot, period, batch, rights, and next-source questions.
- Research-topic candidates: `20` object dossiers with bibliography,
  database, inscription-route, dispute, and review questions.
- Codepoint crosswalk candidates: `1,588` object-local lookup dossiers.
- Registered source objects: `21` source dossiers with access, package,
  field-map, provenance, rights, literature, and pre-research reviews.
- Total object-local bundles audited by the coverage builder: `29,756`.

## Visual And Material Status / 图像与实物资料状态

- HUST-OBC character images: `10,996` local images and `10,996` visual
  notes. `6,595` notes contain direct visible records; `4,401` contain
  reproducible pixel profiles and explicitly remain human-review routes.
- OBIMD component images: `2,719` local image routes among `2,747` objects.
  `14` notes contain manual shape records, `2,705` contain pixel profiles,
  and `28` notes preserve concrete missing-image routes.
- Tracked image assets in character and component archives: `11,942` files,
  `42,985,551` bytes. Rights and source-risk notes remain attached to the
  asset routes.
- Cambridge/Hopkins inscription objects currently hold route galleries and
  concrete image, plate, OCR, catalog, page, and text-quality questions; no
  local source image is treated as collected evidence.
- EVOBC objects currently hold route galleries and source metadata. The raw
  image package remains outside ordinary Git; no route is treated as a
  reviewed paleographic image comparison.

## Source Provenance And Processing / 来源追溯与处理

- Source register: `21` source rows.
- Download/access log: `58` rows, including `47` downloaded rows and `11`
  access-error or access-boundary rows.
- Package manifest: `38` rows.
- Field map: `78` rows.
- Large-source register: `4` rows. Important packages above the repository
  limit remain in ignored local or external archives; Git keeps checksums,
  manifests, extraction notes, rights status, risk notes, and derived routes.
- The largest committed EVOBC source package record is `23,254,733` bytes,
  below the `30 MiB` repository limit. Raw OBIMD and other large packages are
  not used as ordinary committed corpus files.
- Each source object keeps the download or access route, checksum and size
  evidence, package manifest, field mapping, rights status, risk note,
  derivative path, and review state in its own directory or the linked source
  register.

## Relationship-Graph Support / 关系图辅助

The graph is a trace and comparison aid. It does not promote an identity,
variant, inscription reading, evolution chain, or decipherment conclusion.
Current JSONL edge counts are:

- HUST candidate routes: `3,562`
- OBIMD component routes: `44,433`
- EVOBC evolution routes: `51,679`
- Cambridge/Hopkins inscription routes: `4,403`
- Character-asset routes: `10,996`
- Cross-source ID routes: `1,737`
- Component-asset routes: `10,364`
- Topic routes: `672`
- Character-source routes: `10,996`
- Character-variant candidate routes: `2,747`
- Total graph rows scanned: `141,589`

The character-inscription audit still promotes `0` character-inscription
edges. The variant, evolution, and cross-source routes remain candidate or
lookup routes until image, plate, text, catalog, provenance, bibliography,
reviewer, and disagreement evidence are opened.

## Verification Evidence / 校验证据

The following current checks returned zero reported errors:

- Required-path and object-local material audits.
- Character and component visual-observation coverage audits.
- HUST, OBIMD component, Cambridge/Hopkins inscription, and EVOBC local
  material validators.
- Source-object human-material quality and human-research-depth audits.
- Project-ID/source-map, source-coverage, source-processing, phase-coverage,
  relationship-edge, and relationship-statistics validators.
- Full human-material gate over `156,793` research-body Markdown files:
  machine-dominant `0`, missing core slots `0`, mojibake `0`.
- 全量人类资料门禁覆盖 `156,793` 份研究正文 Markdown：机器路线主导 `0`，
  核心研究槽位缺失 `0`，乱码 `0`。
- Targeted visual-observation tests: `3 + 2 + 4 + 2` tests passed.
- Human-material gate regression tests: `4` tests passed.

The repository-wide skeleton validator and full unittest suite are deliberately
reported separately at release time because they are long-running checks. A
timeout or interrupted process must not be treated as a pass.

## Human Review Opening Order / 人工开包顺序

1. Open the concrete object `README.md` and the first human dossier.
2. Open the local image, rubbing, plate, or route gallery with its source row.
3. Open the source-object evidence dossier and the download, manifest, field
   map, checksum, rights, and risk records.
4. Compare independent catalog, inscription, findspot, collection, period,
   batch, bibliography, reading-history, and disagreement evidence.
5. Record the reviewer, date, exact route, uncertainty, and missing evidence
   in the object-local human dossier.
6. Use JSON, CSV, and graph files only after the human evidence route is open.

## Remaining Concrete Review Questions / 尚待人工复核的具体问题

- Which of the `4,401` HUST pixel-profile objects can now receive a direct,
  neutral visible record after a human opens its image?
- Which of the `2,705` OBIMD profile objects can receive a manual component-
  shape note, and which `28` missing-image routes require re-extraction or a
  rights decision?
- Which Cambridge/Hopkins plate, page, image, OCR, full text, and catalog route
  can be opened first for each of the `612` candidates?
- Which EVOBC image reference, oracle/bronze/seal route, period code, modern
  label, bibliography, or disagreement remains metadata-only for each
  candidate?
- Which source access or rights boundary must be resolved before any raw image,
  OCR, PDF, or large package is promoted?
- Which proposed relation has an explicit plate position, inscription text,
  character occurrence, source citation, reviewer, and disagreement record?

These are the next human research tasks, not empty placeholders and not
academic conclusions. Until they are answered with opened evidence, all
candidate identities, readings, variants, components, inscriptions,
correspondences, and evolution relations remain pending.

## Boundary / 边界

This closure report confirms a traceable, human-first preprocessing
infrastructure. It does not confirm an oracle-character reading, an
inscription identity, a component boundary, a variant relation, a modern
character correspondence, a historical evolution, a rights clearance, or a
decipherment conclusion.

本闭合报告确认的是可追溯、以人类档案为主体的预处理基础设施。它不确认
甲骨字释读、卜辞身份、构件边界、异体关系、今字对应、历史演变、权利
清理或破译结论。
