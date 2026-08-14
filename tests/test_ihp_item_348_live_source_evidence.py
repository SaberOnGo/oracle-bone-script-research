import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "005_excavation-sites-periods-and-batches"
    / "002_collection-object-candidates"
    / "018_coll-obj-cand-00018_ihp-item-348_collection-object-candidate"
)
EVIDENCE = OBJECT / "18_live-source-evidence-review.md"


class IhpItem348LiveSourceEvidenceTests(unittest.TestCase):
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
            "https://museum.sinica.edu.tw/en/collection/32/item/348/",
            "https://museum.sinica.edu.tw/collection/32/item/348/",
            "Source collection item ID / 馆藏对象号: `348`",
            "Item No. / 馆藏编号: `R024974`",
            "Inscribed Animal Bone Fragment Chia 2336",
            "獸骨卜辭殘片《甲》2336",
            "Late Shang Period",
            "10.0(L)×6.2(W) cm",
            "Hsiao-t'un, Anyang County, Honan Province",
            "practice inscriptions",
            "source_reported_description_without_full_transcription",
            "OCR correction",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_binds_image_and_3d_routes(self):
        required = (
            "915f68928c0f84a.jpg",
            "507365",
            "65d0eeace3a40d1756e84103693b4aace8a22308d9984e9f7bbfdc5dc9cf933e",
            "975 x 1280",
            "image/jpeg",
            "archeodata.sinica.edu.tw",
            "metadata_only_until_verified",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_records_snapshots_and_rights(self):
        required = (
            "en.html",
            "59,653",
            "4b1521227ac9f4604fa5e84c75469af3ed6890abc71f7c5ac115f07391822e44",
            "zh.html",
            "55,857",
            "62863b9ebc042d1bbf320392e5ad80fc40f9418a6ec321c316c7107c968ce41a",
            "Concrete next checks / 具体下一步待查",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_private_image_hash_matches_when_present(self):
        path = ROOT / ".working" / "ihp-348" / "large.jpg"
        if path.exists():
            self.assertEqual(
                "65d0eeace3a40d1756e84103693b4aace8a22308d9984e9f7bbfdc5dc9cf933e",
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
