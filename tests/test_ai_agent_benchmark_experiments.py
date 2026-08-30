from __future__ import annotations

import copy
import contextlib
import hashlib
import hmac
import io
import json
import tempfile
import unittest
from pathlib import Path

from tools.validation.validate_ai_agent_benchmark_experiments import (
    compare_claimed_metrics,
    compute_run_metrics,
    discover_experiment_paths,
    main,
    validate_experiment,
)


def canonical_experiment() -> dict[str, object]:
    sha_a = "a" * 64
    sha_b = "b" * 64
    sha_c = "c" * 64
    evidence_item = {
        "evidence_ref_id": "evidence-000001",
        "evidence_family_id": "evidence-family-visual-000001",
        "target_candidate_id": "candidate-a",
        "source_id": "src-hust-obc",
        "source_ancestor_id": "src-hust-obc",
        "route_path": "corpus/example/10_source-evidence-dossier.md",
        "locator": "plate 1",
        "snapshot_sha256": sha_a,
        "rights_status": "research_use_only",
        "allowed_delivery_form": "metadata_only",
        "risk_note": "Synthetic fixture route; do not redistribute an asset.",
        "large_source_register_ref": None,
        "dependency_review_status": "reviewed",
        "note": "Controlled fixture evidence.",
    }
    prediction = {
        "case_id": "case-test-000001",
        "ranked_candidates": [
            {"rank": 1, "candidate_id": "candidate-a", "probability": 0.8},
            {"rank": 2, "candidate_id": "candidate-b", "probability": 0.2},
            {
                "rank": 3,
                "candidate_id": "unknown_or_other",
                "probability": 0.0,
            },
        ],
        "action": "predict",
        "selected_candidate_id": "candidate-a",
        "abstention_reason_code": None,
        "supporting_evidence": {
            "status": "collected",
            "items": [evidence_item],
            "search_note": "Primary dossier checked.",
        },
        "opposing_evidence": {
            "status": "searched_none_found",
            "items": [],
            "search_note": "Counter-source route searched.",
        },
        "falsification_checks": [
            {
                "check_id": "falsifier-000001",
                "target_candidate_id": "candidate-a",
                "preregistered_at": "2026-08-09T00:00:00Z",
                "falsifier": "counter-context-agent",
                "method": "Search incompatible inscription contexts.",
                "outcome": "not_triggered",
                "evidence_refs": ["evidence-000001"],
                "note": "No hard contradiction in the frozen fixture.",
            }
        ],
        "leakage_assessment": {
            "status": "screened_no_known_leakage",
            "types": ["pretraining_unknown"],
            "audit_refs": ["audit-000001"],
            "disposition": "include",
        },
    }

    def run(
        run_id: str,
        role: str,
        execution_id: str,
        agent_id: str,
        completed_at: str,
        locked_at: str,
    ) -> dict[str, object]:
        return {
            "run_id": run_id,
            "role": role,
            "execution_id": execution_id,
            "agent_id": agent_id,
            "model_id": "test-model-1",
            "model_family": "test-family",
            "independence_tier": (
                "primary" if role == "primary" else "execution_only"
            ),
            "independence_axes": ["agent_context"],
            "shared_ancestor_ids": ["model-family:test-family"],
            "training_knowledge": "unknown",
            "random_seed": 7,
            "fresh_context": True,
            "prior_run_output_access": "none",
            "gold_access": "sealed_unavailable",
            "prompt_manifest_sha256": sha_a,
            "tool_manifest_sha256": sha_b,
            "evidence_snapshot_sha256": sha_c,
            "retrieval_snapshot_sha256": sha_a,
            "started_at": "2026-08-09T00:01:00Z",
            "completed_at": completed_at,
            "locked_at": locked_at,
            "prediction_lock_sha256": sha_b,
            "predictions": [copy.deepcopy(prediction)],
        }

    def case(
        case_id: str,
        family_id: str,
        split: str,
        case_type: str,
        input_sha256: str,
        pack_id: str,
        pack_sha256: str,
    ) -> dict[str, object]:
        return {
            "case_id": case_id,
            "family_id": family_id,
            "split": split,
            "case_type": case_type,
            "blind_alias": f"blind-{case_id}",
            "input_ref": f"ignored/{case_id}-input",
            "input_sha256": input_sha256,
            "evidence_cutoff_at": "2026-08-08T00:00:00Z",
            "candidate_ids": [
                "candidate-a",
                "candidate-b",
                "unknown_or_other",
            ],
            "candidate_universe_status": "includes_unknown_or_other",
            "evidence_pack_snapshot": {
                "evidence_pack_id": pack_id,
                "path": "doc/public/user_research/example.json",
                "sha256": pack_sha256,
                "status": "hypothesis",
            },
            "source_checksums": [
                {
                    "source_id": "src-hust-obc",
                    "source_ancestor_id": "src-hust-obc",
                    "derivative_family_id": family_id,
                    "snapshot_sha256": input_sha256,
                    "rights_status": "research_use_only",
                    "allowed_delivery_form": "metadata_only",
                    "risk_note": "Synthetic fixture route.",
                    "large_source_register_ref": None,
                    "dependency_review_status": "reviewed",
                }
            ],
            "training_cutoff_evidence": {
                "artifact_id": f"cutoff-{case_id}",
                "path": "ignored/training-cutoff.txt",
                "sha256": sha_a,
                "review_status": "pending",
                "note": "Synthetic fixture has no clean training cutoff.",
            },
            "dependency_manifest": {
                "artifact_id": f"dependency-{case_id}",
                "path": "ignored/dependency-manifest.json",
                "sha256": sha_b,
                "review_status": "verified",
                "note": "Synthetic source and image lineage manifest.",
            },
            "pretraining_exposure": "unknown",
            "benchmark_eligibility": "pretraining_exposure_unknown",
        }

    record = {
        "schema_version": "2.0.0",
        "record_type": "ai_agent_candidate_benchmark_experiment",
        "experiment_id": "ai-bench-exp-000001",
        "status": "adjudicated",
        "research_boundary": "benchmark_experiment_not_scholarship",
        "benchmark": {
            "benchmark_id": "ai-bench-000001",
            "benchmark_version": "1.0.0",
            "task_type": "closed_candidate_ranking",
            "cases": [
                case(
                    "case-calibration-000001",
                    "family-calibration-000001",
                    "calibration",
                    "masked_known_reading",
                    sha_a,
                    "hust-obc-evidence-pack-000001",
                    sha_b,
                ),
                case(
                    "case-test-000001",
                    "family-test-000001",
                    "test",
                    "historically_disputed",
                    sha_b,
                    "hust-obc-evidence-pack-000002",
                    sha_c,
                ),
                case(
                    "case-negative-000001",
                    "family-negative-000001",
                    "development",
                    "null_or_negative_control",
                    sha_c,
                    "hust-obc-evidence-pack-000003",
                    sha_a,
                ),
                case(
                    "case-challenge-000001",
                    "family-challenge-000001",
                    "challenge",
                    "hard_challenge",
                    sha_a,
                    "hust-obc-evidence-pack-000004",
                    sha_b,
                ),
            ],
            "family_split": {
                "unit": "family_id",
                "cross_split_overlap": "forbidden",
                "family_definition": "Same object and derivative image family.",
                "family_manifest_sha256": sha_c,
                "locked_at": "2026-08-09T00:00:00Z",
            },
            "sealed_gold": {
                "gold_key_id": "gold-key-000001",
                "commitment_scheme": "hmac-sha256",
                "commitment": sha_a,
                "storage_class": "ignored_local_diagnostic",
                "case_candidate_manifest_sha256": sha_b,
                "sealed_at": "2026-08-09T00:00:00Z",
                "agent_access": "none",
                "unseal_status": "sealed",
                "unsealed_at": None,
                "scorer_only": True,
                "score_query_limit": 1,
            },
            "calibration": {
                "domain_id": "closed-known-readings-v1",
                "domain_definition": "Frozen known-answer cases from one task family.",
                "method": "isotonic",
                "eligibility_scope": "diagnostic_only",
                "derivation_status": "not_available",
                "artifact_ref": None,
                "prediction_lock_sha256": sha_c,
                "confidence_level": 0.95,
                "target_selective_precision": 0.9,
                "minimum_effective_cases": 20,
                "effective_case_count": 1,
                "threshold": 0.93,
                "threshold_status": "diagnostic_only",
                "selective_precision_lower_bound": 0.0,
                "family_cluster_count": 1,
                "ood_tests": ["source-family distance", "glyph-density range"],
                "ood_action": "withhold_numeric_probability",
            },
        },
        "protocol": {
            "preregistered_at": "2026-08-09T00:00:00Z",
            "protocol_sha256": sha_a,
            "prompt_manifest_sha256": sha_a,
            "tool_manifest_sha256": sha_b,
            "evidence_snapshot_sha256": sha_c,
            "probability_policy": {
                "complete_candidate_distribution": True,
                "sum_tolerance": 1e-9,
            },
            "abstention_policy": {
                "method": "calibrated-threshold-and-ood",
                "threshold": 0.93,
                "guardrails": ["withhold out-of-domain cases"],
            },
                "leakage_controls": {
                "gold_in_prompt": "forbidden",
                "prior_run_outputs": "forbidden",
                "cross_split_family": "forbidden",
                "allowed_routes": ["frozen evidence snapshot"],
                "blocked_routes": ["gold labels", "peer run outputs"],
                "model_training_knowledge": "not_known",
            },
            "metric_policy": {
                "brier_definition": "multiclass_mean_sum_squared_error",
                "log_loss_base": "natural",
                "log_loss_probability_floor": 1e-15,
                "ece_definition": "top1_equal_width",
                "ece_bin_count": 10,
                "coverage_risk_definition": "covered_top1_error",
            },
            "falsification_policy": {
                "minimum_checks_per_case": 1,
                "must_be_preregistered": True,
            },
        },
        "runs": [
            run(
                "run-primary-000001",
                "primary",
                "execution-000001",
                "hypothesis-agent-1",
                "2026-08-09T00:02:00Z",
                "2026-08-09T00:03:00Z",
            ),
            run(
                "run-rerun-000001",
                "independent_rerun",
                "execution-000002",
                "hypothesis-agent-2",
                "2026-08-09T00:04:00Z",
                "2026-08-09T00:05:00Z",
            ),
        ],
        "adjudication": {
            "status": "completed",
            "input_run_ids": ["run-primary-000001", "run-rerun-000001"],
            "adjudicator_kind": "agent_panel",
            "adjudicator_ids": ["adjudicator-agent-1"],
            "adjudicator_runtimes": [
                {
                    "adjudicator_id": "adjudicator-agent-1",
                    "execution_id": "adjudicator-execution-000001",
                    "model_id": "adjudicator-test-model-1",
                    "model_family": "adjudicator-test-family",
                    "context_id": "adjudicator-context-000001",
                    "fresh_context": True,
                    "prior_run_output_access": "none",
                    "gold_access": "sealed_unavailable",
                    "training_knowledge": "unknown",
                    "input_run_ids": [
                        "run-primary-000001",
                        "run-rerun-000001",
                    ],
                    "evidence_snapshot_sha256": sha_c,
                    "retrieval_snapshot_sha256": sha_a,
                    "tool_manifest_sha256": sha_b,
                    "output_lock_sha256": "d" * 64,
                }
            ],
            "gold_access": "sealed_unavailable",
            "case_decisions": [
                {
                    "case_id": "case-test-000001",
                    "decision": "predict",
                    "delivery_status": "withheld",
                    "selected_candidate_id": "candidate-a",
                    "probability": 0.8,
                    "probability_lower_bound": 0.72,
                    "disagreement_resolved": False,
                    "evidence_blockers": [],
                    "hard_opposition": False,
                    "ood_status": "in_domain",
                    "rationale": "Independent runs agree in the controlled fixture.",
                }
            ],
            "completed_at": "2026-08-09T00:06:00Z",
                    "output_lock_sha256": sha_c,
        },
        "evaluation": {
            "status": "not_scored",
            "validity_status": "pending",
            "scored_at": None,
            "scorer_id": None,
            "scorer_version": None,
            "scoring_mode": None,
            "holdout_status": "sealed",
            "score_query_count": 0,
            "scoring_request_sha256": None,
            "scoring_receipt": None,
            "sealed_gold_commitment_ref": "gold-key-000001",
            "metric_sets": [],
            "excluded_cases": [],
        },
        "review_log": [
            {
                "status": "protocol_locked",
                "note": "Synthetic fixture only; no scholarly claim.",
            }
        ],
        "human_delivery_package": {
            "package_id": "human-delivery-000001",
            "status": "incomplete",
            "path": "doc/public/user_research/example-human-package",
            "sha256": sha_a,
            "languages": ["en", "zh-CN"],
            "object_dossier_paths": ["corpus/example/001_object-dossier.md"],
            "inscription_context_paths": ["corpus/example/002_inscription.md"],
            "source_evidence_paths": ["corpus/example/10_source-evidence-dossier.md"],
            "adjudication_memo_path": "ignored/adjudication-memo.md",
            "dependency_graph_path": "ignored/dependency-graph.json",
            "claim_evidence_matrix_path": "ignored/claim-evidence-matrix.csv",
            "rights_review_status": "pending",
            "content_review_status": "pending",
            "missing_items": [
                {
                    "question": "Which public plate route confirms the context?",
                    "next_source": "IHP plate catalogue",
                    "blocking": True,
                }
            ],
        },
        "caution": (
            "This is not a decipherment result and not published scholarship."
        ),
        "created_at": "2026-08-09T00:00:00Z",
        "updated_at": "2026-08-09T00:06:00Z",
    }
    from tools.validation.validate_ai_agent_benchmark_experiments import (
        _case_candidate_manifest_sha256,
    )

    record["benchmark"]["sealed_gold"]["case_candidate_manifest_sha256"] = (
        _case_candidate_manifest_sha256(record["benchmark"])
    )
    return record


