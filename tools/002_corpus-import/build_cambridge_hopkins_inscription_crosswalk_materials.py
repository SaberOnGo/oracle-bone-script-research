#!/usr/bin/env python3
"""Build object-local materials for Cambridge/Hopkins inscription crosswalk candidates."""

from __future__ import annotations

import argparse
import csv
import json
import re
import textwrap
from collections import Counter
from pathlib import Path


CROSSWALK_STAGING = Path(
    "corpus/002_oracle-bone-inscriptions/000_inscription-registers/"
    "002_cambridge-hopkins-crosswalk-staging.csv"
)
CLASSIFIED_SUMMARY = Path(
    "corpus/002_oracle-bone-inscriptions/000_inscription-registers/"
    "003_cambridge-hopkins-classified-summary.csv"
)
REVIEW_QUEUE = Path(
    "corpus/009_statistics-and-derived-features/"
    "098_ai-agent-cambridge-hopkins-inscription-crosswalk-review-queue.csv"
)
INSCRIPTION_MAP = Path(
    "project_registry/002_project-id-to-source-reference-map/"
    "002_oracle-inscription-id-source-map.csv"
)
INSCRIPTION_ROOT = Path("corpus/002_oracle-bone-inscriptions")
SOURCE_ID = "src-cambridge-hopkins"
DOWNLOAD_ID = "dl-cambridge-hopkins-finding-list"
UPDATED_AT = "2026-06-21"
BUCKET_SIZE = 100
MAX_HUMAN_LINE_LENGTH = 80

CAUTION = (
    "This object is a Cambridge/Hopkins inscription crosswalk candidate only. "
    "It is metadata for catalog review; it is not a formal obi-* inscription "
    "record, not an object identity claim, not a transcription, not an "
    "inscription reading, and not a decipherment conclusion."
)
RESEARCH_BOUNDARY = (
    "object_local_cambridge_hopkins_inscription_crosswalk_candidate_not_scholarship"
)

MAP_FIELDS = [
    "project_id",
    "record_type",
    "canonical_path",
    "primary_external_ref_id",
    "all_external_ref_ids",
    "source_ids",
    "rights_status",
    "review_status",
    "updated_at",
]

SOURCE_INDEX_FIELDS = [
    "source_index_id",
    "candidate_inscription_crosswalk_id",
    "project_id",
    "source_id",
    "evidence_download_id",
    "source_file_path",
    "source_row_id",
    "rights_status",
    "review_status",
    "research_boundary",
    "caution",
]

CATALOG_INDEX_FIELDS = [
    "catalog_reference_index_id",
    "candidate_inscription_crosswalk_id",
    "project_id",
    "reference_type",
    "reference_value",
    "reference_status",
    "required_review",
]

PLATE_ROUTE_FIELDS = [
    "plate_route_id",
    "candidate_inscription_crosswalk_id",
    "project_id",
    "route_type",
    "route_label",
    "reference_value",
    "evidence_status",
    "source_or_catalog",
    "human_action",
    "ai_action",
    "rights_status",
    "review_status",
    "caution",
]


def paragraph(text: str, width: int = 76) -> str:
    return textwrap.fill(
        " ".join(text.split()),
        width=width,
        break_long_words=True,
        break_on_hyphens=False,
    )


def assert_human_line_width(path_label: str, text: str) -> None:
    for line_number, line in enumerate(text.splitlines(), start=1):
        if len(line) > MAX_HUMAN_LINE_LENGTH:
            raise ValueError(
                f"{path_label}:{line_number} exceeds "
                f"{MAX_HUMAN_LINE_LENGTH} characters"
            )


def reference_value_markdown_lines(label: str, value: str) -> list[str]:
    if "\ufffd" not in value:
        return [f"  {label}: `{value or '(blank)'}`"]
    cleaned = value.replace("\ufffd", "").strip() or "(blank)"
    return [
        f"  {label}: `{cleaned}`",
        "  Note: unresolved source character; check original source row.",
    ]


def catalog_reference_markdown(catalog_rows: list[dict[str, str]]) -> str:
    lines: list[str] = []
    for ref in catalog_rows:
        lines.append(f"- Type: `{ref['reference_type']}`")
        lines.extend(reference_value_markdown_lines("Value", ref["reference_value"]))
        lines.extend(
            [
                f"  Status: `{ref['reference_status']}`",
                f"  Review: `{ref['required_review']}`",
            ]
        )
    return "\n".join(lines)


def route_markdown(plate_routes: list[dict[str, str]]) -> str:
    lines: list[str] = []
    for route in plate_routes:
        lines.extend(
            [
                f"- Route: `{route['route_type']}`",
                f"  Label: {route['route_label']}",
            ]
        )
        lines.extend(reference_value_markdown_lines("Reference", route["reference_value"]))
        lines.extend(
            [
                f"  Status: `{route['evidence_status']}`",
                f"  Review: `{route['review_status']}`",
            ]
        )
    return "\n".join(lines)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def safe_token(value: str) -> str:
    token = re.sub(r"[^0-9A-Za-z]+", "-", value.strip()).strip("-").lower()
    return token or "unassigned"


