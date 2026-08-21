# The Met 42045 source-record candidate
# 大都会艺术博物馆 42045 来源记录候选

## English

This folder records one The Metropolitan Museum of Art object from its
official Open Access API. The project candidate ID is
`obs-insc-src-cand-000008`; the museum object ID is `42045`, accession
`67.43.14`.

The API reports an oracle bone, inscribed bone, Shang dynasty period, and a
public-domain flag. Two unchanged public image bytes are kept under
`03_visual-assets/`. The API labels them `primaryImage` and
`additionalImages[0]`; this folder does not call them recto or verso.

Read the human Markdown pages in numeric order before opening the JSON or
CSV. This is a source-record candidate, not a formal `obi-*` record. No OCR,
transcription, translation, character assignment, or decipherment was made.

## 简体中文

本目录记录大都会艺术博物馆官方 Open Access API 的一个对象。
本项目候选 ID 为 `obs-insc-src-cand-000008`，博物馆对象 ID 为 `42045`，
馆藏号为 `67.43.14`。

API 报告对象为甲骨、材质为刻辞骨，并给出商代时期和公开领域标记。
两张未改动的公开图像字节保存在 `03_visual-assets/`。API 将它们标为
`primaryImage` 和 `additionalImages[0]`；本目录不把它们称为正面或反面。

请先按编号阅读人类 Markdown，再打开 JSON 或 CSV。本目录不是正式
`obi-*` 卜辞记录，也没有制作 OCR、摹写、翻译、单字分配或破译结论。

## Reading order / 阅读顺序

1. `01_object-and-image-routes.md`: object, API, and image routes.
2. `02_human-inscription-dossier.md`: identity and direct visual notes.
3. `03_source-evidence-review.md`: source, checksum, and rights evidence.
4. `04_text-quality-review.md`: text and OCR quality boundary.
5. `05_character-linkage-review.md`: character and component gaps.
6. `06_literature-and-dispute-review.md`: literature and disagreement gaps.
7. `07_missing-evidence-plan.md`: concrete next checks.
8. `08_visual-region-review.md`: image-first observations without OCR.
9. Open `90_source-record.json` and `91_source-record-index.csv` last.

1. `01_object-and-image-routes.md`：对象、API 和图像路线。
2. `02_human-inscription-dossier.md`：身份与直接视觉观察。
3. `03_source-evidence-review.md`：来源、校验和与权利证据。
4. `04_text-quality-review.md`：文字和 OCR 质量边界。
5. `05_character-linkage-review.md`：单字和构件缺口。
6. `06_literature-and-dispute-review.md`：文献和分歧缺口。
7. `07_missing-evidence-plan.md`：具体下一步待查项。
8. `08_visual-region-review.md`：不做 OCR 的图像优先观察。
9. 最后打开 `90_source-record.json` 和 `91_source-record-index.csv`。

## Boundary / 边界

The Met API fields are source-reported museum metadata. The visual notes are
limited to what is directly visible in the two image files. The API period,
object name, and public-domain flag do not establish a Heji number, findspot,
inscription reading, character identity, or scholarly conclusion.

The Met API 字段是博物馆来源报告的 metadata。视觉观察只限于两张图像中
可直接看到的内容。API 的时期、对象名称和公开领域标记不证明合集号、出土
地、卜辞释读、单字身份或学术结论。

Rights / 权利: `public_domain_verified` for the two API image files;
metadata attribution and object-history checks remain required.

Review / 复核: `source_record_candidate_needs_text_and_catalog_review`.
