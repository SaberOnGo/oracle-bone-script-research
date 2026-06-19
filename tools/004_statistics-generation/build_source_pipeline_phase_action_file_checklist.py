#!/usr/bin/env python3
"""Build a source/file checklist from source pipeline action summaries."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


OUTPUT_CSV = Path("corpus/009_statistics-and-derived-features/141_source-pipeline-phase-action-file-checklist.csv")
SOURCE_PIPELINE_PHASE_ACTION_SOURCE_SUMMARY = Path(
    "corpus/009_statistics-and-derived-features/140_source-pipeline-phase-action-source-summary.csv"
)
UPDATED_AT = "2026-06-19"
REVIEW_STATUS = "pending_human_review"
RESEARCH_BOUNDARY = "source_pipeline_phase_action_file_checklist_not_scholarship"
CAUTION = (
    "This source pipeline phase action file checklist only expands route files "
    "for source review. It is not collected evidence, not a reviewed outcome, "
    "not a rights decision, not source promotion, not a corpus import, and not "
    "a decipherment conclusion."
)

FILE_ROLE_BY_SUFFIX = {
    "132_ai-agent-source-pipeline-gap-matrix.csv": "source_pipeline_gap_matrix",
    "001_all-sources-index.csv": "source_register",
    "094_source-processing-pipeline-audit.csv": "source_processing_pipeline_audit",
    "009_ai-agent-source-route-review-queue.csv": "source_route_review_queue",
    "003_source-download-manifest.csv": "source_download_manifest",
    "002_source-download-log.csv": "source_download_log",
    "007_source-field-map.csv": "source_field_map",
    "009_source-package-file-manifest.csv": "source_package_file_manifest",
    "010_downloaded-metadata-profile.csv": "downloaded_metadata_profile",
    "001_large-source-register.csv": "large_source_register",
}

OUTPUT_FIELDS = [
    "file_check_id",
    "source_summary_id",
    "source_id",
    "source_type",
    "rights_status",
    "pipeline_gap_status",
    "review_lanes",
    "phase_names",
    "route_count",
    "file_open_order",
    "file_to_open",
    "file_role",
    "path_exists",
    "source_summary_path",
    "route_ids",
    "result_scaffold_ids",
    "action_ids",
    "required_for_review",
    "review_status",
    "rights_decision_status",
    "source_promotion_status",
    "corpus_import_status",
    "decipherment_claim_status",
    "research_boundary",
    "caution",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def split_semicolon(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def file_role(path: str) -> str:
    return FILE_ROLE_BY_SUFFIX.get(Path(path).name, "source_review_file")


def build_file_checklist_rows(root: Path, source_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source in source_rows:
        files = split_semicolon(source["route_files_to_open"])
        for order, file_to_open in enumerate(files, start=1):
            rows.append(
                {
                    "file_check_id": f"source-pipeline-phase-action-file-check-{len(rows) + 1:03d}",
                    "source_summary_id": source["source_summary_id"],
                    "source_id": source["source_id"],
                    "source_type": source["source_type"],
                    "rights_status": source["rights_status"],
                    "pipeline_gap_status": source["pipeline_gap_status"],
                    "review_lanes": source["review_lanes"],
                    "phase_names": source["phase_names"],
                    "route_count": source["route_count"],
                    "file_open_order": str(order),
                    "file_to_open": file_to_open,
                    "file_role": file_role(file_to_open),
                    "path_exists": "true" if (root / file_to_open).exists() else "false",
                    "source_summary_path": SOURCE_PIPELINE_PHASE_ACTION_SOURCE_SUMMARY.as_posix(),
                    "route_ids": source["route_ids"],
                    "result_scaffold_ids": source["result_scaffold_ids"],
                    "action_ids": source["action_ids"],
                    "required_for_review": "true",
                    "review_status": REVIEW_STATUS,
                    "rights_decision_status": "no_new_rights_decision",
                    "source_promotion_status": "not_promoted",
                    "corpus_import_status": "not_imported",
                    "decipherment_claim_status": "no_decipherment_claim",
                    "research_boundary": RESEARCH_BOUNDARY,
                    "caution": CAUTION,
                    "updated_at": UPDATED_AT,
                }
            )
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-summary", default=str(SOURCE_PIPELINE_PHASE_ACTION_SOURCE_SUMMARY))
    parser.add_argument("--csv-output", default=str(OUTPUT_CSV))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_file_checklist_rows(root, read_csv_rows(root / args.source_summary))
    write_csv(root / args.csv_output, rows)
    print(f"source_pipeline_phase_action_file_checklist_rows={len(rows)} csv={args.csv_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
