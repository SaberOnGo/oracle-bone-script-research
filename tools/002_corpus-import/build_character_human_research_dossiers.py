#!/usr/bin/env python3
"""Build human-first research dossiers for oracle-character objects.

The generated Markdown files are object-local human research entrances.
They summarize existing packet, visual, source, and graph routes, and mark
missing research sections explicitly. They do not add readings, meanings,
component assignments, inscription identities, or decipherment conclusions.
"""

from __future__ import annotations

import argparse
import csv
import json
import textwrap
from collections import defaultdict
from pathlib import Path
from typing import Any


OBJECT_ROOT = Path("corpus/001_oracle-characters")
GRAPH_FILES = [
    Path("corpus/008_relationship-graph/005_hust-obc-candidate-graph-edges.jsonl"),
    Path("corpus/008_relationship-graph/009_character-asset-graph-edges.jsonl"),
    Path("corpus/008_relationship-graph/010_cross-source-id-graph-edges.jsonl"),
]
UPDATED_AT = "2026-06-21"
WIDTH = 78


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def project_id_from_dir(path: Path) -> str:
    for part in path.name.split("_"):
        if part.startswith("obs-char-") or part.startswith("obs-unk-"):
            return part
    raise ValueError(f"Cannot find project id in {path}")


def discover_packet_dirs(root: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for packet_path in sorted((root / OBJECT_ROOT).glob("*/*/01_*packet.json")):
        object_dir = packet_path.parent
        records.append(
            {
                "project_id": project_id_from_dir(object_dir),
                "object_dir": object_dir,
                "packet_path": packet_path,
                "packet_name": packet_path.name,
            }
        )
    return records


def graph_edges_by_source(root: Path) -> dict[str, list[dict[str, Any]]]:
    edges: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for relative in GRAPH_FILES:
        for edge in read_jsonl(root / relative):
            source = str(edge.get("source_node_id", ""))
            if source.startswith(("obs-char-", "obs-unk-")):
                copied = dict(edge)
                copied["graph_file"] = relative.as_posix()
                edges[source].append(copied)
    return edges


def wrap(text: str, width: int = WIDTH) -> list[str]:
    if not text:
        return [""]
    return textwrap.wrap(
        text,
        width=width,
        break_long_words=False,
        break_on_hyphens=False,
    ) or [""]


def para(text: str) -> str:
    return "\n".join(wrap(text))


def bullet(label: str, value: str) -> str:
    prefix = f"- {label}: "
    if len(prefix) + len(value) <= WIDTH:
        return prefix + value
    lines = textwrap.wrap(
        value,
        width=WIDTH - 2,
        initial_indent=prefix,
        subsequent_indent="  ",
        break_long_words=False,
        break_on_hyphens=False,
    )
    return "\n".join(lines)


def code_value(value: str) -> str:
    return f"`{value}`" if value else "`not_collected`"


def short_code(value: str, limit: int = 48) -> str:
    if not value:
        return "`not_collected`"
    if len(value) <= limit:
        return f"`{value}`"
    return f"`{value[: limit - 3]}...`"


def short_path(path: str) -> str:
    if not path:
        return "not_collected"
    return Path(path).name


def dataset_label(packet: dict[str, Any]) -> dict[str, str]:
    label = packet.get("dataset_label")
    if isinstance(label, dict):
        return {str(key): str(value) for key, value in label.items()}
    return {}


def visual_summary(rows: list[dict[str, str]]) -> dict[str, str]:
    return {
        "row_count": str(len(rows)),
        "image_count": str(sum(1 for row in rows if row.get("committed_image_path"))),
        "source_ref_count": str(sum(1 for row in rows if row.get("source_image_reference_path"))),
        "rights": ";".join(sorted({row.get("rights_status", "") for row in rows if row.get("rights_status")})),
        "review": ";".join(sorted({row.get("review_status", "") for row in rows if row.get("review_status")})),
    }


def edge_summary(edges: list[dict[str, Any]]) -> dict[str, Any]:
    by_type: dict[str, int] = defaultdict(int)
    codepoints: list[str] = []
    route_files: list[str] = []
    statuses: list[str] = []
    for edge in edges:
        by_type[str(edge.get("edge_type", "unknown"))] += 1
        codepoint = str(edge.get("hust_label_codepoints", ""))
        if codepoint and codepoint not in codepoints:
            codepoints.append(codepoint)
        status = str(edge.get("cross_source_status", ""))
        if status and status not in statuses:
            statuses.append(status)
        for route_file in edge.get("route_files", []) or []:
            route_file = str(route_file)
            if route_file and route_file not in route_files:
                route_files.append(route_file)
    return {
        "edge_count": len(edges),
        "edge_type_counts": dict(sorted(by_type.items())),
        "codepoints": codepoints,
        "cross_source_statuses": statuses,
        "route_files": route_files,
    }


def dossier_text(
    project_id: str,
    packet_name: str,
    packet: dict[str, Any],
    visual_rows: list[dict[str, str]],
    edges: list[dict[str, Any]],
) -> str:
    label = dataset_label(packet)
    visual = visual_summary(visual_rows)
    edge = edge_summary(edges)
    lines: list[str] = [
        f"# {project_id} Human Research Dossier",
        "",
        para(
            "This object-local dossier is the human research entrance for this "
            "oracle-character candidate. It gathers current source routes, "
            "images, graph clues, and missing research sections in one place."
        ),
        "",
        para(
            "Nothing on this page is a confirmed reading, meaning, component "
            "assignment, inscription identity, or decipherment conclusion. "
            "Unverified sections stay marked as candidate, not_collected, or "
            "needs_review."
        ),
        "",
        "## 1. Identity And Status",
        "",
        bullet("project id", code_value(project_id)),
        bullet("primary external id", code_value(str(packet.get("primary_external_ref_id", "")))),
        bullet("source id", code_value(str(packet.get("source_id", "")))),
        bullet("packet", code_value(packet_name)),
        bullet("record type", code_value(str(packet.get("record_type", "")))),
        bullet("review status", code_value(str(packet.get("review_status", "")))),
        bullet("promotion status", code_value(str(packet.get("promotion_status", "")))),
        "",
        "## 2. Glyph And Visual Evidence",
        "",
        bullet("visual gallery", code_value("04_visual-gallery.md")),
        bullet("visual source index", code_value("02_visual-source-index.csv")),
        bullet("visual index rows", code_value(visual["row_count"])),
        bullet("local review images", code_value(visual["image_count"])),
        bullet("source image refs", code_value(visual["source_ref_count"])),
        bullet("rights status", code_value(visual["rights"] or str(packet.get("rights_status", "")))),
        bullet("visual review", code_value(visual["review"] or "needs_human_visual_review")),
        "",
        "## 3. Reading, Meaning, And Dataset Label",
        "",
        bullet("accepted reading", "`not_collected`"),
        bullet("accepted meaning", "`not_collected`"),
        bullet("decipherment status", code_value(str(packet.get("decipherment_status", "")))),
        bullet("dataset label status", code_value(label.get("status", ""))),
        bullet("dataset label text", code_value(label.get("source_modern_label_candidate", ""))),
        bullet("dataset label codepoints", code_value(label.get("source_modern_label_codepoints", ""))),
        "",
        para(
            "The dataset label is a lookup clue copied from source metadata. "
            "It is not treated as an accepted modern character, reading, or "
            "meaning until cross-source and human review are complete."
        ),
        "",
        "## 4. Later-Script And Cross-Source Routes",
        "",
        bullet("graph edge count", code_value(str(edge["edge_count"]))),
        bullet("codepoint routes", code_value(";".join(edge["codepoints"]))),
        bullet("cross-source status", code_value(";".join(edge["cross_source_statuses"]))),
        bullet("OBIMD/EvoBC route status", "`candidate_route_or_not_collected`"),
        "",
        "## 5. Variants, Components, And Similar Forms",
        "",
        bullet("variant set", "`not_collected`"),
        bullet("component analysis", "`not_collected`"),
        bullet("similar-form candidates", "`not_collected`"),
        bullet("review route", "`196_shape-component-evolution...checklist.csv`"),
        "",
        "## 6. Inscription Occurrences And Text Context",
        "",
        bullet("inscription occurrence count", "`not_collected`"),
        bullet("full inscription text", "`not_collected`"),
        bullet("plate or catalog number", "`not_collected`"),
        bullet("occurrence review route", "`195_inscription-plate...checklist.csv`"),
        "",
        "## 7. Provenance, Findspot, Collection, And Period",
        "",
        bullet("source package", code_value(str(packet.get("source_package_id", "")))),
        bullet("download ids", code_value(";".join(packet.get("evidence_download_ids", [])))),
        bullet("excavation site", "`not_collected`"),
        bullet("collection or museum", "`not_collected`"),
        bullet("period or batch", "`not_collected`"),
        bullet("rights status", code_value(str(packet.get("rights_status", "")))),
        "",
        "## 8. Decipherment History And Disputes",
        "",
        bullet("published interpretation notes", "`not_collected`"),
        bullet("decipherment history", "`not_collected`"),
        bullet("known disagreement", "`not_collected`"),
        bullet("human review status", short_code(str(packet.get("required_next_review", "")))),
        "",
        "## 9. Missing Data",
        "",
        "- accepted reading and meaning",
        "- inscription occurrences and full text context",
        "- catalog, plate, and old-number crosswalks",
        "- excavation site, collection, period, and batch",
        "- variant set and similar-form comparison",
        "- component candidates and reviewer notes",
        "- published bibliography and decipherment-history notes",
        "",
        "## 10. Local Files To Open",
        "",
        "- `01_*packet.json`",
        "- `02_visual-source-index.csv`",
        "- `04_visual-gallery.md`",
        "- `06_human-review-sheet.md`",
        "- `07_research-dossier-index.json`",
        "",
        "## Boundary",
        "",
        para(
            "This dossier is a preparation-stage research entrance. It records "
            "what is available and what is missing; it does not promote any "
            "candidate into formal scholarship."
        ),
    ]
    return "\n".join(lines).rstrip() + "\n"


def review_sheet_text(project_id: str) -> str:
    lines = [
        f"# {project_id} Human Review Sheet",
        "",
        para(
            "Use this checklist before turning any candidate clue into a "
            "stronger research claim. Keep every unchecked item out of formal "
            "research notes."
        ),
        "",
        "## Required Checks",
        "",
        "- [ ] Open the local glyph gallery.",
        "- [ ] Verify source image and rights rows.",
        "- [ ] Check project ID and external IDs.",
        "- [ ] Check codepoint and later-script routes.",
        "- [ ] Search inscription occurrence and plate routes.",
        "- [ ] Search collection, findspot, period, and batch routes.",
        "- [ ] Search component, variant, and similar-form routes.",
        "- [ ] Search published research and bibliography routes.",
        "- [ ] Record every source path used.",
        "- [ ] Keep unverified readings marked as candidate.",
        "",
        "## Claim Status",
        "",
        bullet("accepted reading", "`not_reviewed`"),
        bullet("accepted meaning", "`not_reviewed`"),
        bullet("component assignment", "`not_reviewed`"),
        bullet("inscription identity", "`not_reviewed`"),
        bullet("later-script correspondence", "`not_reviewed`"),
        bullet("decipherment conclusion", "`no_claim`"),
        "",
        "## Human Notes",
        "",
        "- reviewer id: `not_recorded`",
        "- review date: `not_recorded`",
        "- notes: `not_recorded`",
    ]
    return "\n".join(lines).rstrip() + "\n"


def ai_index(
    project_id: str,
    object_dir: Path,
    packet_name: str,
    packet: dict[str, Any],
    visual_rows: list[dict[str, str]],
    edges: list[dict[str, Any]],
    root: Path,
) -> dict[str, Any]:
    return {
        "project_id": project_id,
        "updated_at": UPDATED_AT,
        "object_dir": object_dir.relative_to(root).as_posix(),
        "human_files": [
            "README.md",
            "04_visual-gallery.md",
            "05_human-research-dossier.md",
            "06_human-review-sheet.md",
        ],
        "ai_files": [
            packet_name,
            "02_visual-source-index.csv",
            "07_research-dossier-index.json",
        ],
        "packet_summary": {
            "primary_external_ref_id": packet.get("primary_external_ref_id", ""),
            "source_id": packet.get("source_id", ""),
            "record_type": packet.get("record_type", ""),
            "review_status": packet.get("review_status", ""),
            "decipherment_status": packet.get("decipherment_status", ""),
            "rights_status": packet.get("rights_status", ""),
        },
        "visual_summary": visual_summary(visual_rows),
        "graph_summary": edge_summary(edges),
        "missing_sections": [
            "accepted_reading_and_meaning",
            "inscription_occurrences",
            "catalog_plate_old_number_crosswalks",
            "excavation_collection_period_batch",
            "variant_and_similar_form_sets",
            "component_candidates",
            "published_bibliography_and_decipherment_history",
        ],
        "claim_boundary": "dossier_index_only_no_decipherment_claim",
    }


def assert_human_line_width(text: str, label: str) -> None:
    for line_number, line in enumerate(text.splitlines(), start=1):
        if len(line) > 80 and not line.startswith("!["):
            raise ValueError(f"{label}:{line_number} exceeds 80 chars: {line}")


def build_outputs(root: Path) -> dict[str, dict[str, Any]]:
    edges_by_source = graph_edges_by_source(root)
    outputs: dict[str, dict[str, Any]] = {}
    for record in discover_packet_dirs(root):
        object_dir = record["object_dir"]
        packet_name = str(record["packet_name"])
        project_id = str(record["project_id"])
        packet = read_json(record["packet_path"])
        visual_rows = read_csv_rows(object_dir / "02_visual-source-index.csv")
        edges = edges_by_source.get(project_id, [])
        dossier = dossier_text(project_id, packet_name, packet, visual_rows, edges)
        review = review_sheet_text(project_id)
        assert_human_line_width(dossier, f"{project_id} dossier")
        assert_human_line_width(review, f"{project_id} review")
        outputs[project_id] = {
            "object_dir": object_dir,
            "dossier_path": object_dir / "05_human-research-dossier.md",
            "review_sheet_path": object_dir / "06_human-review-sheet.md",
            "index_path": object_dir / "07_research-dossier-index.json",
            "dossier_text": dossier,
            "review_sheet_text": review,
            "index_data": ai_index(
                project_id,
                object_dir,
                packet_name,
                packet,
                visual_rows,
                edges,
                root,
            ),
        }
    return outputs


def write_outputs(outputs: dict[str, dict[str, Any]]) -> None:
    for output in outputs.values():
        output["dossier_path"].write_text(
            output["dossier_text"], encoding="utf-8", newline="\n"
        )
        output["review_sheet_path"].write_text(
            output["review_sheet_text"], encoding="utf-8", newline="\n"
        )
        output["index_path"].write_text(
            json.dumps(output["index_data"], ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=Path.cwd(), type=Path)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    outputs = build_outputs(root)
    if not args.check_only:
        write_outputs(outputs)
    print(f"character_human_research_dossier_count={len(outputs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
