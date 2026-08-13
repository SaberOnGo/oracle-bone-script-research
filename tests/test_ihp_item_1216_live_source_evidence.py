import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "005_excavation-sites-periods-and-batches"
    / "002_collection-object-candidates"
    / "005_coll-obj-cand-00005_ihp-item-1216_collection-object-candidate"
)
EVIDENCE = OBJECT / "18_live-source-evidence-review.md"


class IhpItem1216LiveSourceEvidenceTests(unittest.TestCase):
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

    def test_page_binds_plate_metadata_and_placeholders(self):
        required = (
            "https://museum.sinica.edu.tw/en/collection/32/item/1216/",
            "Source collection item ID / 馆藏对象号: `1216`",
            "Item No. / 馆藏编号: `ZR044855`",
            "Tortoise Carapace for DivinationYi Bian 8806+8865+8997",
            "Late Shang Period",
            "SYFYH251, Hsiao-t'un,",
            "Anyang County, Honan Province",
            "Turtle Plastron",
            "source_reported_partial_display_with_inline_placeholders",
        )
        for value in required:
            self.assertIn(value, self.text)
        self.assertEqual(self.text.count("image placeholder:"), 7)

    def test_page_binds_two_image_routes_and_checksums(self):
        routes = (
            (
                "95167571dccccb3c.jpg",
                "227,798",
                "18c245fe7263ede5d5efccf5f868a88c4d531fb158616e47613233ee03d2"
                "c6fe",
                "773 x 1280",
            ),
            (
                "36267571dcd519b2.jpg",
                "250,095",
                "7d553289fbb732e9ee57ee17f789e4518e84ab13926a10b6575ea12a48d"
                "da1d7",
                "773 x 1280",
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

    def test_page_keeps_partial_quality_rights_and_boundary(self):
        required = (
            "metadata_only_until_verified",
            "not a new transcription",
            "not a confirmed",
            "source-reported",
            "museum wording",
            "Concrete next checks / 具体下一步待查",
        )
        for value in required:
            self.assertIn(value, self.text)

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
