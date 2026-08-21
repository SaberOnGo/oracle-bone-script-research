from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUIDE = (
    ROOT
    / "corpus/002_oracle-bone-inscriptions/000_inscription-registers/"
    "005_opened-source-record-candidate-guide.md"
)
README = ROOT / "corpus/002_oracle-bone-inscriptions/README.md"


class OpenedSourceRecordCandidateGuideTests(unittest.TestCase):
    def test_guide_is_bilingual_and_human_first(self):
        text = GUIDE.read_text(encoding="utf-8")
        self.assertIn("## Purpose / 用途", text)
        self.assertIn("## Candidate queue / 候选队列", text)
        self.assertIn("## Queue boundary / 队列边界", text)
        self.assertIn("not a decipherment result", text)
        self.assertIn("破译结果", text)
        self.assertIn("Do not replace a missing item", text)

    def test_guide_covers_all_eight_object_local_candidates(self):
        text = GUIDE.read_text(encoding="utf-8")
        for number in range(1, 9):
            candidate_id = f"obs-insc-src-cand-{number:06d}"
            self.assertIn(candidate_id, text)
            self.assertIn(f"[cand-{number:06d}]", text)
        candidate_dirs = [
            "001_obs-insc-src-cand-000001_obimd-h2_source-record-candidate",
            "002_obs-insc-src-cand-000002_ihp-item-503_source-record-candidate",
            "003_obs-insc-src-cand-000003_ihp-item-1215_source-record-candidate",
            "004_obs-insc-src-cand-000004_ihp-item-771_source-record-candidate",
            "005_obs-insc-src-cand-000005_bl-or-1595_source-record-candidate",
            "006_obs-insc-src-cand-000006_bl-or-1535_source-record-candidate",
            "007_obs-insc-src-cand-000007_ningxia-hyz421_source-record-candidate",
            "008_obs-insc-src-cand-000008_met-42045_source-record-candidate",
        ]
        for candidate_dir in candidate_dirs:
            self.assertTrue(
                (
                    ROOT
                    / "corpus/002_oracle-bone-inscriptions/008_source-record-candidates"
                    / candidate_dir
                    / "README.md"
                ).is_file()
            )

    def test_inscription_readme_links_the_guide(self):
        text = README.read_text(encoding="utf-8")
        self.assertIn("005_opened-source-record-candidate-guide.md", text)

    def test_markdown_lines_are_at_most_eighty_columns(self):
        for path in (GUIDE, README):
            for line_number, line in enumerate(
                path.read_text(encoding="utf-8").splitlines(), 1
            ):
                self.assertLessEqual(
                    len(line),
                    80,
                    f"{path}:{line_number}: {len(line)} characters",
                )


if __name__ == "__main__":
    unittest.main()
