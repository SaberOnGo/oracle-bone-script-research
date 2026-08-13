import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "005_excavation-sites-periods-and-batches"
    / "002_collection-object-candidates"
    / "012_coll-obj-cand-00012_ihp-item-761_collection-object-candidate"
)
EVIDENCE = OBJECT / "18_live-source-evidence-review.md"


class IhpItem761LiveSourceEvidenceTests(unittest.TestCase):
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
            "https://museum.sinica.edu.tw/en/collection/32/item/761/",
            "https://museum.sinica.edu.tw/collection/32/item/761/",
            "Source collection item ID / 馆藏对象号: `761`",
            "Item No. / 馆藏编号: `R034847`",
            "Inscribed Animal Bone Fragment Chia 2659+2716+2763",
            "Late Shang Period",
            "商代晚期",
            "Animal Bone",
            "14.0(L)×12.1(W) cm",
            "practice inscriptions depicting a",
            "deer and two buffalo-like animals locking horns",
            "source_reported_displayed_description_without_transcription",
            "No OCR, character segmentation, or reading",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_binds_all_three_image_routes(self):
        routes = (
            (
                "1865f6886c275aed.jpg",
                "328,234",
                "46c8df3e2cda73a8a9c4a1be989101f1b8274caa1a0fe3646851e28bb6494118",
                "1022 x 1280",
            ),
            (
                "2615f6886b95c8c0.png",
                "1,241,036",
                "0b4f0fbd21c08352ef7deaee86f4d0cbefc5d8a962ddeb26f45de8c26b32d876",
                "1121 x 1280",
            ),
            (
                "1325f6886c023932.jpg",
                "319,181",
                "2f691e133c66ba43435767bfe30e8390bdb48398afc07d275abb09f293c7865b",
                "1022 x 1280",
            ),
        )
        for filename, size, digest, pixels in routes:
            for value in (filename, size, digest, pixels):
                self.assertIn(value, self.text)
        self.assertEqual(self.text.count("image/jpeg"), 2)
        self.assertEqual(self.text.count("image/png"), 1)
        self.assertEqual(
            self.text.count("local_private_visual_inspection_only"), 5
        )
        self.assertIn("processed view", self.text)

    def test_page_records_snapshots_and_rights(self):
        required = (
            "en.html",
            "57,382",
            "1e8975488d7ad8ced4057f39a4dbf4a66fd99b8d032286b4982f6796887b7f23",
            "zh.html",
            "53,531",
            "cbfce084610be72fbecc893154abd674fba5e422bced44f55bffbf6fa7dcaf7a",
            "metadata_only_until_verified",
            "1 / 3",
            "Concrete next checks / 具体下一步待查",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_private_route_files_match_documented_hashes_when_present(self):
        files = {
            "1865f6886c275aed.jpg":
                "46c8df3e2cda73a8a9c4a1be989101f1b8274caa1a0fe3646851e28bb6494118",
            "2615f6886b95c8c0.png":
                "0b4f0fbd21c08352ef7deaee86f4d0cbefc5d8a962ddeb26f45de8c26b32d876",
            "1325f6886c023932.jpg":
                "2f691e133c66ba43435767bfe30e8390bdb48398afc07d275abb09f293c7865b",
        }
        temp = ROOT / ".working" / "ihp-761"
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
