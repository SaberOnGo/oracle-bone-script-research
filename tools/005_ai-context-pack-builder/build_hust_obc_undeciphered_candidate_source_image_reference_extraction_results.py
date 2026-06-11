#!/usr/bin/env python3
"""Extract HUST-OBC unknown-candidate source-image reference paths from the raw zip."""

from __future__ import annotations

import argparse
import csv
import re
import zipfile
from collections import Counter, defaultdict
from pathlib import Path


PRECHECK_RESULTS = Path(
    "corpus/009_statistics-and-derived-features/"
    "066_ai-agent-hust-obc-undeciphered-candidate-full-inscription-context-precheck-results.csv"
)
LARGE_SOURCE_REGISTER = Path("project_registry/006_large-source-register/001_large-source-register.csv")
DOWNLOAD_LOG = Path("project_registry/006_large-source-register/002_source-download-log.csv")
DEFAULT_DETAIL_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "068_ai-agent-hust-obc-undeciphered-candidate-source-image-reference-extraction-results.csv"
)
DEFAULT_SUMMARY_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "069_ai-agent-hust-obc-undeciphered-candidate-source-image-reference-extraction-summary.csv"
)
DEFAULT_LOCAL_ARCHIVE_CANDIDATES = [
    Path("external_local_archive/source_packages/hust-obc/dl-hust-obc-figshare-raw.zip"),
    Path("../52_oracle-bone-script-research-local-archive/source_packages/hust-obc/dl-hust-obc-figshare-raw.zip"),
]
UPDATED_AT = "2026-06-11"
RESEARCH_BOUNDARY = "hust_obc_undeciphered_source_image_reference_extraction_not_scholarship"
FILENAME_RE = re.compile(r"^(?P<prefix>[^_]+)_(?P<unknown>.+)_(?P<number>\d+)_(?P<variant>\d+)\.png$")
CAUTION = (
    "This row records a source-image path extracted from the registered HUST-OBC "
    "raw zip in an external local archive. It is path metadata only, not a raw "
    "image commit, not proof of primary catalog context, not a Heji crosswalk, "
    "not an old catalog number, not a collection or excavation context, not an "
    "accepted glyph identity, not a formal obs-char assignment, not a reading, "
    "not a component or evolution-chain assignment, not a rights decision, not "
    "source promotion, and not a decipherment conclusion."
)

DETAIL_FIELDS = [
    "source_image_reference_extraction_result_id",
    "full_inscription_context_precheck_result_id",
    "source_metadata_evidence_capture_result_id",
    "unknown_candidate_id",
    "primary_external_ref_id",
    "source_id",
    "source_package_id",
    "download_id",
    "source_class_id",
    "source_class_path",
    "source_image_count_expected",
    "source_image_sequence_in_candidate",
    "source_image_path",
    "source_image_filename",
    "filename_source_prefix",
    "filename_unknown_marker_token",
    "filename_catalog_candidate_number_token",
    "filename_variant_sequence_token",
    "filename_token_interpretation_status",
    "registered_storage_hint",
    "resolved_local_archive_path",
    "local_archive_resolution_status",
    "registered_file_size_bytes",
    "actual_file_size_bytes",
    "registered_checksum_sha256",
    "checksum_review_status",
    "source_rights_status",
    "large_source_rights_status",
    "risk_note",
    "evidence_collection_status",
    "catalog_context_status",
    "heji_crosswalk_status",
    "old_catalog_context_status",
    "collection_context_status",
    "excavation_context_status",
    "rights_decision_status",
    "source_promotion_status",
    "identity_claim_status",
    "assignment_status",
    "decipherment_claim_status",
    "component_claim_status",
    "evolution_chain_claim_status",
    "research_boundary",
    "required_next_checks",
    "caution",
    "updated_at",
]

