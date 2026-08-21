import hashlib
import json
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus/002_oracle-bone-inscriptions/008_source-record-candidates/"
    "008_obs-insc-src-cand-000008_met-42045_source-record-candidate"
)
PRIVATE_API = ROOT / ".working/met-42045/api.json"


class Met42045SourceRecordCandidateTests(unittest.TestCase):
    def test_human_entry_is_bilingual_and_bounded(self):
        readme = (OBJECT / "README.md").read_text(encoding="utf-8")
        self.assertIn("## English", readme)
        self.assertIn("## 简体中文", readme)
        self.assertIn("obs-insc-src-cand-000008", readme)
        self.assertIn("not a formal `obi-*` record", readme)
        self.assertIn("没有制作 OCR", readme)
        self.assertIn("10_external-image-label-review.md", readme)
        for path in OBJECT.glob("*.md"):
            for number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), 1
            ):
                self.assertLessEqual(
                    len(line), 80, f"{path}:{number}: {len(line)} characters"
                )

    def test_machine_record_preserves_api_and_candidate_boundaries(self):
        record = json.loads(
            (OBJECT / "90_source-record.json").read_text(encoding="utf-8")
        )
        self.assertEqual(record["candidate_id"], "obs-insc-src-cand-000008")
        self.assertEqual(record["object_id"], 42045)
        self.assertEqual(record["accession_number"], "67.43.14")
        self.assertEqual(record["rights_status"], "public_domain_verified")
        self.assertEqual(
            record["formal_inscription_identity"], "not_assigned"
        )
        self.assertEqual(record["ocr_status"], "not_collected")
        self.assertEqual(record["character_links"], [])
        self.assertIn("no decipherment conclusion", record["boundaries"])
        self.assertEqual(len(record["image_routes"]), 2)
        self.assertEqual(len(record["external_verification_routes"]), 2)
        self.assertEqual(
            record["external_verification_routes"][0]["evidence_role"],
            "secondary_view_label_only",
        )
        self.assertEqual(
            record["external_verification_routes"][0][
                "byte_identity_to_committed_asset"
            ],
            "exact_size_and_sha1_match_to_additionalImages_0",
        )
        self.assertEqual(
            record["external_verification_routes"][1][
                "byte_identity_to_committed_asset"
            ],
            "not_established",
        )

    def test_external_label_page_is_human_readable_and_bounded(self):
        path = OBJECT / "10_external-image-label-review.md"
        text = path.read_text(encoding="utf-8")
        self.assertIn("Oracle bone, China, back", text)
        self.assertIn("formal orientation status: `not_established`", text)
        self.assertIn("正式方向仍为", text)
        self.assertIn("no OCR, transcription", text)
        for number, line in enumerate(text.splitlines(), 1):
            self.assertLessEqual(
                len(line), 80, f"{path}:{number}: {len(line)} characters"
            )

    def test_external_snapshot_routes_match_recorded_hashes_when_present(self):
        record = json.loads(
            (OBJECT / "90_source-record.json").read_text(encoding="utf-8")
        )
        for route in record["external_verification_routes"]:
            path = ROOT / route["local_snapshot_path"]
            if not path.is_file():
                continue
            data = path.read_bytes()
            self.assertEqual(len(data), route["snapshot_size_bytes"])
            self.assertEqual(
                hashlib.sha256(data).hexdigest(), route["snapshot_sha256"]
            )

    def test_committed_images_match_recorded_bytes_and_dimensions(self):
        expected = {
            "001_asset-000001_met-42045-image-002.jpg": (
                1780568,
                "c605ae36f53ffdc5c1200e3bf23683aaaa6106a03e1c002ca5ab8f859e0333df",
            ),
            "002_asset-000002_met-42045-image-001.jpg": (
                1616877,
                "c2c09d618ed7da7e38b845164186590f7fa416ec3487a319c7de75b84330a480",
            ),
        }
        for name, (size, digest) in expected.items():
            path = OBJECT / "03_visual-assets" / name
            self.assertTrue(path.is_file(), path)
            data = path.read_bytes()
            self.assertEqual(len(data), size)
            self.assertEqual(hashlib.sha256(data).hexdigest(), digest)
            with Image.open(path) as image:
                self.assertEqual(image.size, (2667, 4000))

    @unittest.skipUnless(PRIVATE_API.exists(), "ignored Met API snapshot unavailable")
    def test_private_api_snapshot_replays_record_hash(self):
        data = PRIVATE_API.read_bytes()
        self.assertEqual(len(data), 1590)
        self.assertEqual(
            hashlib.sha256(data).hexdigest(),
            "74efc7255beeed6cf1400d86c336c5b97a5638a683956e83fa7216ad42f152b9",
        )
        payload = json.loads(data)
        self.assertEqual(payload["objectID"], 42045)
        self.assertTrue(payload["isPublicDomain"])
        self.assertEqual(payload["accessionNumber"], "67.43.14")
        self.assertEqual(len(payload["additionalImages"]), 1)


if __name__ == "__main__":
    unittest.main()
