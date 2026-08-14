import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "005_excavation-sites-periods-and-batches"
    / "002_collection-object-candidates"
    / "024_coll-obj-cand-00024_ihp-item-781_collection-object-candidate"
)
EVIDENCE = OBJECT / "18_live-source-evidence-review.md"


class IhpItem781LiveSourceEvidenceTests(unittest.TestCase):
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

    def test_page_binds_metadata_and_source_text(self):
        required = (
            "https://museum.sinica.edu.tw/en/collection/32/item/781/",
            "https://museum.sinica.edu.tw/collection/32/item/781/",
            "Source collection item ID / 馆藏对象号: `781`",
            "Item No. / 馆藏编号: `R044755`",
            "Inscribed Carapace I 4683",
            "龜背甲卜辭（龜冊）《乙》4683",
            "Late Shang Period",
            "14.8(L)×5.6(W) cm",
            "Pit YH127, Hsiao-t'un, Anyang County, Honan Province",
            "䖵（害）我。",
            "䖵不我（害）。",
            "source_reported_transcription_with_source_reading",
            "No OCR correction",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_binds_image_route_and_local_observation(self):
        required = (
            "8945f68987791716.jpg",
            "258015",
            "46d8dfc316fa00a58bff70286abd0e98577c1ccd99306c93c07ea945698c0b8b",
            "797 x 1280",
            "image/jpeg",
            "central",
            "round hole",
            "metadata_only_until_verified",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_records_snapshots_and_rights(self):
        required = (
            "en.html",
            "60,604",
            "0862fda2d56e5dcb",
            "c97201e7aedfe778c4f6b535f4694f882514328fee6b7007",
            "zh.html",
            "57,837",
            "53c71f164a0e7b1404a3c008f8a7fd56df1611f389d3ec9e4889b404e8b53ad5",
            "Concrete next checks / 具体下一步待查",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_private_image_hash_matches_when_present(self):
        path = ROOT / ".working" / "ihp-781" / "large.jpg"
        if path.exists():
            self.assertEqual(
                "46d8dfc316fa00a58bff70286abd0e98577c1ccd99306c93c07ea945698c0b8b",
                hashlib.sha256(path.read_bytes()).hexdigest(),
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
