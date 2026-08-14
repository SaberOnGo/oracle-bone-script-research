import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "005_excavation-sites-periods-and-batches"
    / "002_collection-object-candidates"
    / "032_coll-obj-cand-00032_ihp-item-503_collection-object-candidate"
)
EVIDENCE = OBJECT / "18_live-source-evidence-review.md"


class IhpItem503LiveSourceEvidenceTests(unittest.TestCase):
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

    def test_page_binds_live_metadata_and_boundary(self):
        required = (
            "https://museum.sinica.edu.tw/en/collection/32/item/503/",
            "https://museum.sinica.edu.tw/collection/32/item/503/",
            "Source collection item ID: `503`",
            "Inscribed Plastron Ping 0529",
            "帶卜辭龜腹甲《丙》0529",
            "R044498",
            "Late Shang Period",
            "17.4(L) × 13.8(W) cm",
            "Pit YH127",
            "Turtle Plastron",
            "source-reported",
            "metadata_only_until_verified",
            "帝令雨",
            "not a transcription",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_binds_private_routes_and_pixel_boundary(self):
        required = (
            "77859e83b1f6f4f0.jpg",
            "59,585",
            "362,737",
            "753,936",
            "357 × 480",
            "954 × 1280",
            "1431 × 1920",
            "large broken plastron",
            "pixel-level observations only",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_records_image_and_html_hashes(self):
        required = (
            "cb3fd3ffe6b2ef276961de1cddbb32d12b4ab4e7e985690ea7f871068d7876c7",
            "52bb7600d1f746dbc2a3882f6a8ac4ec93caf1f6a39c77ab0ee7af5d023d22d2",
            "febc5c14cd855f9cca4ae314233ffff718a51ae7808aadf4e4d9ba020dbf21c9",
            "be3ca1771fc7de104e273e0717e882006842889f542bf13ea2a79b15acbfa6ab",
            "dcb5960f9d3986d0d6097302550f8d454aa41f935c4150abcdc642cccb4ba5c2",
            "Concrete next checks / 具体待查问题",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_private_image_hashes_match_when_present(self):
        expected = {
            "thumbnail-77859e83b1f6f4f0.jpg":
                "cb3fd3ffe6b2ef276961de1cddbb32d12b4ab4e7e985690ea7f871068d7876c7",
            "large-77859e83b1f6f4f0.jpg":
                "52bb7600d1f746dbc2a3882f6a8ac4ec93caf1f6a39c77ab0ee7af5d023d22d2",
            "hd-77859e83b1f6f4f0.jpg":
                "febc5c14cd855f9cca4ae314233ffff718a51ae7808aadf4e4d9ba020dbf21c9",
        }
        for name, digest in expected.items():
            path = ROOT / ".working" / "ihp-503" / name
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
