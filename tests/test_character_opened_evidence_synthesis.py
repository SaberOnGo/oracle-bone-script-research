import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


OBJECTS = {
    "obs-char-000209": (
        "corpus/001_oracle-characters/"
        "003_000201-000300_obs-char-bucket_oracle-characters/"
        "209_obs-char-000209_hust-obc-cat-0232_oracle-character"
    ),
    "obs-char-000412": (
        "corpus/001_oracle-characters/"
        "005_000401-000500_obs-char-bucket_oracle-characters/"
        "412_obs-char-000412_hust-obc-cat-0468_oracle-character"
    ),
    "obs-char-000621": (
        "corpus/001_oracle-characters/"
        "007_000601-000700_obs-char-bucket_oracle-characters/"
        "621_obs-char-000621_hust-obc-cat-0706_oracle-character"
    ),
    "obs-char-000791": (
        "corpus/001_oracle-characters/"
        "008_000701-000800_obs-char-bucket_oracle-characters/"
        "791_obs-char-000791_hust-obc-cat-0895_oracle-character"
    ),
    "obs-char-000852": (
        "corpus/001_oracle-characters/"
        "009_000801-000900_obs-char-bucket_oracle-characters/"
        "852_obs-char-000852_hust-obc-cat-0961_oracle-character"
    ),
    "obs-char-000963": (
        "corpus/001_oracle-characters/"
        "010_000901-001000_obs-char-bucket_oracle-characters/"
        "963_obs-char-000963_hust-obc-cat-1083_oracle-character"
    ),
}


class CharacterOpenedEvidenceSynthesisTests(unittest.TestCase):
    def test_each_selected_dossier_has_opened_synthesis(self):
        for object_id, relative_dir in OBJECTS.items():
            with self.subTest(object_id=object_id):
                path = ROOT / relative_dir / "05_human-research-dossier.md"
                self.assertTrue(path.is_file(), path)
                text = path.read_text(encoding="utf-8-sig")
                self.assertIn(object_id, text)
                self.assertIn(
                    "## 12. Opened Evidence Synthesis / 已打开证据综合",
                    text,
                )
                self.assertIn("14_material-visual-observation.md", text)
                self.assertIn("15_source-filename-evidence-review.md", text)
                self.assertIn("source-record", text)
                self.assertIn("反证", text)
                self.assertIn("decipherment conclusion", text)
                self.assertIn("metadata_only_until_verified", text)
                self.assertNotIn("not_collected", text)
                self.assertNotIn("TODO", text)

    def test_synthesis_markdown_lines_are_at_most_eighty_characters(self):
        for object_id, relative_dir in OBJECTS.items():
            with self.subTest(object_id=object_id):
                path = ROOT / relative_dir / "05_human-research-dossier.md"
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
