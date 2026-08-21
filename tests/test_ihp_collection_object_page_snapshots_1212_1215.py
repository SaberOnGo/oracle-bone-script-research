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
    "1212": BASE / (
        "001_coll-obj-cand-00001_ihp-item-1212_collection-object-candidate"
    ),
    "1215": BASE / (
        "004_coll-obj-cand-00004_ihp-item-1215_collection-object-candidate"
    ),
}


EXPECTED = {
    "1212": {
        "en": (
            56861,
            "41d05aeb8b0788017c576dd09001a0417e258735f4df0a43beb2cf68a2d0f58a",
        ),
        "zh": (
            53011,
            "330ca1fb56626e744d764a1bc45b9f71dbd3fccc745acdc47deca004da4336f9",
        ),
    },
    "1215": {
        "en": (
            56558,
            "a0edac3896f0b2839afcc27738454897668c1f709bef841fabf9a1d5048a619d",
        ),
        "zh": (
            53534,
            "dad4a5c58cd93058276ded2e6cff4952a527dbfb69608d3283f11536841d461e",
        ),
    },
}


class IhpCollectionObjectPageSnapshot1212And1215Tests(unittest.TestCase):
    def test_packet_records_exact_language_snapshots(self):
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
                size, digest = EXPECTED[item_id][row["language"]]
                self.assertEqual(row["size_bytes"], size)
                self.assertEqual(row["sha256"], digest)
                self.assertEqual(row["http_status"], 200)
                self.assertEqual(row["source_text_locator"], "HTML .fr-view")
                self.assertEqual(
                    row["rights_status"], "metadata_only_until_verified"
                )

    def test_local_snapshot_hashes_match_when_ignored_files_are_present(self):
        for item_id, object_dir in OBJECTS.items():
            packet = json.loads(
                (object_dir / "01_collection-object-packet.json").read_text(
                    encoding="utf-8"
                )
            )
            for row in packet["page_snapshots"]:
                path = ROOT / row["local_ignored_path"]
                if not path.exists():
                    continue
                payload = path.read_bytes()
                self.assertEqual(len(payload), row["size_bytes"])
                self.assertEqual(
                    hashlib.sha256(payload).hexdigest(), row["sha256"]
                )

    def test_human_entries_link_and_bound_source_display(self):
        text_1212 = (
            OBJECTS["1212"] / "19_official-page-text-evidence.md"
        ).read_text(encoding="utf-8")
        text_1215 = (
            OBJECTS["1215"] / "19_official-page-text-evidence.md"
        ).read_text(encoding="utf-8")
        for text in (text_1212, text_1215):
            self.assertIn("metadata_only_until_verified", text)
            self.assertIn("not project OCR", text)
            self.assertIn("abstain_withhold_candidate", text)
        for value in (
            "戊戌帚（婦）喜示一屯。岳。",
            "Jia Bian 3333+3361",
            "R035888",
        ):
            self.assertIn(value, text_1212)
        for value in (
            "帚（婦）井示。韋。",
            "Yi Bian 3330+5281+Yi Bian buyi 4936",
            "R044587",
        ):
            self.assertIn(value, text_1215)
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
