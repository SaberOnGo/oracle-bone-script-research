#!/usr/bin/env python3
"""Build candidate character-to-inscription routes from an opened source row."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


OBJECT_ROOT = Path(
    "corpus/002_oracle-bone-inscriptions/008_source-record-candidates/"
    "001_obs-insc-src-cand-000001_obimd-h2_source-record-candidate"
)
DEFAULT_RECORD = OBJECT_ROOT / "90_source-record.json"
DEFAULT_OCCURRENCES = OBJECT_ROOT / "91_character-occurrence-index.csv"
DEFAULT_OUTPUT = Path(
    "corpus/008_relationship-graph/"
    "015_character-inscription-candidate-graph-edges.jsonl"
)
SOURCE_ID = "src-obimd"
EXPECTED_EDGE_TYPE = "CHARACTER_HAS_INSCRIPTION_SOURCE_RECORD_CANDIDATE"
EXPECTED_REVIEW_STATUS = "needs_human_inscription_review"
EXPECTED_ROUTE_STATUS = "dataset_candidate_not_promoted"
EXPECTED_RIGHTS_STATUS = "metadata_only_until_verified"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def build_edges(
    record: dict[str, object], occurrences: list[dict[str, str]]
) -> list[dict[str, object]]:
    candidate_id = str(record.get("candidate_id", ""))
    source_identifier = str(record.get("source_identifier", ""))
    source_locator = str(record.get("source_record_locator", ""))
    source_record_path = (OBJECT_ROOT / "90_source-record.json").as_posix()
    occurrence_path = (OBJECT_ROOT / "91_character-occurrence-index.csv").as_posix()
    if candidate_id != "obs-insc-src-cand-000001":
        raise ValueError(f"unexpected source-record candidate: {candidate_id}")
    if source_identifier != "H2":
        raise ValueError(f"unexpected source identifier: {source_identifier}")
    if not source_locator:
        raise ValueError("source record locator is required")
    if not occurrences:
        raise ValueError("H2 occurrence index is empty")

    edges: list[dict[str, object]] = []
    for index, occurrence in enumerate(occurrences, start=1):
        source_node_id = occurrence.get("candidate_project_id", "")
        source_uid = occurrence.get("source_uid", "")
        order_number = occurrence.get("order_number", "")
        bounding_box = occurrence.get("bounding_box_xywh", "")
        if not source_node_id.startswith("obs-comp-cand-"):
            raise ValueError(f"invalid candidate project id: {source_node_id}")
        if not source_uid or not order_number or not bounding_box:
            raise ValueError(f"incomplete H2 occurrence row: {index}")
        edges.append(
            {
                "edge_id": f"edge-character-inscription-obimd-h2-{index:03d}",
                "source_node_id": source_node_id,
                "edge_type": EXPECTED_EDGE_TYPE,
                "target_node_id": candidate_id,
                "confidence_level": "unknown",
                "source_ids": [SOURCE_ID],
                "evidence_note": (
                    "OBIMD H2 source-UID and bounding-box route only; it is not a "
                    "confirmed character identity and does not establish one. It is not an "
                    "inscription assignment, transcription, or reading; it is "
                    "not a decipherment conclusion."
                ),
                "review_status": EXPECTED_REVIEW_STATUS,
                "candidate_route_status": EXPECTED_ROUTE_STATUS,
                "identity_claim_status": "no_identity_claim",
                "rights_status": EXPECTED_RIGHTS_STATUS,
                "source_record_path": source_record_path,
                "occurrence_index_path": occurrence_path,
                "source_record_locator": source_locator,
                "source_uid": source_uid,
                "order_number": int(order_number),
                "bounding_box_xywh": [
                    int(value) for value in bounding_box.split(",")
                ],
                "missing_evidence": [
                    "readable full transcription or OCR",
                    "plate and page locator",
                    "independent catalog and object identity",
                    "source-backed character comparison",
                ],
                "next_source_checks": [
                    "open the cited rubbing and facsimile privately",
                    "locate an independent catalog or plate record",
                    "compare the boxed sign with the linked component dossier",
                ],
            }
        )
    return edges


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False, sort_keys=True))
            file.write("\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--record", default=str(DEFAULT_RECORD))
    parser.add_argument("--occurrences", default=str(DEFAULT_OCCURRENCES))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    record = json.loads((root / args.record).read_text(encoding="utf-8"))
    occurrences = read_csv_rows(root / args.occurrences)
    edges = build_edges(record, occurrences)
    write_jsonl(root / args.output, edges)
    print(f"wrote={len(edges)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
