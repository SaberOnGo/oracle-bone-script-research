import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "005_excavation-sites-periods-and-batches"
    / "002_collection-object-candidates"
    / "039_coll-obj-cand-00039_ihp-item-770_collection-object-candidate"
)
EVIDENCE = OBJECT / "18_live-source-evidence-review.md"


class IhpItem770LiveSourceEvidenceTests(unittest.TestCase):
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

    def test_page_binds_official_metadata_and_source_boundary(self):
        required = (
            "https://museum.sinica.edu.tw/en/collection/32/item/770/",
            "https://museum.sinica.edu.tw/collection/32/item/770/",
            "Source collection item ID / 馆藏对象号: `770`",
            "Item No. / 馆藏编号: `R026893`",
            "Inscribed Plastron Colored with Cinnabar I 0778",
            "Late Shang Period",
            "7.3(L)×5.1(W) cm",
            "Pit YH127, Hsiao-t'un, Anyang County, Honan Province",
            "source_reported_description_without_full_transcription",
            "metadata_only_until_verified",
            "not a transcription, reading, or",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_binds_three_routes_and_direct_observation(self):
        required = (
            "8985f48895902dc4.jpg",
            "99,720",
            "530,826",
            "1,029,041",
            "383 x 480",
            "1021 x 1280",
            "1532 x 1920",
            "porous and uneven",
            "red-brown coloration",
            "pixels only",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_records_image_and_html_hashes(self):
        required = (
            "e9a610bd7ba65cbc68a451f640e9ccbdeb53ae575ecd9d2f81e9630c01a159c7",
            "a6d7c816a03468020d27abd4f4bface4dc636317c6ba45e5a409a3799e52260c",
            "4c06ea1753aceca1188e855c8abbadc3f12db83e56ad07af80d751de25022d50",
            "a3733ca4c44c2aac2e8feeea944299f64f3661e07aaec6f4f9ef28efdba5f164",
            "6810b06bf05f6c08aea32fb09fea9c0c81d2fe6b5f249896e0d36abcbef7c433",
            "Concrete next checks / 具体待查问题",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_private_image_hashes_match_when_present(self):
        expected = {
            "thumbnail-8985f48895902dc4.jpg":
                "e9a610bd7ba65cbc68a451f640e9ccbdeb53ae575ecd9d2f81e9630c01a"
                "159c7",
            "large-8985f48895902dc4.jpg":
                "a6d7c816a03468020d27abd4f4bface4dc636317c6ba45e5a409a3799e"
                "52260c",
            "hd-8985f48895902dc4.jpg":
                "4c06ea1753aceca1188e855c8abbadc3f12db83e56ad07af80d751de2502"
                "2d50",
        }
        for name, digest in expected.items():
            path = ROOT / ".working" / "ihp-770" / name
            if path.exists():
                actual = hashlib.sha256(path.read_bytes()).hexdigest()
                self.assertEqual(digest, actual)

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
