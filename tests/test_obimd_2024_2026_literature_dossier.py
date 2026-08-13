import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOSSIER = (
    ROOT
    / "research"
    / "001_published-scholarship-index"
    / "004_obimd-2024-2026_data-paper"
)


class ObimdLiteratureDossierTest(unittest.TestCase):
    def test_human_first_structure(self):
        required = {
            "README.md",
            "01_version-relationship.md",
            "02_scope-and-method.md",
            "03_claim-evidence-locator.md",
            "04_field-evidence-guide.md",
            "05_citations-and-proposers.md",
            "06_limits-disputes-and-rights.md",
            "07_object-transfer-routes.md",
            "08_review-log.md",
            "09_literature-index.json",
        }
        self.assertEqual(required, {path.name for path in DOSSIER.iterdir()})
        self.assertEqual(9, len(list(DOSSIER.glob("*.md"))))
        self.assertEqual(1, len(list(DOSSIER.glob("*.json"))))
        self.assertEqual(0, len(list(DOSSIER.glob("*.csv"))))

    def test_bibliography_and_version_relation(self):
        combined = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (DOSSIER / "README.md", DOSSIER / "01_version-relationship.md")
        )
        for expected in (
            "arXiv:2407.03900",
            "2024-07-04",
            "Scientific Data 13, 681 (2026)",
            "10.1038/s41597-026-06967-0",
            "2026-03-14",
            "2026-04-30",
            "Bang Li",
            "Jing Yang",
            "Donghao Luo",
            "Taisong Jin",
            "not byte-identical versions",
            "不是字节相同版本",
        ):
            self.assertIn(expected, combined)

    def test_claim_locator_and_mark_boundary(self):
        combined = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (
                DOSSIER / "03_claim-evidence-locator.md",
                DOSSIER / "04_field-evidence-guide.md",
            )
        )
        for expected in (
            "10,077",
            "9,913",
            "164",
            "93,652",
            "21,667",
            "21,941",
            "4,192",
            "115,319",
            "SeatFont",
            "Mark = 0",
            "Mark = 1",
            "Mark = 2",
            "Mark = 3",
            "does not mean the dispute is resolved",
            "不表示争议已经解决",
            "Data Records",
            "Technical Validation",
        ):
            self.assertIn(expected, combined)

    def test_proposers_rights_and_scholarly_boundary(self):
        combined = "\n".join(
            path.read_text(encoding="utf-8") for path in DOSSIER.glob("*.md")
        )
        for expected in (
            "CC BY 4.0",
            "academic research purposes only",
            "CC BY-NC-ND 4.0",
            "metadata_only_until_verified",
            "third-party",
            "author-reported",
            "not a project conclusion",
            "不是项目结论",
            "src-obimd",
            "candidate route",
        ):
            self.assertIn(expected, combined)

    def test_local_snapshot_provenance(self):
        text = (DOSSIER / "README.md").read_text(encoding="utf-8")
        for expected in (
            "48860",
            "564ad9626b4a022c979eb26e8e73f9a5dfa0faa5672955e2ddfbad798f9f9fa9",
            "3871",
            "2ad91fb999e3ea176a2f7dd39cf67b5e8cfb327d9f22f6713aa1d196a61932de",
            "5543",
            "3361eb37c65a01de05d73b57525500eeed6db7c35dcc16c303794a467c4bbd3e",
            "independently-checked",
            "unresolved",
        ):
            self.assertIn(expected, text)

    def test_json_is_secondary(self):
        path = DOSSIER / "09_literature-index.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual("human_dossier_support_only", payload["purpose"])
        self.assertEqual("not_a_scholarly_conclusion", payload["boundary"])
        self.assertLess(path.stat().st_size, 5000)

    def test_human_markdown_line_width(self):
        violations = []
        for path in DOSSIER.glob("*.md"):
            for number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), start=1
            ):
                if len(line) > 80:
                    violations.append(f"{path.name}:{number}:{len(line)}")
        self.assertEqual([], violations)


if __name__ == "__main__":
    unittest.main()
