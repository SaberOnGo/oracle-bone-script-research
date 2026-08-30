import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STRATEGY = (
    ROOT
    / "doc/project/005_ai-agent-research-assistant-design/README.md"
)
SCHEMA = (
    ROOT
    / "schemas/007_ai-agent-benchmark-experiment-schema/"
    / "ai-agent-benchmark-experiment-v2.schema.json"
)
SCHEMAS_README = ROOT / "schemas/README.md"
SKILL = ROOT / "skills/ai-agent-evidence-pack-review/SKILL.md"


class AdjudicatorContractStrategyTests(unittest.TestCase):
    def test_strategy_declares_independent_adjudicator_contract(self) -> None:
        text = STRATEGY.read_text(encoding="utf-8")
        for marker in (
            "Independent Adjudicator Contract / 独立裁决 Agent 合同",
            "fresh context",
            "全新上下文",
            "prior_run_output_access=none",
            "opaque court IDs",
            "不透明的法庭 ID",
            "Required decision memo / 必需裁决说明",
            "candidate delivery",
            "候选交付",
            "Human-specialist approval is not a prerequisite",
            "真人专家批准设为前置条件",
        ):
            self.assertIn(marker, text)

    def test_strategy_and_schema_bind_runtime_audit_fields(self) -> None:
        strategy = STRATEGY.read_text(encoding="utf-8")
        schema = SCHEMA.read_text(encoding="utf-8")
        schemas_readme = SCHEMAS_README.read_text(encoding="utf-8")
        skill = SKILL.read_text(encoding="utf-8")
        for field in (
            "adjudicator_id",
            "execution_id",
            "model_id",
            "model_family",
            "context_id",
            "input_run_ids",
            "evidence_snapshot_sha256",
            "tool_manifest_sha256",
            "gold_access",
            "prior_run_output_access",
            "output_lock_sha256",
        ):
            self.assertIn(f"`{field}`", strategy)
            self.assertIn(f'"{field}"', schema)
        self.assertIn('"adjudicator_runtimes"', schema)
        self.assertIn("`adjudicator_runtimes`", schemas_readme)
        self.assertIn("independent `adjudicator_runtimes` record", skill)
        self.assertIn("[v2 benchmark contract]", skill)

    def test_strategy_and_schema_docs_stay_within_human_line_limit(self) -> None:
        for path in (
            STRATEGY,
            ROOT
            / "schemas/007_ai-agent-benchmark-experiment-schema/README.md",
            SCHEMAS_README,
            SKILL,
        ):
            violations = [
                (number, len(line))
                for number, line in enumerate(
                    path.read_text(encoding="utf-8").splitlines(), 1
                )
                if len(line) > 80
            ]
            self.assertEqual([], violations, str(path))


if __name__ == "__main__":
    unittest.main()
