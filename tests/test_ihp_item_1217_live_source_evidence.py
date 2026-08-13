import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "005_excavation-sites-periods-and-batches"
    / "002_collection-object-candidates"
    / "006_coll-obj-cand-00006_ihp-item-1217_collection-object-candidate"
)
EVIDENCE = OBJECT / "18_live-source-evidence-review.md"


class IhpItem1217LiveSourceEvidenceTests(unittest.TestCase):
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

    def test_page_binds_metadata_and_placeholders(self):
        required = (
            "https://museum.sinica.edu.tw/en/collection/32/item/1217/",
            "Source collection item ID / 馆藏对象号: `1217`",
            "Item No. / 馆藏编号: `R041291`",
            "Fanned Tortoise Carapace for Divination Bing Bian 0065",
            "Late Shang Period",
            "SYFYH127, Hsiao-t'un,",
            "Anyang County, Honan Province",
            "Turtle Plastron",
            "source_reported_partial_display_with_inline_placeholders",
        )
        for value in required:
            self.assertIn(value, self.text)
        self.assertEqual(self.text.count("image placeholder:"), 5)

    def test_page_binds_two_image_routes_and_checksums(self):
        routes = (
            (
                "30067571e27eaf93.jpg",
                "292,814",
                "0cd084bbe73f55da560460d57d6793f2255ba51c96fd5e653666a5c2619"
                "2ee09",
                "960 x 1280",
            ),
            (
                "89067571e288ee38.jpg",
                "344,692",
                "c5aaf3baeb4410995cdee9842be03cc93e2d8e8d3e0909b66715b04e02e5"
                "e5e6",
                "960 x 1280",
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
