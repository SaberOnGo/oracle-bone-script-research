#!/usr/bin/env python3
"""Build a combined Xiaoxuetang capture-results route pack from JGW and OBM result tables."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


RESULT_CONFIGS = [
    {
        "family_id": "xxt_jgw_tls_access_boundary_followup",
        "family_label": "Xiaoxuetang JGW Capture Results",
        "family_label_zh": "小学堂甲骨文字页 capture results",
        "result_path": Path(
            "corpus/009_statistics-and-derived-features/"
            "082_ai-agent-xiaoxuetang-followup-jgw-capture-results.csv"
        ),
        "route_source_id": "src-hust-obc",
        "target_source_id": "src-xiaoxuetang-jiaguwen",
        "capture_result_id_field": "capture_result_id",
        "followup_task_id_field": "followup_task_id",
        "artifact_kind": "xiaoxuetang_jgw_character_detail_page",
        "route_status_fields": [
            "manual_followup_route_status",
            "catalog_availability_status",
            "heji_crosswalk_availability_status",
            "collection_match_availability_status",
            "inscription_context_availability_status",
        ],
    },
    {
        "family_id": "xxt_obm_access_boundary_followup",
        "family_label": "Xiaoxuetang OBM Capture Results",
        "family_label_zh": "小学堂《合集材料来源表》capture results",
        "result_path": Path(
            "corpus/009_statistics-and-derived-features/"
            "085_ai-agent-xxt-obm-access-boundary-capture-results.csv"
        ),
        "route_source_id": "src-xiaoxuetang-obm",
        "target_source_id": "src-xiaoxuetang-obm",
        "capture_result_id_field": "capture_result_id",
        "followup_task_id_field": "followup_task_id",
        "artifact_kind": "xxt_obm_access_boundary_capture_result",
        "route_status_fields": [
            "manual_followup_route_status",
            "access_profile_availability_status",
            "staging_availability_status",
        ],
    },
]
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "086_ai-agent-xiaoxuetang-followup-capture-route-pack.json"
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


def _family_index(family_id: str) -> int:
    try:
        return FAMILY_ORDER.index(family_id)
    except ValueError:
        return len(FAMILY_ORDER)


def build_route_rows(result_rows_by_config: list[tuple[dict[str, object], list[dict[str, str]]]]) -> list[dict[str, object]]:
    route_rows: list[dict[str, object]] = []
    for config, rows in result_rows_by_config:
        family_id = str(config["family_id"])
        for index, row in enumerate(rows, start=1):
            route_rows.append(
                {
                    "capture_result_id": row[str(config["capture_result_id_field"])],
                    "capture_route_id": f"xxt-followup-capture-route-{len(route_rows) + 1:03d}",
                    "followup_family_id": family_id,
                    "followup_family_label": str(config["family_label"]),
                    "followup_family_label_zh": str(config["family_label_zh"]),
                    "followup_task_id": row[str(config["followup_task_id_field"])],
                    "route_source_id": str(config["route_source_id"]),
                    "target_source_id": str(config["target_source_id"]),
                    "capture_priority_rank": index,
                    "targeted_download_id": row["targeted_download_id"],
                    "targeted_url": row["targeted_url"],
                    "artifact_kind": row.get("artifact_kind", str(config["artifact_kind"])),
                    "unknown_candidate_id": row.get("unknown_candidate_id", ""),
                    "primary_external_ref_id": row.get("primary_external_ref_id", ""),
                    "official_access_boundary_status": row["official_access_boundary_status"],
                    "capture_status": row["capture_status"],
                    "human_review_status": row["human_review_status"],
                    "rights_decision_status": row["rights_decision_status"],
                    "source_promotion_status": row["source_promotion_status"],
                    "identity_claim_status": row["identity_claim_status"],
                    "assignment_status": row.get("assignment_scope_status", row.get("assignment_status", "")),
                    "decipherment_claim_status": row["decipherment_claim_status"],
                    "component_claim_status": row["component_claim_status"],
                    "evolution_chain_claim_status": row["evolution_chain_claim_status"],
                    "research_boundary": row["research_boundary"],
                    "output_scope": row["output_scope"],
                    "rights_status": row["rights_status"],
                    "risk_note": row["risk_note"],
                    "caution": row["caution"],
                    "updated_at": row["updated_at"],
                    "route_files_to_open": _split_compact(row["route_files_to_open"]),
                    "required_review_sections": _split_compact(row["required_review_sections"]),
                    "required_next_checks": _split_compact(row["required_next_checks"]),
                    "route_status_snapshot": {
                        field: row[field] for field in list(config["route_status_fields"])
                    },
                }
            )

    route_rows.sort(
        key=lambda row: (
            _family_index(str(row["followup_family_id"])),
            int(row["capture_priority_rank"]),
            str(row["followup_task_id"]),
        )
    )
    for index, row in enumerate(route_rows, start=1):
        row["capture_priority_rank"] = index
    return route_rows


def build_route_pack(route_rows: list[dict[str, object]], generated_from: list[str]) -> dict[str, object]:
    family_counts = Counter(str(row["followup_family_id"]) for row in route_rows)
    route_source_counts = Counter(str(row["route_source_id"]) for row in route_rows)
    target_source_counts = Counter(str(row["target_source_id"]) for row in route_rows)
    artifact_kind_counts = Counter(str(row["artifact_kind"]) for row in route_rows)
    capture_status_counts = Counter(str(row["capture_status"]) for row in route_rows)
    human_review_status_counts = Counter(str(row["human_review_status"]) for row in route_rows)
    rights_status_counts = Counter(str(row["rights_status"]) for row in route_rows)
    access_boundary_counts = Counter(str(row["official_access_boundary_status"]) for row in route_rows)
    all_route_files = sorted({route_file for row in route_rows for route_file in row["route_files_to_open"]})
    all_review_sections = sorted({section for row in route_rows for section in row["required_review_sections"]})

    family_routes: list[dict[str, object]] = []
    for family_id in FAMILY_ORDER:
        rows = [row for row in route_rows if row["followup_family_id"] == family_id]
        if not rows:
            continue
        status_counter = Counter()
        for row in rows:
            for key, value in dict(row["route_status_snapshot"]).items():
                status_counter[f"{key}={value}"] += 1
        family_routes.append(
            {
                "followup_family_id": family_id,
                "followup_family_label": rows[0]["followup_family_label"],
                "followup_family_label_zh": rows[0]["followup_family_label_zh"],
                "capture_result_count": len(rows),
                "target_source_ids": sorted({str(row["target_source_id"]) for row in rows}),
                "targeted_download_ids": [str(row["targeted_download_id"]) for row in rows],
                "capture_result_ids": [str(row["capture_result_id"]) for row in rows],
                "route_file_count": len({route_file for row in rows for route_file in row["route_files_to_open"]}),
                "required_review_sections": sorted({section for row in rows for section in row["required_review_sections"]}),
                "official_access_boundary_statuses": sorted({str(row["official_access_boundary_status"]) for row in rows}),
                "route_status_counts": dict(sorted(status_counter.items())),
            }
        )

    target_source_routes: list[dict[str, object]] = []
    for target_source_id in sorted(target_source_counts):
        rows = [row for row in route_rows if row["target_source_id"] == target_source_id]
        target_source_routes.append(
            {
                "target_source_id": target_source_id,
                "capture_result_count": len(rows),
                "followup_family_ids": sorted({str(row["followup_family_id"]) for row in rows}),
                "targeted_download_ids": [str(row["targeted_download_id"]) for row in rows],
                "capture_result_ids": [str(row["capture_result_id"]) for row in rows],
            }
        )

    return {
        "context_pack_id": "ai-context-xiaoxuetang-followup-capture-route-pack-001",
        "title": "Xiaoxuetang Follow-up Capture Route Pack",
        "title_zh": "小学堂 follow-up capture route pack",
        "status": "draft_capture_route_pack_reviewed_metadata_only",
        "updated_at": UPDATED_AT,
        "generated_from": generated_from,
        "purpose": (
            "Combine the reviewed metadata-only Xiaoxuetang JGW and OBM capture-result rows into one routing pack so later AI Agents can open the right capture result, route files, and next checks before any new manual-browser, institutional-export, catalog, collection, assignment, or decipherment work."
        ),
        "purpose_zh": "把已完成的小学堂 JGW 与 OBM reviewed metadata-only capture results 合并成统一 route pack，供后续 AI Agent 在继续人工浏览器、机构导出、著录、馆藏、分配或释读相关工作前，先打开正确的 capture result、route files 和 next checks。",
        "coverage": {
            "capture_result_count": len(route_rows),
            "followup_family_count": len(family_counts),
            "route_source_count": len(route_source_counts),
            "target_source_count": len(target_source_counts),
            "route_file_reference_count": sum(len(row["route_files_to_open"]) for row in route_rows),
            "unique_route_file_count": len(all_route_files),
            "required_review_section_count": len(all_review_sections),
            "followup_family_counts": {family_id: family_counts.get(family_id, 0) for family_id in FAMILY_ORDER},
            "route_source_counts": dict(sorted(route_source_counts.items())),
            "target_source_counts": dict(sorted(target_source_counts.items())),
            "artifact_kind_counts": dict(sorted(artifact_kind_counts.items())),
            "capture_status_counts": dict(sorted(capture_status_counts.items())),
            "human_review_status_counts": dict(sorted(human_review_status_counts.items())),
            "rights_status_counts": dict(sorted(rights_status_counts.items())),
            "official_access_boundary_status_counts": dict(sorted(access_boundary_counts.items())),
        },
        "route_file_summary": {
            "route_files_to_open": all_route_files,
            "required_review_sections": all_review_sections,
        },
        "family_routes": family_routes,
        "target_source_routes": target_source_routes,
        "capture_routes": route_rows,
        "agent_use_rules": [
            "Use this route pack only as a routing index for existing reviewed metadata-only Xiaoxuetang capture results.",
            "Open the capture-result row and every cited route file before recording any new evidence or manual follow-up outcome.",
            "Do not treat this pack as source evidence, a rights decision, a catalog confirmation, a collection/object match, a formal assignment, or a decipherment conclusion.",
            "Keep any new downloads or scratch analysis in ignored temporary directories until source, size, checksum, rights, and risk are recorded.",
        ],
        "agent_use_rules_zh": [
            "本 route pack 只能作为现有 reviewed metadata-only 小学堂 capture results 的路由索引。",
            "记录任何新证据或人工 follow-up 结果前，必须先打开对应 capture-result 行和全部引用的 route files。",
            "不得把本包当作来源证据、权利结论、著录确认、馆藏/对象匹配、正式分配或释读结论。",
            "任何新增下载或临时分析在登记来源、大小、checksum、权利和风险前，必须留在已忽略临时目录。",
        ],
    }


def write_json(path: Path, value: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    result_rows_by_config = [
        (config, read_csv_rows(root / Path(str(config["result_path"]))))
        for config in RESULT_CONFIGS
    ]
    route_pack = build_route_pack(
        build_route_rows(result_rows_by_config),
        generated_from=[str(config["result_path"]).replace("\\", "/") for config in RESULT_CONFIGS],
    )
    write_json(root / args.output, route_pack)
    print(
        f"context_pack_id={route_pack['context_pack_id']} "
        f"capture_result_count={route_pack['coverage']['capture_result_count']} "
        f"followup_family_count={route_pack['coverage']['followup_family_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
