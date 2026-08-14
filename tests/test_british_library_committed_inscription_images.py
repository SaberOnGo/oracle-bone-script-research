import hashlib
import json
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]


CASES = {
    "bl-1595": {
        "directory": ROOT
        / "corpus/002_oracle-bone-inscriptions/008_source-record-candidates/"
        / "005_obs-insc-src-cand-000005_bl-or-1595_source-record-candidate",
        "images": {
            "03_visual-assets/001_asset-000001_bl-1595r.png": (
                942112,
                "ddecad64f5b958ec3c4425bad53dbe90c7f782b41622a672b7ec6d971ddf9c19",
                (681, 898),
            ),
            "03_visual-assets/002_asset-000002_bl-1595v.png": (
                933246,
                "5833d7fc96d0d5a2878bd6981c0110c5919613cd4d382ad45f93f3451bf342f4",
                (610, 905),
            ),
        },
        "dossier": "02_human-inscription-dossier.md",
        "record": "90_source-record.json",
    },
    "bl-1535": {
        "directory": ROOT
        / "corpus/002_oracle-bone-inscriptions/008_source-record-candidates/"
        / "006_obs-insc-src-cand-000006_bl-or-1535_source-record-candidate",
        "images": {
            "03_visual-assets/001_asset-000001_bl-1535v.jpg": (
                975908,
                "88e5337e29035d70c89a2ba6339f1973d0e808865b312dd0131fd9f4d"
                "db96ca6",
                (1670, 1714),
            ),
        },
        "dossier": "02_human-inscription-dossier.md",
        "record": "90_source-record.json",
    },
}


class BritishLibraryCommittedImageTests(unittest.TestCase):
    def test_source_bytes_are_committed_with_expected_hash_and_dimensions(self):
        for case in CASES.values():
            with self.subTest(directory=case["directory"]):
                for relative, (size, digest, dimensions) in case["images"].items():
                    path = case["directory"] / relative
                    self.assertTrue(path.is_file(), path)
                    self.assertEqual(path.stat().st_size, size, path)
                    self.assertEqual(
                        hashlib.sha256(path.read_bytes()).hexdigest(), digest, path
                    )
                    with Image.open(path) as image:
                        self.assertEqual(image.size, dimensions, path)

    def test_records_and_human_pages_link_the_committed_source_bytes(self):
        for case in CASES.values():
            with self.subTest(directory=case["directory"]):
                record = json.loads(
                    (case["directory"] / case["record"]).read_text(
                        encoding="utf-8"
                    )
                )
                self.assertEqual(
                    record["image_status"],
                    "public_direct_route_and_committed_source_bytes",
                )
                self.assertEqual(record["rights_status"], "public_domain_verified")
                committed = {
                    route["committed_path"] for route in record["image_routes"]
                }
                self.assertEqual(committed, set(case["images"]))

                dossier = (case["directory"] / case["dossier"]).read_text(
                    encoding="utf-8"
                )
                for relative in case["images"]:
                    self.assertIn(relative, dossier)
                self.assertNotIn("not committed", dossier.lower())
                self.assertNotIn("不提交二进制图像", dossier)

    def test_markdown_files_stay_within_human_line_limit(self):
        for case in CASES.values():
            for path in case["directory"].glob("*.md"):
                violations = [
                    f"{path}:{line_number}:{len(line)}"
                    for line_number, line in enumerate(
                        path.read_text(encoding="utf-8").splitlines(), start=1
                    )
                    if len(line) > 80
                ]
                self.assertEqual(violations, [])


if __name__ == "__main__":
    unittest.main()
