# The Policy Cannot Self-Extend: Anti-Self-Reference in Promotion Gates

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0215-policy-cannot-self-extend
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-02
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** `#554` 5960552278 (H12 sign-in, 20:05:35Z) / 5960593216 (H12 sign-out, 2026-10-02 20:07:25Z), Naya 4 self-build loop

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

At 12:03 PDT, run 37051569993 made the first observed automatic-promotion attempt under the ratified `STANDING-PRODUCTION-PROMOTION-V1`. Step 4 (`Enforce ratified standing policy before automatic promotion`) failed; steps 5–13 (build/push/dispatch/receipt) were skipped. Production was verified untouched at `8d41eee8`. The H12 verification cycle (read-only; main pinned at `5b68f8dc`) traced the causal chain end to end: the required-CI wait loop fail-closed before any policy verdict was reached — the tip was red on the SN-0213 drift vector, so the gate refused before it even had to decide.

The deeper finding came from re-reading the policy engine itself at the pin (workflow sha `05915637350a`): `evaluate_policy()` (`tools/standing_production_promotion_policy.py` `dd70b3566ceb`) re-reads expiry and status **from the ratified policy document itself** — the code is annotated with the doctrine in plain words: "Ratification is not a license to rely on caller-supplied expiry assertions." And it DENYs automatic promotion for any change under protected paths, including `.naya/governance/` itself — **the policy cannot self-extend on the automatic path**. A governance document is structurally unable to rewrite its own rules without a human's explicit word.

The denial is proven non-vacuous (SN-061 family): the explicit-human path under this same workflow promoted successfully on the Human Director's D3 runs — so the automatic denial is a real verdict, not a broken pipe. Remaining leg, named honestly: the verdict-legibility path never fired live — the denial took the SystemExit fail-closed before the verdict writer ran. That is MISSING EVIDENCE (small), not a bug; the candidate repair (compute the verdict and write the denial receipt even on CI-red) is held because the workflow is protected and Shawn's word is required.

Why this is brain-grade: promotion gates are where "fail closed" is most often theater. A gate that trusts the caller's claims about itself — about its own expiry, its own scope, its own terms — can be talked into opening by exactly the process it exists to restrain. The doctrine: **the governed policy engine must authenticate its own terms from its own canonical record, and protected paths — especially governance — must be structurally unpromotable without a human**. Any cold successor designing a promotion gate needs this before anything else: if the policy can be self-extended, there is no gate, only a door with a sign on it.

## 🩷 HUMAN NOTE

Shawn — the first-ever automatic promotion attempt happened today at 12:03 PDT, and the gate did exactly what it's supposed to: refused, and left production untouched at `8d41eee8`. I traced the whole chain read-only at the pin. Two things worth your ear: the policy engine doesn't trust anyone's word about its own terms — it re-reads expiry and status straight from the ratified doc ("ratification is not a license to rely on caller-supplied expiry assertions"); and `.naya/governance/` can never auto-promote, meaning the policy can never change itself on the automatic path — only your explicit word moves it. One small open leg: the denial-receipt path never fired live (the denial took the fail-closed route before the verdict writer ran). It's missing evidence, not a bug — and I won't touch that protected workflow without your word.

## 🟣 CHILD NOTE

Imagine a school where a rulebook decides who gets to skip class. The dangerous version: a student hands the rulebook a note saying "the rules say I can skip" — and the rulebook believes the note. The safe version (what we have): the rulebook reads its own pages, never the student's note, and there's one more rule the rulebook follows — it can't add new rules by itself. Only the principal can change the rulebook. Today's test: a student tried to skip class automatically; the rulebook said no, read its own pages, and told the principal.

## 👵 GRANDMA NOTE

Think of a gatekeeper who is handed a letter saying "the gatekeeper says I may pass." A careless gatekeeper might just believe the letter. Ours doesn't — it checks its own instruction book instead, every single time. And there's a rule it can never break: the instruction book can't rewrite itself. Only the boss changes the instructions. Today the gate faced its first real test — it turned the request away, and everything valuable stayed safe behind the gate.

## 🤖 NAYA NOTE

Anti-self-reference doctrine for promotion gates (BEHAVIORALLY VERIFIED live, 2026-10-02): ratified `STANDING-PRODUCTION-PROMOTION-V1` v1.0.0 (in force through 2026-10-29) enforced by workflow `Enforce ratified standing policy before automatic promotion` (workflow sha `05915637350a` at pin `5b68f8dc`); `evaluate_policy()` (`tools/standing_production_promotion_policy.py` `dd70b3566ceb`) re-reads expiry/status from the ratified doc, never caller-supplied assertions; protected paths incl. `.naya/governance/` always DENY automatic promotion (policy cannot self-extend). First live automatic-promotion attempt: run 37051569993 (push @ `5b68f8dc`, 12:03 PDT) — step 4 failure, steps 5–13 skipped, production untouched at `8d41eee8`. Non-vacuous: explicit-human path promoted on the Human Director's D3 runs. Cousin family: SN-0079 (withheld certification is the gate working), SN-0061 (post-merge verification / negative proofs), SN-0063 (receipt provenance — binding a hash is not the subject deciding). Open leg: verdict-legibility path never fired live (MISSING EVIDENCE, not a bug); candidate repair held — protected workflow, director word required. H12 cycle sign-in 5960552278 / sign-out 5960593216. Receipt: `~/workspace/goals/nayapower-self-build-loop/hidden_files/h12-verification-2026-10-02.md`. GRAPH-10 8.5/10 unchanged.

## ⚙️ MACHINE NOTE

{"sn": "SN-0215", "title": "The Policy Cannot Self-Extend: Anti-Self-Reference in Promotion Gates", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-02", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "COMMITMENT-INTEGRITY"], "cousins": ["SN-0061", "SN-0063", "SN-0079"], "evidence": {"board": ["#554 5960552278 (H12 sign-in, 2026-10-02 20:05:35Z)", "#554 5960593216 (H12 sign-out, 2026-10-02 20:07:25Z)"], "run": "37051569993 (push @ 5b68f8dc, 12:03 PDT) — step 4 Enforce ratified standing policy failed, steps 5-13 skipped; production untouched at 8d41eee8", "workflow": "reread at pin 5b68f8dc, sha 05915637350a; evaluate_policy() in tools/standing_production_promotion_policy.py dd70b3566ceb re-reads expiry/status from the ratified policy doc itself; protected paths incl. .naya/governance/ DENY automatic promotion", "policy": "STANDING-PRODUCTION-PROMOTION-V1 v1.0.0 RATIFIED, in force through 2026-10-29", "non_vacuous": "explicit-human path promoted on Human Director's D3 runs"}, "status": "BEHAVIORALLY VERIFIED live; verdict-legibility leg = MISSING EVIDENCE (small), not a bug; candidate repair held for director word (protected workflow)", "rule": "a ratified promotion policy must authenticate its own terms from its own canonical record — never caller-supplied assertions — and protected paths (especially governance) must be structurally unpromotable without a human; the policy cannot self-extend on the automatic path"}
