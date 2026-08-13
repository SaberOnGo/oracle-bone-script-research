import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "005_excavation-sites-periods-and-batches"
    / "002_collection-object-candidates"
    / "011_coll-obj-cand-00011_ihp-item-775_collection-object-candidate"
)
EVIDENCE = OBJECT / "18_live-source-evidence-review.md"


class IhpItem775LiveSourceEvidenceTests(unittest.TestCase):
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

    def test_page_binds_metadata_and_source_display(self):
        required = (
            "https://museum.sinica.edu.tw/en/collection/32/item/775/",
            "https://museum.sinica.edu.tw/collection/32/item/775/",
            "Source collection item ID / 馆藏对象号: `775`",
            "Item No. / 馆藏编号: `R044293`",
            "Inscribed Plastron Ping 0086",
            "帶卜辭龜腹甲《丙》0086",
            "Late Shang Period",
            "商代晚期",
            "Turtle Plastron",
            "河南省安陽縣小屯YH127坑",
            "王隻（獲）鹿。允隻（獲）。",
            "允隻（獲）麋四百五十一。",
            "source_reported_displayed_lines_with_image_placeholders",
            "[source glyph image]",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_binds_all_four_image_routes(self):
        routes = (
            (
                "1805f688155263ca.jpg",
                "374,252",
                "5070e3f48e53a2fa51110053c704897e152b91483c8caa80d90617c04ee993ea",
                "959 x 1280",
            ),
            (
                "275f68814bd7953.png",
                "450,558",
                "a0cda077ae16cecf9f7559de0f3edf9fc8e007469be30908083bd334943cc79f",
                "700 x 1280",
            ),
            (
                "8755f688157698e8.jpg",
                "380,254",
                "d18f302e19c4681c86fad44d7626c0d3ee03fa3e4c99653c99da993e00c4cf7a",
                "959 x 1280",
            ),
            (
                "9425f68814f4c9c3.png",
                "1,048,456",
                "0997f8dca4cc19937c9e910641331e2b56161c8397401b623019814cfc9afd8e",
                "690 x 1280",
            ),
        )
        for filename, size, digest, pixels in routes:
            for value in (filename, size, digest, pixels):
                self.assertIn(value, self.text)
        self.assertEqual(self.text.count("image/jpeg"), 2)
        self.assertEqual(self.text.count("image/png"), 2)
        self.assertEqual(
            self.text.count("local_private_visual_inspection_only"), 6
        )
        self.assertEqual(self.text.count("processed view"), 2)

    def test_page_records_snapshots_and_rights(self):
        required = (
            "en.html",
            "63,595",
            "7c7bf0becea064960d6a572fc1afb707c1e0c0c6ce2f26c1143a98bbab846640",
            "zh.html",
            "61,431",
            "6c90f9b5f0b37db0b6b502241e8bab07f88bea598232d304d596a4f2f31754bc",
            "metadata_only_until_verified",
            "Concrete next checks / 具体下一步待查",
            "not a new transcription",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_private_route_files_match_documented_hashes_when_present(self):
        files = {
            "1805f688155263ca.jpg":
                "5070e3f48e53a2fa51110053c704897e152b91483c8caa80d90617c04ee993ea",
            "275f68814bd7953.png":
                "a0cda077ae16cecf9f7559de0f3edf9fc8e007469be30908083bd334943cc79f",
            "8755f688157698e8.jpg":
                "d18f302e19c4681c86fad44d7626c0d3ee03fa3e4c99653c99da993e00c4cf7a",
            "9425f68814f4c9c3.png":
                "0997f8dca4cc19937c9e910641331e2b56161c8397401b623019814cfc9afd8e",
        }
        temp = ROOT / ".working" / "ihp-775"
        for name, digest in files.items():
            path = temp / name
            if not path.exists():
                continue
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(digest, actual, name)

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
