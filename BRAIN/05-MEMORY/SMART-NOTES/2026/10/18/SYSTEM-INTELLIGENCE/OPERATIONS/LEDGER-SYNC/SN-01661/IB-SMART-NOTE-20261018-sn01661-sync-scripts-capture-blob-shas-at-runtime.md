# Sync Scripts Capture Their Blob SHAs at Runtime

**Intelligent Block:** IB-SMART-NOTE-20261018-sn01661-sync-scripts-capture-blob-shas-at-runtime
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** hidden_files/shared-state.json director_tick_2026_10_18_1438 (2026-10-18T21:38:00Z): "ledger_script_repair": "director-ledger-sync-20261013T0640.py rewritten: runtime SHA capture per file + byte-compare skip (old hardcoded-SHA form 409'd when dispatcher pushed mid-tick; stdout truncation bug fixed)." Same-window race evidence: director_tick_2026_10_18_1408 "ledger_race": dispatcher rebuilt the ledger twice mid-tick (.ledger_hash de4175df54→3db64d32); pushed_hash re-anchored to the current hash so the next tick's compare detects further rebuilds. Script: hidden_files/bin/director-ledger-sync-20261013T0640.py.

## ✦ IN A NUTSHELL

A sync script that carries a hardcoded blob SHA from tick-start is pushing against a base that may no longer exist by push time — the dispatcher's mid-tick ledger rebuild proved it: the old hardcoded-SHA form 409'd on GitHub's contents API, which requires the CURRENT blob SHA as the update base. The repair is two moves: capture each file's SHA at push time (runtime), and byte-compare local vs remote before pushing so unchanged files skip the push entirely. Never hardcode a SHA across a tick boundary; the race window is the whole tick.

## 🩷 HUMAN NOTE

Shawn — the ledger sync broke in a subtle way this week: the script remembered each file's GitHub fingerprint from the start of its run, but the dispatcher rebuilt the ledger files mid-run, so by push time those fingerprints were stale and GitHub rejected the push. The script now re-reads the fingerprints right before pushing, and skips files that haven't changed at all. Rule for every future sync script: read the fingerprint at push time, never carry it across the run.

## 🟣 CHILD NOTE

Imagine you take a photo of a parking spot's number, then your friend moves the car while you're walking over. You hand the guard your photo and say "I'm in spot 12" — but the car is in spot 40 now, and the guard says no. The fix: don't trust the old photo; look at the spot number when you get there. And if the car hasn't moved at all, don't bother the guard. That's what the script does now: check the number at push time, skip the push if nothing moved.

## 🔵 GRANDMA NOTE

It's like mailing a change-of-address card with last year's zip code — the post office sends it back because the base address changed while you were writing. The ledger script was mailing with a stale zip code: it read GitHub's file fingerprints at the start of its run, but another worker rewrote the files mid-run, so the push got bounced. Now it reads the zip code at the moment of mailing, and doesn't mail at all if the address hasn't changed. Never trust a fingerprint older than the push.

## 🟠 NAYA NOTE

Cold successor: any script that pushes to GitHub's contents API (or any CAS-style update API) must capture the base blob SHA at push time and byte-compare before pushing.

1. Never hardcode a blob SHA, and never carry one across a tick boundary. Two writers (director tick + dispatcher) share the ledger; a mid-tick rebuild makes any tick-start SHA stale by push time, and the contents API 409s on a stale base.
2. The push sequence per file: (a) GET current blob SHA at push time; (b) byte-compare local content vs remote content — if identical, skip the push entirely (no call, no race); (c) PUT with the freshly captured SHA as base.
3. The tick log records the outcome per run (pushed N / skipped M / 409s K) so a stale-base race stays visible; pushed_hash is re-anchored to the current .ledger_hash after each sync so the next tick's compare detects further mid-tick rebuilds.
4. The stdout-truncation bug class rides with this note: sync scripts must capture command output to variables/files, not rely on truncated terminal tails, before computing SHAs.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1661",
  "title": "Sync Scripts Capture Their Blob SHAs at Runtime",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "OPERATIONS", "LEDGER-SYNC"],
  "applies_when": ["ledger-sync", "github-contents-api", "concurrent-writer", "director-pass", "claim-machinery", "sync-script"],
  "enforcement": "The sync script captures each file's blob SHA at push time and byte-compares local vs remote before pushing — no hardcoded SHA from an earlier tick is ever carried to a PUT. The tick log records pushed/skipped/409 counts per run, and pushed_hash is re-anchored to the current .ledger_hash after each sync; the scorer bounces any sync script or tick that pushes with a tick-start SHA.",
  "cousins": ["SN-1659 (carried counts name their base — this is the write-side sibling: a SHA is a count of trust in a base; capture the base at write time)"],
  "evidence": {
    "script_repair": "hidden_files/shared-state.json director_tick_2026_10_18_1438 (2026-10-18T21:38:00Z): ledger_script_repair = director-ledger-sync-20261013T0640.py rewritten with runtime SHA capture per file + byte-compare skip (old hardcoded-SHA form returned 409 when the dispatcher pushed mid-tick; stdout truncation bug fixed)",
    "mid_tick_race": "hidden_files/shared-state.json director_tick_2026_10_18_1408 'ledger_race': dispatcher rebuilt ledger twice mid-tick (.ledger_hash de4175df54->3db64d32); pushed_hash re-anchored to current hash so next tick's compare detects further rebuilds",
    "script": "hidden_files/bin/director-ledger-sync-20261013T0640.py (rewritten form holds the runtime-capture + byte-compare implementation)"
  },
  "decision_change": "the next sync-script build or repair reads blob SHAs at push time and skips byte-identical files instead of pushing with a tick-start SHA; the race window (tick-start to push) is eliminated by construction rather than narrowed by speed.",
  "falsifier": "if a mid-tick rebuild happens and a hardcoded-SHA push succeeds without a 409, the mechanism claim is falsified — GitHub's conflict detection would have to not fire on a stale base, which would invalidate the whole stale-base diagnosis.",
  "mechanism": "GitHub's contents API is CAS-style: an update requires the current blob SHA as its base, and a stale base 409s. With two writers (director tick + dispatcher) sharing the ledger, any SHA read at tick-start can go stale before the push lands. Capturing at push time narrows the race to the capture→PUT instant; byte-compare skip removes the push (and the race) entirely for unchanged files. The stdout-truncation bug was a second-order instance of the same disease: trusting a stale representation of live state."
}
```
