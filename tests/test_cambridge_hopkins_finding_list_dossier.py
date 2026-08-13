import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOSSIER = (
    ROOT
    / "research"
    / "001_published-scholarship-index"
    / "006_cambridge-hopkins_finding-list"
)
INDEX_README = (
    ROOT / "research" / "001_published-scholarship-index" / "README.md"
)


class CambridgeHopkinsFindingListDossierTest(unittest.TestCase):
    def read(self, relative_path):
        path = DOSSIER / relative_path
        self.assertTrue(path.is_file(), f"missing dossier file: {path}")
        return path.read_text(encoding="utf-8")

    @staticmethod
    def normalized(text):
        return " ".join(text.split())

    def test_human_first_structure(self):
        self.assertTrue(DOSSIER.is_dir(), "item-level dossier is missing")
        markdown = sorted(DOSSIER.glob("*.md"))
        json_files = sorted(DOSSIER.glob("*.json"))
        self.assertGreaterEqual(len(markdown), 7)
        self.assertEqual(len(json_files), 1)
        self.assertFalse(list(DOSSIER.glob("*.csv")))
        self.assertFalse(list(DOSSIER.glob("*.pdf")))
        self.assertFalse(list(DOSSIER.glob("*.png")))
        human_bytes = sum(path.stat().st_size for path in markdown)
        machine_bytes = json_files[0].stat().st_size
        self.assertGreater(human_bytes, machine_bytes * 4)

    def test_identity_live_access_and_snapshot_provenance(self):
        text = self.read("README.md")
        normalized = self.normalized(text)
        required = (
            "Finding List for the Hopkins Collection of Chinese Oracle Bones",
            "Cambridge University Library",
            "2026-08-13",
            "src-cambridge-hopkins",
            "dl-cambridge-hopkins-finding-list",
            "74132",
            "f11bc30e9893e5d5b3d32371364d59503f100157aaa612800974883f5a78b4e7",
            "metadata_only_until_verified",
            "source-reported",
            "independently-checked",
            "unresolved",
        )
        for value in required:
            self.assertIn(value, normalized)
        self.assertIn("https://www.lib.cam.ac.uk/collections/", text)

    def test_classified_toc_and_code_semantics(self):
        text = self.read("01_page-structure-and-code-key.md")
        for value in (
            "Classified Table of Contents",
            "579",
            "609",
            "Shih tsu",
            "Tzu tsu",
            "Wu tsu",
            "Cambridge University Library (CUL) number",
            "F. H. Chalfant",
            "Chia ku wen ho chi",
            "Ying-kuo so ts'ang chia ku chi",
        ):
            self.assertIn(value, text)
        for code in ("`c`", "`h`", "`j`", "`y`"):
            self.assertIn(code, text)
        self.assertIn("cross-reference", text)
        self.assertIn("不能单独证明", text)
        self.assertIn("Chinese scope summaries", text)
        self.assertIn("中文范围摘要", text)
        self.assertNotIn("Page label / 页面标签", text)

    def test_count_disagreement_is_preserved_not_repaired(self):
        text = self.read("02_count-reconciliation.md")
        for value in (
            "609",
            "612",
            "delta `+3`",
            "period-i-group-19",
            "`13`",
            "`22`",
            "period-ii-group-1",
            "`29`",
            "`28`",
            "period-ii-group-19",
            "period-ii-group-4",
            "`16`",
            "`21`",
            "Period V Group 8",
            "`[10]`",
            "Unclassified",
            "不得静默修正",
        ):
            self.assertIn(value, text)
        self.assertIn(
            "does not prove missing or duplicate inscriptions",
            self.normalized(text),
        )
        self.assertIn("four retained rows", text)

    def test_locator_boundaries_and_concrete_questions(self):
        locator = self.read("03_claim-evidence-locator.md")
        limits = self.read("05_limits-disputes-and-rights.md")
        transfer = self.read("06_object-transfer-routes.md")
        review = self.read("07_review-log.md")
        for state in (
            "source-reported",
            "independently-checked",
            "unresolved",
        ):
            self.assertIn(state, locator)
        for value in (
            "not a rights clearance",
            "not a transcription",
            "not a reading",
            "metadata_only_until_verified",
        ):
            self.assertIn(value, limits)
        self.assertIn("candidate", transfer)
        self.assertIn("formal `obi-*`", transfer)
        self.assertIn("image direction", review)
        self.assertIn("page or plate", review)
        self.assertIn("why", review.lower())
        self.assertIn("source archive", limits)
        self.assertIn("src-cambridge-hopkins", limits)
        for name in (
            "26_official-cambridge-literature-and-dispute-review.md",
            "27_official-literature-route-index.csv",
        ):
            self.assertIn(name, limits)
            self.assertTrue(
                (
                    ROOT
                    / "corpus"
                    / "006_research-sources-and-bibliography"
                    / "001_source-objects"
                    / "008_src-cambridge-hopkins_source-object"
                    / name
                ).is_file()
            )

    def test_machine_index_is_small_and_subordinate(self):
        path = DOSSIER / "90_literature-index.json"
        self.assertTrue(path.is_file())
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(data["purpose"], "human_dossier_support_only")
        self.assertEqual(data["rights_status"],
                         "metadata_only_until_verified")
        self.assertEqual(data["page_stated_grand_total"], 609)
        self.assertEqual(data["retained_row_count"], 612)
        self.assertEqual(data["formal_record_count"], 0)
        self.assertLess(path.stat().st_size, 3000)

    def test_markdown_line_width_and_index_link(self):
        for path in DOSSIER.glob("*.md"):
            for line_number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), start=1
            ):
                self.assertLessEqual(
                    len(line),
                    80,
                    f"{path}:{line_number} exceeds 80 characters",
                )
        index_text = INDEX_README.read_text(encoding="utf-8")
        self.assertIn("Cambridge Hopkins Finding List dossier", index_text)
        self.assertIn(
            "006_cambridge-hopkins_finding-list/README.md", index_text
        )
        self.assertIn("The HUST-OBC paper dossier", index_text)


if __name__ == "__main__":
    unittest.main()
