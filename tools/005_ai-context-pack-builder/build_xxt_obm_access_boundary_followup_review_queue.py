#!/usr/bin/env python3
"""Build metadata-only follow-up review queue rows for Xiaoxuetang OBM access-boundary pages."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


SOURCE_INDEX = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/"
    "001_all-sources-index.csv"
)
SOURCE_DOWNLOAD_MANIFEST = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/"
    "003_source-download-manifest.csv"
)
SOURCE_DOWNLOAD_LOG = Path("project_registry/006_large-source-register/002_source-download-log.csv")
CORE_ACCESS_PROFILE = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/"
    "011_core-institutional-access-profile.csv"
)
OBM_ABBREVIATION_STAGING = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/"
    "012_obm-abbreviation-staging.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "074_ai-agent-xxt-obm-access-boundary-followup-review-queue.csv"
)
UPDATED_AT = "2026-06-11"
TARGET_SOURCE_ID = "src-xiaoxuetang-obm"
FOLLOWUP_METHOD = "manual_browser_or_institutional_export_required"
RESEARCH_BOUNDARY = "xxt_obm_access_boundary_followup_review_queue_not_scholarship"
EVIDENCE_COLLECTION_STATUS = "followup_review_not_started"
HUMAN_REVIEW_STATUS = "not_started"
FORMAL_SCHEMA_COMPATIBILITY_STATUS = "not_formal_inscription_or_obs_char_schema"
IDENTITY_CLAIM_STATUS = "no_identity_claim"
NO_CLAIM = "no_claim"
CAUTION = (
    "This queue row is a metadata-only follow-up route for an official Xiaoxuetang OBM page. "
    "It records registered source, download, access-profile, and staged-abbreviation routes for "
    "later manual or institutional-access review; it is not a Heji row import, not an old-catalog "
    "confirmation, not a collection/object match, not a formal inscription assignment, and not a "
    "decipherment conclusion."
)

DOWNLOAD_PRIORITY = {
    "dl-xxt-obm-appendix01": ("1", "appendix_old_catalog_abbrev_followup"),
    "dl-xxt-obm-appendix02": ("2", "appendix_holding_abbrev_followup"),
    "dl-xxt-obm-example": ("3", "source_table_rules_followup"),
    "dl-xxt-obm-guide": ("4", "user_guide_followup"),
}

OUTPUT_FIELDS = [
    "obm_followup_review_task_id",
    "priority_rank",
    "priority_bucket",
    "followup_method",
    "source_id",
    "source_title",
    "targeted_download_id",
    "targeted_url",
    "artifact_kind",
    "commit_policy",
    "download_status",
    "http_status",
    "logged_file_size_bytes",
    "logged_checksum_sha256",
    "profile_match_count",
    "profile_ids",
    "profile_areas",
    "profile_review_statuses",
    "profile_normalized_values",
    "staging_row_count",
    "staging_row_kind_counts",
    "staging_review_statuses",
    "route_file_count",
    "missing_route_file_count",
    "route_file_review_status",
    "expected_output_path",
    "route_files_to_open",
    "required_review_sections",
    "required_next_checks",
    "evidence_collection_status",
    "human_review_status",
    "formal_schema_compatibility_status",
    "rights_decision_status",
    "source_promotion_status",
    "identity_claim_status",
    "assignment_status",
    "decipherment_claim_status",
    "component_claim_status",
    "evolution_chain_claim_status",
    "research_boundary",
    "rights_status",
    "risk_note",
    "caution",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def _compact(values: list[str]) -> str:
    return ";".join(value for value in values if value)


def _route_files(download_id: str) -> list[str]:
    files = [
        SOURCE_INDEX.as_posix(),
        SOURCE_DOWNLOAD_MANIFEST.as_posix(),
        SOURCE_DOWNLOAD_LOG.as_posix(),
        CORE_ACCESS_PROFILE.as_posix(),
    ]
    if download_id in {"dl-xxt-obm-appendix01", "dl-xxt-obm-appendix02"}:
        files.append(OBM_ABBREVIATION_STAGING.as_posix())
    return files


def _route_file_status(root: Path, route_files: list[str]) -> tuple[int, str]:
    missing_count = sum(1 for route_file in route_files if not (root / route_file).exists())
    status = "reviewed_route_files_exist" if missing_count == 0 else "route_files_missing"
    return missing_count, status


def _expected_output_path(priority_rank: str, download_id: str) -> str:
    return (
        "doc/public/user_research/008_xxt-obm-access-boundary-review-queues/"
        "001_access-restricted-pages/"
        f"{int(priority_rank):04d}_{download_id}_review-log.md"
    )


def _by_key(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {row[key]: row for row in rows}


def build_followup_review_rows(
    source_rows: list[dict[str, str]],
    manifest_rows: list[dict[str, str]],
    download_rows: list[dict[str, str]],
    profile_rows: list[dict[str, str]],
    staging_rows: list[dict[str, str]],
    root: Path,
) -> list[dict[str, str]]:
    source_row = _by_key(source_rows, "source_id")[TARGET_SOURCE_ID]
    manifest_by_id = _by_key(manifest_rows, "download_id")
    download_by_id = _by_key(download_rows, "download_id")

    profile_rows_by_download: dict[str, list[dict[str, str]]] = {}
    for row in profile_rows:
        if row["source_id"] != TARGET_SOURCE_ID:
            continue
        profile_rows_by_download.setdefault(row["evidence_download_id"], []).append(row)

    staging_rows_by_download: dict[str, list[dict[str, str]]] = {}
    for row in staging_rows:
        staging_rows_by_download.setdefault(row["evidence_download_id"], []).append(row)

    results: list[dict[str, str]] = []
    for download_id, (priority_rank, priority_bucket) in sorted(
        DOWNLOAD_PRIORITY.items(), key=lambda item: int(item[1][0])
    ):
        manifest_row = manifest_by_id[download_id]
        download_row = download_by_id[download_id]
        matched_profiles = profile_rows_by_download.get(download_id, [])
        matched_staging_rows = staging_rows_by_download.get(download_id, [])
        route_files = _route_files(download_id)
        missing_route_file_count, route_file_review_status = _route_file_status(root, route_files)
        kind_counter: dict[str, int] = {}
        for row in matched_staging_rows:
            kind = row["abbreviation_kind"]
            kind_counter[kind] = kind_counter.get(kind, 0) + 1
        staging_kind_counts = _compact(
            [f"{kind}={count}" for kind, count in sorted(kind_counter.items())]
        )
        results.append(
            {
                "obm_followup_review_task_id": f"xxt-obm-followup-review-{int(priority_rank):04d}",
                "priority_rank": priority_rank,
                "priority_bucket": priority_bucket,
                "followup_method": FOLLOWUP_METHOD,
                "source_id": TARGET_SOURCE_ID,
                "source_title": source_row["title"],
                "targeted_download_id": download_id,
                "targeted_url": manifest_row["url"],
                "artifact_kind": manifest_row["artifact_kind"],
                "commit_policy": manifest_row["commit_policy"],
                "download_status": download_row["status"],
                "http_status": download_row["http_status"],
                "logged_file_size_bytes": download_row["file_size_bytes"],
                "logged_checksum_sha256": download_row["checksum_sha256"],
                "profile_match_count": str(len(matched_profiles)),
                "profile_ids": _compact([row["profile_id"] for row in matched_profiles]),
                "profile_areas": _compact([row["profile_area"] for row in matched_profiles]),
                "profile_review_statuses": _compact(
                    [f"{row['profile_id']}={row['review_status']}" for row in matched_profiles]
                ),
                "profile_normalized_values": _compact(
                    [f"{row['profile_id']}={row['normalized_project_value']}" for row in matched_profiles]
                ),
                "staging_row_count": str(len(matched_staging_rows)),
                "staging_row_kind_counts": staging_kind_counts,
                "staging_review_statuses": _compact(
                    [f"{row['abbrev_row_id']}={row['review_status']}" for row in matched_staging_rows[:5]]
                ),
                "route_file_count": str(len(route_files)),
                "missing_route_file_count": str(missing_route_file_count),
                "route_file_review_status": route_file_review_status,
                "expected_output_path": _expected_output_path(priority_rank, download_id),
                "route_files_to_open": _compact(route_files),
                "required_review_sections": (
                    "source_register_row;source_download_manifest_row;download_log_row;"
                    "access_profile_rows;staging_rows_when_available;official_access_boundary;review_log"
                ),
                "required_next_checks": (
                    "open_registered_source_and_download_rows;"
                    "open_access_profile_rows;"
                    + (
                        "open_staging_rows_before_old_catalog_or_holding_claims;"
                        if matched_staging_rows
                        else "review_access_boundary_before_manual_followup;"
                    )
                    + "use_manual_browser_or_institutional_export_before_any_row_level_claim;"
                    + "record_no_identity_assignment_or_decipherment_claim"
                ),
                "evidence_collection_status": EVIDENCE_COLLECTION_STATUS,
                "human_review_status": HUMAN_REVIEW_STATUS,
                "formal_schema_compatibility_status": FORMAL_SCHEMA_COMPATIBILITY_STATUS,
                "rights_decision_status": "no_new_rights_decision",
                "source_promotion_status": "not_promoted",
                "identity_claim_status": IDENTITY_CLAIM_STATUS,
                "assignment_status": "not_applicable_source_level_followup_only",
                "decipherment_claim_status": NO_CLAIM,
                "component_claim_status": NO_CLAIM,
                "evolution_chain_claim_status": NO_CLAIM,
                "research_boundary": RESEARCH_BOUNDARY,
                "rights_status": source_row["rights_status"],
                "risk_note": download_row["risk_note"],
                "caution": CAUTION,
                "updated_at": UPDATED_AT,
            }
        )
    return results


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-index", default=str(SOURCE_INDEX))
    parser.add_argument("--download-manifest", default=str(SOURCE_DOWNLOAD_MANIFEST))
    parser.add_argument("--download-log", default=str(SOURCE_DOWNLOAD_LOG))
    parser.add_argument("--access-profile", default=str(CORE_ACCESS_PROFILE))
    parser.add_argument("--staging", default=str(OBM_ABBREVIATION_STAGING))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = repo_root()
    rows = build_followup_review_rows(
        read_csv_rows(root / args.source_index),
        read_csv_rows(root / args.download_manifest),
        read_csv_rows(root / args.download_log),
        read_csv_rows(root / args.access_profile),
        read_csv_rows(root / args.staging),
        root,
    )
    write_csv(root / args.output, rows)
    print(f"wrote={len(rows)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
