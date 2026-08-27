from __future__ import annotations

import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = (
    ROOT
    / "corpus/002_oracle-bone-inscriptions/008_source-record-candidates/"
    "010_obs-insc-src-cand-000010_ihp-item-1222_source-record-candidate"
)


class IhpItem1222OriginalPlateEvidenceTests(unittest.TestCase):
    def test_original_plate_dossiers_and_index_exist(self):
        self.assertTrue(
            (CANDIDATE / "11_original-plate-and-join-history.md").is_file()
        )
        self.assertTrue(
            (CANDIDATE / "12_original-pdf-capture-record.md").is_file()
        )
        self.assertTrue((CANDIDATE / "93_plate-source-index.csv").is_file())

    def test_human_record_exposes_join_history_and_plate_limits(self):
        text = (
            CANDIDATE / "11_original-plate-and-join-history.md"
        ).read_text(encoding="utf-8")
        flat = " ".join(text.split())
        for marker in (
            "Yi Bian Supplement 5369",
            "Yinxu wenzi zhuihe",
            "group 295",
            "group 165",
            "page 151",
            "pages 14-17",
            "plate-layout corroboration candidate",
            "图版布局互证候选",
            "source transcription only",
            "仅为来源释文",
            "seam",
            "接缝",
        ):
            self.assertIn(marker, flat)
        self.assertNotIn("not_collected", text)
        self.assertTrue(all(len(line) <= 80 for line in text.splitlines()))

    def test_capture_record_binds_official_pdf_and_workshop_image(self):
        text = (
            CANDIDATE / "12_original-pdf-capture-record.md"
        ).read_text(encoding="utf-8")
        for marker in (
            "b25b6841ee7f7e88c12a076a5c3da4cea55d562e7a978956aec4210841b4caf9",
            "5809557",
            "34 pages",
            "7108f9ec9b5ba25166c73ef6d456a598452c71369e6a4f76fd085183c41bf3d0",
            "metadata_only_until_verified",
            "text extraction failed",
            "文字提取失败",
        ):
            self.assertIn(marker, text)
        self.assertTrue(all(len(line) <= 80 for line in text.splitlines()))

    def test_support_index_keeps_plate_relations_as_candidates(self):
        with (CANDIDATE / "93_plate-source-index.csv").open(
            encoding="utf-8-sig", newline=""
        ) as handle:
            rows = list(csv.DictReader(handle))
        self.assertGreaterEqual(len(rows), 4)
        self.assertTrue(all(row["formal_identity"] == "withheld" for row in rows))
        self.assertTrue(
            all(row["rights_status"] == "metadata_only_until_verified" for row in rows)
        )
        self.assertIn(
            "reverse_face_crosswalk_candidate",
            {row["relation_status"] for row in rows},
        )


if __name__ == "__main__":
    unittest.main()
