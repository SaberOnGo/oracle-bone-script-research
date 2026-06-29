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
            "fact": "Source identity",
            "status": "present" if source.get("source_id") and source.get("title") else "needs_review",
            "evidence_files": "01_source-packet.json; 10_source-evidence-dossier.md",
            "next_check": "Check source_id, title, provider, URL, scope, and authority tier.",
        },
        {
            "fact": "Access or download record",
            "status": "present" if download_routes else "missing_route",
            "evidence_files": "02_download-route-index.csv",
            "next_check": "Check URL, access status, HTTP status, and local route notes.",
        },
        {
            "fact": "Checksum evidence",
            "status": "present" if checksum_count(download_routes) else "needs_review",
            "evidence_files": "02_download-route-index.csv",
            "next_check": "Confirm SHA-256 rows before reusing any downloaded file.",
        },
        {
            "fact": "File size evidence",
            "status": "present" if sized_count(download_routes) else "needs_review",
            "evidence_files": "02_download-route-index.csv; 03_package-route-index.csv",
            "next_check": "Compare download sizes with package manifest file sizes.",
        },
        {
            "fact": "Rights status",
            "status": "present" if source.get("rights_status") else "needs_review",
            "evidence_files": "01_source-packet.json; 03_package-route-index.csv",
            "next_check": "Treat rights status as a review note, not a license grant.",
        },
        {
            "fact": "Risk note",
            "status": "present" if source.get("risk_note") else "needs_review",
            "evidence_files": "01_source-packet.json; 07_material-access-index.md",
            "next_check": "Keep the visible risk note beside any future derivative.",
        },
        {
            "fact": "Package manifest",
            "status": "present" if package_routes else "missing_route",
            "evidence_files": "03_package-route-index.csv",
            "next_check": "Open package rows before treating files as reusable derivatives.",
        },
        {
            "fact": "Field map",
            "status": "present" if field_routes else "missing_route",
            "evidence_files": "04_field-map-route-index.csv",
            "next_check": "Review source fields before moving data into corpus objects.",
        },
        {
            "fact": "Derived paths",
            "status": "present",
            "evidence_files": "; ".join(derived_files),
            "next_check": (
                "Open human files first, then use structured support indexes "
                "only as routes."
            ),
        },
        {
            "fact": "Review status",
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
        ],
        "ai_support_files": [
            "01_source-packet.json",
            "02_download-route-index.csv",
            "03_package-route-index.csv",
            "04_field-map-route-index.csv",
            "09_source-processing-status-index.json",
            "11_source-evidence-dossier-index.json",
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
            "This directory is the object-local human and AI entrance for one "
            "registered research source. It keeps readable notes, route indexes, "
            "processing status, review prompts, and machine-readable packets "
            "inside the same concrete source object directory."
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
        "## Local Entrances / 本目录入口",
        *bullet("AI packet / AI 来源包", "01_source-packet.json"),
        *bullet("Download routes / 下载或访问路线", "02_download-route-index.csv"),
        *bullet("Package routes / 来源包清单路线", "03_package-route-index.csv"),
        *bullet("Field maps / 字段映射路线", "04_field-map-route-index.csv"),
        *bullet("Metadata profiles / 元数据概况路线", "05_metadata-profile-route-index.csv"),
        *bullet("Human review / 人工复核单", "06_human-source-review-sheet.md"),
        *bullet("Material index / 资料访问索引", "07_material-access-index.md"),
        *bullet("Processing status / 处理状态卡", "08_source-processing-status.md"),
        *bullet("Status JSON / 处理状态索引", "09_source-processing-status-index.json"),
        "",
        "## Route Counts / 路线数量",
        *bullet("Download route count / 下载路线数", packet["download_route_count"]),
        *bullet("Package route count / 来源包路线数", packet["package_route_count"]),
        *bullet("Field map route count / 字段映射路线数", packet["field_map_route_count"]),
        *bullet("Metadata profile route count / 元数据概况路线数", packet["metadata_profile_route_count"]),
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
            "materials are visible here and which AI-readable files carry the "
            "structured routes. It is an access map, not a rights decision."
        ),
        "",
        "## 简体中文",
        *wrapped(
            "本索引说明同一来源对象目录中有哪些资料入口，以及哪些 AI 可读文件保存"
            "结构化路线。它只是访问地图，不是权利结论或学术结论。"
        ),
        "",
        "## Human-Readable Entrances / 人类可读入口",
        *bullet("Source summary / 来源摘要", "README.md"),
        *bullet("Human review sheet / 人工复核单", "06_human-source-review-sheet.md"),
        *bullet("Material access index / 资料访问索引", "07_material-access-index.md"),
        *bullet("Processing status card / 处理状态卡", "08_source-processing-status.md"),
        "",
        "## AI-Readable Entrances / AI 可读入口",
        *bullet("Source packet / 来源包", "01_source-packet.json"),
        *bullet("Download route table / 下载路线表", "02_download-route-index.csv"),
        *bullet("Package route table / 来源包路线表", "03_package-route-index.csv"),
        *bullet("Field-map route table / 字段映射表", "04_field-map-route-index.csv"),
        *bullet("Metadata profile table / 元数据概况表", "05_metadata-profile-route-index.csv"),
        *bullet("Processing status JSON / 处理状态索引", "09_source-processing-status-index.json"),
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
