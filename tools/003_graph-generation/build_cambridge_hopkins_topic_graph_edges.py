#!/usr/bin/env python3
"""Build graph edges for Cambridge/Hopkins topic candidate metadata."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


DEFAULT_TOPIC_INDEX = Path(
    "corpus/007_research-topics-and-grammar/000_topic-registers/"
    "001_cambridge-hopkins-topic-candidate-index.csv"
)
DEFAULT_TOPIC_CROSSWALK_LINKS = Path(
    "corpus/007_research-topics-and-grammar/000_topic-registers/"
    "002_cambridge-hopkins-topic-crosswalk-link-staging.csv"
)
DEFAULT_UNROUTED_CROSSWALK_LINKS = Path(
    "corpus/007_research-topics-and-grammar/000_topic-registers/"
    "003_cambridge-hopkins-unrouted-crosswalk-staging.csv"
)
DEFAULT_OUTPUT = Path(
    "corpus/008_relationship-graph/"
    "012_cambridge-hopkins-topic-candidate-graph-edges.jsonl"
)
SOURCE_ID = "src-cambridge-hopkins"
EVIDENCE_NOTE = (
    "Metadata edge from Cambridge/Hopkins classified-table topic candidates; "
    "not a grammar analysis result, not an accepted inscription topic assignment, "
    "not a transcription, not a reading, and not a decipherment conclusion."
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def make_edge(edge_id: str, source_node_id: str, edge_type: str, target_node_id: str) -> dict[str, object]:
    return {
        "edge_id": edge_id,
        "source_node_id": source_node_id,
        "edge_type": edge_type,
        "target_node_id": target_node_id,
        "confidence_level": "high",
        "source_ids": [SOURCE_ID],
        "evidence_note": EVIDENCE_NOTE,
        "review_status": "needs_human_topic_review",
    }


def build_edges(
    topic_rows: list[dict[str, str]],
    route_rows: list[dict[str, str]],
    unrouted_rows: list[dict[str, str]],
) -> list[dict[str, object]]:
    edges: list[dict[str, object]] = []
    for index, row in enumerate(topic_rows, start=1):
        topic_id = row["topic_candidate_id"]
        edges.extend(
            [
                make_edge(
                    f"edge-cam-hopkins-topic-source-{index:03d}",
                    topic_id,
                    "TOPIC_CANDIDATE_HAS_CAMBRIDGE_HOPKINS_SOURCE",
                    row["source_id"],
                ),
                make_edge(
                    f"edge-cam-hopkins-topic-download-{index:03d}",
                    topic_id,
                    "TOPIC_CANDIDATE_HAS_CAMBRIDGE_HOPKINS_DOWNLOAD_RECORD",
                    row["evidence_download_id"],
                ),
                make_edge(
                    f"edge-cam-hopkins-topic-group-{index:03d}",
                    topic_id,
                    "TOPIC_CANDIDATE_HAS_CAMBRIDGE_HOPKINS_CLASSIFICATION_GROUP",
                    row["primary_external_ref_id"],
                ),
            ]
        )
    for index, row in enumerate(route_rows, start=1):
        edges.append(
            make_edge(
                f"edge-cam-hopkins-topic-crosswalk-route-{index:04d}",
                row["topic_candidate_id"],
                "TOPIC_CANDIDATE_HAS_INSCRIPTION_CROSSWALK_ROUTE",
                row["inscription_crosswalk_project_id"],
            )
        )
    for index, row in enumerate(unrouted_rows, start=1):
        edges.append(
            make_edge(
                f"edge-cam-hopkins-topic-unrouted-crosswalk-{index:03d}",
                row["inscription_crosswalk_project_id"],
                "CAMBRIDGE_HOPKINS_UNROUTED_CROSSWALK_NEEDS_TOPIC_REVIEW",
                "cam-hopkins-topic-unclassified-review-bucket",
            )
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
    parser.add_argument("--topic-index", default=str(DEFAULT_TOPIC_INDEX))
    parser.add_argument("--topic-crosswalk-links", default=str(DEFAULT_TOPIC_CROSSWALK_LINKS))
    parser.add_argument("--unrouted-crosswalk-links", default=str(DEFAULT_UNROUTED_CROSSWALK_LINKS))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    edges = build_edges(
        read_csv_rows(root / args.topic_index),
        read_csv_rows(root / args.topic_crosswalk_links),
        read_csv_rows(root / args.unrouted_crosswalk_links),
    )
    write_jsonl(root / args.output, edges)
    print(f"wrote={len(edges)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
