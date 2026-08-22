import hashlib
import json
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


EXPECTED_PAGE = {
    "en": (
        55901,
        "8d0c3b33673cfd44e8414ce0fbb12404dff93efa2b7233dfe61ced3d76160a89",
    ),
    "zh": (
        52337,
        "d087291a21d3aeaadbbfffcff98fc0d0b08d69b99b20861b41f05a471dc072cf",
    ),
}

EXPECTED_IMAGES = {
    "126675715f2cc7d9.jpg": (
        272912,
        "d7c18746ae055d85493cd933caf4844b08156aaff498ad5572cba1b96d6f6832",
    ),
    "74675715f370ec2.jpg": (
        302051,
        "eef05287c2881090c9fd55485db151420292a0bef7227faf596c95ddc87b9f31",
    ),
}


class IhpCollectionObjectPageSnapshot1218Tests(unittest.TestCase):
    def _packet(self):
        return json.loads(
            (OBJECT / "01_collection-object-packet.json").read_text(
                encoding="utf-8"
            )
        )

    def test_packet_records_page_hashes(self):
        packet = self._packet()
        self.assertEqual(
            {row["language"] for row in packet["page_snapshots"]},
            {"en", "zh"},
        )
        for row in packet["page_snapshots"]:
            self.assertEqual(
                (row["size_bytes"], row["sha256"]),
                EXPECTED_PAGE[row["language"]],
            )
            self.assertEqual(row["http_status"], 200)
            self.assertEqual(row["source_text_locator"], "HTML .fr-view")

    def test_packet_records_image_hashes_and_rights(self):
        packet = self._packet()
        images = {row["filename"]: row for row in packet["image_snapshots"]}
        self.assertEqual(set(images), set(EXPECTED_IMAGES))
        for filename, row in images.items():
            self.assertEqual(
                (row["size_bytes"], row["sha256"]),
                EXPECTED_IMAGES[filename],
            )
            self.assertEqual(row["http_status"], 200)
            self.assertEqual(row["content_type"], "image/jpeg")
            self.assertEqual(
                row["rights_status"], "metadata_only_until_verified"
            )

    def test_local_snapshot_hashes_match_when_present(self):
        packet = self._packet()
        for row in packet["page_snapshots"] + packet["image_snapshots"]:
            path = ROOT / row["local_ignored_path"]
            if not path.exists():
                continue
            payload = path.read_bytes()
            self.assertEqual(len(payload), row["size_bytes"])
            self.assertEqual(
                hashlib.sha256(payload).hexdigest(), row["sha256"]
            )

    def test_human_entries_preserve_source_display_and_boundary(self):
        evidence = (OBJECT / "19_official-page-text-evidence.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("壬辰卜，爭：自今五日至于丙申不其雨。", evidence)
        self.assertIn("source_reported_partial_display_with_ellipsis", evidence)
        self.assertIn("metadata_only_until_verified", evidence)
        self.assertIn("abstain_withhold_candidate", evidence)
        self.assertIn("not project OCR", evidence)
        for name in ("README.md", "07_collection-dossier-index.json"):
            text = (OBJECT / name).read_text(encoding="utf-8")
            self.assertIn("19_official-page-text-evidence.md", text)

    def test_human_markdown_is_utf8_and_within_80_columns(self):
        evidence = (OBJECT / "19_official-page-text-evidence.md").read_text(
            encoding="utf-8"
        )
        long_lines = [
            (number, len(line))
            for number, line in enumerate(evidence.splitlines(), 1)
            if len(line) > 80
        ]
        self.assertEqual([], long_lines, str(OBJECT))


if __name__ == "__main__":
    unittest.main()
