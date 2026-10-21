#!/usr/bin/env python3
"""Acceptance tests for feature.scheduler (registry acceptance:
scheduled_post_publishes, cancel_works, missed_job_reported).

Stdlib only (unittest + subprocess). Activation tests run the real
assemble.py end-to-end against a wired copy of the smart-builder tree
(registry status for the breaker flipped to 'built' in the copy, so the
suite is green regardless of the real registry's flip state — the real
registry flips only after these pass).

Honest scope note: the builder module does not run the schedule — it
renders the schedule card and embeds the validated, machine-readable job
spec the runtime scheduler service consumes. Publishing, firing,
canceling, and missed-job reporting belong to that service; the spec is
the binding. What the module proves:

  scheduled_post_publishes -> a valid job spec is embedded (cadence, time,
                             timezone, topic, job_id) for the service to run
  cancel_works             -> a working cancel control exists ONLY when the
                             contract declares manage_endpoint (real POST);
                             no endpoint -> no cancel button, never a dead one
  missed_job_reported      -> the spec is the service's contract input
  activation gate          -> no scheduler markup unless declared
  sanitization             -> bad cadence/time/timezone/endpoint -> refusal
  registry binding         -> unbuilt breaker fails closed (exit 2)
  determinism              -> same contract -> same bytes (no build-time
                              timestamps anywhere)
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
SB_DIR = os.path.normpath(os.path.join(TESTS_DIR, "..", ".."))
INDEX = os.path.normpath(os.path.join(
    SB_DIR, "..", "..", "library", "catalog", "builder-index-v1.json"))
SMOKE = os.path.join(SB_DIR, "contracts", "smoke-test-v1.json")

SCHED_DECL = {
    "enabled": True,
    "cadence": "daily",
    "time": "08:00",
    "timezone": "America/New_York",
    "topic": "daily intelligence",
    "manage_endpoint": "https://sched.nayanet.live/morning-crumb",
}


# All four Wave-D/E breakers, flipped to built in the wired test copies so
# each suite tests its own module against the post-flip world (the real
# registry flips only after these pass).
WAVE_BREAKERS = ("feature.naya_answers", "feature.scheduler",
                 "feature.broadcast", "feature.smart_list")


def wired_tree(tmp):
    tree = os.path.join(tmp, "sb-wired")
    shutil.copytree(SB_DIR, tree)
    regp = os.path.join(tree, "functions", "registry.json")
    reg = json.load(open(regp))
    for g in reg["groups"].values():
        for f in g.get("functions", []):
            if f.get("id") in WAVE_BREAKERS:
                f["status"] = "built"
    json.dump(reg, open(regp, "w"), indent=1)
    return tree


def unbuilt_tree(tmp, target):
    """Wired copy with exactly one breaker back at specified — the
    fail-closed surface: only the target may refuse."""
    tree = os.path.join(tmp, "sb-unbuilt")
    shutil.copytree(SB_DIR, tree)
    regp = os.path.join(tree, "functions", "registry.json")
    reg = json.load(open(regp))
    for g in reg["groups"].values():
        for f in g.get("functions", []):
            if f.get("id") in WAVE_BREAKERS:
                f["status"] = "built"
            if f.get("id") == target:
                f["status"] = "specified"
    json.dump(reg, open(regp, "w"), indent=1)
    return tree


def sched_contract(tmp, decl, connections=None):
    c = json.load(open(SMOKE))
    c["title"] = "Scheduler acceptance contract"
    c["features"] = {"scheduler": decl}
    c["connections"] = {"nayanet": True} if connections is None else connections
    p = os.path.join(tmp, "contract.json")
    json.dump(c, open(p, "w"))
    return p


def run_assemble(contract, workdir, sbdir):
    out = os.path.join(workdir, "page.html")
    man = os.path.join(workdir, "page.manifest.json")
    assemble = os.path.join(sbdir, "assemble.py")
    r = subprocess.run(
        [sys.executable, assemble, "--contract", contract, "--index", INDEX,
         "--template", os.path.join(sbdir, "templates", "page.html"),
         "--out", out, "--manifest", man],
        capture_output=True, text=True, timeout=120)
    page = open(out, encoding="utf-8").read() if os.path.exists(out) else ""
    manifest = {}
    if os.path.exists(man):
        with open(man) as fh:
            manifest = json.load(fh)
    return r, page, manifest


def card_html(page):
    m = re.search(r'<section class="sched-card.*?</section>', page, re.S)
    return m.group(0) if m else ""


def job_spec(page):
    m = re.search(
        r'<script type="application/json" data-scheduler-spec>(.*?)</script>',
        page, re.S)
    return json.loads(m.group(1)) if m else None


class FeatureSchedulerAcceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="fsch-")
        cls.tree = wired_tree(cls.tmp)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def run(self, result=None):
        self.workdir = tempfile.mkdtemp(prefix="fsch-w-", dir=self.tmp)
        super().run(result)

    # ---- scheduled_post_publishes: a valid job spec is embedded ----
    def test_activation_via_contract(self):
        r, page, manifest = run_assemble(
            sched_contract(self.tmp, dict(SCHED_DECL)), self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="scheduler"', page)
        self.assertIn('data-scheduler-status="built"', page)
        card = card_html(page)
        self.assertTrue(card, "scheduler card must render")
        # the rule, not a timestamp: determinism-safe
        self.assertIn("Every day · 08:00 America/New_York", card)
        self.assertIn("daily intelligence", card)
        spec = job_spec(page)
        self.assertIsNotNone(spec, "machine-readable job spec must embed")
        self.assertEqual(spec["cadence"], "daily")
        self.assertEqual(spec["time"], "08:00")
        self.assertEqual(spec["timezone"], "America/New_York")
        self.assertEqual(spec["topic"], "daily intelligence")
        self.assertEqual(spec["feature"], "feature.scheduler")
        self.assertEqual(spec["version"], "1.0.0")
        self.assertEqual(spec["manage_endpoint"],
                         "https://sched.nayanet.live/morning-crumb")
        self.assertRegex(spec["job_id"], r"^[0-9a-f]{16}$")
        machine = json.loads(re.search(
            r'<pre id="machinejson">(.*?)</pre>', page, re.S).group(1))
        self.assertEqual(machine["features_status"]["scheduler"], "built")
        events = manifest.get("receipt", {}).get("events", [])
        self.assertTrue(any(e.get("event") == "scheduler.job.created"
                            and e.get("feature") == "feature.scheduler"
                            for e in events))

    # ---- cancel_works: a real control only when the service is declared ----
    def test_cancel_control_wired(self):
        r, page, _ = run_assemble(
            sched_contract(self.tmp, dict(SCHED_DECL)), self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        card = card_html(page)
        self.assertIn('action="https://sched.nayanet.live/morning-crumb/cancel"',
                      card)
        self.assertIn('name="job_id"', card)
        self.assertIn("Cancel schedule", card)

    def test_no_cancel_without_endpoint(self):
        decl = dict(SCHED_DECL)
        del decl["manage_endpoint"]
        r, page, _ = run_assemble(
            sched_contract(self.tmp, decl), self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        card = card_html(page)
        self.assertTrue(card)
        self.assertNotIn("sched-cancel", card)  # no dead cancel button
        spec = job_spec(page)
        self.assertNotIn("manage_endpoint", spec)

    # ---- gate: no scheduler markup unless the contract declares it ----
    def test_refusal_when_not_declared(self):
        r, page, _ = run_assemble(SMOKE, self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="scheduler"', page)
        self.assertNotIn('<section class="sched-card', page)

    def test_refusal_when_declared_but_disabled(self):
        decl = dict(SCHED_DECL, enabled=False)
        r, page, _ = run_assemble(
            sched_contract(self.tmp, decl), self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="scheduler"', page)

    # ---- three-state: explicit false = off (no render, no claim) ----
    def test_explicit_false_is_off(self):
        r, page, manifest = run_assemble(
            sched_contract(self.tmp, False), self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="scheduler"', page)
        events = manifest.get("receipt", {}).get("events", [])
        self.assertFalse(any(e.get("feature") == "feature.scheduler"
                             for e in events))

    # ---- three-state: omitted = assembler policy (not standard -> off) ----
    def test_omitted_stays_off(self):
        c = json.load(open(SMOKE))
        c["title"] = "Omitted breaker contract"
        c["features"] = {}  # scheduler omitted; not standard -> off
        c["connections"] = {"nayanet": True}
        p = os.path.join(self.workdir, "contract.json")
        json.dump(c, open(p, "w"))
        r, page, _ = run_assemble(p, self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn('data-feature="scheduler"', page)

    # ---- connections: no NayaNET -> queue locally and SAY SO ----
    def test_no_nayanet_queues_locally(self):
        r, page, manifest = run_assemble(
            sched_contract(self.tmp, dict(SCHED_DECL), connections={}),
            self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="scheduler"', page)
        card = card_html(page)
        self.assertIn('data-delivery="queued_locally"', card)
        self.assertIn("queue locally until you connect", card)
        self.assertIn("Nothing is sent yet", card)
        spec = job_spec(page)
        self.assertEqual(spec["delivery"], "queued_locally")
        # the job is still created — the schedule is real
        events = manifest.get("receipt", {}).get("events", [])
        self.assertTrue(any(e.get("event") == "scheduler.job.created"
                            for e in events))

    def test_connected_delivery(self):
        r, page, _ = run_assemble(
            sched_contract(self.tmp, dict(SCHED_DECL)), self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-delivery="nayanet"', card_html(page))
        self.assertEqual(job_spec(page)["delivery"], "nayanet")

    # ---- grant: explicit "delivery": "nayanet" without the grant refuses ----
    def test_grant_required_names_grant(self):
        decl = dict(SCHED_DECL, delivery="nayanet")
        del decl["manage_endpoint"]
        r, page, _ = run_assemble(
            sched_contract(self.tmp, decl, connections={}),
            self.workdir, self.tree)
        self.assertEqual(r.returncode, 2)
        body = json.loads(r.stdout)
        self.assertEqual(body["status"], "refused")
        errs = [e for e in body["errors"]
                if e.get("feature") == "feature.scheduler"]
        self.assertTrue(errs, body["errors"])
        self.assertEqual(errs[0]["code"], "grant_required")
        self.assertIn("connections.nayanet", errs[0]["detail"])
        self.assertNotIn('data-feature="scheduler"', page)

    # ---- readiness mirrored in the receipt ----
    def test_readiness_in_receipt(self):
        r, page, manifest = run_assemble(
            sched_contract(self.tmp, dict(SCHED_DECL)), self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        ready = manifest.get("receipt", {}).get("readiness", [])
        rec = [x for x in ready if x.get("feature") == "feature.scheduler"]
        self.assertTrue(rec, ready)
        self.assertEqual(rec[0]["mode"], "connected")
        self.assertEqual(rec[0]["grant"], "connections.nayanet")
        self.assertTrue(rec[0]["granted"])

    def test_readiness_ready_mode_in_receipt(self):
        r, page, manifest = run_assemble(
            sched_contract(self.tmp, dict(SCHED_DECL), connections={}),
            self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        ready = manifest.get("receipt", {}).get("readiness", [])
        rec = [x for x in ready if x.get("feature") == "feature.scheduler"]
        self.assertTrue(rec, ready)
        self.assertEqual(rec[0]["mode"], "ready")
        self.assertFalse(rec[0]["granted"])

    # ---- day-one: minimal contract -> useful render, zero errors ----
    def test_day_one(self):
        c = json.load(open(SMOKE))
        c["title"] = "Day one"
        c["features"] = {"scheduler": {"enabled": True, "cadence": "daily",
                                       "time": "08:00", "timezone": "UTC"}}
        p = os.path.join(self.workdir, "contract.json")
        json.dump(c, open(p, "w"))
        r, page, _ = run_assemble(p, self.workdir, self.tree)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('data-feature="scheduler"', page)
        self.assertIn("Every day · 08:00 UTC", page)

    # ---- sanitization: bad schedules fail closed, never improvised ----
    def test_bad_schedule_refusals(self):
        bad_decls = [
            dict(SCHED_DECL, cadence="fortnightly"),
            dict(SCHED_DECL, cadence=""),
            dict(SCHED_DECL, time="25:00"),
            dict(SCHED_DECL, time="8am"),
            dict(SCHED_DECL, time="08-00"),
            dict(SCHED_DECL, time=""),
            dict(SCHED_DECL, timezone="Mars/Olympus"),
            dict(SCHED_DECL, timezone=""),
            dict(SCHED_DECL, cadence="weekly", weekday=7),
            dict(SCHED_DECL, cadence="monthly", monthday=31),
            dict(SCHED_DECL, manage_endpoint="javascript:alert(1)"),
        ]
        for decl in bad_decls:
            r, page, _ = run_assemble(
                sched_contract(self.tmp, decl), self.workdir, self.tree)
            self.assertEqual(r.returncode, 2, "accepted: %r" % (decl,))
            body = json.loads(r.stdout)
            self.assertEqual(body["status"], "refused")
            codes = [e["code"] for e in body["errors"]]
            self.assertTrue("bad_scheduler_declaration" in codes
                            or "unsafe_scheduler_endpoint" in codes, decl)
            self.assertNotIn('data-feature="scheduler"', page)

    def test_malformed_declaration_refused(self):
        r, page, _ = run_assemble(
            sched_contract(self.tmp, "every day at eight"), self.workdir, self.tree)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("bad_scheduler_declaration", codes)

    # ---- registry binding: the contract cannot out-claim the registry ----
    def test_unbuilt_breaker_refused(self):
        tree = unbuilt_tree(self.tmp, "feature.scheduler")
        r, page, _ = run_assemble(
            sched_contract(self.tmp, dict(SCHED_DECL)), self.workdir, tree)
        self.assertEqual(r.returncode, 2)
        codes = [e["code"] for e in json.loads(r.stdout)["errors"]]
        self.assertIn("feature_not_built", codes)
        self.assertNotIn('data-feature="scheduler"', page)

    # ---- determinism: same contract -> same bytes (no timestamps) ----
    def test_determinism(self):
        contract = sched_contract(self.tmp, dict(SCHED_DECL))
        _, page1, _ = run_assemble(contract, self.workdir, self.tree)
        d2 = tempfile.mkdtemp(prefix="fsch-b-", dir=self.tmp)
        _, page2, _ = run_assemble(contract, d2, self.tree)
        self.assertEqual(hashlib.sha256(page1.encode()).hexdigest(),
                         hashlib.sha256(page2.encode()).hexdigest())


class FeatureSchedulerUnits(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, os.path.join(SB_DIR, "functions"))
        from feature_scheduler import (  # noqa
            next_run, validated_spec, rule_line, SchedulerRefusal,
            delivery_for, mode_for, GRANT)
        cls.next_run = staticmethod(next_run)
        cls.validated_spec = staticmethod(validated_spec)
        cls.rule_line = staticmethod(rule_line)
        cls.SchedulerRefusal = SchedulerRefusal
        cls.delivery_for = staticmethod(delivery_for)
        cls.mode_for = staticmethod(mode_for)
        cls.GRANT = GRANT

    @classmethod
    def tearDownClass(cls):
        sys.path.pop(0)

    def spec(self, **kw):
        d = dict(SCHED_DECL)
        d.update(kw)
        return self.validated_spec(d)

    def test_next_run_daily(self):
        from zoneinfo import ZoneInfo
        s = self.spec()
        # before 08:00 ET -> today 08:00
        now = datetime(2026, 10, 17, 11, 0, tzinfo=timezone.utc)  # 07:00 ET
        nr = self.next_run(s, now)
        self.assertEqual((nr.day, nr.hour, nr.minute), (17, 8, 0))
        # after 08:00 ET -> tomorrow
        now = datetime(2026, 10, 17, 13, 0, tzinfo=timezone.utc)  # 09:00 ET
        nr = self.next_run(s, now)
        self.assertEqual((nr.day, nr.hour), (18, 8))

    def test_next_run_hourly(self):
        s = self.spec(cadence="hourly")
        # 12:30 UTC = 08:30 America/New_York -> next top of the hour 09:00 ET
        now = datetime(2026, 10, 17, 12, 30, tzinfo=timezone.utc)
        nr = self.next_run(s, now)
        self.assertEqual((nr.hour, nr.minute), (9, 0))

    def test_next_run_weekly(self):
        s = self.spec(cadence="weekly", weekday=0)  # Monday
        # Saturday 2026-10-17 -> next Monday 2026-10-19
        now = datetime(2026, 10, 17, 12, 0, tzinfo=timezone.utc)
        nr = self.next_run(s, now)
        self.assertEqual((nr.day, nr.weekday()), (19, 0))

    def test_next_run_monthly(self):
        s = self.spec(cadence="monthly", monthday=1)
        now = datetime(2026, 10, 17, 12, 0, tzinfo=timezone.utc)
        nr = self.next_run(s, now)
        self.assertEqual((nr.month, nr.day), (11, 1))

    def test_rule_lines(self):
        self.assertEqual(self.rule_line(self.spec()),
                         "Every day · 08:00 America/New_York")
        self.assertEqual(self.rule_line(self.spec(cadence="hourly")),
                         "Every hour")

    def test_job_id_deterministic(self):
        self.assertEqual(self.spec()["job_id"], self.spec()["job_id"])

    def test_hourly_ignores_time(self):
        s = self.spec(cadence="hourly", time="99:99")
        self.assertEqual(s["time"], "00:00")

    def test_bad_cadence_unit(self):
        with self.assertRaises(self.SchedulerRefusal):
            self.validated_spec({"cadence": "yearly"})

    def test_delivery_for(self):
        self.assertEqual(self.GRANT, "connections.nayanet")
        gctx = {"connections": {"nayanet": True}}
        d = {"enabled": True}
        self.assertEqual(self.delivery_for(d, gctx), "nayanet")
        self.assertEqual(self.delivery_for(d, {}), "queued_locally")
        self.assertEqual(self.delivery_for(dict(d, delivery="queued_locally"),
                                           gctx), "queued_locally")
        self.assertEqual(self.delivery_for(dict(d, delivery="nayanet"),
                                           gctx), "nayanet")
        with self.assertRaises(self.SchedulerRefusal) as cm:
            self.delivery_for(dict(d, delivery="nayanet"), {})
        self.assertEqual(cm.exception.code, "grant_required")
        self.assertIn("connections.nayanet", cm.exception.detail)
        with self.assertRaises(self.SchedulerRefusal):
            self.delivery_for(dict(d, delivery="pigeon"), gctx)

    def test_mode_for(self):
        gctx = {"connections": {"nayanet": True}}
        self.assertEqual(self.mode_for({"enabled": True}, gctx), "connected")
        self.assertEqual(self.mode_for({"enabled": True}, {}), "ready")


if __name__ == "__main__":
    unittest.main(verbosity=2)
