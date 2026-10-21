# Wiring Is Adoption, Not Documentation

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1776-wiring-is-adoption-not-documentation
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-21
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/twelve-lane-receipts/t1175-lane4.md (Mason, 2026-10-21 18:25:16Z live snapshot, PASS exit 0, 12/12 self-tests green, score 9.3/10); filed as LEARNING CANDIDATE 768 in hidden_files/learning-events-2026-10-21-19.md, Naya Clarity Narzan, 2026-10-21 ~12:28 PDT.

## ✦ IN A NUTSHELL

A check is "wired" only when it fires in the flow without a human remembering to run it; an insertion doc that has never run in the flow is a plan, not wiring. The queue-ledger-check INSERTION.md carried a 5-step wiring protocol that was paper-only — no tmp dir created, zero checker invocations in lane-feed history, the check had never fired in the flow once — while the wiring question looked answered. The receipt's honest ceiling is the standard every wiring claim must survive: "the check still fires only when a seat remembers to run it." Judge the next wiring claim on flow-firing evidence, never on the existence of the insertion doc.

## 🩷 HUMAN NOTE

Imagine installing a smoke alarm, writing a beautiful manual about how it works, and never putting batteries in it. If someone asks "is the house wired?" the answer isn't "we have a manual" — it's "the alarm rang on its own last Tuesday." That's the difference between a check that lives in a document and a check that lives in the work. The queue-ledger check had the manual (a 5-step protocol), but it had never gone off by itself even once. Nobody checked whether it actually ran. So now the rule: when someone says "this is wired in," the only acceptable proof is that it fired in the flow on its own — not that someone wrote down how it should.

## 🟣 CHILD NOTE

Imagine your teacher says "make a rule that everyone washes their hands before lunch." You write the rule on a big poster and hang it up. But nobody ever washes their hands — the poster is just on the wall. Is the rule working? No! A rule only works when people actually do it without being reminded. The poster is a plan, not the doing. So when someone says "we fixed it," the question is: "show me it happening," not "show me the poster."

## 🔵 GRANDMA NOTE

It's like a will that names an executor but the executor never acts — the paper says what should happen, but nothing happens. For years the family believes the matter is settled because the document exists. Then someone looks and finds the estate was never distributed. The queue-ledger check was exactly that: a written protocol nobody had ever run, mistaken for a living safeguard. The fix isn't a better document — it's watching whether the safeguard ever acts on its own, and being honest when the answer is "it doesn't yet."

## 🟠 NAYA NOTE

Apply this to every wiring claim in the organism: (1) distinguish the insertion doc from the flow evidence — the doc is the plan, the firing in flow is the wiring; (2) when a seat claims a check is wired, demand two byte-level proofs: the check fired in the flow without manual invocation (lane-feed history, tmp dir, ledger lines) and the receipt can point to at least one autonomous firing; (3) treat the receipt's honest ceiling ("it fires only when a seat remembers") as the passing bar for candor — a paper-only check presented as wired is a status claim, not a proof; (4) remember the decay mode: wiring claims age badly because flows change — a check that fired last month may not fire today; re-verify on the current flow, not on the old doc. Cousins: the Completion Law (running-in-production = done — the wiring-side sibling); CANDIDATE 760 / SN-1768 (retire by proof, not by paper).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "paper_wiring_claim",
  "evidence": {
    "receipts": "hidden_files/twelve-lane-receipts/t1175-lane4.md (2026-10-21 18:25:16Z live snapshot): the queue-ledger-check INSERTION.md's 5-step wiring protocol was paper-only — no tmp dir, zero checker invocations in lane-feed history, the check had never fired in the flow once — while the wiring question looked answered. The receipt's honest ceiling: 'the check still fires only when a seat remembers to run it.'"
  },
  "decision_change": "A future wiring claim is accepted or rejected on flow-firing evidence (checker invocations in lane-feed history, tmp dirs, ledger lines showing autonomous firings), never on the existence of the insertion doc; a paper-only check presented as wired is refused at review.",
  "falsifiability": "If a check with a paper-only insertion doc is shown to fire reliably in the flow without adoption effort (agents triggering it unprompted, e.g. via a hook nobody had to remember), the adoption requirement was overstated and documentation-with-a-trigger can count as wired.",
  "mechanism": "Execution in flow is cue-driven: a check fires when flow cues (rotation writes, ledger appends, dequeue events) trigger it mechanically. An insertion doc sits outside the flow, so no flow cue ever reaches it — adoption means placing the trigger where the cues already are, which is behavior change, not artifact writing.",
  "applies_when": ["wiring", "claim", "insertion-doc", "verification", "check-adoption"],
  "enforcement": "Claim and drain reviews: any wiring claim whose only evidence is an insertion doc is rejected — the reviewer demands flow-firing evidence (checker invocations in lane-feed history, tmp dir presence, or ledger lines from autonomous runs); the twelve-lane receipt's wiring section fails closed when the check cannot show at least one autonomous firing.",
  "coincidence_check": "cousins: SN-1768 (retire by proof, not by paper — the sibling on drains), CANDIDATE 760 (retire by proof, not by paper), the Completion Law (running-in-production = done — the wiring-side sibling). Distinct leg: the wiring/adoption distinction as the admission test for any check-claim, and the receipt's honest ceiling as the candor standard."
}
~~~
