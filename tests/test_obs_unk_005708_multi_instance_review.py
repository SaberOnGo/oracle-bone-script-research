import hashlib
import io
import json
import re
import unittest
import zipfile
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "001_oracle-characters"
    / "074_undeciphered-005701-005800_obs-unk-bucket_oracle-character-candidates"
    / "008_obs-unk-005708_hust-obc-und-X-005708_oracle-character-candidate"
)
DOSSIER = OBJECT / "17_multi-instance-visual-comparison.md"
RECEIPT = OBJECT / "18_multi-instance-visual-receipt.json"
RAW_ZIP = (
    ROOT
    / "external_local_archive"
    / "source_packages"
    / "hust-obc"
    / "dl-hust-obc-figshare-raw.zip"
)


class ObsUnk005708MultiInstanceReviewTests(unittest.TestCase):
    def test_receipt_records_all_fifty_members_and_group_counts(self) -> None:
        data = json.loads(RECEIPT.read_text(encoding="utf-8"))
        self.assertEqual("obs-unk-005708", data["project_id"])
        self.assertEqual("large-src-000001", data["source_package_id"])
        self.assertEqual("dl-hust-obc-figshare-raw", data["download_id"])
        self.assertEqual(50, data["member_count"])
        self.assertEqual(50, len(data["members"]))
        expected = {str(value): 4 for value in range(1176, 1188)}
        expected["1188"] = 2
        self.assertEqual(expected, data["source_number_member_counts"])
        self.assertEqual(
            "dataset_grouping_candidate_not_glyph_identity",
            data["claim_boundary"],
        )
        self.assertEqual("withhold", data["adjudication"])
        self.assertNotIn("probability", data)

    def test_human_dossier_records_comparison_counterevidence_and_falsifiers(self):
        text = DOSSIER.read_text(encoding="utf-8-sig")
        for marker in (
            "obs-unk-005708",
            "50 image members",
            "13 source-number groups",
            "Mixed-group warning / 混组警告",
            "Two-way Falsification / 双向证伪",
            "source_marked_risk_noted",
            "18_multi-instance-visual-receipt.json",
            "does not establish a reading",
            "不确认字形身份",
        ):
            self.assertIn(marker, text)
        for number in range(1176, 1189):
            self.assertIn(f"## Group {number} / 来源编号组 {number}", text)
        self.assertNotIn("not_collected", text)
        self.assertNotIn("TODO", text)

    def test_object_human_entries_expose_the_opened_comparison(self) -> None:
        for name in (
            "README.md",
            "05_human-research-dossier.md",
            "10_archaeology-paleography-review.md",
            "12_human-research-readiness-review.md",
        ):
            text = (OBJECT / name).read_text(encoding="utf-8-sig")
            self.assertIn("17_multi-instance-visual-comparison.md", text)
        readiness = (OBJECT / "12_human-research-readiness-review.md").read_text(
            encoding="utf-8-sig"
        )
        self.assertIn("opened visual members: `50`", readiness)
        self.assertIn("dataset grouping: `disputed_candidate`", readiness)

    def test_review_dimensions_do_not_contradict_each_other(self) -> None:
        human = (OBJECT / "12_human-research-readiness-review.md").read_text(
            encoding="utf-8-sig"
        )
        support = json.loads(
            (OBJECT / "13_human-research-readiness-index.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertNotIn("needs_human_visual_review", human)
        self.assertNotIn("not a glyph observation already reviewed", human)
        self.assertIn("source member visual review: `direct_checked`", human)
        self.assertIn("glyph identity review: `withheld`", human)
        self.assertEqual("direct_checked", support["source_member_visual_review"])
        self.assertEqual("disputed_candidate", support["dataset_grouping"])
        self.assertEqual("withheld", support["glyph_identity_review"])

    def test_human_dossier_is_bilingual_and_within_eighty_columns(self) -> None:
        text = DOSSIER.read_text(encoding="utf-8-sig")
        self.assertIn("## Purpose And Boundary / 目的与边界", text)
        self.assertIn("## Research Boundary / 研究边界", text)
        violations = [
            f"{number}:{len(line)}"
            for number, line in enumerate(text.splitlines(), 1)
            if len(line) > 80
        ]
        self.assertEqual([], violations)

    @unittest.skipUnless(RAW_ZIP.exists(), "ignored HUST raw ZIP unavailable")
    def test_receipt_recomputes_from_registered_raw_zip(self) -> None:
        data = json.loads(RECEIPT.read_text(encoding="utf-8"))
        expected = {member["member_key"]: member for member in data["members"]}
        actual = {}
        prefix = "HUST-OBC/undeciphered/X/1264/"
        with zipfile.ZipFile(RAW_ZIP, metadata_encoding="gbk") as archive:
            for name in archive.namelist():
                if not name.startswith(prefix) or name.endswith("/"):
                    continue
                match = re.search(r"_(11(?:7[6-9]|8[0-8]))_([1-4])\.png$", name)
                self.assertIsNotNone(match, name)
                key = f"{match.group(1)}_{match.group(2)}"
                info = archive.getinfo(name)
                payload = archive.read(name)
                with Image.open(io.BytesIO(payload)) as image:
                    image.load()
                    actual[key] = {
                        "sha256": hashlib.sha256(payload).hexdigest(),
                        "size_bytes": len(payload),
                        "compressed_bytes": info.compress_size,
                        "pixel_width": image.width,
                        "pixel_height": image.height,
                        "mode": image.mode,
                    }
        self.assertEqual(set(expected), set(actual))
        for key, computed in actual.items():
            for field, value in computed.items():
                self.assertEqual(value, expected[key][field], f"{key}:{field}")


if __name__ == "__main__":
    unittest.main()
