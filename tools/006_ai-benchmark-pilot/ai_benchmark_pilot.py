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
CORPUS_ROOT = REPOSITORY_ROOT / "corpus"
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
CORPUS_OBJECT_HUMAN_MARKERS = {
    "05_human-research-dossier.md",
    "05_human-review-sheet.md",
    "05_human-inscription-dossier.md",
    "06_human-collection-dossier.md",
    "06_human-inscription-dossier.md",
    "06_human-review-sheet.md",
    "06_human-source-review-sheet.md",
    "07_human-inscription-dossier.md",
    "08_character-context-evidence-dossier.md",
    "08_collection-provenance-evidence-dossier.md",
    "10_source-evidence-dossier.md",
    "14_material-visual-observation.md",
    "16_source-literature-scope-review.md",
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
OPAQUE_CANDIDATE_RE = re.compile(
    r"^(?:candidate-opaque-[a-z0-9][a-z0-9-]*|unknown_or_other)$"
)
BLIND_ALIAS_RE = re.compile(r"^blind-case-[0-9]{6}$")
PROMPT_ANSWER_PATTERNS = (
    re.compile(r"\b(?:gold_candidate_id|correct_candidate_id|ground_truth)\b", re.I),
    re.compile(r"\b(?:answer_label|accepted_identity)\b", re.I),
    re.compile(r"\bU\+[0-9A-Fa-f]{4,6}\b"),
    re.compile(r"(?:今字|现代字)\s*[:=：]"),
    re.compile(
        r"\bcandidate-opaque-[a-z0-9-]+\s*(?:=|means\b|represents\b)",
        re.I,
    ),
)
RUN_REPORT_FIELDS = {
    "run_id",
    "role",
    "execution_id",
    "agent_id",
    "model_id",
    "model_family",
    "context_id",
    "fresh_context",
    "prior_run_output_access",
    "gold_access",
    "started_at",
    "completed_at",
    "frozen_input_sha256",
    "prompt_manifest_sha256",
    "agent_output_sha256",
    "prediction",
}
RUN_OPENING_BINDING_FIELDS = (
    "run_id",
    "execution_id",
    "agent_id",
    "model_id",
    "model_family",
    "context_id",
    "role",
    "fresh_context",
    "prior_run_output_access",
    "gold_access",
    "frozen_input_sha256",
    "case_candidate_manifest_sha256",
    "prompt_manifest_sha256",
    "public_commitment_sha256",
    "gold_key_id",
    "gold_sealed_at",
    "opened_at",
)
RUN_OPENING_FIELDS = {
    "schema_version",
    "record_type",
    "diagnostic_status",
    "research_boundary",
    *RUN_OPENING_BINDING_FIELDS,
    "opening_lock_sha256",
    "caution",
}
RUN_OPENING_REPORT_FIELDS = (
    "run_id",
    "execution_id",
    "agent_id",
    "model_id",
    "model_family",
    "context_id",
    "role",
    "fresh_context",
    "prior_run_output_access",
    "gold_access",
    "frozen_input_sha256",
    "prompt_manifest_sha256",
)
PREDICTION_FIELDS = {
    "case_id",
    "ranked_candidates",
    "action",
    "selected_candidate_id",
    "abstention_reason_code",
    "supporting_evidence",
    "opposing_evidence",
    "falsification_checks",
    "leakage_assessment",
    "reasoning_summary",
}
EVIDENCE_SECTION_FIELDS = {"status", "items", "search_note"}
EVIDENCE_ITEM_FIELDS = {
    "snapshot_sha256",
    "target_candidate_id",
    "locator",
    "note",
}
FALSIFICATION_FIELDS = {
    "check_id",
    "target_candidate_id",
    "method",
    "outcome",
    "evidence_snapshot_sha256s",
    "note",
}
LEAKAGE_FIELDS = {"status", "types", "disposition", "note"}
FROZEN_SNAPSHOT_FIELDS = {
    "object_relative_path",
    "repository_path",
    "sha256",
    "size_bytes",
} | FILE_FIELDS
PUBLIC_COMMITMENT_FIELDS = {
    "schema_version",
    "record_type",
    *DIAGNOSTIC_FIELDS,
    "benchmark_id",
    "benchmark_version",
    "gold_key_id",
    "commitment_scheme",
    "commitment",
    "storage_class",
    "frozen_input_sha256",
    "case_candidate_manifest_sha256",
    "protocol_sha256",
    "sealed_at",
    "agent_access",
    "unseal_status",
    "scorer_only",
    "score_query_limit",
    "caution",
}
LOCKED_RUN_FIELDS = {
    "schema_version",
    "record_type",
    "diagnostic_status",
    "research_boundary",
    "pretraining_exposure",
    "benchmark_eligibility",
    "probability_status",
    "calibration_status",
    "delivery_status",
    "gate3_status",
    "frozen_input_sha256",
    "run_opening_sha256",
    "public_commitment_sha256",
    "prompt_manifest_sha256",
    "agent_output_sha256",
    "case_candidate_manifest_sha256",
    "locked_at",
    "prediction_lock_sha256",
    "run",
    "caution",
}


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
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_unique_json_object,
        )
    except (OSError, json.JSONDecodeError) as exc:
        raise PilotError(f"invalid {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise PilotError(f"{label} must be a JSON object")
    return value


def _write_json_exclusive(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8", newline="\n") as stream:
            json.dump(
                value,
                stream,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            stream.write("\n")
    except FileExistsError as exc:
        raise PilotError("output already exists; refusing to overwrite") from exc
    except OSError as exc:
        raise PilotError(f"output could not be created: {exc}") from exc


def _unique_json_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    value: dict[str, object] = {}
    for key, item in pairs:
        if key in value:
            raise PilotError(f"duplicate JSON key: {key}")
        value[key] = item
    return value


def _repository_relative(path: Path, label: str) -> tuple[Path, str]:
    resolved = path.resolve()
    try:
        relative = resolved.relative_to(REPOSITORY_ROOT)
    except ValueError as exc:
        raise PilotError(f"{label} must be inside the repository") from exc
    return resolved, relative.as_posix()


def _corpus_object_relative(path: Path, label: str) -> tuple[Path, str]:
    """Require an actual human-facing corpus object, not arbitrary repo files."""
    resolved, relative = _repository_relative(path, label)
    try:
        corpus_relative = resolved.relative_to(CORPUS_ROOT)
    except ValueError as exc:
        raise PilotError(
            f"{label} must be a human-facing object directory under corpus"
        ) from exc
    if len(corpus_relative.parts) < 3:
        raise PilotError(
            f"{label} must be a human-facing object directory under corpus"
        )
    if not resolved.is_dir():
        raise PilotError(f"{label} directory does not exist")
    if not any((resolved / marker).is_file() for marker in CORPUS_OBJECT_HUMAN_MARKERS):
        raise PilotError(
            f"{label} is not a registered human-facing corpus object"
        )
    return resolved, relative


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


def _require_exact_fields(
    value: dict[str, object],
    expected: set[str],
    label: str,
) -> None:
    missing = expected - value.keys()
    extra = value.keys() - expected
    if missing or extra:
        raise PilotError(
            f"{label} fields are invalid; "
            f"missing={sorted(missing)}, extra={sorted(extra)}"
        )


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
    if isinstance(blind_alias, str) and _contains_answer_token(blind_alias):
        raise PilotError("answer-bearing blind_alias is forbidden")
    if not isinstance(blind_alias, str) or not BLIND_ALIAS_RE.fullmatch(blind_alias):
        raise PilotError("blind_alias must be an opaque blind-case-NNNNNN identifier")
    _validate_timestamp(metadata["evidence_cutoff_at"], "evidence_cutoff_at")
    if not isinstance(metadata["files"], dict) or not metadata["files"]:
        raise PilotError("case metadata files must be a non-empty object")


def _validate_candidates(candidate_ids: list[str]) -> None:
    if len(candidate_ids) < 3 or len(candidate_ids) != len(set(candidate_ids)):
        raise PilotError("candidate IDs must contain at least three unique values")
    if "unknown_or_other" not in candidate_ids:
        raise PilotError("candidate IDs must include unknown_or_other")
    answer_bearing = [
        item
        for item in candidate_ids
        if item != "unknown_or_other" and _contains_answer_token(item)
    ]
    if answer_bearing:
        raise PilotError(
            f"answer-bearing candidate ID is forbidden: {answer_bearing[0]}"
        )
    invalid = [
        item
        for item in candidate_ids
        if not OPAQUE_CANDIDATE_RE.fullmatch(item)
    ]
    if invalid:
        raise PilotError(f"candidate ID must be opaque ASCII: {invalid[0]}")


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
    object_dir, object_rel = _corpus_object_relative(
        Path(args.object_dir), "object"
    )
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
    snapshot_hashes: set[str] = set()
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
        if output_path == source_path:
            raise PilotError("output must not overwrite input evidence")
        source = _validate_source_metadata(
            file_metadata[relative_path], f"files.{relative_path}"
        )
        digest = _sha256_file(source_path)
        if digest in snapshot_hashes:
            raise PilotError(
                "frozen snapshot hashes must be unique to keep evidence "
                "references unambiguous"
            )
        snapshot_hashes.add(digest)
        snapshots.append(
            {
                "object_relative_path": Path(relative_path).as_posix(),
                "repository_path": source_path.relative_to(
                    REPOSITORY_ROOT
                ).as_posix(),
                "sha256": digest,
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
    _write_json_exclusive(output_path, output)
    return output_path


def _validate_private_gold(
    private_gold: dict[str, object],
    frozen: dict[str, object],
) -> None:
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
    if private_gold["case_candidate_manifest_sha256"] != frozen.get(
        "case_candidate_manifest_sha256"
    ):
        raise PilotError(
            "private gold does not bind the frozen candidate manifest"
        )
    case = frozen.get("case")
    if not isinstance(case, dict):
        raise PilotError("frozen case is missing its case record")
    frozen_case_id = case.get("case_id")
    if set(case_ids) != {frozen_case_id}:
        raise PilotError(
            "private gold label cases must exactly match frozen cases"
        )
    frozen_candidates = case.get("candidate_ids")
    if not isinstance(frozen_candidates, list):
        raise PilotError("frozen candidate universe is invalid")
    for index, label in enumerate(labels):
        assert isinstance(label, dict)
        if label["gold_candidate_id"] not in frozen_candidates:
            raise PilotError(
                f"labels[{index}].gold_candidate_id is outside the "
                "frozen candidate universe"
            )
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
    frozen_path = _require_ignored(Path(args.frozen_case), "frozen case")
    if output_path in {private_path, frozen_path}:
        raise PilotError("seal output must differ from its inputs")
    frozen = _load_object(frozen_path, "frozen case")
    case, _ = _validate_frozen_case(frozen)
    private_gold = _load_object(private_path, "private gold")
    _validate_private_gold(private_gold, frozen)
    sealed_at = _validate_timestamp(args.sealed_at, "sealed_at")
    evidence_cutoff = _validate_timestamp(
        case.get("evidence_cutoff_at"),
        "evidence_cutoff_at",
    )
    if sealed_at < evidence_cutoff:
        raise PilotError("gold cannot be sealed before the evidence cutoff")

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
    committed_payload["frozen_input_sha256"] = frozen[
        "frozen_input_sha256"
    ]
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
        "frozen_input_sha256": frozen["frozen_input_sha256"],
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
    _write_json_exclusive(output_path, public)
    return output_path


def open_run(args: argparse.Namespace) -> Path:
    frozen_path = _require_ignored(Path(args.frozen_case), "frozen case")
    commitment_path = _require_ignored(
        Path(args.public_commitment), "public commitment"
    )
    prompt_path = _require_ignored(Path(args.prompt_manifest), "prompt manifest")
    output_path = _require_ignored(Path(args.output), "output")
    if output_path in {frozen_path, commitment_path, prompt_path}:
        raise PilotError("run opening output must differ from its inputs")
    if not prompt_path.is_file():
        raise PilotError("prompt manifest does not exist")
    try:
        prompt_text = prompt_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise PilotError(f"prompt manifest could not be read: {exc}") from exc
    if any(pattern.search(prompt_text) for pattern in PROMPT_ANSWER_PATTERNS):
        raise PilotError("answer-bearing prompt content is forbidden")
    frozen = _load_object(frozen_path, "frozen case")
    case, _ = _validate_frozen_case(frozen)
    commitment = _load_object(commitment_path, "public commitment")
    if (
        commitment.get("record_type")
        != "ai_benchmark_diagnostic_gold_commitment"
        or commitment.get("diagnostic_status") != "diagnostic_only"
    ):
        raise PilotError("public commitment is not a diagnostic commitment")
    if commitment.get("agent_access") != "none":
        raise PilotError("public commitment must deny Agent gold access")
    if commitment.get("unseal_status") != "sealed":
        raise PilotError("public commitment must remain sealed")
    _require_string(commitment.get("gold_key_id"), "gold_key_id")
    digest = commitment.get("commitment")
    if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
        raise PilotError("public commitment digest is invalid")
    if commitment.get("case_candidate_manifest_sha256") != frozen.get(
        "case_candidate_manifest_sha256"
    ):
        raise PilotError("public commitment does not bind the frozen candidates")
    if commitment.get("frozen_input_sha256") != frozen.get(
        "frozen_input_sha256"
    ):
        raise PilotError("public commitment does not bind the frozen input")
    prompt_sha256 = _sha256_file(prompt_path)
    if commitment.get("protocol_sha256") != prompt_sha256:
        raise PilotError("public commitment does not bind the prompt manifest")
    sealed_at = _validate_timestamp(commitment.get("sealed_at"), "sealed_at")
    opened_at = _validate_timestamp(args.opened_at, "opened_at")
    evidence_cutoff = _validate_timestamp(
        case.get("evidence_cutoff_at"),
        "evidence_cutoff_at",
    )
    if sealed_at < evidence_cutoff:
        raise PilotError("gold cannot be sealed before the evidence cutoff")
    if opened_at <= sealed_at:
        raise PilotError("gold must be sealed before opening a run")
    role = args.role
    if role not in {"primary", "execution_rerun", "model_independent_rerun"}:
        raise PilotError("run opening role is invalid")
    identity = {}
    for field in (
        "run_id",
        "execution_id",
        "agent_id",
        "model_id",
        "model_family",
        "context_id",
    ):
        identity[field] = _require_string(getattr(args, field), field)
    binding = {
        **identity,
        "role": role,
        "fresh_context": True,
        "prior_run_output_access": "none",
        "gold_access": "sealed_unavailable",
        "frozen_input_sha256": frozen["frozen_input_sha256"],
        "case_candidate_manifest_sha256": frozen[
            "case_candidate_manifest_sha256"
        ],
        "prompt_manifest_sha256": prompt_sha256,
        "public_commitment_sha256": _sha256_file(commitment_path),
        "gold_key_id": commitment.get("gold_key_id"),
        "gold_sealed_at": sealed_at,
        "opened_at": opened_at,
    }
    output = {
        "schema_version": "0.2.0",
        "record_type": "ai_benchmark_diagnostic_run_opening",
        "diagnostic_status": "diagnostic_only",
        "research_boundary": "benchmark_pilot_not_scholarship",
        **binding,
        "opening_lock_sha256": hashlib.sha256(
            _canonical_bytes(binding)
        ).hexdigest(),
        "caution": (
            "Pre-dispatch diagnostic receipt only; gold remains sealed and "
            "the run cannot authorize Gate 3, a decipherment result, or "
            "published scholarship."
        ),
    }
    _write_json_exclusive(output_path, output)
    return output_path


def _validate_run_opening(
    opening: dict[str, object],
    frozen: dict[str, object],
    prompt_sha256: str,
) -> tuple[str, str]:
    _require_exact_fields(opening, RUN_OPENING_FIELDS, "run opening")
    if opening.get("record_type") != "ai_benchmark_diagnostic_run_opening":
        raise PilotError("run opening has the wrong record_type")
    if opening.get("diagnostic_status") != "diagnostic_only":
        raise PilotError("run opening is not diagnostic_only")
    if opening.get("research_boundary") != "benchmark_pilot_not_scholarship":
        raise PilotError("run opening has the wrong research boundary")
    binding = {
        field: opening[field]
        for field in RUN_OPENING_BINDING_FIELDS
    }
    expected_lock = hashlib.sha256(_canonical_bytes(binding)).hexdigest()
    if opening.get("opening_lock_sha256") != expected_lock:
        raise PilotError("opening lock SHA-256 does not match its binding")
    for field in (
        "run_id",
        "execution_id",
        "agent_id",
        "model_id",
        "model_family",
        "context_id",
        "gold_key_id",
    ):
        _require_string(opening.get(field), f"run opening {field}")
    if opening.get("role") not in {
        "primary",
        "execution_rerun",
        "model_independent_rerun",
    }:
        raise PilotError("run opening role is invalid")
    if opening.get("fresh_context") is not True:
        raise PilotError("run opening must require a fresh context")
    if opening.get("prior_run_output_access") != "none":
        raise PilotError("run opening must deny prior run output access")
    if opening.get("gold_access") != "sealed_unavailable":
        raise PilotError("run opening must keep gold sealed and unavailable")
    for field in (
        "frozen_input_sha256",
        "case_candidate_manifest_sha256",
        "prompt_manifest_sha256",
        "public_commitment_sha256",
        "opening_lock_sha256",
    ):
        digest = opening.get(field)
        if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
            raise PilotError(f"run opening {field} is not a SHA-256 digest")
    if opening.get("frozen_input_sha256") != frozen.get(
        "frozen_input_sha256"
    ):
        raise PilotError("run opening does not bind the frozen input")
    if opening.get("case_candidate_manifest_sha256") != frozen.get(
        "case_candidate_manifest_sha256"
    ):
        raise PilotError("run opening does not bind the frozen candidates")
    if opening.get("prompt_manifest_sha256") != prompt_sha256:
        raise PilotError("prompt manifest SHA-256 does not match run opening")
    sealed_at = _validate_timestamp(
        opening.get("gold_sealed_at"),
        "gold_sealed_at",
    )
    opened_at = _validate_timestamp(opening.get("opened_at"), "opened_at")
    case = frozen.get("case")
    assert isinstance(case, dict)
    evidence_cutoff = _validate_timestamp(
        case.get("evidence_cutoff_at"),
        "evidence_cutoff_at",
    )
    if not evidence_cutoff <= sealed_at < opened_at:
        raise PilotError(
            "opening timestamps must satisfy evidence cutoff <= sealed < opened"
        )
    _require_string(opening.get("caution"), "run opening caution")
    return sealed_at, opened_at


def _validate_frozen_case(
    frozen: dict[str, object],
) -> tuple[dict[str, object], set[str]]:
    if frozen.get("record_type") != "ai_benchmark_diagnostic_frozen_case":
        raise PilotError("frozen case has the wrong record_type")
    if frozen.get("diagnostic_status") != "diagnostic_only":
        raise PilotError("frozen case is not diagnostic_only")
    case = frozen.get("case")
    snapshots = frozen.get("file_snapshots")
    if not isinstance(case, dict) or not isinstance(snapshots, list) or not snapshots:
        raise PilotError("frozen case is missing case or file snapshots")
    candidate_ids = case.get("candidate_ids")
    if not isinstance(candidate_ids, list) or not all(
        isinstance(item, str) for item in candidate_ids
    ):
        raise PilotError("frozen case candidate universe is invalid")
    _validate_candidates(candidate_ids)
    expected_manifest = _case_candidate_manifest_sha256({"cases": [case]})
    if expected_manifest != frozen.get("case_candidate_manifest_sha256"):
        raise PilotError("frozen case candidate manifest does not match")
    binding = {
        "object_dir": frozen.get("object_dir"),
        "case": case,
        "file_snapshots": snapshots,
    }
    expected_input = hashlib.sha256(_canonical_bytes(binding)).hexdigest()
    if expected_input != frozen.get("frozen_input_sha256"):
        raise PilotError("frozen input SHA-256 does not match its binding")

    evidence_hashes: set[str] = set()
    object_dir = frozen.get("object_dir")
    if not isinstance(object_dir, str):
        raise PilotError("frozen object_dir is invalid")
    object_route = Path(object_dir)
    if object_route.is_absolute() or ".." in object_route.parts:
        raise PilotError("frozen object_dir must stay inside the repository")
    object_path, object_relative = _corpus_object_relative(
        REPOSITORY_ROOT / object_route,
        "frozen object",
    )
    if object_relative != object_route.as_posix():
        raise PilotError("frozen object_dir route is not canonical")
    for index, snapshot in enumerate(snapshots):
        if not isinstance(snapshot, dict):
            raise PilotError(f"frozen snapshot {index} is not an object")
        _require_exact_fields(
            snapshot,
            FROZEN_SNAPSHOT_FIELDS,
            f"frozen snapshot {index}",
        )
        repository_path = snapshot.get("repository_path")
        object_relative_path = snapshot.get("object_relative_path")
        digest = snapshot.get("sha256")
        size_bytes = snapshot.get("size_bytes")
        if (
            not isinstance(repository_path, str)
            or not isinstance(object_relative_path, str)
            or not isinstance(digest, str)
        ):
            raise PilotError(f"frozen snapshot {index} binding is invalid")
        repository_route = Path(repository_path)
        object_relative_route = Path(object_relative_path)
        if (
            repository_route.is_absolute()
            or ".." in repository_route.parts
            or object_relative_route.is_absolute()
            or ".." in object_relative_route.parts
        ):
            raise PilotError(f"frozen snapshot {index} must stay inside the repository")
        source_path = (REPOSITORY_ROOT / repository_route).resolve()
        try:
            source_path.relative_to(REPOSITORY_ROOT)
            source_path.relative_to(object_path)
        except ValueError as exc:
            raise PilotError(
                f"frozen snapshot {index} escapes the object directory"
            ) from exc
        if source_path != (object_path / object_relative_route).resolve():
            raise PilotError(
                f"frozen snapshot {index} object and repository routes disagree"
            )
        if not source_path.is_file():
            raise PilotError(f"frozen source file is missing: {repository_path}")
        if source_path.stat().st_size != size_bytes or _sha256_file(source_path) != digest:
            raise PilotError(f"frozen source file changed: {repository_path}")
        if digest in evidence_hashes:
            raise PilotError(
                "frozen snapshot hashes must be unique to keep evidence "
                "references unambiguous"
            )
        evidence_hashes.add(digest)
    return case, evidence_hashes


def _validate_evidence_section(
    section: object,
    label: str,
    candidate_ids: set[str],
    evidence_hashes: set[str],
) -> None:
    if not isinstance(section, dict):
        raise PilotError(f"{label} must be an object")
    _require_exact_fields(section, EVIDENCE_SECTION_FIELDS, label)
    status = section.get("status")
    items = section.get("items")
    _require_string(section.get("search_note"), f"{label}.search_note")
    if status not in {"collected", "searched_none_found"}:
        raise PilotError(f"{label} must be collected or searched_none_found")
    if not isinstance(items, list):
        raise PilotError(f"{label}.items must be a list")
    if status == "collected" and not items:
        raise PilotError(f"{label} collected evidence requires an item")
    if status == "searched_none_found" and items:
        raise PilotError(f"{label} searched_none_found cannot contain items")
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise PilotError(f"{label}.items[{index}] must be an object")
        _require_exact_fields(item, EVIDENCE_ITEM_FIELDS, f"{label}.items[{index}]")
        digest = item.get("snapshot_sha256")
        if digest not in evidence_hashes:
            raise PilotError(f"{label} cites evidence outside the frozen evidence")
        if item.get("target_candidate_id") not in candidate_ids:
            raise PilotError(f"{label} targets a candidate outside the universe")
        _require_string(item.get("locator"), f"{label}.items[{index}].locator")
        _require_string(item.get("note"), f"{label}.items[{index}].note")


def _validate_prediction(
    prediction: object,
    case: dict[str, object],
    evidence_hashes: set[str],
) -> None:
    if not isinstance(prediction, dict):
        raise PilotError("prediction must be an object")
    _require_exact_fields(prediction, PREDICTION_FIELDS, "prediction")
    if prediction.get("case_id") != case.get("case_id"):
        raise PilotError("prediction case_id does not match the frozen case")
    frozen_candidates = case.get("candidate_ids")
    assert isinstance(frozen_candidates, list)
    candidate_ids = set(frozen_candidates)
    ranked = prediction.get("ranked_candidates")
    if not isinstance(ranked, list) or len(ranked) != len(frozen_candidates):
        raise PilotError("ranked candidates do not cover the candidate universe")
    ranked_ids: list[str] = []
    probabilities: list[float] = []
    for index, item in enumerate(ranked, 1):
        if not isinstance(item, dict) or set(item) != {
            "rank",
            "candidate_id",
            "probability",
        }:
            raise PilotError(f"ranked candidate {index} fields are invalid")
        rank = item.get("rank")
        if isinstance(rank, bool) or not isinstance(rank, int):
            raise PilotError("candidate rank must be an integer")
        if rank != index:
            raise PilotError("candidate ranks must be contiguous from one")
        candidate_id = item.get("candidate_id")
        probability = item.get("probability")
        if not isinstance(candidate_id, str):
            raise PilotError("ranked candidate ID must be a string")
        if (
            not isinstance(probability, (int, float))
            or isinstance(probability, bool)
            or not 0 <= probability <= 1
        ):
            raise PilotError("candidate probability must be between zero and one")
        ranked_ids.append(candidate_id)
        probabilities.append(float(probability))
    if set(ranked_ids) != candidate_ids or len(ranked_ids) != len(set(ranked_ids)):
        raise PilotError("ranked candidates do not match the candidate universe")
    if abs(sum(probabilities) - 1.0) > 1e-9:
        raise PilotError("candidate probabilities must sum to one")
    if any(left < right for left, right in zip(probabilities, probabilities[1:])):
        raise PilotError("candidate probabilities must be non-increasing")

    action = prediction.get("action")
    selected = prediction.get("selected_candidate_id")
    reason = prediction.get("abstention_reason_code")
    if action == "predict":
        if selected != ranked_ids[0] or reason is not None:
            raise PilotError("predict must select rank one without abstention reason")
        if len(probabilities) > 1 and probabilities[0] <= probabilities[1]:
            raise PilotError("predict probability must strictly exceed rank two")
    elif action == "abstain":
        if selected is not None:
            raise PilotError("abstain must not select a candidate")
        _require_string(reason, "abstention_reason_code")
    else:
        raise PilotError("prediction action must be predict or abstain")

    _validate_evidence_section(
        prediction.get("supporting_evidence"),
        "supporting_evidence",
        candidate_ids,
        evidence_hashes,
    )
    _validate_evidence_section(
        prediction.get("opposing_evidence"),
        "opposing_evidence",
        candidate_ids,
        evidence_hashes,
    )
    if action == "predict":
        supporting = prediction.get("supporting_evidence")
        assert isinstance(supporting, dict)
        supporting_items = supporting.get("items")
        assert isinstance(supporting_items, list)
        if not any(
            isinstance(item, dict)
            and item.get("target_candidate_id") == selected
            for item in supporting_items
        ):
            raise PilotError(
                "predict requires supporting evidence for the selected candidate"
            )
    checks = prediction.get("falsification_checks")
    if not isinstance(checks, list) or not checks:
        raise PilotError("prediction requires a falsification check")
    check_ids: list[str] = []
    for index, check in enumerate(checks):
        if not isinstance(check, dict):
            raise PilotError(f"falsification check {index} must be an object")
        _require_exact_fields(check, FALSIFICATION_FIELDS, f"falsification[{index}]")
        check_ids.append(_require_string(check.get("check_id"), "check_id"))
        if check.get("target_candidate_id") not in candidate_ids:
            raise PilotError("falsification check targets an unknown candidate")
        _require_string(check.get("method"), "falsification method")
        if check.get("outcome") not in {"not_triggered", "triggered", "inconclusive"}:
            raise PilotError("falsification outcome is invalid")
        digests = check.get("evidence_snapshot_sha256s")
        if not isinstance(digests, list) or not digests:
            raise PilotError("falsification check requires frozen evidence")
        if any(digest not in evidence_hashes for digest in digests):
            raise PilotError("falsification cites evidence outside the frozen evidence")
        _require_string(check.get("note"), "falsification note")
        if (
            action == "predict"
            and check.get("target_candidate_id") == selected
            and check.get("outcome") == "triggered"
        ):
            raise PilotError(
                "a triggered falsifier requires abstention for the selected candidate"
            )
    if len(check_ids) != len(set(check_ids)):
        raise PilotError("falsification check IDs must be unique")

    leakage = prediction.get("leakage_assessment")
    if not isinstance(leakage, dict):
        raise PilotError("leakage_assessment must be an object")
    _require_exact_fields(leakage, LEAKAGE_FIELDS, "leakage_assessment")
    if leakage.get("status") not in {
        "screened_no_known_leakage",
        "suspected",
        "confirmed",
        "indeterminate",
    }:
        raise PilotError("leakage status is invalid")
    types = leakage.get("types")
    if not isinstance(types, list) or not all(
        isinstance(item, str) and item for item in types
    ):
        raise PilotError("leakage types must be a list of strings")
    if leakage.get("disposition") != "diagnostic_only":
        raise PilotError("pilot leakage disposition must be diagnostic_only")
    leakage_status = leakage.get("status")
    if leakage_status == "screened_no_known_leakage" and types:
        raise PilotError(
            "screened_no_known_leakage cannot report leakage types"
        )
    if leakage_status in {"suspected", "confirmed"} and not types:
        raise PilotError(f"{leakage_status} leakage requires a reported type")
    if set(types) & {
        "gold_label",
        "peer_output",
    }:
        raise PilotError("reported leakage contradicts sealed run access")
    _require_string(leakage.get("note"), "leakage note")
    _require_string(prediction.get("reasoning_summary"), "reasoning_summary")


def lock_run(args: argparse.Namespace) -> Path:
    frozen_path = _require_ignored(Path(args.frozen_case), "frozen case")
    opening_path = _require_ignored(Path(args.run_opening), "run opening")
    report_path = _require_ignored(Path(args.run_report), "run report")
    prompt_path = _require_ignored(Path(args.prompt_manifest), "prompt manifest")
    agent_output_path = _require_ignored(Path(args.agent_output), "Agent output")
    output_path = _require_ignored(Path(args.output), "output")
    if output_path in {
        frozen_path,
        opening_path,
        report_path,
        prompt_path,
        agent_output_path,
    }:
        raise PilotError("locked output must differ from its inputs")
    if not prompt_path.is_file():
        raise PilotError("prompt manifest does not exist")
    if not agent_output_path.is_file():
        raise PilotError("Agent output does not exist")
    frozen = _load_object(frozen_path, "frozen case")
    opening = _load_object(opening_path, "run opening")
    report = _load_object(report_path, "run report")
    forbidden_routes = _answer_field_routes(report)
    if forbidden_routes:
        raise PilotError(
            "answer-bearing run field is forbidden: " + forbidden_routes[0]
        )
    _require_exact_fields(report, RUN_REPORT_FIELDS, "run report")
    case, evidence_hashes = _validate_frozen_case(frozen)
    prompt_sha256 = _sha256_file(prompt_path)
    sealed_at, opened_at = _validate_run_opening(
        opening,
        frozen,
        prompt_sha256,
    )
    for field in (
        "run_id",
        "execution_id",
        "agent_id",
        "model_id",
        "model_family",
        "context_id",
    ):
        _require_string(report.get(field), field)
    if report.get("role") not in {
        "primary",
        "execution_rerun",
        "model_independent_rerun",
    }:
        raise PilotError("run role is invalid")
    if report.get("fresh_context") is not True:
        raise PilotError("run must use a fresh context")
    if report.get("prior_run_output_access") != "none":
        raise PilotError("prior run output access must be none")
    if report.get("gold_access") != "sealed_unavailable":
        raise PilotError("gold access must remain sealed_unavailable")
    if report.get("frozen_input_sha256") != frozen.get("frozen_input_sha256"):
        raise PilotError("run report does not bind the frozen input")
    if report.get("prompt_manifest_sha256") != prompt_sha256:
        raise PilotError("prompt manifest SHA-256 does not match the run report")
    for field in RUN_OPENING_REPORT_FIELDS:
        if report.get(field) != opening.get(field):
            raise PilotError(
                f"run report {field} does not match run opening"
            )
    if report.get("agent_output_sha256") != _sha256_file(agent_output_path):
        raise PilotError("Agent output SHA-256 does not match the run report")
    try:
        agent_prediction = json.loads(
            agent_output_path.read_text(encoding="utf-8"),
            object_pairs_hook=_unique_json_object,
        )
    except (OSError, json.JSONDecodeError) as exc:
        raise PilotError(f"invalid Agent output: {exc}") from exc
    if agent_prediction != report.get("prediction"):
        raise PilotError("Agent output prediction does not match the run report")
    started = _validate_timestamp(report.get("started_at"), "started_at")
    completed = _validate_timestamp(report.get("completed_at"), "completed_at")
    locked_at = _validate_timestamp(args.locked_at, "locked_at")
    if not sealed_at < opened_at < started < completed < locked_at:
        raise PilotError(
            "run timestamps must satisfy "
            "sealed < opened < started < completed < locked"
        )
    _validate_prediction(report.get("prediction"), case, evidence_hashes)

    output = {
        "schema_version": "0.2.0",
        "record_type": "ai_benchmark_diagnostic_locked_run",
        "diagnostic_status": "diagnostic_only",
        "research_boundary": "benchmark_pilot_not_scholarship",
        "pretraining_exposure": "unknown",
        "benchmark_eligibility": "pretraining_exposure_unknown",
        "probability_status": "uncalibrated_agent_distribution",
        "calibration_status": "not_calibrated",
        "delivery_status": "withheld",
        "gate3_status": "not_attempted",
        "frozen_input_sha256": frozen["frozen_input_sha256"],
        "run_opening_sha256": _sha256_file(opening_path),
        "public_commitment_sha256": opening["public_commitment_sha256"],
        "prompt_manifest_sha256": report["prompt_manifest_sha256"],
        "agent_output_sha256": report["agent_output_sha256"],
        "case_candidate_manifest_sha256": frozen[
            "case_candidate_manifest_sha256"
        ],
        "locked_at": locked_at,
        "prediction_lock_sha256": hashlib.sha256(
            _canonical_bytes(report)
        ).hexdigest(),
        "run": report,
        "caution": (
            "Uncalibrated diagnostic Agent distribution only; delivery is "
            "withheld. This is not Gate 3, not a decipherment result, and not "
            "published scholarship."
        ),
    }
    _write_json_exclusive(output_path, output)
    return output_path


def _validate_public_commitment_for_scoring(
    public: dict[str, object],
    frozen: dict[str, object],
) -> str:
    _require_exact_fields(
        public,
        PUBLIC_COMMITMENT_FIELDS,
        "public commitment",
    )
    if public.get("schema_version") != "0.1.0":
        raise PilotError("public commitment schema version is invalid")
    if public.get("record_type") != "ai_benchmark_diagnostic_gold_commitment":
        raise PilotError("public commitment record type is invalid")
    for field, expected in DIAGNOSTIC_FIELDS.items():
        if public.get(field) != expected:
            raise PilotError(f"public commitment {field} is invalid")
    if public.get("commitment_scheme") != "hmac-sha256":
        raise PilotError("public commitment scheme must be hmac-sha256")
    if public.get("storage_class") != "ignored_local_diagnostic":
        raise PilotError("public commitment storage class is invalid")
    if public.get("agent_access") != "none":
        raise PilotError("public commitment must deny Agent gold access")
    if public.get("unseal_status") != "sealed":
        raise PilotError("public commitment must remain sealed before scoring")
    if public.get("scorer_only") is not True:
        raise PilotError("public commitment must reserve gold for the scorer")
    if type(public.get("score_query_limit")) is not int or public.get(
        "score_query_limit"
    ) != 1:
        raise PilotError("public commitment score_query_limit must be one")
    for field in ("benchmark_id", "benchmark_version", "gold_key_id", "caution"):
        _require_string(public.get(field), f"public commitment {field}")
    for field in (
        "commitment",
        "frozen_input_sha256",
        "case_candidate_manifest_sha256",
        "protocol_sha256",
    ):
        digest = public.get(field)
        if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
            raise PilotError(f"public commitment {field} is invalid")
    if public.get("frozen_input_sha256") != frozen.get("frozen_input_sha256"):
        raise PilotError("public commitment does not bind the frozen input")
    if public.get("case_candidate_manifest_sha256") != frozen.get(
        "case_candidate_manifest_sha256"
    ):
        raise PilotError("public commitment does not bind the frozen candidates")
    return _validate_timestamp(public.get("sealed_at"), "sealed_at")


def _validate_locked_run_for_scoring(
    locked: dict[str, object],
    locked_path: Path,
    frozen: dict[str, object],
    case: dict[str, object],
    evidence_hashes: set[str],
    public_sha256: str,
    protocol_sha256: object,
    scored_at: str,
) -> tuple[str, dict[str, object]]:
    _require_exact_fields(locked, LOCKED_RUN_FIELDS, "locked run")
    expected_values = {
        "record_type": "ai_benchmark_diagnostic_locked_run",
        "diagnostic_status": "diagnostic_only",
        "research_boundary": "benchmark_pilot_not_scholarship",
        "pretraining_exposure": "unknown",
        "benchmark_eligibility": "pretraining_exposure_unknown",
        "probability_status": "uncalibrated_agent_distribution",
        "calibration_status": "not_calibrated",
        "delivery_status": "withheld",
        "gate3_status": "not_attempted",
    }
    for field, expected in expected_values.items():
        if locked.get(field) != expected:
            raise PilotError(f"locked run {field} must be {expected}")
    if locked.get("frozen_input_sha256") != frozen.get("frozen_input_sha256"):
        raise PilotError("locked run does not bind the frozen input")
    if locked.get("case_candidate_manifest_sha256") != frozen.get(
        "case_candidate_manifest_sha256"
    ):
        raise PilotError("locked run does not bind the frozen candidates")
    if locked.get("public_commitment_sha256") != public_sha256:
        raise PilotError("locked run does not bind the public commitment")
    if locked.get("prompt_manifest_sha256") != protocol_sha256:
        raise PilotError("locked run does not bind the committed protocol")
    for field in (
        "run_opening_sha256",
        "public_commitment_sha256",
        "prompt_manifest_sha256",
        "agent_output_sha256",
        "prediction_lock_sha256",
    ):
        digest = locked.get(field)
        if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
            raise PilotError(f"locked run {field} is invalid")
    run = locked.get("run")
    if not isinstance(run, dict):
        raise PilotError("locked run is missing its run report")
    _require_exact_fields(run, RUN_REPORT_FIELDS, "locked run report")
    forbidden_routes = _answer_field_routes(run)
    if forbidden_routes:
        raise PilotError(
            "answer-bearing locked run field is forbidden: "
            + forbidden_routes[0]
        )
    if hashlib.sha256(_canonical_bytes(run)).hexdigest() != locked.get(
        "prediction_lock_sha256"
    ):
        raise PilotError("locked run prediction lock does not match its report")
    if run.get("frozen_input_sha256") != frozen.get("frozen_input_sha256"):
        raise PilotError("locked run report does not bind the frozen input")
    if run.get("prompt_manifest_sha256") != protocol_sha256:
        raise PilotError("locked run report does not bind the committed protocol")
    if run.get("agent_output_sha256") != locked.get("agent_output_sha256"):
        raise PilotError("locked run Agent output binding is inconsistent")
    for field in (
        "run_id",
        "execution_id",
        "agent_id",
        "model_id",
        "model_family",
        "context_id",
    ):
        _require_string(run.get(field), f"locked run {field}")
    if run.get("role") not in {
        "primary",
        "execution_rerun",
        "model_independent_rerun",
    }:
        raise PilotError("locked run role is invalid")
    if run.get("fresh_context") is not True:
        raise PilotError("locked run must use a fresh context")
    if run.get("prior_run_output_access") != "none":
        raise PilotError("locked run must deny prior run output access")
    if run.get("gold_access") != "sealed_unavailable":
        raise PilotError("locked run must keep gold sealed and unavailable")
    locked_at = _validate_timestamp(locked.get("locked_at"), "locked_at")
    completed_at = _validate_timestamp(run.get("completed_at"), "completed_at")
    _validate_timestamp(run.get("started_at"), "started_at")
    if not completed_at < locked_at < scored_at:
        raise PilotError(
            "scoring timestamps must satisfy completed < locked < scored"
        )
    prediction = run.get("prediction")
    _validate_prediction(prediction, case, evidence_hashes)
    assert isinstance(prediction, dict)
    ranked = prediction["ranked_candidates"]
    assert isinstance(ranked, list) and ranked and isinstance(ranked[0], dict)
    top_candidate_id = ranked[0]["candidate_id"]
    leakage = prediction["leakage_assessment"]
    assert isinstance(leakage, dict)
    receipt = {
        "locked_run_sha256": _sha256_file(locked_path),
        "run_id": run["run_id"],
        "action": prediction["action"],
        "selected_candidate_id": prediction["selected_candidate_id"],
        "top1_candidate_id": top_candidate_id,
        "leakage_status": leakage["status"],
        "pretraining_exposure_unknown_recorded": (
            "pretraining_exposure_unknown" in leakage["types"]
        ),
    }
    return str(run["run_id"]), receipt


def score_local(args: argparse.Namespace) -> Path:
    frozen_path = _require_ignored(Path(args.frozen_case), "frozen case")
    public_path = _require_ignored(
        Path(args.public_commitment), "public commitment"
    )
    private_path = _require_ignored(Path(args.private_gold), "private gold")
    locked_paths = [
        _require_ignored(Path(path), "locked run")
        for path in args.locked_run
    ]
    output_path = _require_ignored(Path(args.output), "output")
    input_paths = {frozen_path, public_path, private_path, *locked_paths}
    if output_path in input_paths:
        raise PilotError("score output must differ from its inputs")
    if len(locked_paths) < 2:
        raise PilotError("score-local requires at least two locked runs")

    frozen = _load_object(frozen_path, "frozen case")
    case, evidence_hashes = _validate_frozen_case(frozen)
    if case.get("case_type") != "null_or_negative_control":
        raise PilotError("score-local supports only a null or negative control")
    public = _load_object(public_path, "public commitment")
    sealed_at = _validate_public_commitment_for_scoring(public, frozen)
    scored_at = _validate_timestamp(args.scored_at, "scored_at")
    if scored_at <= sealed_at:
        raise PilotError("scoring must occur after gold was sealed")
    public_sha256 = _sha256_file(public_path)

    run_ids: list[str] = []
    run_receipts: list[dict[str, object]] = []
    for locked_path in locked_paths:
        locked = _load_object(locked_path, "locked run")
        run_id, run_receipt = _validate_locked_run_for_scoring(
            locked,
            locked_path,
            frozen,
            case,
            evidence_hashes,
            public_sha256,
            public.get("protocol_sha256"),
            scored_at,
        )
        run_ids.append(run_id)
        run_receipts.append(run_receipt)
    if len(run_ids) != len(set(run_ids)):
        raise PilotError("locked run IDs must be unique")

    # This is the sole private-gold read in score-local. All public and run
    # bindings are checked first so opening gold cannot influence validation.
    private_gold = _load_object(private_path, "private gold")
    _validate_private_gold(private_gold, frozen)
    for field in (
        "benchmark_id",
        "benchmark_version",
        "gold_key_id",
        "case_candidate_manifest_sha256",
        "protocol_sha256",
    ):
        if private_gold.get(field) != public.get(field):
            raise PilotError(f"private gold and public commitment disagree on {field}")
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
    committed_payload["frozen_input_sha256"] = frozen["frozen_input_sha256"]
    expected_commitment = hmac.new(
        bytes.fromhex(str(private_gold["commitment_key_hex"])),
        _canonical_bytes(committed_payload),
        hashlib.sha256,
    ).hexdigest()
    if not hmac.compare_digest(
        expected_commitment,
        str(public.get("commitment")),
    ):
        raise PilotError("public HMAC commitment does not match private gold")

    labels = private_gold["labels"]
    assert isinstance(labels, list) and len(labels) == 1
    label = labels[0]
    assert isinstance(label, dict)
    gold_candidate_id = label["gold_candidate_id"]
    all_runs_match = True
    for receipt in run_receipts:
        top1_matches_gold = receipt["top1_candidate_id"] == gold_candidate_id
        receipt["top1_matches_gold"] = top1_matches_gold
        if not (
            receipt["action"] == "abstain"
            and receipt["selected_candidate_id"] is None
            and top1_matches_gold
            and receipt["leakage_status"] == "indeterminate"
            and receipt["pretraining_exposure_unknown_recorded"] is True
        ):
            all_runs_match = False

    output = {
        "schema_version": "0.1.0",
        "record_type": "ai_benchmark_local_diagnostic_score_receipt",
        "diagnostic_status": "diagnostic_only",
        "research_boundary": "benchmark_pilot_not_scholarship",
        "pretraining_exposure": "unknown",
        "benchmark_eligibility": "pretraining_exposure_unknown",
        "pipeline_diagnostic_status": (
            "pipeline_diagnostic_pass"
            if all_runs_match
            else "diagnostic_fail_withheld"
        ),
        "query_count": 1,
        "score_query_limit": 1,
        "gold_state": "opened_retired_local_diagnostic",
        "evaluation_state": "retired_after_single_scoring",
        "probability_status": "not_generated",
        "calibration_status": "not_calibrated",
        "delivery_status": "withheld",
        "gate3_status": "not_attempted",
        "frozen_input_sha256": frozen["frozen_input_sha256"],
        "case_candidate_manifest_sha256": frozen[
            "case_candidate_manifest_sha256"
        ],
        "public_commitment_sha256": public_sha256,
        "case_type": case["case_type"],
        "scored_at": scored_at,
        "run_count": len(run_receipts),
        "runs": run_receipts,
        "caution": (
            "Retired one-shot local pipeline diagnostic only; no probability, "
            "candidate delivery, Gate 3 authorization, decipherment, or "
            "published scholarship result is created."
        ),
    }
    _write_json_exclusive(output_path, output)
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
    seal.add_argument("--frozen-case", required=True)
    seal.add_argument("--private-gold", required=True)
    seal.add_argument("--sealed-at", required=True)
    seal.add_argument("--output", required=True)
    opening = subparsers.add_parser(
        "open-run", help="lock one diagnostic run before Agent dispatch"
    )
    opening.add_argument("--frozen-case", required=True)
    opening.add_argument("--public-commitment", required=True)
    opening.add_argument("--prompt-manifest", required=True)
    opening.add_argument("--run-id", required=True)
    opening.add_argument(
        "--role",
        choices=["primary", "execution_rerun", "model_independent_rerun"],
        required=True,
    )
    opening.add_argument("--execution-id", required=True)
    opening.add_argument("--agent-id", required=True)
    opening.add_argument("--model-id", required=True)
    opening.add_argument("--model-family", required=True)
    opening.add_argument("--context-id", required=True)
    opening.add_argument("--opened-at", required=True)
    opening.add_argument("--output", required=True)
    locked = subparsers.add_parser(
        "lock-run", help="validate and lock one blind diagnostic Agent run"
    )
    locked.add_argument("--frozen-case", required=True)
    locked.add_argument("--run-opening", required=True)
    locked.add_argument("--run-report", required=True)
    locked.add_argument("--prompt-manifest", required=True)
    locked.add_argument("--agent-output", required=True)
    locked.add_argument("--locked-at", required=True)
    locked.add_argument("--output", required=True)
    scoring = subparsers.add_parser(
        "score-local",
        help="score one retired ignored-local negative-control diagnostic",
    )
    scoring.add_argument("--frozen-case", required=True)
    scoring.add_argument("--public-commitment", required=True)
    scoring.add_argument("--private-gold", required=True)
    scoring.add_argument("--locked-run", action="append", required=True)
    scoring.add_argument("--scored-at", required=True)
    scoring.add_argument("--output", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        if args.command == "freeze":
            output = freeze_case(args)
            print(f"PASS diagnostic frozen case: {output}")
        elif args.command == "seal":
            output = seal_gold(args)
            print(f"PASS diagnostic gold commitment: {output}")
        elif args.command == "open-run":
            output = open_run(args)
            print(f"PASS diagnostic run opening: {output}")
        elif args.command == "lock-run":
            output = lock_run(args)
            print(f"PASS diagnostic locked run: {output}")
        else:
            output = score_local(args)
            print(f"PASS local diagnostic score: {output}")
    except PilotError as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
