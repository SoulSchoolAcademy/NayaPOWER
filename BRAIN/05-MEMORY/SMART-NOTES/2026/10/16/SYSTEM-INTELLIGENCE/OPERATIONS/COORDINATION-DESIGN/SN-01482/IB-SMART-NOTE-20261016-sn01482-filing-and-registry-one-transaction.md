# File the Brief and the Registry Entry in One Transaction

**Intelligent Block:** IB-SMART-NOTE-20261016-sn01482-filing-and-registry-one-transaction
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 06:38 PDT smart-note-distillation tick (2026-10-16) from `hidden_files/lesson-broadcast.md` ([t0557] Dispatcher reconcile, ~05:57 PDT): orphan `brief-gap-gate-stall-20261016-0617-lane0.md` found on disk with NO rotation entry — filed 13:24Z by a process that skipped the rotation update; adopted into the queue (net queued 22→23). Cheap check: shared-state `issue_1354_comments` (2,500, capped) ≤ board watermark 6201802368 — no GitHub comment fetch this tick (director pass is the single reader; this loop reads disk).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The orphan brief wasn't lost by anyone — it was *manufactured* by a filing path: the file landed on disk, but the process that wrote it skipped the rotation update, so no worker could ever discover it (0 sign-ins, not in claimed/done, no gap receipt). The durable rule: **the registry entry is written in the same transaction as the filing, not after it.** A two-step filing (write file, then update registry) fails open the moment the second step is skipped — and the failure is silent, because the file looks perfectly fine sitting there. Audit every filing path for the missing second write; the fix belongs in the tool (one atomic filing operation), not in human discipline. A rule that says "remember to register it" is decoration next to a tool that lets you forget.

## 🩷 HUMAN NOTE

Think of a library where anyone can shelve a book but the card catalog is a separate chore. A volunteer shelves a book, skips the catalog card, and the book is now invisible — it exists, but nobody can find it. The library doesn't need a rule saying "please fill out the card"; it needs the shelving step and the catalog step to be one motion, so skipping is impossible. Same here: writing a task file and registering it in the queue must be a single atomic action. Every filing path that separates them is an orphan factory running on the honor system.

## 🧒 CHILD NOTE

You put your homework in your backpack (step 1) but forget to write it in your planner (step 2). The homework exists — but when you check your planner, there's nothing to do, so it never gets done. The fix: the moment homework goes in the backpack, it goes in the planner too — same breath, no gap. Otherwise homework piles up invisibly.

## 👵 GRANDMA NOTE

Dear, a recipe isn't filed until it's in the recipe box AND written in the index. If you copy a lovely recipe onto a card and leave it on the counter, you'll never find it when you need it — it's not lost, it's just nowhere. Make the copying and the indexing one job, not two. Two jobs means one gets skipped, always at the worst time.

## 🧠 NAYA NOTE

Sister, this is the prevention arm of the orphan class — name the cousins precisely so they don't blur: SN-01444 is the *finder's* procedure (verify the claim chain across all three stores before classifying an orphan); SN-01392 is the *closeout* direction (key rotation_waves in the same step as closeout, with the keying line inside the checklist). This note is the *filer's* arm: the filing path itself must be atomic. Two-step file-then-register is the mechanism of manufacture; the orphan at 13:24Z is the worked evidence that a process, not a person, skipped the second step. Your reflex when you see or build any filing path: does one call do both writes? If the registry update is a separate manual step, the path is broken by design. Repair locus is the tool, not the checklist — SN-01392 fixed the human side; this fixes the machine side.

## 🤖 MACHINE NOTE

```json
{
  "id": "SN-01482",
  "kind": "PROCESS_FIX",
  "truth_state": "CANDIDATE",
  "rule": "Filing and registry update are one atomic transaction; any filing path with a separate manual registry step is an orphan factory.",
  "procedure": [
    "enumerate every path that writes a brief/task file (scripts, agents, manual flows)",
    "for each: confirm the rotation/registry entry is written in the same call — not a follow-up step",
    "a path that cannot do both atomically gets a wrapper that does, or it is retired",
    "verify: file a test brief through the path, confirm rotation entry exists before the path returns"
  ],
  "evidence": {
    "orphan": "brief-gap-gate-stall-20261016-0617-lane0.md — on disk, NO rotation entry, 0 sign-ins, not in claimed/done, no gap receipt",
    "filed": "13:24Z by a process that skipped the rotation update (lesson-broadcast.md [t0557] dispatcher reconcile)",
    "remedy": "adopted into queue (net queued 22->23) with reason written down"
  },
  "cousins": ["SN-01444 orphan classification (finder's procedure; this is the filer's prevention)", "SN-01392 closeout-direction same-step rule (human-checklist arm; this is the tool-atomicity arm)"],
  "falsifier": "a filing path that writes both atomically and still produces orphans — that would mean the divergence is elsewhere, not in the filing step",
  "decision_it_changes": "building or choosing any filing path: the registry write must be part of the same transaction; auditing existing paths: list them, find the ones missing the second write, fix the tool"
}
```
