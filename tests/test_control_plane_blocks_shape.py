import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BLOCKS = ROOT / ".naya" / "control-plane" / "BLOCKS.json"
STATE = ROOT / ".naya" / "control-plane" / "STATE.json"


class BlocksControlPlaneShapeTests(unittest.TestCase):
    def test_top_level_next_action_is_the_canonical_string(self):
        blocks = json.loads(BLOCKS.read_text(encoding="utf-8"))
        state = json.loads(STATE.read_text(encoding="utf-8"))

        next_action = blocks.get("next_action")
        expected = state["current_next_action"]["action"]

        self.assertIsInstance(next_action, str)
        self.assertEqual(next_action, expected)

    def test_top_level_next_action_does_not_contain_serialized_character_keys(self):
        blocks = json.loads(BLOCKS.read_text(encoding="utf-8"))

        next_action = blocks.get("next_action")
        self.assertNotIsInstance(next_action, dict)
        if isinstance(next_action, dict):
            self.assertNotIn("0", next_action)
            self.assertNotIn("1", next_action)
            self.assertNotIn("count", next_action)

    def test_scoped_active_block_frontier_is_kept_separate(self):
        blocks = json.loads(BLOCKS.read_text(encoding="utf-8"))

        self.assertIsInstance(blocks["active_block"]["next_action"], str)
        self.assertEqual(
            blocks["active_block"]["next_action"],
            blocks["active_block"]["current_frontier"]["next_action"],
        )


if __name__ == "__main__":
    unittest.main()
