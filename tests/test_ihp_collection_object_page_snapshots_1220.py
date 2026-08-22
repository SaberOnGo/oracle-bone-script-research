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
    / "009_coll-obj-cand-00009_ihp-item-1220_collection-object-candidate"
)


EXPECTED_PAGE = {
    "en": (
        55815,
        "098dd86f277f230bf319ca32b2e5fd922d2083445156ecb231aeb25441a3c521",
    ),
    "zh": (
        52356,
        "6d5629bfe35dfc337857404511c4e728839a1ce93e83708d6293a42d1a7692a2",
    ),
}

EXPECTED_IMAGES = {
    "4692_8867571a214d619.jpg": (
        436863,
        "4e3ed1b465a20db30bf1a183c83d2971103c795d05b71f35c810106243d6f8e0",
    ),
    "4692_61267571a221a42b.jpg": (
        452835,
        "cbf5ea35a5685e30abd0281e7c39a255edf6675d558da1fbcef234d1360295fa",
    ),
}


class IhpCollectionObjectPageSnapshot1220Tests(unittest.TestCase):
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
        for value in (
            "庚戌卜，爭貞：岳害我。",
            "庚戌卜，爭貞：岳不我害。",
            "source_reported_displayed_two_lines_not_independently_edited",
            "metadata_only_until_verified",
            "abstain_withhold_candidate",
        ):
            self.assertIn(value, evidence)
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
