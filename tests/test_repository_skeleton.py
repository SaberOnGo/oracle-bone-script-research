"""Tests for the policy and content-gate validator.

The validator was rebuilt on 2026-11-02 for the architecture reset in
doc/project/007_architecture-reset-and-human-first-knowledge-base/. These
tests exercise the gate functions on small temporary fixtures instead of
pinning generated repository structure.
"""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools" / "validation" / "check_repository_skeleton.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("repo_validator", VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


V = load_validator()

GOOD_README = """# obs-char-999999 字形档案

状态：已释候选（数据集标签） | 例句：1 | 更新：2026-11-02

## 1 字形与观察

![字形](images/001_asset-999999_test_glyph.png)

观察：上部横画平直，下部两笔外展〔图 images/001_asset-999999_test_glyph.png〕。

## 4 卜辞例句

| 著录号 | 释文 | 来源 |
| --- | --- | --- |
| 合 1 | 貞：□ | src-test 行 2 |

## 10 来源与权利

- src-test：权利状态 `source_marked_risk_noted`。
"""


def make_dossier(base: Path, readme: str, record: dict, extra: dict | None = None) -> Path:
    directory = base / "001_obs-char-999999_test-0001_oracle-character"
    (directory / "images").mkdir(parents=True)
    (directory / "images" / "001_asset-999999_test_glyph.png").write_bytes(b"png")
    (directory / "README.md").write_text(readme, encoding="utf-8")
    (directory / "record.json").write_text(json.dumps(record, ensure_ascii=False), encoding="utf-8")
    for name, text in (extra or {}).items():
        (directory / name).write_text(text, encoding="utf-8")
    return directory


GOOD_RECORD = {
    "id": "obs-char-999999",
    "sources": [{"source_id": "src-test"}],
    "images": [{"path": "images/001_asset-999999_test_glyph.png"}],
}


class DossierGateTests(unittest.TestCase):
    def issues_for(self, readme=GOOD_README, record=GOOD_RECORD, extra=None):
        with tempfile.TemporaryDirectory() as tmp:
            directory = make_dossier(Path(tmp), readme, record, extra)
            return V.dossier_issues(directory / "README.md", "fixture")

    def test_well_formed_dossier_passes(self):
        self.assertEqual([], self.issues_for())

    def test_g2_rejects_parallel_human_markdown(self):
        issues = self.issues_for(extra={"05_human-research-dossier.md": "# x\n"})
        self.assertTrue(any(i.startswith("G2") for i in issues), issues)

    def test_g3_rejects_repeated_disclaimers(self):
        readme = GOOD_README + "\n本文件不是释读结论。\nThis is not a decipherment conclusion.\n"
        issues = self.issues_for(readme=readme)
        self.assertTrue(any(i.startswith("G3") for i in issues), issues)

    def test_g3_allows_one_status_disclaimer(self):
        readme = GOOD_README + "\n本档案不是释读结论。\n"
        self.assertEqual([], self.issues_for(readme=readme))

    def test_g5_rejects_fixed_placeholder_sentences(self):
        for snippet in ("待查：需核对卜辞编号", "status `not_collected`"):
            issues = self.issues_for(readme=GOOD_README + "\n- " + snippet + "\n")
            self.assertTrue(any(i.startswith("G5") for i in issues), (snippet, issues))

    def test_g6_rejects_paths_broken_across_lines(self):
        readme = GOOD_README + "\n- 路径：`corpus/001_oracle-characters/001_ob\n  s-char-bucket`\n"
        issues = self.issues_for(readme=readme)
        self.assertTrue(any(i.startswith("G6") for i in issues), issues)

    def test_g6_ignores_backticks_inside_code_fences(self):
        readme = GOOD_README + "\n```text\na ` b\n```\n"
        self.assertEqual([], self.issues_for(readme=readme))

    def test_g11_requires_record_sources_cited_in_readme(self):
        record = dict(GOOD_RECORD, sources=[{"source_id": "src-test"}, {"source_id": "src-missing"}])
        issues = self.issues_for(record=record)
        self.assertTrue(any("src-missing" in i for i in issues), issues)

    def test_g11_requires_listed_images_to_exist(self):
        record = dict(GOOD_RECORD, images=[{"path": "images/absent.png"}])
        issues = self.issues_for(record=record)
        self.assertTrue(any("absent.png" in i for i in issues), issues)

    def test_g11_requires_object_id_in_readme(self):
        record = dict(GOOD_RECORD, id="obs-char-000000")
        issues = self.issues_for(record=record)
        self.assertTrue(any("obs-char-000000" in i for i in issues), issues)


class GeneratedNameGateTests(unittest.TestCase):
    def test_pattern_matches_work_queue_names(self):
        for name in (
            "061_ai-agent-evidence-pack-scaffold-manifest.csv",
            "005_review-queue.csv",
            "031_wave-handoff-scaffold.json",
            "026_evidence-collection-route-pack.json",
            "203_handoff-route-summary.json",
        ):
            self.assertTrue(V.GENERATED_NAME_PATTERN.search(name), name)

    def test_pattern_allows_research_names(self):
        for name in ("README.md", "record.json", "inscriptions.jsonl", "001_all-sources-index.csv"):
            self.assertIsNone(V.GENERATED_NAME_PATTERN.search(name), name)

    def test_allowlist_entries_exist(self):
        for rel in V.GENERATED_NAME_ALLOWLIST:
            self.assertTrue((ROOT / rel).exists(), rel)


class ObjectDirectoryPatternTests(unittest.TestCase):
    def test_matches_bucketed_and_flat_object_directories(self):
        cases = {
            "corpus/001_oracle-characters/001_000001-000100_obs-char-bucket_oracle-characters/"
            "001_obs-char-000001_hust-obc-cat-0001_oracle-character/README.md":
            "001_obs-char-000001_hust-obc-cat-0001_oracle-character",
            "corpus/006_research-sources-and-bibliography/001_source-objects/"
            "015_src-hust-obc_source-object/README.md": "015_src-hust-obc_source-object",
        }
        for path, tail in cases.items():
            match = V.OBJECT_DIR_PATTERN.match(path)
            self.assertIsNotNone(match, path)
            self.assertTrue(match.group(1).endswith(tail), match.group(1))

    def test_ignores_register_files(self):
        path = "corpus/001_oracle-characters/000_character-registers/001_all-oracle-characters-index.csv"
        self.assertIsNone(V.OBJECT_DIR_PATTERN.match(path))


class SourceRegisterTests(unittest.TestCase):
    def test_current_registers_keep_rights_risk_and_review(self):
        self.assertEqual([], V.check_source_register_fields(ROOT))

    def test_missing_rights_status_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / V.SOURCE_INDEX
            path.parent.mkdir(parents=True)
            path.write_text(
                "source_id,rights_status,risk_note,review_status\n"
                "src-a,,note,reviewed\nsrc-a,ok,note,reviewed\n",
                encoding="utf-8",
            )
            issues = V.check_source_register_fields(root)
        self.assertTrue(any("missing rights_status" in i for i in issues), issues)
        self.assertTrue(any("duplicate source_id src-a" in i for i in issues), issues)


class RepositoryPolicyTests(unittest.TestCase):
    def test_required_paths_exist(self):
        self.assertEqual([], V.check_required_paths(ROOT))

    def test_bilingual_entry_documents(self):
        self.assertEqual([], V.check_bilingual_markers(ROOT))

    def test_gitignore_keeps_temporary_areas_ignored(self):
        self.assertEqual([], V.check_root_gitignore_patterns(ROOT))

    def test_obimd_rights_override_stays_effective(self):
        self.assertEqual([], V.check_obimd_rights_override(ROOT))

    def test_agents_points_to_architecture_reset(self):
        text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("007_architecture-reset-and-human-first-knowledge-base", text)
        self.assertIn("Do not run batch template generators", text)

    def test_reset_documents_are_bilingual_and_wrapped(self):
        directory = ROOT / "doc/project/007_architecture-reset-and-human-first-knowledge-base"
        for path in sorted(directory.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            self.assertRegex(text, r"[一-鿿]", path.name)
            self.assertRegex(text, r"[A-Za-z]{4,} [A-Za-z]{3,}", path.name)


if __name__ == "__main__":
    unittest.main()
