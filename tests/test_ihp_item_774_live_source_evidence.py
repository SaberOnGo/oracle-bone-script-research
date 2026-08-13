import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "005_excavation-sites-periods-and-batches"
    / "002_collection-object-candidates"
    / "010_coll-obj-cand-00010_ihp-item-774_collection-object-candidate"
)
EVIDENCE = OBJECT / "18_live-source-evidence-review.md"


class IhpItem774LiveSourceEvidenceTests(unittest.TestCase):
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
            "https://museum.sinica.edu.tw/en/collection/32/item/774/",
            "https://museum.sinica.edu.tw/collection/32/item/774/",
            "Source collection item ID / 馆藏对象号: `774`",
            "Item No. / 馆藏编号: `R041037`",
            "Inscribed Bovid Skull Chia 3939",
            "牛头骨刻辞《甲》3939",
            "Late Shang Period",
            "商代晚期",
            "Bovid Skull",
            "河南省安阳县小屯",
            "隻（獲）白兕。",
            "source_reported_displayed_single_line_not_independently_edited",
            "not a new transcription",
            "not a project reading",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_page_binds_all_eight_image_routes(self):
        routes = (
            (
                "7625f68801a92d3f.jpg",
                "329,979",
                "0a07288fcb9b65fc240f54cb70db9d89acd023128afe5723d51f87f522e873db",
                "1280 x 1001",
            ),
            (
                "1785f6880252f44b.png",
                "841,522",
                "5eac743794f436bba4fceee8998c3c8ba2a077305d46dd8e9f7867ce6add7beb",
                "582 x 1280",
            ),
            (
                "1085f688020bb556.jpg",
                "312,441",
                "1522d0cdefdad4a21cb6bfb5ff77c689518a7f7e299ba34ac053b646aa4363de",
                "960 x 1280",
            ),
            (
                "4615f68801c4a23b.jpg",
                "299,978",
                "e77bc0158fea16d6d486c36165ebcde6a0fed68f532746cc0e633af9da2eb1c8",
                "960 x 1280",
            ),
            (
                "9765f68802a88ef3.jpg",
                "354,332",
                "52a4bc05c5c9367ba7c8e23abf3625c871eb1a030d9ea0abc3e2f7f7a797231e",
                "1280 x 993",
            ),
            (
                "7905f68801e8e713.jpg",
                "342,072",
                "a07eb002ddfc742f3c4eb9762b09e39f5a37fe1b577a40086cdbf1c6dc12fbeb",
                "1280 x 993",
            ),
            (
                "2435f6880230028a.jpg",
                "326,301",
                "068c20fe7429aafb0120c80306035a26f7586e7fbe1def707ee767688c113393",
                "1280 x 1022",
            ),
            (
                "4675f68802ccd3d6.jpg",
                "289,392",
                "9ad8f85f7b07556e7f0f2751dedfb7ee9f0a70fb8f9c52baee8b87c4829f01dd",
                "1280 x 1022",
            ),
        )
        for filename, size, digest, pixels in routes:
            for value in (filename, size, digest, pixels):
                self.assertIn(value, self.text)
        self.assertEqual(self.text.count("image/jpeg"), 7)
        self.assertEqual(self.text.count("image/png"), 1)
        self.assertEqual(
            self.text.count("local_private_visual_inspection_only"), 10
        )
        self.assertIn("processed or annotated source image", self.text)

    def test_page_records_snapshots_pdf_and_rights(self):
        required = (
            "en.html",
            "64,150",
            "383893de2b39a735f63ec4cd3147612ae541984ef384b414fbd212d4b3267f34",
            "zh.html",
            "60,735",
            "02796c84a7dc5fedfce05ac4f0754b85370a3e2c3134e50ab69f356d175d147c",
            "Cattle_M_cranium_UD.pdf",
            "7,030,210",
            "af57b389ad566ec19b45251c1e0ae3c81700e3d2c94bc91375f3439c4c0b2c37",
            "metadata_only_until_verified",
            "Concrete next checks / 具体下一步待查",
        )
        for value in required:
            self.assertIn(value, self.text)

    def test_private_route_files_match_documented_hashes_when_present(self):
        files = {
            "7625f68801a92d3f.jpg":
                "0a07288fcb9b65fc240f54cb70db9d89acd023128afe5723d51f87f522e873db",
            "1785f6880252f44b.png":
                "5eac743794f436bba4fceee8998c3c8ba2a077305d46dd8e9f7867ce6add7beb",
            "1085f688020bb556.jpg":
                "1522d0cdefdad4a21cb6bfb5ff77c689518a7f7e299ba34ac053b646aa4363de",
            "4615f68801c4a23b.jpg":
                "e77bc0158fea16d6d486c36165ebcde6a0fed68f532746cc0e633af9da2eb1c8",
            "9765f68802a88ef3.jpg":
                "52a4bc05c5c9367ba7c8e23abf3625c871eb1a030d9ea0abc3e2f7f7a797231e",
            "7905f68801e8e713.jpg":
                "a07eb002ddfc742f3c4eb9762b09e39f5a37fe1b577a40086cdbf1c6dc12fbeb",
            "2435f6880230028a.jpg":
                "068c20fe7429aafb0120c80306035a26f7586e7fbe1def707ee767688c113393",
            "4675f68802ccd3d6.jpg":
                "9ad8f85f7b07556e7f0f2751dedfb7ee9f0a70fb8f9c52baee8b87c4829f01dd",
            "Cattle_M_cranium_UD.pdf":
                "af57b389ad566ec19b45251c1e0ae3c81700e3d2c94bc91375f3439c4c0b2c37",
        }
        temp = ROOT / ".working" / "ihp-774"
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
