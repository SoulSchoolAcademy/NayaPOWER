# Spec-True Is Not Code-True — One Grep Kills an Inherited Premise

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01188-spec-true-is-not-code-true-one-grep-kills-inherited-premise
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** `lesson-broadcast.md` [t0632] Naya Conductor (mirror, t0628 auth-gate checklist, 9.0/10); code pin `tools/smart_note_v2.py:545` (`_update_registry_locked` carries zero `retrieval_authorized` refs); contradicted claim from spec-0007 text ('capture-time explicit-FALSE default')

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya Conductor was verifying an auth-gate claim and inherited a premise from spec-0007: that a "capture-time explicit-FALSE default" exists on the stamping path. One grep of the actual code — `tools/smart_note_v2.py:545`, `_update_registry_locked` — showed zero `retrieval_authorized` references. The premise was spec-true and code-false. The new fact came from grepping the CODE, not the spec. The doctrine: **a spec sentence is a claim about the code; the code is the evidence.** When the two disagree, the code wins — always, without a debate. A cold successor who trusts the spec over the bytes inherits a lie with citations.

Why this is brain-grade: this is the sharpest form of a general rot. Specs are written once and believed forever; code changes under them. Every "the spec says" is a hypothesis with an expiry date, and the expiry test is one grep. The t0632 run generalized the brief's watch-for ('re-derive the on-main fact at action time') to *everything* — pins, counts, writers, callers — and the one inherited premise that softened on contact with bytes was exactly the one nobody re-checked. The expensive mistakes are never the facts you verify; they're the ones you cite.

## 🩷 HUMAN NOTE

Shawn — a worker caught a case where the written spec said one thing and the actual code said another. The spec claimed a default was stamped at capture time; one look at the real code showed the function in question never touches that field at all. The lesson we're locking in: the spec is a claim, the code is the evidence — when they disagree, the code wins, no debate. This is the same "read reality" rule the decision machine runs on, applied to our own paperwork.

## 🟣 CHILD NOTE

Imagine the recipe book says "add sugar," but you open the pantry and there's no sugar — the cake you're tasting has no sugar in it. Which do you believe: the book, or your tongue? Your tongue, obviously — the book describes what *should* be there; the tasting tells you what *is* there. That's what happened here: the spec book said a stamp happens at capture time, but tasting the actual code showed the stamping function never touches that ingredient. Believe the tasting. One look at the code beats a whole chapter of the book.

## 👵 GRANDMA NOTE

The map is not the territory, dear. The spec is a map — drawn once, believed forever. The code is the territory — it changes under the map while nobody redraws it. A good traveler checks the road, not the map, when they disagree. Here the traveler checked: one look at the real function, and the spec's claim wasn't on the road at all. Rule for the house: never argue from the map against someone standing on the road. Check the road.

## 🤖 NAYA NOTE

Evidence-hierarchy doctrine, VERIFIED instance. Instance: t0628 auth-gate checklist (mirror receipt [t0632] Naya Conductor, 9.0/10). Inherited premise from spec-0007: a capture-time explicit-FALSE default exists on the stamping path. Mechanism: grepped `tools/smart_note_v2.py:545` (`_update_registry_locked`) → zero `retrieval_authorized` refs → premise FALSE on code. Conclusion: W1 does NOT stamp; spec-true != code-true. Binding: (1) a spec sentence is a claim; the code is the evidence — disagreement resolves to the code, no debate; (2) the 're-derive at action time' discipline generalizes from pins to *every* inherited premise — counts, writers, callers, defaults; (3) the un-re-derived premise is the one that softens: treat every uncited spec claim as a hypothesis with an expiry date, expired by one grep. Cousin family: SN-0950 (merge-commit SHA is a hypothetical preview — same evidence hierarchy, CI flavor); SN-0888 (AST not grep for code-governance gates — code as evidence, different instrument). Status: the auth-gate finding stands as code-verified; spec-0007 text carries the stale claim.

## ⚙️ MACHINE NOTE

{"sn": "SN-1188", "title": "Spec-True Is Not Code-True — One Grep Kills an Inherited Premise", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-13", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "EVIDENCE-DISCIPLINE"], "cousins": ["SN-0950", "SN-0888"], "evidence": {"code": "tools/smart_note_v2.py:545 _update_registry_locked carries zero retrieval_authorized refs", "claim_killed": "spec-0007 'capture-time explicit-FALSE default' — spec-true, code-false", "witness": "lesson-broadcast.md [t0632] Naya Conductor (mirror, t0628 auth-gate checklist, 9.0/10)"}, "status": "auth-gate finding stands as code-verified; spec-0007 text carries the stale claim", "rule": "a spec sentence is a claim about the code; the code is the evidence — on disagreement the code wins, always; every uncited spec claim is a hypothesis with an expiry date, expired by one grep"}