SUMMARY_FIELDS = [
    "source_image_reference_extraction_summary_id",
    "full_inscription_context_precheck_result_id",
    "unknown_candidate_id",
    "primary_external_ref_id",
    "source_id",
    "source_package_id",
    "download_id",
    "source_class_id",
    "source_class_path",
    "source_image_count_expected",
    "source_image_count_extracted",
    "source_image_count_match_status",
    "first_extracted_source_image_path",
    "last_extracted_source_image_path",
    "filename_source_prefixes",
    "filename_catalog_candidate_number_tokens",
    "filename_catalog_candidate_number_token_count",
    "filename_variant_sequence_token_count",
    "filename_token_interpretation_status",
    "detail_output_path",
    "registered_storage_hint",
    "resolved_local_archive_path",
    "local_archive_resolution_status",
    "source_rights_status",
    "large_source_rights_status",
    "risk_note",
    "evidence_collection_status",
    "catalog_context_status",
    "heji_crosswalk_status",
    "old_catalog_context_status",
    "collection_context_status",
    "excavation_context_status",
    "rights_decision_status",
    "source_promotion_status",
    "identity_claim_status",
    "assignment_status",
    "decipherment_claim_status",
    "component_claim_status",
    "evolution_chain_claim_status",
    "research_boundary",
    "required_next_checks",
    "caution",
    "updated_at",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def _by_id(rows: list[dict[str, str]], field: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        key = row[field]
        if key in result:
            raise ValueError(f"duplicate {field}: {key}")
        result[key] = row
    return result


def resolve_local_archive(root: Path, explicit_path: str | None = None) -> Path:
    candidates: list[Path] = []
    if explicit_path:
        candidates.append(Path(explicit_path))
    candidates.extend(root / candidate for candidate in DEFAULT_LOCAL_ARCHIVE_CANDIDATES)
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    checked = ";".join(str(candidate) for candidate in candidates)
    raise FileNotFoundError(f"HUST-OBC raw zip not found; checked: {checked}")


def parse_filename(path: str) -> dict[str, str]:
    filename = Path(path).name
    match = FILENAME_RE.match(filename)
    if not match:
        return {
            "source_image_filename": filename,
            "filename_source_prefix": "",
            "filename_unknown_marker_token": "",
            "filename_catalog_candidate_number_token": "",
            "filename_variant_sequence_token": "",
            "filename_token_interpretation_status": "unparsed_filename_token_only_not_catalog_confirmation",
        }
    return {
        "source_image_filename": filename,
        "filename_source_prefix": match.group("prefix"),
        "filename_unknown_marker_token": match.group("unknown"),
        "filename_catalog_candidate_number_token": match.group("number"),
        "filename_variant_sequence_token": match.group("variant"),
        "filename_token_interpretation_status": "parsed_filename_token_only_not_catalog_confirmation",
    }


def _zip_names_for_prefix(zip_path: Path, prefix: str) -> list[str]:
    with zipfile.ZipFile(zip_path) as archive:
        return sorted(name for name in archive.namelist() if name.startswith(prefix) and not name.endswith("/"))


def build_extraction_rows(
    precheck_rows: list[dict[str, str]],
    large_source_rows: list[dict[str, str]],
    download_rows: list[dict[str, str]],
    *,
    root: Path,
    local_archive_path: str | None = None,
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    large_sources_by_id = _by_id(large_source_rows, "source_package_id")
    downloads_by_id = _by_id(download_rows, "download_id")
    archive_path = resolve_local_archive(root, local_archive_path)
    archive_size = archive_path.stat().st_size
    detail_rows: list[dict[str, str]] = []
    summary_rows: list[dict[str, str]] = []

    for summary_index, precheck in enumerate(precheck_rows, start=1):
        source_package_id = precheck["source_package_id"]
        download_id = precheck["download_id"]
        large_source = large_sources_by_id[source_package_id]
        download = downloads_by_id[download_id]
        names = _zip_names_for_prefix(archive_path, precheck["source_class_path"])
        expected_count = precheck["source_image_count"]
        number_tokens: list[str] = []
        variant_tokens: list[str] = []
        prefix_counter: Counter[str] = Counter()

        for sequence, name in enumerate(names, start=1):
            parsed = parse_filename(name)
            number_tokens.append(parsed["filename_catalog_candidate_number_token"])
            variant_tokens.append(parsed["filename_variant_sequence_token"])
            if parsed["filename_source_prefix"]:
                prefix_counter[parsed["filename_source_prefix"]] += 1
            detail_rows.append(
                {
                    "source_image_reference_extraction_result_id": (
                        f"hust-obc-undeciphered-source-image-ref-extraction-{len(detail_rows) + 1:04d}"
                    ),
                    "full_inscription_context_precheck_result_id": precheck[
                        "full_inscription_context_precheck_result_id"
                    ],
                    "source_metadata_evidence_capture_result_id": precheck[
                        "source_metadata_evidence_capture_result_id"
                    ],
                    "unknown_candidate_id": precheck["unknown_candidate_id"],
                    "primary_external_ref_id": precheck["primary_external_ref_id"],
                    "source_id": precheck["source_id"],
                    "source_package_id": source_package_id,
                    "download_id": download_id,
                    "source_class_id": precheck["source_class_id"],
                    "source_class_path": precheck["source_class_path"],
                    "source_image_count_expected": expected_count,
                    "source_image_sequence_in_candidate": f"{sequence:03d}",
                    "source_image_path": name,
                    **parsed,
                    "registered_storage_hint": large_source["storage_hint"],
                    "resolved_local_archive_path": archive_path.as_posix(),
                    "local_archive_resolution_status": "found_in_external_local_archive_outside_git",
                    "registered_file_size_bytes": large_source["file_size_bytes"],
                    "actual_file_size_bytes": str(archive_size),
                    "registered_checksum_sha256": large_source["checksum_sha256"],
                    "checksum_review_status": "registered_checksum_reused_not_recalculated",
                    "source_rights_status": precheck["source_rights_status"],
                    "large_source_rights_status": precheck["large_source_rights_status"],
                    "risk_note": large_source["risk_note"],
                    "evidence_collection_status": "source_image_reference_path_extracted_metadata_only",
                    "catalog_context_status": "not_collected_filename_token_only",
                    "heji_crosswalk_status": "not_collected",
                    "old_catalog_context_status": "not_collected",
                    "collection_context_status": "not_collected",
                    "excavation_context_status": "not_collected",
                    "rights_decision_status": "no_new_rights_decision",
                    "source_promotion_status": "not_promoted",
                    "identity_claim_status": "no_identity_claim",
                    "assignment_status": "unknown_candidate_id_not_formal_obs_char_assignment",
                    "decipherment_claim_status": "no_claim",
                    "component_claim_status": "no_claim",
                    "evolution_chain_claim_status": "no_claim",
                    "research_boundary": RESEARCH_BOUNDARY,
                    "required_next_checks": (
                        "open_068_detail_row;cross_check_filename_number_token_against_registered_catalog_sources;"
                        "do_not_treat_filename_token_as_catalog_or_inscription_context"
                    ),
                    "caution": CAUTION,
                    "updated_at": UPDATED_AT,
                }
            )

        unique_numbers = sorted({token for token in number_tokens if token}, key=lambda item: int(item))
        unique_variants = sorted({token for token in variant_tokens if token}, key=lambda item: int(item))
        extracted_count = len(names)
        summary_rows.append(
            {
                "source_image_reference_extraction_summary_id": (
                    f"hust-obc-undeciphered-source-image-ref-extraction-summary-{summary_index:04d}"
                ),
                "full_inscription_context_precheck_result_id": precheck[
                    "full_inscription_context_precheck_result_id"
                ],
                "unknown_candidate_id": precheck["unknown_candidate_id"],
                "primary_external_ref_id": precheck["primary_external_ref_id"],
                "source_id": precheck["source_id"],
                "source_package_id": source_package_id,
                "download_id": download_id,
                "source_class_id": precheck["source_class_id"],
                "source_class_path": precheck["source_class_path"],
                "source_image_count_expected": expected_count,
                "source_image_count_extracted": str(extracted_count),
                "source_image_count_match_status": (
                    "matches_precheck_source_image_count"
                    if str(extracted_count) == expected_count
                    else "does_not_match_precheck_source_image_count"
                ),
                "first_extracted_source_image_path": names[0] if names else "",
                "last_extracted_source_image_path": names[-1] if names else "",
                "filename_source_prefixes": ";".join(f"{key}:{value}" for key, value in sorted(prefix_counter.items())),
                "filename_catalog_candidate_number_tokens": ";".join(unique_numbers),
                "filename_catalog_candidate_number_token_count": str(len(unique_numbers)),
                "filename_variant_sequence_token_count": str(len(unique_variants)),
                "filename_token_interpretation_status": "filename_tokens_only_not_catalog_confirmation",
                "detail_output_path": DEFAULT_DETAIL_OUTPUT.as_posix(),
                "registered_storage_hint": large_source["storage_hint"],
                "resolved_local_archive_path": archive_path.as_posix(),
                "local_archive_resolution_status": "found_in_external_local_archive_outside_git",
                "source_rights_status": precheck["source_rights_status"],
                "large_source_rights_status": precheck["large_source_rights_status"],
                "risk_note": download["risk_note"],
                "evidence_collection_status": "source_image_reference_paths_extracted_metadata_only",
                "catalog_context_status": "not_collected_filename_tokens_only",
                "heji_crosswalk_status": "not_collected",
                "old_catalog_context_status": "not_collected",
                "collection_context_status": "not_collected",
                "excavation_context_status": "not_collected",
                "rights_decision_status": "no_new_rights_decision",
                "source_promotion_status": "not_promoted",
                "identity_claim_status": "no_identity_claim",
                "assignment_status": "unknown_candidate_id_not_formal_obs_char_assignment",
                "decipherment_claim_status": "no_claim",
                "component_claim_status": "no_claim",
                "evolution_chain_claim_status": "no_claim",
                "research_boundary": RESEARCH_BOUNDARY,
                "required_next_checks": (
                    "open_069_summary_row;open_068_detail_rows;search_xiaoxuetang_jiaguwen_and_obm;"
                    "verify_filename_number_tokens_before_any_catalog_or_inscription_context_claim"
                ),
                "caution": CAUTION,
                "updated_at": UPDATED_AT,
            }
        )

    return detail_rows, summary_rows


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--precheck-results", default=str(PRECHECK_RESULTS))
    parser.add_argument("--large-source-register", default=str(LARGE_SOURCE_REGISTER))
    parser.add_argument("--download-log", default=str(DOWNLOAD_LOG))
    parser.add_argument("--local-archive-path")
    parser.add_argument("--detail-output", default=str(DEFAULT_DETAIL_OUTPUT))
    parser.add_argument("--summary-output", default=str(DEFAULT_SUMMARY_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    detail_rows, summary_rows = build_extraction_rows(
        read_csv_rows(root / args.precheck_results),
        read_csv_rows(root / args.large_source_register),
        read_csv_rows(root / args.download_log),
        root=root,
        local_archive_path=args.local_archive_path,
    )
    write_csv(root / args.detail_output, detail_rows, DETAIL_FIELDS)
    write_csv(root / args.summary_output, summary_rows, SUMMARY_FIELDS)
    print(
        f"source_image_reference_detail_count={len(detail_rows)} "
        f"source_image_reference_summary_count={len(summary_rows)} "
        f"detail_output={(root / args.detail_output).relative_to(root)} "
        f"summary_output={(root / args.summary_output).relative_to(root)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
