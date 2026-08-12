import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOSSIER = (
    ROOT
    / "research"
    / "001_published-scholarship-index"
    / "003_hust-obc-2024_data-paper"
)


class HustObc2024LiteratureDossierTest(unittest.TestCase):
    def test_human_first_structure(self):
        required = {
            "README.md",
            "01_scope-and-method.md",
            "02_claim-evidence-locator.md",
            "03_citation-network.md",
            "04_limits-disputes-and-rights.md",
            "05_object-transfer-routes.md",
            "06_review-log.md",
            "07_literature-index.json",
        }
        self.assertEqual(required, {path.name for path in DOSSIER.iterdir()})
        self.assertEqual(7, len(list(DOSSIER.glob("*.md"))))
        self.assertEqual(1, len(list(DOSSIER.glob("*.json"))))
        self.assertEqual(0, len(list(DOSSIER.glob("*.csv"))))

    def test_bibliography_and_provenance_are_exact(self):
        text = (DOSSIER / "README.md").read_text(encoding="utf-8")
        for expected in (
            "Pengjie Wang",
            "Kaile Zhang",
            "Yuliang Liu",
            "Scientific Data 11, 976 (2024)",
            "https://doi.org/10.1038/s41597-024-03807-x",
            "2024-09-06",
            "306156",
            "82d734557c125b20f621be13cc6b86ef83f948359b2b7f40059a14925d0f75d9",
            "3016746",
            "5cc89d374e644a8c152521db949f36b250e1d2b34fe074fccf0140b82fb43229",
            "source-reported",
            "independently-checked",
            "unresolved",
        ):
            self.assertIn(expected, text)

    def test_claim_locator_keeps_dataset_and_decipherment_boundaries(self):
        text = (DOSSIER / "02_claim-evidence-locator.md").read_text(
            encoding="utf-8"
        )
        for expected in (
            "140,053",
            "77,064",
            "1,588",
            "62,989",
            "9,411",
            "94.6%",
            "0.914",
            "does not equal a decipherment probability",
            "不等于释读概率",
            "may contain duplicates",
            "可能存在重复",
            "GuoXueDaShi",
            "Data Records",
            "Technical Validation",
        ):
            self.assertIn(expected, text)

    def test_methods_rights_and_transfer_are_bounded(self):
        combined = "\n".join(
            path.read_text(encoding="utf-8") for path in DOSSIER.glob("*.md")
        )
        for expected in (
            "Data Acquisition",
            "Automatic Annotation",
            "Data Integration",
            "Data Validation",
            "Anyang Normal University",
            "CC BY-NC 4.0",
            "third-party",
            "第三方",
            "not a confirmed reading",
            "不是已确认释读",
            "src-hust-obc",
            "candidate route",
        ):
            self.assertIn(expected, combined)

    def test_json_is_small_supporting_index(self):
        path = DOSSIER / "07_literature-index.json"
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
