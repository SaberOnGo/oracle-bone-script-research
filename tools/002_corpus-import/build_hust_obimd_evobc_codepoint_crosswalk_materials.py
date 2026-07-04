#!/usr/bin/env python3
"""Build object-local materials for HUST/OBIMD/EVOBC codepoint crosswalks."""

from __future__ import annotations

import argparse
import csv
import json
import textwrap
from pathlib import Path


CODEPOINT_CROSSWALK = Path(
    "corpus/001_oracle-characters/000_character-registers/"
    "011_hust-obimd-evobc-codepoint-crosswalk-staging.csv"
)
SOURCE_INDEX = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/"
    "001_all-sources-index.csv"
)
DOWNLOAD_LOG = Path("project_registry/006_large-source-register/002_source-download-log.csv")
CODEPOINT_MAP = Path(
    "project_registry/002_project-id-to-source-reference-map/"
    "007_codepoint-crosswalk-id-source-map.csv"
)
OBJECT_ROOT = Path("corpus/001_oracle-characters")
UPDATED_AT = "2026-06-28"
BUCKET_SIZE = 100
FIRST_BUCKET_NUMBER = 112
MAX_HUMAN_LINE_LENGTH = 80
RECORD_TYPE = "codepoint_crosswalk_candidate"
RESEARCH_BOUNDARY = (
    "codepoint_crosswalk_candidate_metadata_only_not_identity_reading_component_"
    "evolution_or_decipherment_claim"
)
CAUTION = (
    "Codepoint crosswalk candidate only. Exact dataset-label codepoint matches "
    "are lookup routes, not confirmed oracle-character identity, not accepted "
    "readings, not component assignments, not evolution-chain assignments, "
    "and not decipherment conclusions."
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
    "source_route_id",
    "project_id",
    "crosswalk_candidate_id",
    "source_id",
    "primary_external_ref_id",
    "download_ids",
    "source_register_path",
    "download_log_path",
    "rights_status",
    "risk_note",
    "review_status",
    "research_boundary",
    "caution",
    "updated_at",
]

