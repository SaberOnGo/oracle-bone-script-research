#!/usr/bin/env python3
"""Build metadata-only HUST/OBIMD/EVOBC codepoint crosswalk candidates."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path


HUST_OBC_PROMOTION_QUEUE = Path(
    "corpus/001_oracle-characters/000_character-registers/"
    "009_hust-obc-obs-char-promotion-review-queue.csv"
)
OBIMD_MAIN_CHARACTER_STAGING = Path(
    "corpus/001_oracle-characters/000_character-registers/"
    "006_obimd-main-character-staging.csv"
)
EVOBC_EVOLUTION_CATEGORY_STAGING = Path(
    "corpus/004_bronze-seal-modern-correspondences/000_evolution-registers/"
    "001_evobc-evolution-category-staging.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/001_oracle-characters/000_character-registers/"
    "011_hust-obimd-evobc-codepoint-crosswalk-staging.csv"
)
SOURCE_INDEX = Path("corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv")
SOURCE_DOWNLOAD_LOG = Path("project_registry/006_large-source-register/002_source-download-log.csv")
UPDATED_AT = "2026-06-10"
MATCH_BASIS = "exact_unicode_codepoint_sequence_from_dataset_labels"
RESEARCH_BOUNDARY = "codepoint_crosswalk_candidate_metadata_only_not_identity_claim"
CAUTION = (
    "Codepoint crosswalk candidate only. Exact dataset-label codepoint matches are lookup "
    "routes, not confirmed oracle-character identity, not accepted readings, not component "
    "assignments, not evolution-chain assignments, and not decipherment conclusions."
)

OUTPUT_FIELDS = [
    "crosswalk_candidate_id",
    "suggested_oracle_character_id",
    "promotion_queue_id",
    "hust_primary_external_ref_id",
    "hust_source_category_id",
    "hust_label_candidate",
    "hust_label_codepoints",
    "label_component_count",
    "has_multi_component_label",
    "candidate_packet_path",
    "obimd_match_count",
    "obimd_candidate_main_character_ids",
    "obimd_primary_external_ref_ids",
    "obimd_source_uids",
    "obimd_transcription_values",
    "evobc_match_count",
    "evobc_candidate_evolution_category_ids",
    "evobc_primary_external_ref_ids",
    "evobc_source_category_ids",
    "evobc_image_reference_count_total",
    "evobc_has_oracle_bone_refs_any",
    "matched_source_ids",
    "match_basis",
    "cross_source_status",
    "identity_claim_status",
    "promotion_status",
    "rights_status",
    "review_status",
    "route_files",
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


def _bucket_candidate_manifest(row: dict[str, str]) -> str:
    return (
        "corpus/001_oracle-characters/"
        f"{row['suggested_bucket_directory']}/001_hust-obc-candidate-packet-manifest.csv"
    )


def _candidate_packet_path(row: dict[str, str]) -> str:
    return (
        "corpus/001_oracle-characters/"
        f"{row['suggested_bucket_directory']}/{row['suggested_character_directory']}/"
        "01_candidate-character-packet.json"
    )


def _route_files(row: dict[str, str]) -> str:
    return _compact(
        [
            HUST_OBC_PROMOTION_QUEUE.as_posix(),
            _bucket_candidate_manifest(row),
            _candidate_packet_path(row),
            OBIMD_MAIN_CHARACTER_STAGING.as_posix(),
            EVOBC_EVOLUTION_CATEGORY_STAGING.as_posix(),
            SOURCE_INDEX.as_posix(),
            SOURCE_DOWNLOAD_LOG.as_posix(),
        ]
    )


def _rows_by_codepoint(rows: list[dict[str, str]], field: str) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row.get(field, "")].append(row)
    return dict(grouped)


def _evobc_image_total(rows: list[dict[str, str]]) -> int:
    total = 0
    for row in rows:
        raw_count = row.get("image_reference_count", "")
        if raw_count.isdigit():
            total += int(raw_count)
    return total


def _matched_source_ids(obimd_rows: list[dict[str, str]], evobc_rows: list[dict[str, str]]) -> str:
    values = ["src-hust-obc"]
    if obimd_rows:
        values.append("src-obimd")
    if evobc_rows:
        values.append("src-evobc")
    return ";".join(values)


def _cross_source_status(obimd_rows: list[dict[str, str]], evobc_rows: list[dict[str, str]]) -> str:
    if obimd_rows and evobc_rows:
        return "matched_obimd_and_evobc_by_codepoint"
    if obimd_rows:
        return "matched_obimd_by_codepoint"
    if evobc_rows:
        return "matched_evobc_by_codepoint"
    return "no_obimd_or_evobc_codepoint_match"


def build_crosswalk_rows(
    hust_rows: list[dict[str, str]],
    obimd_rows: list[dict[str, str]],
    evobc_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    obimd_by_codepoint = _rows_by_codepoint(obimd_rows, "codepoint_uplus")
    evobc_by_codepoint = _rows_by_codepoint(evobc_rows, "source_character_codepoints")

    output_rows: list[dict[str, str]] = []
    for index, row in enumerate(hust_rows, start=1):
        codepoints = row["source_modern_label_codepoints"]
        obimd_matches = obimd_by_codepoint.get(codepoints, [])
        evobc_matches = evobc_by_codepoint.get(codepoints, [])
        output_rows.append(
            {
                "crosswalk_candidate_id": f"hust-obimd-evobc-xwalk-{index:06d}",
                "suggested_oracle_character_id": row["suggested_oracle_character_id"],
                "promotion_queue_id": row["promotion_queue_id"],
                "hust_primary_external_ref_id": row["primary_external_ref_id"],
                "hust_source_category_id": row["source_category_id"],
                "hust_label_candidate": row["source_modern_label_candidate"],
                "hust_label_codepoints": codepoints,
                "label_component_count": row["label_component_count"],
                "has_multi_component_label": row["has_multi_component_label"],
                "candidate_packet_path": _candidate_packet_path(row),
                "obimd_match_count": str(len(obimd_matches)),
                "obimd_candidate_main_character_ids": _compact(
                    [match["candidate_main_character_id"] for match in obimd_matches]
                ),
                "obimd_primary_external_ref_ids": _compact(
                    [match["primary_external_ref_id"] for match in obimd_matches]
                ),
                "obimd_source_uids": _compact([match["source_uid"] for match in obimd_matches]),
                "obimd_transcription_values": _compact(
                    [match["transcription_values"] for match in obimd_matches]
                ),
                "evobc_match_count": str(len(evobc_matches)),
                "evobc_candidate_evolution_category_ids": _compact(
                    [match["candidate_evolution_category_id"] for match in evobc_matches]
                ),
                "evobc_primary_external_ref_ids": _compact(
                    [f"evobc-cat-{match['source_category_id']}" for match in evobc_matches]
                ),
                "evobc_source_category_ids": _compact(
                    [match["source_category_id"] for match in evobc_matches]
                ),
                "evobc_image_reference_count_total": str(_evobc_image_total(evobc_matches)),
                "evobc_has_oracle_bone_refs_any": str(
                    any(match.get("has_oracle_bone_refs") == "true" for match in evobc_matches)
                ).lower(),
                "matched_source_ids": _matched_source_ids(obimd_matches, evobc_matches),
                "match_basis": MATCH_BASIS,
                "cross_source_status": _cross_source_status(obimd_matches, evobc_matches),
                "identity_claim_status": "no_identity_claim",
                "promotion_status": "not_promoted",
                "rights_status": "source_marked_risk_noted",
                "review_status": "needs_cross_source_review",
                "route_files": _route_files(row),
                "caution": CAUTION,
                "updated_at": UPDATED_AT,
            }
        )
    return output_rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hust-promotion-queue", default=str(HUST_OBC_PROMOTION_QUEUE))
    parser.add_argument("--obimd-main-staging", default=str(OBIMD_MAIN_CHARACTER_STAGING))
    parser.add_argument("--evobc-category-staging", default=str(EVOBC_EVOLUTION_CATEGORY_STAGING))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = build_crosswalk_rows(
        read_csv_rows(root / args.hust_promotion_queue),
        read_csv_rows(root / args.obimd_main_staging),
        read_csv_rows(root / args.evobc_category_staging),
    )
    write_csv(root / args.output, rows)
    status_counts: dict[str, int] = defaultdict(int)
    for row in rows:
        status_counts[row["cross_source_status"]] += 1
    print(
        f"wrote={len(rows)} output={(root / args.output).relative_to(root)} "
        f"status_counts={dict(sorted(status_counts.items()))}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
