# A Fix Proven on One Machine Is a Claim About That Machine — Re-Proof Divergence Starts at the Instrument

**Intelligent Block:** IB-SMART-NOTE-20261015-sn01394-fix-proven-one-machine-claim-about-that-machine
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/VERIFICATION/REVERIFICATION-DISCIPLINE
**Provenance:** Captured on the 06:38 PDT smart-note-distillation tick (2026-10-15) from board #2537 comments 6192288414 (wave-187 Compounder re-proof → L415 RE-OPENED) and 6192513048 ([Naya Judge] PULSE corroboration). Sibling of SN-1016 (verifier-environment false-red direction); this is the fix-proof non-transfer direction. Cousin of SN-1009 (name the scope of every delta claim).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The L415 claimability-gate fix was verified on the author's machine — exit 2 refused the Clarity seat, exit 0 allowed the Resolve seat — and declared adopted the same hour. Then a different machine's re-proof (wave-187 Compounder) found `hidden_files/bin/` missing and zero `claim-brief.*` files workspace-wide, and RE-OPENED the lesson. The Judge lane corroborated: on that machine, the prose-only constraint was still the live state. The fix was real where it was proven — and absent where it wasn't. The proof was environment-coupled: it bound the (code, environment) pair it ran in, and said nothing about any other machine.

The durable rule: **when a re-proof contradicts a fix, the first hypothesis is environment divergence — verify the instrument exists on the failing machine before declaring regression.** A verification verdict is a function of (code × environment); a fix proven in environment X is a claim about environment X. The diagnostic order is: (1) is the instrument present on the failing machine? (2) only then, does the content diverge? Skipping step 1 turns a missing tool into a phantom regression and wastes the next seat's hour. Sibling of SN-1016 — which captured the false-red direction (the verifier's own environment breaking the check); this captures the non-transfer direction (the fix's proof not surviving the move to another machine).

## 🩷 HUMAN NOTE

Shawn — we fixed something, proved it worked, and celebrated — then another machine checked and the fix wasn't there at all. The tool the fix depended on simply didn't exist on that machine. Nobody's proof was wrong; the proof just didn't travel. Lesson banked: when a re-check disagrees with a fix, first ask "does the tool even exist on that machine?" before asking "did the fix break?" — it saves the next seat from chasing a ghost.

## 🟣 CHILD NOTE

You prove your science experiment works in the school lab. Your friend tries it at home and it fails — because home doesn't have the special beaker. The experiment wasn't wrong; the beaker was missing. Before saying "the experiment is broken," check: does the other kitchen have the beaker?

## 🔵 GRANDMA NOTE

It's like a recipe that works in your kitchen but flops at your sister's — because her oven runs cold and she doesn't have the right pan. The recipe isn't broken; the kitchens differ. When the same recipe gives different results, first compare the kitchens, then blame the recipe.

## 🟠 NAYA NOTE

Apply this to every fix/re-proof pair: (1) pin the verification environment to the failure's environment — a proof run anywhere else is a claim about that place, not about the failure; (2) when re-proof contradicts a fix, run the instrument-presence check first (`claim-brief.*` files, `hidden_files/bin/`, whatever the fix's load-bearing tool is) — presence is step 1, content divergence is step 2; (3) if the instrument is absent on the failing machine, the verdict is "fix not installed here," not "fix regressed" — route to the install/authority lane, not the content lane; (4) if the instrument IS present and verdicts still diverge, this note's prescription is exhausted — escalate to content; (5) cross-link the family: SN-1016 (verifier-environment false reds), SN-1009 (name every claim's scope), SN-01385 (check the check's assumptions — the temporal cousin; this note is the spatial one).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "category": "SYSTEM-INTELLIGENCE/VERIFICATION/REVERIFICATION-DISCIPLINE",
  "sibling_notes": ["SN-1016 (verifier-environment false-red direction)", "SN-1009 (name the scope of every delta claim)", "SN-01385 (check the check's assumptions — temporal cousin)"],
  "evidence": {
    "fix_proof": "board #2537 comment 6192634799 (INTELLIGENT EVENT): L415 claimability gate verified exit 2 (refused, Clarity) / exit 0 (allowed, Resolve) on author machine — declared adopted",
    "reproof_divergence": "board #2537 comment 6192288414 (wave-187 Compounder): hidden_files/bin/ missing, zero claim-brief.* files workspace-wide → L415 RE-OPENED on re-proof machine",
    "corroboration": "board #2537 comment 6192513048 ([Naya Judge] PULSE): defect L415 names (prose-only eligibility) is the live state on that machine; gate's own falsifier cannot fire without the instrument"
  },
  "rule": "re-proof contradicting a fix → first hypothesis is environment divergence: verify instrument presence on the failing machine before declaring regression",
  "decision_change": "re-proof protocol starts with instrument-presence on the failing machine; absence routes to install/authority lane, not content lane",
  "falsifier": "instrument present on the failing machine and verdicts still diverge — prescription exhausted, escalate to content divergence",
  "mechanism": "a verification verdict is f(code, environment); a proof binds only the (code, environment) pair it ran in — environment-coupled instruments do not transfer proof across machines"
}
~~~
