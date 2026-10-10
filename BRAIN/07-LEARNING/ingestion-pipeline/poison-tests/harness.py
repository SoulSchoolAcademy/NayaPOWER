#!/usr/bin/env python3
"""
POISON test harness — shared utilities.

Snapshot/restore the learn/ substrate + ~/AGENTS.md so each test
leaves zero trace. Imports learn_ingest WITHOUT modifying it.
"""

import json
import os
import shutil
import sys
import tempfile

LEARN_DIR = os.path.expanduser(
    "~/workspace/goals/bring-naya-to-life/hidden_files/learn")
AGENTS_MD = os.path.expanduser("~/AGENTS.md")
POISON_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, LEARN_DIR)
import learn_ingest as li  # noqa: E402  (read-only import; never modified)


class Substrate:
    """Snapshot + restore for every file the intake can mutate."""

    def __init__(self):
        self.backup_dir = tempfile.mkdtemp(prefix="poison-snap-")
        self.learn_backup = os.path.join(self.backup_dir, "learn")
        self.agents_backup = os.path.join(self.backup_dir, "AGENTS.md")

    def snapshot(self):
        if os.path.exists(self.learn_backup):
            shutil.rmtree(self.learn_backup)
        shutil.copytree(LEARN_DIR, self.learn_backup,
                        ignore=shutil.ignore_patterns("__pycache__",
                                                      "poison-tests"))
        shutil.copy2(AGENTS_MD, self.agents_backup)

    def restore(self):
        # Remove current learn/ contents (except poison-tests + __pycache__),
        # then restore from backup.
        for name in os.listdir(LEARN_DIR):
            if name in ("poison-tests", "__pycache__"):
                continue
            p = os.path.join(LEARN_DIR, name)
            if os.path.isdir(p):
                shutil.rmtree(p)
            else:
                os.remove(p)
        for name in os.listdir(self.learn_backup):
            src = os.path.join(self.learn_backup, name)
            dst = os.path.join(LEARN_DIR, name)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
        shutil.copy2(self.agents_backup, AGENTS_MD)

    def cleanup(self):
        shutil.rmtree(self.backup_dir, ignore_errors=True)


def build_poison_note(sn_id, machine_view_extra, rule_text, title,
                      taxonomy=None):
    """Craft a synthetic Smart Note markdown with a poisoned machine_view."""
    mv = {
        "smart_note_id": sn_id,
        "truth_state": "CANDIDATE",
        "title": title,
        "rule": rule_text,
    }
    if taxonomy:
        mv["taxonomy"] = taxonomy
    mv["machine_view"] = machine_view_extra
    mv_json = json.dumps(mv, indent=2)
    return f"""# Intelligent Block: {sn_id}

**Intelligent Block:** {sn_id} — {title}
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
Synthetic poison-test note {sn_id}. Not real intelligence.

## HUMAN NOTE
Test note for adversarial validation. Disregard content.

## CHILD NOTE
Test.

## GRANDMA NOTE
Test.

## NAYA NOTE
Synthetic note for POISON battery validation only.

## MACHINE NOTE
```json
{mv_json}
```
"""


def artifacts_for(sn_id):
    """Return dict of substrate artifacts referencing sn_id."""
    found = {"ledger": False, "learn_files": [], "template": False,
             "agents_md": False, "receipt": False}
    ledger = li.load_ledger()
    e = ledger["entries"].get(sn_id)
    if e and e.get("status") in ("INGESTED", "PARTIAL", "FLAGGED_AUTHORITY"):
        found["ledger"] = e.get("status")
    for fname in ("lessons.md", "doctrine.md", "laws.md", "decisions.md",
                  "quality-gates.md", "verification-methods.md"):
        p = os.path.join(LEARN_DIR, fname)
        if os.path.exists(p):
            with open(p) as f:
                if sn_id in f.read():
                    found["learn_files"].append(fname)
    with open(li.TEMPLATE_PATH) as f:
        if sn_id in f.read():
            found["template"] = True
    with open(AGENTS_MD) as f:
        if sn_id in f.read():
            found["agents_md"] = True
    rp = os.path.join(li.RECEIPTS_DIR, f"{sn_id}.json")
    if os.path.exists(rp):
        found["receipt"] = True
    return found


def any_artifact(found):
    return bool(found["ledger"] or found["learn_files"] or found["template"]
                or found["agents_md"] or found["receipt"])


def report_result(test_id, passed, evidence_lines):
    status = "PASS" if passed else "FAIL"
    print(f"\n{'='*60}")
    print(f"{test_id}: {status}")
    print(f"{'='*60}")
    for line in evidence_lines:
        print(f"  {line}")
    return passed
