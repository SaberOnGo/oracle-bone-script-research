#!/usr/bin/env python3
"""Build object-local human and AI material bundles for registered sources."""

from __future__ import annotations

import argparse
import csv
import json
import textwrap
from collections import defaultdict
from pathlib import Path


SOURCE_INDEX = Path("corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv")
DOWNLOAD_MANIFEST = Path("corpus/006_research-sources-and-bibliography/000_source-registers/003_source-download-manifest.csv")
DOWNLOAD_LOG = Path("project_registry/006_large-source-register/002_source-download-log.csv")
FIELD_MAP = Path("corpus/006_research-sources-and-bibliography/000_source-registers/007_source-field-map.csv")
PACKAGE_MANIFEST = Path("corpus/006_research-sources-and-bibliography/000_source-registers/009_source-package-file-manifest.csv")
METADATA_PROFILE = Path("corpus/006_research-sources-and-bibliography/000_source-registers/010_downloaded-metadata-profile.csv")
OUTPUT_ROOT = Path("corpus/006_research-sources-and-bibliography/001_source-objects")
UPDATED_AT = "2026-06-21"
MAX_HUMAN_LINE_LENGTH = 80


DOWNLOAD_ROUTE_FIELDS = [
    "route_id",
    "source_id",
    "download_id",
    "url",
    "artifact_kind",
    "commit_policy",
    "manifest_max_bytes",
    "manifest_notes",
    "download_status",
    "http_status",
    "file_size_bytes",
    "checksum_sha256",
    "local_temp_path",
    "risk_note",
    "review_status",
]

PACKAGE_ROUTE_FIELDS = [
    "package_route_id",
    "source_id",
    "package_file_id",
    "source_package_id",
    "file_name",
    "file_kind",
    "source_url",
    "file_size_bytes",
    "download_id",
    "commit_policy",
    "handling_strategy",
    "rights_status",
    "review_status",
    "updated_at",
]

FIELD_ROUTE_FIELDS = [
    "field_route_id",
    "source_id",
    "map_id",
    "source_level",
    "source_field_or_unit",
    "source_meaning",
    "target_record_type",
    "target_project_field",
    "import_action",
    "rights_boundary",
    "evidence_download_id",
    "review_status",
    "updated_at",
]

