#!/usr/bin/env python3
"""Build an AI Agent route pack from graph-source evidence note draft manifests."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


MANIFEST_PATHS = [
    Path(
        "corpus/009_statistics-and-derived-features/"
        "017_ai-agent-graph-source-evidence-collection-note-draft-manifest.csv"
    ),
    Path(
        "corpus/009_statistics-and-derived-features/"
        "018_ai-agent-graph-source-download-log-note-draft-manifest.csv"
    ),
    Path(
        "corpus/009_statistics-and-derived-features/"
        "019_ai-agent-graph-source-package-manifest-note-draft-manifest.csv"
    ),
    Path(
        "corpus/009_statistics-and-derived-features/"
        "020_ai-agent-graph-source-metadata-profile-note-draft-manifest.csv"
    ),
    Path(
        "corpus/009_statistics-and-derived-features/"
        "021_ai-agent-graph-source-graph-edges-note-draft-manifest.csv"
    ),
    Path(
        "corpus/009_statistics-and-derived-features/"
        "022_ai-agent-graph-source-staging-row-note-draft-manifest.csv"
    ),
    Path(
        "corpus/009_statistics-and-derived-features/"
        "023_ai-agent-graph-source-counter-source-lookup-note-draft-manifest.csv"
    ),
    Path(
        "corpus/009_statistics-and-derived-features/"
        "024_ai-agent-graph-source-rights-risk-review-note-draft-manifest.csv"
    ),
    Path(
        "corpus/009_statistics-and-derived-features/"
        "025_ai-agent-graph-source-review-log-note-draft-manifest.csv"
    ),
]
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "026_ai-agent-graph-source-evidence-collection-route-pack.json"
)
UPDATED_AT = "2026-06-10"
SOURCE_ORDER = ["src-hust-obc", "src-evobc", "src-obimd"]
SECTION_ORDER = [
    "source_register",
    "download_log",
    "package_manifest",
    "metadata_profile",
    "graph_edges",
    "staging_row",
    "counter_source_lookup",
    "rights_risk_review",
    "review_log",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def _task_number(task_id: str) -> int:
    try:
        return int(task_id.rsplit("-", 1)[1])
    except (IndexError, ValueError):
        return 0


def _split_compact(value: str) -> list[str]:
    return [item for item in value.split(";") if item]


def _section_index(section: str) -> int:
    try:
        return SECTION_ORDER.index(section)
    except ValueError:
        return len(SECTION_ORDER)


def _source_index(source_id: str) -> int:
    try:
        return SOURCE_ORDER.index(source_id)
    except ValueError:
        return len(SOURCE_ORDER)


def _note_route(row: dict[str, str], manifest_path: Path) -> dict[str, object]:
    route_files = _split_compact(row["route_files_to_open"])
    counter_sources = _split_compact(row["counter_source_ids_to_check"])
    return {
        "evidence_collection_note_draft_id": row["evidence_collection_note_draft_id"],
        "evidence_collection_task_id": row["evidence_collection_task_id"],
        "cross_review_result_id": row["cross_review_result_id"],
        "draft_log_id": row["draft_log_id"],
        "cross_review_log_id": row["cross_review_log_id"],
        "cross_review_task_id": row["cross_review_task_id"],
        "source_id": row["source_id"],
        "primary_review_record_id": row["primary_review_record_id"],
        "primary_external_ref_id": row["primary_external_ref_id"],
        "source_record_id": row["source_record_id"],
        "target_evidence_section": row["target_evidence_section"],
        "note_draft_path": row["note_draft_path"],
        "manifest_path": manifest_path.as_posix(),
        "task_queue_source_path": row["task_queue_source_path"],
        "route_files_to_open": route_files,
        "counter_source_ids_to_check": counter_sources,
        "route_file_count": len(route_files),
        "counter_source_count": len(counter_sources),
        "note_status": row["note_status"],
        "evidence_collection_status": row["evidence_collection_status"],
        "promotion_status": row["promotion_status"],
        "research_boundary": row["research_boundary"],
        "caution": row["caution"],
        "updated_at": row["updated_at"],
    }


def build_route_pack(manifest_rows_by_path: list[tuple[Path, list[dict[str, str]]]]) -> dict[str, object]:
    note_routes = [
        _note_route(row, manifest_path)
        for manifest_path, rows in manifest_rows_by_path
        for row in rows
    ]
    note_routes.sort(
        key=lambda row: (
            _source_index(str(row["source_id"])),
            _section_index(str(row["target_evidence_section"])),
            _task_number(str(row["evidence_collection_task_id"])),
        )
    )

    source_counts = Counter(str(row["source_id"]) for row in note_routes)
    section_counts = Counter(str(row["target_evidence_section"]) for row in note_routes)
    note_status_counts = Counter(str(row["note_status"]) for row in note_routes)
    evidence_status_counts = Counter(str(row["evidence_collection_status"]) for row in note_routes)
    promotion_status_counts = Counter(str(row["promotion_status"]) for row in note_routes)
    boundary_counts = Counter(str(row["research_boundary"]) for row in note_routes)

    source_routes = []
    for source_id in SOURCE_ORDER:
        rows = [row for row in note_routes if row["source_id"] == source_id]
        source_routes.append(
            {
                "source_id": source_id,
                "note_draft_count": len(rows),
                "target_evidence_sections": [str(row["target_evidence_section"]) for row in rows],
                "note_draft_paths": [str(row["note_draft_path"]) for row in rows],
                "route_files_to_open": sorted(
                    {
                        route_file
                        for row in rows
                        for route_file in row["route_files_to_open"]
                    }
                ),
                "counter_source_ids_to_check": sorted(
                    {
                        source
                        for row in rows
                        for source in row["counter_source_ids_to_check"]
                    }
                ),
            }
        )

    section_routes = []
    for section in SECTION_ORDER:
        rows = [row for row in note_routes if row["target_evidence_section"] == section]
        section_routes.append(
            {
                "target_evidence_section": section,
                "note_draft_count": len(rows),
                "source_ids": [str(row["source_id"]) for row in rows],
                "note_draft_paths": [str(row["note_draft_path"]) for row in rows],
                "manifest_paths": sorted({str(row["manifest_path"]) for row in rows}),
            }
        )

    return {
        "context_pack_id": "ai-context-graph-source-evidence-collection-001",
        "title": "Graph Source Evidence Collection Route Pack",
        "title_zh": "图谱来源证据收集路由包",
        "status": "draft_route_pack_not_collected",
        "updated_at": UPDATED_AT,
        "generated_from": [path.as_posix() for path, _rows in manifest_rows_by_path],
        "purpose": (
            "Route AI Agents from graph-source evidence collection note draft manifests "
            "to the exact Markdown note drafts and route files that must be opened before "
            "collecting evidence. This pack is an index only."
        ),
        "purpose_zh": (
            "把 AI Agent 从图谱来源证据收集记录草稿 manifest 路由到必须打开的 "
            "Markdown 草稿和 route files。本包只是索引。"
        ),
        "coverage": {
            "manifest_count": len(manifest_rows_by_path),
            "note_draft_count": len(note_routes),
            "source_count": len(source_counts),
            "target_evidence_section_count": len(section_counts),
            "route_file_reference_count": sum(len(row["route_files_to_open"]) for row in note_routes),
            "counter_source_reference_count": sum(
                len(row["counter_source_ids_to_check"]) for row in note_routes
            ),
            "source_counts": dict(sorted(source_counts.items())),
            "section_counts": {section: section_counts.get(section, 0) for section in SECTION_ORDER},
            "note_status_counts": dict(sorted(note_status_counts.items())),
            "evidence_collection_status_counts": dict(sorted(evidence_status_counts.items())),
            "promotion_status_counts": dict(sorted(promotion_status_counts.items())),
            "research_boundary_counts": dict(sorted(boundary_counts.items())),
        },
        "source_routes": source_routes,
        "section_routes": section_routes,
        "note_routes": note_routes,
        "agent_use_rules": [
            "Use this route pack only as an index to not-collected evidence collection note drafts.",
            "Open the note draft and all route_files_to_open before recording evidence.",
            "Do not treat this pack as collected evidence, a rights decision, a promotion decision, or a decipherment conclusion.",
            "Keep any new downloads or scratch analysis in ignored temporary directories until source, size, checksum, rights, and risk are recorded.",
            "Write collected notes under doc/public/user_research until human review promotes them into source-marked corpus records.",
        ],
        "agent_use_rules_zh": [
            "本路由包只能作为未收集证据记录草稿的索引。",
            "记录证据前，必须打开对应 note draft 和全部 route_files_to_open。",
            "不得把本包当作已收集证据、权利决定、提升决定或释读结论。",
            "新增下载或临时分析在记录来源、大小、checksum、权利和风险前必须留在已忽略临时目录。",
            "收集到的笔记在人工复核前应写入 doc/public/user_research。",
        ],
    }


def write_json(path: Path, value: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    manifest_rows_by_path = [
        (manifest_path, read_csv_rows(root / manifest_path))
        for manifest_path in MANIFEST_PATHS
    ]
    route_pack = build_route_pack(manifest_rows_by_path)
    write_json(root / args.output, route_pack)
    print(
        f"context_pack_id={route_pack['context_pack_id']} "
        f"manifest_count={route_pack['coverage']['manifest_count']} "
        f"note_draft_count={route_pack['coverage']['note_draft_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
