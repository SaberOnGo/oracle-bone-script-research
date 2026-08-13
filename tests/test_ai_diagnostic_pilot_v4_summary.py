from __future__ import annotations

import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SUMMARY_PATH = (
    REPOSITORY_ROOT
    / "doc"
    / "public"
    / "user_research"
    / "011_ai-diagnostic-pilot-2026-08-13"
    / "README.md"
)


class AIDiagnosticPilotV4SummaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.summary = SUMMARY_PATH.read_text(encoding="utf-8")

    def test_summary_is_human_readable_bilingual_and_linked_to_receipt(self):
        self.assertIn("AI Diagnostic Pilot v4", self.summary)
        self.assertIn("AI 诊断试点 v4", self.summary)
        self.assertIn("Status / 状态: reviewed", self.summary)
        self.assertIn(
            "research_boundary: benchmark_pilot_not_scholarship",
            self.summary,
        )
        self.assertIn("delivery_status: withheld", self.summary)
        self.assertIn(
            "731D46A2872DCD45803D7603525CB277D717C7580E9F8DDCFFCDD7416E5EB33F",
            self.summary,
        )

    def test_summary_records_bindings_result_and_run_independence(self):
        for digest in (
            "64bc73f5e7526c68a510827502d0cf65df96a5e50747a06ddd8a31d13451171a",
            "152ec01ca7944bb51877c11302e11524bf93e8f504191f9d35a716a9c0e97ab6",
            "25a3942b3aaa695a4bc67af5f2ac5387f2d01319d378f3090c0d0544075b9bbb",
            "6b2974e4e5f0f4dcb589b1b0fafa529392e4a3bf9f2636b478c6fd90924e4025",
            "1091511a80232989bc2e6e611fe4de23db25025c6da0db586aea62fab6fe7505",
            "55aa9301e1a503352ffda2c52beae9ac5f4c2bd8b23df3a4d0fddbbdbdd5225f",
        ):
            self.assertIn(digest, self.summary)
        self.assertIn("diagnostic_fail_withheld", self.summary)
        self.assertIn("pretraining_exposure_unknown", self.summary)
        self.assertIn("same-model execution rerun", self.summary)
        self.assertIn("not model-independent", self.summary)
        self.assertIn("not Gate 3", self.summary)

    def test_summary_does_not_promote_private_or_scholarly_content(self):
        forbidden = (
            "commitment_key_hex",
            "HMAC key",
            "private-gold",
            "agent-output-v4-primary.json",
            "chain of thought",
            "confirmed scholarship",
            "破译成功",
            "已破译",
        )
        for token in forbidden:
            self.assertNotIn(token, self.summary)
        self.assertIn("not a decipherment result", self.summary)
        self.assertIn("不是释读结果", self.summary)

    def test_summary_markdown_stays_within_human_line_width(self):
        overlong = [
            (number, len(line))
            for number, line in enumerate(self.summary.splitlines(), 1)
            if len(line) > 80
        ]
        self.assertEqual(overlong, [])


if __name__ == "__main__":
    unittest.main()
