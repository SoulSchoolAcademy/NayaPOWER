Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

The 13:10Z learning event (board #2793 comment 6365442855, 2026-10-23) had to explicitly re-separate two reds the system had fused: "#3003 cures ONLY brain-index x3, NOT MANIFEST_STALE; #3003 is NOT its cure" — MANIFEST_STALE x14 needed its OWN owner (door/KNOW lane per 6360126130). The failure was not the cure, it was the unscoped cure claim: both reds lived in one "the index is red" namespace, so the team assumed the in-flight cure covered both, urgency was absorbed by the wrong lane, and when the cure shipped the uncovered red would have been found owned by nobody. The durable rule: **a cure lands with a declared addressed-failure set — a red not in the set stays owned-open with its own named owner.** An unscoped cure manufactures phantom coverage.

## 🩷 HUMAN NOTE

Shawn — the team caught itself making an expensive assumption this morning. #3003 (the index cure) was filed against the brain-index failures only — but because it was called "the index cure," everyone assumed it would also fix the MANIFEST_STALE red. The learning event had to say it out loud: #3003 cures ONLY brain-index x3, NOT MANIFEST_STALE — and that failure needs its own owner, its own fix. The lesson: every cure has to declare exactly which failures it addresses. Anything not on that list stays owned and open with a name next to it. An undeclared cure lets the team believe a red is covered when nobody owns it.

## 🟣 CHILD NOTE

Imagine your bike has a flat tire AND a broken bell. The repair shop says "we'll fix your bike" and you assume they mean everything. They fix the tire and hand it back — and the bell is still broken, but nobody checks because everyone thought "the bike is being fixed." Now the rule: the shop has to write down exactly what they're fixing — "flat tire only." Anything not on the list still needs someone to fix it, with a name next to it.

## 🔵 GRANDMA NOTE

It's like calling the plumber for a leaking kitchen sink and a clogged bathroom drain, and saying "fix the plumbing." He fixes the sink and leaves; the drain is still clogged, but nobody follows up because "the plumbing got fixed." The rule going forward: every job starts with a written list of what's included — and whatever isn't on the list still has someone's name next to it. Never let a general claim swallow a specific problem.

## 🟠 NAYA NOTE

This is SN-1806's cousin one layer up. SN-1806 said detection is not remediation — this says a *remediation claim* is not scoped coverage. Both reds (brain-index freshness x3, MANIFEST_STALE x14) shared the "index is red" namespace, so the cure's identity absorbed both and dissolved responsibility for one. The mechanism is phantom coverage: an unscoped claim is read as covering the namespace, the wrong lane's urgency drains, and the uncovered red survives as nobody's. What makes the 13:10Z event the proof rather than the theory is that the separation had to be *explicitly re-stated* hours into the assumption's life — the correction cost was a named hour of misrouted ownership. The seat-level fix is cheap and mechanical: every cure handoff carries an addressed-failure-set field, and the red register cross-checks it — a red absent from every cure's set keeps its own named owner by construction. Cousin: SN-1806 (detection ≠ remediation); sibling in the named-failure-modes list: MANIFEST_STALE (which this note's evidence explicitly re-separated from #3003's scope).

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1872-cure-must-declare-addressed-failures",
  "lesson": "A cure lands with a declared addressed-failure set — a red not in the set stays owned-open with its own named owner. An unscoped cure manufactures phantom coverage: both reds share a namespace, the cure's identity absorbs both, and the uncovered red survives as nobody's. Observed 2026-10-23: #3003 was filed against brain-index freshness x3, but the team assumed it covered MANIFEST_STALE x14 (same 'index is red' namespace); the 13:10Z learning event (board #2793 comment 6365442855) had to explicitly re-state 'SCOPE CLARIFIED - #3003 cures ONLY brain-index x3, NOT MANIFEST_STALE; #3003 is NOT its cure; MANIFEST_STALE x14 needs OWN owner (door/KNOW lane per 6360126130)'. The separation cost ~7h of misrouted ownership (06:24Z door filing -> 13:10Z clarification).",
  "applies_when": ["cure", "routing", "triage", "red-register", "post-merge-cure", "ownership"],
  "enforcement": "Every cure handoff/claim carries an addressed-failure-set field, cross-checked against the open-red register (receipt-breach log / red register / WIRE failing-test list): a red not in any cure's set keeps its own named owner — door/KNOW lane for MANIFEST_STALE x14, KNOW/index lane for #3003's brain-index x3. Verify: learning event 6365442855 explicitly re-separated the sets after the unscoped assumption persisted ~7h (from the 06:24Z door filing); the named-failure-modes list records #3003's cure scope as brain-index-only.",
  "evidence": [
    "board #2793 comment 6365442855 (learning event, 2026-10-23T13:10Z — 'Learning event: 5th consecutive zero-filing hour; SCOPE CLARIFIED - #3003 cures ONLY brain-index x3, NOT MANIFEST_STALE; #3004 failed Kernel Tests + 4 gates at own head; L476 7th zero-breach hour')",
    "shared-state.json director_tick_20261023_1310 carries: 'MANIFEST_STALE x14 needs OWN owner (door/KNOW lane per 6360126130) - #3003 is NOT its cure' + '#3003 cure still OPEN (updated 11:31Z), rebase owed, do not duplicate'",
    "independent audit 6360126130 (2026-10-23T07:47Z) named the door/KNOW lane as MANIFEST_STALE's owner — the owner the unscoped cure assumption displaced",
    "cousin SN-1806 (detection is not remediation) — this is the cure-claim scoping cousin"
  ]
}
```
