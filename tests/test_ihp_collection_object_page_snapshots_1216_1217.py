import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = (
    ROOT
    / "corpus"
    / "005_excavation-sites-periods-and-batches"
    / "002_collection-object-candidates"
)


OBJECTS = {
    "1216": BASE / (
        "005_coll-obj-cand-00005_ihp-item-1216_collection-object-candidate"
    ),
    "1217": BASE / (
        "006_coll-obj-cand-00006_ihp-item-1217_collection-object-candidate"
    ),
}


EXPECTED = {
    "1216": {
        "page": {
            "en": (
                58084,
                "c10cda5a78f589ab4ffbf3004153bc792c9307eb02a29c759c24c881eb413e6c",
            ),
            "zh": (
                54532,
                "20de993b654f412f8f86f3071ddaa4858d9e53d6236bdb40c510154f14630818",
            ),
        },
        "inline": {
            "776675a819a64884.png": (
                13016,
                "87028d44fb2f99caa7bb053553ff085eeb0ca3a759b88f1aba198def42dba068",
            ),
            "966675a787e8714d.png": (
                44840,
                "23306cdddae956b439a2b9b101521ac4e28c052850e7c8675a1052b919d3ce90",
            ),
            "292675a78988c4ae.png": (
                62571,
                "46598ed19f76b71450df5cb49f0fac4d6040f54b7b8745aed1518f89573d5167",
            ),
        },
    },
    "1217": {
        "page": {
            "en": (
                57590,
                "4af8a37e65387587b05e458b035b3642fec1bd75310c12cf68f2427b474ccb22",
            ),
            "zh": (
                54369,
                "8b880db08252edfcc5d1b525dbbfa216540505b4a1a79ee510fa22e2c9d10ca0",
            ),
        },
        "inline": {
            "5986760d3e0ef6dc.png": (
                21946,
                "5a9800cd78692f6f9f0e3e110466e53f07fd9c23f3d1230cfc747b3a1241e66e",
            ),
            "2166760d45a19633.png": (
                14125,
                "2138e6fab64d3a8022605ed9c812cfc11a2dfe575b57bc383879ce5386863fa5",
            ),
            "7686760d4199d20f.png": (
                19662,
                "68e69258be79c30c864ab056f69c6247dd7b8437d17bd0b6064f47f3c54518f6",
            ),
        },
    },
}


class IhpCollectionObjectPageSnapshot1216And1217Tests(unittest.TestCase):
    def test_packet_records_page_and_inline_snapshot_hashes(self):
        for item_id, object_dir in OBJECTS.items():
            packet = json.loads(
                (object_dir / "01_collection-object-packet.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(
                [row["language"] for row in packet["page_snapshots"]],
                ["en", "zh"],
            )
            for row in packet["page_snapshots"]:
                size, digest = EXPECTED[item_id]["page"][row["language"]]
                self.assertEqual((row["size_bytes"], row["sha256"]), (size, digest))
                self.assertEqual(row["http_status"], 200)
                self.assertEqual(row["source_text_locator"], "HTML .fr-view")
            inline = {row["filename"]: row for row in packet["inline_image_snapshots"]}
            self.assertEqual(set(inline), set(EXPECTED[item_id]["inline"]))
            for filename, row in inline.items():
                self.assertEqual(
                    (row["size_bytes"], row["sha256"]),
                    EXPECTED[item_id]["inline"][filename],
                )
                self.assertEqual(row["http_status"], 200)
                self.assertEqual(row["content_type"], "image/png")
                self.assertEqual(
                    row["rights_status"], "metadata_only_until_verified"
                )

    def test_local_snapshot_hashes_match_when_ignored_files_are_present(self):
        for object_dir in OBJECTS.values():
            packet = json.loads(
                (object_dir / "01_collection-object-packet.json").read_text(
                    encoding="utf-8"
                )
            )
            for row in packet["page_snapshots"] + packet["inline_image_snapshots"]:
                path = ROOT / row["local_ignored_path"]
                if not path.exists():
                    continue
                payload = path.read_bytes()
                self.assertEqual(len(payload), row["size_bytes"])
                self.assertEqual(
                    hashlib.sha256(payload).hexdigest(), row["sha256"]
                )

    def test_human_entries_link_and_preserve_placeholders(self):
        text_1216 = (
            OBJECTS["1216"] / "19_official-page-text-evidence.md"
        ).read_text(encoding="utf-8")
        text_1217 = (
            OBJECTS["1217"] / "19_official-page-text-evidence.md"
        ).read_text(encoding="utf-8")
        for text in (text_1216, text_1217):
            self.assertIn("metadata_only_until_verified", text)
            self.assertIn("not project\nOCR", text)
            self.assertIn("abstain_withhold_candidate", text)
        for value in (
            "乙丑卜：又（有）[776675a819a64884.png]（瘳）目今日。",
            "Yi Bian 8806+8865+8997",
            "ZR044855",
            "source_reported_partial_display_with_inline_placeholders",
        ):
            self.assertIn(value, text_1216)
        for value in (
            "壬申卜，古貞：帝令雨。",
            "5986760d3e0ef6dc.png",
            "Bing Bian 0065",
            "R041291",
        ):
            self.assertIn(value, text_1217)
        for object_dir in OBJECTS.values():
            for name in ("README.md", "07_collection-dossier-index.json"):
                self.assertIn(
                    "19_official-page-text-evidence.md",
                    (object_dir / name).read_text(encoding="utf-8"),
                )

    def test_markdown_is_utf8_and_within_80_columns(self):
        for object_dir in OBJECTS.values():
            evidence = object_dir / "19_official-page-text-evidence.md"
            text = evidence.read_text(encoding="utf-8")
            long_lines = [
                (number, len(line))
                for number, line in enumerate(text.splitlines(), 1)
                if len(line) > 80
            ]
            self.assertEqual([], long_lines, str(evidence))


if __name__ == "__main__":
    unittest.main()
