import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STRATEGY = (
    ROOT
    / "doc/project/005_ai-agent-research-assistant-design/README.md"
)


class NetworkSearchStrategyTests(unittest.TestCase):
    def test_network_layer_is_evidence_routing_not_popularity(self):
        text = STRATEGY.read_text(encoding="utf-8")
        for marker in (
            "Network Search And Evidence Routing / 网络搜索与证据路由",
            "Layered search order / 分层搜索顺序",
            "Search receipts / 搜索回执",
            "Graph rules / 图谱规则",
            "Network analyses / 网络分析",
            "Handoff and stopping / 交接与停止",
            "information-gain heuristic",
            "Support is counted by independent source family",
            "Unknown ancestry is treated as dependent or unresolved",
            "high-degree source hub",
            "does not receive extra evidential",
            "HTTP errors and authentication walls are access boundaries",
            "Endless inventory growth is not network progress",
        ):
            self.assertIn(marker, text)

        self.assertIn("impact * falsification_power", text)
        self.assertIn("independence_gain", text)
        self.assertIn("access_likelihood / cost", text)
        self.assertIn("network popularity score", text)

    def test_network_strategy_is_bilingual_and_within_line_limit(self):
        text = STRATEGY.read_text(encoding="utf-8")
        violations = [
            (number, len(line))
            for number, line in enumerate(text.splitlines(), 1)
            if len(line) > 80
        ]
        self.assertEqual(violations, [])
        self.assertIn("网络是证据路由工具", text)
        self.assertIn("每次查询都是可复跑的来源事件", text)
        self.assertIn("支持按独立来源家族计数", text)
        self.assertIn("无止境增加清单不算网络进展", text)


if __name__ == "__main__":
    unittest.main()
