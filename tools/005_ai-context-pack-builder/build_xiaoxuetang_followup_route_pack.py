#!/usr/bin/env python3
"""Build a combined Xiaoxuetang follow-up route pack from existing review queues."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


QUEUE_CONFIGS = [
    {
        "family_id": "xxt_jgw_tls_access_boundary_followup",
        "family_label": "Xiaoxuetang JGW TLS/Access Boundary Follow-up",
        "family_label_zh": "小学堂甲骨文字页 TLS/访问边界后续复核",
        "queue_path": Path(
            "corpus/009_statistics-and-derived-features/"
            "072_ai-agent-hust-obc-undeciphered-candidate-xxt-jgw-followup-review-queue.csv"
        ),
        "manifest_path": Path(
            "corpus/009_statistics-and-derived-features/"
            "073_ai-agent-hust-obc-undeciphered-candidate-xxt-jgw-followup-review-log-draft-manifest.csv"
        ),
        "task_id_field": "xxt_followup_review_task_id",
        "draft_id_field": "review_log_draft_id",
        "draft_path_field": "draft_path",
        "route_source_id_field": "source_id",
        "target_source_id_field": "target_source_id",
        "primary_external_ref_field": "primary_external_ref_id",
        "artifact_kind_field": "official_route_kind",
        "target_evidence_section_field": "target_evidence_section",
        "status_field": "official_access_boundary_status",
        "staging_row_count_field": "",
    },
    {
        "family_id": "xxt_obm_access_boundary_followup",
        "family_label": "Xiaoxuetang OBM Access Boundary Follow-up",
        "family_label_zh": "小学堂《甲骨文合集材料来源表》访问边界后续复核",
        "queue_path": Path(
            "corpus/009_statistics-and-derived-features/"
            "074_ai-agent-xxt-obm-access-boundary-followup-review-queue.csv"
        ),
        "manifest_path": Path(
            "corpus/009_statistics-and-derived-features/"
            "075_ai-agent-xxt-obm-access-boundary-review-log-draft-manifest.csv"
        ),
        "task_id_field": "obm_followup_review_task_id",
        "draft_id_field": "review_log_draft_id",
        "draft_path_field": "draft_path",
        "route_source_id_field": "source_id",
        "target_source_id_field": "source_id",
        "primary_external_ref_field": "",
        "artifact_kind_field": "artifact_kind",
        "target_evidence_section_field": "",
        "status_field": "download_status",
        "staging_row_count_field": "staging_row_count",
    },
]
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "076_ai-agent-xiaoxuetang-followup-route-pack.json"
)
UPDATED_AT = "2026-06-11"
FAMILY_ORDER = [
    "xxt_jgw_tls_access_boundary_followup",
    "xxt_obm_access_boundary_followup",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def _split_compact(value: str) -> list[str]:
    return [item for item in value.split(";") if item]


def _to_int(value: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _family_index(family_id: str) -> int:
    try:
        return FAMILY_ORDER.index(family_id)
    except ValueError:
        return len(FAMILY_ORDER)


def _manifest_index(
    rows: list[dict[str, str]],
    task_id_field: str,
) -> dict[str, dict[str, str]]:
    return {row[task_id_field]: row for row in rows}


def build_route_rows(
    queue_rows_by_config: list[tuple[dict[str, object], list[dict[str, str]]]],
    manifest_rows_by_config: list[tuple[dict[str, object], list[dict[str, str]]]],
) -> list[dict[str, object]]:
    manifest_rows_lookup = {
        str(config["family_id"]): _manifest_index(rows, str(config["task_id_field"]))
        for config, rows in manifest_rows_by_config
    }

    route_rows: list[dict[str, object]] = []
    for config, queue_rows in queue_rows_by_config:
        family_id = str(config["family_id"])
        manifest_index = manifest_rows_lookup[family_id]
        task_id_field = str(config["task_id_field"])
        draft_id_field = str(config["draft_id_field"])
        draft_path_field = str(config["draft_path_field"])
        route_source_id_field = str(config["route_source_id_field"])
        target_source_id_field = str(config["target_source_id_field"])
        primary_external_ref_field = str(config["primary_external_ref_field"])
        artifact_kind_field = str(config["artifact_kind_field"])
        target_evidence_section_field = str(config["target_evidence_section_field"])
        status_field = str(config["status_field"])
        staging_row_count_field = str(config["staging_row_count_field"])

        for row in queue_rows:
            manifest_row = manifest_index[row[task_id_field]]
            route_rows.append(
                {
                    "followup_family_id": family_id,
                    "followup_family_label": str(config["family_label"]),
                    "followup_family_label_zh": str(config["family_label_zh"]),
                    "followup_task_id": row[task_id_field],
                    "review_log_draft_id": manifest_row[draft_id_field],
                    "review_log_draft_path": manifest_row[draft_path_field],
                    "source_queue_path": manifest_row["source_queue_path"],
                    "priority_rank": _to_int(row["priority_rank"]),
                    "priority_bucket": row["priority_bucket"],
                    "followup_method": row["followup_method"],
                    "route_source_id": row[route_source_id_field],
                    "target_source_id": row[target_source_id_field],
                    "unknown_candidate_id": row.get("unknown_candidate_id", ""),
                    "primary_external_ref_id": (
                        row.get(primary_external_ref_field, "")
                        if primary_external_ref_field
                        else ""
                    ),
                    "target_evidence_section": (
                        row.get(target_evidence_section_field, "")
                        if target_evidence_section_field
                        else ""
                    ),
                    "targeted_download_id": row["targeted_download_id"],
                    "targeted_url": row["targeted_url"],
                    "artifact_kind": row.get(artifact_kind_field, ""),
                    "official_access_boundary_status": row.get(status_field, ""),
                    "staging_row_count": (
                        _to_int(row.get(staging_row_count_field, "0"))
                        if staging_row_count_field
                        else 0
                    ),
                    "route_files_to_open": _split_compact(row["route_files_to_open"]),
                    "required_review_sections": _split_compact(
                        row["required_review_sections"]
                    ),
                    "required_next_checks": _split_compact(row["required_next_checks"]),
                    "route_file_count": len(_split_compact(row["route_files_to_open"])),
                    "missing_route_file_count": _to_int(row["missing_route_file_count"]),
                    "route_file_review_status": row["route_file_review_status"],
                    "evidence_collection_status": row["evidence_collection_status"],
                    "human_review_status": row["human_review_status"],
                    "formal_schema_compatibility_status": row[
                        "formal_schema_compatibility_status"
                    ],
                    "rights_decision_status": row["rights_decision_status"],
                    "source_promotion_status": row["source_promotion_status"],
                    "identity_claim_status": row["identity_claim_status"],
                    "assignment_status": row["assignment_status"],
                    "decipherment_claim_status": row["decipherment_claim_status"],
                    "component_claim_status": row["component_claim_status"],
                    "evolution_chain_claim_status": row["evolution_chain_claim_status"],
                    "research_boundary": row["research_boundary"],
                    "rights_status": row["rights_status"],
                    "risk_note": row["risk_note"],
                    "caution": row["caution"],
                    "updated_at": row["updated_at"],
                }
            )

    route_rows.sort(
        key=lambda row: (
            _family_index(str(row["followup_family_id"])),
            int(row["priority_rank"]),
            str(row["followup_task_id"]),
        )
    )
    return route_rows


def build_route_pack(
    route_rows: list[dict[str, object]],
    generated_from: list[str],
) -> dict[str, object]:
    family_counts = Counter(str(row["followup_family_id"]) for row in route_rows)
    route_source_counts = Counter(str(row["route_source_id"]) for row in route_rows)
    target_source_counts = Counter(str(row["target_source_id"]) for row in route_rows)
    method_counts = Counter(str(row["followup_method"]) for row in route_rows)
    artifact_kind_counts = Counter(str(row["artifact_kind"]) for row in route_rows)
    status_counts = Counter(
        str(row["official_access_boundary_status"]) for row in route_rows
    )
    rights_status_counts = Counter(str(row["rights_status"]) for row in route_rows)
    human_status_counts = Counter(str(row["human_review_status"]) for row in route_rows)
    evidence_status_counts = Counter(
        str(row["evidence_collection_status"]) for row in route_rows
    )
    all_route_files = sorted(
        {
            route_file
            for row in route_rows
            for route_file in row["route_files_to_open"]
        }
    )
    all_review_sections = sorted(
        {
            section
            for row in route_rows
            for section in row["required_review_sections"]
        }
    )

    family_routes = []
    for family_id in FAMILY_ORDER:
        rows = [row for row in route_rows if row["followup_family_id"] == family_id]
        if not rows:
            continue
        family_routes.append(
            {
                "followup_family_id": family_id,
                "followup_family_label": rows[0]["followup_family_label"],
                "followup_family_label_zh": rows[0]["followup_family_label_zh"],
                "review_task_count": len(rows),
                "target_source_ids": sorted({str(row["target_source_id"]) for row in rows}),
                "targeted_download_ids": [str(row["targeted_download_id"]) for row in rows],
                "review_log_draft_ids": [str(row["review_log_draft_id"]) for row in rows],
                "review_log_draft_paths": [
                    str(row["review_log_draft_path"]) for row in rows
                ],
                "route_file_count": len(
                    {
                        route_file
                        for row in rows
                        for route_file in row["route_files_to_open"]
                    }
                ),
                "required_review_sections": sorted(
                    {
                        section
                        for row in rows
                        for section in row["required_review_sections"]
                    }
                ),
                "official_access_boundary_statuses": sorted(
                    {str(row["official_access_boundary_status"]) for row in rows}
                ),
            }
        )

    target_source_routes = []
    for target_source_id in sorted(target_source_counts):
        rows = [row for row in route_rows if row["target_source_id"] == target_source_id]
        target_source_routes.append(
            {
                "target_source_id": target_source_id,
                "review_task_count": len(rows),
                "followup_family_ids": sorted(
                    {str(row["followup_family_id"]) for row in rows}
                ),
                "targeted_download_ids": [str(row["targeted_download_id"]) for row in rows],
                "review_log_draft_paths": [
                    str(row["review_log_draft_path"]) for row in rows
                ],
            }
        )

    return {
        "context_pack_id": "ai-context-xiaoxuetang-followup-route-pack-001",
        "title": "Xiaoxuetang Follow-up Route Pack",
        "title_zh": "小学堂后续复核路由包",
        "status": "draft_route_pack_not_collected",
        "updated_at": UPDATED_AT,
        "generated_from": generated_from,
        "purpose": (
            "Combine the existing Xiaoxuetang JGW and OBM follow-up review queues "
            "into one routing-only pack so later AI Agents can choose the correct "
            "manual-browser or institutional-export follow-up route before recording "
            "any catalog, collection, assignment, component, evolution-chain, or "
            "decipherment claim."
        ),
        "purpose_zh": (
            "把现有的小学堂甲骨文字页与《甲骨文合集材料来源表》后续复核队列汇总成一个"
            "只用于路由的索引包，供后续 AI Agent 在记录任何著录、馆藏、分配、构件、"
            "演化链或释读判断前先选择正确的人工浏览器或机构导出跟进路径。"
        ),
        "coverage": {
            "review_task_count": len(route_rows),
            "review_log_draft_count": len(route_rows),
            "followup_family_count": len(family_counts),
            "route_source_count": len(route_source_counts),
            "target_source_count": len(target_source_counts),
            "route_file_reference_count": sum(
                len(row["route_files_to_open"]) for row in route_rows
            ),
            "unique_route_file_count": len(all_route_files),
            "required_review_section_count": len(all_review_sections),
            "staging_row_count_total": sum(int(row["staging_row_count"]) for row in route_rows),
            "followup_family_counts": {
                family_id: family_counts.get(family_id, 0) for family_id in FAMILY_ORDER
            },
            "route_source_counts": dict(sorted(route_source_counts.items())),
            "target_source_counts": dict(sorted(target_source_counts.items())),
            "followup_method_counts": dict(sorted(method_counts.items())),
            "artifact_kind_counts": dict(sorted(artifact_kind_counts.items())),
            "official_access_boundary_status_counts": dict(sorted(status_counts.items())),
            "rights_status_counts": dict(sorted(rights_status_counts.items())),
            "human_review_status_counts": dict(sorted(human_status_counts.items())),
            "evidence_collection_status_counts": dict(
                sorted(evidence_status_counts.items())
            ),
        },
        "route_file_summary": {
            "route_files_to_open": all_route_files,
            "required_review_sections": all_review_sections,
        },
        "family_routes": family_routes,
        "target_source_routes": target_source_routes,
        "followup_routes": route_rows,
        "agent_use_rules": [
            "Use this route pack only as a routing index for existing Xiaoxuetang follow-up tasks.",
            "Open the queue row, review-log draft, and every route file before recording any evidence.",
            "Do not treat this pack as source evidence, a rights decision, a catalog match, a Heji crosswalk, a collection/object match, a formal assignment, or a decipherment conclusion.",
            "Keep any new downloads or scratch analysis in ignored temporary directories until source, size, checksum, rights, and risk are recorded.",
        ],
        "agent_use_rules_zh": [
            "本路由包只能作为现有小学堂后续复核任务的索引。",
            "记录任何证据前，必须先打开对应队列行、review-log 草稿和全部 route files。",
            "不得把本包当作来源证据、权利结论、著录匹配、合集中编号对照、馆藏/对象匹配、正式分配或释读结论。",
            "任何新增下载或临时分析在登记来源、大小、checksum、权利和风险前，必须留在已忽略临时目录。",
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
    queue_rows_by_config = [
        (config, read_csv_rows(root / Path(str(config["queue_path"]))))
        for config in QUEUE_CONFIGS
    ]
    manifest_rows_by_config = [
        (config, read_csv_rows(root / Path(str(config["manifest_path"]))))
        for config in QUEUE_CONFIGS
    ]
    route_pack = build_route_pack(
        build_route_rows(queue_rows_by_config, manifest_rows_by_config),
        generated_from=[
            str(config["queue_path"]).replace("\\", "/") for config in QUEUE_CONFIGS
        ]
        + [str(config["manifest_path"]).replace("\\", "/") for config in QUEUE_CONFIGS],
    )
    write_json(root / args.output, route_pack)
    print(
        f"context_pack_id={route_pack['context_pack_id']} "
        f"review_task_count={route_pack['coverage']['review_task_count']} "
        f"followup_family_count={route_pack['coverage']['followup_family_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
