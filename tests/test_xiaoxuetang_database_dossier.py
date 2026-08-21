import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOSSIER = (
    ROOT
    / "research"
    / "001_published-scholarship-index"
    / "009_xiaoxuetang_database"
)


class XiaoxuetangDatabaseDossierTests(unittest.TestCase):
    def test_human_entry_and_numbered_notes_exist(self):
        expected = {
            "README.md",
            "01_source-identity-and-access.md",
            "02_scope-and-fields.md",
            "03_citation-network.md",
            "04_claim-evidence-locator.md",
            "05_limits-disputes-and-rights.md",
            "06_object-transfer-routes.md",
            "07_review-log.md",
            "90_literature-index.json",
        }
        self.assertEqual(
            expected,
            {p.name for p in DOSSIER.iterdir()},
        )

    def test_readme_is_bilingual_and_links_parent_index(self):
        text = (DOSSIER / "README.md").read_text(encoding="utf-8")
        self.assertIn("Xiaoxuetang Wenzixue Database", text)
        self.assertIn("小學堂文字學資料庫", text)
        self.assertIn("src-xiaoxuetang-jiaguwen", text)
        parent = (
            ROOT
            / "research"
            / "001_published-scholarship-index"
            / "README.md"
        ).read_text(encoding="utf-8")
        self.assertIn("009_xiaoxuetang_database/README.md", parent)

    def test_access_receipt_contains_current_hashes_and_old_route_boundary(self):
        text = (DOSSIER / "01_source-identity-and-access.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("2026-08-21", text)
        self.assertIn(
            "ce4a31874613e995746c6a554dfef9c53492ec23e6437339191158fed3f6377d",
            text,
        )
        self.assertIn("existing project log", text.lower())
        self.assertIn("not as a silent replacement", text.lower())

    def test_scope_keeps_counts_as_time_stamped_source_observations(self):
        text = (DOSSIER / "02_scope-and-fields.md").read_text(encoding="utf-8")
        for value in ("261,117", "1,341,886", "366,530", "24,701", "2,548"):
            self.assertIn(value, text)
        self.assertIn("2026-08-21", text)
        self.assertIn("different units", text)

    def test_boundary_and_rights_are_explicit(self):
        text = (DOSSIER / "05_limits-disputes-and-rights.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("CC0", text)
        self.assertIn("third-party", text)
        self.assertIn("row-level export", text)
        self.assertIn("not a", text.lower())
        transfer = (DOSSIER / "06_object-transfer-routes.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("may not", transfer.lower())
        self.assertIn("probability", transfer.lower())

    def test_machine_file_is_small_support_only(self):
        data = json.loads(
            (DOSSIER / "90_literature-index.json").read_text(encoding="utf-8")
        )
        self.assertEqual(data["record_type"], "human_dossier_support_only")
        self.assertEqual(data["candidate_delivery"], "none")
        self.assertEqual(data["formal_research_status"], "not_started")
        self.assertIn("Not a row-level import", data["caution"])

    def test_markdown_lines_are_at_most_80_columns(self):
        offenders = []
        for path in DOSSIER.glob("*.md"):
            for number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), 1
            ):
                if len(line) > 80:
                    offenders.append(f"{path.name}:{number}:{len(line)}")
        self.assertEqual([], offenders)


if __name__ == "__main__":
    unittest.main()
