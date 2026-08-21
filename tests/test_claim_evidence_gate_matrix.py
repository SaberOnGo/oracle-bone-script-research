from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MATRIX = (
    ROOT
    / "doc/project/005_ai-agent-research-assistant-design/"
    / "02_claim-evidence-gate-matrix.md"
)
STRATEGY = (
    ROOT
    / "doc/project/005_ai-agent-research-assistant-design/README.md"
)
SKILL = ROOT / "skills/ai-agent-evidence-pack-review/SKILL.md"
METHODS = ROOT / "doc/project/004_oracle-bone-script-research-methods/README.md"


class ClaimEvidenceGateMatrixTests(unittest.TestCase):
    def test_matrix_is_bilingual_and_normative(self) -> None:
        text = MATRIX.read_text(encoding="utf-8")
        for marker in [
            "# Claim Evidence Gate Matrix",
            "命题证据门槛矩阵",
            "normative companion",
            "规范配套",
            "C1 Object Identity / 对象身份",
            "C8 Complete Proposition And User Delivery",
            "ai_adjudicated_candidate",
            "confirmed_scholarship",
            "unknown_or_other",
            "source_reported",
            "independently_corroborated",
            "concrete next-source question",
            "具体下一来源待查问题",
        ]:
            self.assertIn(marker, text)

    def test_matrix_has_no_overwide_human_lines(self) -> None:
        for line_number, line in enumerate(
            MATRIX.read_text(encoding="utf-8").splitlines(), start=1
        ):
            self.assertLessEqual(len(line), 80, f"line {line_number}")

    def test_strategy_and_skill_link_matrix(self) -> None:
        strategy = STRATEGY.read_text(encoding="utf-8")
        skill = SKILL.read_text(encoding="utf-8")
        methods = METHODS.read_text(encoding="utf-8")
        self.assertIn("[claim evidence gate matrix]", strategy)
        self.assertIn("02_claim-evidence-gate-matrix.md", strategy)
        self.assertIn("claim evidence gate matrix", skill)
        self.assertIn("02_claim-evidence-gate-matrix.md", skill)
        self.assertIn("C4--C7", skill)
        self.assertIn("02_claim-evidence-gate-matrix.md", methods)

    def test_matrix_has_explicit_blocking_and_reopening_rules(self) -> None:
        text = MATRIX.read_text(encoding="utf-8")
        for marker in [
            "route_only` or missing mandatory evidence: `blocked`",
            "missing mandatory evidence",
            "Reopen the claim",
            "追加新决定，不改写历史",
            "not remove evidence",
            "falsification requirements",
        ]:
            self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()
