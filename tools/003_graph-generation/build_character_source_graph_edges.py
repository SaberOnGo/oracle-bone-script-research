#!/usr/bin/env python3
"""Build candidate character-to-source provenance graph edges.

The edge records that a character candidate came from a registered source
route. It does not confirm a glyph identity, reading, or inscription link.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


CHARACTER_ROOT = Path("corpus/001_oracle-characters")
DEFAULT_OUTPUT = Path(
    "corpus/008_relationship-graph/013_character-source-graph-edges.jsonl"
)
SOURCE_REGISTER = Path(
    "corpus/006_research-sources-and-bibliography/000_source-registers/"
    "001_all-sources-index.csv"
)
DOWNLOAD_LOG = Path("project_registry/006_large-source-register/002_source-download-log.csv")
SOURCE_ID = "src-hust-obc"
EDGE_TYPE = "CHARACTER_HAS_SOURCE_CANDIDATE"
SOURCE_RISK_NOTE = (
    "Dataset is directly relevant to deciphered and undeciphered characters, "
    "but raw images are large, non-commercially licensed, and compiled from "
    "diverse sources including an unreliable GuoXueDaShi split."
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def candidate_sort_key(path: Path) -> tuple[int, str]:
    match = re.search(r"(?:obs-(?:char|unk)-)(\d+)", path.as_posix())
    return (int(match.group(1)) if match else 10**9, path.as_posix())


def candidate_id(packet: dict[str, object]) -> str:
    value = packet.get("suggested_oracle_character_id") or packet.get(
        "unknown_candidate_id"
    )
    if not isinstance(value, str) or not value:
        raise ValueError("character packet has no candidate id")
    return value


def normalized_review_status(packet: dict[str, object]) -> str:
    status = str(packet.get("review_status", ""))
    if status in {"needs_cross_source_review", "needs_review"}:
        return status
    return "needs_cross_source_review"


def build_edges(root: Path) -> list[dict[str, object]]:
    packet_paths = sorted(
        list((root / CHARACTER_ROOT).glob("**/01_candidate-character-packet.json"))
        + list((root / CHARACTER_ROOT).glob("**/01_undeciphered-candidate-packet.json")),
        key=candidate_sort_key,
    )
    if len(packet_paths) != 10996:
        raise ValueError(f"expected 10996 character packets, found {len(packet_paths)}")

    edges: list[dict[str, object]] = []
    seen_ids: set[str] = set()
    for index, packet_path in enumerate(packet_paths, start=1):
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
        project_id = candidate_id(packet)
        if project_id in seen_ids:
            raise ValueError(f"duplicate character candidate: {project_id}")
        seen_ids.add(project_id)
        source_id = str(packet.get("source_id", ""))
        if source_id != SOURCE_ID:
            raise ValueError(f"unexpected source for {project_id}: {source_id}")
        object_dir = packet_path.parent
        route_files = packet.get("route_files")
        if not isinstance(route_files, list) or not route_files:
            route_files = [
                SOURCE_REGISTER.as_posix(),
                DOWNLOAD_LOG.as_posix(),
                packet_path.relative_to(root).as_posix(),
            ]
        route_files = [str(value) for value in route_files]
        route_files.append((object_dir / "README.md").relative_to(root).as_posix())
        evidence_ids = packet.get("evidence_download_ids")
        if not isinstance(evidence_ids, list):
            evidence_ids = [str(packet.get("evidence_download_id", ""))]
        evidence_ids = [str(value) for value in evidence_ids if str(value)]
        caution = str(
            packet.get("caution")
            or "Candidate source route only; source evidence and character identity require human review."
        )
        edges.append(
            {
                "edge_id": f"edge-character-source-hust-obc-candidate-{index:05d}",
                "source_node_id": project_id,
                "edge_type": EDGE_TYPE,
                "target_node_id": SOURCE_ID,
                "confidence_level": "high",
                "source_ids": [SOURCE_ID],
                "evidence_note": (
                    "Source provenance route only. This edge records the registered "
                    "HUST-OBC candidate source and does not confirm a character "
                    "identity, reading, component, inscription, or decipherment. "
                    f"Packet caution: {caution}"
                ),
                "review_status": normalized_review_status(packet),
                "candidate_packet_path": packet_path.relative_to(root).as_posix(),
                "object_dossier_path": (
                    object_dir / "05_human-research-dossier.md"
                ).relative_to(root).as_posix(),
                "source_record_path": SOURCE_REGISTER.as_posix(),
                "route_files": sorted(set(route_files)),
                "evidence_download_ids": evidence_ids,
                "primary_external_ref_id": str(
                    packet.get("primary_external_ref_id", "")
                ),
                "rights_status": str(packet.get("rights_status", "")),
                "risk_note": str(packet.get("risk_note") or SOURCE_RISK_NOTE),
                "candidate_status": str(
                    packet.get("promotion_status")
                    or packet.get("assignment_status")
                    or "candidate"
                ),
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
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)
    root = repo_root()
    edges = build_edges(root)
    write_jsonl(root / args.output, edges)
    print(f"wrote={len(edges)} output={(root / args.output).relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
