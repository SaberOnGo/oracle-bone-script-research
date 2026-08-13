"""Regression tests for the human research material gate CLI contract."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = (
    REPO_ROOT / "tools" / "validation" / "check_human_research_material_gate.py"
)
BASELINE_PATH = (
    REPO_ROOT / "tools" / "validation" / "human_research_material_gate_baseline.json"
)


def load_gate_module():
    """Load the gate as a fresh module so each test owns its patches."""

    name = "check_human_research_material_gate_contract_test"
    spec = importlib.util.spec_from_file_location(name, SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def write_baseline(root: Path, *, minimum_count: int) -> None:
    path = root / "tools" / "validation"
    path.mkdir(parents=True)
    payload = {
        "version": 2,
        "purpose": "test fixture",
        "note": "test fixture",
        "minimums": {"scanned_markdown_count": minimum_count},
        "maximums": {
            "machine_dominant_docs": 0,
            "missing_core_research_docs": 0,
            "modern_label_risk_docs": 0,
            "mojibake_docs": 0,
        },
    }
    (path / "human_research_material_gate_baseline.json").write_text(
        json.dumps(payload), encoding="utf-8"
    )


class HumanResearchMaterialGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_gate_module()

    def bad_score(self):
        return self.module.DocumentScore(
            path="corpus/bad.md",
            machine_hits=2,
            research_hits=0,
            missing_slots=["glyph_image", "scholarship", "inscription"],
            mojibake_hits=[],
            modern_label_risk=False,
        )

    def clean_score(self):
        return self.module.DocumentScore(
            path="corpus/clean.md",
            machine_hits=0,
            research_hits=8,
            missing_slots=[],
            mojibake_hits=[],
            modern_label_risk=False,
        )

    def run_main(self, argv: list[str]):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            result = self.module.main(argv)
        return result, stdout.getvalue(), stderr.getvalue()

    def test_summary_strict_full_cannot_bypass_failure_and_scans_once(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_baseline(root, minimum_count=1)
            fake_path = root / "corpus" / "bad.md"
            with (
                mock.patch.object(
                    self.module, "iter_human_markdown", return_value=[fake_path]
                ) as iter_mock,
                mock.patch.object(
                    self.module, "score_markdown", return_value=self.bad_score()
                ) as score_mock,
            ):
                result, stdout, stderr = self.run_main(
                    ["--root", str(root), "--summary", "--strict", "--full"]
                )

        self.assertEqual(result, 1)
        self.assertEqual(json.loads(stdout)["scanned_markdown_count"], 1)
        self.assertNotIn("FAIL", stdout)
        self.assertIn("FAIL human research material gate", stderr)
        self.assertIn("dominated by machine-route language", stderr)
        iter_mock.assert_called_once_with(root.resolve(), True)
        score_mock.assert_called_once_with(fake_path, root.resolve())

    def test_summary_strict_full_enforces_coverage_floor(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_baseline(root, minimum_count=2)
            fake_path = root / "corpus" / "clean.md"
            with (
                mock.patch.object(
                    self.module, "iter_human_markdown", return_value=[fake_path]
                ),
                mock.patch.object(
                    self.module, "score_markdown", return_value=self.clean_score()
                ),
            ):
                result, stdout, stderr = self.run_main(
                    ["--root", str(root), "--summary", "--strict", "--full"]
                )

        self.assertEqual(result, 1)
        self.assertEqual(json.loads(stdout)["scanned_markdown_count"], 1)
        self.assertIn("scanned_markdown_count", stderr)
        self.assertIn("below baseline minimum 2", stderr)

    def test_summary_full_enforces_debt_ceiling(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_baseline(root, minimum_count=1)
            fake_path = root / "corpus" / "bad.md"
            with (
                mock.patch.object(
                    self.module, "iter_human_markdown", return_value=[fake_path]
                ),
                mock.patch.object(
                    self.module, "score_markdown", return_value=self.bad_score()
                ),
            ):
                result, stdout, stderr = self.run_main(
                    ["--root", str(root), "--summary", "--full"]
                )

        self.assertEqual(result, 1)
        self.assertEqual(json.loads(stdout)["machine_dominant_docs"], 1)
        self.assertIn("machine_dominant_docs", stderr)
        self.assertIn("exceeds baseline maximum 0", stderr)

    def test_default_changed_file_mode_keeps_per_document_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fake_path = root / "corpus" / "bad.md"
            with (
                mock.patch.object(
                    self.module, "iter_human_markdown", return_value=[fake_path]
                ),
                mock.patch.object(
                    self.module, "score_markdown", return_value=self.bad_score()
                ),
            ):
                result, stdout, stderr = self.run_main(["--root", str(root)])

        self.assertEqual(result, 1)
        self.assertIn("FAIL human research material gate", stdout)
        self.assertIn("dominated by machine-route language", stdout)
        self.assertEqual(stderr, "")

    def test_successful_summary_stdout_is_only_json(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_baseline(root, minimum_count=1)
            fake_path = root / "corpus" / "clean.md"
            with (
                mock.patch.object(
                    self.module, "iter_human_markdown", return_value=[fake_path]
                ),
                mock.patch.object(
                    self.module, "score_markdown", return_value=self.clean_score()
                ),
            ):
                result, stdout, stderr = self.run_main(
                    ["--root", str(root), "--summary", "--strict", "--full"]
                )

        self.assertEqual(result, 0)
        self.assertEqual(
            json.loads(stdout),
            {
                "scanned_markdown_count": 1,
                "machine_dominant_docs": 0,
                "missing_core_research_docs": 0,
                "modern_label_risk_docs": 0,
                "mojibake_docs": 0,
            },
        )
        self.assertEqual(stderr, "")

    def test_summary_full_allows_coverage_above_floor(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_baseline(root, minimum_count=1)
            fake_paths = [
                root / "corpus" / "clean-a.md",
                root / "corpus" / "clean-b.md",
            ]
            with (
                mock.patch.object(
                    self.module, "iter_human_markdown", return_value=fake_paths
                ),
                mock.patch.object(
                    self.module, "score_markdown", return_value=self.clean_score()
                ),
            ):
                result, stdout, stderr = self.run_main(
                    ["--root", str(root), "--summary", "--strict", "--full"]
                )

        self.assertEqual(result, 0)
        self.assertEqual(json.loads(stdout)["scanned_markdown_count"], 2)
        self.assertEqual(stderr, "")

    def test_committed_baseline_separates_floor_from_debt_ceilings(self) -> None:
        payload = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))

        self.assertEqual(
            payload["minimums"], {"scanned_markdown_count": 156794}
        )
        self.assertEqual(
            set(payload["maximums"]),
            {
                "machine_dominant_docs",
                "missing_core_research_docs",
                "modern_label_risk_docs",
                "mojibake_docs",
            },
        )
        self.assertNotIn("scanned_markdown_count", payload["maximums"])


if __name__ == "__main__":
    unittest.main()
