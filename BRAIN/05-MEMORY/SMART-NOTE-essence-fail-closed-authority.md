# SN-2154 — Fail Closed: No Write Path Mints Authority

**Status: VERIFIED ESSENCE — VERIFIED-WITH-CORRECTIONS (verifier-oct-2, block PASS); the itemized corrections were executed at landing and are asserted in the landing build.** Distilled from 10 raw notes by the oct-2 maker seat; independently verified by a different seat. Landing corrections (verifier-oct-2 item (b)): SN-0521's CV-07 restored as its own clause — evidence must be verified to be evidence; presence is not verification — and SN-0581's enforcing code paths named (tools/smart_note_v2.py, tools/truth_state_guard.py). Golden-red sections (Why it matters / How it connects / What is in it for you / The learning) completed at landing from the covered sources, per the Full Smart Note ruling. The raw notes in the coverage map below are RETIRED by this filing under SN-2081; this essence is their living form.

## Essence

Authority in NayaPOWER is earned through evidence and ratification, and the machinery is built so that no shortcut can counterfeit it. The capture write path is authority-blind: every ingested object enters at the lowest truth state (CANDIDATE) regardless of what its producer claims, truth-state transitions require independent ratification evidence enforced in code — the capture module and its guard, `tools/smart_note_v2.py` and `tools/truth_state_guard.py`, not convention — and any write path found able to set truth state is the top security hole in its pipeline — above everything else, because a sloppy or compromised writer poisons the whole corpus at its root (SN-0581). Direct jumps are refused mechanically: a RATIFIED predecessor guard makes trust-state leaps fail closed instead of landing (SN-0460). The structural-audit lesson bounds what shape-checking can do: an audit sees shape, not meaning, so elevation needs authority AND evidence checked at write time, not inferred later from a well-formed document (SN-0462).

Refusals themselves are governed. Rejection is a non-event: a refused write must not record itself, or the ledger fills with the ghosts of things that never lawfully existed (SN-0465). A gate ordered after the mutations it guards is a refusal that still writes — CV-06 names the class: the gate must sit before the first mutation, or its "denial" is theater over a completed write (SN-0521). CV-07 is the twin defect, and a different failure: the gate's evidence parameter is never verified to be evidence — caller-supplied `evidence_refs` checked only for non-emptiness let arbitrary strings ("not-a-verification", a forged "CVO-" id) promote a claim while the system reported ok:true, because presence is not verification; a promotion that claims to discharge a verification requirement it never checks contradicts its own text (SN-0521). Every denial must name its subclass — which gate, which condition, which authority — because an unnamed denial cannot be appealed, routed, or learned from (SN-0487). And a control that fails open and silent is worse than one that fails loud: a silent open failure converts a guard into an unmarked hole, while a loud failure at least announces the seam (SN-0468).

The numeric gates get the same adversarial treatment. Every comparison against NaN is False, so a range check like `v < 0 or v > 10` silently passes a NaN score — a fabricated scorecard with NaN scores walked straight through a merge gate's check; the standing doctrine is a two-part validation for every numeric gate on untrusted input: `math.isfinite(v)` first, then the range check, never the range check alone (SN-0579). The production boundary is drawn asymmetrically on purpose: reading at the production boundary is agent-movable for audit (the idempotency audit pattern), while writing is Director-gated (SN-0470). Exposure hides in defaults: a trigger function sitting in the public schema is an RPC endpoint by accident — placement is exposure, whether or not anyone intended to publish it (SN-0611).

## What this settles

- Truth state is never an input: writers propose, evidence and ratification dispose, and the enforcement lives in code, not convention (SN-0581, SN-0460).
- A gate's position and its failure mode are part of its correctness: gate-before-mutation and evidence verified, not merely present (SN-0521), refusal-leaves-no-record (SN-0465), named denial subclass (SN-0487), fail loud over fail silent-open (SN-0468).
- Numeric validation is always finiteness-then-range on untrusted input (SN-0579).
- Read/write asymmetry at the production boundary is deliberate design, not an inconsistency (SN-0470).

## Intelligence views

**Human:** Nobody can promote their own work into "official truth" just by saving it in the right place. New things arrive as drafts, and only real evidence, checked by the system itself, can raise them. When the system says no, it says no before anything changes, it says why, and it doesn't leave fake entries behind. Locks here fail shut, and they fail loudly.

**Child:** Imagine a clubhouse with a special stamp that means "this is really true." Nobody can just grab the stamp — you have to show proof, and a guard checks it. If the guard says no, nothing sneaky gets written down anyway. And the counting machine always checks that a number is a real number before it believes it.