METADATA_ROUTE_FIELDS = [
    "metadata_route_id",
    "source_id",
    "profile_id",
    "evidence_download_id",
    "metadata_file",
    "profile_metric",
    "profile_value",
    "profile_unit",
    "import_relevance",
    "caution",
    "review_status",
    "updated_at",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows([{field: row.get(field, "") for field in fieldnames} for row in rows])


def write_json(path: Path, data: dict[str, object]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def wrapped(text: str, width: int = MAX_HUMAN_LINE_LENGTH) -> list[str]:
    return textwrap.wrap(
        text,
        width=width,
        break_long_words=True,
        break_on_hyphens=False,
    ) or [""]


def bullet(label: str, value: object) -> list[str]:
    prefix = f"- {label}: "
    text = str(value) if value not in (None, "") else "not recorded"
    return textwrap.wrap(
        prefix + text,
        width=MAX_HUMAN_LINE_LENGTH,
        subsequent_indent="  ",
        break_long_words=True,
        break_on_hyphens=False,
    )


def assert_human_line_width(path_label: str, text: str) -> None:
    for line_number, line in enumerate(text.splitlines(), start=1):
        if len(line) > MAX_HUMAN_LINE_LENGTH:
            raise ValueError(f"{path_label}:{line_number} exceeds 80 chars: {line}")


def write_human_markdown(path: Path, path_label: str, text: str) -> None:
    text = text.rstrip() + "\n"
    assert_human_line_width(path_label, text)
    path.write_text(text, encoding="utf-8")


def joined(values: list[str], fallback: str = "none") -> str:
    return "; ".join(values) if values else fallback


def source_dir_name(index: int, source_id: str) -> str:
    safe_source_id = "".join(ch if ch.isascii() and (ch.isalnum() or ch in "-_") else "-" for ch in source_id)
    return f"{index:03d}_{safe_source_id}_source-object"


def index_by_source(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    by_source: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_source[row.get("source_id", "")].append(row)
    return dict(by_source)


def build_download_routes(
    source_id: str,
    manifest_rows: list[dict[str, str]],
    log_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    log_by_download_id = {row["download_id"]: row for row in log_rows}
    routes = []
    for index, manifest in enumerate(manifest_rows, start=1):
        log = log_by_download_id.get(manifest["download_id"], {})
        routes.append(
            {
                "route_id": f"{source_id}-download-route-{index:03d}",
                "source_id": source_id,
                "download_id": manifest["download_id"],
                "url": manifest["url"],
                "artifact_kind": manifest["artifact_kind"],
                "commit_policy": manifest["commit_policy"],
                "manifest_max_bytes": manifest["max_bytes"],
                "manifest_notes": manifest["notes"],
                "download_status": log.get("status", "not_logged_yet"),
                "http_status": log.get("http_status", ""),
                "file_size_bytes": log.get("file_size_bytes", ""),
                "checksum_sha256": log.get("checksum_sha256", ""),
                "local_temp_path": log.get("local_temp_path", ""),
                "risk_note": log.get("risk_note", ""),
                "review_status": "metadata_route_needs_human_review",
            }
        )
    return routes


def add_route_ids(source_id: str, rows: list[dict[str, str]], key: str, prefix: str) -> list[dict[str, str]]:
    routed = []
    for index, row in enumerate(rows, start=1):
        routed.append({prefix: f"{source_id}-{key}-{index:03d}", **row})
    return routed


def source_packet(
    source: dict[str, str],
    object_dir: Path,
    download_routes: list[dict[str, str]],
    package_routes: list[dict[str, str]],
    field_routes: list[dict[str, str]],
    metadata_routes: list[dict[str, str]],
) -> dict[str, object]:
    return {
        "record_type": "source_object_packet",
        "source_id": source["source_id"],
        "source_type": source["source_type"],
        "title": source["title"],
        "provider": source["provider"],
        "authority_tier": source["authority_tier"],
        "source_url": source["source_url"],
        "scope": source["scope"],
        "adoption_status": source["adoption_status"],
        "download_strategy": source["download_strategy"],
        "rights_status": source["rights_status"],
        "risk_note": source["risk_note"],
        "review_status": source["review_status"],
        "object_dir": object_dir.as_posix(),
        "download_route_count": len(download_routes),
        "package_route_count": len(package_routes),
        "field_map_route_count": len(field_routes),
        "metadata_profile_route_count": len(metadata_routes),
        "local_files": [
            "README.md",
            "01_source-packet.json",
            "02_download-route-index.csv",
            "03_package-route-index.csv",
            "04_field-map-route-index.csv",
            "05_metadata-profile-route-index.csv",
            "06_human-source-review-sheet.md",
            "07_material-access-index.md",
            "08_source-processing-status.md",
            "09_source-processing-status-index.json",
            "10_source-evidence-dossier.md",
            "11_source-evidence-dossier-index.json",
            "12_source-provenance-fact-matrix.md",
            "13_source-provenance-fact-matrix-index.json",
            "14_source-to-dossier-transfer-review.md",
            "15_source-to-dossier-transfer-index.json",
            "16_source-literature-scope-review.md",
            "17_source-literature-scope-index.json",
            "18_source-access-integrity-review.md",
            "19_source-access-integrity-index.json",
            "20_source-presearch-readiness-review.md",
            "21_source-presearch-readiness-index.json",
            "22_source-research-brief.md",
        ],
        "research_boundary": (
            "source_object_packet_preprocessing_only; source metadata, routes, "
            "download logs, package manifests, field maps, and status cards are "
            "not decipherment, identity, component, inscription, or "
            "correspondence conclusions"
        ),
        "decipherment_claim_status": "no_claim",
        "updated_at": UPDATED_AT,
    }


def phase_status(row_count: int, ready_status: str) -> str:
    if row_count:
        return ready_status
    return "not_present_in_current_registers"


def checksum_count(download_routes: list[dict[str, str]]) -> int:
    return sum(1 for row in download_routes if row.get("checksum_sha256"))


def sized_count(download_routes: list[dict[str, str]]) -> int:
    return sum(1 for row in download_routes if row.get("file_size_bytes"))


def local_temp_count(download_routes: list[dict[str, str]]) -> int:
    return sum(1 for row in download_routes if row.get("local_temp_path"))


def build_processing_status_index(
    source: dict[str, str],
    download_routes: list[dict[str, str]],
    package_routes: list[dict[str, str]],
    field_routes: list[dict[str, str]],
    metadata_routes: list[dict[str, str]],
) -> dict[str, object]:
    download_statuses = sorted({row.get("download_status", "") for row in download_routes if row.get("download_status")})
    target_record_types = sorted({row.get("target_record_type", "") for row in field_routes if row.get("target_record_type")})
    phases = [
        {
            "phase": "discovered",
            "status": "registered_source_row_present",
            "evidence_file": SOURCE_INDEX.name,
            "evidence_path": SOURCE_INDEX.as_posix(),
            "evidence_count": 1,
            "review_status": source["review_status"],
        },
        {
            "phase": "download_or_access",
            "status": phase_status(len(download_routes), "download_or_access_routes_present"),
            "evidence_file": "02_download-route-index.csv",
            "evidence_count": len(download_routes),
            "status_values": download_statuses,
            "review_status": "metadata_route_needs_human_review",
        },
        {
            "phase": "checksum_and_size",
            "status": "partial_or_complete_checksum_size_evidence",
            "evidence_file": "02_download-route-index.csv",
            "checksum_row_count": checksum_count(download_routes),
            "size_row_count": sized_count(download_routes),
            "local_temp_path_row_count": local_temp_count(download_routes),
            "review_status": "needs_human_source_review",
        },
        {
            "phase": "package_manifest",
            "status": phase_status(len(package_routes), "package_manifest_routes_present"),
            "evidence_file": "03_package-route-index.csv",
            "evidence_count": len(package_routes),
            "review_status": "needs_human_source_review",
        },
        {
            "phase": "field_mapping",
            "status": phase_status(len(field_routes), "field_map_routes_present"),
            "evidence_file": "04_field-map-route-index.csv",
            "evidence_count": len(field_routes),
            "target_record_types": target_record_types,
            "review_status": "candidate_mapping_needs_human_review",
        },
        {
            "phase": "metadata_profile",
            "status": phase_status(len(metadata_routes), "metadata_profile_rows_present"),
            "evidence_file": "05_metadata-profile-route-index.csv",
            "evidence_count": len(metadata_routes),
            "review_status": "needs_human_source_review",
        },
        {
            "phase": "cleaned_structured_linked",
            "status": "candidate_routes_available_not_final_import",
            "evidence_file": "08_source-processing-status.md",
            "evidence_count": len(package_routes) + len(field_routes) + len(metadata_routes),
            "review_status": "pending_human_review",
        },
    ]
    missing = []
    if not download_routes:
        missing.append("download_or_access_route")
    if not package_routes:
        missing.append("package_manifest_route")
    if not field_routes:
        missing.append("field_map_route")
    if not metadata_routes:
        missing.append("metadata_profile_route")
    if checksum_count(download_routes) < len(download_routes):
        missing.append("checksum_for_some_download_routes")
    return {
        "record_type": "source_processing_status_index",
        "source_id": source["source_id"],
        "source_title": source["title"],
        "rights_status": source["rights_status"],
        "risk_note": source["risk_note"],
        "phases": phases,
        "missing_or_review_items": missing,
        "human_entry": "08_source-processing-status.md",
        "research_boundary": (
            "source_processing_status_preprocessing_only; statuses mark evidence "
            "availability and review work, not scholarly conclusions"
        ),
        "decipherment_claim_status": "no_claim",
        "updated_at": UPDATED_AT,
    }


def source_evidence_dossier_index_payload(
    source: dict[str, str],
    download_routes: list[dict[str, str]],
    package_routes: list[dict[str, str]],
    field_routes: list[dict[str, str]],
    metadata_routes: list[dict[str, str]],
) -> dict[str, object]:
    package_kinds = sorted({row.get("file_kind", "") for row in package_routes if row.get("file_kind")})
    target_record_types = sorted(
        {row.get("target_record_type", "") for row in field_routes if row.get("target_record_type")}
    )
    download_statuses = sorted(
        {row.get("download_status", "") for row in download_routes if row.get("download_status")}
    )
    return {
        "record_type": "source_evidence_dossier_index",
        "source_id": source["source_id"],
        "source_title": source["title"],
        "human_readable_files": [
            "README.md",
            "06_human-source-review-sheet.md",
            "07_material-access-index.md",
            "08_source-processing-status.md",
            "10_source-evidence-dossier.md",
            "12_source-provenance-fact-matrix.md",
            "14_source-to-dossier-transfer-review.md",
            "16_source-literature-scope-review.md",
            "18_source-access-integrity-review.md",
            "20_source-presearch-readiness-review.md",
        ],
        "ai_support_files": [
            "01_source-packet.json",
            "02_download-route-index.csv",
            "03_package-route-index.csv",
            "04_field-map-route-index.csv",
            "05_metadata-profile-route-index.csv",
            "09_source-processing-status-index.json",
            "11_source-evidence-dossier-index.json",
            "13_source-provenance-fact-matrix-index.json",
            "15_source-to-dossier-transfer-index.json",
            "17_source-literature-scope-index.json",
            "19_source-access-integrity-index.json",
            "21_source-presearch-readiness-index.json",
        ],
        "source_route_files": [
            SOURCE_INDEX.as_posix(),
            DOWNLOAD_MANIFEST.as_posix(),
            DOWNLOAD_LOG.as_posix(),
            PACKAGE_MANIFEST.as_posix(),
            FIELD_MAP.as_posix(),
            METADATA_PROFILE.as_posix(),
            "10_source-evidence-dossier.md",
        ],
        "evidence_counts": {
            "download_route_count": len(download_routes),
            "checksum_route_count": checksum_count(download_routes),
            "size_route_count": sized_count(download_routes),
            "package_route_count": len(package_routes),
            "field_map_route_count": len(field_routes),
            "metadata_profile_route_count": len(metadata_routes),
            "package_kinds": package_kinds,
            "target_record_types": target_record_types,
            "download_statuses": download_statuses,
        },
        "uncollected_human_research_fields": [
            "bibliographic_citation_relationships",
            "proposer_or_source_editor_review",
            "different_opinions_or_disputes",
            "license_text_review",
            "derived_record_review_results",
            "source_access_integrity_review_results",
        ],
        "claim_boundary": [
            "no rights decision",
            "no corpus import approval",
            "no confirmed source promotion",
            "no reading",
            "no component assignment",
            "no inscription identity",
            "no decipherment conclusion",
        ],
        "review_status": "needs_human_source_review",
        "updated_at": UPDATED_AT,
    }


def source_provenance_fact_rows(
    source: dict[str, str],
    download_routes: list[dict[str, str]],
    package_routes: list[dict[str, str]],
    field_routes: list[dict[str, str]],
    metadata_routes: list[dict[str, str]],
) -> list[dict[str, str]]:
    derived_files = [
        "06_human-source-review-sheet.md",
        "07_material-access-index.md",
        "08_source-processing-status.md",
        "10_source-evidence-dossier.md",
    ]
    if metadata_routes:
        derived_files.append("05_metadata-profile-route-index.csv")
    return [
        {
            "fact": "Source identity / 来源身份",
            "status": "present" if source.get("source_id") and source.get("title") else "needs_review",
            "evidence_files": "01_source-packet.json; 10_source-evidence-dossier.md",
            "next_check": "Check source_id, title, provider, URL, scope, and authority tier.",
        },
        {
            "fact": "Access or download record / 访问或下载记录",
            "status": "present" if download_routes else "missing_route",
            "evidence_files": "02_download-route-index.csv",
            "next_check": "Check URL, access status, HTTP status, and local route notes.",
        },
        {
            "fact": "Checksum evidence / 校验和证据",
            "status": "present" if checksum_count(download_routes) else "needs_review",
            "evidence_files": "02_download-route-index.csv",
            "next_check": "Confirm SHA-256 rows before reusing any downloaded file.",
        },
        {
            "fact": "File size evidence / 文件大小证据",
            "status": "present" if sized_count(download_routes) else "needs_review",
            "evidence_files": "02_download-route-index.csv; 03_package-route-index.csv",
            "next_check": "Compare download sizes with package manifest file sizes.",
        },
        {
            "fact": "Rights status / 权利状态",
            "status": "present" if source.get("rights_status") else "needs_review",
            "evidence_files": "01_source-packet.json; 03_package-route-index.csv",
            "next_check": "Treat rights status as a review note, not a license grant.",
        },
        {
            "fact": "Risk note / 风险提示",
            "status": "present" if source.get("risk_note") else "needs_review",
            "evidence_files": "01_source-packet.json; 07_material-access-index.md",
            "next_check": "Keep the visible risk note beside any future derivative.",
        },
        {
            "fact": "Package manifest / 来源包清单",
            "status": "present" if package_routes else "missing_route",
            "evidence_files": "03_package-route-index.csv",
            "next_check": "Open package rows before treating files as reusable derivatives.",
        },
        {
            "fact": "Field map / 字段映射",
            "status": "present" if field_routes else "missing_route",
            "evidence_files": "04_field-map-route-index.csv",
            "next_check": "Review source fields before moving data into corpus objects.",
        },
        {
            "fact": "Derived paths / 派生路径",
            "status": "present",
            "evidence_files": "; ".join(derived_files),
            "next_check": (
                "Open human files first, then use structured support indexes "
                "only as routes."
            ),
        },
        {
            "fact": "Review status / 复核状态",
            "status": "present" if source.get("review_status") else "needs_review",
            "evidence_files": "01_source-packet.json; 08_source-processing-status.md",
            "next_check": "Record unresolved items as concrete human follow-up questions.",
        },
    ]


def source_provenance_fact_matrix_index_payload(
    source: dict[str, str],
    fact_rows: list[dict[str, str]],
) -> dict[str, object]:
    return {
        "record_type": "source_provenance_fact_matrix_index",
        "source_id": source["source_id"],
        "source_title": source["title"],
        "fact_count": len(fact_rows),
        "human_readable_files": [
            "06_human-source-review-sheet.md",
            "07_material-access-index.md",
            "10_source-evidence-dossier.md",
            "12_source-provenance-fact-matrix.md",
            "18_source-access-integrity-review.md",
            "20_source-presearch-readiness-review.md",
        ],
        "ai_support_files": [
            "01_source-packet.json",
            "02_download-route-index.csv",
            "03_package-route-index.csv",
            "04_field-map-route-index.csv",
            "09_source-processing-status-index.json",
            "11_source-evidence-dossier-index.json",
            "19_source-access-integrity-index.json",
            "21_source-presearch-readiness-index.json",
        ],
        "facts": fact_rows,
        "claim_boundary": [
            "no rights decision",
            "no corpus import approval",
            "no confirmed source promotion",
            "no reading",
            "no component assignment",
            "no inscription identity",
            "no decipherment conclusion",
        ],
        "review_status": "needs_human_source_review",
        "updated_at": UPDATED_AT,
    }


TRANSFER_SLOTS = [
    {
        "slot": "character_dossier_transfer",
        "target": "corpus/001_oracle-characters/",
        "human_heading": "Character dossier transfer",
        "source_evidence": (
            "glyph images, rubbings, photographs, variant notes, near-form "
            "routes, component clues, and source labels"
        ),
        "next_check": (
            "Open character folders only after image rights, source identity, "
            "and candidate-status wording are checked."
        ),
    },
    {
        "slot": "inscription_plate_transfer",
        "target": "corpus/002_oracle-bone-inscriptions/",
        "human_heading": "Inscription and plate transfer",
        "source_evidence": (
            "inscription text, OCR, plate number, catalog number, page, Heji "
            "or OBM route, text quality, and image path"
        ),
        "next_check": (
            "Keep inscription identity and text readings pending until a "
            "reviewer checks the source record and plate evidence."
        ),
    },
    {
        "slot": "collection_findspot_transfer",
        "target": "corpus/005_excavation-sites-periods-and-batches/",
        "human_heading": "Collection and findspot transfer",
        "source_evidence": (
            "museum object, collection, findspot, period, group, batch, "
            "excavation note, and catalog provenance"
        ),
        "next_check": (
            "Record each missing archaeology field as a concrete source "
            "question before using it for context."
        ),
    },
    {
        "slot": "later_form_relation_transfer",
        "target": "corpus/004_bronze-seal-modern-correspondences/",
        "human_heading": "Later-form and relation transfer",
        "source_evidence": (
            "variant, near-form, component, bronze-script, seal-script, "
            "modern-character, and evolution routes"
        ),
        "next_check": (
            "Treat every relation as candidate comparison evidence, not an "
            "accepted paleographic correspondence."
        ),
    },
    {
        "slot": "bibliography_dispute_transfer",
        "target": "research/",
        "human_heading": "Bibliography and dispute transfer",
        "source_evidence": (
            "book, paper, web page, database note, citation relation, proposer, "
            "editor, evidence level, disagreement, and dispute"
        ),
        "next_check": (
            "Move nothing into research notes until the bibliography route and "
            "claim boundary are reviewed."
        ),
    },
    {
        "slot": "rights_public_derivative_transfer",
        "target": "object-local human dossier",
        "human_heading": "Rights and public derivative transfer",
        "source_evidence": (
            "rights status, risk note, checksum, file size, package manifest, "
            "commit policy, and derived path"
        ),
        "next_check": (
            "Keep raw files local or metadata-only when rights, size, or "
            "redistribution risk is unresolved."
        ),
    },
]


def source_to_dossier_transfer_review_text(source: dict[str, str]) -> str:
    lines = [
        "# Source-To-Dossier Transfer Review / 来源进入档案复核表",
        "",
        "## English",
        *wrapped(
            "This human worksheet decides how evidence from this source may "
            "enter concrete character, inscription, plate, collection, later-"
            "form, and bibliography dossiers. It is a review map, not an "
            "import approval or scholarship conclusion."
        ),
        "",
        "## 简体中文",
        *wrapped(
            "本表用于人工判断本来源的证据如何进入具体单字、卜辞、图版、馆藏、"
            "后世字形和文献档案。它只是复核地图，不是导入批准，也不是学术结论。"
        ),
        "",
        "## Human Transfer Order / 人工转入顺序",
        "- Open `10_source-evidence-dossier.md` and",
        "  `12_source-provenance-fact-matrix.md`.",
        "- Check route CSV files only as supporting evidence.",
        "- Decide the target object directory before deriving any record.",
        "- Record missing evidence as a concrete question in the target dossier.",
        "- Keep every unresolved reading, relation, and dispute as pending.",
        "- 先读来源证据档案和来源事实矩阵。",
        "- 结构化 CSV/JSON 只作为辅助路线。",
        "- 先确定目标对象目录，再生成派生记录。",
        "- 缺失证据必须写成目标档案中的具体待查问题。",
        "- 未复核释读、关系和争议都保持待查状态。",
        "",
        "## Source / 来源",
        *bullet("Source ID / 来源 ID", source["source_id"]),
        *bullet("Title / 标题", source["title"]),
        *bullet("Provider / 提供方", source["provider"]),
        *bullet("Rights status / 权利状态", source["rights_status"]),
        *bullet("Review status / 复核状态", source["review_status"]),
        "",
        "## Transfer Slots / 转入复核槽位",
    ]
    for index, slot in enumerate(TRANSFER_SLOTS, start=1):
        lines.extend(
            [
                "",
                f"### {index:02d}. {slot['human_heading']}",
                *bullet("Target / 目标目录", slot["target"]),
                *bullet("Source evidence / 来源证据", slot["source_evidence"]),
                *bullet("Next check / 下一步核查", slot["next_check"]),
            ]
        )
    lines.extend(
        [
            "",
            "## Concrete Questions To Carry Forward / 需带入目标档案的问题",
            "- Which visible image, rubbing, plate, or catalog image can be cited?",
            "- Which inscription text, OCR, catalog number, page, or Heji route",
            "  applies?",
            "- Which findspot, collection, period, group, or batch remains missing?",
            "- Which variant, component, later-form, or evolution route is only",
            "  candidate?",
            "- Which bibliography, proposer, disagreement, or dispute must be opened?",
            "- Which rights, checksum, size, or commit-policy issue blocks",
            "  promotion?",
            "- 哪个字形图像、拓片、图版或著录图像可以引用？",
            "- 哪条卜辞全文、OCR、著录号、页码或合集路线适用？",
            "- 哪个出土地、馆藏、时期、组类或批次仍然缺失？",
            "- 哪条异体、构件、后世字形或演化路线仍只是候选？",
            "- 哪条文献、提出者、不同意见或争议必须先打开？",
            "- 哪个权利、checksum、大小或提交策略问题阻止公开提升？",
            "",
            "## Boundary / 边界",
            "- not a rights decision",
            "- not corpus import approval",
            "- not a confirmed source promotion",
            "- not an accepted reading",
            "- not a component assignment",
            "- not an inscription identity",
            "- not a correspondence conclusion",
            "- not a decipherment conclusion",
            "- 不是权利结论",
            "- 不是语料导入批准",
            "- 不是来源提升结论",
            "- 不是已接受释读",
            "- 不是构件归属",
            "- 不是卜辞身份确认",
            "- 不是字形对应结论",
            "- 不是破译结论",
        ]
    )
    return "\n".join(lines)


def source_to_dossier_transfer_index_payload(source: dict[str, str]) -> dict[str, object]:
    return {
        "record_type": "source_to_dossier_transfer_index",
        "source_id": source["source_id"],
        "source_title": source["title"],
        "human_readable_files": [
            "14_source-to-dossier-transfer-review.md",
            "10_source-evidence-dossier.md",
            "12_source-provenance-fact-matrix.md",
            "06_human-source-review-sheet.md",
            "16_source-literature-scope-review.md",
            "18_source-access-integrity-review.md",
            "20_source-presearch-readiness-review.md",
        ],
        "ai_support_files": [
            "01_source-packet.json",
            "02_download-route-index.csv",
            "03_package-route-index.csv",
            "04_field-map-route-index.csv",
            "05_metadata-profile-route-index.csv",
            "11_source-evidence-dossier-index.json",
            "17_source-literature-scope-index.json",
            "19_source-access-integrity-index.json",
            "21_source-presearch-readiness-index.json",
        ],
        "transfer_slots": [slot["slot"] for slot in TRANSFER_SLOTS],
        "target_routes": [slot["target"] for slot in TRANSFER_SLOTS],
        "claim_boundary": [
            "no rights decision",
            "no corpus import approval",
            "no confirmed source promotion",
            "no accepted reading",
            "no component assignment",
            "no inscription identity",
            "no correspondence conclusion",
            "no decipherment conclusion",
        ],
        "review_status": "needs_human_source_review",
        "updated_at": UPDATED_AT,
    }


def source_literature_scope_review_text(source: dict[str, str]) -> str:
    lines = [
        "# Source Literature Scope Review / 来源文献适用范围复核",
        "",
        "## English",
        *wrapped(
            "This human review file keeps bibliography, database notes, source "
            "scope, evidence level, proposer or editor, citation relations, "
            "different opinions, and disputes visible before the source is "
            "used in any later character, inscription, topic, or bibliography "
            "dossier."
        ),
        "",
        "## 简体中文",
        *wrapped(
            "本文件在来源进入后续单字、卜辞、主题或文献档案前，先把书目、"
            "数据库说明、资料适用范围、证据等级、提出者或整理者、引用关系、"
            "不同意见和争议作为人类复核项目保留在同一来源对象目录内。"
        ),
        "",
        "## Source / 来源",
        *bullet("Source ID / 来源 ID", source["source_id"]),
        *bullet("Title / 题名", source["title"]),
        *bullet("Provider / 提供方", source["provider"]),
        *bullet("Source type / 来源类型", source["source_type"]),
        *bullet("Authority tier / 证据等级", source["authority_tier"]),
        *bullet("Scope / 适用范围", source["scope"]),
        *bullet("Rights status / 权利状态", source["rights_status"]),
        *bullet("Review status / 复核状态", source["review_status"]),
        "",
    ]
    if source["source_id"] == "src-hust-obc":
        lines.extend(
            [
                "## Primary Publication / 主要论文",
                *bullet(
                    "Citation / 引用",
                    "Wang, P., Zhang, K., Wang, X. et al. An open dataset for "
                    "oracle bone character recognition and decipherment. "
                    "Scientific Data 11, 976 (2024).",
                ),
                *bullet(
                    "DOI / DOI",
                    "https://doi.org/10.1038/s41597-024-03807-x",
                ),
                *bullet(
                    "Publication dates / 发表日期",
                    "Received 2024-01-22; accepted 2024-08-20; published "
                    "2024-09-06; version of record 2024-09-06.",
                ),
                *bullet(
                    "Authors and institutions / 作者与机构",
                    "Pengjie Wang, Kaile Zhang, Xinyu Wang, Shengwei Han, "
                    "Yongge Liu, Jinpeng Wan, Haisu Guan, Zhebin Kuang, "
                    "Lianwen Jin, Xiang Bai, and Yuliang Liu; affiliations "
                    "include HUST, University of Adelaide, Anyang Normal "
                    "University, and South China University of Technology.",
                ),
                *bullet(
                    "Evidence level / 证据等级",
                    "Primary peer-reviewed data descriptor; it documents a "
                    "dataset and its construction, not an archaeological "
                    "catalog identity or confirmed reading.",
                ),
                "",
                "## Paper-Reported Research Process / 论文报告的处理过程",
                *bullet(
                    "Source intake / 来源进入",
                    "Books, websites, and databases were combined; reported "
                    "examples include New Compilation of Oracle Bone Scripts, "
                    "Oracle Bone Script: Six Digit Numerical Code, YinQiWenYuan, "
                    "GuoXueDaShi, and HWOBC.",
                ),
                *bullet(
                    "Processing stages / 处理阶段",
                    "The paper reports data acquisition, automatic annotation, "
                    "data integration, and data validation, followed by review "
                    "by oracle-bone scholars from Anyang Normal University.",
                ),
                *bullet(
                    "Reported scale / 论文报告规模",
                    "77,064 images across 1,588 deciphered categories and "
                    "62,989 images across 9,411 undeciphered categories, "
                    "140,053 images in total.",
                ),
                "",
                "## Citation Relations / 引用关系",
                *bullet(
                    "Publication to dataset / 论文到数据集",
                    "The article points to the HUST-OBC Figshare record, "
                    "including version 3, and to the Pengjie-W/HUST-OBC "
                    "repository for code and dataset access routes.",
                ),
                *bullet(
                    "Cited source routes / 被引来源路线",
                    "The article cites books, HWOBC, YinQiWenYuan, "
                    "GuoXueDaShi, OBIMD, and prior recognition studies; each "
                    "route needs independent source and rights review before "
                    "a later dossier reuses it.",
                ),
                "",
                "## Reported Limits And Disputes / 论文报告限制与争议",
                *bullet(
                    "GuoXueDaShi caution / 国学大师风险",
                    "The paper reports 1,390 GuoXueDaShi categories that could "
                    "not be verified and were stored separately; this remains "
                    "a source caution, not a repository identity decision.",
                ),
                *bullet(
                    "Category integration / 类别合并",
                    "The reported reduction from 1,781 to 1,588 categories is "
                    "a dataset-construction statistic, not proof of identity, "
                    "variant, component, or evolution.",
                ),
                *bullet(
                    "Undeciphered split / 未释分组",
                    "The paper notes possible duplicates among 9,411 "
                    "undeciphered categories because their annotations are "
                    "not yet available; local records retain candidate status.",
                ),
                *bullet(
                    "License / 许可",
                    "The article reports CC BY-NC 4.0; local status remains "
                    "source_marked_risk_noted until the license scope for each "
                    "image and derivative is checked against the package route.",
                ),
                *bullet(
                    "Different opinions / 不同意见",
                    "No formal scholarly disagreement is resolved here. "
                    "Cited books, labels, source splits, and review decisions "
                    "remain routes for independent human comparison.",
                ),
                "",
                "## Concrete Bibliography Checks / 具体文献核查",
                "- Verify the DOI, Figshare version, repository revision, and",
                "  local checksum rows before reusing a paper claim.",
                "- Open the cited books and web/database routes and record page,",
                "  plate, catalog, or object references where available.",
                "- Compare each HUST label route with its source provenance before",
                "  connecting it to a character or inscription dossier.",
                "- Record disagreements about labels, source categories, and",
                "  provenance as pending review, not as corrected scholarship.",
                "- 复核 DOI、Figshare 版本、代码仓库版本和本地 checksum 后，",
                "  才能复用论文中的具体说法。",
                "- 打开论文所引图书、网页和数据库路线，记录可得的页码、",
                "  图版号、著录号或馆藏对象号。",
                "- 每条 HUST 标签路线接入单字或卜辞档案前，先核对来源出处。",
                "- 对标签、来源分组和出处的不同意见写成待复核记录，",
                "  不写成已经修正的学术结论。",
                "",
            ]
        )
    elif source["source_id"] == "src-obimd":
        lines.extend(
            [
                "## Primary Publication / 主要论文",
                *bullet(
                    "Citation / 引用",
                    "Li, B., Yang, J., Liang, Y. et al. OBIMD: A Multi-modal "
                    "Dataset for Contextual Interpretation of Oracle Bone "
                    "Inscriptions. Scientific Data 13, 681 (2026).",
                ),
                *bullet(
                    "DOI / DOI",
                    "https://doi.org/10.1038/s41597-026-06967-0",
                ),
                *bullet(
                    "Publication dates / 发表日期",
                    "Received 2025-07-16; accepted 2026-02-24; published "
                    "2026-03-14; version of record 2026-04-30.",
                ),
                *bullet(
                    "Responsible roles / 责任分工",
                    "Bang Li and Jing Yang are recorded as equal first "
                    "contributors; Donghao Luo and Taisong Jin are the "
                    "corresponding authors. The paper also records manual "
                    "annotation and annotation-coordination roles.",
                ),
                *bullet(
                    "Evidence level / 证据等级",
                    "Primary peer-reviewed data descriptor; it documents a "
                    "multimodal dataset and workflow, not a final transcription "
                    "or accepted reading.",
                ),
                "",
                "## Paper-Reported Research Process / 论文报告的处理过程",
                *bullet(
                    "Material base / 资料基础",
                    "The paper reports 10,077 rubbing images: 9,913 from "
                    "Jiaguwen Heji and 164 from Huayuanzhuang East material, "
                    "with aligned facsimile and transcription routes.",
                ),
                *bullet(
                    "Facsimile relation / 摹本关系",
                    "Pixel-aligned facsimiles were redrawn by integrating selected "
                    "rubbings with facsimile references; they are not simply "
                    "treated as direct originals of the cited series.",
                ),
                *bullet(
                    "Annotation stages / 标注阶段",
                    "The reported workflow has data acquisition, pre-annotation, "
                    "and collaborative annotation and verification. Graduates "
                    "cross-check cases; experts arbitrate unresolved cases.",
                ),
                *bullet(
                    "Reported structure / 论文报告结构",
                    "The dataset reports 93,652 annotated characters, 21,667 "
                    "missing-character positions, 21,941 sentence units, and "
                    "4,192 non-sentential elements.",
                ),
                "",
                "## Human Research Relevance / 人类研究相关性",
                *bullet(
                    "Reading context / 阅读上下文",
                    "Rubbing, facsimile, transcription, character boxes, groups, "
                    "and reading-order fields are routes for opening evidence "
                    "before interpretation.",
                ),
                *bullet(
                    "Uncertainty fields / 不确定字段",
                    "SeatFont marks missing positions; Mark records exceptional "
                    "or unresolved cases. Label and SubLabel remain dataset "
                    "routes, not confirmed character identities.",
                ),
                *bullet(
                    "Modern label boundary / 今字边界",
                    "The paper supplies modern-character transcription for "
                    "reference and lookup; local review must not treat it as a "
                    "final decipherment result.",
                ),
                "",
                "## Citation And Access Relations / 引用与访问关系",
                *bullet(
                    "Data and code routes / 数据与代码路线",
                    "The article points to Hugging Face KLOBIP/OBIMD for data, "
                    "libang1991/OBIMD on GitHub for code, and the JGWL platform "
                    "for the annotation environment.",
                ),
                *bullet(
                    "Cited source routes / 被引来源路线",
                    "Important routes include YinQiWenYuan, Jiaguwen Heji, "
                    "Huayuanzhuang East material, Jiaguwen Moben Daxi, the "
                    "Oracular Digital Platform, HUST-OBC, and EVOBC.",
                ),
                "",
                "## Reported Limits And Disputes / 论文报告限制与争议",
                *bullet(
                    "Source-layer distinction / 来源层次区别",
                    "Rubbings, facsimiles, redrawn facsimiles, and transcriptions "
                    "must remain distinct; alignment does not prove equal "
                    "evidentiary status.",
                ),
                *bullet(
                    "Unresolved cases / 待解决情况",
                    "Placeholders, uncertain groups, special marks, and disputed "
                    "classifications remain review routes rather than resolved "
                    "scholarship.",
                ),
                *bullet(
                    "License conflict / 许可冲突",
                    "The article states CC BY-NC-ND 4.0, while local dataset-card "
                    "and repository notes use different wording. Keep the rights "
                    "discrepancy visible and review each derivative.",
                ),
                *bullet(
                    "Large files / 大文件",
                    "Raw annotation and image packages remain outside ordinary Git "
                    "where required; only source-marked, reviewed derivatives may "
                    "enter object dossiers.",
                ),
                "",
                "## Concrete Bibliography Checks / 具体文献核查",
                "- Verify the DOI, Hugging Face snapshot, GitHub revision, and",
                "  local package checksums before reusing any field or count.",
                "- Open the Heji, Huayuanzhuang East, YinQiWenYuan, and facsimile",
                "  routes before transferring a sentence or plate claim.",
                "- Keep rubbing, facsimile, redraw, transcription, Label, and",
                "  SubLabel as separate evidence layers in inscription dossiers.",
                "- Record placeholders, Mark values, disputed labels, and missing",
                "  positions as concrete review questions.",
                "- 复核 DOI、Hugging Face 快照、GitHub 版本和本地来源包 checksum，",
                "  再复用具体字段或统计数值。",
                "- 打开合集、出土地点、殷契文渊和摹本路线后，才能转入卜辞档案。",
                "- 在卜辞档案中分开保存拓片、摹本、重绘摹本、释文、Label 和",
                "  SubLabel，不能把它们合并成单一证据层。",
                "- 把占位框、Mark 值、争议标签和缺失位置写成具体待复核问题。",
                "",
            ]
        )
    lines.extend(
        [
        "## Literature And Database Review Slots / 文献与数据库复核槽位",
        *bullet(
            "Bibliography note / 书目说明",
            "Open README.md and 10_source-evidence-dossier.md before citing "
            "this source in a later research note.",
        ),
        *bullet(
            "Database scope / 数据库范围",
            "Record which object type, catalog range, plate range, glyph "
            "range, or inscription range the source actually covers.",
        ),
        *bullet(
            "Evidence level / 证据等级",
            "Keep authority tier and source type visible; do not treat them "
            "as a scholarly conclusion.",
        ),
        *bullet(
            "Proposer or editor / 提出者或整理者",
            "Check source notes, database pages, paper metadata, or catalog "
            "front matter before assigning responsibility.",
        ),
        *bullet(
            "Citation relation / 引用关系",
            "Record whether the source cites a catalog, dictionary, paper, "
            "museum record, database export, or derived index.",
        ),
        *bullet(
            "Different opinions / 不同意见",
            "Absence of a disagreement row is not agreement; it is a pending "
            "review question until checked against bibliography notes.",
        ),
        *bullet(
            "Dispute record / 争议记录",
            "Keep disputed readings, labels, source fields, and mappings as "
            "pending review routes.",
        ),
        "",
        "## Concrete Questions To Check / 具体待查问题",
        "- Which book, paper, webpage, museum record, or database note defines",
        "  this source?",
        "- Which source scope is directly supported by the local evidence rows?",
        "- Which proposer, editor, compiler, or institution should be recorded?",
        "- Which catalog, dictionary, paper, or database does this source cite?",
        "- Which alternate label, disagreement, or dispute remains unresolved?",
        "- Which later object dossier should receive only a route, not a claim?",
        "- 哪条书目、论文、网页、馆藏记录或数据库说明界定本来源？",
        "- 哪个资料范围能由本目录内证据行直接支持？",
        "- 哪位提出者、整理者、编者或机构需要记录？",
        "- 本来源引用了哪种著录、字编、论文或数据库？",
        "- 哪个替代标签、不同意见或争议仍未解决？",
        "- 哪个后续对象档案只能接收复核路线，而不能接收结论？",
        "",
        "## Local Evidence To Open / 本地证据入口",
        "- README.md",
        "- 06_human-source-review-sheet.md",
        "- 07_material-access-index.md",
        "- 10_source-evidence-dossier.md",
        "- 12_source-provenance-fact-matrix.md",
        "- 14_source-to-dossier-transfer-review.md",
        "",
        "## Boundary / 边界",
        "- not a rights decision",
        "- not corpus import approval",
        "- not a confirmed bibliography conclusion",
        "- not an accepted reading",
        "- not a component assignment",
        "- not an inscription identity",
        "- not a correspondence conclusion",
        "- not a decipherment conclusion",
        "- 不是权利结论",
        "- 不是语料导入批准",
        "- 不是已确认的文献学结论",
        "- 不是已接受释读",
        "- 不是构件归属",
        "- 不是卜辞身份确认",
        "- 不是字形对应结论",
        "- 不是破译结论",
        ]
    )
    return "\n".join(lines)


def source_literature_scope_index_payload(source: dict[str, str]) -> dict[str, object]:
    return {
        "record_type": "source_literature_scope_index",
        "source_id": source["source_id"],
        "source_title": source["title"],
        "human_readable_files": [
            "16_source-literature-scope-review.md",
            "10_source-evidence-dossier.md",
            "14_source-to-dossier-transfer-review.md",
            "06_human-source-review-sheet.md",
            "18_source-access-integrity-review.md",
            "20_source-presearch-readiness-review.md",
        ],
        "ai_support_files": [
            "01_source-packet.json",
            "02_download-route-index.csv",
            "03_package-route-index.csv",
            "04_field-map-route-index.csv",
            "11_source-evidence-dossier-index.json",
            "15_source-to-dossier-transfer-index.json",
            "19_source-access-integrity-index.json",
            "21_source-presearch-readiness-index.json",
        ],
        "review_slots": [
            "bibliography_note",
            "database_scope",
            "evidence_level",
            "proposer_or_editor",
            "citation_relation",
            "different_opinions",
            "dispute_record",
        ],
        "claim_boundary": [
            "no rights decision",
            "no corpus import approval",
            "no confirmed bibliography conclusion",
            "no accepted reading",
            "no component assignment",
            "no inscription identity",
            "no correspondence conclusion",
            "no decipherment conclusion",
        ],
        "review_status": "needs_human_source_literature_scope_review",
        "updated_at": UPDATED_AT,
    }


def source_access_integrity_review_text(
    source: dict[str, str],
    download_routes: list[dict[str, str]],
    package_routes: list[dict[str, str]],
    field_routes: list[dict[str, str]],
    metadata_routes: list[dict[str, str]],
) -> str:
    local_temp_count = sum(1 for row in download_routes if row.get("local_temp_path"))
    missing_checksum_count = len(download_routes) - checksum_count(download_routes)
    missing_size_count = len(download_routes) - sized_count(download_routes)
    lines = [
        "# Source Access Integrity Review / 来源访问完整性复核",
        "",
        "## English",
        *wrapped(
            "This human review page checks whether access, checksum, size, "
            "package manifest, field map, metadata profile, derived path, "
            "rights status, and risk evidence are visible before the source "
            "supports any object dossier."
        ),
        "",
        "## 简体中文",
        *wrapped(
            "本页供人工复核来源的访问记录、checksum、大小、来源包清单、"
            "字段映射、元数据概况、派生路径、权利状态和风险提示是否已经"
            "可见。它服务具体资料对象档案，不是导入批准或学术结论。"
        ),
        "",
        "## Source / 来源",
        *bullet("Source ID / 来源 ID", source["source_id"]),
        *bullet("Title / 题名", source["title"]),
        *bullet("Provider / 提供方", source["provider"]),
        *bullet("Rights status / 权利状态", source["rights_status"]),
        *bullet("Risk note / 风险提示", source["risk_note"]),
        *bullet("Review status / 复核状态", source["review_status"]),
        "",
        "## Human Research Evidence First / 人类研究证据优先",
        *wrapped(
            "Before any technical reuse, a reviewer should ask which glyph "
            "image, rubbing, photograph, inscription, OCR text, plate, catalog "
            "number, provenance note, findspot, collection, period, group, "
            "variant, component, near form, bronze-script form, seal-script "
            "form, modern correspondence, bibliography, proposer, dispute, or "
            "scholarship note this source can actually support."
        ),
        "",
        *wrapped(
            "技术复用之前，应先确认本来源能支持哪些字形图像、拓片、照片、"
            "卜辞、OCR 全文、图版、著录号、出处、出土地、馆藏、时期、"
            "组类、异体、构件、近形、金文、小篆、今字对应、书目、提出者、"
            "争议或释读史线索。"
        ),
        "",
        "## Research Slots To Protect / 必须保护的研究槽位",
        "- Glyph image, rubbing, photograph, plate, and catalog evidence.",
        "- Inscription text, OCR text, Heji number, and text quality note.",
        "- Findspot, collection, period, group, batch, and provenance note.",
        "- Variant, component, near-form, bronze, seal, and modern relation.",
        "- Bibliography, source scope, proposer, dispute, and scholarship note.",
        "- 字形图像、拓片、照片、图版和著录证据。",
        "- 卜辞全文、OCR、合集号和文本质量说明。",
        "- 出土地、馆藏、时期、组类、批次和出处说明。",
        "- 异体、构件、近形、金文、小篆、今字和字形关系。",
        "- 书目、来源范围、提出者、争议和释读史记录。",
        "",
        "## Access Download Checksum And Size / 访问下载校验与大小",
        *bullet("Download route file / 下载路线文件", "02_download-route-index.csv"),
        *bullet("Download route count / 下载路线数", len(download_routes)),
        *bullet("Checksum route count / checksum 路线数", checksum_count(download_routes)),
        *bullet("Missing checksum count / 缺 checksum 数", missing_checksum_count),
        *bullet("Size route count / 大小路线数", sized_count(download_routes)),
        *bullet("Missing size count / 缺大小数", missing_size_count),
        *bullet("Local temp route count / 本地临时路线数", local_temp_count),
        "",
        "## Package Manifest Field Map And Derivatives / 清单映射与派生",
        *bullet("Package route file / 来源包路线文件", "03_package-route-index.csv"),
        *bullet("Package route count / 来源包路线数", len(package_routes)),
        *bullet("Field map file / 字段映射文件", "04_field-map-route-index.csv"),
        *bullet("Field map route count / 字段映射路线数", len(field_routes)),
        *bullet("Metadata profile file / 元数据概况文件", "05_metadata-profile-route-index.csv"),
        *bullet("Metadata profile count / 元数据概况数", len(metadata_routes)),
        *bullet("Evidence dossier / 来源证据档案", "10_source-evidence-dossier.md"),
        *bullet("Fact matrix / 来源事实矩阵", "12_source-provenance-fact-matrix.md"),
        "",
        "## Rights Risk And Public Commit Decision / 权利风险与公开提交判断",
        *wrapped(
            "Review rights status, risk note, file size, commit policy, and "
            "large-source handling before any public derivative or Git commit. "
            "Raw material that exceeds repository limits must stay in an "
            "ignored local or external archive with source-marked manifests."
        ),
        "",
        *wrapped(
            "公开派生记录或 Git 提交之前，必须先复核权利状态、风险提示、"
            "文件大小、提交策略和大文件处理方式。超过仓库限制的原始资料"
            "应留在已忽略本地目录或外部归档中，只提交可审计清单。"
        ),
        "",
        "## Concrete Access Integrity Questions / 具体访问完整性问题",
        "- Which download or access row is missing checksum or size?",
        "- Which package manifest row proves the extracted file?",
        "- Which field-map row is safe for corpus object use?",
        "- Which metadata profile row signals OCR or quality risk?",
        "- Which rights or risk issue blocks public promotion?",
        "- Which local or external archive holds raw material if too large?",
        "- 哪条下载或访问记录仍缺 checksum 或文件大小？",
        "- 哪条来源包清单记录能证明已抽取文件？",
        "- 哪条字段映射记录可以安全进入具体语料对象？",
        "- 哪条元数据概况记录提示 OCR 或质量风险？",
        "- 哪个权利或风险问题阻止公开提升？",
        "- 如果原始资料过大，存放在哪个本地或外部归档？",
        "",
        "## Files To Open / 应打开文件",
        "- README.md",
        "- 02_download-route-index.csv",
        "- 03_package-route-index.csv",
        "- 04_field-map-route-index.csv",
        "- 05_metadata-profile-route-index.csv",
        "- 10_source-evidence-dossier.md",
        "- 12_source-provenance-fact-matrix.md",
        "",
        "## Boundary / 边界",
        "- not a rights decision",
        "- not corpus import approval",
        "- not a confirmed source promotion",
        "- not an accepted reading",
        "- not a component assignment",
        "- not an inscription identity",
        "- not a correspondence conclusion",
        "- not a decipherment conclusion",
        "- 不是权利结论",
        "- 不是语料导入批准",
        "- 不是来源提升结论",
        "- 不是已接受释读",
        "- 不是构件归属",
        "- 不是卜辞身份确认",
        "- 不是字形对应结论",
        "- 不是破译结论",
    ]
    return "\n".join(lines)


def source_access_integrity_index_payload(
    source: dict[str, str],
    download_routes: list[dict[str, str]],
    package_routes: list[dict[str, str]],
    field_routes: list[dict[str, str]],
    metadata_routes: list[dict[str, str]],
) -> dict[str, object]:
    return {
        "record_type": "source_access_integrity_index",
        "source_id": source["source_id"],
        "source_title": source["title"],
        "human_readable_files": [
            "18_source-access-integrity-review.md",
            "10_source-evidence-dossier.md",
            "12_source-provenance-fact-matrix.md",
            "06_human-source-review-sheet.md",
            "20_source-presearch-readiness-review.md",
        ],
        "ai_support_files": [
            "01_source-packet.json",
            "02_download-route-index.csv",
            "03_package-route-index.csv",
            "04_field-map-route-index.csv",
            "05_metadata-profile-route-index.csv",
            "09_source-processing-status-index.json",
            "11_source-evidence-dossier-index.json",
            "21_source-presearch-readiness-index.json",
        ],
        "integrity_slots": [
            "access_or_download_record",
            "checksum",
            "file_size",
            "package_manifest",
            "field_map",
            "metadata_profile",
            "derived_paths",
            "rights_status",
            "risk_note",
            "large_source_exception_or_storage",
        ],
        "route_counts": {
            "download_route_count": len(download_routes),
            "checksum_route_count": checksum_count(download_routes),
            "size_route_count": sized_count(download_routes),
            "package_route_count": len(package_routes),
            "field_map_route_count": len(field_routes),
            "metadata_profile_route_count": len(metadata_routes),
            "local_temp_route_count": sum(
                1 for row in download_routes if row.get("local_temp_path")
            ),
        },
        "claim_boundary": [
            "no rights decision",
            "no corpus import approval",
            "no confirmed source promotion",
            "no reading",
            "no component assignment",
            "no inscription identity",
            "no correspondence conclusion",
            "no decipherment conclusion",
        ],
        "review_status": "needs_human_source_access_integrity_review",
        "updated_at": UPDATED_AT,
    }


def source_presearch_readiness_slots(
    source: dict[str, str],
    download_routes: list[dict[str, str]],
    package_routes: list[dict[str, str]],
    field_routes: list[dict[str, str]],
    metadata_routes: list[dict[str, str]],
) -> list[dict[str, str]]:
    target_record_types = sorted(
        {row.get("target_record_type", "") for row in field_routes if row.get("target_record_type")}
    )
    download_statuses = sorted(
        {row.get("download_status", "") for row in download_routes if row.get("download_status")}
    )
    missing_checks: list[str] = []
    if checksum_count(download_routes) < len(download_routes):
        missing_checks.append("which access rows still lack checksum evidence")
    if sized_count(download_routes) < len(download_routes):
        missing_checks.append("which access rows still lack file-size evidence")
    if not package_routes:
        missing_checks.append("which package manifest row must be created")
    if not field_routes:
        missing_checks.append("which field map must be reviewed")
    if not metadata_routes:
        missing_checks.append("whether metadata profile rows are absent by design")
    if not source.get("risk_note"):
        missing_checks.append("which visible risk note should accompany reuse")
    if not missing_checks:
        missing_checks.append("which human reviewer can close remaining route checks")

    return [
        {
            "slot": "visible_source_identity",
            "status": "route_present",
            "evidence": "README.md; 10_source-evidence-dossier.md",
            "human_question": (
                "Which source system, title, provider, URL, scope, and "
                "authority tier can a reviewer cite before opening data rows?"
            ),
        },
        {
            "slot": "access_checksum_size",
            "status": "needs_human_review",
            "evidence": "02_download-route-index.csv; 18_source-access-integrity-review.md",
            "human_question": (
                "Which access or download row has status "
                f"{joined(download_statuses)}; which checksum and size rows "
                "are ready for audit?"
            ),
        },
        {
            "slot": "package_and_field_map",
            "status": "needs_human_review",
            "evidence": "03_package-route-index.csv; 04_field-map-route-index.csv",
            "human_question": (
                "Which package, manifest, and field-map rows can support "
                f"{joined(target_record_types)} without becoming claims?"
            ),
        },
        {
            "slot": "human_dossier_transfer",
            "status": "needs_target_dossier_review",
            "evidence": "14_source-to-dossier-transfer-review.md",
            "human_question": (
                "Which character, inscription, plate, collection, later-form, "
                "or bibliography dossier can receive only a reviewed route?"
            ),
        },
        {
            "slot": "literature_and_dispute_scope",
            "status": "needs_human_literature_review",
            "evidence": "16_source-literature-scope-review.md",
            "human_question": (
                "Which bibliography, database note, proposer, editor, "
                "citation relation, different opinion, or dispute remains "
                "to be opened?"
            ),
        },
        {
            "slot": "rights_risk_public_commit",
            "status": "needs_rights_boundary_review",
            "evidence": "12_source-provenance-fact-matrix.md; 18_source-access-integrity-review.md",
            "human_question": (
                "Which rights status, risk note, size limit, checksum, and "
                "commit-policy issue blocks public promotion?"
            ),
        },
        {
            "slot": "concrete_missing_questions",
            "status": "needs_followup_before_formal_research",
            "evidence": "20_source-presearch-readiness-review.md",
            "human_question": "; ".join(missing_checks),
        },
    ]


def source_presearch_readiness_review_text(
    source: dict[str, str],
    download_routes: list[dict[str, str]],
    package_routes: list[dict[str, str]],
    field_routes: list[dict[str, str]],
    metadata_routes: list[dict[str, str]],
) -> str:
    slots = source_presearch_readiness_slots(
        source,
        download_routes,
        package_routes,
        field_routes,
        metadata_routes,
    )
    lines = [
        "# Source Pre-Research Readiness Review / 来源预研究就绪复核",
        "",
        "## English",
        *wrapped(
            "This human review page tells a researcher what this source object "
            "can support before formal oracle-bone research begins. It gathers "
            "the visible source identity, access evidence, package and field "
            "maps, transfer routes, literature scope, rights boundary, and "
            "concrete missing questions in one readable place."
        ),
        "",
        "## 简体中文",
        *wrapped(
            "本页说明正式甲骨文研究开始前，这个来源对象目前能够支持哪些"
            "人工核查。它把来源身份、访问证据、来源包和字段映射、转入"
            "档案路线、文献范围、权利边界和具体缺失问题集中到一个人类"
            "可读页面。"
        ),
        "",
        "## Source / 来源",
        *bullet("Source ID / 来源 ID", source["source_id"]),
        *bullet("Title / 题名", source["title"]),
        *bullet("Provider / 提供方", source["provider"]),
        *bullet("Source type / 来源类型", source["source_type"]),
        *bullet("Scope / 适用范围", source["scope"]),
        *bullet("Rights status / 权利状态", source["rights_status"]),
        *bullet("Risk note / 风险提示", source["risk_note"]),
        *bullet("Review status / 复核状态", source["review_status"]),
        "",
        "## Human Reading Order / 人工阅读顺序",
        "- Read `README.md` and `10_source-evidence-dossier.md` first.",
        "- Check `12_source-provenance-fact-matrix.md` for source facts.",
        "- Check `14_source-to-dossier-transfer-review.md` before transfer.",
        "- Check `16_source-literature-scope-review.md` for scope and disputes.",
        "- Check `18_source-access-integrity-review.md` before reuse.",
        "- Use JSON and CSV only after the human files are clear.",
        "- 先读 `README.md` 和 `10_source-evidence-dossier.md`。",
        "- 再读 `12_source-provenance-fact-matrix.md` 核对来源事实。",
        "- 转入对象档案前先读 `14_source-to-dossier-transfer-review.md`。",
        "- 通过 `16_source-literature-scope-review.md` 核对范围和争议。",
        "- 复用资料前先读 `18_source-access-integrity-review.md`。",
        "- JSON 和 CSV 只能在人类文件清楚之后作为辅助资料使用。",
        "",
        "## Readiness Slots / 就绪复核槽位",
    ]
    for index, slot in enumerate(slots, start=1):
        lines.extend(
            [
                "",
                f"### {index:02d}. {slot['slot']}",
                *bullet("Status / 状态", slot["status"]),
                *bullet("Evidence / 证据文件", slot["evidence"]),
                *bullet("Question / 待查问题", slot["human_question"]),
            ]
        )
    lines.extend(
        [
            "",
            "## Concrete Questions Before Formal Research / 正式研究前待查问题",
            "- Which visible image, rubbing, plate, catalog, or URL is evidence?",
            "- Which checksum, file size, package row, or field map proves it?",
            "- Which target dossier can receive a route without receiving a claim?",
            "- Which bibliography, proposer, alternate view, or dispute is open?",
            "- Which rights, risk, size, or commit-policy issue blocks reuse?",
            "- 哪个图片、拓片、图版、著录或 URL 是可见证据？",
            "- 哪条 checksum、文件大小、来源包或字段映射记录能证明它？",
            "- 哪个目标档案只能接收路线，而不能接收结论？",
            "- 哪条书目、提出者、不同意见或争议仍需打开？",
            "- 哪个权利、风险、大小或提交策略问题阻止复用？",
            "",
            "## Boundary / 边界",
            "- not a rights decision",
            "- not corpus import approval",
            "- not a confirmed source promotion",
            "- not an accepted reading",
            "- not a component assignment",
            "- not an inscription identity",
            "- not a correspondence conclusion",
            "- not a decipherment conclusion",
            "- 不是权利结论",
            "- 不是语料导入批准",
            "- 不是来源提升结论",
            "- 不是已接受释读",
            "- 不是构件归属",
            "- 不是卜辞身份确认",
            "- 不是字形对应结论",
            "- 不是破译结论",
        ]
    )
    return "\n".join(lines)


def source_presearch_readiness_index_payload(
    source: dict[str, str],
    download_routes: list[dict[str, str]],
    package_routes: list[dict[str, str]],
    field_routes: list[dict[str, str]],
    metadata_routes: list[dict[str, str]],
) -> dict[str, object]:
    slots = source_presearch_readiness_slots(
        source,
        download_routes,
        package_routes,
        field_routes,
        metadata_routes,
    )
    return {
        "record_type": "source_presearch_readiness_index",
        "source_id": source["source_id"],
        "source_title": source["title"],
        "human_entry": "20_source-presearch-readiness-review.md",
        "human_readable_files": [
            "README.md",
            "10_source-evidence-dossier.md",
            "12_source-provenance-fact-matrix.md",
            "14_source-to-dossier-transfer-review.md",
            "16_source-literature-scope-review.md",
            "18_source-access-integrity-review.md",
            "20_source-presearch-readiness-review.md",
        ],
        "ai_support_files": [
            "01_source-packet.json",
            "02_download-route-index.csv",
            "03_package-route-index.csv",
            "04_field-map-route-index.csv",
            "05_metadata-profile-route-index.csv",
            "11_source-evidence-dossier-index.json",
            "13_source-provenance-fact-matrix-index.json",
            "15_source-to-dossier-transfer-index.json",
            "17_source-literature-scope-index.json",
            "19_source-access-integrity-index.json",
        ],
        "readiness_slots": slots,
        "route_counts": {
            "download_route_count": len(download_routes),
            "checksum_route_count": checksum_count(download_routes),
            "size_route_count": sized_count(download_routes),
            "package_route_count": len(package_routes),
            "field_map_route_count": len(field_routes),
            "metadata_profile_route_count": len(metadata_routes),
        },
        "claim_boundary": [
            "no rights decision",
            "no corpus import approval",
            "no confirmed source promotion",
            "no reading",
            "no component assignment",
            "no inscription identity",
            "no correspondence conclusion",
            "no decipherment conclusion",
        ],
        "review_status": "needs_human_source_presearch_readiness_review",
        "updated_at": UPDATED_AT,
    }


def route_detail_section(
    title: str,
    rows: list[dict[str, str]],
    field_labels: list[tuple[str, str]],
    empty_note: str,
) -> list[str]:
    lines = [title]
    if not rows:
        lines.extend(["", *wrapped(empty_note)])
        return lines
    for index, row in enumerate(rows, start=1):
        lines.extend(["", f"### Route {index:03d}"])
        for field, label in field_labels:
            lines.extend(bullet(label, row.get(field, "")))
    return lines


def download_route_evidence_lines(
    download_routes: list[dict[str, str]],
) -> list[str]:
    return route_detail_section(
        "## Download Route Evidence / 下载路线证据",
        download_routes,
        [
            ("download_id", "Download ID / 下载 ID"),
            ("artifact_kind", "Artifact kind / 资料类型"),
            ("download_status", "Status / 状态"),
            ("http_status", "HTTP status / HTTP 状态"),
            ("file_size_bytes", "File size bytes / 文件大小 bytes"),
            ("checksum_sha256", "Checksum SHA-256 / checksum SHA-256"),
            ("commit_policy", "Commit policy / 提交策略"),
            ("local_temp_path", "Local temp path / 本地临时路径"),
            ("risk_note", "Risk note / 风险提示"),
            ("review_status", "Review status / 复核状态"),
        ],
        (
            "No download or access route is recorded in the current source "
            "registers. Add an access route before deriving corpus records."
        ),
    )


def package_manifest_evidence_lines(
    package_routes: list[dict[str, str]],
) -> list[str]:
    return route_detail_section(
        "## Package Manifest Evidence / 来源包清单证据",
        package_routes,
        [
            ("package_file_id", "Package file ID / 来源包文件 ID"),
            ("source_package_id", "Source package ID / 来源包 ID"),
            ("file_name", "File name / 文件名"),
            ("file_kind", "File kind / 文件类型"),
            ("file_size_bytes", "File size bytes / 文件大小 bytes"),
            ("download_id", "Download ID / 下载 ID"),
            ("commit_policy", "Commit policy / 提交策略"),
            ("handling_strategy", "Handling strategy / 处理策略"),
            ("rights_status", "Rights status / 权利状态"),
            ("review_status", "Review status / 复核状态"),
        ],
        (
            "No package manifest route is recorded in the current source "
            "registers. Treat reusable files as unverified until a manifest row "
            "is added."
        ),
    )


def field_map_evidence_lines(
    field_routes: list[dict[str, str]],
) -> list[str]:
    return route_detail_section(
        "## Field Map Evidence / 字段映射证据",
        field_routes,
        [
            ("map_id", "Field map ID / 字段映射 ID"),
            ("source_level", "Source level / 来源层级"),
            ("source_field_or_unit", "Source field or unit / 来源字段或单位"),
            ("source_meaning", "Source meaning / 来源含义"),
            ("target_record_type", "Target record type / 目标记录类型"),
            ("target_project_field", "Target project field / 目标字段"),
            ("import_action", "Import action / 导入动作"),
            ("rights_boundary", "Rights boundary / 权利边界"),
            ("evidence_download_id", "Evidence download ID / 证据下载 ID"),
            ("review_status", "Review status / 复核状态"),
        ],
        (
            "No field-map route is recorded in the current source registers. "
            "Do not import source fields into corpus objects until mappings are "
            "reviewed."
        ),
    )


def metadata_profile_evidence_lines(
    metadata_routes: list[dict[str, str]],
) -> list[str]:
    return route_detail_section(
        "## Metadata Profile Evidence / 元数据概况证据",
        metadata_routes,
        [
            ("profile_id", "Profile ID / 概况 ID"),
            ("evidence_download_id", "Evidence download ID / 证据下载 ID"),
            ("metadata_file", "Metadata file / 元数据文件"),
            ("profile_metric", "Profile metric / 概况指标"),
            ("profile_value", "Profile value / 概况值"),
            ("profile_unit", "Profile unit / 概况单位"),
            ("import_relevance", "Import relevance / 导入相关性"),
            ("caution", "Caution / 提醒"),
            ("review_status", "Review status / 复核状态"),
        ],
        (
            "No metadata profile route is recorded in the current source "
            "registers. Record profile metrics before relying on source-scale "
            "coverage or quality claims."
        ),
    )


def human_research_review_lines() -> list[str]:
    return [
        "## Human Research Review Slots / 人工研究复核槽位",
        "",
        *wrapped(
            "Use the source rows above to decide what can be carried into a "
            "human object dossier. The first review task is not import; it is "
            "to identify visible glyph image, rubbing, photograph, plate, "
            "catalog, inscription, OCR, provenance, findspot, collection, "
            "period, group, variant, near-form, component, later-script, "
            "bibliography, citation, disagreement, and dispute evidence."
        ),
        "",
        *bullet(
            "Glyph image and rubbing check / 字形图像与拓片检查",
            "复核：本来源是否提供可复核的字形图像、拓片、照片或图版页，"
            "以及这些材料能否放入具体单字、卜辞或图版档案。",
        ),
        *bullet(
            "Inscription and catalog context / 卜辞与著录上下文",
            "复核：本来源是否记录卜辞全文、OCR、图版号、页码、合集号、"
            "著录号或数据库编号，以及文本质量和缺失位置。",
        ),
        *bullet(
            "Provenance and dating context / 出处与年代背景",
            "复核：本来源是否记录出土地、馆藏、时期、组类、批次、"
            "收藏对象或考古背景；没有记录时要写成具体缺口。",
        ),
        *bullet(
            "Variant component relation check / 异体构件关系检查",
            "复核：本来源是否只提供候选异体、近形、构件、金文、"
            "小篆、今字或字形演化关系；不得直接写成确认结论。",
        ),
        *bullet(
            "Bibliography citation dispute check / 书目引用争议检查",
            "复核：本来源说明、书目、网页或论文中是否有提出者、"
            "引用关系、不同意见、争议或适用范围限制。",
        ),
        *bullet(
            "Rights and derivative decision / 权利与派生决定",
            "复核：本来源哪些图像、文本、OCR、索引、表格或统计结果"
            "可公开派生，哪些只能保留来源记录和人工复核问题。",
        ),
        "",
        "### Source-To-Dossier Research Lenses / 来源进入档案的研究视角",
        "",
        *wrapped(
            "Glyph image lens: compare each visible glyph image with its "
            "rubbing, photograph, plate, catalog note, and object provenance "
            "before it is copied into a character dossier."
        ),
        "",
        *wrapped(
            "Inscription lens: compare inscription text, OCR text, catalog "
            "number, plate number, page number, Heji number, and text quality "
            "before linking a form to an inscription dossier."
        ),
        "",
        *wrapped(
            "Provenance lens: check findspot, collection, period, group, "
            "batch, museum object, excavation note, and catalog provenance "
            "before using the source for dating or archaeological context."
        ),
        "",
        *wrapped(
            "Form relation lens: treat variant, near-form, component, "
            "bronze-script, seal-script, modern-character, and evolution "
            "relations as candidate comparison evidence until reviewed."
        ),
        "",
        *wrapped(
            "Scholarship lens: keep bibliography, citation, proposer, editor, "
            "scope, disagreement, dispute, and rights evidence visible beside "
            "any later human note derived from this source."
        ),
        "",
        *wrapped(
            "Modern labels, dataset names, source fields, and download-route "
            "captions are not an accepted reading, glyph identity, component "
            "assignment, inscription identity, or historical correspondence."
        ),
        "",
    ]


def source_evidence_dossier_text(
    source: dict[str, str],
    download_routes: list[dict[str, str]],
    package_routes: list[dict[str, str]],
    field_routes: list[dict[str, str]],
    metadata_routes: list[dict[str, str]],
) -> str:
    package_kinds = sorted({row.get("file_kind", "") for row in package_routes if row.get("file_kind")})
    target_record_types = sorted(
        {row.get("target_record_type", "") for row in field_routes if row.get("target_record_type")}
    )
    download_statuses = sorted(
        {row.get("download_status", "") for row in download_routes if row.get("download_status")}
    )
    lines = [
        "# Source Evidence Dossier / 来源证据档案",
        "",
        *wrapped(
            "This human dossier gathers bibliography, access, download, "
            "checksum, rights, risk, field-map, package, and derivative-route "
            "evidence for one source object."
        ),
        "",
        *wrapped(
            "本档案整理来源对象的书目、访问、下载、checksum、权利、风险、"
            "字段映射、来源包和派生路线证据。它服务后续人工复核，不给出"
            "释读或权利结论。"
        ),
        "",
        "## Bibliography And Source Identity / 书目与来源身份",
        *bullet("Source ID / 来源 ID", source["source_id"]),
        *bullet("Title / 标题", source["title"]),
        *bullet("Provider / 提供方", source["provider"]),
        *bullet("Source type / 来源类型", source["source_type"]),
        *bullet("Source URL / 来源链接", source["source_url"]),
        *bullet("Scope / 适用范围", source["scope"]),
        *bullet("Authority tier / 证据等级", source["authority_tier"]),
        *bullet("Adoption status / 采用状态", source["adoption_status"]),
        "",
        "## Access Download Checksum And Size / 访问、下载、checksum 与大小",
        *bullet("Download route count / 下载路线数", len(download_routes)),
        *bullet("Download statuses / 下载状态", joined(download_statuses)),
        *bullet("Checksum route count / checksum 路线数", checksum_count(download_routes)),
        *bullet("Size route count / 大小记录路线数", sized_count(download_routes)),
        *bullet("Local temp route count / 临时路径路线数", local_temp_count(download_routes)),
        *wrapped(
            "Open `02_download-route-index.csv` before reusing any downloaded "
            "file. Check URL, access date, checksum, file size, local archive "
            "path, rights note, and review status."
        ),
        "",
        *wrapped(
            "复用任何下载文件前，应打开 `02_download-route-index.csv`，核对"
            "链接、访问日期、checksum、大小、本地归档路径、权利说明和复核"
            "状态。"
        ),
        "",
        *download_route_evidence_lines(download_routes),
        "",
        "## Package Manifest Field Map And Derivatives / 来源包清单、字段映射与派生记录",
        *bullet("Package route count / 来源包路线数", len(package_routes)),
        *bullet("Package kinds / 来源包类型", joined(package_kinds)),
        *bullet("Field map route count / 字段映射路线数", len(field_routes)),
        *bullet("Target record types / 目标记录类型", joined(target_record_types)),
        *bullet("Metadata route count / metadata 路线数", len(metadata_routes)),
        *wrapped(
            "Package rows, field maps, and metadata profiles are candidate "
            "routes. They do not approve corpus import until a human reviewer "
            "checks the source trail and target object directory."
        ),
        "",
        *wrapped(
            "来源包清单、字段映射和 metadata profile 只是候选路线。必须由"
            "人工复核来源链和目标对象目录后，才可进入语料导入。"
        ),
        "",
        *package_manifest_evidence_lines(package_routes),
        "",
        *field_map_evidence_lines(field_routes),
        "",
        *metadata_profile_evidence_lines(metadata_routes),
        "",
        *human_research_review_lines(),
        "## Scope Evidence Level And Review Status / 适用范围、证据等级与复核状态",
        *bullet("Rights status / 权利状态", source["rights_status"]),
        *bullet("Review status / 复核状态", source["review_status"]),
        *bullet("Risk note / 风险提示", source["risk_note"]),
        *bullet("Processing status card / 处理状态卡", "08_source-processing-status.md"),
        *bullet("Auxiliary JSON / 辅助 JSON", "11_source-evidence-dossier-index.json"),
        "",
        "## Citation Disagreement And Risk Notes / 引用、分歧与风险记录",
        *bullet(
            "Citation relationship / 引用关系",
            "待查：先开 `07_material-access-index.md`、"
            "`11_source-evidence-dossier-index.json`，再核对引用关系。",
        ),
        *bullet(
            "Proposer or editor / 提出者或整理者",
            "待查：先开 `07_material-access-index.md` 和"
            "`04_field-map-route-index.csv` 核对提出者或整理者线索。",
        ),
        *bullet(
            "Different opinions / 不同意见",
            "待查：先开 `07_material-access-index.md` 和"
            "`08_source-processing-status.md` 核对不同意见线索。",
        ),
        *bullet(
            "Disputes / 争议",
            "待查：先开 `07_material-access-index.md`、"
            "`08_source-processing-status.md` 和风险说明核对争议线索。",
        ),
        *wrapped(
            "Do not treat absence of a dispute row as scholarly agreement. It "
            "only means the current preprocessing register still needs a "
            "specific follow-up check for that human review field."
        ),
        "",
        *wrapped(
            "没有争议行不等于学界已经一致，只表示当前预处理登记表尚未采集"
            "这类人工复核字段。"
        ),
        "",
        "## Concrete Questions To Check / 具体待查问题",
        "- Which bibliography or database note defines this source?",
        "- 哪条书目、论文、网页或数据库说明界定本来源？",
        "- Which access, download, checksum, and size rows can be verified?",
        "- 哪些访问、下载、checksum 和大小记录可以复核？",
        "- Which package files are safe derived records rather than raw dumps?",
        "- 哪些来源包文件是安全派生记录，而不是原始大包？",
        "- Which field maps can enter concrete corpus object directories?",
        "- 哪些字段映射可以进入具体语料对象目录？",
        "- Which proposer, citation relation, disagreement, or dispute remains?",
        "- 还缺哪位提出者、引用关系、不同意见或争议？",
        "- Which rights or redistribution risk blocks public promotion?",
        "- 哪些权利或再分发风险阻止公开提升？",
        "",
        "## Boundary / 边界",
        "- not a rights decision",
        "- not corpus import approval",
        "- not a confirmed source promotion",
        "- not an accepted modern label or reading",
        "- not a reading",
        "- not a component assignment",
        "- not an inscription identity",
        "- not a decipherment conclusion",
        "- 不是权利结论",
        "- 不是语料导入批准",
        "- 不是已确认来源提升",
        "- 不是释读",
        "- 不是构件归属",
        "- 不是卜辞身份确认",
        "- 不是破译结论",
    ]
    return "\n".join(lines)


def source_research_brief_text(
    source: dict[str, str],
    download_routes: list[dict[str, str]],
    package_routes: list[dict[str, str]],
    field_routes: list[dict[str, str]],
    metadata_routes: list[dict[str, str]],
) -> str:
    """Render a concise, fact-led human entry for a registered source."""
    lines = [
        "# Source Research Brief / 来源研究资料简报",
        "",
        *wrapped(
            "This brief is the first human reading page for this registered "
            "source. It reports only evidence already recorded in this object "
            "folder and names the limits on research use."
        ),
        "",
        *wrapped(
            "本简报是该已登记来源的首个供人阅读页面。它只陈述本对象目录已经"
            "记录的证据，并明确该资料可用于研究的范围和限制。"
        ),
        "",
        "## Source Identity And Scope / 来源身份与范围",
        *bullet("Title / 标题", source["title"]),
        *bullet("Provider / 提供方", source["provider"]),
        *bullet("Evidence level / 证据等级", source["authority_tier"]),
        *bullet("Registered scope / 已登记范围", source["scope"]),
        *bullet("Source page / 来源页面", source["source_url"]),
        "",
        "## Actual Registered Evidence / 已登记的实际证据",
        *bullet("Download or access records / 下载或访问记录", len(download_routes)),
        *bullet("Recorded checksums / 已记录 checksum", checksum_count(download_routes)),
        *bullet("Recorded file sizes / 已记录文件大小", sized_count(download_routes)),
        *bullet("Package files / 来源包文件", len(package_routes)),
        *bullet("Field mappings / 字段映射", len(field_routes)),
        *bullet("Metadata measurements / 元数据测量", len(metadata_routes)),
        "",
    ]
    for route in download_routes:
        detail = "; ".join(
            value
            for value in [
                route.get("download_id", ""),
                route.get("download_status", ""),
                route.get("file_size_bytes", "") + " bytes"
                if route.get("file_size_bytes")
                else "",
            ]
            if value
        )
        lines.extend(bullet("Recorded access item / 已记录访问项", detail))
    if not download_routes:
        lines.extend(
            bullet(
                "Recorded access item / 已记录访问项",
                "No access row is registered; do not reuse material before one is recorded.",
            )
        )
    lines.extend(
        [
            "",
            "## Usable Material Routes / 可用资料路径",
        ]
    )
    for route in package_routes:
        detail = "; ".join(
            value
            for value in [
                route.get("file_name", ""),
                route.get("file_kind", ""),
                route.get("handling_strategy", ""),
            ]
            if value
        )
        lines.extend(bullet("Package material / 来源包资料", detail))
    for route in field_routes:
        detail = " -> ".join(
            value
            for value in [
                route.get("source_field_or_unit", ""),
                route.get("target_record_type", ""),
                route.get("target_project_field", ""),
            ]
            if value
        )
        lines.extend(bullet("Candidate transfer field / 候选转入字段", detail))
    if not package_routes and not field_routes:
        lines.extend(
            bullet(
                "Usable material route / 可用资料路径",
                "No package or field-map route is registered; source use remains pending.",
            )
        )
    lines.extend(
        [
            "",
            "## Research-Use Limits / 研究使用限制",
            *bullet("Rights status / 权利状态", source["rights_status"]),
            *bullet("Risk note / 风险提示", source["risk_note"]),
            *bullet("Adoption status / 采用状态", source["adoption_status"]),
            *wrapped(
                "Open 10_source-evidence-dossier.md for full checksums, package "
                "rows, field-map details, and source-specific pending questions."
            ),
            "",
            *wrapped(
                "需要完整 checksum、来源包条目、字段映射和具体待查问题时，请打开 "
                "10_source-evidence-dossier.md。"
            ),
            "",
            "## Boundary / 边界",
            "- not a rights decision",
            "- not corpus import approval",
            "- not a reading or component assignment",
            "- not an inscription identity",
            "- not a decipherment conclusion",
            "- 不是权利结论、语料导入批准、释读、构件归属、卜辞身份或破译结论",
        ]
    )
    return "\n".join(lines)


def source_provenance_fact_matrix_text(
    source: dict[str, str],
    fact_rows: list[dict[str, str]],
) -> str:
    lines = [
        "# Source Provenance Fact Matrix / 来源追溯事实矩阵",
        "",
        *wrapped(
            "This human matrix gives a fast review path for the required "
            "provenance facts before any source material is reused."
        ),
        "",
        *wrapped(
            "本矩阵把来源对象必须核查的出处事实集中在同一页，供研究者在"
            "复用任何材料前快速打开、核对和记录缺口。"
        ),
        "",
        "## Human Review Order / 人工复核顺序",
        "- Open `12_source-provenance-fact-matrix.md` first.",
        "- Then open `10_source-evidence-dossier.md` for route detail.",
        "- Use `13_source-provenance-fact-matrix-index.json` only as an index.",
        "- Then use structured route files only as supporting route evidence.",
        "- Do not treat this matrix as a rights or scholarship decision.",
        "- 先读本矩阵，再读来源证据档案。",
        "- 结构化路线文件只作辅助路线证据。",
        "- 本矩阵不作权利结论，也不作学术结论。",
        "",
        "## Source / 来源",
        *bullet("Source ID / 来源 ID", source["source_id"]),
        *bullet("Title / 题名", source["title"]),
        *bullet("Rights status / 权利状态", source["rights_status"]),
        *bullet("Review status / 复核状态", source["review_status"]),
        "",
        "## Provenance Fact Matrix / 出处事实矩阵",
    ]
    for index, row in enumerate(fact_rows, start=1):
        lines.extend(
            [
                "",
                f"### Fact {index:02d}: {row['fact']}",
                *bullet("Status / 状态", row["status"]),
                *bullet("Evidence files / 证据文件", row["evidence_files"]),
                *bullet("Next check / 下一步核查", row["next_check"]),
            ]
        )
    lines.extend(
        [
            "",
            "## Human Research Slots / 人类研究槽位",
            *wrapped(
                "Glyph image and rubbing slot: check whether this source has a "
                "visible glyph image, rubbing, photograph, or plate image that "
                "can later support a concrete character dossier."
            ),
            "",
            *wrapped(
                "Inscription and catalog slot: check inscription text, OCR, "
                "plate number, catalog number, Heji number, page, and text "
                "quality before linking forms to inscriptions."
            ),
            "",
            *wrapped(
                "Provenance slot: check findspot, collection, museum object, "
                "period, group, batch, and excavation note before using the "
                "source for archaeological context."
            ),
            "",
            *wrapped(
                "Relation slot: treat variant, near-form, component, bronze, "
                "seal, modern-character, and evolution relations as candidate "
                "comparison evidence until reviewed."
            ),
            "",
            *wrapped(
                "Scholarship slot: keep bibliography, proposer, editor, "
                "citation relation, disagreement, dispute, and scope limits "
                "visible beside later human notes."
            ),
            "",
            *wrapped(
                "字形图像槽：核查本来源是否有字形图像、拓片、照片或图版。"
            ),
            *wrapped(
                "卜辞著录槽：核查卜辞全文、OCR、图版号、著录号、合集号、页码"
                "和文本质量。"
            ),
            *wrapped(
                "出土背景槽：核查出土地、馆藏、博物馆对象、时期、组类、批次"
                "和考古记录。"
            ),
            *wrapped(
                "关系比较槽：异体、近形、构件、金文、小篆、今字和演化关系"
                "只能作为候选比较证据。"
            ),
            *wrapped(
                "学术争议槽：保留书目、提出者、整理者、引用关系、不同意见、"
                "争议和适用范围限制。"
            ),
            "",
            "## Concrete Next Checks / 具体待查问题",
            "- Which access or download rows have dates, sizes, and checksums?",
            "- Which package manifest rows describe reusable derived records?",
            "- Which field maps can safely feed concrete corpus directories?",
            "- Which rights or redistribution risk blocks public promotion?",
            "- Which derived files should a human reviewer open first?",
            "- 哪些访问或下载记录已有日期、大小和 checksum？",
            "- 哪些来源包 manifest 行说明了可复核派生记录？",
            "- 哪些字段映射可以安全进入具体语料对象目录？",
            "- 哪些权利或再分发风险阻止公开提升？",
            "- 人工复核者应先打开哪些派生文件？",
            "",
            "## Boundary / 边界",
            "- not a rights decision",
            "- not corpus import approval",
            "- not a confirmed source promotion",
            "- not a reading",
            "- not a component assignment",
            "- not an inscription identity",
            "- not a decipherment conclusion",
            "- 不是权利结论",
            "- 不是语料导入批准",
            "- 不是来源提升结论",
            "- 不是释读、构件归属、卜辞身份或破译结论",
        ]
    )
    return "\n".join(lines)


def readme_text(source: dict[str, str], packet: dict[str, object]) -> str:
    lines = [
        f"# {source['source_id']} Source Object",
        "",
        "## English",
        *wrapped(
            "This directory is the object-local human source research entrance "
            "for one registered research source. Open the human source summary, "
            "review sheet, material access index, processing status, evidence "
            "dossier, and fact matrix before using structured support files."
        ),
        "",
        "## 简体中文",
        *wrapped(
            "本目录是一个已登记研究来源的对象内入口。人类可读说明、访问路线、"
            "处理状态、复核提示和 AI 可读索引都放在同一个具体来源对象目录中。"
        ),
        "",
        "## Source Summary / 来源摘要",
        *bullet("Source ID / 来源 ID", source["source_id"]),
        *bullet("Type / 类型", source["source_type"]),
        *bullet("Title / 标题", source["title"]),
        *bullet("Provider / 提供方", source["provider"]),
        *bullet("Authority tier / 权威等级", source["authority_tier"]),
        *bullet("URL / 链接", source["source_url"]),
        *bullet("Adoption status / 采用状态", source["adoption_status"]),
        *bullet("Rights status / 权利状态", source["rights_status"]),
        *bullet("Review status / 复核状态", source["review_status"]),
        "",
        "## Source Research Review Slots / 来源研究复核槽位",
        *wrapped(
            "Glyph image and rubbing: check whether this source provides glyph "
            "images, rubbings, photographs, plates, or catalog images that can "
            "be reviewed inside character, inscription, or plate dossiers."
        ),
        "",
        *wrapped(
            "Inscription and catalog: record which inscription text, OCR, plate "
            "number, catalog number, page, Heji number, or text-quality note can "
            "be traced before linking a form to an inscription dossier."
        ),
        "",
        *wrapped(
            "Provenance and archaeology: check findspot, collection, museum "
            "object, period, group, batch, excavation note, and catalog "
            "provenance before using this source for dating or context."
        ),
        "",
        *wrapped(
            "Form relations: keep variant, near-form, component, bronze-script, "
            "seal-script, modern-character, and evolution relations as candidate "
            "comparison evidence until human review is complete."
        ),
        "",
        *wrapped(
            "Scholarship and dispute: record bibliography, citation relation, "
            "proposer, editor, scope, evidence level, disagreement, and dispute "
            "before reusing this source in a human research note."
        ),
        "",
        *wrapped(
            "Rights and derivatives: decide which image, text, OCR, table, or "
            "statistics derivative can be public, and which material must remain "
            "metadata-only or local-private."
        ),
        "",
        *wrapped(
            "字形图像与拓片：核对本来源是否提供可复核的字形图像、拓片、照片、图版、"
            "著录图像，并判断能否进入单字、卜辞或图版档案。"
        ),
        "",
        *wrapped(
            "卜辞与著录：记录可追溯的卜辞全文、OCR、图版号、著录号、页码、合集号"
            "和文本质量说明，再关联到卜辞档案。"
        ),
        "",
        *wrapped(
            "出土与考古：核对出土地、馆藏、博物馆对象、时期、组类、批次、发掘说明"
            "和著录出处，再用于断代或考古语境。"
        ),
        "",
        *wrapped(
            "字形关系：异体、近形、构件、金文、小篆、今字和字形演化关系只能作为"
            "候选比较证据，等待人工复核。"
        ),
        "",
        *wrapped(
            "文献与争议：记录书目、引用关系、提出者、整理者、适用范围、证据等级、"
            "不同意见和争议，再写入人类研究札记。"
        ),
        "",
        "## Human Source Dossier Entrances / 人类来源档案入口",
        *bullet("Source summary / 来源摘要", "README.md"),
        *bullet("Human review / 人工复核单", "06_human-source-review-sheet.md"),
        *bullet("Material index / 资料访问索引", "07_material-access-index.md"),
        *bullet("Processing status / 处理状态卡", "08_source-processing-status.md"),
        *bullet("Evidence dossier / 来源证据档案", "10_source-evidence-dossier.md"),
        *bullet("Fact matrix / 来源事实矩阵", "12_source-provenance-fact-matrix.md"),
        *bullet("Transfer review / 转入复核", "14_source-to-dossier-transfer-review.md"),
        *bullet("Literature scope / 文献范围", "16_source-literature-scope-review.md"),
        *bullet("Access integrity / 访问完整性", "18_source-access-integrity-review.md"),
        *bullet("Pre-research readiness / 预研究就绪", "20_source-presearch-readiness-review.md"),
        "",
        "## Structured Support Entrances / 结构化辅助入口",
        *bullet("Structured source packet / 结构化来源包", "01_source-packet.json"),
        *bullet("Download routes / 下载或访问路线", "02_download-route-index.csv"),
        *bullet("Package routes / 来源包清单路线", "03_package-route-index.csv"),
        *bullet("Field maps / 字段映射路线", "04_field-map-route-index.csv"),
        *bullet("Metadata profiles / 元数据概况路线", "05_metadata-profile-route-index.csv"),
        *bullet("Status index / 处理状态索引", "09_source-processing-status-index.json"),
        *bullet("Access integrity index / 访问完整性索引", "19_source-access-integrity-index.json"),
        *bullet("Readiness index / 就绪索引", "21_source-presearch-readiness-index.json"),
        "",
        *wrapped(
            "Structured support files only serve the human source dossier. They "
            "must not replace the source summary, review sheet, evidence "
            "dossier, fact matrix, rights note, or concrete next-check questions."
        ),
        "",
        *wrapped(
            "结构化辅助文件只服务人类来源档案，不得替代来源摘要、复核单、证据档案、"
            "事实矩阵、权利说明或具体待查问题。"
        ),
        "",
        "## Evidence Counts / 证据计数",
        *bullet("Download evidence count / 下载证据数", packet["download_route_count"]),
        *bullet("Package evidence count / 来源包证据数", packet["package_route_count"]),
        *bullet("Field-map evidence count / 字段映射证据数", packet["field_map_route_count"]),
        *bullet("Metadata profile count / 元数据概况数", packet["metadata_profile_route_count"]),
        "",
        "## Risk And Boundary / 风险与边界",
        *wrapped(str(source["risk_note"])),
        "",
        *wrapped(
            "These rows are preparation-stage source routes. They are not rights "
            "clearance, not an import decision, not a confirmed reading, not a "
            "component assignment, not an inscription identity, and not a "
            "decipherment conclusion."
        ),
        "",
        *wrapped(
            "这些记录只是准备阶段的来源路线。它们不是权利清理结论，不是导入决定，"
            "不是已确认释读，不是构件归属，不是卜辞身份结论，也不是破译结论。"
        ),
    ]
    return "\n".join(lines)


def material_access_index_text(
    source: dict[str, str],
    packet: dict[str, object],
    download_routes: list[dict[str, str]],
    package_routes: list[dict[str, str]],
    field_routes: list[dict[str, str]],
    metadata_routes: list[dict[str, str]],
) -> str:
    download_statuses = sorted({row.get("download_status", "") for row in download_routes if row.get("download_status")})
    package_kinds = sorted({row.get("file_kind", "") for row in package_routes if row.get("file_kind")})
    target_record_types = sorted({row.get("target_record_type", "") for row in field_routes if row.get("target_record_type")})
    metadata_metrics = sorted({row.get("profile_metric", "") for row in metadata_routes if row.get("profile_metric")})
    lines = [
        f"# {source['source_id']} Material Access Index",
        "",
        "## English",
        *wrapped(
            "This object-local index tells a human reviewer what source "
            "materials are visible here and which structured support files "
            "carry the route data. It is an access map, not a rights decision."
        ),
        "",
        "## 简体中文",
        *wrapped(
            "本索引说明同一来源对象目录中有哪些资料入口，以及哪些结构化辅助文件保存"
            "结构化路线。它只是访问地图，不是权利结论或学术结论。"
        ),
        "",
        "## Human-Readable Entrances / 人类可读入口",
        *bullet("Source summary / 来源摘要", "README.md"),
        *bullet("Human review sheet / 人工复核单", "06_human-source-review-sheet.md"),
        *bullet("Material access index / 资料访问索引", "07_material-access-index.md"),
        *bullet("Processing status card / 处理状态卡", "08_source-processing-status.md"),
        *bullet("Evidence dossier / 来源证据档案", "10_source-evidence-dossier.md"),
        *bullet("Fact matrix / 来源事实矩阵", "12_source-provenance-fact-matrix.md"),
        *bullet("Transfer review / 转入复核", "14_source-to-dossier-transfer-review.md"),
        *bullet("Literature scope / 文献范围", "16_source-literature-scope-review.md"),
        *bullet("Access integrity / 访问完整性", "18_source-access-integrity-review.md"),
        "",
        "## Structured Support Entrances / 结构化辅助入口",
        *bullet("Structured source packet / 结构化来源包", "01_source-packet.json"),
        *bullet("Download route table / 下载路线表", "02_download-route-index.csv"),
        *bullet("Package route table / 来源包路线表", "03_package-route-index.csv"),
        *bullet("Field-map route table / 字段映射表", "04_field-map-route-index.csv"),
        *bullet("Metadata profile table / 元数据概况表", "05_metadata-profile-route-index.csv"),
        *bullet("Processing status JSON / 处理状态索引", "09_source-processing-status-index.json"),
        *bullet("Access integrity JSON / 访问完整性索引", "19_source-access-integrity-index.json"),
        "",
        *wrapped(
            "Structured support files only serve the human source dossier. They "
            "must not replace the source summary, review sheet, evidence "
            "dossier, fact matrix, rights note, or concrete next-check questions."
        ),
        "",
        *wrapped(
            "结构化辅助文件只服务人类来源档案，不得替代来源摘要、复核单、证据档案、"
            "事实矩阵、权利说明或具体待查问题。"
        ),
        "",
        "## Route Signals / 路线信号",
        *bullet("Download route count / 下载路线数", len(download_routes)),
        *bullet("Download statuses / 下载状态", joined(download_statuses)),
        *bullet("Package route count / 来源包路线数", len(package_routes)),
        *bullet("Package kinds / 来源包类型", joined(package_kinds)),
        *bullet("Field map count / 字段映射数", len(field_routes)),
        *bullet("Target records / 目标记录", joined(target_record_types)),
        *bullet("Metadata profile count / 元数据概况数", len(metadata_routes)),
        *bullet("Profile metrics / 概况指标", joined(metadata_metrics)),
        "",
        "## Next Review Step / 下一步复核入口",
        *bullet("Rights status / 权利状态", source["rights_status"]),
        *bullet("Review status / 复核状态", source["review_status"]),
        *bullet("Risk note / 风险提示", source["risk_note"]),
        "",
        *wrapped(
            "Inspect the route rows above, then decide whether source-safe "
            "visual or text derivatives can be added inside the relevant "
            "concrete corpus object directories."
        ),
        "",
        *wrapped(
            "请先复核上述路线，再判断能否把安全的图像或文本派生记录放入对应的具体"
            "语料对象目录。"
        ),
        "",
        "## Boundary / 边界",
        *wrapped(
            "This index does not collect new evidence, clear rights, promote a "
            "source, import corpus records, confirm a character identity, assign "
            "a component, identify an inscription, confirm an evolution chain, "
            "or make a decipherment conclusion."
        ),
        "",
        *wrapped(
            "本索引不采集新证据，不完成权利清理，不提升来源等级，不导入正式语料，"
            "不确认字形身份，不指定构件，不确认卜辞身份，不确认演化链，也不作"
            "释读结论。"
        ),
    ]
    return "\n".join(lines)


def review_sheet_text(source: dict[str, str]) -> str:
    lines = [
        f"# {source['source_id']} Human Source Review Sheet",
        "",
        "## Source Provenance Review / 来源出处复核",
        *wrapped(
            "Use this sheet to decide which source routes have enough "
            "provenance for safe preprocessing, and which routes still need "
            "human review before any derived record is promoted."
        ),
        "",
        *wrapped(
            "本表用于判断哪些来源路线已有足够出处证据，可以进入安全的"
            "预处理；哪些路线仍需人工复核，才能提升为派生记录。"
        ),
        "",
        "## Review Scope / 复核范围",
        *wrapped(
            "Review source provenance, access status, package or file metadata, "
            "field mapping, rights status, and whether any raw material is safe "
            "to promote into object-local derived records."
        ),
        "",
        *wrapped(
            "只复核来源出处、访问状态、来源包或文件 metadata、字段映射、权利状态，"
            "以及是否可以把某些原始资料提升为对象内派生记录。"
        ),
        "",
        "## Bibliographic And Database Scope Review / 文献与数据库适用范围复核",
        *wrapped(
            "For books, papers, web pages, museum records, and databases, record "
            "the bibliography or source note, scope, evidence level, proposer "
            "or provider, citation relationship, disagreements, and disputes "
            "as review items before derived records are reused."
        ),
        "",
        *wrapped(
            "对图书、论文、网页、博物馆记录和数据库，应先记录书目或来源说明、"
            "适用范围、证据等级、提出者或提供方、引用关系、不同意见和争议，"
            "再复用任何派生记录。"
        ),
        "",
        "## Checklist / 清单",
        "- [ ] Source register row checked against `01_source-packet.json`",
        "- [ ] Download routes checked in `02_download-route-index.csv`",
        "- [ ] Package manifest checked in `03_package-route-index.csv`",
        "- [ ] Field maps checked in `04_field-map-route-index.csv`",
        "- [ ] Metadata profiles checked in `05_metadata-profile-route-index.csv`",
        "- [ ] Processing card checked in `08_source-processing-status.md`",
        "- [ ] Rights status reviewed before any asset promotion",
        "- [ ] No reading, identity, component, or inscription claim added",
        "",
        "## Concrete Questions To Check / 具体待查问题",
        "- [ ] Which source register row anchors this source?",
        "- [ ] 哪条来源登记行可以定位本来源？",
        "- [ ] Which download or access routes have dates, sizes, and checksums?",
        "- [ ] 哪些下载或访问路线已有日期、大小和 checksum？",
        "- [ ] Which package manifest rows describe reusable derived files?",
        "- [ ] 哪些来源包 manifest 行描述了可复用的派生文件？",
        "- [ ] Which field maps can safely feed corpus object records?",
        "- [ ] 哪些字段映射可以安全进入语料对象？",
        "- [ ] What rights or redistribution risk blocks public promotion?",
        "- [ ] 哪些权利或再分发风险阻止公开提升？",
        "- [ ] Which object-local corpus directories should receive derivatives?",
        "- [ ] 哪些对象内语料目录应接收派生记录？",
        "- [ ] Which bibliography, paper, web page, or database note defines",
        "  this source?",
        "- [ ] 哪条书目、论文、网页或数据库说明界定本来源？",
        "- [ ] What scope and evidence level should be recorded?",
        "- [ ] 应记录什么适用范围和证据等级？",
        "- [ ] Which proposer, citation relation, disagreement, or dispute",
        "  should be preserved?",
        "- [ ] 哪位提出者、引用关系、不同意见或争议需要保留？",
        "",
        "## Status / 状态",
        *bullet("Source ID / 来源 ID", source["source_id"]),
        *bullet("Rights status / 权利状态", source["rights_status"]),
        *bullet("Review status / 复核状态", "needs_human_source_review"),
        *bullet("Decipherment claim status / 释读结论状态", "no_claim"),
    ]
    return "\n".join(lines)


def processing_status_text(
    source: dict[str, str],
    status_index: dict[str, object],
) -> str:
    lines = [
        f"# {source['source_id']} Source Processing Status",
        "",
        "## English",
        *wrapped(
            "This card summarizes the current preprocessing stage for this "
            "source. It shows what has evidence, what has only candidate routes, "
            "and what still needs human review before formal research use."
        ),
        "",
        "## 简体中文",
        *wrapped(
            "本卡片汇总该来源目前的预处理阶段。它说明哪些环节已有证据，哪些只是"
            "候选路线，哪些仍需人工复核后才能进入正式研究。"
        ),
        "",
        "## Source / 来源",
        *bullet("Title / 标题", source["title"]),
        *bullet("Provider / 提供方", source["provider"]),
        *bullet("Rights status / 权利状态", source["rights_status"]),
        *bullet("Risk note / 风险提示", source["risk_note"]),
        "",
        "## Phase Status / 阶段状态",
    ]
    for phase in status_index["phases"]:
        lines.extend(
            [
                "",
                f"### {phase['phase']}",
                *bullet("Status / 状态", phase["status"]),
                *bullet("Evidence file / 证据文件", phase["evidence_file"]),
                *bullet("Evidence count / 证据数量", phase.get("evidence_count", "not recorded")),
                *bullet("Review status / 复核状态", phase["review_status"]),
            ]
        )
    missing = status_index["missing_or_review_items"]
    lines.extend(
        [
            "",
            "## Missing Or Review Items / 缺失或待复核项",
            *bullet("Items / 项目", joined(list(missing), "none_recorded")),
            "",
            "## Concrete Questions To Check / 具体待查问题",
            "- 应核对哪些下载、访问或 checksum 记录？",
            "- 哪些来源包 manifest 行需要打开原始路径复核？",
            "- 哪些字段映射可以安全进入语料对象？",
            "- 哪些 metadata profile 行提示数据质量或 OCR 风险？",
            "- 哪些权利状态或风险提示阻止公开提交原始资料？",
            "- 哪些派生记录路径仍缺少人工复核结论？",
            "",
            "## Human Next Step / 人工下一步",
            *wrapped(
                "Open the route CSV files listed above, compare them with the "
                "source register and download log, and record whether derived "
                "records can be safely created in the relevant corpus objects."
            ),
            "",
            *wrapped(
                "请打开上述路线 CSV，与来源登记和下载日志比对，并记录能否在相应语料"
                "对象中安全生成派生记录。"
            ),
            "",
            "## Boundary / 边界",
            *wrapped(
                "All statuses here are infrastructure statuses. They are not "
                "scholarly conclusions and do not start formal decipherment work."
            ),
            "",
            *wrapped(
                "这里的所有状态都是资料工程状态，不是学术结论，也不开始正式释读研究。"
            ),
        ]
    )
    return "\n".join(lines)


def build_materials(root: Path) -> dict[str, int]:
    root = root.resolve()
    sources = read_csv(root / SOURCE_INDEX)
    downloads_by_source = index_by_source(read_csv(root / DOWNLOAD_MANIFEST))
    download_logs_by_source = index_by_source(read_csv(root / DOWNLOAD_LOG))
    packages_by_source = index_by_source(read_csv(root / PACKAGE_MANIFEST))
    fields_by_source = index_by_source(read_csv(root / FIELD_MAP))
    metadata_by_source = index_by_source(read_csv(root / METADATA_PROFILE))

    for index, source in enumerate(sources, start=1):
        source_id = source["source_id"]
        object_dir = root / OUTPUT_ROOT / source_dir_name(index, source_id)
        object_dir.mkdir(parents=True, exist_ok=True)
        download_routes = build_download_routes(
            source_id,
            downloads_by_source.get(source_id, []),
            download_logs_by_source.get(source_id, []),
        )
        package_routes = add_route_ids(
            source_id, packages_by_source.get(source_id, []), "package-route", "package_route_id"
        )
        field_routes = add_route_ids(source_id, fields_by_source.get(source_id, []), "field-route", "field_route_id")
        metadata_routes = add_route_ids(
            source_id, metadata_by_source.get(source_id, []), "metadata-route", "metadata_route_id"
        )
        packet = source_packet(
            source,
            object_dir.relative_to(root),
            download_routes,
            package_routes,
            field_routes,
            metadata_routes,
        )
        status_index = build_processing_status_index(
            source,
            download_routes,
            package_routes,
            field_routes,
            metadata_routes,
        )
        fact_rows = source_provenance_fact_rows(
            source,
            download_routes,
            package_routes,
            field_routes,
            metadata_routes,
        )
        write_human_markdown(object_dir / "README.md", f"{source_id}/README.md", readme_text(source, packet))
        write_json(object_dir / "01_source-packet.json", packet)
        write_csv(object_dir / "02_download-route-index.csv", download_routes, DOWNLOAD_ROUTE_FIELDS)
        write_csv(object_dir / "03_package-route-index.csv", package_routes, PACKAGE_ROUTE_FIELDS)
        write_csv(object_dir / "04_field-map-route-index.csv", field_routes, FIELD_ROUTE_FIELDS)
        write_csv(object_dir / "05_metadata-profile-route-index.csv", metadata_routes, METADATA_ROUTE_FIELDS)
        write_human_markdown(
            object_dir / "06_human-source-review-sheet.md",
            f"{source_id}/06_human-source-review-sheet.md",
            review_sheet_text(source),
        )
        write_human_markdown(
            object_dir / "07_material-access-index.md",
            f"{source_id}/07_material-access-index.md",
            material_access_index_text(
                source,
                packet,
                download_routes,
                package_routes,
                field_routes,
                metadata_routes,
            ),
        )
        write_human_markdown(
            object_dir / "08_source-processing-status.md",
            f"{source_id}/08_source-processing-status.md",
            processing_status_text(source, status_index),
        )
        write_json(object_dir / "09_source-processing-status-index.json", status_index)
        write_human_markdown(
            object_dir / "10_source-evidence-dossier.md",
            f"{source_id}/10_source-evidence-dossier.md",
            source_evidence_dossier_text(
                source,
                download_routes,
                package_routes,
                field_routes,
                metadata_routes,
            ),
        )
        write_json(
            object_dir / "11_source-evidence-dossier-index.json",
            source_evidence_dossier_index_payload(
                source,
                download_routes,
                package_routes,
                field_routes,
                metadata_routes,
            ),
        )
        write_human_markdown(
            object_dir / "12_source-provenance-fact-matrix.md",
            f"{source_id}/12_source-provenance-fact-matrix.md",
            source_provenance_fact_matrix_text(source, fact_rows),
        )
        write_json(
            object_dir / "13_source-provenance-fact-matrix-index.json",
            source_provenance_fact_matrix_index_payload(source, fact_rows),
        )
        write_human_markdown(
            object_dir / "14_source-to-dossier-transfer-review.md",
            f"{source_id}/14_source-to-dossier-transfer-review.md",
            source_to_dossier_transfer_review_text(source),
        )
        write_json(
            object_dir / "15_source-to-dossier-transfer-index.json",
            source_to_dossier_transfer_index_payload(source),
        )
        write_human_markdown(
            object_dir / "16_source-literature-scope-review.md",
            f"{source_id}/16_source-literature-scope-review.md",
            source_literature_scope_review_text(source),
        )
        write_json(
            object_dir / "17_source-literature-scope-index.json",
            source_literature_scope_index_payload(source),
        )
        write_human_markdown(
            object_dir / "18_source-access-integrity-review.md",
            f"{source_id}/18_source-access-integrity-review.md",
            source_access_integrity_review_text(
                source,
                download_routes,
                package_routes,
                field_routes,
                metadata_routes,
            ),
        )
        write_json(
            object_dir / "19_source-access-integrity-index.json",
            source_access_integrity_index_payload(
                source,
                download_routes,
                package_routes,
                field_routes,
                metadata_routes,
            ),
        )
        write_human_markdown(
            object_dir / "20_source-presearch-readiness-review.md",
            f"{source_id}/20_source-presearch-readiness-review.md",
            source_presearch_readiness_review_text(
                source,
                download_routes,
                package_routes,
                field_routes,
                metadata_routes,
            ),
        )
        write_json(
            object_dir / "21_source-presearch-readiness-index.json",
            source_presearch_readiness_index_payload(
                source,
                download_routes,
                package_routes,
                field_routes,
                metadata_routes,
            ),
        )
        write_human_markdown(
            object_dir / "22_source-research-brief.md",
            f"{source_id}/22_source-research-brief.md",
            source_research_brief_text(
                source,
                download_routes,
                package_routes,
                field_routes,
                metadata_routes,
            ),
        )
    return {"source_object_count": len(sources)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=Path.cwd(), type=Path)
    args = parser.parse_args()
    result = build_materials(args.root)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
