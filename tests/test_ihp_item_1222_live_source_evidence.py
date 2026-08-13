import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "005_excavation-sites-periods-and-batches"
    / "002_collection-object-candidates"
    / "008_coll-obj-cand-00008_ihp-item-1222_collection-object-candidate"
)
EVIDENCE = OBJECT / "18_live-source-evidence-review.md"


class IhpItem1222LiveSourceEvidenceTests(unittest.TestCase):
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

    def test_page_binds_metadata_and_fragmentary_text(self):
        required = (
            "https://museum.sinica.edu.tw/en/collection/32/item/1222/",
            "Source collection item ID / 馆藏对象号: `1222`",
            "Item No. / 馆藏编号: `ZR038421`",
            "Tortoise Carapace Fragments Yi Bian 4817+5061+5520+5804+6087+"
            "R60751",
            "Late Shang Period",
            "SYFYH127, Hsiao-t'un,",
            "Anyang County, Honan Province",
            "Turtle Plastron",
            "source_reported_fragmentary_display_with_placeholders",
            "[子]曰□子曰名曰",
        )
        for value in required:
            self.assertIn(value, self.text)
        self.assertEqual(self.text.count("image placeholder:"), 5)

    def test_page_binds_two_image_routes_and_checksums(self):
        routes = (
            (
                "43367571cc964c58.jpg",
                "335,264",
                "d59a6cbd401daf184880e58a7aa826e310bc2ee481f71a91a4aa2f3d18ac"
                "45bf",
                "1150 x 1280",
            ),
            (
                "99967571cca1e09f.jpg",
                "370,055",
                "cf9f1e84be0a26d7f21eac7c06014dc1370eb08f346c6f01ac37e8004578"
                "631d",
                "1150 x 1280",
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
            "source-reported museum wording",
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
