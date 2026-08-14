import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOSSIER = (
    ROOT
    / "research"
    / "001_published-scholarship-index"
    / "007_schwartz-2019_hyz-monograph"
)


class SchwartzHyzLiteratureDossierTests(unittest.TestCase):
    def test_human_reading_order_and_parent_links(self):
        readme = (DOSSIER / "README.md").read_text(encoding="utf-8")
        parent = (
            ROOT / "research" / "001_published-scholarship-index" / "README.md"
        ).read_text(encoding="utf-8")
        object_note = (
            ROOT
            / "corpus"
            / "002_oracle-bone-inscriptions"
            / "008_source-record-candidates"
            / "007_obs-insc-src-cand-000007_ningxia-hyz421_source-record-candidate"
            / "06_literature-and-dispute-review.md"
        ).read_text(encoding="utf-8")
        self.assertIn("007_schwartz-2019_hyz-monograph/README.md", parent)
        self.assertIn("lit-schwartz-hyz-2019", object_note)
        for name in (
            "01_scope-and-method.md",
            "02_claim-evidence-locator.md",
            "03_citation-network.md",
            "04_limits-disputes-and-rights.md",
            "05_object-transfer-routes.md",
            "06_review-log.md",
        ):
            self.assertTrue((DOSSIER / name).is_file(), name)
            self.assertIn(name, readme)

    def test_bibliography_and_boundary_are_explicit(self):
        readme = (DOSSIER / "README.md").read_text(encoding="utf-8")
        for marker in (
            "Adam C. Schwartz",
            "10.1515/9781501505294",
            "Library of Sinology",
            "HYZ 421, H3:1325",
            "not a",
            "decipherment result",
        ):
            self.assertIn(marker, readme)

    def test_support_json_keeps_unopened_page_boundary(self):
        record = json.loads(
            (DOSSIER / "90_literature-index.json").read_text(encoding="utf-8")
        )
        self.assertEqual(record["doi"], "10.1515/9781501505294")
        self.assertEqual(
            record["publisher_route_status"],
            "publisher_metadata_checked_not_downloaded",
        )
        self.assertEqual(
            record["page_citation_status"],
            "source_reported_not_opened",
        )
        self.assertEqual(
            record["effective_project_rights"],
            "metadata_only_until_verified",
        )

    def test_human_markdown_is_utf8_and_within_80_columns(self):
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
