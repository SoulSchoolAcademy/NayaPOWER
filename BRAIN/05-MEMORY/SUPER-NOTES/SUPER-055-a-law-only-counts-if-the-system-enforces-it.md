# SUPER NOTE — A Law Only Counts If the System Enforces It

> **The essence layer: 71 distilled Super Notes.** Raw Smart Notes live in the archive; the Hub wall shows these essences. Nothing here deletes or replaces any raw note.

| Field | Value |
|---|---|
| Super Note ID | `SUPER-055` |
| Hub wall row | `public.hub_smart_notes` ib_id `SUPER-055` |
| Human title | A Law Only Counts If the System Enforces It |
| Layer | ESSENCE — distilled from raw Smart Notes, never a raw capture |
| Distilled | 2026-10-21 — corrective distillation drive (639 raw → 71 essences); REPAIRED 2026-10-21 after independent audit found 42 MISSING + 151 PARTIAL — lost lessons restored from the originals (see REPAIR-LOG); coverage map regenerated mechanically from these files |
| Sources | 5 raw notes (full list below) |
| Cluster file | `cluster-07-super.json` |
| Canonical machine object | Hub DB row `public.hub_smart_notes` + `distill/all-super-notes.json` |
| Human projection | This Markdown file |
| Sync note | NOT ingested by hub-sync (its watcher parses only `BRAIN/05-MEMORY/SMART-NOTES`); archive + queue untouched |

---

## ✦ IN A NUTSHELL

A rule written on paper but not built into the machine is just a suggestion. Real law lives in the system itself: it cannot be skipped, walked around, or quietly weakened — and when the machine says no, it's usually protecting you.

---

## 🩷 HUMAN NOTE

If a rule can be written into code, it must be enforced by the code — not left as advice each person may or may not follow. A guard that sits beside the path instead of on it stops nobody: a direct hand-edit can walk around beautiful machinery, and no audit will notice. A specification that nothing actually runs is decoration, not law; enforcement needs a real execution point. And when a safeguard blocks you — a database refusing a deletion, a tracker refusing a mismatch — read why before overriding. Twice in one deploy, those "failures" were the system saving production.

---

## 🟣 CHILD NOTE

A rule only works if the door actually locks. If anyone can just walk around the lock, it's not a real lock. And if the lock says "stop," check why — it might be keeping something precious safe.

---

## 👵 GRANDMA NOTE

It's like a good fence, dear. A sign saying "please stay out" is polite, but the fence is what protects the garden. Rules here are built in so they can't be forgotten or faked — and when something refuses to budge, it's often guarding something valuable.

---

## 🤖 NAYA NOTE

I build laws as unskippable state machines and gates that fail closed, where "no known violation" can never authorize an act. Capture must pass through the governed path — a published page without its registry entry is drift the ratchet will collect. I audit for consumers, not spec files: if nothing executes a law, I say so plainly. The amendment path is coded too — the ratification route is the only mutation route. When tooling blocks me, I read the reason first; safeguards are evidence, not obstacles.

---

## WHAT IT MEANS

The difference between governance and theater is the write path. Systems drift toward whatever is easiest; if the easy path bypasses the law, the law is fiction no matter how well it is written. Enforcement at the point of action, plus a coded way to legitimately change the law, is what makes rules survive contact with real work and real pressure.

---

## WHAT'S IN IT FOR YOU

You don't have to police anyone. The protections hold on their own — bad changes get stopped, good changes flow through the front door, and the rules you agreed to are the rules actually in force. When something does get blocked, you get a reason worth reading instead of silent damage.

---

## HOW IT APPLIES

For every rule, ask: where does the machine enforce this, and can anyone walk around that point? If yes, move the guard onto the path. Check that every machine-readable law has a real consumer that runs it. Route all capture through the governed path so registry and record grow together. When a safeguard fires, diagnose before overriding.

---

## ⟲ RESTORED BY REPAIR — 2026-10-21

> Restored by the distillation repair after the independent essence audit (distillation-audit-20261021) found the lessons below MISSING from, or only partially carried by, this Super Note. Each entry restores the named source note's own rule in checkable words, traced to that source. Nothing here is new doctrine.

### SN-0269 — Intelligent Block [audit: PARTIAL → lost element restored]

Evidence counters must physically not double-count one provenance root: the same `root_provenance` repeated never increments `independent_verifications` — `return`, don't increment. Code the rails, not the driver: gates and transitions are coded (sequence, gates, thresholds, unskippable transitions), while judgment inside them stays with the verifier — the machine enforces the shape of lawful behaviour, never the verdict inside.

### SN-0338 — The Registry Is the Law — Capture Must Pass the Governed Path, or the Merge Ratchet Will Collect [audit: PARTIAL → lost element restored]

Branch-head green is not merge-clean: classify the RED on the merge ref (e.g. `refs/pull/1229/merge`), on provably virgin state, before any repair — the branch head alone went pytest green (540 passed) while the merge ref failed 1/650. Never weaken the pinned baseline to cure drift: pinned stays 1; the repair is triage → register → relocate → drop → rebase → re-run, and gate-weakening is never on the menu. Deferral is a decision, not drift: when triage exceeds the lane, defer it explicitly — named, dated, owned, and recorded on the board with its repair path.

### SN-0631 — A Guard Off the Write Path Is a Suggestion, Not a Guard [audit: PARTIAL → lost element restored]

The closure test: no closure counts until the original attack is re-run on the exact new bytes and fails — after any "poisoning closure" PR, attempt the direct-edit attack on the new bytes and require a loud failure; if the audit still passes a hand edit, the PR shipped a suggestion. Authority must be bound to something upstream and trusted: `authority_is_valid()` checking only non-empty `promoter` + `scope` is not valid — a forged non-empty authority object otherwise passes — so non-empty ≠ valid, and authority binds upstream of the check.

## SOURCES (traceability — every raw note this essence was distilled from)

- `IB-SMART-NOTE-20260930-sn0269-law-as-code-enforced-operating-law`
- `IB-SMART-NOTE-20261006-sn0454-spec-without-consumer-is-doc-only-law`
- `IB-SMART-NOTE-20261005-sn0631-guard-off-write-path-is-suggestion`
- `IB-SMART-NOTE-20261005-sn0338-registry-is-the-law`
- `IB-SMART-NOTE-20261006-sn0477-production-deploy-two-saves`
