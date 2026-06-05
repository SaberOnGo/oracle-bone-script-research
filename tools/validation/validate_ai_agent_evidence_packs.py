#!/usr/bin/env python3
"""Validate AI Agent evidence-pack draft JSON files."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


DEFAULT_EVIDENCE_PACK_ROOT = Path("doc/public/user_research/001_ai-agent-evidence-packs")
REQUIRED_QUEUE_PATH = (
    "corpus/009_statistics-and-derived-features/"
    "005_ai-agent-hust-obc-candidate-evidence-pack-request-queue.csv"
)

REQUIRED_TOP_LEVEL_FIELDS = {
    "evidence_pack_id",
    "evidence_request_id",
    "status",
    "research_boundary",
    "assignment_status",
    "suggested_oracle_character_id",
    "candidate_class_id",
    "primary_external_ref_id",
    "draft_source_queue_path",
    "route_pack_id",
    "bucket_manifest_path",
    "route_files",
    "source_route_requirement_ids",
    "evidence_gap_types",
    "character_or_unknown_glyph_id",
    "source_references_and_asset_metadata",
    "full_inscription_context",
    "neighboring_characters",
    "component_breakdown_and_variant_notes",
    "excavation_period_and_catalog_provenance",
    "bronze_seal_or_modern_comparanda",
    "supporting_evidence",
    "opposing_evidence",
    "open_questions_and_next_checks",
    "review_log",
    "caution",
    "updated_at",
}

EVIDENCE_SECTION_FIELDS = [
    "character_or_unknown_glyph_id",
    "source_references_and_asset_metadata",
    "full_inscription_context",
    "neighboring_characters",
    "component_breakdown_and_variant_notes",
    "excavation_period_and_catalog_provenance",
    "bronze_seal_or_modern_comparanda",
    "supporting_evidence",
    "opposing_evidence",
]

ALLOWED_PACK_STATUSES = {"draft", "hypothesis", "needs_review", "reviewed", "deprecated"}
ALLOWED_SECTION_STATUSES = {"not_collected", "partial", "complete", "not_applicable"}
ALLOWED_ASSIGNMENT_STATUSES = {
    "reserved_candidate_not_assigned",
    "candidate_promoted_after_human_review",
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _relative_posix(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def discover_pack_paths(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    if not path.exists():
        return []
    paths = sorted(path.rglob("*_evidence-pack-draft.json"))
    if paths:
        return paths
    return sorted(path.rglob("*.json"))


def _validate_review_items(data: object, field_name: str) -> list[str]:
    issues: list[str] = []
    if not isinstance(data, list):
        return [f"{field_name} must be a list"]
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            issues.append(f"{field_name}[{index}] must be an object")
            continue
        if not item.get("status"):
            issues.append(f"{field_name}[{index}] missing status")
        if not item.get("note"):
            issues.append(f"{field_name}[{index}] missing note")
    return issues


def validate_pack(data: object, path: Path | None = None, root: Path | None = None) -> list[str]:
    issues: list[str] = []
    root = root or repo_root()
    label = _relative_posix(path, root) if path else "<memory>"

    if path and _relative_posix(path, root).startswith("research/"):
        issues.append(f"{label} must not be under root research/")
    if not isinstance(data, dict):
        return issues + [f"{label} must be a JSON object"]

    missing = sorted(REQUIRED_TOP_LEVEL_FIELDS.difference(data))
    if missing:
        issues.append(f"{label} missing required fields: {', '.join(missing)}")

    evidence_pack_id = str(data.get("evidence_pack_id", ""))
    evidence_request_id = str(data.get("evidence_request_id", ""))
    if not re.fullmatch(r"hust-obc-evidence-pack-[0-9]{6}", evidence_pack_id):
        issues.append(f"{label} evidence_pack_id malformed")
    if not re.fullmatch(r"hust-obc-evidence-request-[0-9]{6}", evidence_request_id):
        issues.append(f"{label} evidence_request_id malformed")
    if evidence_pack_id and evidence_request_id:
        expected_pack_id = evidence_request_id.replace("evidence-request", "evidence-pack")
        if evidence_pack_id != expected_pack_id:
            issues.append(f"{label} evidence_pack_id does not match evidence_request_id")

    if data.get("status") not in ALLOWED_PACK_STATUSES:
        issues.append(f"{label} status outside allowed evidence-pack statuses")
    if data.get("research_boundary") != "draft_not_scholarship":
        issues.append(f"{label} research_boundary must be draft_not_scholarship")
    if data.get("assignment_status") not in ALLOWED_ASSIGNMENT_STATUSES:
        issues.append(f"{label} assignment_status outside allowed values")
    if data.get("draft_source_queue_path") != REQUIRED_QUEUE_PATH:
        issues.append(f"{label} draft_source_queue_path must point to the request queue")
    if "not a decipherment result" not in str(data.get("caution", "")):
        issues.append(f"{label} caution must state it is not a decipherment result")

    for list_field in ["route_files", "source_route_requirement_ids", "evidence_gap_types"]:
        value = data.get(list_field)
        if not isinstance(value, list) or not value:
            issues.append(f"{label} {list_field} must be a non-empty list")

    for section_name in EVIDENCE_SECTION_FIELDS:
        section = data.get(section_name)
        if not isinstance(section, dict):
            issues.append(f"{label} {section_name} must be an object")
            continue
        if section.get("status") not in ALLOWED_SECTION_STATUSES:
            issues.append(f"{label} {section_name}.status outside allowed values")
        if not isinstance(section.get("items"), list):
            issues.append(f"{label} {section_name}.items must be a list")
        if "notes" not in section:
            issues.append(f"{label} {section_name}.notes missing")

    issues.extend(_validate_review_items(data.get("open_questions_and_next_checks"), f"{label} open_questions_and_next_checks"))
    issues.extend(_validate_review_items(data.get("review_log"), f"{label} review_log"))
    return issues


def validate_path(path: Path, root: Path) -> list[str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{_relative_posix(path, root)} invalid JSON: {exc.msg}"]
    return validate_pack(data, path, root)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path",
        default=str(DEFAULT_EVIDENCE_PACK_ROOT),
        help="Evidence-pack JSON file or directory to validate.",
    )
    args = parser.parse_args(argv)

    root = repo_root()
    target = root / args.path
    paths = discover_pack_paths(target)
    if not paths:
        print(f"FAIL no evidence-pack JSON files found under {args.path}")
        return 1

    issues: list[str] = []
    for path in paths:
        issues.extend(validate_path(path, root))

    if issues:
        print("FAIL AI Agent evidence packs")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print(f"PASS AI Agent evidence packs ({len(paths)} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
