import unittest

from continuation_prompt import render_continuation_prompt
from naya_power_runtime import MissionState


class ContinuationPromptTests(unittest.TestCase):
    def test_prompt_contains_operational_state_and_no_now_what_behavior(self):
        state = MissionState(
            project="Naya Power",
            mission="Build the host executor bridge.",
            vision="Continuous responsible execution.",
            desired_outcome="Fresh Naya can continue without a human-authored next task.",
            protected_scope=["canonical laws"],
            known=["runtime kernel exists"],
            last_verified_state="Bridge skeleton exists; integration remains.",
            next_action="integrate-host-tools",
            next_action_reason="Highest-value remaining runtime gap.",
        )
        prompt = render_continuation_prompt(state)
        self.assertIn("Build the host executor bridge", prompt)
        self.assertIn("integrate-host-tools", prompt)
        self.assertIn("NO “NOW WHAT?”", prompt)
        self.assertIn("BEGIN NOW", prompt)
        self.assertIn("copy-paste-ready continuation prompt", prompt)


if __name__ == "__main__":
    unittest.main()
