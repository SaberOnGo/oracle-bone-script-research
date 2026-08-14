import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "005_excavation-sites-periods-and-batches"
    / "002_collection-object-candidates"
    / "042_coll-obj-cand-00042_ihp-item-508_collection-object-candidate"
)
EVIDENCE = OBJECT / "18_live-source-evidence-review.md"


class IhpItem508LiveSourceEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.text = EVIDENCE.read_text(encoding="utf-8-sig")

    def test_live_evidence_is_linked_from_human_entries(self):
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

    def test_page_binds_metadata_and_reading_boundary(self):
        required = (
            "https://museum.sinica.edu.tw/en/collection/32/item/508/",
            "https://museum.sinica.edu.tw/collection/32/item/508/",
            "Source collection item ID: `508`",
            "Item No.: `R044852`",
            "Inscribed Plastron Colored with Cinnabar I 0867",
            "Late Shang Period",
            "20.3(L)×11.7(W) cm",
            "source_reported_description_without_independent_transcription",
            "positive-and-negative harvest question",
            "metadata_only_until_verified",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_binds_three_routes_and_visual_boundary(self):
        required = (
            "8835a16885a45d95.jpg",
            "68,093",
            "357,282",
            "354,922",
            "280 x 480",
            "748 x 1280",
            "776 x 1327",
            "cracks divide",
            "red or brown pigment traces",
            "pixel observations only",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_records_image_and_html_hashes(self):
        required = (
            "1c4fbdca93a707b892909173250f159ff004894dc41a2526ea0a1d0cc5720728",
            "ef84b528a7afad337cf577b4fbe50e0433a7168159d98c4816103fb30ac87292",
            "d9e28eb1cd33dd71d2ad5b11fa8fee3dcf11c96b7d6eff1998f33eb056445eb6",
            "f1c43764d9f04be550f373f177c69a67db7a784b5e9e149ccee4b4de5f3107a4",
            "528a0b24d263e0fccba391f7eed4be67b0c9bc37b4827b70327283a7bb",
            "Concrete next checks / 具体待查问题",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_private_image_hashes_match_when_present(self):
        expected = {
            "thumbnail-8835a16885a45d95.jpg":
                "1c4fbdca93a707b892909173250f159ff004894dc41a2526ea0a1d0cc5720728",
            "large-8835a16885a45d95.jpg":
                "ef84b528a7afad337cf577b4fbe50e0433a7168159d98c4816103fb30ac87292",
            "hd-8835a16885a45d95.jpg":
                "d9e28eb1cd33dd71d2ad5b11fa8fee3dcf11c96b7d6eff1998f33eb056445eb6",
        }
        for name, digest in expected.items():
            path = ROOT / ".working" / "ihp-508" / name
            if path.exists():
                self.assertEqual(digest, hashlib.sha256(path.read_bytes()).hexdigest())

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
