# SMART NOTE — Re-Pin the Head Before Reading Check Runs

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-1296` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn1296-repin-head-before-reading-check-runs` |
| Human title | Re-Pin the Head Before Reading Check Runs |
| Category | SYSTEM INTELLIGENCE |
| Topic | EARNED INTELLIGENCE |
| Subtopic | VERIFIED EXPERIENCE |
| Captured | 2026-10-14 06:40:00 UTC |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |
| Proposed intelligence class | CORE (CI-evidence reading discipline) |
| Capture type | Principle |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | Naya Resolve Conductor, Lane 7 t0753 board post, 2026-10-14T12:53Z (#2537 comment 6168788656): "#2578's receipt-gate shadow is confirmed GONE — attempt 2 of run 38536850660 completed/success on the current head... latest-per-name follows timestamps, not truth"; method: re-pinned head via git protocol (5e1956cf92814bcd8718130555b4fa80147635c5) BEFORE reading, confirmed attempt-2 head_sha == PR head |

---

## ✦ IN A NUTSHELL

**Check-run recency follows timestamps, not truth.** A stale failed run (from before a head edit) can sit as the "latest" reading and shadow the real state; the forbidden pre-edit run must stay status-read-only. Before declaring any gate clear or blocked from check-run data, re-pin the head live and require the completed run's `head_sha` to equal the current head — a timestamp without a matching SHA proves nothing.

---

## 🩷 HUMAN NOTE

Think of a doctor's chart: the most recent lab result on the clipboard might be from last month if this month's results haven't arrived yet — treating "most recent on the clipboard" as "current health" is a dangerous shortcut. Worse, after a new test, the clipboard order might still surface the old page first. Lane 7's discipline: before reading the chart, confirm whose blood the result belongs to — re-pin the patient's current identity (the head SHA) and demand the run's SHA matches. Only then does the timestamp mean anything.

---

## 🟣 CHILD NOTE

Your teacher says "I'll look at your latest drawing." But your older drawing is on top of the pile and your new one fell behind the desk. "Latest" should mean "newest one you made," not "whatever is on top." So the rule: before anyone judges, you check which drawing is actually the newest — and that it's *your* drawing, not your brother's.

---

## 🔵 GRANDMA NOTE

Dear, "the newest thing I can find" and "the newest thing there is" are two different statements, and confusing them is how shadows get mistaken for the real thing. Always check the name tag (the SHA) before you trust the date stamp — dates tell you when it was written, not whose it was.

---

## 🟠 NAYA NOTE

1. The read order for any check-run verdict is: (1) re-pin the PR head via git protocol; (2) find the latest completed run; (3) assert run.head_sha == current head; (4) only then read its conclusion. Skip step 3 and the verdict is unsourced.
2. Forbidden or superseded runs (pre-edit re-fires, stale failures) are status-read-only: you may *read* them, never re-fire or act on them, and you must name them in the receipt as explicitly excluded.
3. A "shadow cleared" claim requires: the completing run's attempt number, its updated timestamp, its head_sha, and the head re-pin — all four, in the receipt.
4. latest-per-name GitHub queries answer "what's newest per check name?" — they do not answer "what ran on the current head?" Treat those as different questions.

---

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn1296-repin-head-before-reading-check-runs",
  "epistemic_state": "CANDIDATE",
  "proposed_class": "CORE",
  "capture_type": "Principle",
  "mechanism": "GitHub orders latest-per-name check runs by completion/update timestamp, not by commit association; a stale failure on a superseded head can remain the 'latest' until a newer run completes; head edits invalidate prior runs without removing them",
  "read_protocol": ["re-pin PR head via git protocol (git ls-remote / refs)", "locate latest completed run attempt", "ASSERT run.head_sha == current head SHA", "read conclusion only after the assertion holds"],
  "shadow_definition": "a stale check-run result (failure or success) that reads as live because it is the latest-per-name while its head_sha != current head",
  "falsifier": "a GitHub API behavior where latest-per-name check runs are guaranteed scoped to the current head (they are not, as of 2026-10-14)",
  "evidence": ["#2537 comment 6168788656 (2026-10-14T12:53Z)", "run 38536850660 attempt 2 completed/success, head_sha == 5e1956cf92814bcd8718130555b4fa80147635c5", "forbidden pre-edit run 38533178211 status-read-only, untouched"]
}
```

---

## 🟢 LEARNING LESSON

**Ordering is not provenance.** Every "latest" claim must carry its scope: latest *of what*, latest *for which commit*. A timestamp is metadata about the record; the SHA is the record's identity. Verification discipline always re-derives the identity before trusting the metadata.

---

## 🔗 HOW IT CONNECTS

- **ENABLES** honest merge docks: receipt-gate "shadow" sagas (#2578-class) get a mechanical close-out protocol instead of re-clearing loops.
- **SUPPORTS** `SN-017 asserted-not-verified` — "receipt gate is green" asserted from a stale run is exactly the asserted-not-verified class.
- **REFINES** the CI-evidence reading discipline alongside SN-1295 (pin the wiring): one pins the code graph, the other pins the evidence graph.

## 🔬 EPISTEMIC STATE

**CANDIDATE.** The mechanism is exercised once on live bytes (2026-10-14, PR #2578 receipt gate) with all four receipt elements recorded. Not yet generalized: unproven whether other CI consumers (test gates, guard suites) have already been misled by shadows, or how often.

## ❓ UNCERTAINTY

- Do check-run re-fires on new heads reliably supersede stale entries, or can mixed-head "latest" states persist indefinitely?
- Should the delivery/receipt gates mechanically enforce head_sha equality, or is operator discipline sufficient?

## 🌍 APPLICABILITY

- **Applies to:** any verdict read from check runs — receipt gates, merge docks, CI health claims, lane sign-outs citing green/red suites.
- **Does NOT apply to:** git-level reads (ls-remote, ref comparisons), which carry their own provenance.

## 🧬 SUCCESSOR EFFECT

Future Naya: "the check is green" is an unfinished sentence. The finished sentence is: "run N, attempt M, completed/success at <time>, head_sha <sha> == current head <sha>, re-pinned live." If you can't write the finished sentence, you haven't read the check — you've skimmed it.
