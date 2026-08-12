#!/usr/bin/env python3
"""Freeze diagnostic benchmark inputs and seal ignored-local gold."""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from tools.validation.validate_ai_agent_benchmark_experiments import (  # noqa: E402
    FORBIDDEN_PUBLIC_GOLD_KEYS,
    _case_candidate_manifest_sha256,
)


DIAGNOSTIC_FIELDS = {
    "diagnostic_status": "diagnostic_only",
    "research_boundary": "benchmark_pilot_not_scholarship",
    "pretraining_exposure": "unknown",
    "benchmark_eligibility": "pretraining_exposure_unknown",
    "probability_status": "not_generated",
    "gate3_status": "not_attempted",
}
CASE_FIELDS = {
    "case_id",
    "family_id",
    "case_type",
    "split",
    "blind_alias",
    "evidence_cutoff_at",
    "files",
}
FILE_FIELDS = {
    "source_id",
    "source_ancestor_id",
    "derivative_family_id",
    "rights_status",
    "allowed_delivery_form",
    "risk_note",
    "large_source_register_ref",
    "dependency_review_status",
}
ANSWER_FIELD_NAMES = FORBIDDEN_PUBLIC_GOLD_KEYS | {
    "accepted_identity",
    "answer_label",
    "codepoint",
    "decipherment",
    "labels",
    "modern_character",
    "modern_label",
    "reading",
    "transcription",
    "unicode",
}
ANSWER_PATH_TOKENS = {
    "answer",
    "codepoint",
    "decipherment",
    "gold",
    "label",
    "modern",
    "reading",
    "transcription",
    "unicode",
}
CASE_TYPES = {
    "masked_known_reading",
    "historically_disputed",
    "null_or_negative_control",
    "hard_challenge",
}
SPLITS = {"train", "development", "calibration", "test", "challenge"}
RIGHTS_STATUSES = {
    "verified_redistributable",
    "research_use_only",
    "rights_conflict",
    "unknown",
}
DELIVERY_FORMS = {
    "full_asset",
    "citation_and_excerpt_only",
    "metadata_only",
    "withhold",
}
DEPENDENCY_STATUSES = {"reviewed", "pending", "blocked"}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
OPAQUE_CANDIDATE_RE = re.compile(
    r"^(?:candidate-[a-z0-9][a-z0-9-]*|unknown_or_other)$"
)
BLIND_ALIAS_RE = re.compile(r"^blind-[a-z0-9][a-z0-9-]*$")


