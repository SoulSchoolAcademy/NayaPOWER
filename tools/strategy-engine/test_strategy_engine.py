"""Tests for strategy_engine.py. Run: python3 -m unittest test_strategy_engine -v
from ~/workspace/strategy-engine/
"""
import unittest
from datetime import datetime, timedelta, timezone

from strategy_engine import (
    QueueItem, aaa_check, can_claim, can_land, disposition_status,
    kill_decision, verification_lane_action, verdict_sla_ok,
    resource_budget_ok, front_door_route, weighted_value, scoreboard,
    thirty_second_test, STANDING_RED_TOTAL, TODAY_QUEUE, WIP_CAP_TEAM,
)


def _item(**kw):
    base = dict(key="test-item", priority=100, owner="Power",
                gate="test gate", scorer="Nitro", verifier_login="verifier-login",
                builder_login="builder-login", builder="Power")
    base.update(kw)
    return QueueItem(**base)


class TestAAA(unittest.TestCase):
    def test_all_three_required(self):
        ok, missing = aaa_check(True, True, True)
        self.assertTrue(ok)
        self.assertEqual(missing, [])
        ok, missing = aaa_check(True, False, True)
        self.assertFalse(ok)
        self.assertEqual(missing, ["AUTHENTICATED"])

    def test_two_of_three_is_not_finished(self):
        ok, _ = aaa_check(True, True, False)
        self.assertFalse(ok)


class TestClaimAndLand(unittest.TestCase):
    def test_claim_is_lock(self):
        item = _item()
        ok, _ = can_claim(item, "Power", team_wip=0)
        self.assertTrue(ok)
        ok, _ = can_claim(item, "Nitro", team_wip=1)
        self.assertFalse(ok)

    def test_wip_cap_blocks(self):
        item = _item()
        ok, _ = can_claim(item, "Power", team_wip=WIP_CAP_TEAM)
        self.assertFalse(ok)

    def test_blank_roster_blocks_start(self):
        item = _item(scorer="", verifier_login="")
        ok, _ = can_claim(item, "Power", team_wip=0)
        self.assertFalse(ok)

    def test_land_requires_threshold_and_separation(self):
        item = _item(score=9.5, scorer="Nitro", verifier_login="other-login")
        ok, _ = can_land(item, failures=[])
        self.assertTrue(ok)
        item2 = _item(score=8.5, scorer="Nitro", verifier_login="other-login")
        ok, _ = can_land(item2, failures=[])
        self.assertFalse(ok)
        item3 = _item(score=9.5, scorer="Power", verifier_login="other-login")
        ok, _ = can_land(item3, failures=[])
        self.assertFalse(ok)
        item4 = _item(score=9.5, scorer="Nitro", verifier_login="builder-login")
        ok, _ = can_land(item4, failures=[])
        self.assertFalse(ok)

    def test_new_red_blocks_landing(self):
        item = _item(score=9.5, scorer="Nitro", verifier_login="other-login")
        ok, _ = can_land(item, failures=["retrieval_page_hash_mismatch"])
        self.assertTrue(ok)
        ok, msg = can_land(item, failures=["brand_new_failure_family"])
        self.assertFalse(ok)
        self.assertIn("new red", msg)


class TestDispositionAndKill(unittest.TestCase):
    def test_disposition_clock(self):
        now = datetime(2026, 10, 24, 18, 0, tzinfo=timezone.utc)
        item = _item(score=9.5, verified_at=now - timedelta(hours=1))
        self.assertEqual(disposition_status(item, now), "WITHIN_SLA")
        item.verified_at = now - timedelta(hours=2, minutes=30)
        self.assertEqual(disposition_status(item, now), "ESCALATE_INTEGRATOR")
        item.verified_at = now - timedelta(hours=5)
        self.assertEqual(disposition_status(item, now), "WEAKEST_POINT")

    def test_kill_criteria(self):
        self.assertEqual(kill_decision(_item(failures_same_way=2)), "CHANGE_MECHANISM")
        self.assertEqual(kill_decision(_item(failures_same_way=0, failures_total=3)), "RETURN_TO_THINK")
        self.assertEqual(kill_decision(_item()), "CONTINUE_SAME_PASS")


class TestLanesBudgetsAndDoor(unittest.TestCase):
    def test_verify_lane_rotation(self):
        self.assertEqual(verification_lane_action(2, 5), "ROTATE_BUILDERS_TO_VERIFY")
        self.assertEqual(verification_lane_action(5, 2), "NORMAL_FLOW")

    def test_verdict_sla(self):
        self.assertTrue(verdict_sla_ok(5, 5))
        self.assertFalse(verdict_sla_ok(3, 5))

    def test_resource_budget(self):
        ok, _ = resource_budget_ok(700, 10)
        self.assertTrue(ok)
        ok, _ = resource_budget_ok(801, 10)
        self.assertFalse(ok)
        ok, _ = resource_budget_ok(100, 0)
        self.assertFalse(ok)

    def test_front_door_threshold(self):
        self.assertEqual(front_door_route(False), "CERTIFICATE_WELCOME")
        self.assertEqual(front_door_route(True), "HUB")

    def test_weighted_value(self):
        self.assertEqual(weighted_value(["journey", "system", "fix"]), 16)
        self.assertEqual(weighted_value([]), 0)

    def test_thirty_second_test(self):
        self.assertTrue(thirty_second_test(True, True, True))
        self.assertFalse(thirty_second_test(True, False, True))


class TestBaseline(unittest.TestCase):
    def test_standing_red_totals_22(self):
        self.assertEqual(STANDING_RED_TOTAL, 22)

    def test_today_queue_has_owners_and_gates(self):
        self.assertGreaterEqual(len(TODAY_QUEUE), 10)
        for item in TODAY_QUEUE:
            self.assertTrue(item.owner, item.key)
            self.assertTrue(item.gate, item.key)


if __name__ == "__main__":
    unittest.main()
