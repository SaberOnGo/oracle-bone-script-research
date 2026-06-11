#!/usr/bin/env python3
"""Build an AI Agent context pack for HUST-OBC undeciphered candidates."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


UNDECIPHERED_INDEX = Path(
    "corpus/001_oracle-characters/000_character-registers/"
    "003_undeciphered-oracle-characters-index.csv"
)
SOURCE_INDEX = Path("corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv")
LARGE_SOURCE_REGISTER = Path("project_registry/006_large-source-register/001_large-source-register.csv")
SOURCE_DOWNLOAD_LOG = Path("project_registry/006_large-source-register/002_source-download-log.csv")
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "050_ai-agent-hust-obc-undeciphered-candidate-context-pack.json"
)
UPDATED_AT = "2026-06-11"
CONTEXT_PACK_ID = "ai-context-hust-obc-undeciphered-candidate-001"
CAUTION = (
    "HUST-OBC undeciphered zip-directory candidate metadata only. These obs-unk rows are "
    "not formal obs-char assignments, not accepted oracle-character identities, not readings, "
    "not components, not evolution chains, and not decipherment conclusions."
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def _int(row: dict[str, str], key: str) -> int:
    value = row.get(key, "")
    return int(value) if value.isdigit() else 0


def _bucket_directory(row: dict[str, str]) -> str:
    packet_path = row["materialized_candidate_packet_path"]
    parts = packet_path.split("/")
    if len(parts) < 3:
        raise ValueError(f"cannot parse bucket directory from {packet_path}")
    return parts[2]


def _bucket_manifest_path(bucket_directory: str) -> str:
    return (
        "corpus/001_oracle-characters/"
        f"{bucket_directory}/000_hust-obc-undeciphered-candidate-bucket-manifest.csv"
    )


def _sample_row(row: dict[str, str]) -> dict[str, object]:
    return {
        "unknown_candidate_id": row["unknown_candidate_id"],
        "primary_external_ref_id": row["primary_external_ref_id"],
        "source_group": row["source_group"],
        "source_group_label": row["source_group_label"],
        "source_class_path": row["source_class_path"],
        "source_image_count": _int(row, "source_image_count"),
        "candidate_packet_path": row["materialized_candidate_packet_path"],
        "identity_claim_status": row["identity_claim_status"],
        "assignment_status": row["assignment_status"],
        "promotion_status": row["promotion_status"],
        "rights_status": row["rights_status"],
        "review_status": row["review_status"],
    }


def _group_summaries(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["source_group"]].append(row)

    order = {"L": 0, "X": 1, "Y+H": 2}
    output: list[dict[str, object]] = []
    for group, group_rows in sorted(grouped.items(), key=lambda item: order.get(item[0], 99)):
        output.append(
            {
                "source_group": group,
                "source_group_label": group_rows[0]["source_group_label"],
                "candidate_count": len(group_rows),
                "source_image_count": sum(_int(row, "source_image_count") for row in group_rows),
                "first_unknown_candidate_id": group_rows[0]["unknown_candidate_id"],
                "last_unknown_candidate_id": group_rows[-1]["unknown_candidate_id"],
                "first_primary_external_ref_id": group_rows[0]["primary_external_ref_id"],
                "last_primary_external_ref_id": group_rows[-1]["primary_external_ref_id"],
                "sample_row": _sample_row(group_rows[0]),
            }
        )
    return output


def _bucket_routes(root: Path, rows: list[dict[str, str]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[_bucket_directory(row)].append(row)

    routes: list[dict[str, object]] = []
    for index, (bucket_directory, bucket_rows) in enumerate(sorted(grouped.items()), start=1):
        manifest_path = _bucket_manifest_path(bucket_directory)
        routes.append(
            {
                "bucket_route_id": f"hust-obc-undeciphered-bucket-route-{index:03d}",
                "bucket_directory": bucket_directory,
                "bucket_manifest_path": manifest_path,
                "bucket_manifest_exists": (root / manifest_path).exists(),
                "candidate_count": len(bucket_rows),
                "source_image_count": sum(_int(row, "source_image_count") for row in bucket_rows),
                "first_unknown_candidate_id": bucket_rows[0]["unknown_candidate_id"],
                "last_unknown_candidate_id": bucket_rows[-1]["unknown_candidate_id"],
                "first_candidate_packet_path": bucket_rows[0]["materialized_candidate_packet_path"],
                "last_candidate_packet_path": bucket_rows[-1]["materialized_candidate_packet_path"],
                "review_route": "open_bucket_manifest_then_candidate_packet",
                "review_route_zh": "先打开 bucket manifest，再打开候选 packet",
            }
        )
    return routes


def _count_values(rows: list[dict[str, str]], key: str) -> dict[str, int]:
    return dict(sorted(Counter(row[key] for row in rows).items()))


def build_context_pack(root: Path, rows: list[dict[str, str]]) -> dict[str, object]:
    if not rows:
        raise ValueError("no undeciphered candidate rows")

    bucket_routes = _bucket_routes(root, rows)
    route_files = [
        UNDECIPHERED_INDEX.as_posix(),
        SOURCE_INDEX.as_posix(),
        LARGE_SOURCE_REGISTER.as_posix(),
        SOURCE_DOWNLOAD_LOG.as_posix(),
    ]

    return {
        "context_pack_id": CONTEXT_PACK_ID,
        "title": "HUST-OBC Undeciphered Candidate Routing Context Pack",
        "title_zh": "HUST-OBC 未释读候选路由上下文包",
        "status": "reviewed_metadata_only",
        "updated_at": UPDATED_AT,
        "generated_from": route_files,
        "purpose": (
            "Give AI Agents a single metadata-only entry point for the 9,408 observed "
            "HUST-OBC undeciphered candidate class directories and their 95 local bucket routes."
        ),
        "purpose_zh": (
            "为 AI Agent 提供一个 metadata-only 入口，用于定位 9,408 个已观测 HUST-OBC "
            "未释读候选 class 目录及其 95 个本地 bucket 路由。"
        ),
        "coverage": {
            "total_candidate_rows": len(rows),
            "total_bucket_routes": len(bucket_routes),
            "total_source_image_count": sum(_int(row, "source_image_count") for row in rows),
            "source_reported_undeciphered_class_count": _int(
                rows[0], "source_reported_undeciphered_class_count"
            ),
            "zip_observed_undeciphered_class_count": _int(
                rows[0], "zip_observed_undeciphered_class_count"
            ),
            "zip_observed_undeciphered_image_count": _int(
                rows[0], "zip_observed_undeciphered_image_count"
            ),
            "reported_vs_observed_class_delta": _int(
                rows[0], "source_reported_undeciphered_class_count"
            )
            - _int(rows[0], "zip_observed_undeciphered_class_count"),
            "source_group_counts": _count_values(rows, "source_group"),
            "materialization_status_counts": _count_values(rows, "materialization_status"),
            "decipherment_status_counts": _count_values(rows, "decipherment_status"),
            "identity_claim_status_counts": _count_values(rows, "identity_claim_status"),
            "assignment_status_counts": _count_values(rows, "assignment_status"),
            "promotion_status_counts": _count_values(rows, "promotion_status"),
            "rights_status_counts": _count_values(rows, "rights_status"),
            "review_status_counts": _count_values(rows, "review_status"),
            "all_bucket_manifests_exist": all(route["bucket_manifest_exists"] for route in bucket_routes),
        },
        "source_routes": [
            {
                "source_id": "src-hust-obc",
                "source_package_id": rows[0]["source_package_id"],
                "evidence_download_id": rows[0]["evidence_download_id"],
                "route_files": route_files,
                "raw_package_policy": "raw_zip_registered_not_committed_to_regular_git",
                "rights_status": rows[0]["rights_status"],
                "risk_note": rows[0]["risk_note"],
                "review_status": "reviewed_metadata_only",
            }
        ],
        "group_summaries": _group_summaries(rows),
        "bucket_routes": bucket_routes,
        "sample_rows": {
            "first": _sample_row(rows[0]),
            "last": _sample_row(rows[-1]),
        },
        "agent_use_rules": [
            "Use this context pack as a routing index for undeciphered candidate metadata, not as evidence by itself.",
            "Open the global undeciphered index, the bucket manifest, and the candidate packet before collecting evidence.",
            "Keep obs-unk IDs separate from formal obs-char IDs until cross-source review and human approval.",
            "Do not infer identity, reading, component breakdown, evolution chain, or decipherment from source class paths or image counts.",
            "Resolve the HUST-OBC reported 9,411 versus zip-observed 9,408 candidate-class discrepancy before any source promotion.",
            "Raw HUST-OBC images remain outside regular Git; commit only source-marked metadata and reviewed small derivatives.",
        ],
        "agent_use_rules_zh": [
            "本上下文包只作为未释读候选 metadata 的路由索引，不能单独当作证据。",
            "收集证据前必须打开全局未释读索引、bucket manifest 和候选 packet。",
            "跨来源复核和人工批准前，obs-unk ID 必须与正式 obs-char ID 分开。",
            "不得根据来源 class 路径或图片数量推断身份、释读、构件拆分、演化链或破译结论。",
            "HUST-OBC 论文报告 9,411 与 zip 实测 9,408 个候选 class 的差异，在任何来源提升前都要复核。",
            "HUST-OBC 原始图片保留在普通 Git 之外；只提交带来源标记的 metadata 和经复核的小型派生记录。",
        ],
        "caution": CAUTION,
    }


def write_json(path: Path, value: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--undeciphered-index", default=str(UNDECIPHERED_INDEX))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    rows = read_csv_rows(root / args.undeciphered_index)
    context_pack = build_context_pack(root, rows)
    write_json(root / args.output, context_pack)
    print(
        f"context_pack_id={context_pack['context_pack_id']} "
        f"candidate_rows={context_pack['coverage']['total_candidate_rows']} "
        f"bucket_routes={context_pack['coverage']['total_bucket_routes']} "
        f"output={args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
