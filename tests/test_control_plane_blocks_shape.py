import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BLOCKS = ROOT / ".naya" / "control-plane" / "BLOCKS.json"


class BlocksControlPlaneShapeTests(unittest.TestCase):
    def test_top_level_next_action_is_a_typed_object(self):
        data = json.loads(BLOCKS.read_text(encoding="utf-8"))
        next_action = data.get("next_action")

        self.assertIsInstance(next_action, dict)
        self.assertEqual(set(next_action.keys()), {"action", "reason"})
        self.assertIsInstance(next_action["action"], str)
        self.assertIsInstance(next_action["reason"], str)
        self.assertNotIn("0", next_action)
        self.assertNotIn("1", next_action)

    def test_top_level_next_action_matches_current_frontier(self):
        data = json.loads(BLOCKS.read_text(encoding="utf-8"))
        next_action = data["next_action"]

        self.assertEqual(next_action["action"], data["active_block"]["current_frontier"]["next_action"])
        self.assertEqual(next_action["action"], data["current_frontier"]["next_action"])


if __name__ == "__main__":
    unittest.main()
