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
    "1213": BASE / (
        "003_coll-obj-cand-00003_ihp-item-1213_collection-object-candidate"
    ),
    "1214": BASE / (
        "002_coll-obj-cand-00002_ihp-item-1214_collection-object-candidate"
    ),
}


EXPECTED = {
    "1213": {
        "en": (
            56872,
            "ee9d6d1527f4582df05e9915954bc3c4c43cd205122dd31ce7ae895068c226b6",
        ),
        "zh": (
            53500,
            "09d267ed23a21df98408ef35a92fde0c167de7566abd6399b5546400bb2c416d",
        ),
    },
    "1214": {
        "en": (
            60390,
            "d1808741004f62387dafb4464b6a8a16c9c03e84e5c74e476cd204474db936a2",
        ),
        "zh": (
            56788,
            "ed2135f0d27b1296293c9e9def9d55a95621473534a2dc4bfe0d26c3a2a556b0",
        ),
    },
}


class IhpCollectionObjectPageSnapshotTests(unittest.TestCase):
    def test_packet_records_two_language_snapshots(self):
        for item_id, object_dir in OBJECTS.items():
            packet = json.loads(
                (object_dir / "01_collection-object-packet.json").read_text(
                    encoding="utf-8"
                )
            )
            snapshots = packet["page_snapshots"]
            self.assertEqual([s["language"] for s in snapshots], ["en", "zh"])
            for snapshot in snapshots:
                size, digest = EXPECTED[item_id][snapshot["language"]]
                self.assertEqual(snapshot["size_bytes"], size)
                self.assertEqual(snapshot["sha256"], digest)
                self.assertEqual(snapshot["http_status"], 200)
                self.assertEqual(snapshot["source_text_locator"], "HTML .fr-view")
                self.assertEqual(
                    snapshot["rights_status"], "metadata_only_until_verified"
                )

    def test_snapshot_hashes_match_ignored_files_when_present(self):
        for item_id, object_dir in OBJECTS.items():
            packet = json.loads(
                (object_dir / "01_collection-object-packet.json").read_text(
                    encoding="utf-8"
                )
            )
            for snapshot in packet["page_snapshots"]:
                path = ROOT / snapshot["local_ignored_path"]
                if not path.exists():
                    continue
                payload = path.read_bytes()
                self.assertEqual(len(payload), snapshot["size_bytes"])
                self.assertEqual(
                    hashlib.sha256(payload).hexdigest(), snapshot["sha256"]
                )

    def test_human_entries_link_snapshot_evidence(self):
        for object_dir in OBJECTS.values():
            evidence = object_dir / "21_official-page-text-evidence.md"
            self.assertTrue(evidence.exists())
            text = evidence.read_text(encoding="utf-8")
            self.assertIn("metadata_only_until_verified", text)
            self.assertIn("not a project OCR", text)
            self.assertIn("abstain_withhold_candidate", text)
            for name in ("README.md", "07_collection-dossier-index.json"):
                self.assertIn(
                    "21_official-page-text-evidence.md",
                    (object_dir / name).read_text(encoding="utf-8"),
                )

    def test_source_display_is_bound_without_promotion(self):
        text_1213 = (
            OBJECTS["1213"] / "21_official-page-text-evidence.md"
        ).read_text(encoding="utf-8")
        text_1214 = (
            OBJECTS["1214"] / "21_official-page-text-evidence.md"
        ).read_text(encoding="utf-8")
        for value in (
            "丙辰卜，□貞：我受黍年。",
            "王占曰：吉。受有年。",
            "Bing Bian 0008",
            "R044295",
        ):
            self.assertIn(value, text_1213)
        for value in (
            "今夕又（有）",
            "□子（巳）卜，□□亡□。",
            "Jia Bian 0959",
            "R038861",
        ):
            self.assertIn(value, text_1214)

    def test_markdown_is_utf8_and_within_80_columns(self):
        for object_dir in OBJECTS.values():
            evidence = object_dir / "21_official-page-text-evidence.md"
            text = evidence.read_text(encoding="utf-8")
            long_lines = [
                (number, len(line))
                for number, line in enumerate(text.splitlines(), 1)
                if len(line) > 80
            ]
            self.assertEqual([], long_lines, str(evidence))


if __name__ == "__main__":
    unittest.main()
