# SMART NOTE — Gate-Failure Triage: Grammar, Discrimination, Delivery

> **Attribute every RED to the right layer before blaming the gate or the PR.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-0995` |
| Intelligent Block | `IB-SMART-NOTE-20261011-sn0995-gate-failure-triage` |
| Human title | Gate-Failure Triage: Grammar, Discrimination, Delivery |
| Category | SYSTEM INTELLIGENCE |
| Topic | CI-TRIAGE |
| Subtopic | FAILURE-ATTRIBUTION |
| Captured | 2026-10-11 16:45:00 UTC |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |

---

## ✦ IN A NUTSHELL

**A red gate is not automatically a broken gate, and a red PR is not automatically a broken PR.** Triage in three layers, in order: **(1) GRAMMAR** — is the input well-formed per the gate's contract? **(2) DISCRIMINATION** — does the gate pass good inputs and fail bad ones? **(3) DELIVERY** — did the triggering event actually fire the gate? Attribute the RED to the right layer. Never declare a gate malfunction or blame a PR's content until all three layers are checked.

---

## 🩷 HUMAN NOTE

When a check goes red, three different things could be wrong:

1. **The input is malformed** (grammar). The gate is working — it correctly rejected something that doesn't meet the contract. Example: a receipt gate fails on a PR whose body has no `## Evidence` heading. That's not a gate bug; that's the gate doing its job.
2. **The gate is genuinely broken** (discrimination). The test: does it fail bad inputs AND pass good ones? If the same gate goes green on well-formed bodies, it discriminates correctly — the mechanism is sound.
3. **The event never reached the gate** (delivery). The content was fixed, but the gate never re-ran — a trigger-wiring gap, not a content failure. The fix is mechanical (re-fire: empty commit, synchronize, close-reopen), not editorial.

Check in that order: grammar → discrimination → delivery. Each layer cleared is evidence; each skipped layer is a misdiagnosis waiting to happen.

---

## 🟣 CHILD NOTE

Imagine a smoke alarm. If it rings because there is smoke, the alarm is right — don't blame the alarm. If it rings when there is no smoke AND stays quiet when there IS smoke, the alarm is broken. And if someone fixes the smoke but the alarm never got the message, the problem is the message, not the smoke and not the alarm. Check which one it is before you decide what to fix.

---

## 🔵 GRANDMA NOTE

When the red light comes on, don't guess what's wrong — check three things in order: first, is what we gave it in the right shape? Second, does the checker itself give right answers on known-good and known-bad cases? Third, did the checker even run? Only then decide whether the checker, the message, or the work needs fixing. That way nobody "repairs" the wrong thing.

---

## 🟠 NAYA NOTE

Adopt this as the standard gate-debugging order before any repair, revert, or blame:

1. **Grammar:** read the gate's contract (e.g., L224: literal heading + live-resolvable handles). Is the input contract-conformant? A gate that REDs a malformed head is *firing as designed*.
2. **Discrimination:** find a known-good input. Does the gate GREEN there? If yes, the gate discriminates correctly — mechanism sound, content at fault. Record the positive control.
3. **Delivery:** check the gate run log timestamps. Zero runs since the fixing edit = a trigger-delivery gap (one-off `edited`-event loss is observed and recoverable), not a content verdict. Re-fire mechanically; do NOT re-edit content to "fix" it and do NOT attribute the RED to the PR.

Real case (2026-10-11): #2283's receipt-gate FAILURE was grammar (no `## Evidence` in body) — correct RED; #2340's SUCCESS 5 seconds after the body edit was the discrimination positive control; #2343's stale RED was delivery (no gate runs after the edit) — unblocked by re-fire, not by content change.

---

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20261011-sn0995-gate-failure-triage",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-11T16:45:00Z",
  "triage_order": [
    {
      "layer": "GRAMMAR",
      "check": "input conforms to gate contract (e.g. L224 literal heading + live-resolvable handles)",
      "if_red": "gate firing as designed; fix the input"
    },
    {
      "layer": "DISCRIMINATION",
      "check": "gate GREENs on known-good inputs and REDs on known-bad inputs",
      "if_red": "mechanism suspect; record positive control before repair"
    },
    {
      "layer": "DELIVERY",
      "check": "gate run timestamps show a run AFTER the fixing edit",
      "if_red": "trigger-delivery gap; re-fire mechanically (empty commit / synchronize / close-reopen); do NOT re-edit content"
    }
  ],
  "evidence": [
    {"board": "#2175", "comment": 6110710537, "kind": "VERIFY sign-out B-08 evidence sweep"},
    {"pr": 2283, "gate": "receipt", "verdict": "FAILURE", "head": "54f9ba08", "cause": "grammar: no ## Evidence heading"},
    {"pr": 2340, "gate": "receipt", "verdict": "SUCCESS", "head": "93eb473d", "cause": "positive control, 5s post-edit"},
    {"pr": 2343, "gate": "no runs since 15:12:27Z edit", "cause": "delivery: one-off edited-event gap", "unblock": "empty-commit/synchronize"}
  ],
  "related_notes": [],
  "supersedes": null
}
```

---

## ⚠️ TRUTH BOUNDARY

**Proven:** the three-layer triage correctly classified #2283 (grammar), #2340 (discrimination positive control), and #2343 (delivery gap) on 2026-10-11. **Not implied:** every RED fits exactly one layer (compound failures exist — clear one layer at a time); the triage replaces gate repair (it only diagnoses).

This IB remains **CANDIDATE** — only Shawn ratifies.

---

**END — SMART NOTE / INTELLIGENT BLOCK**
