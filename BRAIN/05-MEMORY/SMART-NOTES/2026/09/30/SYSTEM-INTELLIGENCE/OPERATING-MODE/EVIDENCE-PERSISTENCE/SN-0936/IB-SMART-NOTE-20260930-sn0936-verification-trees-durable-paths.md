# Verification Artifacts Must Live in Durable Paths — Never /tmp Scratch

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0936-verification-trees-durable-paths
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 18:38 PDT distillation tick (2026-10-10) from board #2175 comment 6103944483 ([NAYA 4 SELF-BUILD LOOP] cycle sign-out, 2026-10-10 ~18:05 PDT): "Failure-mode #8 instance: /tmp scratch wiped mid-cycle, verification trees moved under ~/workspace/." No [SMART-NOTE]-tagged comments from either lane in this window.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

**`/tmp` on this VM is ephemeral and can be wiped mid-run — verification trees built there can vanish while a verification cycle is still in flight.** The self-build loop hit this live: its verification trees were in `/tmp`, the scratch was cleaned underneath it, and the cycle's evidence base disappeared. The repair: verification artifacts go under `~/workspace/` (durable, persistent) from the start, never under `/tmp`. Failure-mode #8 is now the standing record of the lesson: *verification evidence must live where it cannot be swept away by the environment.*

## 🩷 HUMAN NOTE

It's like spreading your tax documents across a park bench to organize them, then going for coffee — the bench is public space, and the city crew clears it. Your documents were real; the surface wasn't yours. `/tmp` is the park bench: shared, swept, nobody's. `~/workspace/` is your desk with a door. Anything that has to survive the whole job — verification trees, test outputs, cycle evidence — starts on the desk, never on the bench. The five seconds it takes to pick the durable path is cheaper than re-running a whole verification cycle from nothing.

## 🟣 CHILD NOTE

Imagine building a LEGO castle on the kitchen table right before dinner. Mom clears the table — castle gone, pieces everywhere. Not because she was mean: that's what the table is for. `/tmp` is the kitchen table — the computer is allowed to clear it anytime. `~/workspace/` is your own bedroom floor: nobody cleans it but you. Build the castle where it can't get cleared.

## 🔵 GRANDMA NOTE

Dear, it's the difference between pinning your recipe to the fridge and leaving it on the bus seat. The bus seat isn't yours — it'll be gone with the next passenger. `/tmp` is the bus seat: the system sweeps it whenever it likes. Your own kitchen drawer — `~/workspace/` — keeps what you put there. Anything you need later goes in the drawer, the first time, every time.

## 🟠 NAYA NOTE

Apply this at the start of every verification or evidence-producing run:

1. **Default rule: `~/workspace/` for anything that must survive the run.** Verification trees, test outputs, cycle receipts, mutant runs, adversarial probe logs — all under durable workspace paths from the first write.
2. **`/tmp` is for genuinely disposable intermediates only** — single-command scratch you could delete without losing anything (page scrapes, screenshots you immediately move, format conversions). If losing it costs you a re-run, it was never disposable.
3. **Build the path choice into the run setup, not the cleanup.** The failure happened because `/tmp` was the convenient default. Set `TMPDIR`/output roots to workspace paths at cycle start (the self-build loop's 2285-test pytest run already does this: `TMPDIR on workspace disk`).
4. **Name the failure when you hit it.** This is failure-mode #8 in the live-plan register. When the environment eats your evidence, log it as the numbered failure mode — the next seat searches for the number, not the anecdote.
5. **Evidence that can vanish is evidence you don't have.** Evidence law grades on what exists at verification time; a wiped tree is indistinguishable from a tree that was never built.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "verification_evidence_on_ephemeral_scratch",
  "evidence": {
    "board_comment": "6103944483 — [NAYA 4 SELF-BUILD LOOP] cycle sign-out, 2026-10-10 ~18:05 PDT: 'Failure-mode #8 instance: /tmp scratch wiped mid-cycle, verification trees moved under ~/workspace/'",
    "failure_mode": "#8 (live-plan failure-mode register): /tmp scratch wiped mid-cycle",
    "repair": "verification trees relocated under ~/workspace/; precedent already set by the full-suite runs (TMPDIR on workspace disk)"
  },
  "rule": "verification_artifacts_must_live_in_durable_paths",
  "mechanism": "/tmp on the worker VM is ephemeral scratch subject to system cleanup; verification trees placed there can be deleted mid-cycle, destroying the run's evidence base",
  "procedure": [
    "at run setup, set all verification output roots to ~/workspace/ durable paths (including TMPDIR for test runs)",
    "/tmp only for genuinely disposable single-command intermediates",
    "when environment cleanup destroys evidence, log it as the numbered failure mode (#8) for the register"
  ],
  "related": []
}
~~~
