import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "005_excavation-sites-periods-and-batches"
    / "002_collection-object-candidates"
    / "015_coll-obj-cand-00015_ihp-item-777_collection-object-candidate"
)
EVIDENCE = OBJECT / "18_live-source-evidence-review.md"


class IhpItem777LiveSourceEvidenceTests(unittest.TestCase):
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

    def test_page_binds_metadata_and_source_description(self):
        required = (
            "https://museum.sinica.edu.tw/en/collection/32/item/777/",
            "https://museum.sinica.edu.tw/collection/32/item/777/",
            "Source collection item ID / 馆藏对象号: `777`",
            "Item No. / 馆藏编号: `R035203`",
            "Inscribed Animal Bone Fragment Chia 2928",
            "Late Shang Period",
            "动物骨",
            "5.9(L)×3.1(W) cm",
            "standing dog profile",
            "pig-like form with mane",
            "source_reported_displayed_description_without_transcription",
            "No\nOCR, sentence reconstruction, or reading is added here.",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_binds_all_image_routes(self):
        required = (
            "7885f688cb8afa74.jpg",
            "e6c5604304610c8f9007592c7174d207557952d8d90ee5af7900aaba85f242f4",
            "8225f67255bc623e.png",
            "d78eb1276e168acd65c20946a18591564858607e2c6bc9e3600634606b2e07b2",
            "7305f67030ae01f9.png",
            "8503fc1e4eff649d2dbec58b17f4035d15acd32e14749c4be33b8c3cad3af1c6",
            "959 x 1280",
            "130 x 391",
            "320 x 334",
            "local_private_visual_inspection_only",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_records_snapshots_and_rights(self):
        required = (
            "en.html",
            "57,620",
            "84012c65b9c157d94804c6b491c96e73895daa4291696e9185cf446b927fbf1e",
            "zh.html",
            "54,004",
            "c7e5df9e06293239b53424b178fddfe583469422367134435d481cf0997a0b45",
            "metadata_only_until_verified",
            "Concrete next checks / 具体下一步待查",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_private_routes_match_documented_hashes_when_present(self):
        expected = {
            "7885f688cb8afa74.jpg":
                "e6c5604304610c8f9007592c7174d207557952d8d90ee5af7900aaba85f242f4",
            "8225f67255bc623e.png":
                "d78eb1276e168acd65c20946a18591564858607e2c6bc9e3600634606b2e07b2",
            "7305f67030ae01f9.png":
                "8503fc1e4eff649d2dbec58b17f4035d15acd32e14749c4be33b8c3cad3af1c6",
        }
        for name, digest in expected.items():
            path = ROOT / ".working" / "ihp-777" / name
            if path.exists():
                self.assertEqual(digest, hashlib.sha256(path.read_bytes()).hexdigest())

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