**Grandma:** It's like a bank vault with honest clerks, dear. Anyone can hand in a paper, but it goes into the "unproven" tray no matter what the person claims. Only checked proof moves it up. If a request is refused, it's refused before any money moves, the reason is written plainly, and no false entry appears in the ledger. A lock that silently stops working is treated as worse than one that makes a noise — because at least then you know.

**Naya (AI):** Audit every pipeline you touch with one question first: can this writer mint authority (SN-0581)? Then check the four gate properties in order — position before mutation (SN-0521), refusal as non-event (SN-0465), named denial subclass (SN-0487), failure loud rather than open-silent (SN-0468). Validate every untrusted number with isfinite before range (SN-0579). Treat schema placement as exposure (SN-0611) and keep the read/write production boundary asymmetric (SN-0470). A structural pass never substitutes for authority-plus-evidence at write time (SN-0462).

**What it means:** Ten notes about guards, gates, denials, and boundaries are one teaching: authority is a property the system defends mechanically at the moment of writing, not a label it trusts afterward. A cold reader holding only this essence can still audit any new write path or gate and find the hole the way these notes found theirs.

## Why it matters

One write path that can mint authority poisons the whole corpus at its root: every later read, retrieval, and proof inherits the counterfeit as fact (SN-0581). The failures this cluster names are all cheap at the gate and ruinous downstream — a refusal that writes anyway (SN-0521), a refusal that records itself and fills the ledger with ghosts (SN-0465), a range check that silently passes a fabricated NaN score (SN-0579). Fail-closed discipline is what makes the memory safe to compound.

## How it connects

It is the write-time twin of Provenance Is Sacred: that essence governs what may be claimed at intake, this one the machinery that refuses to let a claim become authority. Its entry-state guard is the same code the identity watcher protects — SN-0581 names `tools/smart_note_v2.py` and `tools/truth_state_guard.py` — and its NaN doctrine (SN-0579) is the numeric face of the theater tests in The Instrument Must Execute. Within the Seven Essences it serves SN-2069 (E2, Proof Is Behavior, Not a Badge) and SN-2073 (E6, The Note System Itself).

## What is in it for you

A complete audit drill for any pipeline you touch. Ask first whether the writer can mint authority (SN-0581); then check the four gate properties in order — position before the first mutation, and evidence verified rather than merely present (SN-0521); refusal as a non-event (SN-0465); a named denial subclass on every refusal (SN-0487); failure loud rather than open and silent (SN-0468). Validate every untrusted number finiteness-then-range (SN-0579), and treat schema placement as exposure (SN-0611).

## The learning

The durable lesson is that authority is a property the system defends mechanically at the moment of writing, not a label it trusts afterward (SN-0581, SN-0460). The behavior that changes: a structural pass never substitutes for authority-plus-evidence checked at write time (SN-0462); a deny verdict is never accepted as proof the gate is sound until its ordering and its evidence check are read (SN-0521); and the read/write asymmetry at the production boundary is kept deliberate (SN-0470). What would falsify this essence's teaching is a covered note that lets a writer set truth state, or lets a range check stand alone on untrusted input — none does.

## Coverage map — raw notes this essence covers (10)

SN-0460 · SN-0462 · SN-0465 · SN-0468 · SN-0470 · SN-0487 · SN-0521 · SN-0579 · SN-0581 · SN-0611

## Verification contract (for the verifying seat — falsify these)

1. **Coverage integrity:** the coverage map lists exactly 10 IDs; each exists in the block manifest exactly once; no ID appears in any other oct-2 essence's coverage map or in the batch-1 covered list.
2. **Entry state:** SN-0581 states new notes ALWAYS enter as CANDIDATE and names the enforcing code (`tools/smart_note_v2.py`, `tools/truth_state_guard.py`) — verify both against the source page.
3. **Gate-after-mutations:** SN-0521 names the defect classes CV-06/CV-07 — verify the essence's claim traces to that note and that it requires the gate before the first mutation.
4. **NaN doctrine:** SN-0579's evidence is a fabricated scorecard passing a merge gate's step-2 check (board comment 6047695918, PR #1780) — verify the two-part check (isfinite, then range) matches the source.
5. **Boundary asymmetry:** SN-0470's rule is read agent-movable / write Director-gated — fail the draft if the essence presents the boundary as symmetric.
6. **No-orphan check:** pick any five sentences in the Essence section at random; each must cite at least one covered SN ID, and the cited page must contain the claim.