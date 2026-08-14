import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOSSIER = (
    ROOT
    / "research/001_published-scholarship-index/"
    "008_liu-2014_yingcang-eclipse"
)


class Liu2014LiteratureDossierTests(unittest.TestCase):
    def test_human_files_and_parent_link_exist(self):
        readme = (DOSSIER / "README.md").read_text(encoding="utf-8")
        parent = (
            ROOT / "research/001_published-scholarship-index/README.md"
        ).read_text(encoding="utf-8")
        for name in (
            "01_scope-and-method.md",
            "02_claim-evidence-locator.md",
            "03_citation-network.md",
            "04_limits-disputes-and-rights.md",
            "05_object-transfer-routes.md",
            "06_review-log.md",
            "90_literature-index.json",
        ):
            self.assertTrue((DOSSIER / name).exists(), name)
            self.assertIn(name, readme)
        self.assertIn("[liu-eclipse]", parent)

    def test_bibliography_and_claim_boundary(self):
        readme = (DOSSIER / "README.md").read_text(encoding="utf-8")
        locator = (DOSSIER / "02_claim-evidence-locator.md").read_text(
            encoding="utf-8"
        )
        for marker in (
            "Xueshun Liu",
            "Early China",
            "10.1017/eac.2014.10",
            "2014-07-24",
            "1166 BCE",
            "Yingcang 885/886",
            "project transcription",
        ):
            self.assertIn(marker, readme + locator)
        self.assertIn("No date is adopted", locator)

    def test_machine_record_keeps_metadata_only_status(self):
        record = json.loads(
            (DOSSIER / "90_literature-index.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(record["dossier_id"], "literature-liu-early-china-2014")
        self.assertEqual(record["doi"], "10.1017/eac.2014.10")
        self.assertEqual(
            record["rights_status"], "metadata_only_until_verified"
        )
        self.assertEqual(
            record["reading_status"],
            "source_reported_needs_full_text_and_object_crosswalk",
        )
        self.assertEqual(
            record["related_candidate_id"], "obs-insc-src-cand-000005"
        )

    def test_markdown_is_utf8_and_within_80_columns(self):
        for path in DOSSIER.glob("*.md"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("\ufffd", text)
            long_lines = [
                (number, len(line))
                for number, line in enumerate(text.splitlines(), 1)
                if len(line) > 80
            ]
            self.assertEqual([], long_lines, str(path))


if __name__ == "__main__":
    unittest.main()
