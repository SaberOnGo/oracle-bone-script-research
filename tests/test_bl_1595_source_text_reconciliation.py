import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus/002_oracle-bone-inscriptions/008_source-record-candidates/"
    "005_obs-insc-src-cand-000005_bl-or-1595_source-record-candidate"
)


class BritishLibrary1595SourceTextTests(unittest.TestCase):
    def test_readme_exposes_the_human_reconciliation_page(self):
        text = (OBJECT / "README.md").read_text(encoding="utf-8-sig")
        self.assertIn("08_source-text-line-reconciliation.md", text)
        self.assertIn("09_british-library-catalog-record.md", text)
        self.assertIn("90_source-record.json", text)
        self.assertIn("91_source-record-index.csv", text)

    def test_catalog_record_is_source_reported_and_bounded(self):
        path = OBJECT / "09_british-library-catalog-record.md"
        self.assertTrue(path.is_file(), path)
        text = path.read_text(encoding="utf-8-sig")
        for marker in (
            "Or 7694/1595",
            "Shang dynasty oracle bone",
            "Couling-Chalfant",
            "Oriental Manuscripts",
            "1300 BC-1050 BC",
            "Images currently unavailable",
            "source-reported",
            "item-level JSON payload",
            "no project OCR",
            "or decipherment claim",
        ):
            self.assertIn(marker, text)
        self.assertNotIn("twentieth century", text)
        self.assertNotIn("project translation", text)

    def test_reconciliation_preserves_source_strings_and_boundaries(self):
        path = OBJECT / "08_source-text-line-reconciliation.md"
        self.assertTrue(path.is_file(), path)
        text = path.read_text(encoding="utf-8-sig")
        for marker in (
            "obs-insc-src-cand-000005",
            "Or. 7694/1595r",
            "Or. 7694/1595v",
            "已未庚申月㞢[食]",
            "七日己未斲庚申月又食",
            "庚申",
            "已未",
            "己未",
            "source_display_only",
            "not a project transcription",
            "not a formal inscription identity",
            "proposer",
        ):
            self.assertIn(marker, text)
        self.assertNotIn("project translation", text)

    def test_literature_review_records_named_date_dispute(self):
        path = OBJECT / "06_literature-and-dispute-review.md"
        text = path.read_text(encoding="utf-8-sig")
        for marker in (
            "Emma Goodliffe",
            "Roberto Soria",
            "Xueshun Liu",
            "Chang Yuzhi",
            "1192 BC",
            "1166 BCE",
            "astronomical_date_dispute",
            "source_citation_route_only",
            "10.1017/eac.2014.10",
        ):
            self.assertIn(marker, text)
        self.assertIn("do not settle the reading", text)

    def test_human_markdown_stays_within_eighty_characters(self):
        for name in (
            "README.md",
            "06_literature-and-dispute-review.md",
            "08_source-text-line-reconciliation.md",
            "09_british-library-catalog-record.md",
        ):
            path = OBJECT / name
            for number, line in enumerate(
                path.read_text(encoding="utf-8-sig").splitlines(), 1
            ):
                self.assertLessEqual(
                    len(line),
                    80,
                    f"{path}:{number}: {len(line)} characters",
                )


if __name__ == "__main__":
    unittest.main()
