import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "005_excavation-sites-periods-and-batches"
    / "002_collection-object-candidates"
    / "022_coll-obj-cand-00022_ihp-item-780_collection-object-candidate"
)
EVIDENCE = OBJECT / "18_live-source-evidence-review.md"


class IhpItem780LiveSourceEvidenceTests(unittest.TestCase):
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
            "https://museum.sinica.edu.tw/en/collection/32/item/780/",
            "https://museum.sinica.edu.tw/collection/32/item/780/",
            "Source collection item ID / 馆藏对象号: `780`",
            "Item No. / 馆藏编号: `R034327`",
            "Inscribed Plastron Fragment Chia 2224",
            "龜甲卜辭殘片《甲》2224",
            "Late Shang Period",
            "2.6(L)×1.9(W) cm",
            "Hsiao-t'un, Anyang County, Honan Province",
            "meteorological divination",
            "source_reported_description_without_full_transcription",
            "No OCR correction",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_binds_image_access_boundary(self):
        required = (
            "4055f689d7d912d.jpg",
            "external_route_access_not_verified",
            "HTTP 200",
            "text/html",
            "no local image",
            "metadata_only_until_verified",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_records_snapshots_and_registered_route(self):
        required = (
            "en.html",
            "59,123",
            "1a09bc5455818566d5be43dd982001c85d87d9519f0ca2332cbfc2aeb80d41e4",
            "zh.html",
            "55,876",
            "70f02ee4dce46b34a82e0bc71807b68d2a4d02743c32316a7500c5ced5dee19e3",
            "3756b0a5bbf7dc4b595e0f363bd9f5a0ab818d667ca0303903ef74eb7dcdfe57",
            "Concrete next checks / 具体下一步待查",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_private_route_is_not_mistaken_for_image(self):
        path = ROOT / ".working" / "ihp-780" / "large.jpg"
        if path.exists():
            self.assertEqual(b"<!DOCTYPE", path.read_bytes()[:9])
            self.assertEqual(
                (
                    "77c5c9124e04442445bce0b25f096c2795de35ba82314de3111255a8d43d6654"
                ),
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
