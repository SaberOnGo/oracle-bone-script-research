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

    def test_freeze_rejects_answer_bearing_blind_alias(self):
        metadata = self._case_metadata()
        metadata["blind_alias"] = "blind-reading-jia"
        metadata_path = self._write_metadata(metadata)
        output_path = self.work_dir / "must-not-exist.json"

        result = self._freeze(metadata_path, output_path)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("answer-bearing blind_alias", result.stderr)
        self.assertFalse(output_path.exists())

    def test_freeze_requires_an_ignored_output_path(self):
        metadata_path = self._write_metadata(self._case_metadata())
        output_path = ROOT / "tests/forbidden-pilot-output.json"

        result = self._freeze(metadata_path, output_path)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("output path must be Git-ignored", result.stderr)
        self.assertFalse(output_path.exists())

    def test_seal_writes_only_schema_007_hmac_commitment_publicly(self):
        labels = [
            {
                "case_id": "case-diagnostic-000001",
                "gold_candidate_id": "candidate-opaque-a",
            }
        ]
        private_gold = {
            "benchmark_id": "ai-benchmark-diagnostic-000001",
            "benchmark_version": "2.0.0",
            "gold_key_id": "gold-key-diagnostic-000001",
            "case_candidate_manifest_sha256": "a" * 64,
            "protocol_sha256": "b" * 64,
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


if __name__ == "__main__":
    unittest.main()
