import contextlib
import io
import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools/006_ai-benchmark-pilot/select_case_triage.py"


def load_tool():
    spec = importlib.util.spec_from_file_location("select_case_triage_test", TOOL)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class AiCaseSelectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_tool()

    def test_real_work_order_starts_with_visible_permitted_images(self):
        rows = self.module.select_candidates(ROOT)
        self.assertEqual(len(rows), 6)
        self.assertEqual(
            [row["source_label"] for row in rows[:2]],
            ["BL", "BL"],
        )
        self.assertTrue(all(row["image_paths"] for row in rows[:2]))
        self.assertTrue(
            all(row["lane"] == "open_for_deep_review" for row in rows[:2])
        )
        for row in rows:
            self.assertNotIn("hypothesis_probability", row)
            self.assertIn("not a probability", row["triage_basis"])

    def test_rights_blocked_route_keeps_concrete_next_checks(self):
        rows = self.module.select_candidates(ROOT)
        h2 = next(
            row
            for row in rows
            if row["candidate_id"] == "obs-insc-src-cand-000001"
        )
        self.assertEqual(h2["lane"], "rights_blocked_route_review")
        self.assertIn(
            "Resolve effective rights before public image or derivative use.",
            h2["blockers"],
        )
        self.assertTrue(any("plate" in blocker for blocker in h2["blockers"]))

    def test_render_is_bilingual_and_stays_human_readable(self):
        rows = self.module.select_candidates(ROOT)
        text = self.module.render_markdown(rows)
        self.assertIn("## Selection rule / 选案规则", text)
        self.assertIn("## Human review cards / 人类复核卡", text)
        self.assertIn("不是概率", text)
        self.assertNotIn("hypothesis_probability", text)
        self.assertNotIn("ai_adjudicated_candidate", text)
        violations = [
            f"{line_number}:{len(line)}"
            for line_number, line in enumerate(text.splitlines(), start=1)
            if len(line) > 80
        ]
        self.assertEqual(violations, [])

    def test_cli_output_is_ignored_and_not_overwritten(self):
        with tempfile.TemporaryDirectory(dir=ROOT / ".working") as temporary:
            output = Path(temporary) / "triage.md"
            args = ["--root", str(ROOT), "--output", str(output)]
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(self.module.main(args), 0)
                self.assertEqual(self.module.main(args), 1)
            self.assertTrue(output.read_text(encoding="utf-8").startswith("# AI"))


if __name__ == "__main__":
    unittest.main()
