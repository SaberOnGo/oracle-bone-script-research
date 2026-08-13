import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOSSIER = ROOT / (
    "corpus/001_oracle-characters/"
    "010_000901-001000_obs-char-bucket_oracle-characters/"
    "963_obs-char-000963_hust-obc-cat-1083_oracle-character/"
    "17_multi-instance-visual-comparison.md"
)


class ObsChar000963MultiInstanceReviewTests(unittest.TestCase):
    def test_review_records_five_opened_archive_members(self):
        self.assertTrue(DOSSIER.is_file(), DOSSIER)
        text = DOSSIER.read_text(encoding="utf-8-sig")
        members = re.findall(
            r"^- Archive member / 原包成员：`([^`]+)`$", text, re.M
        )
        self.assertEqual(5, len(members))
        self.assertEqual(5, len(set(members)))
        self.assertTrue(all("/1083/G_1083_" in item for item in members))
        self.assertEqual(5, len(re.findall(r"^- SHA-256：`[0-9a-f]{64}`$", text, re.M)))
        self.assertEqual(5, len(re.findall(r"^- Pixel size / 像素：`\d+ × \d+`$", text, re.M)))

    def test_review_is_object_specific_and_falsifiable(self):
        text = DOSSIER.read_text(encoding="utf-8-sig")
        for marker in (
            "obs-char-000963",
            "hust-obc-cat-1083",
            "合20217",
            "合7896",
            "合7897",
            "合13543𠂤組",
            "合30173歷無名間",
            "## Pairwise Differences And Counterevidence",
            "近形风险",
            "source_marked_risk_noted",
            "does not confirm inscription identity",
            "not an accepted reading",
        ):
            self.assertIn(marker, text)
        self.assertNotIn("not_collected", text)
        self.assertNotIn("TODO", text)

    def test_human_markdown_lines_do_not_exceed_eighty_characters(self):
        for line_number, line in enumerate(
            DOSSIER.read_text(encoding="utf-8-sig").splitlines(), 1
        ):
            self.assertLessEqual(
                len(line),
                80,
                f"{DOSSIER}:{line_number}: {len(line)} characters",
            )


if __name__ == "__main__":
    unittest.main()
