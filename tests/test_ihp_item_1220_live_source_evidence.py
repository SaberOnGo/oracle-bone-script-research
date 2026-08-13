import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "005_excavation-sites-periods-and-batches"
    / "002_collection-object-candidates"
    / "009_coll-obj-cand-00009_ihp-item-1220_collection-object-candidate"
)
EVIDENCE = OBJECT / "18_live-source-evidence-review.md"


class IhpItem1220LiveSourceEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.text = EVIDENCE.read_text(encoding="utf-8-sig")

    def test_live_page_is_linked_from_human_entries(self):
        self.assertTrue(EVIDENCE.exists())
        for name in (
            "README.md",
            "06_human-collection-dossier.md",
            "08_collection-provenance-evidence-dossier.md",
            "12_archaeological-context-review.md",
            "14_human-research-readiness-review.md",
            "16_preformal-research-start-check.md",
        ):
            page = (OBJECT / name).read_text(encoding="utf-8-sig")
            self.assertIn("18_live-source-evidence-review.md", page)

    def test_page_binds_bilingual_metadata_and_source_display(self):
        required = (
            "https://museum.sinica.edu.tw/en/collection/32/item/1220/",
            "https://museum.sinica.edu.tw/collection/32/item/1220/",
            "Source collection item ID / 馆藏对象号: `1220`",
            "Item No. / 馆藏编号: `R044776`",
            "Reshaped Tortoise Carapace Yi Bian 5271",
            "改製龜背甲卜辭 《乙》5271",
            "Late Shang Period",
            "SYFYH127, Hsiao-t'un,",
            "Anyang County, Honan Province",
            "Turtle Plastron",
            "庚戌卜，爭貞：岳害我。",
            "庚戌卜，爭貞：岳不我害。",
            "source_reported_displayed_two_lines_not_independently_edited",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_binds_two_image_routes_and_checksums(self):
        routes = (
            (
                "4692_8867571a214d619.jpg",
                "436,863",
                "4e3ed1b465a20db30bf1a183c83d2971103c795d05b71f35c810106243d6f8e0",
                "1014 x 1280",
            ),
            (
                "4692_61267571a221a42b.jpg",
                "452,835",
                "cbf5ea35a5685e30abd0281e7c39a255edf6675d558da1fbcef234d1360295fa",
                "1011 x 1280",
            ),
        )
        for filename, size, digest, pixels in routes:
            self.assertIn(filename, self.text)
            self.assertIn(size, self.text)
            self.assertIn(digest, self.text)
            self.assertIn(pixels, self.text)
        self.assertEqual(self.text.count("image/jpeg"), 2)
        self.assertEqual(
            self.text.count("local_private_visual_inspection_only"), 2
        )

    def test_page_records_source_snapshots_and_rights_boundary(self):
        required = (
            "official-page.html",
            "55,815",
            "c7b7ece60323645aa2e9cc4bb935e030b302e2bd9cea57d16c577d43461922ca",
            "official-page-zh.html",
            "52,356",
            "b196fa6041a39190253ca48ed4ac5f4149f304cd33706f3f9e2f81e00cccd043",
            "metadata_only_until_verified",
            "not a new transcription",
            "not a project translation",
            "Concrete next checks / 具体下一步待查",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_visual_index_keeps_public_asset_lane_separate(self):
        index = (OBJECT / "03_visual-asset-index.csv").read_text(
            encoding="utf-8-sig"
        )
        for value in ("coll-obj-cand-00009-visual-01", "metadata_only_until_verified"):
            self.assertIn(value, index)
        self.assertNotIn("committed_public_asset", index)

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
