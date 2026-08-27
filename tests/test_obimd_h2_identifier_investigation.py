import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBJECT = (
    ROOT
    / "corpus"
    / "002_oracle-bone-inscriptions"
    / "008_source-record-candidates"
    / "001_obs-insc-src-cand-000001_obimd-h2_source-record-candidate"
)
INVESTIGATION = OBJECT / "07_identifier-crosswalk-investigation.md"


class ObimdH2IdentifierInvestigationTests(unittest.TestCase):
    def test_direct_evidence_is_separated_from_candidate_inference(self):
        text = INVESTIGATION.read_text(encoding="utf-8")
        for phrase in (
            "Direct source evidence",
            "Replayed visual comparison",
            "具体待查问题",
            "Catalog abbreviation of the",
            "rubbing image",
            "high-confidence Heji 2 cross-source candidate",
            "高置信跨来源候选",
        ):
            self.assertIn(phrase, text)

    def test_routes_hashes_and_access_observation_are_exact(self):
        text = INVESTIGATION.read_text(encoding="utf-8")
        for phrase in (
            "https://doi.org/10.1038/s41597-026-06967-0",
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC13128845/",
            "c8b1f31bb61c6d1cafb6e55ca377b1df4c9951b8",
            "https://jgw.aynu.edu.cn/AynuBone/BookList",
            "https://jgw.aynu.edu.cn/AynuBone/Search",
            "010001H",
            "108548",
            "Code=406",
            "5321d3b9adf0a1bde32e4092715741a04461908c9c6e911c57e1f7544ab32437",
        ):
            self.assertIn(phrase, text)
        self.assertIn("only a query observation", text)
        self.assertIn("不能证明映射不存在", text)
        self.assertNotIn("This proves", text)

    def test_visual_comparison_counts_and_replay_links_are_present(self):
        text = INVESTIGATION.read_text(encoding="utf-8")
        for phrase in (
            "10,077 package members",
            "10,076 alternative candidates",
            "dHash distance 0",
            "next distance was 12",
            "rubbing/h00002.jpg",
            "92_visual-crosswalk-replay-manifest.json",
            "tools/007_obimd-h2-crosswalk/README.md",
            "10,076 个替代候选",
        ):
            self.assertIn(phrase, text)
        self.assertNotIn("10,077 negative controls", text)

    def test_text_and_rights_boundaries_are_explicit(self):
        text = INVESTIGATION.read_text(encoding="utf-8")
        for phrase in (
            "source-reported partial transcription",
            "no project reading is proposed",
            "metadata_only_until_verified",
            "No thumbnail bytes were saved or committed",
            "不确认《合集》",
        ):
            self.assertIn(phrase, text)

    def test_investigation_is_bilingual_and_within_line_limit(self):
        text = INVESTIGATION.read_text(encoding="utf-8")
        self.assertIn("## English", text)
        self.assertIn("## 简体中文", text)
        violations = [
            f"{number}:{len(line)}"
            for number, line in enumerate(text.splitlines(), start=1)
            if len(line) > 80
        ]
        self.assertEqual(violations, [])


if __name__ == "__main__":
    unittest.main()
