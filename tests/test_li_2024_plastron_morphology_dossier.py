import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOSSIER = (
    ROOT
    / "research"
    / "001_published-scholarship-index"
    / "011_li-2024_plastron-morphology"
)


class Li2024PlastronMorphologyDossierTests(unittest.TestCase):
    def test_human_dossier_and_parent_route_exist(self):
        readme = (DOSSIER / "README.md").read_text(encoding="utf-8")
        parent = (
            ROOT / "research" / "001_published-scholarship-index" / "README.md"
        ).read_text(encoding="utf-8")
        self.assertIn("011_li-2024_plastron-morphology/README.md", parent)
        for marker in (
            "李延彦",
            "故宫博物院院刊",
            "34-44",
            "Huadong 421",
            "blunt-rounded",
            "not diagnostic",
            "not a project",
        ):
            self.assertIn(marker, readme)

    def test_support_index_keeps_identity_boundary(self):
        record = json.loads(
            (DOSSIER / "90_literature-index.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            record["official_pdf_sha256"],
            "f67a269954a649ce69ac4f75156e35481a5b42f4f39f1ca69f73015a257f48f7",
        )
        self.assertEqual(
            record["identity_effect"],
            "low_specificity_compatible_not_diagnostic",
        )
        self.assertIn("not an object identity", record["research_boundary"])

    def test_human_markdown_is_readable_and_wrapped(self):
        for path in DOSSIER.glob("*.md"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("\ufffd", text)
            for line_number, line in enumerate(text.splitlines(), 1):
                self.assertLessEqual(
                    len(line),
                    80,
                    f"{path}:{line_number}: {len(line)} characters",
                )


if __name__ == "__main__":
    unittest.main()
