#!/usr/bin/env python3
"""Build object-local materials for Cambridge/Hopkins inscription crosswalk candidates."""

from __future__ import annotations

import argparse
import csv
import json
import re
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
UPDATED_AT = "2026-06-20"
BUCKET_SIZE = 100

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
    refs = "\n".join(
        f"- {ref['reference_type']}: {ref['reference_value'] or '(blank)'} "
        f"[{ref['reference_status']}]"
        for ref in catalog_rows
    )
    missing = [
        ref["reference_type"]
        for ref in catalog_rows
        if ref["reference_status"] == "missing_or_unassigned"
    ]
    missing_text = ", ".join(missing) if missing else "none"
    return f"""# {project_id} Cambridge/Hopkins inscription crosswalk candidate

English:
This is an object-local research entrance for a Cambridge/Hopkins inscription crosswalk candidate. The human-readable notes, plate/catalog routes, and AI-readable indexes are stored in this same concrete `corpus/002_oracle-bone-inscriptions` object directory.

Simplified Chinese:
这是 Cambridge/Hopkins 卜辞目录互证候选的对象内研究入口。人类可读说明、图版/著录路线和 AI 可读索引都放在同一个具体 `corpus/002_oracle-bone-inscriptions` 对象目录内，不另建并行的人类目录。

## Boundary / 边界

- This is not a formal `obi-*` inscription record.
- This is not an object identity claim.
- This is not a transcription or inscription reading.
- This is not a decipherment conclusion.
- 这不是正式 `obi-*` 卜辞记录，不是馆藏对象同一性结论，不是释文或卜辞读法，也不是释读结论。

## Local Files / 本目录文件

- `01_candidate-inscription-crosswalk-packet.json`: AI-readable candidate packet.
- `02_crosswalk-source-index.csv`: source, rights, and route index.
- `03_catalog-reference-index.csv`: Yingguo, CUL, Chalfant, and Heji reference index.
- `04_human-review-sheet.md`: human review sheet for catalog and image/context checks.
- `05_plate-text-route-index.csv`: plate, image, catalog, and text-evidence route index.
- `06_plate-text-gallery.md`: human-readable route gallery for finding plate/image/text evidence.

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

Current status: `route_indexed_not_collected`. Open `06_plate-text-gallery.md` in this same object directory to see the human-readable route list for source images, object records, Heji/OBM records, and catalog entries. No image, OCR text, transcription, reading, or object identity is confirmed here.

当前状态：`route_indexed_not_collected`。请打开同目录的 `05_plate-text-gallery.md` 查看图版、馆藏对象、合集/OBM 对应和著录证据路线。本文件不确认图片、OCR、释文、读法或对象同一性。

## Review Status / 复核状态

Current status: `needs_human_inscription_crosswalk_review`. Reviewers must compare the row against primary catalog/object records, Heji/OBM records, and source images before any formal `obi-*` assignment.

Generated row index: `{index}`.
"""
    return f"""# {project_id} Cambridge/Hopkins inscription crosswalk candidate

English:
This is an object-local research entrance for a Cambridge/Hopkins inscription crosswalk candidate. The human-readable notes and AI-readable indexes are stored in this same concrete `corpus/002_oracle-bone-inscriptions` object directory.

Simplified Chinese:
这是 Cambridge/Hopkins 卜辞目录互证候选的对象内研究入口。人类可读说明和 AI 可读索引放在同一个具体 `corpus/002_oracle-bone-inscriptions` 对象目录内，不另建并行的人类目录。

## Boundary / 边界

- This is not a formal `obi-*` inscription record.
- This is not an object identity claim.
- This is not a transcription or inscription reading.
- This is not a decipherment conclusion.
- 这不是正式 `obi-*` 卜辞记录，不是馆藏对象同一性结论，不是释文或卜辞读法，也不是释读结论。

## Local Files / 本目录文件

- `01_candidate-inscription-crosswalk-packet.json`: AI-readable candidate packet.
- `02_crosswalk-source-index.csv`: source, rights, and route index.
- `03_catalog-reference-index.csv`: Yingguo, CUL, Chalfant, and Heji reference index.
- `04_human-review-sheet.md`: human review sheet for catalog and image/context checks.

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

## Review Status / 复核状态

Current status: `needs_human_inscription_crosswalk_review`. Reviewers must compare the row against primary catalog/object records, Heji/OBM records, and source images before any formal `obi-*` assignment.

Generated row index: `{index}`.
"""


def plate_text_gallery_text(
    row: dict[str, str],
    project_id: str,
    plate_routes: list[dict[str, str]],
) -> str:
    route_lines = "\n".join(
        (
            f"- `{route['route_type']}`: {route['route_label']} "
            f"`{route['reference_value'] or '(blank)'}` "
            f"[{route['evidence_status']}]"
        )
        for route in plate_routes
    )
    return f"""# Plate And Text Route Gallery / 图版与文本路线图
Project ID: `{project_id}`

Candidate crosswalk ID: `{row['candidate_inscription_crosswalk_id']}`

English:
This file is a human-readable object-local route gallery. It lists where a reviewer should look for plate images, object records, catalog entries, Heji/OBM references, OCR text, and full inscription context. It does not contain confirmed images or transcriptions.

简体中文：
本文件是对象内的人类可读路线图，用来提示复核者到哪里寻找图版图片、馆藏对象记录、著录条目、合集/OBM 对应、OCR 文本和完整卜辞上下文。这里不包含已确认图片或释文。

## Routes / 路线

{route_lines}

## Evidence Status / 证据状态

- Local plate image: `not_collected`
- Local OCR text: `not_collected`
- Full inscription transcription: `not_collected`
- Object identity: `not_confirmed_catalog_identity`
- Formal `obi-*` assignment: `not_assigned_formal_obi_id`

## Boundary / 边界

This route gallery is preprocessing infrastructure only. It is not a formal inscription record, not an image-rights decision, not a transcription, not an inscription reading, and not a decipherment conclusion.
"""


def review_sheet_text(row: dict[str, str], project_id: str) -> str:
    return f"""# Human Review Sheet / 人工复核单

Project ID: `{project_id}`

Candidate crosswalk ID: `{row['candidate_inscription_crosswalk_id']}`

## Required Checks / 必须复核

- Open `02_crosswalk-source-index.csv` and verify the source/download trail.
- Open `03_catalog-reference-index.csv` and compare all references against primary catalog or object records.
- Open `05_plate-text-route-index.csv` and `06_plate-text-gallery.md` before searching for images or inscription text.
- Confirm whether source images, object records, Heji/OBM records, and full inscription context have been collected.
- Do not assign a formal `obi-*` ID from this sheet alone.
- Do not record a transcription, inscription reading, object identity claim, or decipherment conclusion here.

## Current Evidence Status / 当前证据状态

- Image evidence: `route_indexed_not_collected`
- Text transcription: `route_indexed_not_collected`
- Collection object match: `not_collected`
- Formal inscription assignment: `not_assigned_formal_obi_id`
- Review status: `needs_human_inscription_crosswalk_review`

## Caution / 风险提示

{CAUTION}
"""


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