class PilotError(ValueError):
    """Raised for a rejected diagnostic pilot request."""


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_object(path: Path, label: str) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PilotError(f"invalid {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise PilotError(f"{label} must be a JSON object")
    return value


def _repository_relative(path: Path, label: str) -> tuple[Path, str]:
    resolved = path.resolve()
    try:
        relative = resolved.relative_to(REPOSITORY_ROOT)
    except ValueError as exc:
        raise PilotError(f"{label} must be inside the repository") from exc
    return resolved, relative.as_posix()


def _is_git_ignored(path: Path) -> bool:
    _, relative = _repository_relative(path, "path")
    result = subprocess.run(
        ["git", "check-ignore", "-q", "--", relative],
        cwd=REPOSITORY_ROOT,
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


def _require_ignored(path: Path, label: str) -> Path:
    resolved, _ = _repository_relative(path, label)
    if not _is_git_ignored(resolved):
        raise PilotError(f"{label} path must be Git-ignored")
    return resolved


def _answer_field_routes(value: object, route: str = "$") -> list[str]:
    routes: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            item_route = f"{route}.{key}"
            if key.casefold() in ANSWER_FIELD_NAMES:
                routes.append(item_route)
            routes.extend(_answer_field_routes(item, item_route))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            routes.extend(_answer_field_routes(item, f"{route}[{index}]"))
    return routes


def _contains_answer_token(value: str) -> bool:
    tokens = {
        token
        for token in re.split(r"[^a-z0-9]+", value.casefold())
        if token
    }
    return bool(tokens & ANSWER_PATH_TOKENS)


def _validate_timestamp(value: object, label: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(
        r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z",
        value,
    ):
        raise PilotError(f"{label} must be a UTC second-precision timestamp")
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise PilotError(f"{label} is not a valid timestamp") from exc
    return value


def _require_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PilotError(f"{label} must be a non-empty string")
    return value


def _validate_case_metadata(metadata: dict[str, object]) -> None:
    forbidden_routes = _answer_field_routes(metadata)
    if forbidden_routes:
        raise PilotError(
            "answer-bearing metadata field is forbidden: " + forbidden_routes[0]
        )
    missing = CASE_FIELDS - metadata.keys()
    extra = metadata.keys() - CASE_FIELDS
    if missing or extra:
        raise PilotError(
            "case metadata fields must match the pilot contract; "
            f"missing={sorted(missing)}, extra={sorted(extra)}"
        )
    for field in ("case_id", "family_id"):
        _require_string(metadata[field], field)
    if metadata["case_type"] not in CASE_TYPES:
        raise PilotError("case_type is not allowed by schema 007")
    if metadata["split"] not in SPLITS:
        raise PilotError("split is not allowed by schema 007")
    blind_alias = metadata["blind_alias"]
    if not isinstance(blind_alias, str) or not BLIND_ALIAS_RE.fullmatch(blind_alias):
        raise PilotError("blind_alias must be an opaque blind-* identifier")
    if _contains_answer_token(blind_alias):
        raise PilotError("answer-bearing blind_alias is forbidden")
    _validate_timestamp(metadata["evidence_cutoff_at"], "evidence_cutoff_at")
    if not isinstance(metadata["files"], dict) or not metadata["files"]:
        raise PilotError("case metadata files must be a non-empty object")


def _validate_candidates(candidate_ids: list[str]) -> None:
    if len(candidate_ids) < 3 or len(candidate_ids) != len(set(candidate_ids)):
        raise PilotError("candidate IDs must contain at least three unique values")
    if "unknown_or_other" not in candidate_ids:
        raise PilotError("candidate IDs must include unknown_or_other")
    invalid = [
        item
        for item in candidate_ids
        if not OPAQUE_CANDIDATE_RE.fullmatch(item)
    ]
    if invalid:
        raise PilotError(f"candidate ID must be opaque ASCII: {invalid[0]}")
    answer_bearing = [
        item
        for item in candidate_ids
        if item != "unknown_or_other" and _contains_answer_token(item)
    ]
    if answer_bearing:
        raise PilotError(
            f"answer-bearing candidate ID is forbidden: {answer_bearing[0]}"
        )


def _validate_source_metadata(value: object, route: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise PilotError(f"source metadata at {route} must be an object")
    missing = FILE_FIELDS - value.keys()
    extra = value.keys() - FILE_FIELDS
    if missing or extra:
        raise PilotError(
            f"source metadata fields at {route} are invalid; "
            f"missing={sorted(missing)}, extra={sorted(extra)}"
        )
    for field in (
        "source_id",
        "source_ancestor_id",
        "derivative_family_id",
        "risk_note",
    ):
        _require_string(value[field], f"{route}.{field}")
    if value["rights_status"] not in RIGHTS_STATUSES:
        raise PilotError(f"{route}.rights_status is not allowed by schema 007")
    if value["allowed_delivery_form"] not in DELIVERY_FORMS:
        raise PilotError(
            f"{route}.allowed_delivery_form is not allowed by schema 007"
        )
    if value["dependency_review_status"] not in DEPENDENCY_STATUSES:
        raise PilotError(
            f"{route}.dependency_review_status is not allowed by schema 007"
        )
    large_ref = value["large_source_register_ref"]
    if large_ref is not None:
        _require_string(large_ref, f"{route}.large_source_register_ref")
    return value


def freeze_case(args: argparse.Namespace) -> Path:
    output_path = _require_ignored(Path(args.output), "output")
    object_dir, object_rel = _repository_relative(Path(args.object_dir), "object")
    if not object_dir.is_dir():
        raise PilotError("object directory does not exist")
    metadata = _load_object(Path(args.case_metadata), "case metadata")
    _validate_case_metadata(metadata)
    _validate_candidates(args.candidate_id)

    allowed_files = args.allowed_file
    if len(allowed_files) != len(set(allowed_files)):
        raise PilotError("allowed files must be unique")
    for relative_path in allowed_files:
        if _contains_answer_token(relative_path):
            raise PilotError(
                f"answer-bearing allowed path is forbidden: {relative_path}"
            )
        candidate_path = Path(relative_path)
        if candidate_path.is_absolute() or ".." in candidate_path.parts:
            raise PilotError(
                f"allowed path must stay inside the object: {relative_path}"
            )

    file_metadata = metadata["files"]
    assert isinstance(file_metadata, dict)
    if set(allowed_files) != set(file_metadata):
        raise PilotError(
            "allowed files must exactly match case metadata file routes"
        )

    snapshots: list[dict[str, object]] = []
    for relative_path in allowed_files:
        source_path = (object_dir / relative_path).resolve()
        try:
            source_path.relative_to(object_dir)
        except ValueError as exc:
            raise PilotError(
                f"allowed path escapes the object directory: {relative_path}"
            ) from exc
        if not source_path.is_file():
            raise PilotError(f"allowed file does not exist: {relative_path}")
        source = _validate_source_metadata(
            file_metadata[relative_path], f"files.{relative_path}"
        )
        snapshots.append(
            {
                "object_relative_path": Path(relative_path).as_posix(),
                "repository_path": source_path.relative_to(
                    REPOSITORY_ROOT
                ).as_posix(),
                "sha256": _sha256_file(source_path),
                "size_bytes": source_path.stat().st_size,
                **source,
            }
        )

    case = {
        key: metadata[key]
        for key in (
            "case_id",
            "family_id",
            "case_type",
            "split",
            "blind_alias",
            "evidence_cutoff_at",
        )
    }
    case["candidate_ids"] = list(args.candidate_id)
    case["candidate_universe_status"] = "includes_unknown_or_other"
    case_manifest_sha256 = _case_candidate_manifest_sha256({"cases": [case]})
    if case_manifest_sha256 is None:
        raise PilotError("schema 007 case candidate manifest could not be computed")
    frozen_binding = {
        "object_dir": object_rel,
        "case": case,
        "file_snapshots": snapshots,
    }
    output = {
        "schema_version": "0.1.0",
        "record_type": "ai_benchmark_diagnostic_frozen_case",
        **DIAGNOSTIC_FIELDS,
        **frozen_binding,
        "case_candidate_manifest_sha256": case_manifest_sha256,
        "frozen_input_sha256": hashlib.sha256(
            _canonical_bytes(frozen_binding)
        ).hexdigest(),
        "caution": (
            "Diagnostic input freeze only; not a model run, not Gate 3, "
            "not a decipherment result, and not published scholarship."
        ),
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return output_path


def _validate_private_gold(private_gold: dict[str, object]) -> None:
    required = {
        "benchmark_id",
        "benchmark_version",
        "gold_key_id",
        "case_candidate_manifest_sha256",
        "protocol_sha256",
        "labels",
        "commitment_key_hex",
    }
    missing = required - private_gold.keys()
    extra = private_gold.keys() - required
    if missing or extra:
        raise PilotError(
            "private gold fields must match schema 007 commitment binding; "
            f"missing={sorted(missing)}, extra={sorted(extra)}"
        )
    for field in ("benchmark_id", "benchmark_version", "gold_key_id"):
        _require_string(private_gold[field], field)
    for field in ("case_candidate_manifest_sha256", "protocol_sha256"):
        if not isinstance(private_gold[field], str) or not SHA256_RE.fullmatch(
            private_gold[field]
        ):
            raise PilotError(f"{field} must be a lowercase SHA-256 digest")
    labels = private_gold["labels"]
    if not isinstance(labels, list) or not labels:
        raise PilotError("private gold labels must be a non-empty list")
    case_ids: list[str] = []
    for index, label in enumerate(labels):
        if not isinstance(label, dict) or set(label) != {
            "case_id",
            "gold_candidate_id",
        }:
            raise PilotError(f"private gold label {index} has invalid fields")
        case_ids.append(_require_string(label["case_id"], f"labels[{index}].case_id"))
        candidate_id = label["gold_candidate_id"]
        if not isinstance(candidate_id, str) or not OPAQUE_CANDIDATE_RE.fullmatch(
            candidate_id
        ):
            raise PilotError(
                f"labels[{index}].gold_candidate_id must be an opaque candidate ID"
            )
    if len(case_ids) != len(set(case_ids)):
        raise PilotError("private gold labels must be unique by case")
    key_hex = private_gold["commitment_key_hex"]
    if not isinstance(key_hex, str):
        raise PilotError("commitment_key_hex must be hexadecimal")
    try:
        key = bytes.fromhex(key_hex)
    except ValueError as exc:
        raise PilotError("commitment_key_hex must be valid hexadecimal") from exc
    if len(key) < 32:
        raise PilotError("commitment_key_hex must contain at least 32 bytes")


def seal_gold(args: argparse.Namespace) -> Path:
    private_path = _require_ignored(Path(args.private_gold), "private gold")
    output_path = _require_ignored(Path(args.output), "output")
    if private_path == output_path:
        raise PilotError("private gold and public output paths must differ")
    private_gold = _load_object(private_path, "private gold")
    _validate_private_gold(private_gold)
    sealed_at = _validate_timestamp(args.sealed_at, "sealed_at")

    committed_payload = {
        key: private_gold[key]
        for key in (
            "benchmark_id",
            "benchmark_version",
            "gold_key_id",
            "case_candidate_manifest_sha256",
            "protocol_sha256",
            "labels",
        )
    }
    key = bytes.fromhex(str(private_gold["commitment_key_hex"]))
    commitment = hmac.new(
        key, _canonical_bytes(committed_payload), hashlib.sha256
    ).hexdigest()
    public = {
        "schema_version": "0.1.0",
        "record_type": "ai_benchmark_diagnostic_gold_commitment",
        **DIAGNOSTIC_FIELDS,
        "benchmark_id": private_gold["benchmark_id"],
        "benchmark_version": private_gold["benchmark_version"],
        "gold_key_id": private_gold["gold_key_id"],
        "commitment_scheme": "hmac-sha256",
        "commitment": commitment,
        "storage_class": "ignored_local_diagnostic",
        "case_candidate_manifest_sha256": private_gold[
            "case_candidate_manifest_sha256"
        ],
        "protocol_sha256": private_gold["protocol_sha256"],
        "sealed_at": sealed_at,
        "agent_access": "none",
        "unseal_status": "sealed",
        "scorer_only": True,
        "score_query_limit": 1,
        "caution": (
            "Diagnostic commitment only; no answer, probability, model result, "
            "Gate 3 authorization, decipherment, or scholarship is published."
        ),
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(public, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return output_path


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    freeze = subparsers.add_parser("freeze", help="freeze one diagnostic case")
    freeze.add_argument("--object-dir", required=True)
    freeze.add_argument("--case-metadata", required=True)
    freeze.add_argument("--allowed-file", action="append", required=True)
    freeze.add_argument("--candidate-id", action="append", required=True)
    freeze.add_argument("--output", required=True)

    seal = subparsers.add_parser("seal", help="seal ignored-local diagnostic gold")
    seal.add_argument("--private-gold", required=True)
    seal.add_argument("--sealed-at", required=True)
    seal.add_argument("--output", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        if args.command == "freeze":
            output = freeze_case(args)
            print(f"PASS diagnostic frozen case: {output}")
        else:
            output = seal_gold(args)
            print(f"PASS diagnostic gold commitment: {output}")
    except PilotError as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
