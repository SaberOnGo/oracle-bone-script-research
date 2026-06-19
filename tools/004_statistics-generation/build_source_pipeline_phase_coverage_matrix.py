#!/usr/bin/env python3
"""Build per-source preprocessing phase coverage from source evidence tables."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


OUTPUT_CSV = Path("corpus/009_statistics-and-derived-features/136_source-pipeline-phase-coverage-matrix.csv")
SOURCE_PIPELINE_EVIDENCE_LEDGER = Path(
    "corpus/009_statistics-and-derived-features/134_ai-agent-source-pipeline-evidence-ledger.csv"
)
UPDATED_AT = "2026-06-19"
CLAIM_BOUNDARY = "source_pipeline_phase_coverage_not_review_outcome_not_scholarship"
CAUTION = (
    "Source pipeline phase coverage only; phase statuses summarize existing engineering evidence "
    "and do not decide rights, promote sources, import corpus records, or make decipherment claims."
)

PHASE_FIELDS = [
    "discovered",
    "downloaded",
    "registered",
    "unpacked",
    "extracted",
    "cleaned",
    "structured",
    "linked",
    "verified",
    "pending_human_review",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def as_int(row: dict[str, str], field: str) -> int:
    value = row.get(field, "")
    return int(value) if value.isdigit() else 0


def downloaded_status(row: dict[str, str]) -> str:
    if as_int(row, "downloaded_count") == 0:
        return "missing"
    if row.get("download_evidence_status") == "downloaded_with_access_or_checksum_review_needed":
        return "review_needed"
    return "present"


def manifest_status(row: dict[str, str]) -> str:
    if as_int(row, "package_manifest_count"):
        return "present"
    return "review_needed"


def metadata_status(row: dict[str, str]) -> str:
    if as_int(row, "metadata_profile_count"):
        return "present"
    return "review_needed"


def linked_status(row: dict[str, str]) -> str:
    if as_int(row, "candidate_queue_count") or as_int(row, "graph_edge_count") or as_int(
        row, "cross_source_crosswalk_match_count"
    ):
        return "present"
    return "missing"


def derived_status(row: dict[str, str]) -> str:
    if linked_status(row) == "present":
        return "present"
    return "review_needed"


def phase_values(row: dict[str, str]) -> dict[str, str]:
    return {
        "discovered_status": "present",
        "downloaded_status": downloaded_status(row),
        "registered_status": "present",
        "unpacked_status": manifest_status(row),
        "extracted_status": "present" if metadata_status(row) == "present" or linked_status(row) == "present" else "review_needed",
        "cleaned_status": "present" if metadata_status(row) == "present" or linked_status(row) == "present" else "review_needed",
        "structured_status": "present" if metadata_status(row) == "present" or linked_status(row) == "present" else "review_needed",
        "linked_status": linked_status(row),
        "verified_status": "pending_human_review",
        "pending_human_review_status": "present",
    }


def missing_or_review_needed_phases(phases: dict[str, str]) -> str:
    missing = []
    for phase in PHASE_FIELDS:
        status = phases[f"{phase}_status"]
        if status in {"missing", "review_needed", "pending_human_review"}:
            missing.append(phase)
    return ";".join(missing)


def build_phase_rows(root: Path) -> list[dict[str, str]]:
    ledger_rows = read_csv_rows(root / SOURCE_PIPELINE_EVIDENCE_LEDGER)
    rows: list[dict[str, str]] = []
    for index, ledger in enumerate(sorted(ledger_rows, key=lambda item: item["source_id"]), start=1):
        phases = phase_values(ledger)
        rows.append(
            {
                "phase_row_id": f"source-pipeline-phase-{index:03d}",
                "ledger_id": ledger["ledger_id"],
                "source_id": ledger["source_id"],
                "source_type": ledger["source_type"],
                "rights_status": ledger["rights_status"],
                "pipeline_gap_status": ledger["pipeline_gap_status"],
                "review_lane": ledger["review_lane"],
                **phases,
                "manifest_status": manifest_status(ledger),
                "metadata_profile_status": metadata_status(ledger),
                "derivative_status": derived_status(ledger),
                "download_manifest_count": ledger["download_manifest_count"],
                "downloaded_count": ledger["downloaded_count"],
                "checksum_present_count": ledger["checksum_present_count"],
                "package_manifest_count": ledger["package_manifest_count"],
                "metadata_profile_count": ledger["metadata_profile_count"],
                "candidate_queue_count": ledger["candidate_queue_count"],
                "cross_source_crosswalk_match_count": ledger["cross_source_crosswalk_match_count"],
                "graph_edge_count": ledger["graph_edge_count"],
                "phase_coverage_status": ledger["evidence_completeness_status"],
                "missing_or_review_needed_phases": missing_or_review_needed_phases(phases),
                "next_review_steps": ledger["required_review_steps"],
                "phase_evidence_paths": ";".join(
                    [
                        SOURCE_PIPELINE_EVIDENCE_LEDGER.as_posix(),
                        ledger["checklist_path"],
                        ledger["pipeline_audit_path"],
                        ledger["gap_matrix_path"],
                    ]
                ),
                "route_files_to_open": ledger["route_files_to_open"],
                "review_outcome_status": "not_recorded",
                "claim_boundary": CLAIM_BOUNDARY,
                "rights_decision_status": "no_new_rights_decision",
                "source_promotion_status": "not_promoted",
                "corpus_import_status": "not_imported",
                "decipherment_claim_status": "no_decipherment_claim",
                "caution": CAUTION,
                "updated_at": UPDATED_AT,
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv-output", default=str(OUTPUT_CSV))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_phase_rows(root)
    write_csv(root / args.csv_output, rows)
    print(f"source_pipeline_phase_coverage_rows={len(rows)} csv={args.csv_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