def attach_private_gold(
    record: dict[str, object],
    labels: dict[str, str],
    key_hex: str = "11" * 32,
) -> dict[str, object]:
    committed_payload = {
        "benchmark_id": record["benchmark"]["benchmark_id"],
        "benchmark_version": record["benchmark"]["benchmark_version"],
        "gold_key_id": record["benchmark"]["sealed_gold"]["gold_key_id"],
        "case_candidate_manifest_sha256": record["benchmark"][
            "sealed_gold"
        ]["case_candidate_manifest_sha256"],
        "protocol_sha256": record["protocol"]["protocol_sha256"],
        "labels": [
            {"case_id": case_id, "gold_candidate_id": candidate_id}
            for case_id, candidate_id in labels.items()
        ],
    }
    message = json.dumps(
        committed_payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    record["benchmark"]["sealed_gold"]["commitment"] = hmac.new(
        bytes.fromhex(key_hex), message, hashlib.sha256
    ).hexdigest()
    return {**committed_payload, "commitment_key_hex": key_hex}


def complete_candidate_delivery_experiment() -> dict[str, object]:
    record = canonical_experiment()
    test_case = record["benchmark"]["cases"][1]
    test_case["pretraining_exposure"] = "verified_post_training_cutoff"
    test_case["benchmark_eligibility"] = "clean_holdout_eligible"
    test_case["training_cutoff_evidence"]["review_status"] = "verified"
    for run in record["runs"]:
        run["training_knowledge"] = "documented"
        run["predictions"][0]["leakage_assessment"]["types"] = []
    for runtime in record["adjudication"]["adjudicator_runtimes"]:
        runtime["training_knowledge"] = "documented"
    rerun = record["runs"][1]
    rerun["role"] = "model_independent_rerun"
    rerun["independence_tier"] = "model_independent"
    rerun["independence_axes"] = ["agent_context", "model_family"]
    rerun["model_id"] = "independent-test-model-1"
    rerun["model_family"] = "independent-test-family"
    record["protocol"]["leakage_controls"]["model_training_knowledge"] = (
        "documented"
    )
    calibration = record["benchmark"]["calibration"]
    calibration["eligibility_scope"] = "clean_holdout"
    calibration["derivation_status"] = "isolated_scorer_verified"
    calibration["artifact_ref"] = {
        "artifact_id": "calibration-receipt-000001",
        "path": "external/calibration-receipt.json",
        "sha256": "c" * 64,
        "review_status": "verified",
        "note": "Synthetic isolated scorer receipt.",
    }
    calibration["threshold_status"] = "scorer_derived_supported"
    calibration["minimum_effective_cases"] = 1
    calibration["selective_precision_lower_bound"] = 0.95
    record["human_delivery_package"]["status"] = "complete"
    record["human_delivery_package"]["rights_review_status"] = "complete"
    record["human_delivery_package"]["content_review_status"] = "complete"
    record["human_delivery_package"]["missing_items"] = []
    second_evidence = copy.deepcopy(
        record["runs"][0]["predictions"][0]["supporting_evidence"]["items"][0]
    )
    second_evidence["evidence_ref_id"] = "evidence-000002"
    second_evidence["evidence_family_id"] = "evidence-family-context-000001"
    second_evidence["source_id"] = "src-ihp-oracle-rubbings"
    second_evidence["source_ancestor_id"] = "src-ihp-oracle-rubbings"
    for run in record["runs"]:
        run["predictions"][0]["supporting_evidence"]["items"].append(
            copy.deepcopy(second_evidence)
        )
    sealed_gold = record["benchmark"]["sealed_gold"]
    sealed_gold["storage_class"] = "external_isolated_scorer"
    sealed_gold["unseal_status"] = "scorer_only_unsealed_retired"
    sealed_gold["unsealed_at"] = "2026-08-09T00:07:00Z"
    evaluation = record["evaluation"]
    evaluation.update(
        {
            "status": "scored",
            "validity_status": "valid",
            "scored_at": "2026-08-09T00:08:00Z",
            "scorer_id": "external-scorer-000001",
            "scorer_version": "2.0.0",
            "scoring_mode": "external_isolated",
            "holdout_status": "retired_after_single_scoring",
            "score_query_count": 1,
            "scoring_request_sha256": "a" * 64,
            "scoring_receipt": {
                "artifact_id": "scoring-receipt-000001",
                "path": "external/scoring-receipt.json",
                "sha256": "b" * 64,
                "review_status": "verified",
                "note": "Synthetic isolated scorer receipt.",
            },
            "metric_sets": [
                {
                    "run_id": "run-primary-000001",
                    "test_case_count": 1,
                    "abstained_count": 0,
                    "covered_count": 1,
                    "brier_multiclass_mean": 0.08,
                    "log_loss_nats_mean": 0.223143551314,
                    "ece_top1": 0.2,
                    "coverage": 1.0,
                    "selective_risk": 0.0,
                },
                {
                    "run_id": "run-rerun-000001",
                    "test_case_count": 1,
                    "abstained_count": 0,
                    "covered_count": 1,
                    "brier_multiclass_mean": 0.08,
                    "log_loss_nats_mean": 0.223143551314,
                    "ece_top1": 0.2,
                    "coverage": 1.0,
                    "selective_risk": 0.0,
                },
            ],
        }
    )
    decision = record["adjudication"]["case_decisions"][0]
    decision.update(
        {
            "delivery_status": "ai_adjudicated_candidate",
            "probability": 0.96,
            "probability_lower_bound": 0.95,
            "disagreement_resolved": True,
        }
    )
    return record


class BenchmarkExperimentValidationTests(unittest.TestCase):
    def test_v2_schema_preserves_autonomous_candidate_boundary(self) -> None:
        schema_path = (
            Path(__file__).resolve().parents[1]
            / "schemas/007_ai-agent-benchmark-experiment-schema/"
            / "ai-agent-benchmark-experiment-v2.schema.json"
        )

        schema = json.loads(schema_path.read_text(encoding="utf-8"))

        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(schema["properties"]["schema_version"]["const"], "2.0.0")
        self.assertEqual(
            schema["properties"]["research_boundary"]["const"],
            "benchmark_experiment_not_scholarship",
        )
        adjudicator_kinds = schema["$defs"]["adjudication"]["properties"][
            "adjudicator_kind"
        ]["enum"]
        self.assertEqual(adjudicator_kinds, ["ai_agent", "agent_panel"])
        self.assertIn(
            "adjudicator_runtimes",
            schema["$defs"]["adjudication"]["required"],
        )
        self.assertNotIn("commitment_key_hex", schema_path.read_text(encoding="utf-8"))

    def test_valid_adjudicated_experiment_passes(self) -> None:
        self.assertEqual(validate_experiment(canonical_experiment()), [])

    def test_public_record_rejects_embedded_gold_label(self) -> None:
        record = canonical_experiment()
        record["runs"][0]["predictions"][0]["correct_candidate_id"] = (
            "candidate-a"
        )

        issues = validate_experiment(record)

        self.assertTrue(
            any("forbidden public gold key" in issue for issue in issues),
            issues,
        )

    def test_family_cannot_cross_benchmark_splits(self) -> None:
        record = canonical_experiment()
        record["benchmark"]["cases"][1]["family_id"] = (
            "family-calibration-000001"
        )

        issues = validate_experiment(record)

        self.assertTrue(
            any("family_id crosses splits" in issue for issue in issues),
            issues,
        )

    def test_prediction_must_cover_complete_candidate_universe(self) -> None:
        record = canonical_experiment()
        for run in record["runs"]:
            run["predictions"][0]["ranked_candidates"] = [
                {
                    "rank": 1,
                    "candidate_id": "candidate-a",
                    "probability": 1.0,
                }
            ]

        issues = validate_experiment(record)

        self.assertTrue(
            any("candidate universe" in issue for issue in issues),
            issues,
        )

    def test_candidate_probabilities_must_sum_to_one(self) -> None:
        record = canonical_experiment()
        record["runs"][0]["predictions"][0]["ranked_candidates"][1][
            "probability"
        ] = 0.3

        issues = validate_experiment(record)

        self.assertTrue(
            any("probabilities must sum to one" in issue for issue in issues),
            issues,
        )

    def test_candidate_ranks_must_be_consecutive(self) -> None:
        record = canonical_experiment()
        ranked = record["runs"][0]["predictions"][0]["ranked_candidates"]
        ranked[0]["rank"] = 2
        ranked[1]["rank"] = 1

        issues = validate_experiment(record)

        self.assertTrue(
            any("ranks must be consecutive" in issue for issue in issues),
            issues,
        )

    def test_ranked_candidate_probabilities_must_be_nonincreasing(self) -> None:
        record = canonical_experiment()
        ranked = record["runs"][0]["predictions"][0]["ranked_candidates"]
        ranked[0]["probability"] = 0.2
        ranked[1]["probability"] = 0.8

        issues = validate_experiment(record)

        self.assertTrue(
            any("probabilities must be nonincreasing" in issue for issue in issues),
            issues,
        )

    def test_predict_action_must_select_rank_one_candidate(self) -> None:
        record = canonical_experiment()
        record["runs"][0]["predictions"][0]["selected_candidate_id"] = (
            "candidate-b"
        )

        issues = validate_experiment(record)

        self.assertTrue(
            any("predict action must select rank one" in issue for issue in issues),
            issues,
        )

    def test_abstain_action_must_clear_selected_candidate(self) -> None:
        record = canonical_experiment()
        prediction = record["runs"][0]["predictions"][0]
        prediction["action"] = "abstain"
        prediction["abstention_reason_code"] = None

        issues = validate_experiment(record)

        self.assertTrue(
            any("abstain action must clear selection" in issue for issue in issues),
            issues,
        )

    def test_abstain_action_must_name_reason_code(self) -> None:
        record = canonical_experiment()
        prediction = record["runs"][0]["predictions"][0]
        prediction["action"] = "abstain"
        prediction["selected_candidate_id"] = None
        prediction["abstention_reason_code"] = None

        issues = validate_experiment(record)

        self.assertTrue(
            any("abstain action requires a reason code" in issue for issue in issues),
            issues,
        )

    def test_prediction_cannot_leave_opposing_evidence_unchecked(self) -> None:
        record = canonical_experiment()
        opposition = record["runs"][0]["predictions"][0]["opposing_evidence"]
        opposition["status"] = "not_checked"
        opposition["search_note"] = ""

        issues = validate_experiment(record)

        self.assertTrue(
            any("opposing_evidence must be checked" in issue for issue in issues),
            issues,
        )

    def test_prediction_requires_rank_one_falsification_check(self) -> None:
        record = canonical_experiment()
        record["runs"][0]["predictions"][0]["falsification_checks"] = []

        issues = validate_experiment(record)

        self.assertTrue(
            any("rank one falsification check" in issue for issue in issues),
            issues,
        )

    def test_independent_rerun_requires_distinct_execution(self) -> None:
        record = canonical_experiment()
        record["runs"][1]["execution_id"] = "execution-000001"

        issues = validate_experiment(record)

        self.assertTrue(
            any("execution_id must be unique" in issue for issue in issues),
            issues,
        )

    def test_experiment_requires_an_independent_rerun(self) -> None:
        record = canonical_experiment()
        record["runs"] = [record["runs"][0]]

        issues = validate_experiment(record)

        self.assertTrue(
            any("requires at least one independent rerun" in issue for issue in issues),
            issues,
        )

    def test_experiment_requires_exactly_one_primary_run(self) -> None:
        record = canonical_experiment()
        record["runs"][0]["role"] = "independent_rerun"

        issues = validate_experiment(record)

        self.assertTrue(
            any("requires exactly one primary run" in issue for issue in issues),
            issues,
        )

    def test_adjudicator_runtime_must_not_reuse_research_agent(self) -> None:
        record = canonical_experiment()
        record["adjudication"]["adjudicator_runtimes"][0][
            "adjudicator_id"
        ] = "hypothesis-agent-1"
        record["adjudication"]["adjudicator_ids"] = ["hypothesis-agent-1"]

        issues = validate_experiment(record)

        self.assertTrue(
            any(
                "must not reuse a research-court agent identity" in issue
                for issue in issues
            ),
            issues,
        )

    def test_adjudicator_runtime_must_not_reuse_research_execution(self) -> None:
        record = canonical_experiment()
        record["adjudication"]["adjudicator_runtimes"][0][
            "execution_id"
        ] = "execution-000001"

        issues = validate_experiment(record)

        self.assertTrue(
            any(
                "must not reuse a research-court execution identity" in issue
                for issue in issues
            ),
            issues,
        )

    def test_adjudicator_runtime_must_bind_every_locked_run(self) -> None:
        record = canonical_experiment()
        record["adjudication"]["adjudicator_runtimes"][0][
            "input_run_ids"
        ] = ["run-primary-000001"]

        issues = validate_experiment(record)

        self.assertTrue(
            any(
                "adjudicator_runtimes" in issue and "every locked run" in issue
                for issue in issues
            ),
            issues,
        )

    def test_adjudicator_runtime_ids_must_be_unique(self) -> None:
        record = canonical_experiment()
        runtime = record["adjudication"]["adjudicator_runtimes"][0]
        duplicate = copy.deepcopy(runtime)
        duplicate["execution_id"] = "adjudicator-execution-000002"
        duplicate["context_id"] = "adjudicator-context-000002"
        duplicate["output_lock_sha256"] = "e" * 64
        record["adjudication"]["adjudicator_runtimes"].append(duplicate)
        record["adjudication"]["adjudicator_ids"] = [
            "adjudicator-agent-1"
        ]

        issues = validate_experiment(record)

        self.assertTrue(
            any("must not duplicate adjudicator_id" in issue for issue in issues),
            issues,
        )

    def test_adjudicator_runtime_must_bind_protocol_snapshot(self) -> None:
        record = canonical_experiment()
        record["adjudication"]["adjudicator_runtimes"][0][
            "evidence_snapshot_sha256"
        ] = "e" * 64

        issues = validate_experiment(record)

        self.assertTrue(
            any("protocol evidence snapshot" in issue for issue in issues),
            issues,
        )

    def test_candidate_delivery_requires_independent_adjudicator_runtime(self) -> None:
        record = complete_candidate_delivery_experiment()
        runtime = record["adjudication"]["adjudicator_runtimes"][0]
        runtime["model_id"] = record["runs"][0]["model_id"]
        runtime["model_family"] = record["runs"][0]["model_family"]

        issues = validate_experiment(record)

        self.assertTrue(
            any("independent adjudicator runtime" in issue for issue in issues),
            issues,
        )

    def test_independent_rerun_requires_fresh_context(self) -> None:
        record = canonical_experiment()
        record["runs"][1]["fresh_context"] = False

        issues = validate_experiment(record)

        self.assertTrue(
            any("independent rerun requires fresh_context" in issue for issue in issues),
            issues,
        )

    def test_independent_rerun_cannot_read_prior_run_output(self) -> None:
        record = canonical_experiment()
        record["runs"][1]["prior_run_output_access"] = "primary_output"

        issues = validate_experiment(record)

        self.assertTrue(
            any("independent rerun cannot read prior run output" in issue for issue in issues),
            issues,
        )

    def test_confirmed_leakage_cannot_remain_in_valid_evaluation(self) -> None:
        record = canonical_experiment()
        leakage = record["runs"][0]["predictions"][0]["leakage_assessment"]
        leakage["status"] = "confirmed"
        leakage["types"] = ["gold_label_exposure"]
        leakage["disposition"] = "include"

        issues = validate_experiment(record)

        self.assertTrue(
            any("confirmed leakage must be excluded" in issue for issue in issues),
            issues,
        )

    def test_out_of_domain_adjudication_must_abstain(self) -> None:
        record = canonical_experiment()
        decision = record["adjudication"]["case_decisions"][0]
        decision["ood_status"] = "out_of_calibration_domain"

        issues = validate_experiment(record)

        self.assertTrue(
            any("out-of-domain decision must abstain" in issue for issue in issues),
            issues,
        )

    def test_out_of_domain_case_cannot_enter_candidate_delivery(self) -> None:
        record = canonical_experiment()
        decision = record["adjudication"]["case_decisions"][0]
        decision["ood_status"] = "out_of_calibration_domain"
        decision["decision"] = "abstain"
        decision["delivery_status"] = "ai_adjudicated_candidate"
        decision["selected_candidate_id"] = None
        decision["probability"] = None
        decision["probability_lower_bound"] = None

        issues = validate_experiment(record)

        self.assertTrue(
            any("out-of-domain candidate delivery is forbidden" in issue for issue in issues),
            issues,
        )

    def test_candidate_delivery_requires_lower_bound_over_threshold(self) -> None:
        record = canonical_experiment()
        decision = record["adjudication"]["case_decisions"][0]
        decision["delivery_status"] = "ai_adjudicated_candidate"

        issues = validate_experiment(record)

        self.assertTrue(
            any("lower bound is below calibrated threshold" in issue for issue in issues),
            issues,
        )

    def test_candidate_delivery_rejects_unresolved_evidence_blocker(self) -> None:
        record = canonical_experiment()
        decision = record["adjudication"]["case_decisions"][0]
        decision["delivery_status"] = "ai_adjudicated_candidate"
        decision["probability_lower_bound"] = 0.95
        decision["evidence_blockers"] = ["missing full inscription context"]

        issues = validate_experiment(record)

        self.assertTrue(
            any("candidate delivery has evidence blockers" in issue for issue in issues),
            issues,
        )

    def test_candidate_delivery_rejects_hard_opposition(self) -> None:
        record = canonical_experiment()
        decision = record["adjudication"]["case_decisions"][0]
        decision["delivery_status"] = "ai_adjudicated_candidate"
        decision["probability_lower_bound"] = 0.95
        decision["hard_opposition"] = True

        issues = validate_experiment(record)

        self.assertTrue(
            any("candidate delivery has hard opposition" in issue for issue in issues),
            issues,
        )

    def test_candidate_delivery_requires_supported_calibration(self) -> None:
        record = canonical_experiment()
        decision = record["adjudication"]["case_decisions"][0]
        decision["delivery_status"] = "ai_adjudicated_candidate"
        decision["probability_lower_bound"] = 0.95
        record["benchmark"]["calibration"]["threshold_status"] = (
            "insufficient_effective_cases"
        )

        issues = validate_experiment(record)

        self.assertTrue(
            any("calibration does not support delivery" in issue for issue in issues),
            issues,
        )

    def test_candidate_delivery_requires_minimum_effective_sample(self) -> None:
        record = canonical_experiment()
        decision = record["adjudication"]["case_decisions"][0]
        decision["delivery_status"] = "ai_adjudicated_candidate"
        decision["probability_lower_bound"] = 0.95
        record["benchmark"]["calibration"]["effective_case_count"] = 19

        issues = validate_experiment(record)

        self.assertTrue(
            any("calibration effective sample is below minimum" in issue for issue in issues),
            issues,
        )

    def test_candidate_delivery_requires_scored_valid_evaluation(self) -> None:
        record = canonical_experiment()
        decision = record["adjudication"]["case_decisions"][0]
        decision["delivery_status"] = "ai_adjudicated_candidate"
        decision["probability_lower_bound"] = 0.95

        issues = validate_experiment(record)

        self.assertTrue(
            any("scored valid evaluation" in issue for issue in issues),
            issues,
        )

    def test_candidate_delivery_rejects_unknown_pretraining_exposure(self) -> None:
        record = canonical_experiment()
        decision = record["adjudication"]["case_decisions"][0]
        decision["delivery_status"] = "ai_adjudicated_candidate"
        decision["probability_lower_bound"] = 0.95

        issues = validate_experiment(record)

        self.assertTrue(
            any("clean holdout eligibility" in issue for issue in issues),
            issues,
        )

    def test_candidate_delivery_requires_predict_decision(self) -> None:
        record = canonical_experiment()
        decision = record["adjudication"]["case_decisions"][0]
        decision["delivery_status"] = "ai_adjudicated_candidate"
        decision["decision"] = "abstain"
        decision["selected_candidate_id"] = None
        decision["probability"] = None
        decision["probability_lower_bound"] = 0.95

        issues = validate_experiment(record)

        self.assertTrue(
            any("delivery requires a predict decision" in issue for issue in issues),
            issues,
        )

    def test_candidate_delivery_rejects_candidate_outside_case_universe(self) -> None:
        record = canonical_experiment()
        decision = record["adjudication"]["case_decisions"][0]
        decision["delivery_status"] = "ai_adjudicated_candidate"
        decision["selected_candidate_id"] = "invented-candidate"
        decision["probability_lower_bound"] = 0.95

        issues = validate_experiment(record)

        self.assertTrue(
            any("outside the case candidate universe" in issue for issue in issues),
            issues,
        )

    def test_out_of_domain_decision_must_clear_numeric_probability(self) -> None:
        record = canonical_experiment()
        decision = record["adjudication"]["case_decisions"][0]
        decision["ood_status"] = "out_of_calibration_domain"
        decision["decision"] = "abstain"
        decision["selected_candidate_id"] = None

        issues = validate_experiment(record)

        self.assertTrue(
            any("out-of-domain decision must clear probability" in issue for issue in issues),
            issues,
        )

    def test_duplicate_case_ids_are_rejected(self) -> None:
        record = canonical_experiment()
        record["benchmark"]["cases"][0]["case_id"] = "case-test-000001"

        issues = validate_experiment(record)

        self.assertTrue(any("case_id must be unique" in issue for issue in issues), issues)

    def test_benchmark_requires_all_four_case_types(self) -> None:
        record = canonical_experiment()
        record["benchmark"]["cases"] = record["benchmark"]["cases"][:2]

        issues = validate_experiment(record)

        self.assertTrue(any("four case types" in issue for issue in issues), issues)

    def test_candidate_universe_requires_explicit_unknown_mass(self) -> None:
        record = canonical_experiment()
        record["benchmark"]["cases"][0]["candidate_ids"].remove(
            "unknown_or_other"
        )

        issues = validate_experiment(record)

        self.assertTrue(
            any("unknown_or_other" in issue for issue in issues),
            issues,
        )

    def test_candidate_delivery_requires_two_reviewed_evidence_families(self) -> None:
        record = canonical_experiment()
        decision = record["adjudication"]["case_decisions"][0]
        decision["delivery_status"] = "ai_adjudicated_candidate"
        decision["probability_lower_bound"] = 0.95

        issues = validate_experiment(record)

        self.assertTrue(
            any("two independent evidence families" in issue for issue in issues),
            issues,
        )

    def test_candidate_delivery_requires_human_package(self) -> None:
        record = canonical_experiment()
        decision = record["adjudication"]["case_decisions"][0]
        decision["delivery_status"] = "ai_adjudicated_candidate"
        decision["probability_lower_bound"] = 0.95
        package = record["human_delivery_package"]
        package["status"] = "complete"
        package["rights_review_status"] = "complete"
        package["content_review_status"] = "complete"

        issues = validate_experiment(record)

        self.assertTrue(
            any("external isolated scorer" in issue for issue in issues),
            issues,
        )

    def test_candidate_delivery_requires_external_isolated_gold(self) -> None:
        record = canonical_experiment()
        decision = record["adjudication"]["case_decisions"][0]
        decision["delivery_status"] = "ai_adjudicated_candidate"
        decision["probability_lower_bound"] = 0.95
        package = record["human_delivery_package"]
        package["status"] = "complete"
        package["rights_review_status"] = "complete"
        package["content_review_status"] = "complete"

        issues = validate_experiment(record)

        self.assertTrue(
            any("external isolated scorer" in issue for issue in issues),
            issues,
        )

    def test_complete_ai_candidate_delivery_contract_can_pass(self) -> None:
        record = complete_candidate_delivery_experiment()

        self.assertEqual(validate_experiment(record), [])

    def test_clean_holdout_requires_verified_training_cutoff_evidence(self) -> None:
        record = complete_candidate_delivery_experiment()
        record["benchmark"]["cases"][1]["training_cutoff_evidence"][
            "review_status"
        ] = "pending"

        issues = validate_experiment(record)

        self.assertTrue(
            any("training cutoff evidence is not verified" in issue for issue in issues),
            issues,
        )

    def test_delivery_evaluation_must_reference_sealed_gold(self) -> None:
        record = complete_candidate_delivery_experiment()
        record["evaluation"]["sealed_gold_commitment_ref"] = "wrong-gold-key"

        issues = validate_experiment(record)

        self.assertTrue(
            any("evaluation does not reference sealed gold" in issue for issue in issues),
            issues,
        )

    def test_delivery_metrics_must_cover_every_locked_run(self) -> None:
        record = complete_candidate_delivery_experiment()
        record["evaluation"]["metric_sets"].pop()

        issues = validate_experiment(record)

        self.assertTrue(
            any("metric sets must bind every locked run" in issue for issue in issues),
            issues,
        )

    def test_model_independent_rerun_requires_distinct_model_family(self) -> None:
        record = complete_candidate_delivery_experiment()
        record["runs"][1]["model_family"] = record["runs"][0]["model_family"]

        issues = validate_experiment(record)

        self.assertTrue(
            any("model-independent rerun reuses model family" in issue for issue in issues),
            issues,
        )

    def test_model_independent_rerun_requires_distinct_model_id(self) -> None:
        record = complete_candidate_delivery_experiment()
        record["runs"][1]["model_id"] = record["runs"][0]["model_id"]

        issues = validate_experiment(record)

        self.assertTrue(
            any("model-independent rerun reuses model id" in issue for issue in issues),
            issues,
        )

    def test_delivery_evidence_families_require_distinct_source_ancestors(
        self,
    ) -> None:
        record = complete_candidate_delivery_experiment()
        for run in record["runs"]:
            items = run["predictions"][0]["supporting_evidence"]["items"]
            items[1]["source_ancestor_id"] = items[0]["source_ancestor_id"]

        issues = validate_experiment(record)

        self.assertTrue(
            any("independent source ancestors" in issue for issue in issues),
            issues,
        )

    def test_gold_must_be_sealed_before_first_run(self) -> None:
        record = canonical_experiment()
        record["benchmark"]["sealed_gold"]["sealed_at"] = (
            "2026-08-09T00:02:00Z"
        )

        issues = validate_experiment(record)

        self.assertTrue(
            any("gold must be sealed before first run" in issue for issue in issues),
            issues,
        )

    def test_gold_unseal_must_follow_locked_adjudication(self) -> None:
        record = canonical_experiment()
        record["benchmark"]["sealed_gold"]["unseal_status"] = (
            "scorer_only_unsealed_retired"
        )
        record["benchmark"]["sealed_gold"]["unsealed_at"] = (
            "2026-08-09T00:05:30Z"
        )

        issues = validate_experiment(record)

        self.assertTrue(
            any("gold unseal must follow locked adjudication" in issue for issue in issues),
            issues,
        )

    def test_agents_cannot_access_gold_before_scoring(self) -> None:
        record = canonical_experiment()
        record["runs"][1]["gold_access"] = "available"

        issues = validate_experiment(record)

        self.assertTrue(
            any("agent gold_access must remain sealed" in issue for issue in issues),
            issues,
        )

    def test_run_disagreement_requires_adjudication_decision(self) -> None:
        record = canonical_experiment()
        rerun_prediction = record["runs"][1]["predictions"][0]
        rerun_prediction["ranked_candidates"] = [
            {"rank": 1, "candidate_id": "candidate-b", "probability": 0.8},
            {"rank": 2, "candidate_id": "candidate-a", "probability": 0.2},
        ]
        rerun_prediction["selected_candidate_id"] = "candidate-b"
        rerun_prediction["falsification_checks"][0]["target_candidate_id"] = (
            "candidate-b"
        )
        record["adjudication"]["case_decisions"] = []

        issues = validate_experiment(record)

        self.assertTrue(
            any("disagreement case missing adjudication" in issue for issue in issues),
            issues,
        )

    def test_public_record_rejects_unknown_top_level_field(self) -> None:
        record = canonical_experiment()
        record["unreviewed_payload"] = {"value": 1}

        issues = validate_experiment(record)

        self.assertTrue(
            any("unknown top-level fields" in issue for issue in issues),
            issues,
        )

    def test_public_record_requires_every_top_level_contract_field(self) -> None:
        record = canonical_experiment()
        del record["protocol"]

        issues = validate_experiment(record)

        self.assertTrue(
            any("missing top-level fields" in issue for issue in issues),
            issues,
        )

    def test_schema_requires_case_evidence_snapshot(self) -> None:
        record = canonical_experiment()
        record["benchmark"]["cases"][0].pop("evidence_pack_snapshot")

        issues = validate_experiment(record)

        self.assertTrue(
            any("evidence_pack_snapshot" in issue for issue in issues),
            issues,
        )

    def test_schema_requires_family_split_contract(self) -> None:
        record = canonical_experiment()
        record["benchmark"].pop("family_split")

        issues = validate_experiment(record)

        self.assertTrue(any("family_split" in issue for issue in issues), issues)

    def test_schema_requires_falsification_policy(self) -> None:
        record = canonical_experiment()
        record["protocol"].pop("falsification_policy")

        issues = validate_experiment(record)

        self.assertTrue(
            any("falsification_policy" in issue for issue in issues),
            issues,
        )

    def test_schema_requires_nonempty_review_log(self) -> None:
        record = canonical_experiment()
        record["review_log"] = []

        issues = validate_experiment(record)

        self.assertTrue(any("review_log" in issue for issue in issues), issues)

    def test_experiment_record_cannot_live_under_scholarship_root(self) -> None:
        root = Path("controlled-repository-root")
        path = root / "research" / "experiment.json"

        issues = validate_experiment(canonical_experiment(), path=path, root=root)

        self.assertTrue(
            any("must not be under root research" in issue for issue in issues),
            issues,
        )

    def test_caution_must_preserve_non_scholarship_boundary(self) -> None:
        record = canonical_experiment()
        record["caution"] = "Candidate record."

        issues = validate_experiment(record)

        self.assertTrue(
            any("caution must state the research boundary" in issue for issue in issues),
            issues,
        )

    def test_discovery_ignores_v1_evidence_pack_json(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            v1_path = root / "case_evidence-pack-draft.json"
            v2_path = root / "case_benchmark-experiment-v2.json"
            v1_path.write_text("{}", encoding="utf-8")
            v2_path.write_text("{}", encoding="utf-8")

            paths = discover_experiment_paths(root)

        self.assertEqual(paths, [v2_path])

    def test_cli_marks_metrics_unrecomputed_without_private_gold(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "case_benchmark-experiment-v2.json"
            path.write_text(
                json.dumps(canonical_experiment(), ensure_ascii=False),
                encoding="utf-8",
            )
            stdout = io.StringIO()

            with contextlib.redirect_stdout(stdout):
                return_code = main(["--path", str(path)])

        self.assertEqual(return_code, 0)
        self.assertIn("METRICS_NOT_RECOMPUTED", stdout.getvalue())

    def test_metric_recomputation_matches_hand_checked_fixture(self) -> None:
        record = canonical_experiment()
        sha_d = "d" * 64
        record["benchmark"]["cases"].append(
            {
                "case_id": "case-test-000002",
                "family_id": "family-test-000002",
                "split": "test",
                "input_ref": "ignored/test-input-000002",
                "input_sha256": sha_d,
                "candidate_ids": ["candidate-a", "candidate-b"],
                "evidence_pack_snapshot": {
                    "evidence_pack_id": "hust-obc-evidence-pack-000003",
                    "path": "doc/public/user_research/example-3.json",
                    "sha256": sha_d,
                    "status": "hypothesis",
                },
            }
        )
        second_prediction = copy.deepcopy(record["runs"][0]["predictions"][0])
        second_prediction["case_id"] = "case-test-000002"
        second_prediction["ranked_candidates"] = [
            {"rank": 1, "candidate_id": "candidate-a", "probability": 0.6},
            {"rank": 2, "candidate_id": "candidate-b", "probability": 0.4},
        ]
        second_prediction["action"] = "abstain"
        second_prediction["selected_candidate_id"] = None
        second_prediction["abstention_reason_code"] = "below_threshold"
        record["runs"][0]["predictions"].append(second_prediction)

        metrics = compute_run_metrics(
            record,
            {
                "case-test-000001": "candidate-a",
                "case-test-000002": "candidate-b",
            },
            "run-primary-000001",
        )

        self.assertEqual(metrics["test_case_count"], 2)
        self.assertEqual(metrics["abstained_count"], 1)
        self.assertAlmostEqual(metrics["brier_multiclass_mean"], 0.4)
        self.assertAlmostEqual(metrics["log_loss_nats_mean"], 0.569717141594)
        self.assertAlmostEqual(metrics["ece_top1"], 0.4)
        self.assertAlmostEqual(metrics["coverage"], 0.5)
        self.assertAlmostEqual(metrics["selective_risk"], 0.0)

    def test_metric_recomputation_rejects_empty_test_split(self) -> None:
        record = canonical_experiment()
        record["benchmark"]["cases"] = [
            case
            for case in record["benchmark"]["cases"]
            if case["split"] != "test"
        ]
        record["runs"][0]["predictions"] = []

        with self.assertRaisesRegex(ValueError, "at least one test case"):
            compute_run_metrics(
                record,
                {"case-test-000001": "candidate-a"},
                "run-primary-000001",
            )

    def test_cli_recomputes_metrics_with_ignored_private_gold(self) -> None:
        record = canonical_experiment()
        private_gold = attach_private_gold(
            record, {"case-test-000001": "candidate-a"}
        )

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            experiment_path = root / "case_benchmark-experiment-v2.json"
            gold_path = root / "private-gold.json"
            experiment_path.write_text(
                json.dumps(record, ensure_ascii=False), encoding="utf-8"
            )
            gold_path.write_text(
                json.dumps(private_gold, ensure_ascii=False), encoding="utf-8"
            )
            stdout = io.StringIO()

            with contextlib.redirect_stdout(stdout):
                return_code = main(
                    [
                        "--path",
                        str(experiment_path),
                        "--gold-path",
                        str(gold_path),
                    ]
                )

        self.assertEqual(return_code, 0)
        self.assertIn("METRICS_RECOMPUTED", stdout.getvalue())

    def test_cli_rejects_private_gold_that_breaks_commitment(self) -> None:
        record = canonical_experiment()
        private_gold = {
            "benchmark_id": "ai-bench-000001",
            "benchmark_version": "1.0.0",
            "gold_key_id": "gold-key-000001",
            "case_candidate_manifest_sha256": record["benchmark"][
                "sealed_gold"
            ]["case_candidate_manifest_sha256"],
            "protocol_sha256": "a" * 64,
            "commitment_key_hex": "22" * 32,
            "labels": [
                {
                    "case_id": "case-test-000001",
                    "gold_candidate_id": "candidate-b",
                }
            ],
        }

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            experiment_path = root / "case_benchmark-experiment-v2.json"
            gold_path = root / "private-gold.json"
            experiment_path.write_text(json.dumps(record), encoding="utf-8")
            gold_path.write_text(json.dumps(private_gold), encoding="utf-8")
            stdout = io.StringIO()

            with contextlib.redirect_stdout(stdout):
                return_code = main(
                    [
                        "--path",
                        str(experiment_path),
                        "--gold-path",
                        str(gold_path),
                    ]
                )

        self.assertEqual(return_code, 1)
        self.assertIn("does not match sealed commitment", stdout.getvalue())

    def test_cli_rejects_gold_bound_to_another_benchmark(self) -> None:
        record = canonical_experiment()
        key_hex = "33" * 32
        committed_payload = {
            "benchmark_id": "ai-bench-999999",
            "benchmark_version": "1.0.0",
            "gold_key_id": "gold-key-000001",
            "case_candidate_manifest_sha256": "b" * 64,
            "protocol_sha256": "a" * 64,
            "labels": [
                {
                    "case_id": "case-test-000001",
                    "gold_candidate_id": "candidate-a",
                }
            ],
        }
        message = json.dumps(
            committed_payload,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        record["benchmark"]["sealed_gold"]["commitment"] = hmac.new(
            bytes.fromhex(key_hex), message, hashlib.sha256
        ).hexdigest()
        private_gold = {
            **committed_payload,
            "commitment_key_hex": key_hex,
        }

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            experiment_path = root / "case_benchmark-experiment-v2.json"
            gold_path = root / "private-gold.json"
            experiment_path.write_text(json.dumps(record), encoding="utf-8")
            gold_path.write_text(json.dumps(private_gold), encoding="utf-8")
            stdout = io.StringIO()

            with contextlib.redirect_stdout(stdout):
                return_code = main(
                    [
                        "--path",
                        str(experiment_path),
                        "--gold-path",
                        str(gold_path),
                    ]
                )

        self.assertEqual(return_code, 1)
        self.assertIn("does not bind to experiment benchmark", stdout.getvalue())

    def test_cli_rejects_duplicate_private_gold_case(self) -> None:
        record = canonical_experiment()
        private_gold = attach_private_gold(
            record, {"case-test-000001": "candidate-a"}
        )
        private_gold["labels"].append(
            {"case_id": "case-test-000001", "gold_candidate_id": "candidate-b"}
        )

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            experiment_path = root / "case_benchmark-experiment-v2.json"
            gold_path = root / "private-gold.json"
            experiment_path.write_text(json.dumps(record), encoding="utf-8")
            gold_path.write_text(json.dumps(private_gold), encoding="utf-8")
            stdout = io.StringIO()

            with contextlib.redirect_stdout(stdout):
                return_code = main(
                    [
                        "--path",
                        str(experiment_path),
                        "--gold-path",
                        str(gold_path),
                    ]
                )

        self.assertEqual(return_code, 1)
        self.assertIn("gold labels must be unique", stdout.getvalue())

    def test_cli_rejects_unignored_repository_gold_path(self) -> None:
        record = canonical_experiment()

        with tempfile.TemporaryDirectory() as temporary_directory:
            experiment_path = Path(temporary_directory) / "case_benchmark-experiment-v2.json"
            experiment_path.write_text(json.dumps(record), encoding="utf-8")
            stdout = io.StringIO()

            with contextlib.redirect_stdout(stdout):
                return_code = main(
                    [
                        "--path",
                        str(experiment_path),
                        "--gold-path",
                        str(Path(__file__).resolve().parents[1] / "README.md"),
                    ]
                )

        self.assertEqual(return_code, 1)
        self.assertIn("outside the repository or Git-ignored", stdout.getvalue())

    def test_scored_record_rejects_claimed_metric_drift(self) -> None:
        record = canonical_experiment()
        record["evaluation"]["status"] = "scored"
        record["evaluation"]["metric_sets"] = [
            {
                "run_id": "run-primary-000001",
                "test_case_count": 1,
                "abstained_count": 0,
                "covered_count": 1,
                "brier_multiclass_mean": 1.0,
                "log_loss_nats_mean": 0.223143551314,
                "ece_top1": 0.2,
                "coverage": 1.0,
                "selective_risk": 0.0,
            }
        ]
        recomputed = {
            "run-primary-000001": compute_run_metrics(
                record,
                {"case-test-000001": "candidate-a"},
                "run-primary-000001",
            )
        }

        issues = compare_claimed_metrics(record, recomputed)

        self.assertTrue(
            any("claimed metric mismatch" in issue for issue in issues),
            issues,
        )

    def test_scored_record_rejects_duplicate_metric_sets(self) -> None:
        record = canonical_experiment()
        record["evaluation"]["status"] = "scored"
        metric = {
            "run_id": "run-primary-000001",
            "test_case_count": 1,
            "abstained_count": 0,
            "covered_count": 1,
            "brier_multiclass_mean": 0.08,
            "log_loss_nats_mean": 0.223143551314,
            "ece_top1": 0.2,
            "coverage": 1.0,
            "selective_risk": 0.0,
        }
        record["evaluation"]["metric_sets"] = [copy.deepcopy(metric), metric]

        issues = compare_claimed_metrics(
            record,
            {"run-primary-000001": metric},
        )

        self.assertTrue(any("metric set run_id must be unique" in issue for issue in issues), issues)

    def test_cli_fails_when_scored_metrics_do_not_recompute(self) -> None:
        record = canonical_experiment()
        record["evaluation"]["status"] = "scored"
        record["evaluation"]["metric_sets"] = [
            {
                "run_id": "run-primary-000001",
                "test_case_count": 1,
                "abstained_count": 0,
                "covered_count": 1,
                "brier_multiclass_mean": 1.0,
                "log_loss_nats_mean": 0.223143551314,
                "ece_top1": 0.2,
                "coverage": 1.0,
                "selective_risk": 0.0,
            }
        ]
        private_gold = attach_private_gold(
            record, {"case-test-000001": "candidate-a"}
        )

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            experiment_path = root / "case_benchmark-experiment-v2.json"
            gold_path = root / "private-gold.json"
            experiment_path.write_text(json.dumps(record), encoding="utf-8")
            gold_path.write_text(json.dumps(private_gold), encoding="utf-8")
            stdout = io.StringIO()

            with contextlib.redirect_stdout(stdout):
                return_code = main(
                    [
                        "--path",
                        str(experiment_path),
                        "--gold-path",
                        str(gold_path),
                    ]
                )

        self.assertEqual(return_code, 1)
        self.assertIn("claimed metric mismatch", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
