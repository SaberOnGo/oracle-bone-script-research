from __future__ import annotations

import hashlib
import hmac
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/006_ai-benchmark-pilot/ai_benchmark_pilot.py"
OBJECT_REL = Path(
    "corpus/001_oracle-characters/"
    "017_undeciphered-000001-000100_obs-unk-bucket_"
    "oracle-character-candidates/"
    "001_obs-unk-000001_hust-obc-und-L-000001_"
    "oracle-character-candidate"
)
OBJECT_DIR = ROOT / OBJECT_REL
ALLOWED_FILES = [
    "05_human-research-dossier.md",
    "14_material-visual-observation.md",
]


class AIBenchmarkPilotCLITests(unittest.TestCase):
    def setUp(self) -> None:
        working_root = ROOT / ".working"
        working_root.mkdir(exist_ok=True)
        self.work_dir = Path(
            tempfile.mkdtemp(prefix="ai-benchmark-pilot-test-", dir=working_root)
        )

    def tearDown(self) -> None:
        shutil.rmtree(self.work_dir)

    def _case_metadata(self) -> dict[str, object]:
        files = {}
        for relative_path in ALLOWED_FILES:
            files[relative_path] = {
                "source_id": "src-hust-obc",
                "source_ancestor_id": "src-hust-obc",
                "derivative_family_id": "hust-obc-und-L-000001",
                "rights_status": "research_use_only",
                "allowed_delivery_form": "metadata_only",
                "risk_note": (
                    "HUST-OBC rights signals require source-level review; "
                    "this diagnostic snapshot redistributes no source image."
                ),
                "large_source_register_ref": "large-src-000001",
                "dependency_review_status": "reviewed",
            }
        return {
            "case_id": "case-diagnostic-000001",
            "family_id": "family-hust-obc-und-L-000001",
            "case_type": "hard_challenge",
            "split": "challenge",
            "blind_alias": "blind-case-000001",
            "evidence_cutoff_at": "2026-08-12T00:00:00Z",
            "files": files,
        }

    def _write_metadata(self, value: dict[str, object]) -> Path:
        path = self.work_dir / "case-metadata.json"
        path.write_text(
            json.dumps(value, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return path

    def _run(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )

    def _freeze(self, metadata_path: Path, output_path: Path):
        arguments = [
            "freeze",
            "--object-dir",
            str(OBJECT_DIR),
            "--case-metadata",
            str(metadata_path),
            "--candidate-id",
            "candidate-opaque-a",
            "--candidate-id",
            "candidate-opaque-b",
            "--candidate-id",
            "unknown_or_other",
        ]
        for relative_path in ALLOWED_FILES:
            arguments.extend(["--allowed-file", relative_path])
        arguments.extend(["--output", str(output_path)])
        return self._run(*arguments)

    def _write_run_report(self, frozen: dict[str, object]) -> Path:
        snapshots = frozen["file_snapshots"]
        prompt_path = self.work_dir / "prompt-manifest.md"
        prompt_path.write_text(
            "# Blind pilot\n\nRank the opaque candidates from frozen evidence.\n",
            encoding="utf-8",
        )
        report = {
            "run_id": "pilot-run-primary-000001",
            "role": "primary",
            "execution_id": "pilot-execution-000001",
            "agent_id": "blind-hypothesis-agent-000001",
            "model_id": "diagnostic-model-000001",
            "model_family": "diagnostic-family-000001",
            "context_id": "fresh-context-000001",
            "fresh_context": True,
            "prior_run_output_access": "none",
            "gold_access": "sealed_unavailable",
            "started_at": "2026-08-12T00:01:01Z",
            "completed_at": "2026-08-12T00:02:00Z",
            "frozen_input_sha256": frozen["frozen_input_sha256"],
            "prompt_manifest_sha256": hashlib.sha256(
                prompt_path.read_bytes()
            ).hexdigest(),
            "prediction": {
                "case_id": frozen["case"]["case_id"],
                "ranked_candidates": [
                    {
                        "rank": 1,
                        "candidate_id": "candidate-opaque-a",
                        "probability": 0.5,
                    },
                    {
                        "rank": 2,
                        "candidate_id": "candidate-opaque-b",
                        "probability": 0.3,
                    },
                    {
                        "rank": 3,
                        "candidate_id": "unknown_or_other",
                        "probability": 0.2,
                    },
                ],
                "action": "abstain",
                "selected_candidate_id": None,
                "abstention_reason_code": "insufficient_independent_evidence",
                "supporting_evidence": {
                    "status": "collected",
                    "items": [
                        {
                            "snapshot_sha256": snapshots[0]["sha256"],
                            "target_candidate_id": "candidate-opaque-a",
                            "locator": "lower enclosure and central stem",
                            "note": "Visible geometry supports only a weak ranking.",
                        }
                    ],
                    "search_note": "All frozen snapshots were inspected.",
                },
                "opposing_evidence": {
                    "status": "collected",
                    "items": [
                        {
                            "snapshot_sha256": snapshots[1]["sha256"],
                            "target_candidate_id": "candidate-opaque-a",
                            "locator": "missing inscription context",
                            "note": "The frozen material cannot verify context.",
                        }
                    ],
                    "search_note": "Counterevidence was recorded before ranking.",
                },
                "falsification_checks": [
                    {
                        "check_id": "pilot-falsifier-000001",
                        "target_candidate_id": "candidate-opaque-a",
                        "method": "Seek a context incompatible with the top form.",
                        "outcome": "inconclusive",
                        "evidence_snapshot_sha256s": [
                            snapshots[0]["sha256"],
                            snapshots[1]["sha256"],
                        ],
                        "note": "No inscription context is present in the freeze.",
                    }
                ],
                "leakage_assessment": {
                    "status": "indeterminate",
                    "types": ["pretraining_unknown"],
                    "disposition": "diagnostic_only",
                    "note": "Model training exposure cannot be excluded.",
                },
                "reasoning_summary": (
                    "The frozen visual record supports ranking but not delivery."
                ),
            },
        }
        agent_output_path = self.work_dir / "agent-output.json"
        agent_output_path.write_text(
            json.dumps(
                report["prediction"],
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )
            + "\n",
            encoding="utf-8",
        )
        report["agent_output_sha256"] = hashlib.sha256(
            agent_output_path.read_bytes()
        ).hexdigest()
        path = self.work_dir / "run-report.json"
        path.write_text(
            json.dumps(report, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return path

    def _prepare_frozen_case(self) -> tuple[Path, dict[str, object]]:
        metadata_path = self._write_metadata(self._case_metadata())
        frozen_path = self.work_dir / "frozen-case.json"
        result = self._freeze(metadata_path, frozen_path)
        self.assertEqual(result.returncode, 0, result.stderr)
        return frozen_path, json.loads(frozen_path.read_text(encoding="utf-8"))

    def _private_gold(self, frozen: dict[str, object]) -> dict[str, object]:
        prompt_path = self.work_dir / "prompt-manifest.md"
        return {
            "benchmark_id": "ai-benchmark-diagnostic-000001",
            "benchmark_version": "2.0.0",
            "gold_key_id": "gold-key-diagnostic-000001",
            "case_candidate_manifest_sha256": frozen[
                "case_candidate_manifest_sha256"
            ],
            "protocol_sha256": hashlib.sha256(
                prompt_path.read_bytes()
            ).hexdigest(),
            "labels": [
                {
                    "case_id": frozen["case"]["case_id"],
                    "gold_candidate_id": "unknown_or_other",
                }
            ],
            "commitment_key_hex": "11" * 32,
        }

    def _seal_gold(
        self,
        frozen_path: Path,
        frozen: dict[str, object],
    ) -> tuple[Path, Path, subprocess.CompletedProcess[str]]:
        private_path = self.work_dir / "private-gold.json"
        private_path.write_text(
            json.dumps(self._private_gold(frozen)),
            encoding="utf-8",
        )
        public_path = self.work_dir / "public-commitment.json"
        result = self._run(
            "seal",
            "--frozen-case",
            str(frozen_path),
            "--private-gold",
            str(private_path),
            "--sealed-at",
            "2026-08-12T00:00:00Z",
            "--output",
            str(public_path),
        )
        return private_path, public_path, result

    def _prepare_run_chain(
        self,
    ) -> tuple[Path, dict[str, object], Path, Path]:
        frozen_path, frozen = self._prepare_frozen_case()
        report_path = self._write_run_report(frozen)
        _, _, seal = self._seal_gold(frozen_path, frozen)
        self.assertEqual(seal.returncode, 0, seal.stderr)
        opening_path = self.work_dir / "run-opening.json"
        opening = self._open_run(frozen_path, opening_path)
        self.assertEqual(opening.returncode, 0, opening.stderr)
        return frozen_path, frozen, report_path, opening_path

    def _rewrite_agent_prediction(
        self,
        report_path: Path,
        report: dict[str, object],
    ) -> None:
        agent_output_path = self.work_dir / "agent-output.json"
        agent_output_path.write_text(
            json.dumps(
                report["prediction"],
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )
            + "\n",
            encoding="utf-8",
        )
        report["agent_output_sha256"] = hashlib.sha256(
            agent_output_path.read_bytes()
        ).hexdigest()
        report_path.write_text(json.dumps(report), encoding="utf-8")

    def _lock_run(
        self,
        frozen_path: Path,
        report_path: Path,
        output_path: Path,
    ) -> subprocess.CompletedProcess[str]:
        return self._run(
            "lock-run",
            "--frozen-case",
            str(frozen_path),
            "--run-opening",
            str(self.work_dir / "run-opening.json"),
            "--run-report",
            str(report_path),
            "--prompt-manifest",
            str(self.work_dir / "prompt-manifest.md"),
            "--agent-output",
            str(self.work_dir / "agent-output.json"),
            "--locked-at",
            "2026-08-12T00:03:00Z",
            "--output",
            str(output_path),
        )

    def _open_run(
        self,
        frozen_path: Path,
        output_path: Path,
    ) -> subprocess.CompletedProcess[str]:
        return self._run(
            "open-run",
            "--frozen-case",
            str(frozen_path),
            "--public-commitment",
            str(self.work_dir / "public-commitment.json"),
            "--prompt-manifest",
            str(self.work_dir / "prompt-manifest.md"),
            "--run-id",
            "pilot-run-primary-000001",
            "--role",
            "primary",
            "--execution-id",
            "pilot-execution-000001",
            "--agent-id",
            "blind-hypothesis-agent-000001",
            "--model-id",
            "diagnostic-model-000001",
            "--model-family",
            "diagnostic-family-000001",
            "--context-id",
            "fresh-context-000001",
            "--opened-at",
            "2026-08-12T00:01:00Z",
            "--output",
            str(output_path),
        )

    def _set_scoring_prediction(
        self,
        report: dict[str, object],
        top_candidate_id: str,
    ) -> None:
        prediction = report["prediction"]
        assert isinstance(prediction, dict)
        ranked = prediction["ranked_candidates"]
        assert isinstance(ranked, list)
        ordered_ids = [top_candidate_id] + [
            candidate_id
            for candidate_id in (
                "candidate-opaque-a",
                "candidate-opaque-b",
                "unknown_or_other",
            )
            if candidate_id != top_candidate_id
        ]
        prediction["ranked_candidates"] = [
            {
                "rank": index,
                "candidate_id": candidate_id,
                "probability": probability,
            }
            for index, (candidate_id, probability) in enumerate(
                zip(ordered_ids, (0.5, 0.3, 0.2)),
                1,
            )
        ]
        leakage = prediction["leakage_assessment"]
        assert isinstance(leakage, dict)
        leakage["status"] = "indeterminate"
        leakage["types"] = ["pretraining_exposure_unknown"]

    def _write_report_and_agent_output(
        self,
        report: dict[str, object],
        report_path: Path,
        agent_output_path: Path,
    ) -> None:
        prediction = report["prediction"]
        agent_output_path.write_text(
            json.dumps(
                prediction,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )
            + "\n",
            encoding="utf-8",
        )
        report["agent_output_sha256"] = hashlib.sha256(
            agent_output_path.read_bytes()
        ).hexdigest()
        report_path.write_text(
            json.dumps(report, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _prepare_scoring_inputs(
        self,
        first_top: str = "unknown_or_other",
        second_top: str = "unknown_or_other",
    ) -> tuple[Path, Path, Path, list[Path]]:
        metadata = self._case_metadata()
        metadata["case_type"] = "null_or_negative_control"
        metadata["split"] = "test"
        frozen_path = self.work_dir / "score-frozen-case.json"
        freeze = self._freeze(self._write_metadata(metadata), frozen_path)
        self.assertEqual(freeze.returncode, 0, freeze.stderr)
        frozen = json.loads(frozen_path.read_text(encoding="utf-8"))

        first_report_path = self._write_run_report(frozen)
        first_report = json.loads(first_report_path.read_text(encoding="utf-8"))
        self._set_scoring_prediction(first_report, first_top)
        self._write_report_and_agent_output(
            first_report,
            first_report_path,
            self.work_dir / "agent-output.json",
        )
        private_path, public_path, seal = self._seal_gold(frozen_path, frozen)
        self.assertEqual(seal.returncode, 0, seal.stderr)
        first_opening_path = self.work_dir / "run-opening.json"
        first_opening = self._open_run(frozen_path, first_opening_path)
        self.assertEqual(first_opening.returncode, 0, first_opening.stderr)
        first_locked_path = self.work_dir / "locked-run-primary.json"
        first_locked = self._lock_run(
            frozen_path,
            first_report_path,
            first_locked_path,
        )
        self.assertEqual(first_locked.returncode, 0, first_locked.stderr)

        second_report = json.loads(first_report_path.read_text(encoding="utf-8"))
        second_report.update(
            {
                "run_id": "pilot-run-execution-000002",
                "role": "execution_rerun",
                "execution_id": "pilot-execution-000002",
                "agent_id": "blind-hypothesis-agent-000002",
                "context_id": "fresh-context-000002",
                "started_at": "2026-08-12T00:01:02Z",
                "completed_at": "2026-08-12T00:02:01Z",
            }
        )
        self._set_scoring_prediction(second_report, second_top)
        second_report_path = self.work_dir / "run-report-2.json"
        second_agent_path = self.work_dir / "agent-output-2.json"
        self._write_report_and_agent_output(
            second_report,
            second_report_path,
            second_agent_path,
        )
        second_opening_path = self.work_dir / "run-opening-2.json"
        second_opening = self._run(
            "open-run",
            "--frozen-case",
            str(frozen_path),
            "--public-commitment",
            str(public_path),
            "--prompt-manifest",
            str(self.work_dir / "prompt-manifest.md"),
            "--run-id",
            "pilot-run-execution-000002",
            "--role",
            "execution_rerun",
            "--execution-id",
            "pilot-execution-000002",
            "--agent-id",
            "blind-hypothesis-agent-000002",
            "--model-id",
            "diagnostic-model-000001",
            "--model-family",
            "diagnostic-family-000001",
            "--context-id",
            "fresh-context-000002",
            "--opened-at",
            "2026-08-12T00:01:00Z",
            "--output",
            str(second_opening_path),
        )
        self.assertEqual(second_opening.returncode, 0, second_opening.stderr)
        second_locked_path = self.work_dir / "locked-run-execution.json"
        second_locked = self._run(
            "lock-run",
            "--frozen-case",
            str(frozen_path),
            "--run-opening",
            str(second_opening_path),
            "--run-report",
            str(second_report_path),
            "--prompt-manifest",
            str(self.work_dir / "prompt-manifest.md"),
            "--agent-output",
            str(second_agent_path),
            "--locked-at",
            "2026-08-12T00:03:01Z",
            "--output",
            str(second_locked_path),
        )
        self.assertEqual(second_locked.returncode, 0, second_locked.stderr)
        return (
            frozen_path,
            public_path,
            private_path,
            [first_locked_path, second_locked_path],
        )

    def _score_local(
        self,
        frozen_path: Path,
        public_path: Path,
        private_path: Path,
        locked_paths: list[Path],
        output_path: Path,
    ) -> subprocess.CompletedProcess[str]:
        arguments = [
            "score-local",
            "--frozen-case",
            str(frozen_path),
            "--public-commitment",
            str(public_path),
            "--private-gold",
            str(private_path),
        ]
        for locked_path in locked_paths:
            arguments.extend(["--locked-run", str(locked_path)])
        arguments.extend(
            [
                "--scored-at",
                "2026-08-12T00:04:00Z",
                "--output",
                str(output_path),
            ]
        )
        return self._run(*arguments)

    def test_freeze_hashes_real_allowed_files_and_marks_diagnostic_boundary(self):
        metadata_path = self._write_metadata(self._case_metadata())
        output_path = self.work_dir / "frozen-case.json"

        result = self._freeze(metadata_path, output_path)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS diagnostic frozen case", result.stdout)
        frozen = json.loads(output_path.read_text(encoding="utf-8"))
        self.assertEqual(frozen["diagnostic_status"], "diagnostic_only")
        self.assertEqual(
            frozen["benchmark_eligibility"], "pretraining_exposure_unknown"
        )
        self.assertEqual(frozen["pretraining_exposure"], "unknown")
        self.assertEqual(
            frozen["research_boundary"], "benchmark_pilot_not_scholarship"
        )
        self.assertEqual(frozen["probability_status"], "not_generated")
        self.assertEqual(frozen["gate3_status"], "not_attempted")
        self.assertEqual(frozen["case"]["blind_alias"], "blind-case-000001")
        self.assertEqual(
            frozen["case"]["evidence_cutoff_at"], "2026-08-12T00:00:00Z"
        )
        self.assertEqual(
            frozen["case"]["candidate_ids"],
            ["candidate-opaque-a", "candidate-opaque-b", "unknown_or_other"],
        )
        self.assertEqual(frozen["object_dir"], OBJECT_REL.as_posix())
        snapshots = frozen["file_snapshots"]
        self.assertEqual(
            [item["object_relative_path"] for item in snapshots], ALLOWED_FILES
        )
        for snapshot in snapshots:
            source_path = OBJECT_DIR / snapshot["object_relative_path"]
            expected = hashlib.sha256(source_path.read_bytes()).hexdigest()
            self.assertEqual(snapshot["sha256"], expected)
            self.assertEqual(snapshot["size_bytes"], source_path.stat().st_size)
            self.assertEqual(snapshot["source_ancestor_id"], "src-hust-obc")
            self.assertEqual(
                snapshot["derivative_family_id"], "hust-obc-und-L-000001"
            )
            self.assertEqual(snapshot["rights_status"], "research_use_only")
            self.assertTrue(snapshot["risk_note"])
        self.assertRegex(frozen["frozen_input_sha256"], r"^[0-9a-f]{64}$")
        self.assertRegex(
            frozen["case_candidate_manifest_sha256"], r"^[0-9a-f]{64}$"
        )

    def test_freeze_rejects_answer_bearing_metadata_field(self):
        metadata = self._case_metadata()
        metadata["gold_candidate_id"] = "candidate-opaque-a"
        metadata_path = self._write_metadata(metadata)
        output_path = self.work_dir / "must-not-exist.json"

        result = self._freeze(metadata_path, output_path)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("answer-bearing metadata field", result.stderr)
        self.assertFalse(output_path.exists())

    def test_freeze_rejects_answer_bearing_allowed_path_before_file_lookup(self):
        metadata = self._case_metadata()
        metadata["files"]["gold-label.json"] = metadata["files"].pop(
            ALLOWED_FILES[0]
        )
        metadata_path = self._write_metadata(metadata)
        output_path = self.work_dir / "must-not-exist.json"

        result = self._run(
            "freeze",
            "--object-dir",
            str(OBJECT_DIR),
            "--case-metadata",
            str(metadata_path),
            "--allowed-file",
            "gold-label.json",
            "--allowed-file",
            ALLOWED_FILES[1],
            "--candidate-id",
            "candidate-opaque-a",
            "--candidate-id",
            "candidate-opaque-b",
            "--candidate-id",
            "unknown_or_other",
            "--output",
            str(output_path),
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("answer-bearing allowed path", result.stderr)
        self.assertNotIn("does not exist", result.stderr)
        self.assertFalse(output_path.exists())

    def test_freeze_rejects_candidate_universe_without_unknown(self):
        metadata_path = self._write_metadata(self._case_metadata())
        output_path = self.work_dir / "must-not-exist.json"

        arguments = [
            "freeze",
            "--object-dir",
            str(OBJECT_DIR),
            "--case-metadata",
            str(metadata_path),
            "--candidate-id",
            "candidate-opaque-a",
            "--candidate-id",
            "candidate-opaque-b",
            "--candidate-id",
            "candidate-opaque-c",
            "--output",
            str(output_path),
        ]
        for relative_path in ALLOWED_FILES:
            arguments.extend(["--allowed-file", relative_path])
        result = self._run(*arguments)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unknown_or_other", result.stderr)
        self.assertFalse(output_path.exists())

    def test_freeze_rejects_answer_bearing_candidate_id(self):
        metadata_path = self._write_metadata(self._case_metadata())
        output_path = self.work_dir / "must-not-exist.json"
        arguments = [
            "freeze",
            "--object-dir",
            str(OBJECT_DIR),
            "--case-metadata",
            str(metadata_path),
            "--candidate-id",
            "candidate-reading-jia",
            "--candidate-id",
            "candidate-opaque-b",
            "--candidate-id",
            "unknown_or_other",
            "--output",
            str(output_path),
        ]
        for relative_path in ALLOWED_FILES:
            arguments.extend(["--allowed-file", relative_path])

        result = self._run(*arguments)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("answer-bearing candidate ID", result.stderr)
        self.assertFalse(output_path.exists())

    def test_freeze_rejects_semantic_looking_candidate_id_without_token(self):
        metadata_path = self._write_metadata(self._case_metadata())
        output_path = self.work_dir / "must-not-exist.json"
        arguments = [
            "freeze",
            "--object-dir",
            str(OBJECT_DIR),
            "--case-metadata",
            str(metadata_path),
            "--candidate-id",
            "candidate-jia",
            "--candidate-id",
            "candidate-7532",
            "--candidate-id",
            "unknown_or_other",
            "--output",
            str(output_path),
        ]
        for relative_path in ALLOWED_FILES:
            arguments.extend(["--allowed-file", relative_path])

        result = self._run(*arguments)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("opaque ASCII", result.stderr)
        self.assertFalse(output_path.exists())

    def test_freeze_rejects_answer_bearing_blind_alias(self):
        metadata = self._case_metadata()
        metadata["blind_alias"] = "blind-reading-jia"
        metadata_path = self._write_metadata(metadata)
        output_path = self.work_dir / "must-not-exist.json"

        result = self._freeze(metadata_path, output_path)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("answer-bearing blind_alias", result.stderr)
        self.assertFalse(output_path.exists())

    def test_freeze_rejects_semantic_looking_blind_alias(self):
        metadata = self._case_metadata()
        metadata["blind_alias"] = "blind-jia"
        metadata_path = self._write_metadata(metadata)
        output_path = self.work_dir / "must-not-exist.json"

        result = self._freeze(metadata_path, output_path)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("opaque blind-case", result.stderr)
        self.assertFalse(output_path.exists())

    def test_freeze_requires_an_ignored_output_path(self):
        metadata_path = self._write_metadata(self._case_metadata())
        output_path = ROOT / "tests/forbidden-pilot-output.json"

        result = self._freeze(metadata_path, output_path)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("output path must be Git-ignored", result.stderr)
        self.assertFalse(output_path.exists())

    def test_seal_writes_only_schema_007_hmac_commitment_publicly(self):
        frozen_path, frozen = self._prepare_frozen_case()
        self._write_run_report(frozen)
        labels = [
            {
                "case_id": frozen["case"]["case_id"],
                "gold_candidate_id": "candidate-opaque-a",
            }
        ]
        private_gold = {
            "benchmark_id": "ai-benchmark-diagnostic-000001",
            "benchmark_version": "2.0.0",
            "gold_key_id": "gold-key-diagnostic-000001",
            "case_candidate_manifest_sha256": frozen[
                "case_candidate_manifest_sha256"
            ],
            "protocol_sha256": hashlib.sha256(
                (self.work_dir / "prompt-manifest.md").read_bytes()
            ).hexdigest(),
            "labels": labels,
            "commitment_key_hex": "11" * 32,
        }
        private_path = self.work_dir / "private-gold.json"
        private_path.write_text(
            json.dumps(private_gold, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        public_path = self.work_dir / "public-commitment.json"

        result = self._run(
            "seal",
            "--frozen-case",
            str(frozen_path),
            "--private-gold",
            str(private_path),
            "--sealed-at",
            "2026-08-12T00:00:00Z",
            "--output",
            str(public_path),
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS diagnostic gold commitment", result.stdout)
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
        message = json.dumps(
            committed_payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        expected = hmac.new(bytes.fromhex("11" * 32), message, hashlib.sha256)
        public = json.loads(public_path.read_text(encoding="utf-8"))
        self.assertEqual(public["commitment"], expected.hexdigest())
        self.assertEqual(public["commitment_scheme"], "hmac-sha256")
        self.assertEqual(public["storage_class"], "ignored_local_diagnostic")
        self.assertEqual(
            public["frozen_input_sha256"],
            frozen["frozen_input_sha256"],
        )
        self.assertEqual(public["diagnostic_status"], "diagnostic_only")
        self.assertEqual(
            public["benchmark_eligibility"], "pretraining_exposure_unknown"
        )
        self.assertEqual(public["probability_status"], "not_generated")
        self.assertEqual(public["gate3_status"], "not_attempted")
        serialized = public_path.read_text(encoding="utf-8")
        self.assertNotIn("labels", public)
        self.assertNotIn("commitment_key_hex", public)
        self.assertNotIn("gold_candidate_id", serialized)
        self.assertNotIn("candidate-opaque-a", serialized)

    def test_seal_rejects_private_gold_outside_ignored_storage(self):
        private_path = ROOT / "tests/forbidden-private-gold.json"
        private_path.write_text("{}\n", encoding="utf-8")
        self.addCleanup(private_path.unlink, missing_ok=True)
        public_path = self.work_dir / "must-not-exist.json"

        result = self._run(
            "seal",
            "--frozen-case",
            str(self.work_dir / "missing-frozen-case.json"),
            "--private-gold",
            str(private_path),
            "--sealed-at",
            "2026-08-12T00:00:00Z",
            "--output",
            str(public_path),
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("private gold path must be Git-ignored", result.stderr)
        self.assertFalse(public_path.exists())

    def test_seal_rejects_gold_for_a_case_outside_the_frozen_case(self):
        frozen_path, frozen = self._prepare_frozen_case()
        self._write_run_report(frozen)
        private_gold = self._private_gold(frozen)
        private_gold["labels"][0]["case_id"] = "case-diagnostic-999999"
        private_path = self.work_dir / "private-gold.json"
        private_path.write_text(json.dumps(private_gold), encoding="utf-8")
        public_path = self.work_dir / "must-not-exist.json"

        result = self._run(
            "seal",
            "--frozen-case",
            str(frozen_path),
            "--private-gold",
            str(private_path),
            "--sealed-at",
            "2026-08-12T00:00:00Z",
            "--output",
            str(public_path),
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("label cases must exactly match", result.stderr)
        self.assertFalse(public_path.exists())

    def test_seal_rejects_gold_candidate_outside_the_frozen_universe(self):
        frozen_path, frozen = self._prepare_frozen_case()
        self._write_run_report(frozen)
        private_gold = self._private_gold(frozen)
        private_gold["labels"][0]["gold_candidate_id"] = (
            "candidate-opaque-c"
        )
        private_path = self.work_dir / "private-gold.json"
        private_path.write_text(json.dumps(private_gold), encoding="utf-8")
        public_path = self.work_dir / "must-not-exist.json"

        result = self._run(
            "seal",
            "--frozen-case",
            str(frozen_path),
            "--private-gold",
            str(private_path),
            "--sealed-at",
            "2026-08-12T00:00:00Z",
            "--output",
            str(public_path),
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("outside the frozen candidate universe", result.stderr)
        self.assertFalse(public_path.exists())

    def test_seal_rejects_a_manifest_not_bound_to_the_frozen_case(self):
        frozen_path, frozen = self._prepare_frozen_case()
        self._write_run_report(frozen)
        private_gold = self._private_gold(frozen)
        private_gold["case_candidate_manifest_sha256"] = "f" * 64
        private_path = self.work_dir / "private-gold.json"
        private_path.write_text(json.dumps(private_gold), encoding="utf-8")
        public_path = self.work_dir / "must-not-exist.json"

        result = self._run(
            "seal",
            "--frozen-case",
            str(frozen_path),
            "--private-gold",
            str(private_path),
            "--sealed-at",
            "2026-08-12T00:00:00Z",
            "--output",
            str(public_path),
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not bind the frozen candidate manifest", result.stderr)
        self.assertFalse(public_path.exists())

    def test_seal_rejects_a_timestamp_before_the_evidence_cutoff(self):
        frozen_path, frozen = self._prepare_frozen_case()
        self._write_run_report(frozen)
        private_path = self.work_dir / "private-gold.json"
        private_path.write_text(
            json.dumps(self._private_gold(frozen)),
            encoding="utf-8",
        )
        public_path = self.work_dir / "must-not-exist.json"

        result = self._run(
            "seal",
            "--frozen-case",
            str(frozen_path),
            "--private-gold",
            str(private_path),
            "--sealed-at",
            "2026-08-11T23:59:59Z",
            "--output",
            str(public_path),
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("before the evidence cutoff", result.stderr)
        self.assertFalse(public_path.exists())

    def test_freeze_refuses_to_overwrite_an_existing_output_file(self):
        metadata_path = self._write_metadata(self._case_metadata())
        output_path = self.work_dir / "frozen-case.json"
        output_path.write_text("preserve me\n", encoding="utf-8")

        result = self._freeze(metadata_path, output_path)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("output already exists", result.stderr)
        self.assertEqual(
            output_path.read_text(encoding="utf-8"),
            "preserve me\n",
        )

    def test_freeze_rejects_non_corpus_object_before_reading_input(self):
        object_dir = self.work_dir / "diagnostic-object"
        object_dir.mkdir()
        evidence_path = object_dir / "evidence.md"
        evidence_path.write_text("irreplaceable evidence\n", encoding="utf-8")
        metadata = self._case_metadata()
        metadata["files"] = {
            "evidence.md": self._case_metadata()["files"][ALLOWED_FILES[0]]
        }
        metadata_path = self._write_metadata(metadata)

        result = self._run(
            "freeze",
            "--object-dir",
            str(object_dir),
            "--case-metadata",
            str(metadata_path),
            "--allowed-file",
            "evidence.md",
            "--candidate-id",
            "candidate-opaque-a",
            "--candidate-id",
            "candidate-opaque-b",
            "--candidate-id",
            "unknown_or_other",
            "--output",
            str(evidence_path),
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("human-facing object directory under corpus", result.stderr)
        self.assertEqual(
            evidence_path.read_text(encoding="utf-8"),
            "irreplaceable evidence\n",
        )

    def test_freeze_rejects_non_corpus_object_before_duplicate_check(self):
        object_dir = self.work_dir / "diagnostic-object"
        object_dir.mkdir()
        for name in ("evidence-a.md", "evidence-b.md"):
            (object_dir / name).write_text(
                "identical evidence\n",
                encoding="utf-8",
            )
        source = self._case_metadata()["files"][ALLOWED_FILES[0]]
        metadata = self._case_metadata()
        metadata["files"] = {
            "evidence-a.md": source,
            "evidence-b.md": source,
        }
        metadata_path = self._write_metadata(metadata)
        output_path = self.work_dir / "must-not-exist.json"

        result = self._run(
            "freeze",
            "--object-dir",
            str(object_dir),
            "--case-metadata",
            str(metadata_path),
            "--allowed-file",
            "evidence-a.md",
            "--allowed-file",
            "evidence-b.md",
            "--candidate-id",
            "candidate-opaque-a",
            "--candidate-id",
            "candidate-opaque-b",
            "--candidate-id",
            "unknown_or_other",
            "--output",
            str(output_path),
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("human-facing object directory under corpus", result.stderr)
        self.assertFalse(output_path.exists())

    def test_freeze_rejects_non_object_directory_inside_corpus(self):
        corpus_work = ROOT / "corpus" / ".working"
        corpus_work.mkdir(exist_ok=True)
        route_parent = corpus_work / "pilot-routes"
        route_parent.mkdir(exist_ok=True)
        object_dir = Path(tempfile.mkdtemp(prefix="pilot-route-", dir=route_parent))
        try:
            evidence_path = object_dir / "evidence.md"
            evidence_path.write_text(
                "route-only test evidence\n", encoding="utf-8"
            )
            metadata = self._case_metadata()
            metadata["files"] = {
                "evidence.md": self._case_metadata()["files"][ALLOWED_FILES[0]]
            }
            metadata_path = self._write_metadata(metadata)
            output_path = self.work_dir / "must-not-exist.json"
            result = self._run(
                "freeze",
                "--object-dir",
                str(object_dir),
                "--case-metadata",
                str(metadata_path),
                "--allowed-file",
                "evidence.md",
                "--candidate-id",
                "candidate-opaque-a",
                "--candidate-id",
                "candidate-opaque-b",
                "--candidate-id",
                "unknown_or_other",
                "--output",
                str(output_path),
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("registered object directory under corpus", result.stderr)
            self.assertFalse(output_path.exists())
        finally:
            shutil.rmtree(object_dir, ignore_errors=True)

    def test_seal_rejects_a_frozen_object_outside_corpus_scope(self):
        frozen_path, frozen = self._prepare_frozen_case()
        self._write_run_report(frozen)
        frozen["object_dir"] = "doc/public/user_research"
        binding = {
            "object_dir": frozen["object_dir"],
            "case": frozen["case"],
            "file_snapshots": frozen["file_snapshots"],
        }
        frozen["frozen_input_sha256"] = hashlib.sha256(
            json.dumps(
                binding,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        frozen_path.write_text(
            json.dumps(frozen, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        private_path = self.work_dir / "private-gold.json"
        private_path.write_text(
            json.dumps(self._private_gold(frozen)),
            encoding="utf-8",
        )
        output_path = self.work_dir / "must-not-exist.json"
        result = self._run(
            "seal",
            "--frozen-case",
            str(frozen_path),
            "--private-gold",
            str(private_path),
            "--sealed-at",
            "2026-08-12T00:00:00Z",
            "--output",
            str(output_path),
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("human-facing object directory under corpus", result.stderr)
        self.assertFalse(output_path.exists())

    def test_seal_refuses_to_overwrite_an_existing_output(self):
        frozen_path, frozen = self._prepare_frozen_case()
        self._write_run_report(frozen)
        private_path, public_path, first = self._seal_gold(
            frozen_path,
            frozen,
        )
        self.assertEqual(first.returncode, 0, first.stderr)
        original = public_path.read_bytes()

        second = self._run(
            "seal",
            "--frozen-case",
            str(frozen_path),
            "--private-gold",
            str(private_path),
            "--sealed-at",
            "2026-08-12T00:00:00Z",
            "--output",
            str(public_path),
        )

        self.assertNotEqual(second.returncode, 0)
        self.assertIn("output already exists", second.stderr)
        self.assertEqual(public_path.read_bytes(), original)

    def test_lock_run_binds_blind_evidence_and_withholds_uncalibrated_output(self):
        frozen_path, frozen, report_path, opening_path = (
            self._prepare_run_chain()
        )
        output_path = self.work_dir / "locked-run.json"

        result = self._lock_run(frozen_path, report_path, output_path)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS diagnostic locked run", result.stdout)
        locked = json.loads(output_path.read_text(encoding="utf-8"))
        self.assertEqual(
            locked["record_type"], "ai_benchmark_diagnostic_locked_run"
        )
        self.assertEqual(locked["diagnostic_status"], "diagnostic_only")
        self.assertEqual(
            locked["probability_status"], "uncalibrated_agent_distribution"
        )
        self.assertEqual(locked["delivery_status"], "withheld")
        self.assertEqual(locked["calibration_status"], "not_calibrated")
        self.assertEqual(
            locked["frozen_input_sha256"], frozen["frozen_input_sha256"]
        )
        self.assertEqual(
            locked["case_candidate_manifest_sha256"],
            frozen["case_candidate_manifest_sha256"],
        )
        self.assertEqual(
            locked["run_opening_sha256"],
            hashlib.sha256(opening_path.read_bytes()).hexdigest(),
        )
        run = locked["run"]
        self.assertEqual(run["prediction"]["action"], "abstain")
        self.assertIsNone(run["prediction"]["selected_candidate_id"])
        canonical = json.dumps(
            run,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        self.assertEqual(
            locked["prediction_lock_sha256"],
            hashlib.sha256(canonical).hexdigest(),
        )
        serialized = output_path.read_text(encoding="utf-8")
        self.assertNotIn("gold_candidate_id", serialized)
        self.assertNotIn("commitment_key_hex", serialized)

    def test_lock_run_rejects_candidate_universe_mismatch(self):
        frozen_path, frozen, report_path, _ = self._prepare_run_chain()
        report = json.loads(report_path.read_text(encoding="utf-8"))
        report["prediction"]["ranked_candidates"][1]["candidate_id"] = (
            "candidate-opaque-c"
        )
        self._rewrite_agent_prediction(report_path, report)
        output_path = self.work_dir / "must-not-exist.json"

        result = self._lock_run(frozen_path, report_path, output_path)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("candidate universe", result.stderr)
        self.assertFalse(output_path.exists())

    def test_lock_run_rejects_evidence_outside_frozen_snapshot(self):
        frozen_path, frozen, report_path, _ = self._prepare_run_chain()
        report = json.loads(report_path.read_text(encoding="utf-8"))
        report["prediction"]["supporting_evidence"]["items"][0][
            "snapshot_sha256"
        ] = "f" * 64
        self._rewrite_agent_prediction(report_path, report)
        output_path = self.work_dir / "must-not-exist.json"

        result = self._lock_run(frozen_path, report_path, output_path)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("outside the frozen evidence", result.stderr)
        self.assertFalse(output_path.exists())

    def test_lock_run_rejects_peer_output_or_gold_access(self):
        frozen_path, frozen, report_path, _ = self._prepare_run_chain()
        report = json.loads(report_path.read_text(encoding="utf-8"))
        report["prior_run_output_access"] = "primary_output"
        report["gold_access"] = "available"
        report_path.write_text(json.dumps(report), encoding="utf-8")
        output_path = self.work_dir / "must-not-exist.json"

        result = self._lock_run(frozen_path, report_path, output_path)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("prior run output access", result.stderr)
        self.assertFalse(output_path.exists())

    def test_lock_run_rejects_prompt_manifest_drift(self):
        frozen_path, frozen, report_path, _ = self._prepare_run_chain()
        prompt_path = self.work_dir / "prompt-manifest.md"
        prompt_path.write_text("changed after the Agent run\n", encoding="utf-8")
        output_path = self.work_dir / "must-not-exist.json"

        result = self._lock_run(frozen_path, report_path, output_path)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("prompt manifest SHA-256", result.stderr)
        self.assertFalse(output_path.exists())

    def test_lock_run_rejects_agent_output_drift(self):
        frozen_path, frozen, report_path, _ = self._prepare_run_chain()
        agent_output_path = self.work_dir / "agent-output.json"
        agent_output_path.write_text("{}\n", encoding="utf-8")
        output_path = self.work_dir / "must-not-exist.json"

        result = self._lock_run(frozen_path, report_path, output_path)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Agent output SHA-256", result.stderr)
        self.assertFalse(output_path.exists())

    def test_lock_run_rejects_duplicate_json_keys_in_agent_output(self):
        frozen_path, frozen, report_path, _ = self._prepare_run_chain()
        report = json.loads(report_path.read_text(encoding="utf-8"))
        agent_output_path = self.work_dir / "agent-output.json"
        raw = agent_output_path.read_text(encoding="utf-8")
        raw = raw.replace(
            '"case_id":',
            '"case_id":"wrong-duplicate","case_id":',
            1,
        )
        agent_output_path.write_text(raw, encoding="utf-8")
        report["agent_output_sha256"] = hashlib.sha256(
            agent_output_path.read_bytes()
        ).hexdigest()
        report_path.write_text(json.dumps(report), encoding="utf-8")
        output_path = self.work_dir / "must-not-exist.json"

        result = self._lock_run(frozen_path, report_path, output_path)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("duplicate JSON key", result.stderr)
        self.assertFalse(output_path.exists())

    def test_lock_run_rejects_predicting_a_tied_top_candidate(self):
        frozen_path, frozen, report_path, _ = self._prepare_run_chain()
        report = json.loads(report_path.read_text(encoding="utf-8"))
        prediction = report["prediction"]
        prediction["ranked_candidates"][0]["probability"] = 0.4
        prediction["ranked_candidates"][1]["probability"] = 0.4
        prediction["ranked_candidates"][2]["probability"] = 0.2
        prediction["action"] = "predict"
        prediction["selected_candidate_id"] = "candidate-opaque-a"
        prediction["abstention_reason_code"] = None
        self._rewrite_agent_prediction(report_path, report)
        output_path = self.work_dir / "must-not-exist.json"

        result = self._lock_run(frozen_path, report_path, output_path)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("strictly exceed rank two", result.stderr)
        self.assertFalse(output_path.exists())

    def test_lock_run_rejects_confirmed_gold_or_peer_leakage(self):
        frozen_path, frozen, report_path, _ = self._prepare_run_chain()
        report = json.loads(report_path.read_text(encoding="utf-8"))
        leakage = report["prediction"]["leakage_assessment"]
        leakage["status"] = "confirmed"
        leakage["types"] = ["gold_label", "peer_output"]
        self._rewrite_agent_prediction(report_path, report)
        output_path = self.work_dir / "must-not-exist.json"

        result = self._lock_run(frozen_path, report_path, output_path)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("contradicts sealed run access", result.stderr)
        self.assertFalse(output_path.exists())

    def test_lock_run_rejects_report_identity_drift_from_run_opening(self):
        frozen_path, _, report_path, _ = self._prepare_run_chain()
        report = json.loads(report_path.read_text(encoding="utf-8"))
        report["run_id"] = "pilot-run-primary-999999"
        report_path.write_text(json.dumps(report), encoding="utf-8")
        output_path = self.work_dir / "must-not-exist.json"

        result = self._lock_run(frozen_path, report_path, output_path)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("run report run_id does not match run opening", result.stderr)
        self.assertFalse(output_path.exists())

    def test_lock_run_rejects_a_broken_opening_lock(self):
        frozen_path, _, report_path, opening_path = self._prepare_run_chain()
        opening = json.loads(opening_path.read_text(encoding="utf-8"))
        opening["context_id"] = "tampered-context"
        opening_path.write_text(json.dumps(opening), encoding="utf-8")
        output_path = self.work_dir / "must-not-exist.json"

        result = self._lock_run(frozen_path, report_path, output_path)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("opening lock SHA-256 does not match", result.stderr)
        self.assertFalse(output_path.exists())

    def test_lock_run_rejects_a_run_started_before_its_opening(self):
        frozen_path, _, report_path, _ = self._prepare_run_chain()
        report = json.loads(report_path.read_text(encoding="utf-8"))
        report["started_at"] = "2026-08-12T00:00:59Z"
        report_path.write_text(json.dumps(report), encoding="utf-8")
        output_path = self.work_dir / "must-not-exist.json"

        result = self._lock_run(frozen_path, report_path, output_path)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("sealed < opened < started < completed < locked", result.stderr)
        self.assertFalse(output_path.exists())

    def test_lock_run_rejects_boolean_candidate_rank(self):
        frozen_path, _, report_path, _ = self._prepare_run_chain()
        report = json.loads(report_path.read_text(encoding="utf-8"))
        report["prediction"]["ranked_candidates"][0]["rank"] = True
        self._rewrite_agent_prediction(report_path, report)
        output_path = self.work_dir / "must-not-exist.json"

        result = self._lock_run(frozen_path, report_path, output_path)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("rank must be an integer", result.stderr)
        self.assertFalse(output_path.exists())

    def test_lock_run_rejects_predict_without_support_for_selected_candidate(self):
        frozen_path, _, report_path, _ = self._prepare_run_chain()
        report = json.loads(report_path.read_text(encoding="utf-8"))
        prediction = report["prediction"]
        prediction["action"] = "predict"
        prediction["selected_candidate_id"] = "candidate-opaque-a"
        prediction["abstention_reason_code"] = None
        prediction["supporting_evidence"]["items"][0][
            "target_candidate_id"
        ] = "candidate-opaque-b"
        self._rewrite_agent_prediction(report_path, report)
        output_path = self.work_dir / "must-not-exist.json"

        result = self._lock_run(frozen_path, report_path, output_path)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("supporting evidence for the selected candidate", result.stderr)
        self.assertFalse(output_path.exists())

    def test_lock_run_requires_abstention_when_selected_falsifier_triggered(self):
        frozen_path, _, report_path, _ = self._prepare_run_chain()
        report = json.loads(report_path.read_text(encoding="utf-8"))
        prediction = report["prediction"]
        prediction["action"] = "predict"
        prediction["selected_candidate_id"] = "candidate-opaque-a"
        prediction["abstention_reason_code"] = None
        prediction["falsification_checks"][0]["outcome"] = "triggered"
        self._rewrite_agent_prediction(report_path, report)
        output_path = self.work_dir / "must-not-exist.json"

        result = self._lock_run(frozen_path, report_path, output_path)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("triggered falsifier requires abstention", result.stderr)
        self.assertFalse(output_path.exists())

    def test_lock_run_rejects_no_leakage_status_with_reported_types(self):
        frozen_path, _, report_path, _ = self._prepare_run_chain()
        report = json.loads(report_path.read_text(encoding="utf-8"))
        leakage = report["prediction"]["leakage_assessment"]
        leakage["status"] = "screened_no_known_leakage"
        leakage["types"] = ["pretraining_unknown"]
        self._rewrite_agent_prediction(report_path, report)
        output_path = self.work_dir / "must-not-exist.json"

        result = self._lock_run(frozen_path, report_path, output_path)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("cannot report leakage types", result.stderr)
        self.assertFalse(output_path.exists())

    def test_lock_run_refuses_to_overwrite_an_existing_output(self):
        frozen_path, _, report_path, _ = self._prepare_run_chain()
        output_path = self.work_dir / "locked-run.json"
        first = self._lock_run(frozen_path, report_path, output_path)
        self.assertEqual(first.returncode, 0, first.stderr)
        original = output_path.read_bytes()

        second = self._lock_run(frozen_path, report_path, output_path)

        self.assertNotEqual(second.returncode, 0)
        self.assertIn("output already exists", second.stderr)
        self.assertEqual(output_path.read_bytes(), original)

    def test_open_run_locks_prompt_case_gold_and_independence_before_dispatch(self):
        frozen_path, frozen = self._prepare_frozen_case()
        self._write_run_report(frozen)
        private_gold = {
            "benchmark_id": "ai-benchmark-diagnostic-000001",
            "benchmark_version": "2.0.0",
            "gold_key_id": "gold-key-diagnostic-000001",
            "case_candidate_manifest_sha256": frozen[
                "case_candidate_manifest_sha256"
            ],
            "protocol_sha256": hashlib.sha256(
                (self.work_dir / "prompt-manifest.md").read_bytes()
            ).hexdigest(),
            "labels": [
                {
                    "case_id": frozen["case"]["case_id"],
                    "gold_candidate_id": "unknown_or_other",
                }
            ],
            "commitment_key_hex": "11" * 32,
        }
        private_path = self.work_dir / "private-gold.json"
        private_path.write_text(json.dumps(private_gold), encoding="utf-8")
        public_path = self.work_dir / "public-commitment.json"
        seal = self._run(
            "seal",
            "--frozen-case",
            str(frozen_path),
            "--private-gold",
            str(private_path),
            "--sealed-at",
            "2026-08-12T00:00:00Z",
            "--output",
            str(public_path),
        )
        self.assertEqual(seal.returncode, 0, seal.stderr)
        output_path = self.work_dir / "run-opening.json"

        result = self._open_run(frozen_path, output_path)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS diagnostic run opening", result.stdout)
        opening = json.loads(output_path.read_text(encoding="utf-8"))
        self.assertEqual(
            opening["record_type"], "ai_benchmark_diagnostic_run_opening"
        )
        self.assertEqual(opening["gold_sealed_at"], "2026-08-12T00:00:00Z")
        self.assertEqual(opening["opened_at"], "2026-08-12T00:01:00Z")
        self.assertEqual(
            opening["frozen_input_sha256"], frozen["frozen_input_sha256"]
        )
        self.assertEqual(
            opening["prompt_manifest_sha256"],
            hashlib.sha256(
                (self.work_dir / "prompt-manifest.md").read_bytes()
            ).hexdigest(),
        )
        self.assertEqual(opening["prior_run_output_access"], "none")
        self.assertEqual(opening["gold_access"], "sealed_unavailable")
        serialized = output_path.read_text(encoding="utf-8")
        self.assertNotIn("gold_candidate_id", serialized)
        self.assertNotIn("commitment_key_hex", serialized)

    def test_open_run_refuses_to_overwrite_an_existing_output(self):
        frozen_path, _, _, opening_path = self._prepare_run_chain()
        original = opening_path.read_bytes()

        result = self._open_run(frozen_path, opening_path)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("output already exists", result.stderr)
        self.assertEqual(opening_path.read_bytes(), original)

    def test_open_run_rejects_dispatch_before_gold_seal(self):
        frozen_path, frozen = self._prepare_frozen_case()
        self._write_run_report(frozen)
        public_path = self.work_dir / "public-commitment.json"
        public_path.write_text(
            json.dumps(
                {
                    "record_type": "ai_benchmark_diagnostic_gold_commitment",
                    "diagnostic_status": "diagnostic_only",
                    "gold_key_id": "gold-key-diagnostic-000001",
                    "frozen_input_sha256": frozen["frozen_input_sha256"],
                    "case_candidate_manifest_sha256": frozen[
                        "case_candidate_manifest_sha256"
                    ],
                    "protocol_sha256": hashlib.sha256(
                        (self.work_dir / "prompt-manifest.md").read_bytes()
                    ).hexdigest(),
                    "sealed_at": "2026-08-12T00:02:00Z",
                    "agent_access": "none",
                    "unseal_status": "sealed",
                    "commitment": "a" * 64,
                }
            ),
            encoding="utf-8",
        )
        output_path = self.work_dir / "must-not-exist.json"

        result = self._open_run(frozen_path, output_path)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("gold must be sealed before opening a run", result.stderr)
        self.assertFalse(output_path.exists())

    def test_open_run_rejects_gold_sealed_before_the_evidence_cutoff(self):
        frozen_path, frozen = self._prepare_frozen_case()
        self._write_run_report(frozen)
        public_path = self.work_dir / "public-commitment.json"
        public_path.write_text(
            json.dumps(
                {
                    "record_type": "ai_benchmark_diagnostic_gold_commitment",
                    "diagnostic_status": "diagnostic_only",
                    "gold_key_id": "gold-key-diagnostic-000001",
                    "frozen_input_sha256": frozen["frozen_input_sha256"],
                    "case_candidate_manifest_sha256": frozen[
                        "case_candidate_manifest_sha256"
                    ],
                    "protocol_sha256": hashlib.sha256(
                        (self.work_dir / "prompt-manifest.md").read_bytes()
                    ).hexdigest(),
                    "sealed_at": "2026-08-11T23:59:59Z",
                    "agent_access": "none",
                    "unseal_status": "sealed",
                    "commitment": "a" * 64,
                }
            ),
            encoding="utf-8",
        )
        output_path = self.work_dir / "must-not-exist.json"

        result = self._open_run(frozen_path, output_path)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("before the evidence cutoff", result.stderr)
        self.assertFalse(output_path.exists())

    def test_open_run_rejects_answer_bearing_prompt_content(self):
        frozen_path, frozen = self._prepare_frozen_case()
        self._write_run_report(frozen)
        prompt_path = self.work_dir / "prompt-manifest.md"
        prompt_path.write_text(
            "gold_candidate_id: candidate-opaque-a\n",
            encoding="utf-8",
        )
        private_gold = {
            "benchmark_id": "ai-benchmark-diagnostic-000002",
            "benchmark_version": "2.0.0",
            "gold_key_id": "gold-key-diagnostic-000002",
            "case_candidate_manifest_sha256": frozen[
                "case_candidate_manifest_sha256"
            ],
            "protocol_sha256": hashlib.sha256(prompt_path.read_bytes()).hexdigest(),
            "labels": [
                {
                    "case_id": frozen["case"]["case_id"],
                    "gold_candidate_id": "unknown_or_other",
                }
            ],
            "commitment_key_hex": "22" * 32,
        }
        private_path = self.work_dir / "private-gold.json"
        private_path.write_text(json.dumps(private_gold), encoding="utf-8")
        public_path = self.work_dir / "public-commitment.json"
        seal = self._run(
            "seal",
            "--frozen-case",
            str(frozen_path),
            "--private-gold",
            str(private_path),
            "--sealed-at",
            "2026-08-12T00:00:00Z",
            "--output",
            str(public_path),
        )
        self.assertEqual(seal.returncode, 0, seal.stderr)
        output_path = self.work_dir / "must-not-exist.json"

        result = self._open_run(frozen_path, output_path)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("answer-bearing prompt content", result.stderr)
        self.assertFalse(output_path.exists())

    def test_score_local_passes_only_when_every_blind_run_matches_null_gold(self):
        frozen_path, public_path, private_path, locked_paths = (
            self._prepare_scoring_inputs()
        )
        public_before = public_path.read_bytes()
        output_path = self.work_dir / "local-score-receipt.json"

        result = self._score_local(
            frozen_path,
            public_path,
            private_path,
            locked_paths,
            output_path,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS local diagnostic score", result.stdout)
        receipt = json.loads(output_path.read_text(encoding="utf-8"))
        self.assertEqual(
            receipt["record_type"],
            "ai_benchmark_local_diagnostic_score_receipt",
        )
        self.assertEqual(
            receipt["pipeline_diagnostic_status"],
            "pipeline_diagnostic_pass",
        )
        self.assertEqual(receipt["query_count"], 1)
        self.assertEqual(receipt["score_query_limit"], 1)
        self.assertEqual(
            receipt["gold_state"],
            "opened_retired_local_diagnostic",
        )
        self.assertEqual(
            receipt["evaluation_state"],
            "retired_after_single_scoring",
        )
        self.assertEqual(receipt["delivery_status"], "withheld")
        self.assertEqual(receipt["gate3_status"], "not_attempted")
        self.assertEqual(len(receipt["runs"]), 2)
        for run in receipt["runs"]:
            self.assertEqual(run["action"], "abstain")
            self.assertIsNone(run["selected_candidate_id"])
            self.assertEqual(run["top1_candidate_id"], "unknown_or_other")
            self.assertIs(run["top1_matches_gold"], True)
            self.assertRegex(run["locked_run_sha256"], r"^[0-9a-f]{64}$")
        serialized = output_path.read_text(encoding="utf-8")
        self.assertNotIn("commitment_key_hex", serialized)
        self.assertNotIn("gold_candidate_id", serialized)
        self.assertEqual(public_path.read_bytes(), public_before)

    def test_score_local_withholds_when_only_one_run_ranks_gold_first(self):
        frozen_path, public_path, private_path, locked_paths = (
            self._prepare_scoring_inputs(
                first_top="unknown_or_other",
                second_top="candidate-opaque-a",
            )
        )
        output_path = self.work_dir / "local-score-receipt.json"

        result = self._score_local(
            frozen_path,
            public_path,
            private_path,
            locked_paths,
            output_path,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        receipt = json.loads(output_path.read_text(encoding="utf-8"))
        self.assertEqual(
            receipt["pipeline_diagnostic_status"],
            "diagnostic_fail_withheld",
        )
        self.assertEqual(
            [run["top1_matches_gold"] for run in receipt["runs"]],
            [True, False],
        )
        self.assertEqual(receipt["delivery_status"], "withheld")

    def test_score_local_rejects_a_commitment_with_the_wrong_hmac(self):
        frozen_path, public_path, private_path, locked_paths = (
            self._prepare_scoring_inputs()
        )
        private_gold = json.loads(private_path.read_text(encoding="utf-8"))
        private_gold["commitment_key_hex"] = "22" * 32
        private_path.write_text(json.dumps(private_gold), encoding="utf-8")
        output_path = self.work_dir / "must-not-exist.json"

        result = self._score_local(
            frozen_path,
            public_path,
            private_path,
            locked_paths,
            output_path,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("HMAC commitment", result.stderr)
        self.assertFalse(output_path.exists())

    def test_score_local_rejects_a_locked_run_bound_to_another_freeze(self):
        frozen_path, public_path, private_path, locked_paths = (
            self._prepare_scoring_inputs()
        )
        locked = json.loads(locked_paths[1].read_text(encoding="utf-8"))
        locked["frozen_input_sha256"] = "0" * 64
        locked_paths[1].write_text(json.dumps(locked), encoding="utf-8")
        output_path = self.work_dir / "must-not-exist.json"

        result = self._score_local(
            frozen_path,
            public_path,
            private_path,
            locked_paths,
            output_path,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("locked run does not bind the frozen input", result.stderr)
        self.assertFalse(output_path.exists())

    def test_score_local_rejects_the_same_run_twice(self):
        frozen_path, public_path, private_path, locked_paths = (
            self._prepare_scoring_inputs()
        )
        output_path = self.work_dir / "must-not-exist.json"

        result = self._score_local(
            frozen_path,
            public_path,
            private_path,
            [locked_paths[0], locked_paths[0]],
            output_path,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("locked run IDs must be unique", result.stderr)
        self.assertFalse(output_path.exists())

    def test_score_local_refuses_to_overwrite_an_existing_receipt(self):
        frozen_path, public_path, private_path, locked_paths = (
            self._prepare_scoring_inputs()
        )
        output_path = self.work_dir / "local-score-receipt.json"
        first = self._score_local(
            frozen_path,
            public_path,
            private_path,
            locked_paths,
            output_path,
        )
        self.assertEqual(first.returncode, 0, first.stderr)
        original = output_path.read_bytes()

        second = self._score_local(
            frozen_path,
            public_path,
            private_path,
            locked_paths,
            output_path,
        )

        self.assertNotEqual(second.returncode, 0)
        self.assertIn("output already exists", second.stderr)
        self.assertEqual(output_path.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
