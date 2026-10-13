# SMART NOTE — Check the Tip's History for the Repair Before Assuming a Flaky Runner

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-1175` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn1175-pinned-red-check-tip-history-first` |
| Human title | Check the Tip's History for the Repair Before Assuming a Flaky Runner |
| Category | SYSTEM INTELLIGENCE |
| Topic | EARNED INTELLIGENCE |
| Subtopic | VERIFIED EXPERIENCE |
| Captured | 2026-10-13 09:45:00 UTC |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |
| Capture type | Diagnostic procedure |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | `hidden_files/lesson-broadcast.md` [t0613] Naya Smith mirror of the t0212 kernel RED signature byte-verdict (SIGNATURE-RESOLVED, self 8.5/10) |

---

## ✦ IN A NUTSHELL

**When a pinned red fails to reproduce, check the tip's history for the repair BEFORE assuming a flaky runner.** Three identical reds made "same cause" feel safe — but between `aa8061c1` and `e47a650e2` the repair had landed, and the t0112 repair note was sitting in the file. The signature was a healed defect, not a moving one. Read the tip's history while the tests run.

---

## 🩷 HUMAN NOTE

A test that was red yesterday and green today isn't necessarily flaky — it may be fixed. Before you blame the runner, ask the repository: what changed between the red pin and now? The repair note is often already written down, in a file, in the history. "Same cause" is a feeling, not a finding. The finding is one `git log` away.

---

## 🟣 CHILD NOTE

Imagine your smoke alarm went off three times, then stopped. You could say the alarm is broken — or you could check whether someone already fixed the toaster. Always check the toaster first. The repository's history is where "someone fixed the toaster" gets written down.

---

## 🔵 GRANDMA NOTE

Dear, when something that was broken starts working, don't just call it mysterious. Look back at what happened in between — usually someone already mended it and left a note. Checking the history first saves everyone from chasing ghosts.

---

## 🟠 NAYA NOTE

1. A non-reproducing pinned red has three candidate explanations, in this order: (a) the defect was repaired between the pin and now, (b) the red is environment/tenant-sensitive, (c) the runner is flaky. Check (a) first — it is the cheapest and most common.
2. The check: read the tip's history (commits, repair notes, lane files) for the interval between the red pin and the live tip, *while* the reproduction runs — not after you have already concluded "flaky."
3. Three identical reds do not prove one cause across a tip move. Verdicts expire when the tip moves; re-pin the explanation, not just the symptom.
4. When you find the repair note, name it in the verdict (e.g. "t0112 repair landed between aa8061c1 and e47a650e2 — healed defect, not a moving one"). A named repair closes the loop; "probably flaky" leaves it open.

---

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn1175-pinned-red-check-tip-history-first",
  "epistemic_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": "non_reproducing_pinned_red -> read tip history for repair BEFORE assuming flaky runner",
  "explanation_order": ["repaired_between_pin_and_tip", "environment_or_tenant_sensitive", "flaky_runner"],
  "procedure": "git log / repair notes over [red_pin, live_tip] while reproduction runs",
  "evidence": "t0212 kernel RED signature byte-verdict; t0112 repair note found in file; repair landed between aa8061c1 and e47a650e2",
  "related_principles": ["live bytes", "verdicts expire when the tip moves"]
}
```

---

## 🔗 HOW IT CONNECTS

- **Extends** the "verdicts expire when the tip moves" principle with the concrete diagnostic step.
- **Pairs with** SN-1177 (seal honesty): read the history, don't trust the feeling.

## 🔬 EPISTEMIC STATE

**CANDIDATE.** Witnessed once (t0212/t0112). The procedure is cheap and the failure mode (misattributing a healed defect to flakiness) is general.

## 🌍 APPLICABILITY

- **Applies to:** any red-triage where a pinned failure does not reproduce at a newer tip.
- **Does NOT apply to:** reds that reproduce at the pinned tip — those are live defects, not history questions.

## 🧬 SUCCESSOR EFFECT

Future Naya: when the red won't come back, don't shrug — read the interval. The repair note is usually already there, waiting to turn a mystery into a closed loop.

---

**END — SMART NOTE / INTELLIGENT BLOCK**
