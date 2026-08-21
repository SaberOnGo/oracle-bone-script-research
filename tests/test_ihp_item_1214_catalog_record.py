import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOSSIER = (
    ROOT
    / "research"
    / "001_published-scholarship-index"
    / "010_ihp-item-1214_catalog-record"
)
OBJECT = (
    ROOT
    / "corpus"
    / "005_excavation-sites-periods-and-batches"
    / "002_collection-object-candidates"
    / "002_coll-obj-cand-00002_ihp-item-1214_collection-object-candidate"
)


class IHPItem1214CatalogRecordTest(unittest.TestCase):
    def read(self, relative_path):
        path = DOSSIER / relative_path
        self.assertTrue(path.is_file(), f"missing dossier file: {path}")
        return path.read_text(encoding="utf-8")

    def test_human_first_dossier_and_identity(self):
        markdown = sorted(DOSSIER.glob("*.md"))
        self.assertGreaterEqual(len(markdown), 7)
        self.assertEqual(len(list(DOSSIER.glob("*.json"))), 1)
        self.assertFalse(list(DOSSIER.glob("*.csv")))
        self.assertFalse(list(DOSSIER.glob("*.jpg")))
        text = self.read("README.md")
        for value in (
            "Museum of the Institute of History and Philology",
            "1214",
            "R038861",
            "Jia Bian 0959",
            "src-ihp-museum-oracle-bones",
            "dl-ihp-museum-oracle-bones",
            "54136",
            "3756b0a5bbf7dc4b595e0f363bd9f5a0ab818d667ca0303903ef74eb7dcdfe57",
            "not registered",
            "metadata_only_until_verified",
        ):
            self.assertIn(value, text)

    def test_claim_scope_and_source_family_boundaries(self):
        scope = self.read("02_scope-and-method.md")
        locator = self.read("03_claim-evidence-locator.md")
        network = self.read("04_catalog-citation-network.md")
        limits = self.read("05_limits-disputes-and-rights.md")
        for value in (
            "source-reported",
            "complete OCR",
            "image placeholders",
            "not a project translation",
            "Jia Bian 0959",
        ):
            self.assertIn(value, scope)
        for value in (
            "independently-checked",
            "exact plate locator",
            "complete OCR and text order",
            "not silently converted",
        ):
            self.assertIn(value, locator)
        self.assertIn("one institutional source family", network)
        self.assertIn("Counting them twice", network)
        for value in (
            "abstain_withhold_candidate",
            "not a rights clearance",
            "metadata_only_until_verified",
        ):
            self.assertIn(value, limits)

    def test_machine_index_is_subordinate_and_object_linked(self):
        index = DOSSIER / "90_literature-index.json"
        data = json.loads(index.read_text(encoding="utf-8"))
        self.assertEqual(data["record_type"], "human_dossier_support_only")
        self.assertEqual(data["item_id"], "1214")
        self.assertEqual(data["accession"], "R038861")
        self.assertEqual(data["formal_record_count"], 0)
        self.assertEqual(data["item_snapshot"], "not_registered")
        self.assertLess(index.stat().st_size, 3000)
        route = (OBJECT / "20_catalog-record-route.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("010_ihp-1214.md", route)
        alias = (ROOT / "research" / "001_published-scholarship-index" /
                 "010_ihp-1214.md").read_text(encoding="utf-8")
        self.assertIn("010_ihp-item-1214_catalog-record/README.md", alias)
        self.assertIn("abstain_withhold_candidate", route)

    def test_bilingual_and_markdown_width(self):
        for path in DOSSIER.glob("*.md"):
            text = path.read_text(encoding="utf-8")
            self.assertIn("/", text, f"missing bilingual markers: {path}")
            for line_number, line in enumerate(text.splitlines(), start=1):
                self.assertLessEqual(
                    len(line),
                    80,
                    f"{path}:{line_number} exceeds 80 characters",
                )
        path = OBJECT / "20_catalog-record-route.md"
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            self.assertLessEqual(
                len(line),
                80,
                f"{path}:{line_number} exceeds 80 characters",
            )


if __name__ == "__main__":
    unittest.main()
