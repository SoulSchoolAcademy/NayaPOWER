# Name the Gate's Read Surface Before Choosing Re-fire vs Fix

**Intelligent Block:** IB-SMART-NOTE-20261018-sn01660-name-the-gates-read-surface-before-re-fire-vs-fix
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** hidden_files/live-plan.md (2026-10-18): L529 [F7] (INTELLIGENT EVENTS ×13, board comment 6256271577) — "name the gate's read surface before choosing re-fire vs fix (Kappa's #2763 MERGE-READY superseded her own w479 frozen-payload theory)." Kappa's MERGE-READY verdict on #2763 relayed in hidden_files/shared-state.json director_tick_2026_10_18_1508 (board comment 6255539930). Receipt-pin trigger-gap precedent (Kappa w454, 6253244392): receipt-gate.yml listens to [opened, synchronize] only — pull_request:edited never fires it.

## ✦ IN A NUTSHELL

When a gate misbehaves, the first question is not "do I re-fire it or fix it" — it is "what does this gate actually read?" Kappa first theorized the merge gate's payload was frozen (w479); her own #2763 MERGE-READY verdict later superseded that theory, because once the gate's read surface was named, the verdict followed from what the gate could see, not from the theory. The order of operations is load-bearing: name the read surface first, then choose re-fire vs fix. A theory argued against an assumed read is a theory argued against a ghost.

## 🩷 HUMAN NOTE

Shawn — when a check looks stuck or wrong, the team now names what the check actually reads before deciding whether to re-run it or repair it. Kappa showed why: she first guessed the merge gate's data was frozen, then her own verdict on #2763 overruled that guess — because once she wrote down the gate's real read surface, the answer was in what the gate sees, not in the theory. New rule: no "re-fire or fix" call without the read surface quoted on the record.

## 🟣 CHILD NOTE

Imagine the vending machine eats your dollar. You could kick it (re-fire) or open it up (fix) — but first, look at which slot it actually takes dollars from. If you kick the candy door while your dollar went into the bill slot, you learned nothing. Kappa's lesson: before you choose kick vs open, point at the slot the machine reads. The machine can only react to what it can see; your plan has to start there, not with your guess about what broke.

## 🔵 GRANDMA NOTE

It's like the thermostat wars: the house feels cold, so someone cranks the heat — but nobody checked where the thermostat reads the temperature. It's sitting over the stove, so it thinks the house is warm and shuts the furnace off. Cranking the dial (re-fire) and replacing the furnace (fix) both miss the point until you look at where the thing actually senses. Kappa's rule: read where the gate reads, then decide what to do. The sensor's location is the first fact; everything else follows.

## 🟠 NAYA NOTE

Cold successor: when a gate's verdict looks stale, wrong, or stuck, do NOT choose between re-firing and fixing until the gate's read surface is on the record.

1. Quote the gate's read surface: the workflow's `on:` trigger block (which events fire it — e.g. receipt-gate.yml listens to [opened, synchronize] only; pull_request:edited never fires it) and the payload/read paths it acts on (which API surfaces it queries).
2. Re-derive the verdict FROM that read surface. If the surface explains the behavior (e.g. "pending" because the gate never saw the re-save — its trigger never fired), the theory about staleness is superseded: the gate is behaving correctly on a narrow read, and the decision is extend-the-surface or re-fire-on-a-firing-event, not fix-the-logic.
3. Only if the named read surface is fresh-and-correct AND the verdict still misbehaves do you choose fix-the-gate. That falsifies the read-surface theory — file the falsification.
4. Receipt line: "gate <name> read surface: on=<triggers>, reads=<paths>; verdict <x> follows / does not follow from the surface; decision: <re-fire|fix|extend-surface>."

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1660",
  "title": "Name the Gate's Read Surface Before Choosing Re-fire vs Fix",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "GATE-VERDICTS"],
  "applies_when": ["gate", "ci-gate", "merge-watch", "receipt-pin", "verdict-adjudication", "gate-misbehavior"],
  "enforcement": "Any gate-misbehavior verdict (re-fire vs fix) must quote the gate's read surface — the workflow's on: trigger block and the payload/read paths it acts on — before adjudicating. The scorer bounces gate verdicts that name neither a read surface nor quote the trigger block; the merge-watch carries a standing re-check of receipt-gate.yml's on: block (opened/synchronize only) at each adjudication.",
  "cousins": ["SN-1605 (gate evidence surface mismatch — that note is about posting where the gate reads; this note is about quoting the read before adjudicating)", "SN-1112 (sweep names its read set — the read-set naming family)", "SN-1658 (IV-head binding: exact heads — a verdict that follows from the named read is exact, not theoretical)"],
  "evidence": {
    "l529_f7": "hidden_files/live-plan.md: L529 [F7] (6256271577): 'name the gate's read surface before choosing re-fire vs fix (Kappa's #2763 MERGE-READY superseded her own w479 frozen-payload theory)'",
    "merge_ready_verdict": "hidden_files/shared-state.json director_tick_2026_10_18_1508 relay: Kappa #2763 MERGE-READY verdict 6255539930",
    "read_surface_precedent": "hidden_files/shared-state.json director_tick_2026_10_18_1108: receipt-gate.yml listens to [opened, synchronize] ONLY (L19 @ tip); pull_request:edited never fires it — the read surface that explained the 'verdict pending' misread"
  },
  "decision_change": "the next gate-misbehavior verdict quotes the gate's read surface (triggers + read paths) before choosing re-fire vs fix; a theory about the gate's state argued against an unnamed read is inadmissible.",
  "falsifier": "a gate whose named read surface is fresh-and-correct yet whose verdict still misbehaves on re-fire falsifies the read-surface theory — the bug is then in the verdict logic, not the read; file the falsification and choose fix-the-gate.",
  "mechanism": "a gate acts only on what it reads (its trigger events and query surfaces), never on what you assume it reads. Staleness theories are almost always theories about an assumed read; naming the actual read collapses the theory space to a single checkable fact. Kappa's w479 frozen-payload theory died the moment the real read surface was quoted, because the theory had been argued against a ghost read."
}
```
