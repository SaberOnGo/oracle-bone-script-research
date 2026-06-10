#!/usr/bin/env python3
"""Build an AI Agent context pack for HUST/OBIMD/EVOBC codepoint crosswalk rows."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


HUST_OBIMD_EVOBC_CODEPOINT_CROSSWALK = Path(
    "corpus/001_oracle-characters/000_character-registers/"
    "011_hust-obimd-evobc-codepoint-crosswalk-staging.csv"
)
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
SOURCE_INDEX = Path("corpus/006_research-sources-and-bibliography/000_source-registers/001_all-sources-index.csv")
SOURCE_DOWNLOAD_LOG = Path("project_registry/006_large-source-register/002_source-download-log.csv")
DEFAULT_OUTPUT = Path(
    "corpus/009_statistics-and-derived-features/"
    "040_ai-agent-hust-obimd-evobc-codepoint-crosswalk-context-pack.json"
)
UPDATED_AT = "2026-06-10"
CONTEXT_PACK_ID = "ai-context-hust-obimd-evobc-codepoint-crosswalk-001"
SOURCE_IDS = ["src-hust-obc", "src-obimd", "src-evobc"]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def _int_value(row: dict[str, str], key: str) -> int:
    value = row.get(key, "")
    return int(value) if value.isdigit() else 0


def _split_values(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def _counter_dict(values: list[str]) -> dict[str, int]:
    return dict(sorted(Counter(values).items()))


def _source_role(source_id: str) -> str:
    if source_id == "src-hust-obc":
        return "starting_hust_candidate_label_and_packet_route"
    if source_id == "src-obimd":
        return "codepoint_lookup_against_obimd_main_character_staging"
    if source_id == "src-evobc":
        return "codepoint_lookup_against_evobc_evolution_category_staging"
    return "source_route"


def _source_role_zh(source_id: str) -> str:
    if source_id == "src-hust-obc":
        return "HUST 候选标签和单字候选包入口"
    if source_id == "src-obimd":
        return "OBIMD main-character staging 的 codepoint 反查入口"
    if source_id == "src-evobc":
        return "EVOBC evolution category staging 的 codepoint 反查入口"
    return "来源路由"


def _source_entry(row: dict[str, str]) -> dict[str, object]:
    source_id = row["source_id"]
    route_files = {
        "src-hust-obc": [HUST_OBC_PROMOTION_QUEUE.as_posix(), SOURCE_INDEX.as_posix(), SOURCE_DOWNLOAD_LOG.as_posix()],
        "src-obimd": [OBIMD_MAIN_CHARACTER_STAGING.as_posix(), SOURCE_INDEX.as_posix(), SOURCE_DOWNLOAD_LOG.as_posix()],
        "src-evobc": [EVOBC_EVOLUTION_CATEGORY_STAGING.as_posix(), SOURCE_INDEX.as_posix(), SOURCE_DOWNLOAD_LOG.as_posix()],
    }[source_id]
    return {
        "source_id": source_id,
        "title": row["title"],
        "provider": row["provider"],
        "authority_tier": row["authority_tier"],
        "adoption_status": row["adoption_status"],
        "rights_status": row["rights_status"],
        "risk_note": row["risk_note"],
        "crosswalk_role": _source_role(source_id),
        "crosswalk_role_zh": _source_role_zh(source_id),
        "route_files": route_files,
    }


def _sample_row(row: dict[str, str]) -> dict[str, object]:
    return {
        "crosswalk_candidate_id": row["crosswalk_candidate_id"],
        "suggested_oracle_character_id": row["suggested_oracle_character_id"],
        "promotion_queue_id": row["promotion_queue_id"],
        "hust_primary_external_ref_id": row["hust_primary_external_ref_id"],
        "hust_label_codepoints": row["hust_label_codepoints"],
        "obimd_match_count": _int_value(row, "obimd_match_count"),
        "obimd_candidate_main_character_ids": _split_values(row["obimd_candidate_main_character_ids"]),
        "evobc_match_count": _int_value(row, "evobc_match_count"),
        "evobc_candidate_evolution_category_ids": _split_values(row["evobc_candidate_evolution_category_ids"]),
        "evobc_image_reference_count_total": _int_value(row, "evobc_image_reference_count_total"),
        "evobc_has_oracle_bone_refs_any": row["evobc_has_oracle_bone_refs_any"],
        "matched_source_ids": _split_values(row["matched_source_ids"]),
        "cross_source_status": row["cross_source_status"],
        "identity_claim_status": row["identity_claim_status"],
        "promotion_status": row["promotion_status"],
        "review_status": row["review_status"],
        "candidate_packet_path": row["candidate_packet_path"],
        "route_files": _split_values(row["route_files"]),
        "caution": row["caution"],
    }


def _sample_rows_by_status(rows: list[dict[str, str]]) -> dict[str, dict[str, object]]:
    samples: dict[str, dict[str, object]] = {}
    for row in rows:
        status = row["cross_source_status"]
        if status not in samples:
            samples[status] = _sample_row(row)
    return dict(sorted(samples.items()))


def _status_route(status: str, count: int) -> dict[str, object]:
    route = {
        "matched_obimd_and_evobc_by_codepoint": (
            "Open HUST packet, OBIMD main-character row, EVOBC category row, source register, and download log."
        ),
        "matched_obimd_by_codepoint": (
            "Open HUST packet, OBIMD main-character row, source register, and download log."
        ),
        "matched_evobc_by_codepoint": (
            "Open HUST packet, EVOBC category row, source register, and download log."
        ),
        "no_obimd_or_evobc_codepoint_match": (
            "Open the HUST packet and treat missing current OBIMD/EVOBC matches as a routing gap only."
        ),
    }[status]
    route_zh = {
        "matched_obimd_and_evobc_by_codepoint": "打开 HUST 候选包、OBIMD main-character 行、EVOBC category 行、来源登记和下载日志。",
        "matched_obimd_by_codepoint": "打开 HUST 候选包、OBIMD main-character 行、来源登记和下载日志。",
        "matched_evobc_by_codepoint": "打开 HUST 候选包、EVOBC category 行、来源登记和下载日志。",
        "no_obimd_or_evobc_codepoint_match": "打开 HUST 候选包；当前未命中 OBIMD/EVOBC 只能视为路由缺口。",
    }[status]
    return {
        "cross_source_status": status,
        "row_count": count,
        "recommended_route": route,
        "recommended_route_zh": route_zh,
        "claim_boundary": "lookup_route_only_no_identity_or_decipherment_claim",
    }


def build_context_pack(
    crosswalk_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
) -> dict[str, object]:
    status_counts = Counter(row["cross_source_status"] for row in crosswalk_rows)
    source_by_id = {row["source_id"]: row for row in source_rows}
    unique_route_files = sorted(
        {
            route_file
            for row in crosswalk_rows
            for route_file in _split_values(row["route_files"])
        }
    )
    rows_with_obimd = [
        row
        for row in crosswalk_rows
        if _int_value(row, "obimd_match_count") > 0
    ]
    rows_with_evobc = [
        row
        for row in crosswalk_rows
        if _int_value(row, "evobc_match_count") > 0
    ]
    rows_with_any_match = [
        row
        for row in crosswalk_rows
        if _int_value(row, "obimd_match_count") > 0 or _int_value(row, "evobc_match_count") > 0
    ]
    rows_with_both = [
        row
        for row in crosswalk_rows
        if _int_value(row, "obimd_match_count") > 0 and _int_value(row, "evobc_match_count") > 0
    ]

    return {
        "context_pack_id": CONTEXT_PACK_ID,
        "title": "HUST/OBIMD/EVOBC Codepoint Crosswalk Routing Context Pack",
        "title_zh": "HUST/OBIMD/EVOBC codepoint 交叉路由上下文包",
        "status": "reviewed_metadata_only",
        "updated_at": UPDATED_AT,
        "generated_from": [
            HUST_OBIMD_EVOBC_CODEPOINT_CROSSWALK.as_posix(),
            HUST_OBC_PROMOTION_QUEUE.as_posix(),
            OBIMD_MAIN_CHARACTER_STAGING.as_posix(),
            EVOBC_EVOLUTION_CATEGORY_STAGING.as_posix(),
            SOURCE_INDEX.as_posix(),
            SOURCE_DOWNLOAD_LOG.as_posix(),
        ],
        "purpose": (
            "Route AI Agents from HUST-OBC promotion candidates to OBIMD and EVOBC "
            "metadata rows that share the same dataset-label Unicode codepoint sequence. "
            "This pack is a lookup aid only and does not contain identity, reading, "
            "component, evolution-chain, or decipherment conclusions."
        ),
        "purpose_zh": (
            "把 AI Agent 从 HUST-OBC 提升候选路由到具有相同数据集标签 Unicode codepoint "
            "序列的 OBIMD 和 EVOBC metadata 行。本包只是反查入口，不包含身份、释读、构件、"
            "演化链或破译结论。"
        ),
        "coverage": {
            "total_crosswalk_rows": len(crosswalk_rows),
            "rows_with_any_obimd_or_evobc_codepoint_match": len(rows_with_any_match),
            "rows_with_obimd_codepoint_match": len(rows_with_obimd),
            "rows_with_evobc_codepoint_match": len(rows_with_evobc),
            "rows_with_both_obimd_and_evobc_codepoint_match": len(rows_with_both),
            "rows_without_obimd_or_evobc_codepoint_match": status_counts[
                "no_obimd_or_evobc_codepoint_match"
            ],
            "total_obimd_match_count": sum(_int_value(row, "obimd_match_count") for row in crosswalk_rows),
            "total_evobc_match_count": sum(_int_value(row, "evobc_match_count") for row in crosswalk_rows),
            "evobc_image_reference_count_total": sum(
                _int_value(row, "evobc_image_reference_count_total") for row in crosswalk_rows
            ),
            "evobc_oracle_ref_candidate_row_count": sum(
                1 for row in crosswalk_rows if row["evobc_has_oracle_bone_refs_any"] == "true"
            ),
            "multi_component_label_row_count": sum(
                1 for row in crosswalk_rows if row["has_multi_component_label"] == "true"
            ),
            "cross_source_status_counts": dict(sorted(status_counts.items())),
            "identity_claim_status_counts": _counter_dict(
                [row["identity_claim_status"] for row in crosswalk_rows]
            ),
            "promotion_status_counts": _counter_dict([row["promotion_status"] for row in crosswalk_rows]),
            "review_status_counts": _counter_dict([row["review_status"] for row in crosswalk_rows]),
            "rights_status_counts": _counter_dict([row["rights_status"] for row in crosswalk_rows]),
            "matched_source_set_counts": _counter_dict([row["matched_source_ids"] for row in crosswalk_rows]),
            "unique_route_file_count": len(unique_route_files),
            "route_file_reference_count": sum(
                len(_split_values(row["route_files"])) for row in crosswalk_rows
            ),
        },
        "source_routes": [
            _source_entry(source_by_id[source_id])
            for source_id in SOURCE_IDS
            if source_id in source_by_id
        ],
        "status_routes": [
            _status_route(status, count)
            for status, count in sorted(status_counts.items())
        ],
        "route_file_catalog": {
            "required_source_files": [
                HUST_OBIMD_EVOBC_CODEPOINT_CROSSWALK.as_posix(),
                HUST_OBC_PROMOTION_QUEUE.as_posix(),
                OBIMD_MAIN_CHARACTER_STAGING.as_posix(),
                EVOBC_EVOLUTION_CATEGORY_STAGING.as_posix(),
                SOURCE_INDEX.as_posix(),
                SOURCE_DOWNLOAD_LOG.as_posix(),
            ],
            "unique_route_file_count": len(unique_route_files),
            "unique_route_files": unique_route_files,
        },
        "sample_rows_by_status": _sample_rows_by_status(crosswalk_rows),
        "agent_use_rules": [
            "Use this pack as a codepoint lookup route, not as evidence by itself.",
            "Open the cited crosswalk row, HUST candidate packet, OBIMD/EVOBC staging rows, source register, and download log before collecting evidence.",
            "Exact Unicode codepoint matches do not confirm oracle-character identity, readings, components, evolution chains, or decipherment conclusions.",
            "Treat no OBIMD/EVOBC match as a current routing gap, not as negative evidence about character identity.",
            "Keep any follow-up downloads or OCR work in ignored temporary directories until provenance, size, checksum, rights, and risk are recorded.",
        ],
        "agent_use_rules_zh": [
            "本包只作为 codepoint 反查路由使用，不能单独当作证据。",
            "收集证据前，必须打开被引用的 crosswalk 行、HUST 候选包、OBIMD/EVOBC staging 行、来源登记和下载日志。",
            "Unicode codepoint 精确命中不等于确认甲骨字身份、释读、构件、演化链或破译结论。",
            "当前没有 OBIMD/EVOBC 命中只能视为路由缺口，不能当作身份判断的反证。",
            "后续下载或 OCR 在记录来源、大小、checksum、权利和风险前必须留在已忽略临时目录。",
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
    parser.add_argument("--crosswalk", default=str(HUST_OBIMD_EVOBC_CODEPOINT_CROSSWALK))
    parser.add_argument("--source-index", default=str(SOURCE_INDEX))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args(argv)

    root = repo_root()
    context_pack = build_context_pack(
        read_csv_rows(root / args.crosswalk),
        read_csv_rows(root / args.source_index),
    )
    write_json(root / args.output, context_pack)
    print(
        f"context_pack_id={context_pack['context_pack_id']} "
        f"rows={context_pack['coverage']['total_crosswalk_rows']} "
        f"any_match={context_pack['coverage']['rows_with_any_obimd_or_evobc_codepoint_match']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
