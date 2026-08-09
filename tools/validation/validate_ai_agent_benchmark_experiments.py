#!/usr/bin/env python3
"""Validate version 2 AI Agent benchmark experiment records."""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import math
import re
import subprocess
from datetime import datetime
from functools import lru_cache
from pathlib import Path


FORBIDDEN_PUBLIC_GOLD_KEYS = {
    "answer",
    "correct_candidate_id",
    "gold_candidate_id",
    "gold_label",
    "ground_truth",
}

TOP_LEVEL_FIELDS = {
    "adjudication",
    "benchmark",
    "caution",
    "created_at",
    "evaluation",
    "experiment_id",
    "human_delivery_package",
    "protocol",
    "record_type",
    "research_boundary",
    "review_log",
    "runs",
    "schema_version",
    "status",
    "updated_at",
}

EXPERIMENT_SUFFIX = "_benchmark-experiment-v2.json"
DEFAULT_EXPERIMENT_ROOT = Path(
    "doc/public/user_research/generated/ai-agent-benchmark-experiments"
)
SCHEMA_PATH = Path(
    "schemas/007_ai-agent-benchmark-experiment-schema/"
    "ai-agent-benchmark-experiment-v2.schema.json"
)


@lru_cache(maxsize=1)
def _load_public_schema() -> dict[str, object]:
    schema_path = _repo_root() / SCHEMA_PATH
    data = json.loads(schema_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("benchmark experiment schema must be an object")
    return data


def _schema_ref(root: dict[str, object], reference: str) -> object:
    if not reference.startswith("#/"):
        raise ValueError(f"unsupported nonlocal schema reference: {reference}")
    value: object = root
    for token in reference[2:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        if not isinstance(value, dict) or token not in value:
            raise ValueError(f"unresolved schema reference: {reference}")
        value = value[token]
    return value


def _matches_schema_type(value: object, expected: str) -> bool:
    if expected == "null":
        return value is None
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "string":
        return isinstance(value, str)
    if expected == "array":
        return isinstance(value, list)
    if expected == "object":
        return isinstance(value, dict)
    raise ValueError(f"unsupported schema type: {expected}")


def _schema_issues(
    value: object,
    schema: object,
    root: dict[str, object],
    route: str = "$",
) -> list[str]:
    if not isinstance(schema, dict):
        return [f"schema {route}: contract node must be an object"]
    reference = schema.get("$ref")
    if isinstance(reference, str):
        return _schema_issues(value, _schema_ref(root, reference), root, route)

    issues: list[str] = []
    all_of = schema.get("allOf")
    if isinstance(all_of, list):
        for branch in all_of:
            issues.extend(_schema_issues(value, branch, root, route))
    one_of = schema.get("oneOf")
    if isinstance(one_of, list):
        matching = [
            branch
            for branch in one_of
            if not _schema_issues(value, branch, root, route)
        ]
        if len(matching) != 1:
            issues.append(f"schema {route}: value must match exactly one option")
        return issues

    if "const" in schema and value != schema["const"]:
        issues.append(f"schema {route}: value must equal {schema['const']!r}")
    enum = schema.get("enum")
    if isinstance(enum, list) and value not in enum:
        issues.append(f"schema {route}: value is outside the allowed enum")

    expected_type = schema.get("type")
    if isinstance(expected_type, str):
        if not _matches_schema_type(value, expected_type):
            issues.append(f"schema {route}: expected {expected_type}")
            return issues
    elif isinstance(expected_type, list):
        if not any(
            isinstance(item, str) and _matches_schema_type(value, item)
            for item in expected_type
        ):
            issues.append(f"schema {route}: value has an invalid type")
            return issues

    if isinstance(value, dict):
        required = schema.get("required")
        if isinstance(required, list):
            for key in required:
                if isinstance(key, str) and key not in value:
                    issues.append(f"schema {route}.{key}: required field is missing")
        properties = schema.get("properties")
        if isinstance(properties, dict):
            if schema.get("additionalProperties") is False:
                for key in value:
                    if key not in properties:
                        issues.append(
                            f"schema {route}.{key}: additional field is forbidden"
                        )
            for key, child_schema in properties.items():
                if key in value:
                    issues.extend(
                        _schema_issues(
                            value[key], child_schema, root, f"{route}.{key}"
                        )
                    )

    if isinstance(value, list):
        minimum_items = schema.get("minItems")
        if isinstance(minimum_items, int) and len(value) < minimum_items:
            issues.append(
                f"schema {route}: requires at least {minimum_items} items"
            )
        if schema.get("uniqueItems") is True:
            serialized = [
                json.dumps(item, ensure_ascii=False, sort_keys=True)
                for item in value
            ]
            if len(serialized) != len(set(serialized)):
                issues.append(f"schema {route}: items must be unique")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                issues.extend(
                    _schema_issues(item, item_schema, root, f"{route}[{index}]")
                )

    if isinstance(value, str):
        minimum_length = schema.get("minLength")
        if isinstance(minimum_length, int) and len(value) < minimum_length:
            issues.append(
                f"schema {route}: requires at least {minimum_length} characters"
            )
        pattern = schema.get("pattern")
        if isinstance(pattern, str) and re.search(pattern, value) is None:
            issues.append(f"schema {route}: value does not match {pattern!r}")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        minimum = schema.get("minimum")
        maximum = schema.get("maximum")
        exclusive_minimum = schema.get("exclusiveMinimum")
        exclusive_maximum = schema.get("exclusiveMaximum")
        if isinstance(minimum, (int, float)) and value < minimum:
            issues.append(f"schema {route}: value is below minimum {minimum}")
        if isinstance(maximum, (int, float)) and value > maximum:
            issues.append(f"schema {route}: value exceeds maximum {maximum}")
        if isinstance(exclusive_minimum, (int, float)) and value <= exclusive_minimum:
            issues.append(
                f"schema {route}: value must exceed {exclusive_minimum}"
            )
        if isinstance(exclusive_maximum, (int, float)) and value >= exclusive_maximum:
            issues.append(
                f"schema {route}: value must be below {exclusive_maximum}"
            )
    return issues


def _validate_public_schema(data: object) -> list[str]:
    try:
        schema = _load_public_schema()
        return _schema_issues(data, schema, schema)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [f"schema contract could not be evaluated: {exc}"]


def discover_experiment_paths(path: Path) -> list[Path]:
    """Find v2 benchmark records without scanning v1 evidence packs."""

    if path.is_file():
        return [path] if path.name.endswith(EXPERIMENT_SUFFIX) else []
    if not path.exists():
        return []
    return sorted(path.rglob(f"*{EXPERIMENT_SUFFIX}"))


def _find_forbidden_gold_keys(value: object, route: str = "$") -> list[str]:
    issues: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            item_route = f"{route}.{key}"
            if key in FORBIDDEN_PUBLIC_GOLD_KEYS:
                issues.append(f"forbidden public gold key at {item_route}")
            issues.extend(_find_forbidden_gold_keys(item, item_route))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            issues.extend(_find_forbidden_gold_keys(item, f"{route}[{index}]"))
    return issues


def _parse_timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _validate_family_splits(data: dict[str, object]) -> list[str]:
    benchmark = data.get("benchmark")
    if not isinstance(benchmark, dict):
        return ["benchmark must be an object"]
    cases = benchmark.get("cases")
    if not isinstance(cases, list):
        return ["benchmark.cases must be a list"]

    family_splits: dict[str, str] = {}
    issues: list[str] = []
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            issues.append(f"benchmark.cases[{index}] must be an object")
            continue
        family_id = case.get("family_id")
        split = case.get("split")
        if not isinstance(family_id, str) or not isinstance(split, str):
            continue
        prior_split = family_splits.setdefault(family_id, split)
        if prior_split != split:
            issues.append(
                f"family_id crosses splits: {family_id} is in "
                f"{prior_split} and {split}"
            )
    return issues


def _validate_case_identifiers(data: dict[str, object]) -> list[str]:
    benchmark = data.get("benchmark")
    if not isinstance(benchmark, dict) or not isinstance(
        benchmark.get("cases"), list
    ):
        return []
    case_ids = [
        case.get("case_id")
        for case in benchmark["cases"]
        if isinstance(case, dict) and isinstance(case.get("case_id"), str)
    ]
    issues: list[str] = []
    if len(case_ids) != len(set(case_ids)):
        issues.append("benchmark case_id must be unique")
    case_types = {
        case.get("case_type")
        for case in benchmark["cases"]
        if isinstance(case, dict)
    }
    required_types = {
        "masked_known_reading",
        "historically_disputed",
        "null_or_negative_control",
        "hard_challenge",
    }
    if not required_types.issubset(case_types):
        issues.append("benchmark must contain all four case types")
    for index, case in enumerate(benchmark["cases"]):
        if not isinstance(case, dict):
            continue
        candidate_ids = case.get("candidate_ids")
        if isinstance(candidate_ids, list) and "unknown_or_other" not in candidate_ids:
            issues.append(
                f"benchmark.cases[{index}] candidate universe must include "
                "unknown_or_other"
            )
        exposure = case.get("pretraining_exposure")
        eligibility = case.get("benchmark_eligibility")
        if (
            eligibility == "clean_holdout_eligible"
            and exposure != "verified_post_training_cutoff"
        ):
            issues.append(
                f"benchmark.cases[{index}] clean eligibility requires "
                "verified post-cutoff exposure"
            )
        cutoff_evidence = case.get("training_cutoff_evidence")
        if (
            eligibility == "clean_holdout_eligible"
            and (
                not isinstance(cutoff_evidence, dict)
                or cutoff_evidence.get("review_status") != "verified"
            )
        ):
            issues.append(
                f"benchmark.cases[{index}] training cutoff evidence is not verified"
            )
        if (
            exposure == "unknown"
            and eligibility != "pretraining_exposure_unknown"
        ):
            issues.append(
                f"benchmark.cases[{index}] unknown exposure must be diagnostic"
            )
    return issues


def _case_candidate_manifest_sha256(benchmark: dict[str, object]) -> str | None:
    cases = benchmark.get("cases")
    if not isinstance(cases, list):
        return None
    manifest = []
    for case in cases:
        if not isinstance(case, dict):
            return None
        case_id = case.get("case_id")
        candidate_ids = case.get("candidate_ids")
        if not isinstance(case_id, str) or not isinstance(candidate_ids, list):
            return None
        manifest.append(
            {
                "case_id": case_id,
                "family_id": case.get("family_id"),
                "split": case.get("split"),
                "candidate_ids": candidate_ids,
            }
        )
    message = json.dumps(
        sorted(manifest, key=lambda item: item["case_id"]),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(message).hexdigest()


def _test_case_candidates(
    data: dict[str, object],
) -> tuple[dict[str, list[str]], list[str]]:
    benchmark = data.get("benchmark")
    if not isinstance(benchmark, dict) or not isinstance(
        benchmark.get("cases"), list
    ):
        return {}, []
    result: dict[str, list[str]] = {}
    issues: list[str] = []
    for index, case in enumerate(benchmark["cases"]):
        if not isinstance(case, dict) or case.get("split") != "test":
            continue
        case_id = case.get("case_id")
        candidate_ids = case.get("candidate_ids")
        if not isinstance(case_id, str) or not isinstance(candidate_ids, list):
            issues.append(f"benchmark.cases[{index}] has invalid test case route")
            continue
        if not all(isinstance(value, str) for value in candidate_ids):
            issues.append(f"benchmark.cases[{index}].candidate_ids must be strings")
            continue
        result[case_id] = candidate_ids
    return result, issues


def _validate_prediction_universes(data: dict[str, object]) -> list[str]:
    test_cases, issues = _test_case_candidates(data)
    tolerance = 1e-9
    protocol = data.get("protocol")
    if isinstance(protocol, dict):
        probability_policy = protocol.get("probability_policy")
        if isinstance(probability_policy, dict):
            configured_tolerance = probability_policy.get("sum_tolerance")
            if isinstance(configured_tolerance, (int, float)) and not isinstance(
                configured_tolerance, bool
            ):
                tolerance = float(configured_tolerance)
    runs = data.get("runs")
    if not isinstance(runs, list):
        return issues + ["runs must be a list"]

    for run_index, run in enumerate(runs):
        if not isinstance(run, dict) or not isinstance(run.get("predictions"), list):
            issues.append(f"runs[{run_index}].predictions must be a list")
            continue
        predictions = run["predictions"]
        predicted_case_ids = [
            prediction.get("case_id")
            for prediction in predictions
            if isinstance(prediction, dict)
        ]
        if len(predicted_case_ids) != len(set(predicted_case_ids)):
            issues.append(f"runs[{run_index}] predicts a test case more than once")
        if set(predicted_case_ids) != set(test_cases):
            issues.append(f"runs[{run_index}] must cover every test case exactly once")

        for prediction_index, prediction in enumerate(predictions):
            if not isinstance(prediction, dict):
                issues.append(
                    f"runs[{run_index}].predictions[{prediction_index}] must be an object"
                )
                continue
            case_id = prediction.get("case_id")
            ranked = prediction.get("ranked_candidates")
            if case_id not in test_cases or not isinstance(ranked, list):
                continue
            ranked_ids = [
                item.get("candidate_id")
                for item in ranked
                if isinstance(item, dict)
            ]
            ranks = [
                item.get("rank") for item in ranked if isinstance(item, dict)
            ]
            if ranks != list(range(1, len(ranked) + 1)):
                issues.append(
                    f"runs[{run_index}].predictions[{prediction_index}] "
                    "ranks must be consecutive from one"
                )
            expected = test_cases[case_id]
            if (
                len(ranked_ids) != len(set(ranked_ids))
                or set(ranked_ids) != set(expected)
            ):
                issues.append(
                    f"runs[{run_index}].predictions[{prediction_index}] "
                    "does not cover the complete candidate universe"
                )
            probabilities = [
                item.get("probability")
                for item in ranked
                if isinstance(item, dict)
            ]
            if not all(
                isinstance(value, (int, float))
                and not isinstance(value, bool)
                and 0 <= value <= 1
                for value in probabilities
            ):
                issues.append(
                    f"runs[{run_index}].predictions[{prediction_index}] "
                    "probabilities must be numbers between zero and one"
                )
            elif abs(sum(probabilities) - 1.0) > tolerance:
                issues.append(
                    f"runs[{run_index}].predictions[{prediction_index}] "
                    "probabilities must sum to one"
                )
            elif any(
                probabilities[index] < probabilities[index + 1]
                for index in range(len(probabilities) - 1)
            ):
                issues.append(
                    f"runs[{run_index}].predictions[{prediction_index}] "
                    "probabilities must be nonincreasing by rank"
                )
            action = prediction.get("action")
            rank_one_id = ranked_ids[0] if ranked_ids else None
            if (
                action == "predict"
                and prediction.get("selected_candidate_id") != rank_one_id
            ):
                issues.append(
                    f"runs[{run_index}].predictions[{prediction_index}] "
                    "predict action must select rank one candidate"
                )
            if (
                action == "abstain"
                and prediction.get("selected_candidate_id") is not None
            ):
                issues.append(
                    f"runs[{run_index}].predictions[{prediction_index}] "
                    "abstain action must clear selection"
                )
            if action == "abstain" and not isinstance(
                prediction.get("abstention_reason_code"), str
            ):
                issues.append(
                    f"runs[{run_index}].predictions[{prediction_index}] "
                    "abstain action requires a reason code"
                )
            leakage = prediction.get("leakage_assessment")
            if (
                isinstance(leakage, dict)
                and leakage.get("status") == "confirmed"
                and leakage.get("disposition") == "include"
            ):
                issues.append(
                    f"runs[{run_index}].predictions[{prediction_index}] "
                    "confirmed leakage must be excluded or diagnostic only"
                )
            if action == "predict":
                for evidence_name in ("supporting_evidence", "opposing_evidence"):
                    evidence = prediction.get(evidence_name)
                    if not isinstance(evidence, dict) or evidence.get(
                        "status"
                    ) == "not_checked":
                        issues.append(
                            f"runs[{run_index}].predictions[{prediction_index}] "
                            f"{evidence_name} must be checked before prediction"
                        )
                falsification_checks = prediction.get("falsification_checks")
                if not isinstance(falsification_checks, list) or not any(
                    isinstance(check, dict)
                    and check.get("target_candidate_id") == rank_one_id
                    for check in falsification_checks
                ):
                    issues.append(
                        f"runs[{run_index}].predictions[{prediction_index}] "
                        "requires a rank one falsification check"
                    )
    return issues


def _validate_run_independence(data: dict[str, object]) -> list[str]:
    runs = data.get("runs")
    if not isinstance(runs, list):
        return []
    execution_ids = [
        run.get("execution_id") for run in runs if isinstance(run, dict)
    ]
    issues: list[str] = []
    if len(execution_ids) != len(set(execution_ids)):
        issues.append("runs execution_id must be unique")
    if (
        sum(
            isinstance(run, dict) and run.get("role") == "primary"
            for run in runs
        )
        != 1
    ):
        issues.append("experiment requires exactly one primary run")
    rerun_roles = {
        "independent_rerun",
        "execution_rerun",
        "model_independent_rerun",
    }
    if not any(
        isinstance(run, dict) and run.get("role") in rerun_roles for run in runs
    ):
        issues.append("experiment requires at least one independent rerun")
    primary_model_families = {
        run.get("model_family")
        for run in runs
        if isinstance(run, dict)
        and run.get("role") == "primary"
        and isinstance(run.get("model_family"), str)
    }
    primary_model_ids = {
        run.get("model_id")
        for run in runs
        if isinstance(run, dict)
        and run.get("role") == "primary"
        and isinstance(run.get("model_id"), str)
    }
    for index, run in enumerate(runs):
        if isinstance(run, dict) and run.get("gold_access") != "sealed_unavailable":
            issues.append(f"runs[{index}] agent gold_access must remain sealed")
        if (
            isinstance(run, dict)
            and run.get("role") in rerun_roles
            and run.get("fresh_context") is not True
        ):
            issues.append(
                f"runs[{index}] independent rerun requires fresh_context=true"
            )
        if (
            isinstance(run, dict)
            and run.get("role") in rerun_roles
            and run.get("prior_run_output_access") != "none"
        ):
            issues.append(
                f"runs[{index}] independent rerun cannot read prior run output"
            )
        if (
            isinstance(run, dict)
            and run.get("role") == "model_independent_rerun"
            and run.get("model_family") in primary_model_families
        ):
            issues.append(
                f"runs[{index}] model-independent rerun reuses model family"
            )
        if (
            isinstance(run, dict)
            and run.get("role") == "model_independent_rerun"
            and run.get("model_id") in primary_model_ids
        ):
            issues.append(
                f"runs[{index}] model-independent rerun reuses model id"
            )
    return issues


def _validate_adjudication(data: dict[str, object]) -> list[str]:
    adjudication = data.get("adjudication")
    if not isinstance(adjudication, dict):
        return ["adjudication must be an object"]
    decisions = adjudication.get("case_decisions")
    if not isinstance(decisions, list):
        return ["adjudication.case_decisions must be a list"]
    threshold: float | None = None
    threshold_status: object = None
    minimum_effective_cases: object = None
    effective_case_count: object = None
    benchmark = data.get("benchmark")
    if isinstance(benchmark, dict):
        calibration = benchmark.get("calibration")
        if isinstance(calibration, dict):
            value = calibration.get("threshold")
            threshold_status = calibration.get("threshold_status")
            minimum_effective_cases = calibration.get("minimum_effective_cases")
            effective_case_count = calibration.get("effective_case_count")
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                threshold = float(value)
    issues: list[str] = []
    test_cases, case_issues = _test_case_candidates(data)
    issues.extend(case_issues)
    benchmark = data.get("benchmark")
    case_records = {}
    if isinstance(benchmark, dict) and isinstance(benchmark.get("cases"), list):
        case_records = {
            case.get("case_id"): case
            for case in benchmark["cases"]
            if isinstance(case, dict) and isinstance(case.get("case_id"), str)
        }
    decision_case_ids = {
        decision.get("case_id")
        for decision in decisions
        if isinstance(decision, dict)
    }
    if len(decision_case_ids) != len(decisions):
        issues.append("adjudication case_id must be unique")
    if decision_case_ids != set(test_cases):
        issues.append("adjudication must cover every test case exactly once")
    if adjudication.get("gold_access") != "sealed_unavailable":
        issues.append("adjudicator gold_access must remain sealed")

    runs = data.get("runs")
    run_ids = {
        run.get("run_id")
        for run in runs
        if isinstance(runs, list)
        and isinstance(run, dict)
        and isinstance(run.get("run_id"), str)
    } if isinstance(runs, list) else set()
    input_run_ids = adjudication.get("input_run_ids")
    if not isinstance(input_run_ids, list) or set(input_run_ids) != run_ids:
        issues.append("adjudication input_run_ids must bind every locked run")
    run_selections: dict[str, set[object]] = {}
    if isinstance(runs, list):
        for run in runs:
            if not isinstance(run, dict) or not isinstance(
                run.get("predictions"), list
            ):
                continue
            for prediction in run["predictions"]:
                if not isinstance(prediction, dict):
                    continue
                case_id = prediction.get("case_id")
                if isinstance(case_id, str):
                    selection = (
                        prediction.get("selected_candidate_id")
                        if prediction.get("action") == "predict"
                        else "__abstain__"
                    )
                    run_selections.setdefault(case_id, set()).add(selection)
    for case_id, selections in run_selections.items():
        if len(selections) > 1 and case_id not in decision_case_ids:
            issues.append(f"disagreement case missing adjudication: {case_id}")
    for index, decision in enumerate(decisions):
        if not isinstance(decision, dict):
            issues.append(f"adjudication.case_decisions[{index}] must be an object")
            continue
        if (
            decision.get("ood_status") == "out_of_calibration_domain"
            and decision.get("decision") != "abstain"
        ):
            issues.append(
                f"adjudication.case_decisions[{index}] "
                "out-of-domain decision must abstain"
            )
        if decision.get("ood_status") == "out_of_calibration_domain" and (
            decision.get("probability") is not None
            or decision.get("probability_lower_bound") is not None
        ):
            issues.append(
                f"adjudication.case_decisions[{index}] "
                "out-of-domain decision must clear probability"
            )
        case_id = decision.get("case_id")
        selected_candidate_id = decision.get("selected_candidate_id")
        if (
            case_id in test_cases
            and selected_candidate_id is not None
            and selected_candidate_id not in test_cases[case_id]
        ):
            issues.append(
                f"adjudication.case_decisions[{index}] selected candidate is "
                "outside the case candidate universe"
            )
        if decision.get("delivery_status") == "ai_adjudicated_candidate":
            if decision.get("decision") != "predict":
                issues.append(
                    f"adjudication.case_decisions[{index}] "
                    "delivery requires a predict decision"
                )
            if decision.get("ood_status") != "in_domain":
                issues.append(
                    f"adjudication.case_decisions[{index}] "
                    "out-of-domain candidate delivery is forbidden"
                )
            calibration = (
                benchmark.get("calibration")
                if isinstance(benchmark, dict)
                else None
            )
            if threshold_status != "scorer_derived_supported":
                issues.append(
                    f"adjudication.case_decisions[{index}] "
                    "calibration does not support delivery"
                )
            if (
                not isinstance(calibration, dict)
                or calibration.get("eligibility_scope") != "clean_holdout"
                or calibration.get("derivation_status")
                != "isolated_scorer_verified"
                or not isinstance(calibration.get("artifact_ref"), dict)
                or calibration["artifact_ref"].get("review_status") != "verified"
                or not isinstance(
                    calibration.get("selective_precision_lower_bound"),
                    (int, float),
                )
                or calibration.get("selective_precision_lower_bound", 0)
                < calibration.get("target_selective_precision", 1)
            ):
                issues.append(
                    f"adjudication.case_decisions[{index}] calibration artifact "
                    "is not independently verified"
                )
            if (
                not isinstance(minimum_effective_cases, int)
                or isinstance(minimum_effective_cases, bool)
                or not isinstance(effective_case_count, int)
                or isinstance(effective_case_count, bool)
                or effective_case_count < minimum_effective_cases
            ):
                issues.append(
                    f"adjudication.case_decisions[{index}] calibration "
                    "effective sample is below minimum"
                )
            lower_bound = decision.get("probability_lower_bound")
            if (
                threshold is None
                or not isinstance(lower_bound, (int, float))
                or isinstance(lower_bound, bool)
                or lower_bound < threshold
            ):
                issues.append(
                    f"adjudication.case_decisions[{index}] probability "
                    "lower bound is below calibrated threshold"
                )
            blockers = decision.get("evidence_blockers")
            if not isinstance(blockers, list) or blockers:
                issues.append(
                    f"adjudication.case_decisions[{index}] "
                    "candidate delivery has evidence blockers"
                )
            if decision.get("hard_opposition") is not False:
                issues.append(
                    f"adjudication.case_decisions[{index}] "
                    "candidate delivery has hard opposition"
                )
            case_record = case_records.get(case_id)
            if (
                not isinstance(case_record, dict)
                or case_record.get("benchmark_eligibility")
                != "clean_holdout_eligible"
            ):
                issues.append(
                    f"adjudication.case_decisions[{index}] "
                    "candidate case is not clean-holdout eligible"
                )
            package = data.get("human_delivery_package")
            if (
                not isinstance(package, dict)
                or package.get("status") != "complete"
                or package.get("rights_review_status") != "complete"
                or package.get("content_review_status") != "complete"
                or any(
                    isinstance(item, dict) and item.get("blocking") is True
                    for item in package.get("missing_items", [])
                )
            ):
                issues.append(
                    f"adjudication.case_decisions[{index}] "
                    "candidate requires a complete human delivery package"
                )
            sealed_gold = (
                benchmark.get("sealed_gold")
                if isinstance(benchmark, dict)
                else None
            )
            if (
                not isinstance(sealed_gold, dict)
                or sealed_gold.get("storage_class") != "external_isolated_scorer"
                or sealed_gold.get("unseal_status")
                != "scorer_only_unsealed_retired"
            ):
                issues.append(
                    f"adjudication.case_decisions[{index}] candidate delivery "
                    "requires an external isolated scorer"
                )
            if not isinstance(runs, list) or not any(
                isinstance(run, dict)
                and run.get("role") == "model_independent_rerun"
                and run.get("independence_tier") == "model_independent"
                for run in runs
            ):
                issues.append(
                    f"adjudication.case_decisions[{index}] candidate delivery "
                    "requires a model-independent rerun"
                )
            if isinstance(runs, list):
                for run_index, run in enumerate(runs):
                    if not isinstance(run, dict):
                        continue
                    for prediction in run.get("predictions", []):
                        if not isinstance(prediction, dict) or prediction.get(
                            "case_id"
                        ) != case_id:
                            continue
                        if (
                            prediction.get("action") != "predict"
                            or prediction.get("selected_candidate_id")
                            != selected_candidate_id
                        ):
                            issues.append(
                                f"adjudication.case_decisions[{index}] "
                                f"delivery disagrees with locked run {run_index}"
                            )
            evidence_families: set[str] = set()
            evidence_source_ancestors: set[str] = set()
            if isinstance(runs, list):
                for run in runs:
                    if not isinstance(run, dict):
                        continue
                    for prediction in run.get("predictions", []):
                        if not isinstance(prediction, dict) or prediction.get(
                            "case_id"
                        ) != case_id:
                            continue
                        supporting = prediction.get("supporting_evidence")
                        if not isinstance(supporting, dict):
                            continue
                        for item in supporting.get("items", []):
                            if not isinstance(item, dict):
                                continue
                            if (
                                item.get("dependency_review_status") == "reviewed"
                                and item.get("allowed_delivery_form") != "withhold"
                                and item.get("rights_status")
                                in {"verified_redistributable", "research_use_only"}
                                and isinstance(item.get("evidence_family_id"), str)
                            ):
                                evidence_families.add(item["evidence_family_id"])
                                source_ancestor_id = item.get("source_ancestor_id")
                                if isinstance(source_ancestor_id, str):
                                    evidence_source_ancestors.add(source_ancestor_id)
            if len(evidence_families) < 2:
                issues.append(
                    f"adjudication.case_decisions[{index}] candidate delivery "
                    "requires two independent evidence families"
                )
            if len(evidence_source_ancestors) < 2:
                issues.append(
                    f"adjudication.case_decisions[{index}] candidate delivery "
                    "requires two independent source ancestors"
                )
            if (
                adjudication.get("status") != "completed"
                or not isinstance(adjudication.get("completed_at"), str)
                or not isinstance(adjudication.get("output_lock_sha256"), str)
            ):
                issues.append(
                    f"adjudication.case_decisions[{index}] "
                    "delivery requires completed locked adjudication"
                )
            probability = decision.get("probability")
            if (
                not isinstance(probability, (int, float))
                or isinstance(probability, bool)
                or not isinstance(lower_bound, (int, float))
                or isinstance(lower_bound, bool)
                or lower_bound > probability
            ):
                issues.append(
                    f"adjudication.case_decisions[{index}] "
                    "delivery probability interval is invalid"
                )
            evaluation = data.get("evaluation")
            if (
                not isinstance(evaluation, dict)
                or evaluation.get("status") != "scored"
                or evaluation.get("validity_status") != "valid"
                or evaluation.get("scoring_mode") != "external_isolated"
                or evaluation.get("holdout_status")
                != "retired_after_single_scoring"
                or evaluation.get("score_query_count") != 1
                or not isinstance(evaluation.get("scoring_request_sha256"), str)
                or not isinstance(evaluation.get("scoring_receipt"), dict)
                or evaluation["scoring_receipt"].get("review_status")
                != "verified"
                or not isinstance(evaluation.get("metric_sets"), list)
                or not evaluation.get("metric_sets")
            ):
                issues.append(
                    f"adjudication.case_decisions[{index}] "
                    "delivery requires a scored valid evaluation"
                )
            if (
                not isinstance(evaluation, dict)
                or not isinstance(sealed_gold, dict)
                or evaluation.get("sealed_gold_commitment_ref")
                != sealed_gold.get("gold_key_id")
            ):
                issues.append(
                    f"adjudication.case_decisions[{index}] "
                    "evaluation does not reference sealed gold"
                )
            metric_sets = (
                evaluation.get("metric_sets")
                if isinstance(evaluation, dict)
                else None
            )
            metric_run_ids = (
                [
                    metric_set.get("run_id")
                    for metric_set in metric_sets
                    if isinstance(metric_set, dict)
                ]
                if isinstance(metric_sets, list)
                else []
            )
            if (
                len(metric_run_ids) != len(set(metric_run_ids))
                or set(metric_run_ids) != run_ids
            ):
                issues.append(
                    f"adjudication.case_decisions[{index}] "
                    "metric sets must bind every locked run"
                )
            protocol = data.get("protocol")
            leakage_controls = (
                protocol.get("leakage_controls")
                if isinstance(protocol, dict)
                else None
            )
            clean_protocol = (
                isinstance(leakage_controls, dict)
                and leakage_controls.get("model_training_knowledge")
                == "documented"
            )
            clean_runs = isinstance(runs, list) and all(
                isinstance(run, dict)
                and run.get("training_knowledge") == "documented"
                for run in runs
            )
            case_leakage_clean = True
            if isinstance(runs, list):
                for run in runs:
                    predictions = (
                        run.get("predictions") if isinstance(run, dict) else None
                    )
                    if not isinstance(predictions, list):
                        continue
                    for prediction in predictions:
                        if (
                            not isinstance(prediction, dict)
                            or prediction.get("case_id") != case_id
                        ):
                            continue
                        leakage = prediction.get("leakage_assessment")
                        if not isinstance(leakage, dict) or (
                            leakage.get("status")
                            in {"suspected", "confirmed", "indeterminate"}
                            or "pretraining_unknown" in leakage.get("types", [])
                        ):
                            case_leakage_clean = False
            if not clean_protocol or not clean_runs or not case_leakage_clean:
                issues.append(
                    f"adjudication.case_decisions[{index}] "
                    "delivery lacks clean holdout eligibility"
                )
    return issues


def _validate_gold_sealing_order(data: dict[str, object]) -> list[str]:
    benchmark = data.get("benchmark")
    runs = data.get("runs")
    if not isinstance(benchmark, dict) or not isinstance(runs, list):
        return []
    sealed_gold = benchmark.get("sealed_gold")
    if not isinstance(sealed_gold, dict):
        return []
    sealed_at = _parse_timestamp(sealed_gold.get("sealed_at"))
    started_times = [
        parsed
        for run in runs
        if isinstance(run, dict)
        for parsed in [_parse_timestamp(run.get("started_at"))]
        if parsed is not None
    ]
    issues: list[str] = []
    if sealed_at is not None and started_times and sealed_at >= min(started_times):
        issues.append("gold must be sealed before first run")
    unsealed_at = _parse_timestamp(sealed_gold.get("unsealed_at"))
    if sealed_gold.get("unseal_status") == "sealed":
        if unsealed_at is not None:
            issues.append("sealed gold cannot have an unsealed_at timestamp")
        return issues
    adjudication = data.get("adjudication")
    completed_at = (
        _parse_timestamp(adjudication.get("completed_at"))
        if isinstance(adjudication, dict)
        else None
    )
    locked_times = [
        parsed
        for run in runs
        if isinstance(run, dict)
        for parsed in [_parse_timestamp(run.get("locked_at"))]
        if parsed is not None
    ]
    required_locks = locked_times + ([completed_at] if completed_at else [])
    if unsealed_at is None or (
        required_locks and unsealed_at <= max(required_locks)
    ):
        issues.append("gold unseal must follow locked adjudication")
    return issues


def validate_experiment(
    data: object,
    path: Path | None = None,
    root: Path | None = None,
) -> list[str]:
    """Return validation issues for one public experiment record."""

    if not isinstance(data, dict):
        return ["<memory> must be a JSON object"]

    issues = _validate_public_schema(data)
    missing = sorted(TOP_LEVEL_FIELDS.difference(data))
    if missing:
        issues.append(f"missing top-level fields: {', '.join(missing)}")
    if path is not None and root is not None:
        try:
            relative = path.relative_to(root)
        except ValueError:
            relative = path
        if relative.parts and relative.parts[0] == "research":
            issues.append("experiment record must not be under root research/")
    unknown = sorted(set(data).difference(TOP_LEVEL_FIELDS))
    if unknown:
        issues.append(f"unknown top-level fields: {', '.join(unknown)}")
    if data.get("schema_version") != "2.0.0":
        issues.append("schema_version must be 2.0.0")
    if data.get("record_type") != "ai_agent_candidate_benchmark_experiment":
        issues.append("record_type is not an AI Agent benchmark experiment")
    if data.get("research_boundary") != "benchmark_experiment_not_scholarship":
        issues.append(
            "research_boundary must be benchmark_experiment_not_scholarship"
        )
    caution = str(data.get("caution", "")).lower()
    if (
        "not a decipherment result" not in caution
        or "not published scholarship" not in caution
    ):
        issues.append("caution must state the research boundary")
    issues.extend(_find_forbidden_gold_keys(data))
    issues.extend(_validate_family_splits(data))
    issues.extend(_validate_case_identifiers(data))
    benchmark = data.get("benchmark")
    if isinstance(benchmark, dict):
        expected_manifest = _case_candidate_manifest_sha256(benchmark)
        sealed_gold = benchmark.get("sealed_gold")
        if (
            expected_manifest is not None
            and isinstance(sealed_gold, dict)
            and sealed_gold.get("case_candidate_manifest_sha256")
            != expected_manifest
        ):
            issues.append(
                "sealed gold case_candidate_manifest_sha256 does not match cases"
            )
    issues.extend(_validate_prediction_universes(data))
    issues.extend(_validate_run_independence(data))
    issues.extend(_validate_adjudication(data))
    issues.extend(_validate_gold_sealing_order(data))
    return issues


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _private_path_is_external_or_ignored(path: Path, root: Path) -> bool:
    try:
        relative = path.resolve().relative_to(root.resolve())
    except ValueError:
        return True
    completed = subprocess.run(
        ["git", "check-ignore", "--quiet", "--", str(relative)],
        cwd=root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return completed.returncode == 0


def compute_run_metrics(
    data: dict[str, object],
    gold_labels: dict[str, str],
    run_id: str,
) -> dict[str, int | float | None]:
    """Recompute preregistered metrics for one locked run."""

    runs = data.get("runs")
    if not isinstance(runs, list):
        raise ValueError("runs must be a list")
    selected_run = next(
        (
            run
            for run in runs
            if isinstance(run, dict) and run.get("run_id") == run_id
        ),
        None,
    )
    if not isinstance(selected_run, dict) or not isinstance(
        selected_run.get("predictions"), list
    ):
        raise ValueError(f"run not found: {run_id}")
    if not selected_run["predictions"]:
        raise ValueError("at least one test case is required for metrics")

    probability_floor = 1e-15
    bin_count = 10
    protocol = data.get("protocol")
    if isinstance(protocol, dict):
        metric_policy = protocol.get("metric_policy")
        if isinstance(metric_policy, dict):
            floor_value = metric_policy.get("log_loss_probability_floor")
            bins_value = metric_policy.get("ece_bin_count")
            if isinstance(floor_value, (int, float)) and not isinstance(
                floor_value, bool
            ):
                probability_floor = float(floor_value)
            if isinstance(bins_value, int) and not isinstance(bins_value, bool):
                bin_count = bins_value

    brier_values: list[float] = []
    log_losses: list[float] = []
    top1_rows: list[tuple[float, int]] = []
    covered_errors: list[int] = []
    abstained_count = 0
    for prediction in selected_run["predictions"]:
        if not isinstance(prediction, dict):
            raise ValueError("prediction must be an object")
        case_id = prediction.get("case_id")
        if not isinstance(case_id, str) or case_id not in gold_labels:
            raise ValueError(f"gold label missing for case: {case_id}")
        ranked = prediction.get("ranked_candidates")
        if not isinstance(ranked, list) or not ranked:
            raise ValueError(f"ranked candidates missing for case: {case_id}")
        distribution = {
            item["candidate_id"]: float(item["probability"])
            for item in ranked
            if isinstance(item, dict)
        }
        gold_candidate_id = gold_labels[case_id]
        if gold_candidate_id not in distribution:
            raise ValueError(f"gold candidate outside universe for case: {case_id}")
        brier_values.append(
            sum(
                (probability - (1.0 if candidate_id == gold_candidate_id else 0.0))
                ** 2
                for candidate_id, probability in distribution.items()
            )
        )
        log_losses.append(
            -math.log(max(distribution[gold_candidate_id], probability_floor))
        )
        rank_one = ranked[0]
        confidence = float(rank_one["probability"])
        correct = int(rank_one["candidate_id"] == gold_candidate_id)
        top1_rows.append((confidence, correct))
        if prediction.get("action") == "abstain":
            abstained_count += 1
        else:
            covered_errors.append(1 - correct)

    ece = 0.0
    total = len(top1_rows)
    for bin_index in range(bin_count):
        lower = bin_index / bin_count
        upper = (bin_index + 1) / bin_count
        rows = [
            (confidence, correct)
            for confidence, correct in top1_rows
            if lower <= confidence < upper
            or (bin_index == bin_count - 1 and confidence == 1.0)
        ]
        if not rows:
            continue
        mean_confidence = sum(row[0] for row in rows) / len(rows)
        mean_accuracy = sum(row[1] for row in rows) / len(rows)
        ece += len(rows) / total * abs(mean_accuracy - mean_confidence)

    covered_count = len(covered_errors)
    return {
        "test_case_count": total,
        "abstained_count": abstained_count,
        "covered_count": covered_count,
        "brier_multiclass_mean": sum(brier_values) / total,
        "log_loss_nats_mean": sum(log_losses) / total,
        "ece_top1": ece,
        "coverage": covered_count / total,
        "selective_risk": (
            sum(covered_errors) / covered_count if covered_count else None
        ),
    }


def compare_claimed_metrics(
    data: dict[str, object],
    recomputed: dict[str, dict[str, int | float | None]],
    *,
    tolerance: float = 1e-12,
) -> list[str]:
    """Compare a scored public record with isolated-scorer results."""

    evaluation = data.get("evaluation")
    if not isinstance(evaluation, dict) or evaluation.get("status") != "scored":
        return []
    metric_sets = evaluation.get("metric_sets")
    if not isinstance(metric_sets, list):
        return ["scored evaluation metric_sets must be a list"]
    metric_ids = [
        metric_set.get("run_id")
        for metric_set in metric_sets
        if isinstance(metric_set, dict)
    ]
    issues: list[str] = []
    if len(metric_ids) != len(set(metric_ids)):
        issues.append("metric set run_id must be unique")
    claimed_by_run = {
        metric_set.get("run_id"): metric_set
        for metric_set in metric_sets
        if isinstance(metric_set, dict)
        and isinstance(metric_set.get("run_id"), str)
    }
    if set(claimed_by_run) != set(recomputed):
        issues.append("scored evaluation metric sets must match scored runs")
    for run_id, expected_metrics in recomputed.items():
        claimed = claimed_by_run.get(run_id)
        if claimed is None:
            issues.append(f"scored evaluation missing metric set for {run_id}")
            continue
        for key, expected in expected_metrics.items():
            actual = claimed.get(key)
            if expected is None:
                matches = actual is None
            elif isinstance(expected, float):
                matches = (
                    isinstance(actual, (int, float))
                    and not isinstance(actual, bool)
                    and abs(float(actual) - expected) <= tolerance
                )
            else:
                matches = actual == expected
            if not matches:
                issues.append(
                    f"claimed metric mismatch for {run_id}.{key}: "
                    f"claimed={actual!r}, recomputed={expected!r}"
                )
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--path",
        default=str(DEFAULT_EXPERIMENT_ROOT),
        help="v2 experiment JSON file or directory",
    )
    parser.add_argument(
        "--gold-path",
        help="ignored private gold payload used by the isolated scorer",
    )
    args = parser.parse_args(argv)

    root = _repo_root()
    target = Path(args.path)
    if not target.is_absolute():
        target = root / target
    paths = discover_experiment_paths(target)
    if not paths:
        print(f"FAIL no v2 benchmark experiment records found under {args.path}")
        return 1

    issues: list[str] = []
    records: list[dict[str, object]] = []
    for path in paths:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            issues.append(f"{path}: invalid JSON: {exc}")
            continue
        if isinstance(data, dict):
            records.append(data)
        issues.extend(validate_experiment(data, path=path, root=root))
    if issues:
        print("FAIL AI Agent benchmark experiments")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print(f"PASS AI Agent benchmark experiments ({len(paths)} files)")
    if not args.gold_path:
        print("METRICS_NOT_RECOMPUTED: no private gold payload was supplied")
        return 0

    if len(records) != 1:
        print("FAIL private gold scoring requires exactly one experiment record")
        return 1
    gold_path = Path(args.gold_path)
    if not gold_path.is_absolute():
        gold_path = root / gold_path
    if not _private_path_is_external_or_ignored(gold_path, root):
        print(
            "FAIL private gold path must be outside the repository or Git-ignored"
        )
        return 1
    try:
        private_gold = json.loads(gold_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL invalid private gold payload: {exc}")
        return 1
    if not isinstance(private_gold, dict):
        print("FAIL private gold payload must be an object")
        return 1
    key_hex = private_gold.get("commitment_key_hex")
    labels = private_gold.get("labels")
    required_private_fields = {
        "benchmark_id",
        "benchmark_version",
        "gold_key_id",
        "case_candidate_manifest_sha256",
        "protocol_sha256",
        "labels",
        "commitment_key_hex",
    }
    if not required_private_fields.issubset(private_gold):
        print("FAIL private gold payload is missing binding fields")
        return 1
    label_case_ids = [
        item.get("case_id")
        for item in labels
        if isinstance(item, dict) and isinstance(item.get("case_id"), str)
    ]
    if len(label_case_ids) != len(set(label_case_ids)):
        print("FAIL gold labels must be unique by case")
        return 1
    committed_payload = {
        "benchmark_id": private_gold.get("benchmark_id"),
        "benchmark_version": private_gold.get("benchmark_version"),
        "gold_key_id": private_gold.get("gold_key_id"),
        "case_candidate_manifest_sha256": private_gold.get(
            "case_candidate_manifest_sha256"
        ),
        "protocol_sha256": private_gold.get("protocol_sha256"),
        "labels": labels,
    }
    message = json.dumps(
        committed_payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    try:
        calculated_commitment = hmac.new(
            bytes.fromhex(key_hex), message, hashlib.sha256
        ).hexdigest()
    except ValueError:
        print("FAIL private gold commitment key is not valid hexadecimal")
        return 1
    benchmark = records[0].get("benchmark")
    sealed_gold = benchmark.get("sealed_gold") if isinstance(benchmark, dict) else None
    if (
        not isinstance(benchmark, dict)
        or private_gold.get("benchmark_id") != benchmark.get("benchmark_id")
        or private_gold.get("benchmark_version")
        != benchmark.get("benchmark_version")
        or not isinstance(sealed_gold, dict)
        or private_gold.get("gold_key_id") != sealed_gold.get("gold_key_id")
        or private_gold.get("case_candidate_manifest_sha256")
        != sealed_gold.get("case_candidate_manifest_sha256")
        or private_gold.get("protocol_sha256")
        != (
            records[0].get("protocol", {}).get("protocol_sha256")
            if isinstance(records[0].get("protocol"), dict)
            else None
        )
    ):
        print("FAIL private gold does not bind to experiment benchmark")
        return 1
    expected_commitment = (
        sealed_gold.get("commitment") if isinstance(sealed_gold, dict) else None
    )
    if not isinstance(expected_commitment, str) or not hmac.compare_digest(
        calculated_commitment, expected_commitment
    ):
        print("FAIL private gold payload does not match sealed commitment")
        return 1
    gold_labels = {
        item.get("case_id"): item.get("gold_candidate_id")
        for item in labels
        if isinstance(item, dict)
        and isinstance(item.get("case_id"), str)
        and isinstance(item.get("gold_candidate_id"), str)
    }
    benchmark_cases = (
        benchmark.get("cases") if isinstance(benchmark, dict) else None
    )
    test_candidate_universes = {
        case.get("case_id"): case.get("candidate_ids")
        for case in benchmark_cases
        if isinstance(case, dict)
        and case.get("split") == "test"
        and isinstance(case.get("case_id"), str)
    } if isinstance(benchmark_cases, list) else {}
    if set(label_case_ids) != set(test_candidate_universes):
        print("FAIL gold labels must cover every test case exactly once")
        return 1
    for case_id, candidate_id in gold_labels.items():
        candidates = test_candidate_universes.get(case_id)
        if not isinstance(candidates, list) or candidate_id not in candidates:
            print(f"FAIL gold candidate is outside case universe: {case_id}")
            return 1
    run_metrics = {
        run["run_id"]: compute_run_metrics(records[0], gold_labels, run["run_id"])
        for run in records[0].get("runs", [])
        if isinstance(run, dict) and isinstance(run.get("run_id"), str)
    }
    metric_issues = compare_claimed_metrics(records[0], run_metrics)
    if metric_issues:
        print("FAIL claimed metrics do not match isolated recomputation")
        for issue in metric_issues:
            print(f"- {issue}")
        return 1
    storage_class = (
        sealed_gold.get("storage_class")
        if isinstance(sealed_gold, dict)
        else None
    )
    metric_status = (
        "METRICS_RECOMPUTED"
        if storage_class == "external_isolated_scorer"
        else "METRICS_RECOMPUTED_DIAGNOSTIC"
    )
    print(
        metric_status
        + " "
        + json.dumps(run_metrics, ensure_ascii=False, sort_keys=True)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
