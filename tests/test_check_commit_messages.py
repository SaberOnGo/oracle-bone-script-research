from pathlib import Path
from contextlib import redirect_stdout
from io import StringIO
import tempfile
import unittest

from tools.git.check_commit_messages import validate_commit_message, validate_message_file


class CommitMessageValidationTests(unittest.TestCase):
    def test_valid_multilingual_message_passes(self) -> None:
        message = """Initialize research skeleton

ZH:
- 建立甲骨文开放研究项目骨架，包含 AGENTS、双语 README、来源追溯规则、基础 skills 和校验脚本。

EN:
- Add the oracle bone script research skeleton with AGENTS, bilingual README files, provenance rules, basic skills, and validation scripts.

JA:
- 甲骨文字研究プロジェクトの骨格、AGENTS、二言語 README、出典追跡規則、基本 skills、検証スクリプトを追加します。
"""
        self.assertEqual(validate_commit_message(message), [])

    def test_inline_language_label_fails(self) -> None:
        message = """Bad commit

ZH: inline text is not allowed
EN:
- This English section is long enough to pass length validation in this test case.
JA:
- この日本語セクションは長さ検証を通過するために十分な内容を持っています。
"""
        issues = validate_commit_message(message)
        self.assertIn("ZH label must be on its own line", issues)

    def test_message_file_validation(self) -> None:
        message = """Missing sections

ZH:
- 只有中文段落是不够的，因为推送规则还要求英文和日文摘要。
"""
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "message.txt"
            path.write_text(message, encoding="utf-8")
            with redirect_stdout(StringIO()):
                self.assertEqual(validate_message_file(path), 1)


if __name__ == "__main__":
    unittest.main()
