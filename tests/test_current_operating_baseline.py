import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASELINE = (
    ROOT
    / "doc/project/005_ai-agent-research-assistant-design/"
    / "03_current-operating-baseline-2026-08-30.md"
)


class CurrentOperatingBaselineTests(unittest.TestCase):
    def test_baseline_binds_current_decisions_without_false_probability(self):
        text = BASELINE.read_text(encoding="utf-8")
        for marker in (
            "current_operating_baseline",
            "2026-08-30",
            "b7db600ef3806b9c5984025a88e40ceef9a3c595",
            "not a second normative strategy",
            "不是第二份规范战略",
            "Gate 0",
            "Gate 6",
            "HYZ421",
            "2022JGTP0627",
            "obs-unk-005708",
            "bounded AI decision",
            "C8",
            "calibrated probability",
            "file count",
            "文件数量",
            "SYS_FLD_SYSID=124308",
            "SYS_FLD_SYSID=263185",
            "same platform",
            "HTTP 406",
        ):
            self.assertIn(marker, text)

        self.assertIn("C1--C4", text)
        self.assertIn("withhold", text)
        self.assertIn("abstain", text)
        self.assertIn("Gate 2: `BLOCKED`", text)
        self.assertIn("Gate 3: `BLOCKED`", text)
        self.assertIn("Gate 5: `CLOSED`", text)
        self.assertIn("Probability channel / 概率通道: `withheld`", text)
        self.assertNotIn("hypothesis_probability=", text)

    def test_baseline_is_bilingual_and_within_line_limit(self):
        text = BASELINE.read_text(encoding="utf-8")
        self.assertIn("Current Decision / 当前决定", text)
        self.assertIn("Replacement Rule / 替换规则", text)
        violations = [
            (number, len(line))
            for number, line in enumerate(text.splitlines(), 1)
            if len(line) > 80
        ]
        self.assertEqual(violations, [])

    def test_strategy_points_to_one_current_and_one_historical_audit(self):
        strategy = (
            ROOT
            / "doc/project/005_ai-agent-research-assistant-design/README.md"
        ).read_text(encoding="utf-8")
        historical = (
            ROOT
            / "doc/project/005_ai-agent-research-assistant-design/"
            / "01_current-state-audit-2026-08-14.md"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "[2026-08-30 current operating baseline][current-baseline]",
            strategy,
        )
        self.assertIn("historical frozen receipt", strategy)
        self.assertIn("superseded_historical_audit", historical)
        self.assertNotIn(
            "[2026-08-14 current-state audit][current-audit]",
            strategy,
        )


if __name__ == "__main__":
    unittest.main()
