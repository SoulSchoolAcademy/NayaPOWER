# Exhaust the Existing Instrument Before Building a New One

**Intelligent Block:** IB-SMART-NOTE-20261006-sn0516-exhaust-the-existing-instrument-before-building-a-new-one
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A proof gap is usually not missing infrastructure — it is an unasked question of the existing instrument. When the github-dispatch proof seam appeared unproven, the fix was not new tooling: the existing VM-executed contract suite could already fire the real handler branches; the proof layer had simply never asked it to. Before building anything new, enumerate what the current harness can already observe, and ask it the right question first.

## 🩷 HUMAN NOTE

Naya 1's cycle attacked the github-dispatch proof seam by extending the EXISTING VM-executed contract suite to fire the real handler branches instead of grepping source text — added observed firing proofs for seven guards, request-order assertions, preserved happy-path and replay controls, and ratcheted guard liveness 59→65/147 with a full green suite. Her stated lesson: the gap was not missing guard logic or missing tooling. It was missing observation. The team habit this installs: diagnose against the existing instrument first; build new machinery only after the current one is proven exhausted. New tools are invented slowly, maintained forever; asking one new question of an old tool is cheap.

## 🟣 CHILD NOTE

Before you buy a new tool, check the toolbox. The wrench you already own might fit — you just haven't tried turning it on the right bolt.

## 🔵 GRANDMA NOTE

Don't build a new machine before you've asked the old one everything it can do. The proof was already possible with what was in hand; someone just hadn't asked the right question yet.

## 🟠 NAYA NOTE

Operational procedure when a proof gap appears:

1. Enumerate the existing instruments (harnesses, suites, scanners) and what each can already observe — read their capabilities, don't assume.
2. Ask whether the gap is missing observation (the harness CAN reach the path but hasn't been asked to) vs missing capability (the harness CANNOT reach it).
3. Only build new tooling on a proven cannot-reach.

In this instance the real branches (AUTHORITY_GRANT_REQUIRED, EXPLICIT_APPROVAL_REQUIRED, IDEMPOTENCY_KEY_REQUIRED, INTELLIGENT_BLOCK_ID_INVALID, GITHUB_READ_FAILED, GITHUB_COMMIT_FAILED, PROJECTION_UNVERIFIED) were all reachable by the existing VM-executed suite; the proof layer had only ever asked it to fire lower-blast-radius branches. Result: closed on PR #1682 head `a9834a28`, no new infrastructure, no merge authority crossed, main untouched.

Related: pairs with SN-0514 — one says gates must be able to fail, this says existing gates/harnesses must be asked fully before being declared insufficient. Evidence: `#1354` comment 6029033679 (2026-10-07T01:39Z, Naya 1 github-dispatch sign-out), PR #1682 (OPEN, MERGEABLE, NOT MERGED at sign-out).

## 🟢 MACHINE NOTE

~~~json
{
  "smart_note": {
    "id": "SN-0516",
    "ib_identity": "IB-SMART-NOTE-20261006-sn0516-exhaust-the-existing-instrument-before-building-a-new-one",
    "truth_state": "CANDIDATE",
    "scope": "PRIVATE",
    "captured": "2026-10-06",
    "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
    "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/MEASUREMENT-BOUNDARY"
  },
  "doctrine": {
    "rule": "Exhaust the existing instrument before building a new one.",
    "diagnostic": "Classify a proof gap as missing-observation vs missing-capability before building tooling.",
    "cost_note": "New tools are invented slowly and maintained forever; one new question to an existing tool is cheap."
  },
  "lineage": ["SN-0514"],
  "evidence": {
    "board": "#1354 comment 6029033679",
    "carrier": "PR #1682 head a9834a28f6f0aa1b114b0b98aef7daae4fa94eea",
    "result": "guard liveness 59/147 -> 65/147, full suites green, PR OPEN not merged"
  }
}
~~~
