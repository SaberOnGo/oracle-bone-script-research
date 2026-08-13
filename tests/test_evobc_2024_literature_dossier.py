import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOSSIER = (
    ROOT
    / "research"
    / "001_published-scholarship-index"
    / "005_evobc-2024_data-paper"
)


class EvobcLiteratureDossierTests(unittest.TestCase):
    def test_human_first_bundle_exists(self):
        markdown = sorted(DOSSIER.glob("*.md"))
        self.assertEqual(len(markdown), 5)
        self.assertTrue((DOSSIER / "90_literature-index.json").is_file())

    def test_simulation_metrics_are_bounded(self):
        text = (DOSSIER / "02_claim-evidence-locator.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Top-1 16.7%", text)
        self.assertIn("Top-20 55.8%", text)
        self.assertIn(
            "not a\nprobability distribution over scholarly readings", text
        )
        self.assertIn("校准后验概率", text)

    def test_raw_package_and_rights_limits_are_visible(self):
        scope = (DOSSIER / "01_scope-and-method.md").read_text(
            encoding="utf-8"
        )
        rights = (DOSSIER / "03_limits-disputes-and-rights.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("unified raw image package remains not obtained", scope)
        self.assertIn("source_marked_risk_noted", rights)
        self.assertIn("not accepted readings", rights)

    def test_index_is_secondary_and_non_scholarly(self):
        data = json.loads(
            (DOSSIER / "90_literature-index.json").read_text(encoding="utf-8")
        )
        self.assertEqual(data["purpose"], "human_dossier_support_only")
        self.assertIn("not_a_decipherment", data["boundary"])

    def test_human_markdown_is_readable_and_within_80_columns(self):
        for path in DOSSIER.glob("*.md"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("\ufffd", text)
            for number, line in enumerate(text.splitlines(), start=1):
                self.assertLessEqual(len(line), 80, f"{path}:{number}")


if __name__ == "__main__":
    unittest.main()