def project_id_for_index(index: int) -> str:
    return f"obs-insc-cw-cand-{index:06d}"


def primary_external_ref(row: dict[str, str]) -> str:
    return row["candidate_inscription_crosswalk_id"].replace("cam-hopkins-crosswalk", "cam-hopkins-cw")


def bucket_dir_for_index(index: int) -> Path:
    bucket_index = ((index - 1) // BUCKET_SIZE) + 1
    start = ((index - 1) // BUCKET_SIZE) * BUCKET_SIZE + 1
    end = start + BUCKET_SIZE - 1
    return (
        INSCRIPTION_ROOT
        / f"{bucket_index:03d}_{start:06d}-{end:06d}_obs-insc-cw-bucket_crosswalk-candidates"
    )


def object_dir_for_row(index: int, row: dict[str, str]) -> Path:
    return (
        bucket_dir_for_index(index)
        / (
            f"{index:03d}_{project_id_for_index(index)}_"
            f"{primary_external_ref(row)}_crosswalk-candidate"
        )
    )


def reference_status(value: str) -> str:
    stripped = value.strip()
    if not stripped or set(stripped) == {"*"}:
        return "missing_or_unassigned"
    return "present_in_cambridge_hopkins_metadata"


def catalog_reference_rows(index: int, row: dict[str, str], project_id: str) -> list[dict[str, str]]:
    specs = [
        ("yingguo_ref_id", "yingguo"),
        ("cul_ref_id", "cambridge_university_library"),
        ("chalfant_ref_id", "chalfant"),
        ("heji_ref_id", "heji"),
    ]
    output = []
    for ref_index, (field_name, reference_type) in enumerate(specs, start=1):
        value = row.get(field_name, "")
        status = reference_status(value)
        output.append(
            {
                "catalog_reference_index_id": (
                    f"{project_id}-catalog-ref-{ref_index:02d}"
                ),
                "candidate_inscription_crosswalk_id": row["candidate_inscription_crosswalk_id"],
                "project_id": project_id,
                "reference_type": reference_type,
                "reference_value": value,
                "reference_status": status,
                "required_review": (
                    "verify_against_primary_catalog_object_record_and_source_image"
                    if status == "present_in_cambridge_hopkins_metadata"
                    else "locate_or_confirm_missing_reference_before_formal_assignment"
                ),
            }
        )
    return output


def plate_route_rows(row: dict[str, str], project_id: str) -> list[dict[str, str]]:
    route_specs = [
        (
            "cambridge_hopkins_finding_list",
            "Cambridge/Hopkins finding-list row",
            row["candidate_inscription_crosswalk_id"],
            "src-cambridge-hopkins",
            "open_source_download_or_live_page_and_verify_period_group_and_cross_references",
            "use_crosswalk_source_index_and_catalog_reference_index_as_metadata_routes",
        ),
        (
            "yingguo_catalog_reference",
            "Yingguo suo cang jiagu ji reference",
            row.get("yingguo_ref_id", ""),
            "Yingguo reference cited by Cambridge/Hopkins",
            "locate_or_open_the_cited_catalog_entry_before_using_as_image_or_text_evidence",
            "treat_as_external_catalog_route_only_until_catalog_entry_is_reviewed",
        ),
        (
            "cambridge_university_library_reference",
            "Cambridge University Library object/reference number",
            row.get("cul_ref_id", ""),
            "Cambridge University Library reference cited by Cambridge/Hopkins",
            "open_the_CUL_object_or_catalog_record_and_check_for_images_rights_and_object_metadata",
            "treat_as_object_record_route_only_until_source_image_and_rights_are_reviewed",
        ),
        (
            "chalfant_reference",
            "Chalfant reference",
            row.get("chalfant_ref_id", ""),
            "Chalfant reference cited by Cambridge/Hopkins",
            "locate_or_open_the_Chalfant_entry_before_using_as_plate_or_transcription_evidence",
            "treat_as_bibliographic_route_only_until_entry_is_reviewed",
        ),
        (
            "heji_reference",
            "Heji reference",
            row.get("heji_ref_id", ""),
            "Heji reference cited by Cambridge/Hopkins",
            "locate_or_open_the_Heji_entry_before_using_as_plate_or_text_evidence",
            "treat_as_catalog_route_only_until_entry_is_reviewed",
        ),
    ]
    routes: list[dict[str, str]] = []
    for route_index, (
        route_type,
        route_label,
        reference_value,
        source_or_catalog,
        human_action,
        ai_action,
    ) in enumerate(route_specs, start=1):
        evidence_status = (
            "route_present_image_or_text_not_collected"
            if reference_status(reference_value) == "present_in_cambridge_hopkins_metadata"
            else "route_missing_or_unassigned"
        )
        routes.append(
            {
                "plate_route_id": f"{project_id}-plate-route-{route_index:02d}",
                "candidate_inscription_crosswalk_id": row["candidate_inscription_crosswalk_id"],
                "project_id": project_id,
                "route_type": route_type,
                "route_label": route_label,
                "reference_value": reference_value,
                "evidence_status": evidence_status,
                "source_or_catalog": source_or_catalog,
                "human_action": human_action,
                "ai_action": ai_action,
                "rights_status": "metadata_only_until_verified",
                "review_status": "needs_human_inscription_crosswalk_review",
                "caution": (
                    "Route only: no local plate image, OCR text, transcription, "
                    "object identity, or formal obi-* record has been confirmed."
                ),
            }
        )
    return routes


def source_index_row(index: int, row: dict[str, str], project_id: str) -> dict[str, str]:
    return {
        "source_index_id": f"{project_id}-source-01",
        "candidate_inscription_crosswalk_id": row["candidate_inscription_crosswalk_id"],
        "project_id": project_id,
        "source_id": SOURCE_ID,
        "evidence_download_id": DOWNLOAD_ID,
        "source_file_path": CROSSWALK_STAGING.as_posix(),
        "source_row_id": str(index),
        "rights_status": row["rights_status"],
        "review_status": "reviewed_metadata_only",
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
    }


def packet_for_row(
    index: int,
    row: dict[str, str],
    project_id: str,
    object_dir: Path,
    catalog_rows: list[dict[str, str]],
    plate_routes: list[dict[str, str]],
    period_group_counts: Counter[str],
) -> dict[str, object]:
    missing_types = [
        ref["reference_type"]
        for ref in catalog_rows
        if ref["reference_status"] == "missing_or_unassigned"
    ]
    period_group_key = f"{row['period_label']}|{row['group_number']}"
    return {
        "project_id": project_id,
        "record_type": "inscription_crosswalk_candidate",
        "candidate_inscription_crosswalk_id": row["candidate_inscription_crosswalk_id"],
        "primary_external_ref_id": primary_external_ref(row),
        "source_id": SOURCE_ID,
        "evidence_download_id": DOWNLOAD_ID,
        "canonical_path": object_dir.as_posix(),
        "period_label": row["period_label"],
        "group_number": row["group_number"],
        "group_declared_count": row["group_declared_count"],
        "period_group_observed_row_count": period_group_counts[period_group_key],
        "catalog_references": catalog_rows,
        "plate_and_text_evidence_routes": plate_routes,
        "missing_reference_types": missing_types,
        "formal_inscription_assignment_status": "not_assigned_formal_obi_id",
        "catalog_identity_claim_status": "not_confirmed_catalog_identity",
        "image_evidence_status": "route_indexed_not_collected",
        "text_transcription_status": "route_indexed_not_collected",
        "collection_object_match_status": "not_collected",
        "project_import_status": "dataset_candidate_not_promoted",
        "rights_status": row["rights_status"],
        "review_status": "needs_human_inscription_crosswalk_review",
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def readme_text(
    index: int,
    row: dict[str, str],
    project_id: str,
    catalog_rows: list[dict[str, str]],
) -> str:
    refs = catalog_reference_markdown(catalog_rows)
    missing = [
        ref["reference_type"]
        for ref in catalog_rows
        if ref["reference_status"] == "missing_or_unassigned"
    ]
    missing_text = ", ".join(missing) if missing else "none"
    text = f"""# {project_id} Cambridge/Hopkins inscription candidate

English:
{paragraph("This is an object-local research entrance for a Cambridge/Hopkins inscription crosswalk candidate. The human-readable notes, plate/catalog routes, and AI-readable indexes are stored in this same concrete corpus object directory.")}

Simplified Chinese:
{paragraph("这是 Cambridge/Hopkins 卜辞目录互证候选的对象内研究入口。人类可读说明、图版与著录路线、AI 可读索引都放在本对象目录内，不另建平行目录。")}

## Boundary / 边界

- This is not a formal `obi-*` inscription record.
- This is not an object identity claim.
- This is not a transcription or inscription reading.
- This is not a decipherment conclusion.
- 这不是正式 `obi-*` 卜辞记录。
- 这不是馆藏对象同一性结论。
- 这不是释文或卜辞读法。
- 这不是释读结论。

## Local Files / 本目录文件

- `01_candidate-inscription-crosswalk-packet.json`
  AI-readable candidate packet.
- `02_crosswalk-source-index.csv`
  Source, rights, and route index.
- `03_catalog-reference-index.csv`
  Yingguo, CUL, Chalfant, and Heji reference index.
- `04_human-review-sheet.md`
  Human review sheet for catalog and image/context checks.
- `05_plate-text-route-index.csv`
  Plate, image, catalog, and text-evidence route index.
- `06_plate-text-gallery.md`
  Human-readable route gallery for plate/image/text evidence.
- `07_human-inscription-dossier.md`
  Human-readable dossier for this candidate inscription object.
- `08_inscription-dossier-index.json`
  AI-readable index for the dossier and review gaps.
- `09_inscription-plate-evidence-dossier.md`
  Human-readable evidence dossier for text, OCR, plate, and catalog routes.
- `10_inscription-plate-evidence-index.json`
  AI-readable support index for the inscription and plate dossier.

## Candidate Metadata / 候选 metadata

- Project ID: `{project_id}`
- Cambridge/Hopkins row ID: `{row['candidate_inscription_crosswalk_id']}`
- Source: `{SOURCE_ID}`
- Download evidence: `{DOWNLOAD_ID}`
- Period label: `{row['period_label']}`
- Classification group: `{row['group_number']}`
- Missing reference types: `{missing_text}`

## Catalog References / 目录引用

{refs}

## Plate And Text Evidence / 图版与文本证据

Current status: `route_indexed_not_collected`.

Open `06_plate-text-gallery.md` for plate, object, Heji/OBM, and
catalog routes.

当前状态：`route_indexed_not_collected`。

请打开同目录的 `06_plate-text-gallery.md`。

本文件不确认图片、OCR、释文、读法或对象同一性。

## Human Dossier / 人类研究入口

Open `07_human-inscription-dossier.md` first when reviewing this object.

该 dossier 汇总来源、著录、图版路线、时期线索和缺失项。

## Review Status / 复核状态

Current status: `needs_human_inscription_crosswalk_review`.

Reviewers must compare primary catalog/object records, Heji/OBM records,
and source images before any formal `obi-*` assignment.

Generated row index: `{index}`.
"""
    assert_human_line_width(f"{project_id}/README.md", text)
    return text


def plate_text_gallery_text(
    row: dict[str, str],
    project_id: str,
    plate_routes: list[dict[str, str]],
) -> str:
    route_lines = route_markdown(plate_routes)
    text = f"""# Plate And Text Route Gallery / 图版与文本路线图

Project ID: `{project_id}`

Candidate crosswalk ID: `{row['candidate_inscription_crosswalk_id']}`

English:
{paragraph("This file is a human-readable object-local route gallery. It lists where a reviewer should look for plate images, object records, catalog entries, Heji/OBM references, OCR text, and full inscription context. It does not contain confirmed images or transcriptions.")}

简体中文：
{paragraph("本文件是对象内的人类可读路线图，用来提示复核者到哪里寻找图版图片、馆藏对象记录、著录条目、合集或 OBM 对应、OCR 文本和完整卜辞上下文。这里不包含已确认图片或释文。")}

## Routes / 路线

{route_lines}

## Evidence Status / 证据状态

- Local plate image: `not_collected`
- Local OCR text: `not_collected`
- Full inscription transcription: `not_collected`
- Object identity: `not_confirmed_catalog_identity`
- Formal `obi-*` assignment: `not_assigned_formal_obi_id`

## Boundary / 边界

{paragraph("This route gallery is preprocessing infrastructure only. It is not a formal inscription record, not an image-rights decision, not a transcription, not an inscription reading, and not a decipherment conclusion.")}
"""
    assert_human_line_width(f"{project_id}/06_plate-text-gallery.md", text)
    return text


def review_sheet_text(row: dict[str, str], project_id: str) -> str:
    text = f"""# Human Review Sheet / 人工复核单

Project ID: `{project_id}`

Candidate crosswalk ID: `{row['candidate_inscription_crosswalk_id']}`

## Required Checks / 必须复核

- Open `02_crosswalk-source-index.csv` and verify the source/download trail.
- Open `03_catalog-reference-index.csv`.
- Compare all references against primary catalog or object records.
- Open `05_plate-text-route-index.csv`.
- Open `06_plate-text-gallery.md`.
- Search for images or inscription text only after reading both files.
- Confirm source images and object records.
- Confirm Heji/OBM records and full inscription context.
- Do not assign a formal `obi-*` ID from this sheet alone.
- Do not record a transcription here.
- Do not record an inscription reading here.
- This sheet is not an inscription reading.
- Do not record an object identity claim here.
- Do not record a decipherment conclusion here.

## Current Evidence Status / 当前证据状态

- Image evidence: `route_indexed_not_collected`
- Text transcription: `route_indexed_not_collected`
- Collection object match: `not_collected`
- Formal inscription assignment: `not_assigned_formal_obi_id`
- Review status: `needs_human_inscription_crosswalk_review`

## Concrete Questions To Check / 具体待查问题

Use these specific questions before recording any conclusion.

- Which plate, page, Heji, or catalog number should be checked first?
- Which object record or collection shelfmark can anchor the physical item?
- Which excavation, findspot, period, or batch context is still missing?
- Which image, rubbing, OCR, or full-text route can supply context?
- Which linked character occurrence routes are only candidates?
- Which rights, checksum, manifest, or download log needs review?
- What evidence is still missing before any formal `obi-*` assignment?

- 应先核对哪一个图版号、页码、合集号或著录号？
- 哪个馆藏对象记录或库藏号可以定位实物？
- 还缺哪些出土地、出土点、时期或批次上下文？
- 哪条图像、拓片、OCR 或全文路线可以补足上下文？
- 哪些关联字形或字序路线仍只是候选线索？
- 还要复核哪些权利、checksum、manifest 或下载记录？
- 正式分配任何 `obi-*` 编号前还缺哪些证据？

## Caution / 风险提示

{paragraph(CAUTION)}
"""
    assert_human_line_width(f"{project_id}/04_human-review-sheet.md", text)
    return text


def human_dossier_text(
    index: int,
    row: dict[str, str],
    project_id: str,
    catalog_rows: list[dict[str, str]],
    plate_routes: list[dict[str, str]],
) -> str:
    refs = catalog_reference_markdown(catalog_rows)
    routes = route_markdown(plate_routes)
    missing = [
        ref["reference_type"]
        for ref in catalog_rows
        if ref["reference_status"] == "missing_or_unassigned"
    ]
    missing_text = ", ".join(missing) if missing else "none"
    text = f"""# Human Inscription Dossier / 人类卜辞资料夹

Project ID: `{project_id}`

Candidate crosswalk ID: `{row['candidate_inscription_crosswalk_id']}`

## Status / 状态

- Record type: `inscription_crosswalk_candidate`
- Formal `obi-*` ID: `not_assigned_formal_obi_id`
- Object identity: `not_confirmed_catalog_identity`
- Plate image: `not_collected`
- OCR text: `not_collected`
- Full transcription: `not_collected`
- Review status: `needs_human_inscription_crosswalk_review`

## What A Human Can Read Here / 人可读内容

This dossier gives the reviewer a compact local reading path.

本资料夹提供一个本对象内的人工阅读入口。

It lists the catalog clues, period/group metadata, evidence routes,
known gaps, and the files that must be opened before formal research.

这里列出著录线索、时期与分组、证据路线、缺失项和复核入口。

## Source Trail / 来源链

- Source ID: `{SOURCE_ID}`
- Download ID: `{DOWNLOAD_ID}`
- Source staging row: `{index}`
- Rights status: `{row['rights_status']}`
- Boundary: metadata route only, pending source review.

## Period And Group / 时期与组别

- Period label: `{row['period_label']}`
- Classification group: `{row['group_number']}`
- Declared group count: `{row['group_declared_count']}`

These labels are imported metadata, not a new chronological judgement.

这些标签来自导入资料，不是本仓库新增断代结论。

## Catalog Clues / 著录线索

{refs}

## Plate, Image, And Text Routes / 图版、图像与文本路线

{routes}

## Text And OCR Quality Review / 文本与 OCR 质量复核

- Full text or OCR status: `not_collected`
- 全文或 OCR 状态：`not_collected`
- Text quality status: `needs_primary_text_or_OCR_route_review`
- 文本质量状态：`needs_primary_text_or_OCR_route_review`
- Which unreadable, missing, or uncertain signs must be marked?
- 哪些不可读、缺失或不确定字形必须标出？
- Which source line, page, plate, OCR file, or catalog route supports it?
- 哪条来源行、页码、图版、OCR 文件或著录路线支持它？
- Do not turn OCR text or catalog labels into an inscription reading.
- 不要把 OCR 文本或著录标签写成卜辞释读结论。

## Missing Or Not Yet Collected / 缺失或未采集

- Missing reference types: `{missing_text}`
- Excavation site: `not_collected`
- Collection object record: `not_collected`
- Findspot: `not_collected`
- Batch or pit context: `not_collected`
- Plate image path: `not_collected`
- Inscription OCR: `not_collected`
- Full inscription text: `not_collected`
- Linked character occurrences: `not_collected`
- Later-script correspondence: `not_applicable_to_this_record`

### Concrete Questions To Check / 具体待查问题

- Which plate numbers, page numbers, Heji IDs, or catalog numbers need review?
- 需要核对哪些图版号、页码、合集号或著录号？
- Which source route should be opened first for this crosswalk candidate?
- 这个互证候选应先打开哪条来源路线？
- Which object record or collection shelfmark can anchor the physical item?
- 哪个馆藏对象记录或库藏号可以定位实物？
- Which collection, findspot, period, or batch records are relevant?
- 哪些馆藏、出土地、时期或批次记录与本对象有关？
- Which image, rubbing, OCR, or full-text route can supply context?
- 哪条图像、拓片、OCR 或全文路线可以补足上下文？
- Which linked character occurrences are only candidates needing review?
- 哪些关联字形或字序只是候选线索，仍需人工复核？
- Which rights, checksum, manifest, or download-log records must be opened?
- 下一步应打开哪些权利、checksum、manifest 或下载记录？
- What evidence is still missing before any formal `obi-*` assignment?
- 在任何正式 `obi-*` 分配前，还缺哪些证据？

## Review Entry Points / 复核入口

- Start with `README.md`.
- Read this dossier.
- Check `03_catalog-reference-index.csv`.
- Check `05_plate-text-route-index.csv`.
- Use `06_plate-text-gallery.md` as the human route list.
- Record conclusions only after primary evidence review.

## Boundary / 边界

{paragraph(CAUTION)}
"""
    assert_human_line_width(f"{project_id}/07_human-inscription-dossier.md", text)
    return text


def plate_evidence_dossier_text(
    index: int,
    row: dict[str, str],
    project_id: str,
    catalog_rows: list[dict[str, str]],
    plate_routes: list[dict[str, str]],
) -> str:
    missing_refs = [
        ref["reference_type"]
        for ref in catalog_rows
        if ref["reference_status"] == "missing_or_unassigned"
    ]
    unresolved_note = (
        "- Note: unresolved source character; check original source row."
        if any("\ufffd" in ref["reference_value"] for ref in catalog_rows)
        else "- Note: no unresolved source character marker in catalog refs."
    )
    text = f"""# Inscription And Plate Evidence Dossier / 卜辞与图版证据档案

Project ID: `{project_id}`

Candidate crosswalk ID: `{row['candidate_inscription_crosswalk_id']}`

## Inscription Number And Text State / 卜辞编号与文本状态

- Formal `obi-*` ID: `not_assigned_formal_obi_id`
- Source row number: `{index}`
- Full text or OCR: `not_collected`
- Full inscription transcription: `not_collected`
- Text quality: `needs_primary_text_or_OCR_route_review`
- Review status: `needs_human_inscription_crosswalk_review`

{paragraph("This file is a human evidence dossier for one inscription and plate crosswalk candidate. It gathers the routes a reviewer must open before treating any text, OCR, plate, catalog number, or object record as evidence.")}

{paragraph("本文件是一个卜辞与图版互证候选的人类证据档案。它汇总复核者在使用任何全文、OCR、图版、著录号或馆藏对象记录前必须打开的路线。")}

## Plate Catalog Heji And Collection Routes / 图版、著录、合集与馆藏路线

- Plate image path: `not_collected`
- Local rubbing or photograph: `not_collected`
- Catalog route count: `{len(catalog_rows)}`
- Plate and text route count: `{len(plate_routes)}`
- Present catalog refs: see `03_catalog-reference-index.csv`
- Missing catalog refs: `{'; '.join(missing_refs) if missing_refs else 'none'}`
- Route type list: see `05_plate-text-route-index.csv`
{unresolved_note}

Open `03_catalog-reference-index.csv` and `05_plate-text-route-index.csv`
before using a plate, Heji number, catalog number, CUL object route, or
Chalfant reference.

## Findspot Period Batch And Linked Characters / 出土地、时期、批次与关联字形

- Period label: `{row['period_label']}`
- Classification group: `{row['group_number']}`
- Declared group count: `{row['group_declared_count']}`
- Collection object record: `not_collected`
- Excavation site: `not_collected`
- Findspot: `not_collected`
- Batch or pit context: `not_collected`
- Linked character occurrences: `not_collected`

{paragraph("The period and group labels come from imported metadata. They are review signals, not new chronological conclusions. Linked characters still need a separate occurrence review before they can support character dossiers.")}

{paragraph("时期和分组标签来自导入 metadata，只是复核信号，不是新增断代结论。关联字形仍需单独的字形出处复核，才可支持单字档案。")}

## Text Quality Missing Items And Review Status / 文本质量、缺失项与复核状态

- Missing text evidence: `full_inscription_text_or_ocr`
- Missing visual evidence: `plate_image_or_rubbing`
- Missing provenance: `collection_findspot_period_batch_context`
- Missing relation evidence: `linked_character_occurrences`
- Rights status: `{row['rights_status']}`
- Evidence download ID: `{DOWNLOAD_ID}`

Concrete questions to check:

- Which source row, plate, page, Heji ID, or catalog number anchors it?
- Which image, rubbing, OCR, or full-text route can be opened first?
- Which collection object, shelfmark, findspot, period, or batch is relevant?
- Which linked character occurrences are only candidate routes?
- Which rights, checksum, manifest, or download-log row must be reviewed?

具体待查问题：

- 哪条来源行、图版号、页码、合集号或著录号定位本对象？
- 哪条图像、拓片、OCR 或全文路线应优先打开？
- 哪个馆藏对象、库藏号、出土地、时期或批次相关？
- 哪些关联字形或字序仍只是候选路线？
- 哪些权利、checksum、manifest 或下载记录必须复核？

## Boundary / 边界

- not a formal inscription record
- not an object identity claim
- not a transcription
- not an inscription reading
- not corpus import approval
- not a decipherment conclusion
- 不是正式卜辞记录
- 不是馆藏对象同一性结论
- 不是释文
- 不是卜辞读法
- 不是语料导入批准
- 不是释读结论
"""
    assert_human_line_width(f"{project_id}/09_inscription-plate-evidence-dossier.md", text)
    return text


def plate_evidence_index(
    row: dict[str, str],
    project_id: str,
    catalog_rows: list[dict[str, str]],
    plate_routes: list[dict[str, str]],
) -> dict[str, object]:
    missing_refs = [
        ref["reference_type"]
        for ref in catalog_rows
        if ref["reference_status"] == "missing_or_unassigned"
    ]
    return {
        "project_id": project_id,
        "record_type": "inscription_plate_evidence_dossier_index",
        "candidate_inscription_crosswalk_id": row["candidate_inscription_crosswalk_id"],
        "human_readable_files": [
            "README.md",
            "04_human-review-sheet.md",
            "06_plate-text-gallery.md",
            "07_human-inscription-dossier.md",
            "09_inscription-plate-evidence-dossier.md",
        ],
        "ai_support_files": [
            "01_candidate-inscription-crosswalk-packet.json",
            "02_crosswalk-source-index.csv",
            "03_catalog-reference-index.csv",
            "05_plate-text-route-index.csv",
            "08_inscription-dossier-index.json",
            "10_inscription-plate-evidence-index.json",
        ],
        "catalog_reference_count": len(catalog_rows),
        "plate_text_route_count": len(plate_routes),
        "missing_reference_types": missing_refs,
        "missing_or_review_fields": [
            "full_inscription_text_or_ocr",
            "plate_image_or_rubbing",
            "collection_findspot_period_batch_context",
            "linked_character_occurrences",
            "rights_checksum_manifest_download_log_review",
        ],
        "text_quality_status": "needs_primary_text_or_OCR_route_review",
        "formal_inscription_assignment_status": "not_assigned_formal_obi_id",
        "review_status": "needs_human_inscription_crosswalk_review",
        "claim_boundary": [
            "no formal inscription record",
            "no object identity claim",
            "no transcription",
            "no inscription reading",
            "no corpus import approval",
            "no decipherment conclusion",
        ],
        "updated_at": UPDATED_AT,
    }


def dossier_index(
    row: dict[str, str],
    project_id: str,
    catalog_rows: list[dict[str, str]],
    plate_routes: list[dict[str, str]],
) -> dict[str, object]:
    missing = [
        ref["reference_type"]
        for ref in catalog_rows
        if ref["reference_status"] == "missing_or_unassigned"
    ]
    return {
        "project_id": project_id,
        "record_type": "inscription_crosswalk_candidate_dossier_index",
        "candidate_inscription_crosswalk_id": row["candidate_inscription_crosswalk_id"],
        "human_readable_files": [
            "README.md",
            "04_human-review-sheet.md",
            "06_plate-text-gallery.md",
            "07_human-inscription-dossier.md",
            "09_inscription-plate-evidence-dossier.md",
        ],
        "ai_readable_files": [
            "01_candidate-inscription-crosswalk-packet.json",
            "02_crosswalk-source-index.csv",
            "03_catalog-reference-index.csv",
            "05_plate-text-route-index.csv",
            "10_inscription-plate-evidence-index.json",
        ],
        "catalog_reference_count": len(catalog_rows),
        "plate_text_route_count": len(plate_routes),
        "missing_reference_types": missing,
        "human_review_status": "needs_human_inscription_crosswalk_review",
        "formal_inscription_assignment_status": "not_assigned_formal_obi_id",
        "catalog_identity_claim_status": "not_confirmed_catalog_identity",
        "image_evidence_status": "route_indexed_not_collected",
        "text_transcription_status": "route_indexed_not_collected",
        "uncollected_human_research_fields": [
            "excavation_site",
            "collection_object_record",
            "findspot",
            "batch_or_pit_context",
            "plate_image_path",
            "inscription_ocr",
            "full_inscription_text",
            "linked_character_occurrences",
        ],
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def build_outputs(root: Path) -> dict[str, dict[str, object]]:
    crosswalk_rows = read_csv_rows(root / CROSSWALK_STAGING)
    period_group_counts = Counter(
        f"{row['period_label']}|{row['group_number']}" for row in crosswalk_rows
    )
    outputs: dict[str, dict[str, object]] = {}
    for index, row in enumerate(crosswalk_rows, start=1):
        project_id = project_id_for_index(index)
        relative_object_dir = object_dir_for_row(index, row)
        object_dir = root / relative_object_dir
        catalog_rows = catalog_reference_rows(index, row, project_id)
        plate_routes = plate_route_rows(row, project_id)
        packet = packet_for_row(
            index,
            row,
            project_id,
            relative_object_dir,
            catalog_rows,
            plate_routes,
            period_group_counts,
        )
        source_rows = [source_index_row(index, row, project_id)]
        outputs[project_id] = {
            "object_dir": object_dir,
            "relative_object_dir": relative_object_dir,
            "readme_text": readme_text(index, row, project_id, catalog_rows),
            "packet": packet,
            "source_rows": source_rows,
            "catalog_rows": catalog_rows,
            "plate_routes": plate_routes,
            "plate_text_gallery_text": plate_text_gallery_text(row, project_id, plate_routes),
            "review_sheet_text": review_sheet_text(row, project_id),
            "human_dossier_text": human_dossier_text(
                index,
                row,
                project_id,
                catalog_rows,
                plate_routes,
            ),
            "dossier_index": dossier_index(row, project_id, catalog_rows, plate_routes),
            "plate_evidence_dossier_text": plate_evidence_dossier_text(
                index,
                row,
                project_id,
                catalog_rows,
                plate_routes,
            ),
            "plate_evidence_index": plate_evidence_index(
                row,
                project_id,
                catalog_rows,
                plate_routes,
            ),
            "map_row": {
                "project_id": project_id,
                "record_type": "inscription_crosswalk_candidate",
                "canonical_path": relative_object_dir.as_posix(),
                "primary_external_ref_id": primary_external_ref(row),
                "all_external_ref_ids": ";".join(
                    [
                        row["candidate_inscription_crosswalk_id"],
                        row.get("yingguo_ref_id", ""),
                        row.get("cul_ref_id", ""),
                        row.get("chalfant_ref_id", ""),
                        row.get("heji_ref_id", ""),
                    ]
                ),
                "source_ids": SOURCE_ID,
                "rights_status": row["rights_status"],
                "review_status": "needs_human_inscription_crosswalk_review",
                "updated_at": UPDATED_AT,
            },
        }
    return outputs


def write_bucket_manifests(root: Path, outputs: dict[str, dict[str, object]]) -> None:
    buckets: dict[Path, list[dict[str, str]]] = {}
    for project_id, output in outputs.items():
        relative_object_dir = output["relative_object_dir"]
        assert isinstance(relative_object_dir, Path)
        buckets.setdefault(relative_object_dir.parent, []).append(
            {
                "project_id": project_id,
                "record_type": "inscription_crosswalk_candidate",
                "object_dir": relative_object_dir.as_posix(),
                "packet_path": (relative_object_dir / "01_candidate-inscription-crosswalk-packet.json").as_posix(),
                "source_index_path": (relative_object_dir / "02_crosswalk-source-index.csv").as_posix(),
                "catalog_reference_index_path": (relative_object_dir / "03_catalog-reference-index.csv").as_posix(),
                "human_review_sheet_path": (relative_object_dir / "04_human-review-sheet.md").as_posix(),
                "plate_text_route_index_path": (relative_object_dir / "05_plate-text-route-index.csv").as_posix(),
                "plate_text_gallery_path": (relative_object_dir / "06_plate-text-gallery.md").as_posix(),
                "human_dossier_path": (relative_object_dir / "07_human-inscription-dossier.md").as_posix(),
                "dossier_index_path": (relative_object_dir / "08_inscription-dossier-index.json").as_posix(),
                "plate_evidence_dossier_path": (
                    relative_object_dir / "09_inscription-plate-evidence-dossier.md"
                ).as_posix(),
                "plate_evidence_index_path": (
                    relative_object_dir / "10_inscription-plate-evidence-index.json"
                ).as_posix(),
                "review_status": "needs_human_inscription_crosswalk_review",
                "updated_at": UPDATED_AT,
            }
        )
    fields = [
        "project_id",
        "record_type",
        "object_dir",
        "packet_path",
        "source_index_path",
        "catalog_reference_index_path",
        "human_review_sheet_path",
        "plate_text_route_index_path",
        "plate_text_gallery_path",
        "human_dossier_path",
        "dossier_index_path",
        "plate_evidence_dossier_path",
        "plate_evidence_index_path",
        "review_status",
        "updated_at",
    ]
    for bucket_dir, rows in buckets.items():
        write_csv(
            root / bucket_dir / "000_cambridge-hopkins-inscription-crosswalk-bucket-manifest.csv",
            fields,
            rows,
        )


def write_outputs(root: Path, outputs: dict[str, dict[str, object]]) -> None:
    for output in outputs.values():
        object_dir = output["object_dir"]
        assert isinstance(object_dir, Path)
        object_dir.mkdir(parents=True, exist_ok=True)
        (object_dir / "README.md").write_text(str(output["readme_text"]), encoding="utf-8", newline="\n")
        (object_dir / "01_candidate-inscription-crosswalk-packet.json").write_text(
            json.dumps(output["packet"], ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        write_csv(
            object_dir / "02_crosswalk-source-index.csv",
            SOURCE_INDEX_FIELDS,
            output["source_rows"],  # type: ignore[arg-type]
        )
        write_csv(
            object_dir / "03_catalog-reference-index.csv",
            CATALOG_INDEX_FIELDS,
            output["catalog_rows"],  # type: ignore[arg-type]
        )
        write_csv(
            object_dir / "05_plate-text-route-index.csv",
            PLATE_ROUTE_FIELDS,
            output["plate_routes"],  # type: ignore[arg-type]
        )
        (object_dir / "06_plate-text-gallery.md").write_text(
            str(output["plate_text_gallery_text"]),
            encoding="utf-8",
            newline="\n",
        )
        (object_dir / "04_human-review-sheet.md").write_text(
            str(output["review_sheet_text"]),
            encoding="utf-8",
            newline="\n",
        )
        (object_dir / "07_human-inscription-dossier.md").write_text(
            str(output["human_dossier_text"]),
            encoding="utf-8",
            newline="\n",
        )
        (object_dir / "08_inscription-dossier-index.json").write_text(
            json.dumps(output["dossier_index"], ensure_ascii=False, indent=2, sort_keys=True)
            + "\n",
            encoding="utf-8",
            newline="\n",
        )
        (object_dir / "09_inscription-plate-evidence-dossier.md").write_text(
            str(output["plate_evidence_dossier_text"]),
            encoding="utf-8",
            newline="\n",
        )
        (object_dir / "10_inscription-plate-evidence-index.json").write_text(
            json.dumps(output["plate_evidence_index"], ensure_ascii=False, indent=2, sort_keys=True)
            + "\n",
            encoding="utf-8",
            newline="\n",
        )
    write_csv(root / INSCRIPTION_MAP, MAP_FIELDS, [output["map_row"] for output in outputs.values()])  # type: ignore[list-item]
    write_bucket_manifests(root, outputs)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=repo_root())
    args = parser.parse_args(argv)

    root = args.root.resolve()
    outputs = build_outputs(root)
    write_outputs(root, outputs)
    print(f"inscription_crosswalk_candidate_count={len(outputs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
