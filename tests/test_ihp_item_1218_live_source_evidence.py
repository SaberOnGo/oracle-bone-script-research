import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "005_excavation-sites-periods-and-batches"
    / "002_collection-object-candidates"
    / "007_coll-obj-cand-00007_ihp-item-1218_collection-object-candidate"
)
EVIDENCE = OBJECT / "18_live-source-evidence-review.md"


class IhpItem1218LiveSourceEvidenceTests(unittest.TestCase):
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

    def test_page_binds_metadata_and_partial_text(self):
        required = (
            "https://museum.sinica.edu.tw/en/collection/32/item/1218/",
            "Source collection item ID / 馆藏对象号: `1218`",
            "Item No. / 馆藏编号: `R044753`",
            "Reshaped Tortoise Carapace Yi Bian 4681",
            "Late Shang Period",
            "SYFYH127, Hsiao-t'un,",
            "Anyang County, Honan Province",
            "Turtle Plastron",
            "source_reported_partial_display_with_ellipsis",
            "壬辰卜，爭：自今五日至于丙申不其雨。",
        )
        for value in required:
            self.assertIn(value, self.text)
        self.assertIn("自今五日至于…", self.text)

    def test_page_binds_two_image_routes_and_checksums(self):
        routes = (
            (
                "126675715f2cc7d9.jpg",
                "272,912",
                "d7c18746ae055d85493cd933caf4844b08156aaff498ad5572cba1b96d6"
                "f6832",
                "997 x 1280",
            ),
            (
                "74675715f370ec2.jpg",
                "302,051",
                "eef05287c2881090c9fd55485db151420292a0bef7227faf596c95ddc87b9"
                "f31",
                "997 x 1280",
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
