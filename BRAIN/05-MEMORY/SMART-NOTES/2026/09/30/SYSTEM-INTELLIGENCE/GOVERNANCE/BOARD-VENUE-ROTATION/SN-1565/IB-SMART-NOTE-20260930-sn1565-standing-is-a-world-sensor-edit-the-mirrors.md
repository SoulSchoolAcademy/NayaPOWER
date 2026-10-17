# Standing Is a World-Sensor: Edit the Mirrors When the World Moves

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1565-standing-is-a-world-sensor-edit-the-mirrors
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A machine-owned STANDING section that mirrors world state is a world-sensor, not a static plaque. When the board moved from #2641 to #2721, the gates' own STANDING still said live_board=2641 — every downstream reader inherited a dead world. The migration procedure must edit the mirrors; a grep for the old value across machine-owned STANDING sections is the completion check.

## 🩷 HUMAN NOTE

Think of a STANDING section as a dashboard gauge: it is supposed to show the current world. When the team moved its live board from issue #2641 to issue #2721, the migration updated the shared state — but the gates' own STANDING blocks still read live_board=2641. Any machine that trusted the STANDING section was now operating in a world that no longer existed: reading the old board, posting to the old venue, reconciling against dead numbers. The boot-pointer repair in PR #2728 caught it. The fix is procedural, not clever: the board-migration checklist must include editing every machine-owned STANDING mirror, and the migration is not complete until a grep for the old board number across those sections returns zero hits. A plaque you hang once; a sensor you recalibrate every time the world moves.

## 🟣 CHILD NOTE

If your sign says "we meet at the old playground" after everyone moved to the new one, nobody finds you. Change the sign the same day you move.

## 🔵 GRANDMA NOTE

Machines keep little cards that say how the world is. When the world changes — a new meeting place, a new number — someone has to rewrite those cards, or the machines keep living in the old world. Make rewriting the cards part of the moving checklist.

## 🟠 NAYA NOTE

STANDING is read as authoritative world state by every downstream machine. A stale mirror is not a cosmetic defect — it is a fork of reality: each reader proceeds on the old world with full confidence. The migration is the only moment the world-move is known to the mover, so the mirror edit must be pinned to the migration procedure itself, not left as follow-up hygiene. The grep is the enforcement: the old value must be unfindable in machine-owned STANDING when the migration closes.

## 🟢 MACHINE NOTE

~~~json
{
  "applies_when": ["migration", "standing", "board", "world-move", "config-rot", "venue"],
  "canonical_object": "INTELLIGENT_BLOCK",
  "automatic_truth_ceiling": "CANDIDATE",
  "enforcement": "The board-migration procedure greps machine-owned STANDING sections for the old board number (and any other moved world values); the migration is not marked complete until the grep returns zero hits. A migration closeout with surviving old-value mirrors is bounced.",
  "evidence": "lesson-broadcast.md t0660 (2026-10-17 ~14:00 UTC): the boot-pointer gate repair found the gates' own STANDING still said live_board=2641 after the move to #2721. Receipt distill-daily-20261017 (Naya Clarity Narzan); PR #2728 boot-pointer fix.",
  "falsifier": "A migration where every machine-owned STANDING mirror is verified correct at closeout and no downstream reader consumed stale state — the check is then a no-op, not a failure. Out of scope: STANDING values that are design constants rather than world mirrors.",
  "mechanism": "Machines read STANDING as authoritative world state. A mirror that is not edited on a world move keeps serving the old world with full authority, so every downstream read inherits the stale world silently. The migration is the only moment the mover knows the world moved, so the mirror edit must be a pinned migration step; the grep makes staleness mechanically detectable.",
  "names_decision_changed": "The board-migration procedure's closeout checklist: add 'edit STANDING mirrors' as a required step with the zero-hit grep as its proof. Future venue/world moves route their STANDING edits through this step instead of discovering the rot later."
}
~~~

## 🟢 LEARNING LESSON

A STANDING section that mirrors the world is a sensor, not a plaque: recalibrate it on every world move, and prove the recalibration with a grep.

## 🟡 WHAT IT MEANS

World-moves (board migrations, venue changes, contract moves) are only as complete as their mirrors. The migration isn't done when the new venue is live — it's done when nothing machine-readable still points at the old one.

## ⚪ WHAT'S IN IT FOR YOU

No more machines operating on a dead world after a migration: no stale board reads, no phantom reconciliations, no archaeology to find which STANDING lied.

## 🟨 HOW TO APPLY / HOW TO USE

1. When a world value moves (board number, venue, contract address), list every machine-owned STANDING section that mirrors it.
2. Edit each mirror as a pinned step of the migration — not as follow-up.
3. Grep the old value across machine-owned STANDING sections; zero hits = migration complete.
4. Distinguish mirrors from constants: design constants don't move; mirrors do.

## 🔗 HOW IT CONNECTS

- **REFINES** → SN-01555 — board-rollover-before-the-cap (the migration itself; this note is the migration's mirror-edit step)
- **COUSIN** → SN-01220 — sealed-verdict-expires-when-world-changes (world-moves invalidate cached truth)
- **COUSIN** → SN-01416 — venue-rotation-verifies-override-on-evidence (migration verification discipline)

## 🧭 KEY DECISIONS / PRINCIPLES

- A mirror is a sensor: it must be recalibrated when the world moves.
- The migration procedure owns the mirror edit — never follow-up hygiene.
- The grep is the proof: old value unfindable = migration complete.

## 🟾 PROOF / PROVENANCE

~~~json
{
  "event": "board migration #2641 -> #2721 (2026-10-17)",
  "found": "gates' STANDING still said live_board=2641 after the move",
  "fixed_in": "PR #2728 (distill-daily boot-pointer fix)",
  "receipt": "distill-daily-20261017 (Naya Clarity Narzan)",
  "logged": "lesson-broadcast.md t0660, 2026-10-17 ~14:00 UTC"
}
~~~

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

Applies to STANDING values that mirror world state. Design constants (thresholds, band edges, law text) are not mirrors and don't move with the world. The grep covers machine-owned STANDING sections; human-facing docs are out of scope for the gate (nice to fix, not required).

## ➜ NEXT ACTION / SUCCESS CONDITION

Add the mirror-edit + zero-hit grep as a required step in the board-migration procedure, so the next venue move recalibrates its sensors by construction.
