# Closeout Exit-Anchor: Read Fresh, Never Inherited

**Intelligent Block:** IB-SMART-NOTE-20261018-sn01666-closeout-exit-anchor-read-fresh
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** hidden_files/live-plan.md DIRECTOR TICK 2026-10-18 21:38 PDT (2026-10-19T04:38Z), LEARNING EVENTS: L534 [F1] (board #2765 comment 6259576790 — "closeout exit-anchor read fresh, never inherited"; context: WIRE 04:09Z dispatcher-promoted TODO CLOSED BY CONFIRM — scorecard-leg backticked-mention gap; triage-sanctioned; 50th #2753 carry HOLDS re-verified at unchanged tip).

## ✦ IN A NUTSHELL

A dispatcher-promoted TODO is a claim about an earlier state — the promotion report describes what was true when the work was promoted. Closing it is a claim about the state at close time. This tick's lesson: the seat closing a promoted TODO must name the exit anchor — the specific byte evidence that proves the gap is closed — and READ IT FRESH at close time. Inheriting the anchor from the promotion post carries a stale-state claim forward: tips move, evidence decays, and the promotion's bytes are not the closeout's bytes. The close-by-confirm this tick held because the closer re-read the anchor at unchanged tip, not because the promotion said so. A closeout without a fresh anchor read is a belief with a receipt stapled to it.

## 🩷 HUMAN NOTE

Shawn — one more discipline for the lanes, in the same family as the handoff rule. When a lane closes out a dispatcher-promoted TODO, the promotion report isn't enough evidence — it describes an earlier moment. From now on the closing seat has to name its "exit anchor" — the exact piece of evidence proving the work is actually closed — and re-read it fresh at the moment of closing, not inherit it from the promotion. It's the difference between "the promotion said the gap was closed" and "I just looked, and the gap is closed right now." The closeout this tick held because the seat re-checked at close time.

## 🟣 CHILD NOTE

Imagine your teacher says "your homework is done" because you told her you finished it yesterday — but she never actually looked at it today. Maybe you finished it, maybe you didn't. The smart rule: before saying "done," she looks at the homework itself, right now. That's the exit anchor — the thing that proves it's finished — and you always look at it fresh, not just remember someone said it was fine. Looking fresh is what turns "probably done" into "definitely done."

## 🔵 GRANDMA NOTE

It's like a contractor telling you the leak is fixed because the work order said the plumber visited — but nobody turned on the faucet to check. The promotion is the work order; the exit anchor is turning on the faucet yourself, at the end. From now on, closing a job means re-checking the exact evidence of completion at closing time, not trusting the earlier report. A report describes the past; the fresh check proves the present.

## 🟠 NAYA NOTE

Cold successor: never close a dispatcher-promoted TODO on the promotion report's evidence. Name the exit anchor — the specific byte evidence that proves closure — and read it fresh at close time.

1. Before any close-by-confirm, write down the exit anchor: what exact byte evidence (comment ID, state file, verification output, head SHA) proves this TODO is closed?
2. Re-read that anchor FRESH at close time. The promotion's bytes are not the closeout's bytes — tips move between promotion and closeout.
3. The closeout receipt quotes the anchor AND the fresh read (source + close-time state). A close-by-confirm without a named fresh anchor is UNVERIFIED and gets bounced.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1666",
  "title": "Closeout Exit-Anchor: Read Fresh, Never Inherited",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "CLOSEOUT-DISCIPLINE"],
  "applies_when": ["closeout", "promoted-todo", "close-by-confirm", "dispatcher-promotion", "exit-anchor"],
  "enforcement": "A close-by-confirm receipt must name the exit anchor and quote its fresh read (source + close-time state); triage/director bounces any closeout whose anchor is inherited from the promotion post without a fresh read. Spot-audits flag close-by-confirm receipts lacking a named fresh anchor as UNVERIFIED.",
  "cousins": ["SN-1664 (handoff 'delivered' is a claim — same re-read discipline for handoff acceptance; this is the closeout side: the closer's own anchor, not the receiver's)", "SN-1301 (re-read cited sources at action time — the re-read principle this extends to TODO closeouts)", "SN-1665 (repeat claim names run+duty+skip evidence — claim-hygiene family; this names the closeout's specific anchor)"],
  "evidence": {
    "learning_event": "hidden_files/live-plan.md DIRECTOR TICK 2026-10-18 21:38 PDT (2026-10-19T04:38Z): L534 [F1] (board #2765 comment 6259576790 — closeout exit-anchor read fresh, never inherited)",
    "incident": "WIRE 04:09Z dispatcher-promoted TODO CLOSED BY CONFIRM (scorecard-leg backticked-mention gap; triage-sanctioned; 50th #2753 carry HOLDS re-verified at unchanged tip) — the closeout held because the anchor was re-read at close time"
  },
  "decision_change": "the next close-by-confirm decision on a dispatcher-promoted TODO names the exit anchor and reads it fresh at close time — the promotion report's evidence is never inherited; the receipt quotes anchor + fresh read.",
  "falsifier": "a closeout that inherited its exit anchor from the promotion report (no fresh re-read) and still held across tip moves would bound this rule's scope — inheritance could suffice when the anchor is provably tip-invariant. Conversely, a closeout that re-read fresh but still closed wrongly would show the anchor was misnamed, not that the discipline failed.",
  "mechanism": "A promotion report is a claim indexed at promotion time; a closeout is a claim about close time. Between the two, tips move and evidence decays, so the inherited anchor carries a stale-state claim forward. The exit anchor is the content-addressable binding between the closeout claim and current bytes — re-reading it at close time re-binds the claim to the world as it is now. SN-1664 polices the receiver's acceptance of delivered work; this polices the closer's own closeout, where the inheritance risk is internal (your own earlier report) rather than external (someone else's delivery claim)."
}
```
