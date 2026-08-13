import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "005_excavation-sites-periods-and-batches"
    / "002_collection-object-candidates"
    / "002_coll-obj-cand-00002_ihp-item-1214_collection-object-candidate"
)
EVIDENCE = OBJECT / "18_live-source-evidence-review.md"


class IhpItem1214LiveSourceEvidenceTests(unittest.TestCase):
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

    def test_page_binds_official_object_metadata_and_partial_text(self):
        required = (
            "https://museum.sinica.edu.tw/en/collection/32/item/1214/",
            "Source collection item ID / 馆藏对象号: `1214`",
            "Item No. / 对象编号: `R038861`",
            "Jia Bian 0959",
            "Late Shang Period",
            "Hsiao-t'un, Anyang County",
            "Turtle Plastron",
            "今夕又（有）",
            "source_reported_partial_text",
            "not a new interpretation",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_binds_two_image_routes(self):
        routes = (
            (
                "9556755eabc7d122.jpg",
                "288,687",
                "818f2a3fb7add38b74d8d54410cca689110e3e6c939f9422e5e27d49d9f1601d",
            ),
            (
                "6356755eac0c5214.jpg",
                "283,825",
                "86b99f8433b7b036eb4f3ccb7dcc2e8fc5ed10d0e7fe17c8c3c4bf0edbdbddf6",
            ),
        )
        for filename, size, digest in routes:
            self.assertIn(filename, self.text)
            self.assertIn(size, self.text)
            self.assertIn(digest, self.text)
        self.assertEqual(self.text.count("image/jpeg"), 2)
        self.assertEqual(self.text.count("local_private_visual_inspection_only"), 2)

    def test_page_keeps_rights_and_boundary(self):
        required = (
            "metadata_only_until_verified",
            "No image is committed",
            "不再分发图像",
            "not a confirmed",
            "破译结果",
            "具体下一步待查",
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
