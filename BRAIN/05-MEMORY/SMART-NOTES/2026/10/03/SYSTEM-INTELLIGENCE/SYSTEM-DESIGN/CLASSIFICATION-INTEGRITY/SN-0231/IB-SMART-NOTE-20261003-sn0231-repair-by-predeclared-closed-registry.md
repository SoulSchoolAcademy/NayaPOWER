# Repair by Predeclared Registry — Fail-Closed, Text-as-Proposals, Declared-Class-or-UNKNOWN

**Intelligent Block:** IB-SMART-NOTE-20261003-sn0231-repair-by-predeclared-closed-registry
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-03
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Naya 4 self-build sign-in #554 comment 5973006019 (2026-10-03T20:07:06Z) — H8-7 applicability repair design decision, main pin `5b68f8dc`; extends SN-0225 (CONFIRMED BUG: lesson-text regex gamable)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

After SN-0225 confirmed that `deriveGraphApplicability` keys applicability on literal lesson-text strings (gamable: 3 adversarial false-positives + 1 false-negative under Deno 2.9.7, with 4/4 green positive controls), the repair-design decision — made and recorded on the board at sign-in — went for a **predeclared task-class registry** over a governed classifier: the repair is **fail-closed**. Free text no longer confers APPLICABLE; text triggers are **downgraded to proposals only**. A relationship row earns APPLICABLE only when a declared class belongs to the **closed registry** (provenance-attested); otherwise the verdict is UNKNOWN, never a guess. Design chosen before a single line of code: branch `naya4/h87-applicability-governed-registry`, single-file patch to `nayanet-learning-verify/index.ts`, Deno-executed positive/negative/adversarial controls, PR opened unmerged, merge parked with Shawn.

Why this is brain-grade: this is SN-0095's honest-UNKNOWN discipline applied as *repair design*. When the vulnerability is "a string in the world can plant a trust verdict," there are exactly two repair shapes — make the classifier smarter, or stop deriving verdicts from the string. The registry shape is chosen because it **moves the trust decision off the attack surface entirely**: the class must already exist, attested, in the closed set; nothing the lesson text says can mint a new one. The general form: at any trust boundary, prefer a **predeclared closed set of claimable values** over a smarter parser of untrusted input. Text proposes; the registry disposes; everything else is UNKNOWN. A cold successor facing the same design fork (registry vs classifier, allowlist vs parser) can adopt this decision and its justification without re-deriving it.

## 🩷 HUMAN NOTE

Shawn — the H8-7 fix design is decided and on the board: a predeclared registry, fail-closed. Lesson text stops being able to grant APPLICABLE — it becomes a proposal only, and a class has to already exist in a closed, provenance-attested registry to count. Anything else is UNKNOWN, never a guess. Small patch, Deno proof with adversarial controls, PR opens unmerged; the merge itself is yours as always.

## 🟣 CHILD NOTE

Remember the gamable-clerk bug (SN-0225)? A sneaky sentence could trick the system into stamping a lesson as "applies here!" even when it didn't. The fix that's designed now: a **special list** of allowed classes, made ahead of time, that nobody can add to at runtime. A sentence can only *suggest* — "hey, maybe this class applies!" — and the system checks the list. If the class is on the list, it's allowed. If not, the answer is "UNKNOWN," which just means "I don't know" — never a guess. That's how you beat a trickster: stop letting the trickster's words decide.

## 👵 GRANDMA NOTE

You remember the bug where a clever sentence could fake an "applicable" stamp (SN-0225)? The fix design is decided. Instead of building a smarter reader of those sentences, the team chose a **fixed list of permitted classes**, written ahead of time and sealed — nothing at runtime can sneak a new one onto it. Sentences can now only *suggest* an answer; the list has the final word. If the suggested class is on the list, fine. If not, the honest answer is "UNKNOWN" — a plain "I don't know," never a guess. The principle: when someone's words could be trying to fool you, don't trust the words — trust only a list you made yourself beforehand.

## 🤖 NAYA NOTE

H8-7 repair design DECISION (CANDIDATE, implementation not yet proven). Source: Naya 4 self-build sign-in #554 5973006019 (2026-10-03T20:07:06Z, main pin `5b68f8dc`). Decision: **predeclared task-class registry (provenance-attested) over governed classifier**. Fail-closed semantics: (1) free-text triggers downgraded from verdicts to **proposals**; (2) APPLICABLE requires a declared class ∈ the **closed registry**; (3) else UNKNOWN — the honest non-verdict (SN-0095/SN-0083 discipline). Execution plan (recorded, not yet proven): branch `naya4/h87-applicability-governed-registry`, single-file patch `nayanet-learning-verify/index.ts`, Deno-executed positive/negative/adversarial controls, PR opened unmerged, merge parked with the director. Cycle form worth preserving: the *design decision* was posted to the board at sign-in before code — the decision is reviewable by the lane before implementation, and the sign-out will carry proof or the exact blocker. Cousins: SN-0225 (the bug this repairs — string-keyed classifier is gamable), SN-0226 (the stale-gap lesson that preceded it — re-verify the gap at the pin), SN-0095 (compose-at-the-consumer / honest UNKNOWN), SN-0083 (retain the UNKNOWN with missing evidence named). Anti-pattern named: making the untrusted-input parser smarter instead of moving the verdict off the attack surface. The decision record names what was NOT chosen (governed classifier) and why — a cold successor re-opening the fork must weigh the same alternative, not rediscover it.

## ⚙️ MACHINE NOTE

{"sn": "SN-0231", "title": "Repair by Predeclared Registry — Fail-Closed, Text-as-Proposals, Declared-Class-or-UNKNOWN", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-03", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "SYSTEM-DESIGN", "CLASSIFICATION-INTEGRITY"], "cousins": ["SN-0225", "SN-0226", "SN-0095", "SN-0083", "SN-0221"], "evidence": {"decision": "#554 comment 5973006019 (2026-10-03T20:07:06Z) — H8-7 repair design decision at sign-in, main pin 5b68f8dc", "bug": "SN-0225 — deriveGraphApplicability regex gamable (3 FP + 1 FN, Deno 2.9.7)", "rejected_alternative": "governed classifier (smarter parser) — rejected: keeps verdict on the attack surface"}, "status": "design decision recorded CANDIDATE; implementation + Deno proof + unmerged PR pending sign-out; merge parks with the director", "rule": "at trust boundaries prefer a predeclared closed registry over a smarter parser: text proposes, the registry disposes, everything else is UNKNOWN"}
