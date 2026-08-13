import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "005_excavation-sites-periods-and-batches"
    / "002_collection-object-candidates"
    / "013_coll-obj-cand-00013_ihp-item-776_collection-object-candidate"
)
EVIDENCE = OBJECT / "18_live-source-evidence-review.md"


class IhpItem776LiveSourceEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.text = EVIDENCE.read_text(encoding="utf-8-sig")

    def test_live_page_is_linked_from_human_entries(self):
        self.assertTrue(EVIDENCE.exists())
        for name in (
            "README.md",
            "04_visual-gallery.md",
            "05_human-review-sheet.md",
            "06_human-collection-dossier.md",
            "08_collection-provenance-evidence-dossier.md",
            "10_collection-provenance-fact-matrix.md",
            "12_archaeological-context-review.md",
            "14_human-research-readiness-review.md",
            "16_preformal-research-start-check.md",
        ):
            page = (OBJECT / name).read_text(encoding="utf-8-sig")
            self.assertIn("18_live-source-evidence-review.md", page)

    def test_page_binds_metadata_and_source_description(self):
        required = (
            "https://museum.sinica.edu.tw/en/collection/32/item/776/",
            "https://museum.sinica.edu.tw/collection/32/item/776/",
            "Source collection item ID / 馆藏对象号: `776`",
            "Item No. / 馆藏编号: `R041288`",
            "Inscribed Plastron I 507+Ping 284",
            "Late Shang Period",
            "商代晚期",
            "Turtle Plastron",
            "19.4(L)×18.2(W) cm",
            "one tiger,",
            "40 deer, 164 foxes",
            "159 deer fawns",
            "source_reported_displayed_description_without_transcription",
            "No OCR, character segmentation, or reading",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_binds_image_route(self):
        for value in (
            "7085f6889c78ddf8.jpg",
            "345,224",
            "62a3aa533c4f75b043d7d072908e79fd6d90a71b1e11d1eee062cbc31cf8b1dc",
            "959 x 1280",
            "image/jpeg",
            "local_private_visual_inspection_only",
        ):
            self.assertIn(value, self.text)

    def test_page_records_snapshots_and_rights(self):
        required = (
            "en.html",
            "62,383",
            "2e00cc878ab884c263ffb83d569a99ec1ae6ef5948f7782ec4131df0f862a0d0",
            "zh.html",
            "61,568",
            "17e7abf813401273ef7d9c776f427002ed5bdfae9790ce819a08b54723ffe735",
            "metadata_only_until_verified",
            "Concrete next checks / 具体下一步待查",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_private_route_file_matches_documented_hash_when_present(self):
        path = ROOT / ".working" / "ihp-776" / "7085f6889c78ddf8.jpg"
        if path.exists():
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(
                "62a3aa533c4f75b043d7d072908e79fd6d90a71b1e11d1eee062cbc31cf8b1dc",
                actual,
            )

    def test_markdown_is_utf8_and_within_line_width(self):
        EVIDENCE.read_bytes().decode("utf-8")
        long_lines = [
            (number, len(line))
            for number, line in enumerate(self.text.splitlines(), 1)
            if len(line) > 80
        ]
        self.assertEqual([], long_lines)


if __name__ == "__main__":
    unittest.main()
