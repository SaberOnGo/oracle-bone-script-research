import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "005_excavation-sites-periods-and-batches"
    / "002_collection-object-candidates"
    / "036_coll-obj-cand-00036_ihp-item-506_collection-object-candidate"
)
EVIDENCE = OBJECT / "18_live-source-evidence-review.md"


class IhpItem506LiveSourceEvidenceTests(unittest.TestCase):
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

    def test_page_binds_live_metadata_and_source_discrepancy(self):
        required = (
            "https://museum.sinica.edu.tw/en/collection/32/item/506/",
            "https://museum.sinica.edu.tw/collection/32/item/506/",
            "Source collection item ID: `506`",
            "Inscribed Plastron Ping 0538",
            "帶卜辭龜腹甲《丙》0538",
            "R044502",
            "Late Shang Period",
            "17.4(L) × 10.3(W) cm",
            "Pit YH127",
            "Turtle Plastron",
            "source descriptions only",
            "metadata_only_until_verified",
            "2026-06-04 registered HTML snapshot",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_binds_private_routes_and_pixel_boundary(self):
        required = (
            "15959e86fbe02d72.jpg",
            "86,319",
            "635,467",
            "1,439,590",
            "351 × 480",
            "937 × 1280",
            "1406 × 1920",
            "Broad cracks",
            "black handwritten-looking annotations",
            "pixel-level observations only",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_records_image_and_html_hashes(self):
        required = (
            "8d1002f0310e0d6dade4c8f4e44664dc764bedf21a81cf5100ad84a070b1d9eb",
            "336c3b8c094dbde751e644aeedea0509225b4329c5e6173a7801b25859cad61b",
            "f907c81a97df14270a8e15128cc1a5dd6ddabfba20092676784e08a41b72ba0c",
            "1396ba3049566840be2de0231bface1c61028c0116f87f4dc97525a05a415dbe",
            "daacd2999bea51d246a5bf08fc9f5d54e3fed890cf84c716fb9db3c2183170fd",
            "Concrete next checks / 具体下一步待查",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_private_image_hashes_match_when_present(self):
        expected = {
            "thumbnail.jpg":
                (
                    "8d1002f0310e0d6dade4c8f4e44664dc764bedf21a81cf510"
                    "0ad84a070b1d9eb"
                ),
            "large.jpg":
                (
                    "336c3b8c094dbde751e644aeedea0509225b4329c5e6173a"
                    "7801b25859cad61b"
                ),
            "hd.jpg":
                (
                    "f907c81a97df14270a8e15128cc1a5dd6ddabfba20092676784e08a4"
                    "1b72ba0c"
                ),
        }
        for name, digest in expected.items():
            path = ROOT / ".working" / "ihp-506" / name
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
