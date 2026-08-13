import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "corpus" / "009_statistics-and-derived-features"
CLOSURE = REPORTS / "230_preformal-research-preprocessing-closure.md"
AUDIT = REPORTS / "231_preprocessing-completion-audit-2026-08-12.md"


class PreformalThirdBatchAuditTests(unittest.TestCase):
    def test_historical_snapshot_is_not_recast_as_completion(self):
        text = CLOSURE.read_text(encoding="utf-8")
        for marker in (
            "historical snapshot of the `2026-08-07`",
            "inventory evidence, not completion evidence",
            "少量可证伪",
            "local diagnostic locked two v4 Agent outputs",
            "后续本地诊断虽锁定两份",
        ):
            self.assertIn(marker, text)

    def test_current_audit_records_the_three_opened_evidence_units(self):
        text = AUDIT.read_text(encoding="utf-8")
        for marker in (
            "`obs-char-000621`",
            "`17_multi-instance-visual-comparison.md`",
            "`08_sequence-context-evidence.md`",
            "source serialization order `5, 0, 1, 2, 3, 6, 4`",
            "Cambridge Hopkins Finding List dossier",
            "`609` and `612`",
            "`metadata_only_until_verified`",
        ):
            self.assertIn(marker, text)

    def test_current_audit_keeps_ai_and_scholarly_boundaries_explicit(self):
        text = AUDIT.read_text(encoding="utf-8")
        for marker in (
            "Candidate delivery / 候选交付: `none`",
            "diagnostic_fail_withheld",
            "not a model-independent rerun",
            "不是模型独立复跑",
            "A local one-shot score receipt now exists",
            "现在已有本地一次性评分 receipt",
            "isolated-scorer receipt or a validated benchmark experiment",
            "隔离评分器 receipt 或已验证基准实验",
            "pipeline pass",
            "少量可证伪、带反证、可复跑",
            "not_complete",
        ):
            self.assertIn(marker, text)
        self.assertNotIn("v3 benchmark passed", text.lower())

    def test_reports_are_bilingual_readable_and_within_eighty_columns(self):
        for path in (CLOSURE, AUDIT):
            text = path.read_text(encoding="utf-8")
            self.assertIn(" / ", text.splitlines()[0])
            self.assertRegex(text, r"[\u4e00-\u9fff]")
            self.assertNotIn("\ufffd", text)
            for mojibake in ("×ÊÁÏ", "ÕýÊ½", "ºòÑ¡"):
                self.assertNotIn(mojibake, text)
            violations = [
                f"{line_number}:{len(line)}"
                for line_number, line in enumerate(text.splitlines(), 1)
                if len(line) > 80
            ]
            self.assertEqual([], violations, path.as_posix())


if __name__ == "__main__":
    unittest.main()
