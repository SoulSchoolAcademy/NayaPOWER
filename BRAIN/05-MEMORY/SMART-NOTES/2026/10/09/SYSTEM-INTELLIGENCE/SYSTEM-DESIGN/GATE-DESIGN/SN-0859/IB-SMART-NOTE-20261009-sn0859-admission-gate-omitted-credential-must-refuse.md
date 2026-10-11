# An Omitted Credential Is Not an Absent Check — Fail Closed on the Missing Ticket

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0859-admission-gate-omitted-credential-must-refuse
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09 ~21:20 PDT
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6093707728 (Naya 5 safety achievement); `kernel/self_integration.py` `integrate_verified_lesson`; branch `naya5/safety-lesson-admission-chokepoint` (remote `cbc08e1c`); tip `8a41a18e2`

## ✦ IN A NUTSHELL

Gate 4 of `integrate_verified_lesson` — the gate that lets a verified lesson change how the system behaves — read `if admitted_as and admitted_as != "CANDIDATE"`. The `and` short-circuit meant a lesson arriving with **no admission ticket at all** skipped the check entirely and walked straight through. The seam's own contract said "all gates must hold / anything failing is refused" — but the code whitelisted omission. The gate only checked the ticket *when one was attached*; a missing ticket meant no check ran, which the code read as a pass. The fix is one word shorter than the bug: `if admitted_as != "CANDIDATE"` — no ticket, or the wrong ticket, means refused, and the store stays untouched. The doctrine: **an admission check must be fail-closed on absence.** The signature of this bug class is `if x and x != expected` — the guard tests the credential only when present, and treats "nothing to test" as "pass." Any gate where a missing field means *no check runs* is an open door wearing a lock's costume. Five new falsifiers went RED→GREEN proving it (pre-fix, all three omit-field cases integrated without raising); existing 30/30 unchanged; full suite 1706 passed / 11 skipped at tip `8a41a18e2`. The blast radius was latent — the behavior store isn't read by production decisions yet — so the gate is now fail-closed *before* the wiring lands, which is the only time closing it is cheap.

## 🩷 HUMAN NOTE

The guard checked IDs at the door — but only if you showed one. Walk up empty-handed and the guard just waved you in, because the rule was written as "if you have an ID and it's the wrong one, stop." The fix rewrites the rule as "if you don't have the right ID, stop" — which covers the empty-handed case too. Whenever you write a permission check, ask: what happens when the field is simply missing? If "missing" means "skip the check," you don't have a lock — you have a door with a sign on it.

## 🟣 CHILD NOTE

The rule said: "If you have a ticket AND your ticket is the wrong kind, you can't come in." But what if you have NO ticket at all? The rule forgot to say anything about that — so people with no ticket walked right in. The fixed rule says: "If your ticket is not the right kind, you can't come in" — and no ticket at all definitely counts. Always make rules that say what happens when something is missing, not just when it's wrong.

## 🔵 GRANDMA NOTE

It's like a bouncer told to check invitations — "if someone shows you an invitation and it's a fake, turn them away" — but nobody told him what to do when someone shows up with nothing at all. So he just let them in. The fix tells the bouncer: no proper invitation, no entry — no exceptions, no loopholes. Whenever a rule guards something precious, it has to cover the empty-handed case.

## 🟠 NAYA NOTE

Fail-closed is not a slogan, it's a shape: the default path refuses, and only a positive credential opens it. The bug shape to burn into memory: `if credential and credential != EXPECTED` — truthy-guard short-circuit silently passes the absent case. The correct shape is `if credential != EXPECTED` (refuse on absent *and* wrong), or an explicit two-gate (presence check, then value check). Audit protocol for any admission/authorization gate: (1) enumerate every gate's inputs; (2) for each input, ask what the code does when the input is absent/None/empty — not wrong, *absent*; (3) if absence skips the gate, that's a bypass, not a corner case — write the falsifier first (omit-field cases must RAISE), then fix; (4) prefer closing gates *before* the machinery they guard goes live — latent blast radius is the cheapest moment to fix. Companion checks: the seam's contract ("all gates must hold") must be true of the code, not just the docstring — diff the contract against the implementation.

## 🟢 MACHINE NOTE
```json
{
  "block": "IB-SMART-NOTE-20261009-sn0859",
  "status": "CANDIDATE",
  "mechanism": "Admission/authorization gates must fail closed on ABSENT credentials, not just wrong ones. The bug signature is `if x and x != EXPECTED`: the truthy-guard short-circuits when x is absent, so no check runs and absence reads as pass. The fix shape is `if x != EXPECTED` (absent or wrong both refuse) or an explicit presence-gate plus value-gate.",
  "bug_signature": "truthy-guard short-circuit on the credential input — `if admitted_as and admitted_as != \"CANDIDATE\"`",
  "audit_protocol": [
    "Enumerate every admission gate's inputs.",
    "For each input, determine what the code does when the input is absent/None/empty — not wrong, absent.",
    "If absence skips the gate, write omit-field falsifiers first (must RAISE pre-fix), then fix.",
    "Close gates before the machinery they guard goes live — latent blast radius is the cheapest fix window.",
    "Diff the seam's stated contract ('all gates must hold') against the implementation."
  ],
  "evidence": {
    "board_comments": ["6093707728"],
    "file": "kernel/self_integration.py",
    "function": "integrate_verified_lesson gate 4",
    "branch": "naya5/safety-lesson-admission-chokepoint",
    "branch_head": "cbc08e1c",
    "proof": "5 new falsifiers RED->GREEN (3 omit-field cases integrated pre-fix without raising); existing 30/30 unchanged; full suite 1706 passed / 11 skipped at tip 8a41a18e2"
  }
}
```
