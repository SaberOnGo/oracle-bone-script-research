import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


CASES = {
    "obs-char-000963": {
        "directory": (
            "corpus/001_oracle-characters/"
            "010_000901-001000_obs-char-bucket_oracle-characters/"
            "963_obs-char-000963_hust-obc-cat-1083_oracle-character"
        ),
        "count": 14,
        "specific": ["合20217", "合13543𠂤組", "合30173歷無名間"],
    },
    "obs-char-000621": {
        "directory": (
            "corpus/001_oracle-characters/"
            "007_000601-000700_obs-char-bucket_oracle-characters/"
            "621_obs-char-000621_hust-obc-cat-0706_oracle-character"
        ),
        "count": 20,
        "specific": ["合6583賓組", "合11439𠂤賓間", "合231賓組"],
    },
    "obs-char-000791": {
        "directory": (
            "corpus/001_oracle-characters/"
            "008_000701-000800_obs-char-bucket_oracle-characters/"
            "791_obs-char-000791_hust-obc-cat-0895_oracle-character"
        ),
        "count": 21,
        "specific": ["合26786出組", "合28087何組", "合34612歷組"],
    },
    "obs-char-000852": {
        "directory": (
            "corpus/001_oracle-characters/"
            "009_000801-000900_obs-char-bucket_oracle-characters/"
            "852_obs-char-000852_hust-obc-cat-0961_oracle-character"
        ),
        "count": 18,
        "specific": ["合31923無名組", "合8315賓組副本0", "合28183何組"],
    },
    "obs-char-000209": {
        "directory": (
            "corpus/001_oracle-characters/"
            "003_000201-000300_obs-char-bucket_oracle-characters/"
            "209_obs-char-000209_hust-obc-cat-0232_oracle-character"
        ),
        "count": 10,
        "specific": ["合4814賓組", "合21988子組", "合21021𠂤組"],
    },
    "obs-char-000412": {
        "directory": (
            "corpus/001_oracle-characters/"
            "005_000401-000500_obs-char-bucket_oracle-characters/"
            "412_obs-char-000412_hust-obc-cat-0468_oracle-character"
        ),
        "count": 10,
        "specific": ["合22049午組", "合693賓組", "合17382賓組"],
    },
}


class CharacterSourceFilenameEvidenceBatchTests(unittest.TestCase):
    def test_each_selected_object_has_complete_filename_evidence(self):
        for object_id, case in CASES.items():
            with self.subTest(object_id=object_id):
                path = ROOT / case["directory"] / (
                    "15_source-filename-evidence-review.md"
                )
                self.assertTrue(path.is_file(), path)
                text = path.read_text(encoding="utf-8-sig")
                rows = re.findall(r"^- `HUST-OBC/.+?/G_.+`$", text, re.M)
                self.assertEqual(case["count"], len(rows), path)
                for marker in case["specific"]:
                    self.assertIn(marker, text)

    def test_dossiers_are_object_specific_and_preserve_boundaries(self):
        texts = []
        for object_id, case in CASES.items():
            path = ROOT / case["directory"] / (
                "15_source-filename-evidence-review.md"
            )
            text = path.read_text(encoding="utf-8-sig")
            texts.append(text)
            self.assertIn(object_id, text)
            self.assertIn("文件名来源记录", text)
            self.assertIn("does not confirm inscription identity", text)
            self.assertIn("not an accepted reading", text)
            self.assertIn("## Direct Visual Observation", text)
            self.assertIn("## Cross-source Routes", text)
            self.assertIn("## Concrete Next Checks", text)
            self.assertNotIn("not_collected", text)
            self.assertNotIn("TODO", text)
        self.assertEqual(len(texts), len(set(texts)))

    def test_human_markdown_lines_do_not_exceed_eighty_characters(self):
        for object_id, case in CASES.items():
            with self.subTest(object_id=object_id):
                path = ROOT / case["directory"] / (
                    "15_source-filename-evidence-review.md"
                )
                for line_number, line in enumerate(
                    path.read_text(encoding="utf-8-sig").splitlines(), 1
                ):
                    self.assertLessEqual(
                        len(line),
                        80,
                        f"{path}:{line_number}: {len(line)} characters",
                    )


if __name__ == "__main__":
    unittest.main()
