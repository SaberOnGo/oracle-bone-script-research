import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "005_excavation-sites-periods-and-batches"
    / "002_collection-object-candidates"
    / "019_coll-obj-cand-00019_ihp-item-763_collection-object-candidate"
)
EVIDENCE = OBJECT / "18_live-source-evidence-review.md"


class IhpItem763LiveSourceEvidenceTests(unittest.TestCase):
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
            "https://museum.sinica.edu.tw/en/collection/32/item/763/",
            "https://museum.sinica.edu.tw/collection/32/item/763/",
            "Source collection item ID / 馆藏对象号: `763`",
            "Item No. / 馆藏编号: `R003617`",
            "Antler Object Chia 3942",
            "鹿角器《甲》3942",
            "Late Shang Period",
            "7.2(H)×3(Dia.) cm",
            "Pit HPK1091, Hsi-pei-kang, Hou-chia-chuang",
            "亞（ ）雀（ ）",
            "source_reported_name_description_with_inline_gaps",
            "OCR correction",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_binds_image_route_and_local_observation(self):
        required = (
            "3305f6893b38768f.jpg",
            "367549",
            "fa63c4f4f4313908beea72bfdae10dbf49dbb10ffc531bacb02329c33ac554ad",
            "959 x 1280",
            "image/jpeg",
            "darkened carved",
            "metadata_only_until_verified",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_records_snapshots_and_rights(self):
        required = (
            "en.html",
            "58,680",
            "10ce2db5b883e6e0a7aada44f5e705b4e2eede0b151ab0d3e9b54895a0177ebf1",
            "zh.html",
            "55,383",
            "9794d06819887510255f3e7e08fa57872e87d83c21611498fb3c71c81bbcc790",
            "Concrete next checks / 具体下一步待查",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_private_image_hash_matches_when_present(self):
        path = ROOT / ".working" / "ihp-763" / "large.jpg"
        if path.exists():
            self.assertEqual(
                "fa63c4f4f4313908beea72bfdae10dbf49dbb10ffc531bacb02329c33ac554ad",
                hashlib.sha256(path.read_bytes()).hexdigest(),
            )

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
