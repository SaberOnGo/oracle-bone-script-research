import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus/002_oracle-bone-inscriptions/008_source-record-candidates/"
    "005_obs-insc-src-cand-000005_bl-or-1595_source-record-candidate"
)
PAGE = OBJECT / "12_astronomical-date-dispute.md"
README = OBJECT / "README.md"


class Bl1595AstronomicalDateDisputeTests(unittest.TestCase):
    def test_page_is_bilingual_and_human_bounded(self):
        text = PAGE.read_text(encoding="utf-8")
        self.assertIn("Astronomical date dispute", text)
        self.assertIn("月食年代争议", text)
        self.assertIn("source-reported only", text)
        self.assertIn("不构成校准概率分布", text)
        self.assertIn("not an astronomical result", text)
        self.assertNotIn("TODO", text)
        self.assertNotIn("not_collected", text)
        self.assertTrue(all(len(line) <= 80 for line in text.splitlines()))

    def test_page_preserves_both_date_routes_and_scopes(self):
        text = PAGE.read_text(encoding="utf-8")
        for value in (
            "1192 BC",
            "27 December 1192 BC",
            "1166 BCE",
            "14 August 1166 BCE",
            "Yingcang 886",
            "Yingcang 885/886",
            "D-01",
            "D-02",
        ):
            self.assertIn(value, text)
        self.assertIn("26 years", text)
        self.assertIn("twentieth-century-addition", text)

    def test_page_links_authoritative_routes_and_next_checks(self):
        text = PAGE.read_text(encoding="utf-8")
        self.assertIn("scroll.in/article/801747", text)
        self.assertIn("doi.org/10.1017/eac.2014.10", text)
        self.assertIn("www1.ihp.sinica.edu.tw", text)
        self.assertIn("Heji", text)
        self.assertIn("逐项记录", text)

    def test_readme_links_the_dispute_page_in_both_languages(self):
        text = README.read_text(encoding="utf-8")
        self.assertIn("12_astronomical-date-dispute.md", text)
        self.assertIn("有名年代主张及其限制", text)


if __name__ == "__main__":
    unittest.main()
