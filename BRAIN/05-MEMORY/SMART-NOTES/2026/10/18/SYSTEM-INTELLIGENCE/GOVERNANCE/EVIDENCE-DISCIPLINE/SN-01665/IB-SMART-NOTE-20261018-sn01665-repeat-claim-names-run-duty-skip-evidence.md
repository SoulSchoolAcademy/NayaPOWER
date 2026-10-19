# A Repeat Claim Names the Run, the Duty, and the Skip Evidence

**Intelligent Block:** IB-SMART-NOTE-20261018-sn01665-repeat-claim-names-run-duty-skip-evidence
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** hidden_files/live-plan.md DIRECTOR TICK 2026-10-18 20:38 PDT (2026-10-19T03:38Z), LEARNING EVENTS: L532 [F7] ("repeat claim names the run + duty + skip evidence").

## ✦ IN A NUTSHELL

The same claim gets re-posted tick after tick — a verdict re-carried, a renewal re-stated, a watch's finding re-announced. Without anchors, the repeat is indistinguishable from fresh evidence: nobody can tell whether it's a new observation or a stale echo wearing the same words. The discipline is three anchors on every repeat: the RUN (which run observed it), the DUTY (what duty that run was under), and the SKIP EVIDENCE (the evidence for what was skipped or absent). A repeat claim that names all three is a live signal with a traceable origin; one that doesn't is a stale echo and must not be re-carried.

## 🩷 HUMAN NOTE

Shawn — the team re-posts the same claims across ticks: verdicts re-carried, renewals re-stated. When the repeats don't say which run saw it, under what duty, and what evidence the skipped parts rest on, they blur together — old claims start looking like new observations. The new rule: any claim being repeated must re-anchor itself — name the run, the duty, and the skip evidence. Three words of provenance, and a stale echo can never masquerade as a fresh finding.

## 🟣 CHILD NOTE

Imagine a game of telephone where someone whispers the same message every round. If nobody says who heard it first and when, after ten rounds nobody knows if it's still the original message or a garbled copy. The fix: every time you repeat the message, you say "I heard this in round 3, from Emma, and I skipped the last part because the timer ran out." Now everyone can check: is this fresh, or just an old echo? Claims are the same — repeat them only with their three anchors: which run, which duty, what was skipped.

## 🔵 GRANDMA NOTE

It's like a rumor that keeps coming back around. If everyone just repeats "did you hear..." without saying who heard it first, when, and what's known versus guessed, the rumor starts feeling like a fact. The rule going forward: before a claim is repeated, the repeater must say where it came from — which run observed it, what job that run was doing, and what evidence covers the parts that were skipped. A repeated claim without its origins is just an echo, and echoes don't count as news.

## 🟠 NAYA NOTE

Cold successor: treat every re-posted claim as a stale echo until it re-anchors itself. The three anchors are mandatory:

1. **The run** — which run (tick window, lane seat, comment ID) observed this claim. Not "the night-shift said it" — the specific run.
2. **The duty** — what duty that run was under when it made the claim (BUILD sweep? VERIFY audit? WIRE renewal?). The same words mean different things under different duties.
3. **The skip evidence** — the evidence backing what the claim says was skipped or absent. "0 births" needs the sweep that read the set; "carry holds" needs the byte-identity proof.

A repeat claim carrying all three is a live signal with a traceable origin — re-carry it freely. A repeat missing any of them is UN-ANCHORED: do not re-carry it to the next tick; bounce it back to the author for the anchors first.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1665",
  "title": "A Repeat Claim Names the Run, the Duty, and the Skip Evidence",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "EVIDENCE-DISCIPLINE"],
  "applies_when": ["claim", "carry", "repeat", "lane-executor", "stale-echo", "board"],
  "enforcement": "A repeat claim is INCOMPLETE unless it quotes the run (which run observed it — tick window, seat, comment ID), the duty (what duty the run was under when it made the claim), and the skip evidence (the evidence backing what the claim says was skipped or absent). A scorer spots re-carried claims lacking any of the three anchors and bounces them as UN-ANCHORED (stale-echo class). Un-anchored claims are not re-carried to the next tick.",
  "cousins": ["SN-1659 (a carried count names its counting base — the count-side sibling; this is the claim-side: counts name their base, claims name their origin)", "SN-1664 (handoff 'delivered' is a claim — the same claim-hygiene family; this extends it to repeat claims across ticks)", "SN-1306 (delivery proven where the Naya reads, not where the author writes — the principle this operationalizes for repeats)"],
  "evidence": {
    "learning_event": "hidden_files/live-plan.md DIRECTOR TICK 2026-10-18 20:38 PDT (2026-10-19T03:38Z), LEARNING EVENTS: L532 [F7] (repeat claim names the run + duty + skip evidence)",
    "context": "night ticks re-post the same claims (PIN-MATCH streaks, ENFORCED renewals, adjudication verdicts); the WP-163 stale-echo standing practice (21st-25th consecutive application the same night) names the failure class this discipline closes"
  },
  "decision_change": "the next repeat-claim decision (re-carrying a verdict, re-stating a renewal, re-announcing a finding) names the run + duty + skip evidence, or the claim is bounced as UN-ANCHORED and is not re-carried to the next tick.",
  "falsifier": "an anchored repeat claim (run + duty + skip evidence all quoted) that still produces stale-echo confusion — e.g. two anchored repeats of the same claim under different runs that get misattributed, or an anchor that no one can verify because the named run never existed — would falsify the three-anchor discipline's sufficiency: the anchors would be ritual, not discrimination.",
  "mechanism": "Identical prose re-posted by different runs under different duties is indistinguishable from fresh evidence: the words are the same, the origins are not. The three anchors pin the claim to its origin — the run fixes the observation point, the duty fixes the meaning of the words, the skip evidence fixes what was verified as absent. Together they make a stale echo visible as stale rather than mistaken for fresh, the same drift class SN-1659 closed for counts."
}
```
