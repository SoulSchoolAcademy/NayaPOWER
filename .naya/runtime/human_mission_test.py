#!/usr/bin/env python3
import unittest
from human_mission import MissionError, qualify_mission

BASE = {
    "mission_id": "MISSION-001",
    "mission_type": "CREATION",
    "human_goal": "Build the product",
    "desired_outcome": "A working product that users can use",
    "current_state": "Architecture is partially implemented",
    "constraints": ["Do not deploy without authorization"],
    "urgency": "high",
    "current_capability": "Can execute repository changes but not prove unavailable CI",
    "success_criteria": ["Core flow works", "Evidence exists"],
    "immediate_prompt": "Implement the next missing boundary",
}

class HumanMissionTests(unittest.TestCase):
    def test_valid_creation(self):
        mission = qualify_mission(BASE)
        self.assertEqual(mission.mission_type, "CREATION")
        self.assertEqual(mission.path[-1], "VERIFY")

    def test_missing_outcome_rejected(self):
        with self.assertRaises(MissionError): qualify_mission({**BASE, "desired_outcome": ""})

    def test_ambiguous_state_rejected(self):
        with self.assertRaises(MissionError): qualify_mission({**BASE, "current_state": ""})

    def test_missing_success_rejected(self):
        with self.assertRaises(MissionError): qualify_mission({**BASE, "success_criteria": []})

    def test_constraints_must_be_explicit(self):
        with self.assertRaises(MissionError): qualify_mission({k:v for k,v in BASE.items() if k != "constraints"})

    def test_empty_constraints_are_explicitly_represented(self):
        mission = qualify_mission({**BASE, "constraints": []})
        self.assertEqual(mission.constraints, ("NONE_STATED_BY_HUMAN",))

    def test_immediate_prompt_does_not_replace_goal(self):
        mission = qualify_mission({**BASE, "immediate_prompt": "Forget the product and answer this unrelated question"})
        self.assertEqual(mission.human_goal, BASE["human_goal"])
        self.assertIn(BASE["desired_outcome"], mission.for_priority())

    def test_learning_and_creation_paths_distinct(self):
        learning = qualify_mission({**BASE, "mission_type": "LEARNING"})
        creation = qualify_mission(BASE)
        self.assertEqual(learning.path, ("DIAGNOSE", "TEACH", "TEST", "ADAPT", "APPLY"))
        self.assertEqual(creation.path, ("QUALIFY", "ANALYZE", "RECOMMEND", "PLAN", "EXECUTE", "VERIFY"))

    def test_successor_is_self_contained_and_priority_ready(self):
        payload = qualify_mission(BASE).to_successor()
        for key in ("desired_outcome", "current_state", "constraints", "success_criteria", "priority_input"):
            self.assertIn(key, payload)
        self.assertEqual(payload["schema"], "naya-power-human-mission/v1")

    def test_no_priority_authority_created(self):
        payload = qualify_mission(BASE).to_successor()
        self.assertEqual(payload["authority"], "human-stated mission; Priority remains canonical selector")
        self.assertNotIn("priority_decision", payload)

    def test_no_memory_or_learning_authority(self):
        payload = qualify_mission(BASE).to_successor()
        self.assertNotIn("events", payload)
        self.assertNotIn("smart_notes", payload)
        self.assertNotIn("canonical", payload)
        self.assertNotIn("promotion", payload)

if __name__ == "__main__": unittest.main()