ROUTE_INDEX_FIELDS = [
    "route_id",
    "project_id",
    "crosswalk_candidate_id",
    "route_type",
    "route_label",
    "route_path",
    "route_status",
    "human_action",
    "ai_action",
    "rights_status",
    "review_status",
    "caution",
    "updated_at",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def paragraph(text: str, width: int = 76) -> str:
    return textwrap.fill(
        " ".join(text.split()),
        width=width,
        break_long_words=False,
        break_on_hyphens=False,
    )


def bullet(text: str, width: int = 74) -> str:
    wrapped = textwrap.wrap(
        " ".join(text.split()),
        width=width,
        break_long_words=False,
        break_on_hyphens=False,
    )
    if not wrapped:
        return "-"
    lines = [f"- {wrapped[0]}"]
    lines.extend(f"  {line}" for line in wrapped[1:])
    return "\n".join(lines)


def assert_human_line_width(path_label: str, text: str) -> None:
    for line_number, line in enumerate(text.splitlines(), start=1):
        if line.startswith("|") or line.startswith("!["):
            continue
        if len(line) > MAX_HUMAN_LINE_LENGTH:
            raise ValueError(
                f"{path_label}:{line_number} exceeds "
                f"{MAX_HUMAN_LINE_LENGTH} characters: {line}"
            )


def split_semicolon(value: str) -> list[str]:
    return [item for item in value.split(";") if item]


def project_id_for_index(index: int) -> str:
    return f"obs-xwalk-cand-{index:06d}"


def object_dir_for_index(index: int, row: dict[str, str]) -> Path:
    bucket_zero = (index - 1) // BUCKET_SIZE
    bucket_number = FIRST_BUCKET_NUMBER + bucket_zero
    bucket_start = bucket_zero * BUCKET_SIZE + 1
    bucket_end = min(bucket_start + BUCKET_SIZE - 1, 1588)
    item_in_bucket = index - bucket_start + 1
    project_id = project_id_for_index(index)
    short_external_id = f"xwalk-{index:06d}"
    bucket_dir = (
        f"{bucket_number:03d}_{bucket_start:06d}-{bucket_end:06d}_"
        "obs-xwalk-bucket_codepoint-xwalk"
    )
    object_name = (
        f"{item_in_bucket:03d}_{project_id}_{short_external_id}_"
        "codepoint-xwalk"
    )
    return OBJECT_ROOT / bucket_dir / object_name


def matched_source_ids(row: dict[str, str]) -> list[str]:
    return split_semicolon(row.get("matched_source_ids", ""))


def external_refs(row: dict[str, str]) -> list[str]:
    refs = [row["crosswalk_candidate_id"], row["hust_primary_external_ref_id"]]
    refs.extend(split_semicolon(row.get("obimd_primary_external_ref_ids", "")))
    refs.extend(split_semicolon(row.get("evobc_primary_external_ref_ids", "")))
    return [item for item in refs if item]


def download_ids_for_source(source_id: str, download_rows: list[dict[str, str]]) -> list[str]:
    return [
        row["download_id"]
        for row in download_rows
        if row.get("source_id") == source_id and row.get("download_id")
    ]


def risk_note_for_source(source_id: str, source_rows: list[dict[str, str]]) -> str:
    for row in source_rows:
        if row.get("source_id") == source_id:
            return row.get("risk_note", "")
    return ""


def source_ref_for_id(source_id: str, row: dict[str, str]) -> str:
    if source_id == "src-hust-obc":
        return row.get("hust_primary_external_ref_id", "")
    if source_id == "src-obimd":
        return row.get("obimd_primary_external_ref_ids", "")
    if source_id == "src-evobc":
        return row.get("evobc_primary_external_ref_ids", "")
    return ""


def build_packet(
    index: int,
    row: dict[str, str],
    object_dir: Path,
) -> dict[str, object]:
    project_id = project_id_for_index(index)
    return {
        "project_id": project_id,
        "record_type": RECORD_TYPE,
        "object_dir": object_dir.as_posix(),
        "crosswalk_candidate_id": row["crosswalk_candidate_id"],
        "suggested_oracle_character_id": row["suggested_oracle_character_id"],
        "promotion_queue_id": row["promotion_queue_id"],
        "hust_primary_external_ref_id": row["hust_primary_external_ref_id"],
        "hust_source_category_id": row["hust_source_category_id"],
        "hust_label_candidate": row["hust_label_candidate"],
        "hust_label_codepoints": row["hust_label_codepoints"],
        "label_component_count": row["label_component_count"],
        "has_multi_component_label": row["has_multi_component_label"],
        "candidate_packet_path": row["candidate_packet_path"],
        "obimd_match_count": row["obimd_match_count"],
        "obimd_candidate_main_character_ids": split_semicolon(
            row.get("obimd_candidate_main_character_ids", "")
        ),
        "obimd_primary_external_ref_ids": split_semicolon(
            row.get("obimd_primary_external_ref_ids", "")
        ),
        "evobc_match_count": row["evobc_match_count"],
        "evobc_candidate_evolution_category_ids": split_semicolon(
            row.get("evobc_candidate_evolution_category_ids", "")
        ),
        "evobc_primary_external_ref_ids": split_semicolon(
            row.get("evobc_primary_external_ref_ids", "")
        ),
        "evobc_image_reference_count_total": row["evobc_image_reference_count_total"],
        "matched_source_ids": matched_source_ids(row),
        "match_basis": row["match_basis"],
        "cross_source_status": row["cross_source_status"],
        "identity_claim_status": row["identity_claim_status"],
        "promotion_status": row["promotion_status"],
        "rights_status": row["rights_status"],
        "review_status": row["review_status"],
        "route_files": split_semicolon(row.get("route_files", "")),
        "local_human_files": [
            "README.md",
            "04_human-codepoint-crosswalk-review-sheet.md",
            "05_codepoint-crosswalk-route-gallery.md",
            "06_human-codepoint-crosswalk-dossier.md",
            "08_codepoint-crosswalk-fact-matrix.md",
            "10_cross-source-conflict-review.md",
            "12_modern-label-boundary-review.md",
            "14_codepoint-research-readiness-review.md",
        ],
        "local_ai_support_files": [
            "01_codepoint-crosswalk-packet.json",
            "02_codepoint-crosswalk-source-index.csv",
            "03_codepoint-crosswalk-route-index.csv",
            "07_codepoint-crosswalk-dossier-index.json",
            "09_codepoint-crosswalk-fact-matrix-index.json",
            "11_cross-source-conflict-index.json",
            "13_modern-label-boundary-index.json",
            "15_codepoint-research-readiness-index.json",
        ],
        "research_boundary": RESEARCH_BOUNDARY,
        "caution": CAUTION,
        "updated_at": UPDATED_AT,
    }


def build_source_rows(
    project_id: str,
    row: dict[str, str],
    source_rows: list[dict[str, str]],
    download_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, source_id in enumerate(matched_source_ids(row), start=1):
        rows.append(
            {
                "source_route_id": f"{project_id}-source-route-{index:02d}",
                "project_id": project_id,
                "crosswalk_candidate_id": row["crosswalk_candidate_id"],
                "source_id": source_id,
                "primary_external_ref_id": source_ref_for_id(source_id, row),
                "download_ids": ";".join(download_ids_for_source(source_id, download_rows)),
                "source_register_path": SOURCE_INDEX.as_posix(),
                "download_log_path": DOWNLOAD_LOG.as_posix(),
                "rights_status": row["rights_status"],
                "risk_note": risk_note_for_source(source_id, source_rows),
                "review_status": row["review_status"],
                "research_boundary": RESEARCH_BOUNDARY,
                "caution": CAUTION,
                "updated_at": UPDATED_AT,
            }
        )
    return rows


def route_rows_for_candidate(project_id: str, row: dict[str, str]) -> list[dict[str, str]]:
    route_files = split_semicolon(row.get("route_files", ""))
    route_items = [
        (
            "staging",
            "Codepoint crosswalk staging",
            CODEPOINT_CROSSWALK.as_posix(),
            "open row before any human claim",
            "machine source for this object-local packet",
        ),
        (
            "hust_packet",
            "HUST candidate route",
            row["candidate_packet_path"],
            "open packet and local glyph dossier first",
            "joins HUST candidate route to this packet",
        ),
        (
            "source_index",
            "All source register",
            SOURCE_INDEX.as_posix(),
            "check title, scope, rights, and risk note",
            "source metadata lookup route",
        ),
        (
            "download_log",
            "Large source download log",
            DOWNLOAD_LOG.as_posix(),
            "check checksum, size, status, and risk note",
            "download provenance lookup route",
        ),
    ]
    for route_file in route_files:
        if "006_obimd-main-character-staging.csv" in route_file:
            route_items.append(
                (
                    "obimd_staging",
                    "OBIMD route",
                    route_file,
                    "open matched OBIMD rows when present",
                    "OBIMD codepoint lookup route",
                )
            )
        if "001_evobc-evolution-category-staging.csv" in route_file:
            route_items.append(
                (
                    "evobc_staging",
                    "EVOBC route",
                    route_file,
                    "open matched EVOBC rows when present",
                    "EVOBC codepoint lookup route",
                )
            )
    rows: list[dict[str, str]] = []
    for index, (route_type, label, path, human_action, ai_action) in enumerate(
        route_items,
        start=1,
    ):
        rows.append(
            {
                "route_id": f"{project_id}-route-{index:02d}",
                "project_id": project_id,
                "crosswalk_candidate_id": row["crosswalk_candidate_id"],
                "route_type": route_type,
                "route_label": label,
                "route_path": path,
                "route_status": "route_present_candidate_only",
                "human_action": human_action,
                "ai_action": ai_action,
                "rights_status": row["rights_status"],
                "review_status": row["review_status"],
                "caution": CAUTION,
                "updated_at": UPDATED_AT,
            }
        )
    return rows


def source_table(row: dict[str, str]) -> str:
    return "\n".join(
        [
            "| Source / 来源 | Candidate route / 候选路线 | Status / 状态 |",
            "|---|---|---|",
            (
                f"| HUST-OBC | `{row['hust_primary_external_ref_id']}` | "
                "source label route |"
            ),
            (
                f"| OBIMD | `{row.get('obimd_primary_external_ref_ids') or 'pending route'}` | "
                f"{row['obimd_match_count']} codepoint match rows |"
            ),
            (
                f"| EVOBC | `{row.get('evobc_primary_external_ref_ids') or 'pending route'}` | "
                f"{row['evobc_match_count']} codepoint match rows |"
            ),
        ]
    )


def route_table(route_rows: list[dict[str, str]]) -> str:
    lines = [
        "| Route / 路线 | File / 文件 | Human action / 人工动作 |",
        "|---|---|---|",
    ]
    for row in route_rows:
        lines.append(
            f"| {row['route_label']} | `{row['route_path']}` | "
            f"{row['human_action']} |"
        )
    return "\n".join(lines)


def concrete_questions(row: dict[str, str]) -> list[str]:
    return [
        (
            "Which real glyph image, rubbing, or photograph should be opened "
            "before trusting this codepoint route?"
        ),
        (
            "Which inscription context, plate number, catalog number, findspot, "
            "collection, period, and group records can be tied to the route?"
        ),
        (
            "Does the HUST label describe a source label only, or is there a "
            "reviewed palaeographic argument in cited literature?"
        ),
        (
            "Do the OBIMD or EVOBC rows provide independent evidence, or only a "
            "shared Unicode dataset label?"
        ),
        (
            "Which later bronze, seal, modern-form, bibliography, proposer, "
            "or dispute notes still need to be opened from source routes?"
        ),
    ]


def human_comparison_order_markdown() -> str:
    return "\n".join(
        [
            "## Human Comparison Order / 人工比对顺序",
            "",
            bullet("Open the matched oracle-character human dossier first."),
            bullet("Open local glyph images, rubbing routes, and plate routes."),
            bullet("Compare OBIMD and EVOBC rows only after the glyph dossier."),
            bullet("Record disagreement before any promotion review."),
            bullet("Do not promote this codepoint route into identity."),
        ]
    )


def render_readme(project_id: str, row: dict[str, str]) -> str:
    lines = [
        f"# {project_id} Codepoint Crosswalk Candidate",
        "",
        "## Object-Local Research Entrance / 对象内研究入口",
        "",
        paragraph(
            "This is an object-local research entrance for a HUST-OBC, OBIMD, "
            "and EVOBC codepoint crosswalk candidate. It keeps human review "
            "materials and AI support files together in this candidate folder."
        ),
        "",
        paragraph(
            "这是一个候选跨来源码位路线档案。人类研究者应先打开字形图片、"
            "拓片、照片、著录、卜辞、出处和争议路线，再决定是否继续复核。"
        ),
        "",
        "## Boundary / 边界",
        "",
        bullet(CAUTION),
        bullet("This folder is not confirmed oracle-character identity."),
        bullet("This folder is not accepted readings."),
        bullet("This folder is not component assignments."),
        bullet("This folder is not evolution-chain assignments."),
        bullet("This folder is not decipherment conclusions."),
        "",
        "## Human Files / 人类可读文件",
        "",
        bullet("04_human-codepoint-crosswalk-review-sheet.md"),
        bullet("05_codepoint-crosswalk-route-gallery.md"),
        bullet("06_human-codepoint-crosswalk-dossier.md"),
        bullet("08_codepoint-crosswalk-fact-matrix.md"),
        bullet("10_cross-source-conflict-review.md"),
        bullet("12_modern-label-boundary-review.md"),
        bullet("14_codepoint-research-readiness-review.md"),
        "",
        "## AI Support Files / AI 辅助文件",
        "",
        bullet("01_codepoint-crosswalk-packet.json"),
        bullet("02_codepoint-crosswalk-source-index.csv"),
        bullet("03_codepoint-crosswalk-route-index.csv"),
        bullet("07_codepoint-crosswalk-dossier-index.json"),
        bullet("09_codepoint-crosswalk-fact-matrix-index.json"),
        bullet("11_cross-source-conflict-index.json"),
        bullet("13_modern-label-boundary-index.json"),
        bullet("15_codepoint-research-readiness-index.json"),
        "",
        "## Concrete Questions To Check / 具体待查问题",
        "",
    ]
    lines.extend(bullet(question) for question in concrete_questions(row))
    text = "\n".join(lines) + "\n"
    assert_human_line_width(f"{project_id}/README.md", text)
    return text


def render_review_sheet(project_id: str, row: dict[str, str]) -> str:
    lines = [
        f"# {project_id} Human Codepoint Crosswalk Review Sheet",
        "",
        "## Review Order / 复核顺序",
        "",
        bullet("Open the local HUST candidate packet and visual dossier first."),
        bullet("Record which glyph image, rubbing, photo, or plate is visible."),
        bullet("Check the source label codepoint before using any source match."),
        bullet("Open OBIMD and EVOBC rows only as lookup routes."),
        bullet("Write disagreement, missing evidence, and next source questions."),
        "",
        "## Candidate Snapshot / 候选概览",
        "",
        source_table(row),
        "",
        "## Concrete Questions To Check / 具体待查问题",
        "",
    ]
    lines.extend(bullet(question) for question in concrete_questions(row))
    lines.extend(
        [
            "",
            "## Boundary / 边界",
            "",
            bullet(CAUTION),
        ]
    )
    text = "\n".join(lines) + "\n"
    assert_human_line_width(
        f"{project_id}/04_human-codepoint-crosswalk-review-sheet.md",
        text,
    )
    return text


def render_route_gallery(
    project_id: str,
    row: dict[str, str],
    route_rows: list[dict[str, str]],
) -> str:
    lines = [
        f"# {project_id} Codepoint Crosswalk Route Gallery",
        "",
        "## Route Gallery / 路线索引",
        "",
        paragraph(
            "This gallery lists the local evidence routes a human reviewer "
            "should open. It is a route gallery, not a source-image gallery, "
            "because the crosswalk still needs human source review."
        ),
        "",
        route_table(route_rows),
        "",
        "## Visual And Text Evidence Still Needed / 仍需打开的证据",
        "",
        bullet("Glyph image route from the HUST candidate packet."),
        bullet("Rubbing or photograph route, if the cited source exposes one."),
        bullet("Inscription context route with plate and catalog evidence."),
        bullet("Bibliography route for reading history and disagreement notes."),
        "",
        "## Boundary / 边界",
        "",
        bullet(CAUTION),
    ]
    text = "\n".join(lines) + "\n"
    assert_human_line_width(
        f"{project_id}/05_codepoint-crosswalk-route-gallery.md",
        text,
    )
    return text


def render_dossier(project_id: str, row: dict[str, str]) -> str:
    lines = [
        f"# {project_id} Human Codepoint Crosswalk Dossier",
        "",
        "## Dossier Scope / 档案范围",
        "",
        paragraph(
            "This dossier is for human palaeographic and archaeological review "
            "of a codepoint lookup route. It gathers what must be opened before "
            "any stronger claim can be reviewed."
        ),
        "",
        "## Source Codepoint Route / 来源码位路线",
        "",
        source_table(row),
        "",
        human_comparison_order_markdown(),
        "",
        "## Material Evidence To Open / 需打开的实物证据",
        "",
        bullet("glyph image, rubbing, and photograph routes"),
        bullet("inscription context, plate image, and catalog number routes"),
        bullet("findspot, collection, period, batch, and group records"),
        bullet("variant, near-form, and component clue review notes"),
        bullet("bronze, seal, and modern-form correspondence routes"),
        "",
        "## Reading History And Dispute Route / 释读史与争议路线",
        "",
        bullet("Open bibliography before writing any accepted reading."),
        bullet("Record proposer, evidence level, and disagreement notes."),
        bullet("Keep unmatched source labels as candidates pending review."),
        "",
        "## Concrete Questions To Check / 具体待查问题",
        "",
    ]
    lines.extend(bullet(question) for question in concrete_questions(row))
    lines.extend(
        [
            "",
            "## Boundary / 边界",
            "",
            bullet(CAUTION),
        ]
    )
    text = "\n".join(lines) + "\n"
    assert_human_line_width(
        f"{project_id}/06_human-codepoint-crosswalk-dossier.md",
        text,
    )
    return text


def render_fact_matrix(
    project_id: str,
    row: dict[str, str],
    route_rows: list[dict[str, str]],
) -> str:
    lines = [
        f"# {project_id} Codepoint Crosswalk Fact Matrix",
        "",
        "## Human Review Order / 人类复核顺序",
        "",
        bullet("1. Open the HUST candidate route and local glyph materials."),
        bullet("2. Check the Source Codepoint Route against the staging row."),
        bullet("3. Open the OBIMD route only if a match row is present."),
        bullet("4. Open the EVOBC route only if a match row is present."),
        bullet("5. Write missing evidence before any promotion review."),
        "",
        "## Fact Matrix / 事实矩阵",
        "",
        "| Slot / 项目 | Current route evidence / 当前路线证据 | Review boundary / 复核边界 |",
        "|---|---|---|",
        (
            f"| Source Codepoint Route / 来源码位路线 | `{row['hust_label_codepoints']}` | "
            "not identity |"
        ),
        (
            f"| HUST candidate route / HUST 候选路线 | `{row['hust_primary_external_ref_id']}` | "
            "not reading |"
        ),
        (
            f"| OBIMD route / OBIMD 路线 | `{row.get('obimd_candidate_main_character_ids') or 'pending route'}` | "
            "not component |"
        ),
        (
            f"| EVOBC route / EVOBC 路线 | `{row.get('evobc_candidate_evolution_category_ids') or 'pending route'}` | "
            "not evolution |"
        ),
        (
            f"| Source and rights trail / 来源与权利链 | `{row['rights_status']}` | "
            "source-marked risk note required |"
        ),
        (
            f"| Missing evidence route / 缺失证据路线 | `{row['cross_source_status']}` | "
            "not decipherment |"
        ),
        (
            f"| Review status / 复核状态 | `{row['review_status']}` | "
            "needs human cross-source review |"
        ),
        "",
        human_comparison_order_markdown(),
        "",
        "## Required Routes / 必查路线",
        "",
        route_table(route_rows),
        "",
        "## Required Files / 必查文件",
        "",
        bullet("011_hust-obimd-evobc-codepoint-crosswalk-staging.csv"),
        bullet("01_candidate-character-packet.json"),
        bullet("006_obimd-main-character-staging.csv"),
        bullet("001_evobc-evolution-category-staging.csv"),
        bullet("001_all-sources-index.csv"),
        bullet("002_source-download-log.csv"),
        "",
        "## Boundary / 边界",
        "",
        bullet(
            "This matrix records lookup-route facts only: not identity, not "
            "reading, not component, not evolution, and not decipherment."
        ),
    ]
    text = "\n".join(lines) + "\n"
    assert_human_line_width(
        f"{project_id}/08_codepoint-crosswalk-fact-matrix.md",
        text,
    )
    return text


def source_presence_table(row: dict[str, str]) -> str:
    matched_ids = matched_source_ids(row)
    rows = [
        "| Source id | Evidence route | Human conflict question |",
        "|---|---|---|",
        (
            f"| src-hust-obc | `{row['hust_primary_external_ref_id']}` | "
            "Does the label match a visible glyph source? |"
        ),
        (
            f"| src-obimd | `{row.get('obimd_primary_external_ref_ids') or 'absent in match set'}` | "
            f"Are {row['obimd_match_count']} match rows independent evidence? |"
        ),
        (
            f"| src-evobc | `{row.get('evobc_primary_external_ref_ids') or 'absent in match set'}` | "
            f"Are {row['evobc_match_count']} evolution rows only codepoint clues? |"
        ),
        (
            f"| matched_source_ids | `{';'.join(matched_ids)}` | "
            "Which source ids agree only by codepoint? |"
        ),
    ]
    return "\n".join(rows)


def render_conflict_review(project_id: str, row: dict[str, str]) -> str:
    absent_sources = [
        source_id
        for source_id in ["src-obimd", "src-evobc"]
        if source_id not in matched_source_ids(row)
    ]
    absent_source_text = "; ".join(absent_sources) if absent_sources else "none"
    lines = [
        f"# {project_id} Cross-Source Conflict Review",
        "",
        "## Review Purpose / 复核目的",
        "",
        paragraph(
            "This human review sheet turns cross-source codepoint agreement "
            "and disagreement into explicit questions. Any source "
            "disagreement must be recorded before this route can support "
            "a stronger object review."
        ),
        "",
        bullet("Codepoint agreement is a lookup clue only."),
        bullet("source disagreement must be recorded."),
        bullet("No source match may be promoted into identity here."),
        bullet("No reading, component, evolution, or decipherment claim is made."),
        "",
        "## Candidate Source State / 候选来源状态",
        "",
        source_presence_table(row),
        "",
        "## Source Notes To Compare / 需比对的来源说明",
        "",
        bullet(f"HUST label: {row['hust_label_candidate']}"),
        bullet(f"HUST label codepoints: {row['hust_label_codepoints']}"),
        bullet(f"OBIMD match rows: {row['obimd_match_count']}"),
        bullet(f"EVOBC match rows: {row['evobc_match_count']}"),
        bullet(f"Absent source ids for this candidate: {absent_source_text}"),
        bullet(f"Current cross-source status: {row['cross_source_status']}"),
        "",
        "## Research Slots To Open / 需打开的研究项",
        "",
        bullet("Glyph image, rubbing, photograph, and visual observation notes."),
        bullet("Inscription text, OCR, plate, catalog, and collection records."),
        bullet("Findspot, collection, period, batch, and group evidence."),
        bullet("Variant, near-form, component, and relation comparison notes."),
        bullet("Reading history, proposer, bibliography, and dispute records."),
        bullet("Bronze, seal, modern-form, and evolution comparison materials."),
        "",
        "## Concrete Conflict Questions / 具体冲突待查问题",
        "",
        bullet("Which source ids agree only by codepoint?"),
        bullet("Which sources are absent for this candidate?"),
        bullet("Which bibliography or plate route can test the disagreement?"),
        bullet("Does any source cite a visible glyph, rubbing, or photograph?"),
        bullet("Does any source provide proposer, period, group, or findspot data?"),
        bullet("Which variant or component relation still needs source evidence?"),
        "",
        human_comparison_order_markdown(),
        "",
        "## Boundary / 边界",
        "",
        bullet(CAUTION),
    ]
    text = "\n".join(lines) + "\n"
    assert_human_line_width(
        f"{project_id}/10_cross-source-conflict-review.md",
        text,
    )
    return text


def render_modern_label_boundary_review(project_id: str, row: dict[str, str]) -> str:
    lines = [
        f"# {project_id} Modern Label Boundary Review",
        "",
        "## Review Purpose / 复核目的",
        "",
        paragraph(
            "This human review page separates modern labels, Unicode "
            "codepoints, dataset labels, and later-form hints from the "
            "oracle-bone sign itself. A label may help locate evidence, but "
            "it cannot become the character identity without source review."
        ),
        "",
        paragraph(
            "本页把现代标签、Unicode 码位、数据集标签和后世字形线索，"
            "同甲骨字形本身分开。标签可以帮助定位证据，但未经来源复核，"
            "不能写成这个甲骨字的身份。"
        ),
        "",
        "## Current Label Clues / 当前标签线索",
        "",
        bullet(f"HUST label candidate: {row['hust_label_candidate']}"),
        bullet(f"HUST label codepoints: {row['hust_label_codepoints']}"),
        bullet(f"Label component count: {row['label_component_count']}"),
        bullet(f"Multi-component label: {row['has_multi_component_label']}"),
        bullet(f"Match basis: {row['match_basis']}"),
        bullet(f"Cross-source status: {row['cross_source_status']}"),
        "",
        "## Evidence To Open Before Identity / 身份判断前必须打开",
        "",
        bullet("Visible glyph image, rubbing, photograph, or hand copy."),
        bullet("Inscription context, OCR text, plate, catalog, and Heji route."),
        bullet("Findspot, collection, period, group, batch, and object record."),
        bullet("Variant, near-form, component, and source disagreement notes."),
        bullet("Bronze, seal, modern-form, bibliography, proposer, and dispute."),
        bullet("可见字形图像、拓片、照片或摹本。"),
        bullet("卜辞语境、OCR 全文、图版、著录和合集路线。"),
        bullet("出土地、馆藏、时期、组类、批次和馆藏对象记录。"),
        bullet("异体、近形、构件和来源分歧说明。"),
        bullet("金文、小篆、今字、书目、提出者和争议。"),
        "",
        "## Concrete Boundary Questions / 具体边界问题",
        "",
        bullet("Is the modern label only a source lookup clue?"),
        bullet("Which visible glyph evidence supports or conflicts with it?"),
        bullet("Which inscription or plate route can test the label?"),
        bullet("Which bibliography or proposer argues for the reading?"),
        bullet("Which OBIMD or EVOBC row repeats only a Unicode codepoint?"),
        bullet("Which dispute or missing source blocks promotion?"),
        bullet("现代标签是否只是来源检索线索？"),
        bullet("哪条可见字形证据支持或冲突于该标签？"),
        bullet("哪条卜辞或图版路线可以检验标签？"),
        bullet("哪条书目或提出者记录论证了释读？"),
        bullet("哪条 OBIMD 或 EVOBC 行只是重复 Unicode 码位？"),
        bullet("哪项争议或缺失来源阻止提升？"),
        "",
        human_comparison_order_markdown(),
        "",
        "## Boundary / 边界",
        "",
        bullet("Modern labels are lookup metadata, not oracle-character identity."),
        bullet("Unicode codepoints are lookup metadata, not accepted readings."),
        bullet("Dataset labels are source records, not component assignments."),
        bullet("Later-form hints are comparison routes, not accepted evolution."),
        bullet("This is not a decipherment conclusion."),
        bullet("现代标签是检索 metadata，不是甲骨字身份。"),
        bullet("Unicode 码位是检索 metadata，不是已接受释读。"),
        bullet("数据集标签是来源记录，不是构件归属。"),
        bullet("后世字形线索是比较路线，不是已接受演化关系。"),
        bullet("这不是释读结论。"),
    ]
    text = "\n".join(lines) + "\n"
    assert_human_line_width(
        f"{project_id}/12_modern-label-boundary-review.md",
        text,
    )
    return text


def build_index(
    project_id: str,
    row: dict[str, str],
    human_files: list[str],
    ai_files: list[str],
    index_type: str,
) -> dict[str, object]:
    return {
        "project_id": project_id,
        "record_type": index_type,
        "crosswalk_candidate_id": row["crosswalk_candidate_id"],
        "human_readable_files": human_files,
        "ai_support_files": ai_files,
        "source_ids": matched_source_ids(row),
        "claim_boundary": (
            "candidate codepoint route only; no identity, reading, component, "
            "evolution, or decipherment conclusion"
        ),
        "review_status": row["review_status"],
        "updated_at": UPDATED_AT,
    }


def build_conflict_index(project_id: str, row: dict[str, str]) -> dict[str, object]:
    return {
        "project_id": project_id,
        "record_type": "codepoint_crosswalk_conflict_review_index",
        "crosswalk_candidate_id": row["crosswalk_candidate_id"],
        "human_readable_files": ["10_cross-source-conflict-review.md"],
        "ai_support_files": ["11_cross-source-conflict-index.json"],
        "source_ids": matched_source_ids(row),
        "absent_source_ids": [
            source_id
            for source_id in ["src-obimd", "src-evobc"]
            if source_id not in matched_source_ids(row)
        ],
        "claim_boundary": (
            "cross-source conflict review only; no identity claim, no reading, "
            "no component, no evolution, and no decipherment conclusion"
        ),
        "review_status": row["review_status"],
        "updated_at": UPDATED_AT,
    }


def build_modern_label_boundary_index(
    project_id: str,
    row: dict[str, str],
) -> dict[str, object]:
    return {
        "project_id": project_id,
        "record_type": "codepoint_modern_label_boundary_index",
        "crosswalk_candidate_id": row["crosswalk_candidate_id"],
        "human_readable_files": ["12_modern-label-boundary-review.md"],
        "ai_support_files": ["13_modern-label-boundary-index.json"],
        "label_boundary_slots": [
            "modern_label_candidate",
            "unicode_codepoint_route",
            "dataset_label_boundary",
            "visible_glyph_evidence",
            "inscription_or_plate_route",
            "bibliography_or_proposer",
            "source_dispute_or_missing_evidence",
        ],
        "hust_label_candidate": row["hust_label_candidate"],
        "hust_label_codepoints": row["hust_label_codepoints"],
        "match_basis": row["match_basis"],
        "claim_boundary": (
            "modern label boundary review only; label metadata is not "
            "oracle-character identity, not reading, not component, not "
            "evolution, and not decipherment conclusion"
        ),
        "review_status": row["review_status"],
        "updated_at": UPDATED_AT,
    }


def codepoint_readiness_slots(row: dict[str, str]) -> list[dict[str, str]]:
    return [
        {
            "slot": "candidate_identity_route",
            "status": "candidate_only",
            "human_question": "Which object-local packet and source row anchor this route?",
        },
        {
            "slot": "visible_glyph_evidence",
            "status": "needs_opened_visual_review",
            "human_question": "Which glyph image, rubbing, photo, or hand copy must be opened?",
        },
        {
            "slot": "inscription_plate_context",
            "status": "needs_source_context_review",
            "human_question": "Which inscription, plate, catalog, or Heji route can test it?",
        },
        {
            "slot": "cross_source_agreement",
            "status": row["cross_source_status"],
            "human_question": "Which sources agree only by codepoint or dataset label?",
        },
        {
            "slot": "modern_label_boundary",
            "status": "lookup_metadata_only",
            "human_question": "Which modern label is only a search clue?",
        },
        {
            "slot": "source_rights_manifest",
            "status": row["rights_status"],
            "human_question": "Which manifest, checksum, field map, rights note, and risk note apply?",
        },
        {
            "slot": "bibliography_or_proposer",
            "status": "needs_source_review",
            "human_question": "Which bibliography, proposer, or dispute route remains missing?",
        },
        {
            "slot": "formal_crosswalk_research_blockers",
            "status": "blocked_until_human_review",
            "human_question": "Which issue blocks formal codepoint crosswalk research?",
        },
    ]


def render_readiness_review(project_id: str, row: dict[str, str]) -> str:
    lines = [
        f"# {project_id} Codepoint Research Readiness Review",
        "",
        "## Purpose / 用途",
        "",
        paragraph(
            "This human page checks whether a codepoint crosswalk candidate has "
            "enough opened source evidence for later formal research. It does "
            "not approve a character identity, reading, component, or evolution "
            "correspondence."
        ),
        "",
        paragraph(
            "本页只复核代码点互证候选在正式研究前还缺哪些可打开证据。"
            "它不确认甲骨字身份、释读、构件归属或字形演化关系。"
        ),
        "",
        "## Human Reading Order / 人工阅读顺序",
        "",
        bullet("Open 04_human-codepoint-crosswalk-review-sheet.md first."),
        bullet("Open 06_human-codepoint-crosswalk-dossier.md next."),
        bullet("Open 10_cross-source-conflict-review.md before promotion review."),
        bullet("Open 12_modern-label-boundary-review.md before using labels."),
        bullet("Open source registers, download logs, and field maps last."),
        bullet("先读人工复核表，再读互证档案和来源冲突复核。"),
        bullet("使用现代标签或 Unicode 码位前，先读现代标签边界页。"),
        "",
        "## Readiness Slots / 就绪复核槽位",
        "",
    ]
    for slot in codepoint_readiness_slots(row):
        lines.append(
            bullet(
                f"{slot['slot']}: {slot['status']}; {slot['human_question']}"
            )
        )
    lines.extend(
        [
            "",
            "## Concrete Questions Before Formal Research / 正式研究前待查问题",
            "",
            bullet("Which source codepoint route needs direct human comparison?"),
            bullet("Which visible glyph evidence supports or conflicts with it?"),
            bullet("Which inscription, plate, catalog, or Heji route can test it?"),
            bullet("Which source rows agree only by Unicode or dataset label?"),
            bullet("Which modern label is only lookup metadata?"),
            bullet("Which bibliography, proposer, or dispute route is missing?"),
            bullet("Which manifest, checksum, field map, rights note, and risk note apply?"),
            bullet("Which issue blocks formal codepoint crosswalk research?"),
            bullet("哪条来源码位路线需要人工直接比对？"),
            bullet("哪条可见字形证据支持或冲突于该路线？"),
            bullet("哪条卜辞、图版、著录或合集路线可用于核查？"),
            bullet("哪些来源行只是共享 Unicode 或数据集标签？"),
            bullet("哪个现代标签只可作为检索 metadata？"),
            bullet("哪条书目、提出者或争议路线仍然缺失？"),
            "",
            "## Boundary / 边界",
            "",
            bullet("This is not an oracle-character identity confirmation."),
            bullet("This is not an accepted reading."),
            bullet("This is not a component assignment."),
            bullet("This is not an evolution correspondence."),
            bullet("This is not a decipherment conclusion."),
            bullet("本页不是甲骨字身份确认。"),
            bullet("本页不是已接受释读、构件归属、演化对应或破译结论。"),
        ]
    )
    text = "\n".join(lines) + "\n"
    assert_human_line_width(
        f"{project_id}/14_codepoint-research-readiness-review.md",
        text,
    )
    return text


def build_readiness_index(project_id: str, row: dict[str, str]) -> dict[str, object]:
    return {
        "project_id": project_id,
        "record_type": "codepoint_research_readiness_index",
        "crosswalk_candidate_id": row["crosswalk_candidate_id"],
        "human_entry": "14_codepoint-research-readiness-review.md",
        "human_readable_files": [
            "04_human-codepoint-crosswalk-review-sheet.md",
            "05_codepoint-crosswalk-route-gallery.md",
            "06_human-codepoint-crosswalk-dossier.md",
            "08_codepoint-crosswalk-fact-matrix.md",
            "10_cross-source-conflict-review.md",
            "12_modern-label-boundary-review.md",
            "14_codepoint-research-readiness-review.md",
        ],
        "ai_support_files": [
            "01_codepoint-crosswalk-packet.json",
            "02_codepoint-crosswalk-source-index.csv",
            "03_codepoint-crosswalk-route-index.csv",
            "07_codepoint-crosswalk-dossier-index.json",
            "09_codepoint-crosswalk-fact-matrix-index.json",
            "11_cross-source-conflict-index.json",
            "13_modern-label-boundary-index.json",
            "15_codepoint-research-readiness-index.json",
        ],
        "readiness_slots": codepoint_readiness_slots(row),
        "source_ids": matched_source_ids(row),
        "claim_boundary": (
            "codepoint readiness review only; no oracle-character identity "
            "confirmation, no accepted reading, no component assignment, no "
            "evolution correspondence, and no decipherment conclusion"
        ),
        "review_status": row["review_status"],
        "updated_at": UPDATED_AT,
    }


def build_outputs(root: Path) -> dict[str, dict[str, object]]:
    staging_rows = read_csv(root / CODEPOINT_CROSSWALK)
    source_rows = read_csv(root / SOURCE_INDEX)
    download_rows = read_csv(root / DOWNLOAD_LOG)
    outputs: dict[str, dict[str, object]] = {}
    for index, row in enumerate(staging_rows, start=1):
        project_id = project_id_for_index(index)
        object_dir = object_dir_for_index(index, row)
        packet = build_packet(index, row, object_dir)
        source_index_rows = build_source_rows(project_id, row, source_rows, download_rows)
        route_index_rows = route_rows_for_candidate(project_id, row)
        readme_text = render_readme(project_id, row)
        review_sheet_text = render_review_sheet(project_id, row)
        route_gallery_text = render_route_gallery(project_id, row, route_index_rows)
        dossier_text = render_dossier(project_id, row)
        fact_matrix_text = render_fact_matrix(project_id, row, route_index_rows)
        conflict_review_text = render_conflict_review(project_id, row)
        modern_label_boundary_text = render_modern_label_boundary_review(
            project_id,
            row,
        )
        readiness_review_text = render_readiness_review(project_id, row)
        human_files = packet["local_human_files"]
        ai_files = packet["local_ai_support_files"]
        outputs[project_id] = {
            "object_dir": object_dir,
            "packet": packet,
            "source_index_rows": source_index_rows,
            "route_index_rows": route_index_rows,
            "readme_text": readme_text,
            "review_sheet_text": review_sheet_text,
            "route_gallery_text": route_gallery_text,
            "dossier_text": dossier_text,
            "fact_matrix_text": fact_matrix_text,
            "conflict_review_text": conflict_review_text,
            "modern_label_boundary_text": modern_label_boundary_text,
            "readiness_review_text": readiness_review_text,
            "dossier_index": build_index(
                project_id,
                row,
                human_files,
                ai_files,
                "codepoint_crosswalk_dossier_index",
            ),
            "fact_matrix_index": build_index(
                project_id,
                row,
                human_files,
                ai_files,
                "codepoint_crosswalk_fact_matrix_index",
            ),
            "conflict_index": build_conflict_index(project_id, row),
            "modern_label_boundary_index": build_modern_label_boundary_index(
                project_id,
                row,
            ),
            "readiness_index": build_readiness_index(project_id, row),
            "map_row": {
                "project_id": project_id,
                "record_type": RECORD_TYPE,
                "canonical_path": object_dir.as_posix(),
                "primary_external_ref_id": row["crosswalk_candidate_id"],
                "all_external_ref_ids": ";".join(external_refs(row)),
                "source_ids": ";".join(matched_source_ids(row)),
                "rights_status": row["rights_status"],
                "review_status": row["review_status"],
                "updated_at": UPDATED_AT,
            },
        }
    return outputs


def write_outputs(root: Path, outputs: dict[str, dict[str, object]]) -> None:
    map_rows: list[dict[str, str]] = []
    for output in outputs.values():
        object_dir = root / output["object_dir"]
        object_dir.mkdir(parents=True, exist_ok=True)
        (object_dir / "README.md").write_text(output["readme_text"], encoding="utf-8")
        write_json(object_dir / "01_codepoint-crosswalk-packet.json", output["packet"])
        write_csv(
            object_dir / "02_codepoint-crosswalk-source-index.csv",
            output["source_index_rows"],
            SOURCE_INDEX_FIELDS,
        )
        write_csv(
            object_dir / "03_codepoint-crosswalk-route-index.csv",
            output["route_index_rows"],
            ROUTE_INDEX_FIELDS,
        )
        (object_dir / "04_human-codepoint-crosswalk-review-sheet.md").write_text(
            output["review_sheet_text"],
            encoding="utf-8",
        )
        (object_dir / "05_codepoint-crosswalk-route-gallery.md").write_text(
            output["route_gallery_text"],
            encoding="utf-8",
        )
        (object_dir / "06_human-codepoint-crosswalk-dossier.md").write_text(
            output["dossier_text"],
            encoding="utf-8",
        )
        write_json(object_dir / "07_codepoint-crosswalk-dossier-index.json", output["dossier_index"])
        (object_dir / "08_codepoint-crosswalk-fact-matrix.md").write_text(
            output["fact_matrix_text"],
            encoding="utf-8",
        )
        write_json(
            object_dir / "09_codepoint-crosswalk-fact-matrix-index.json",
            output["fact_matrix_index"],
        )
        (object_dir / "10_cross-source-conflict-review.md").write_text(
            output["conflict_review_text"],
            encoding="utf-8",
        )
        write_json(
            object_dir / "11_cross-source-conflict-index.json",
            output["conflict_index"],
        )
        (object_dir / "12_modern-label-boundary-review.md").write_text(
            output["modern_label_boundary_text"],
            encoding="utf-8",
        )
        write_json(
            object_dir / "13_modern-label-boundary-index.json",
            output["modern_label_boundary_index"],
        )
        (object_dir / "14_codepoint-research-readiness-review.md").write_text(
            output["readiness_review_text"],
            encoding="utf-8",
        )
        write_json(
            object_dir / "15_codepoint-research-readiness-index.json",
            output["readiness_index"],
        )
        map_rows.append(output["map_row"])
    write_csv(root / CODEPOINT_MAP, map_rows, MAP_FIELDS)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=Path.cwd(), type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    outputs = build_outputs(root)
    write_outputs(root, outputs)
    print(f"codepoint_crosswalk_object_count={len(outputs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
