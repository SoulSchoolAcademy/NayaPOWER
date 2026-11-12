# SUPER NOTE — Permission Is Real, or It Is Nothing

> **The essence layer: 71 distilled Super Notes.** Raw Smart Notes live in the archive; the Hub wall shows these essences. Nothing here deletes or replaces any raw note.

| Field | Value |
|---|---|
| Super Note ID | `SUPER-001` |
| Hub wall row | `public.hub_smart_notes` ib_id `SUPER-001` |
| Human title | Permission Is Real, or It Is Nothing |
| Layer | ESSENCE — distilled from raw Smart Notes, never a raw capture |
| Distilled | 2026-10-21 — corrective distillation drive (639 raw → 71 essences); REPAIRED 2026-10-21 after independent audit found 42 MISSING + 151 PARTIAL — lost lessons restored from the originals (see REPAIR-LOG); coverage map regenerated mechanically from these files |
| Sources | 12 raw notes (full list below) |
| Cluster file | `cluster-01-super.json` |
| Canonical machine object | Hub DB row `public.hub_smart_notes` + `distill/all-super-notes.json` |
| Human projection | This Markdown file |
| Sync note | NOT ingested by hub-sync (its watcher parses only `BRAIN/05-MEMORY/SMART-NOTES`); archive + queue untouched |

---

## ✦ IN A NUTSHELL

A good score, a green light, a login, or a confident claim never gives anyone permission. Permission is real only when it traces back to an actual grant — the director's own words, a ratified law, or an active grant with clear limits. Anything else is just a claim wearing a costume.

---

## 🩷 HUMAN NOTE

Two jobs look alike but are not the same: deciding what should happen, and permitting who may do it. A scorecard, a test suite, a workflow identity, or a document declaring itself effective immediately can do the first job — never the second. Real permission has a root you can point to: the director said it (his exact words, written down with the time), a ratified law covers it, or a grant record exists that is active, in scope, and unexpired. If the same person who wants to act also declares themselves allowed, that is the defect — hold the work and escalate.

---

## 🟣 CHILD NOTE

Just because you wrote 'I am allowed' on a piece of paper doesn't mean you are allowed. Permission comes from the person in charge, or from a real rule everyone agreed on. You can't give yourself a permission slip — and you can't pretend to be the teacher who checks the work.

---

## 👵 GRANDMA NOTE

Dear, think of it like a house key. A key only counts if the homeowner actually gave it to you. Writing your name on a tag, or saying 'he wouldn't mind,' doesn't make it your key. And a note you wrote yourself saying 'I may come in' — that's not permission, that's just paper.

---

## 🤖 NAYA NOTE

On every action that needs authority, name the two jobs separately: who decides what should happen, and what permits it. Trace permission to its root before acting — the director's recorded word, ratified law, or an active scoped grant. Treat green checks, logins, self-declared grants, and self-written receipts as claims, not proof. Never impersonate a named verifier, never let a write path mint trust, and never let a policy stretch its own envelope. When a command is the grant, record it verbatim with its timestamp, and keep the still-gated items named.

---

## WHAT IT MEANS

Authority is the load-bearing wall of the whole system. If claims can quietly become permissions, every other safeguard becomes decoration — the gates still stand, but anyone can walk around them by typing the right words. Keeping deciding and permitting separate, and demanding a real root for every permission, is what makes trust in the system something earned rather than performed.

---

## WHAT'S IN IT FOR YOU

You never have to wonder whether something important was done by someone actually allowed to do it. Decisions that touched your money, your data, or your production system carry a permission you can inspect — who granted it, when, and for exactly what. That means fewer surprises, and a clear answer when you ask 'who said this was okay?'

---

## HOW IT APPLIES

Before any consequential act, ask three questions: What exactly is being permitted? Who granted it — and can I point to the record? Does the grant cover this action, at this scope, right now? If any answer is missing, stop and get the real grant; do not widen a matcher, invent a document, or proceed on a green light. When you receive a command, write it down word-for-word with the time before you act on it.

---

## ⟲ RESTORED BY REPAIR — 2026-10-21

> Restored by the distillation repair after the independent essence audit (distillation-audit-20261021) found the lessons below MISSING from, or only partially carried by, this Super Note. Each entry restores the named source note's own rule in checkable words, traced to that source. Nothing here is new doctrine.

### SN-0215 — The Policy Cannot Self-Extend: Anti-Self-Reference in Promotion Gates [audit: PARTIAL → lost element restored]

A ratified promotion policy must authenticate its own terms from its own canonical record — never caller-supplied assertions: `evaluate_policy()` (`tools/standing_production_promotion_policy.py`) re-reads expiry and status from the ratified policy document itself ("Ratification is not a license to rely on caller-supplied expiry assertions"). Protected paths, including `.naya/governance/` itself, always DENY automatic promotion — the policy cannot self-extend on the automatic path, and a governance document is structurally unable to rewrite its own rules without a human's explicit word.

