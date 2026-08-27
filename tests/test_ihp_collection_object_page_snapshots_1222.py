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
    / "008_coll-obj-cand-00008_ihp-item-1222_collection-object-candidate"
)


EXPECTED_PAGE = {
    "en": (
        58529,
        "af682fc6e6ff786cf79c5f91033ba5c59ea3025246208d791e9167cccced15f4",
    ),
    "zh": (
        55018,
        "9abb7e7bff9b05789e06810f7b8c3c2b5b9ab37ebf756e16a25c67a3d8c150f4",
    ),
}

EXPECTED_IMAGES = {
    "43367571cc964c58.jpg": (
        335264,
        "d59a6cbd401daf184880e58a7aa826e310bc2ee481f71a91a4aa2f3d18ac45bf",
    ),
    "99967571cca1e09f.jpg": (
        370055,
        "cf9f1e84be0a26d7f21eac7c06014dc1370eb08f346c6f01ac37e8004578631d",
    ),
}

EXPECTED_INLINE_IMAGES = {
    "615675a84fd057c0.png": (
        9755,
        "790b5bdfab55f32e5c70754bd8d31919e7e7b4d411191840347f051639f80d68",
    ),
    "45675a850458b46.png": (
        11960,
        "c7faa73136d26f31577dd07f0281cdc83c74a56c8560108504f3f562c057147e",
    ),
    "501675a8509b92c9.png": (
        13174,
        "7843660cb4d19a105f2bea0aafbdae51fe0dc953baa3dd667062a12660df4805",
    ),
}


class IhpCollectionObjectPageSnapshot1222Tests(unittest.TestCase):
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

    def test_packet_records_large_image_hashes_and_rights(self):
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

    def test_packet_records_inline_image_hashes_and_rights(self):
        packet = self._packet()
        images = {
            row["filename"]: row
            for row in packet["inline_image_snapshots"]
        }
        self.assertEqual(set(images), set(EXPECTED_INLINE_IMAGES))
        for filename, row in images.items():
            self.assertEqual(
                (row["size_bytes"], row["sha256"]),
                EXPECTED_INLINE_IMAGES[filename],
            )
            self.assertEqual(row["http_status"], 200)
            self.assertEqual(row["content_type"], "image/png")
            self.assertEqual(
                row["rights_status"], "metadata_only_until_verified"
            )

    def test_local_snapshot_hashes_match_when_present(self):
        packet = self._packet()
        rows = (
            packet["page_snapshots"]
            + packet["image_snapshots"]
            + packet["inline_image_snapshots"]
        )
        for row in rows:
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
        for value in (
            "[子]曰□子曰名曰",
            "615675a84fd057c0.png",
            "source_reported_fragmentary_display_with_placeholders",
            "metadata_only_until_verified",
            "abstain_withhold_candidate",
        ):
            self.assertIn(value, evidence)
        self.assertIn("not project OCR", evidence)
        for name in (
            "README.md",
            "07_collection-dossier-index.json",
            "09_collection-provenance-evidence-index.json",
        ):
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