### SN-0263 — The Ratification Receipt: Bounded Authorization, Recorded — the First Live Ritual [audit: PARTIAL → lost element restored]

Ratification is a ritual with a shape: (1) an exact authorization string from the Human Director that names the SHA being blessed; (2) independent verification of every claim BEFORE the authorization is executed; (3) a receipt that records BOTH what the ratification authorizes AND what it explicitly does NOT. Any future ratification must (a) cite an exact authorization string with SHA, (b) attach independent pre-verification of every claim, and (c) produce a receipt naming both what it authorizes and what it does NOT — or it is not a ratification. The distinction is preserved verbatim: `RATIFIED ≠ MERGED ≠ RUNTIME_ACTIVE ≠ BEHAVIORALLY_PROVEN ≠ PRODUCTION_PROVEN` — each is a separate gate with its own evidence class, and "it was ratified" must never silently purchase a merge, a deploy, or a lived-machine claim.

### SN-0362 — The Unkeyed Seal, Live: promote_note Elevates on a Self-Asserted String [audit: PARTIAL → lost element restored]

A hash binds content, never identity. `promote_note`'s receipt is an unkeyed seal: `receipt_hash` proves the receipt was not altered, and carries no proof of who promoted — no `authority`, no `promotion_authority`, no issuer, no grant id, not one field recording that the promoter was entitled to do this. Any promotion path that records WHAT and WHY but never proves WHO was entitled is an unkeyed seal; bind every promotion transition to an authenticated grant.

### SN-0368 — The Promoter Chooses the Evidence — A Passing Audit Attests to Internal Coherence, Not to Truth [audit: MISSING → restored in full]

An audit attests to internal coherence of the bundle it is given, never to truth. `verify_receipt` re-derives rather than trusting the seal — it re-runs the threshold gates instead of trusting the receipt — and that re-validation is the engineering bar. But re-validation re-derives against the evidence bundle supplied by the promoter under audit, so a PASS means internal coherence only. Proven by drill: invented gatherers `party-X` / `party-Y`, existing nowhere in the repo, PASS `gatherer_independence`, because `gatherer_independence` measures string diversity, not corroboration — never cite it as independent confirmation. The remaining gap is authenticating the evidence suppliers, not strengthening the seal. Every audit check that consumes attacker-chosen inputs without independent sourcing inherits the attacker's frame; the standing question for any future gate is: who supplies the evidence?

### SN-0464 — Name-Checking Is Not Entitlement-Checking [audit: PARTIAL → lost element restored]

A guard that verifies the promoter's name is non-blank proves a claim was recorded, not that the claimant was entitled to promote: `authority_is_valid` returning True for any non-empty string is authentication theater — it answers "did someone sign?" while the attack answers "was the signer allowed?" A fail-closed elevation guard must bind the named promoter against an entitlement source (authority-grant roster, scoped to the promotion) and fail closed when that binding is absent; "non-blank string" is never an entitlement proof.

### SN-0581 — IB-SMART-NOTE — SN-0581 — Write Paths Never Mint Authority [audit: PARTIAL → lost element restored]

The specific mechanism: new notes ALWAYS enter as CANDIDATE, regardless of what their producer claims, and truth-state changes require ratification evidence, enforced in code (`tools/smart_note_v2.py`, `tools/truth_state_guard.py`), not by convention. Every ingested object enters at the lowest truth state; truth-state transitions require independent evidence (ratification) and are enforced by a guard on the transition, not by the writer's honesty. Any write path found able to set truth state is a security hole.

## SOURCES (traceability — every raw note this essence was distilled from)

- `IB-SMART-NOTE-20260930-sn0223-workflow-binding-not-authorization`
- `IB-SMART-NOTE-20260930-sn0441-green-is-not-go`
- `IB-SMART-NOTE-20260930-sn0444-self-declared-grant-is-a-claim`
- `IB-SMART-NOTE-20260930-sn0464-name-check-vs-entitlement-check`
- `IB-SMART-NOTE-20260930-sn0565-scorecard-decides-never-authorizes`
- `IB-SMART-NOTE-20260930-sn0215-policy-cannot-self-extend`
- `IB-SMART-NOTE-20260930-sn0362-unkeyed-seal-promote-note-elevates-unauthenticated`
- `IB-SMART-NOTE-20261007-sn0538-director-command-is-the-grant-permission-slip-doctrine`
- `IB-SMART-NOTE-20261007-sn0581-write-paths-never-mint-authority`
- `IB-SMART-NOTE-20261006-sn0592-never-impersonate-the-verifier`
- `IB-SMART-NOTE-20261005-sn0368-promoter-chooses-the-evidence`
- `IB-SMART-NOTE-20261004-sn0263-ratification-receipt-bounded-authorization`
