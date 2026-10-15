# Name the Authority on Every Install Point — Installable-in-Principle Is Not Installed

**Intelligent Block:** IB-SMART-NOTE-20261015-sn01382-name-the-authority-on-every-install-point
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 04:38 PDT smart-note-distillation tick (2026-10-15) from `hidden_files/twelve-lane-receipts/gap-lane-scorer-20261015-0340-lane8.md` (Naya Clarity Narzan, Lane 8 Sentinel hat, 2026-10-15 11:33–11:35 UTC) — the mirror lesson of an install that split across two authorities.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A repair proposal carried two install points: (1) a VOID-feed formatter to install in `hidden_files/bin/claim_liveness_audit.py`, and (2) a RECONCILE step in the dispatcher cron definition so every void lands a canonical line in the lane feed. The executing seat installed point (1) byte-verbatim — pre-edit pin `4dcee9f0…` re-derived, new SHA `faf6e3b3…`, detection-only behavior verified (`AUDIT-CLEAN`, exit 0), formatter 10/10 shapes + 2/2 refusal guards. Point (2) was BLOCKED by design: the cron definition file is a read-only copy of the saved schedule — an edit attempt was refused with "edits do not update the scheduled job," and the seat's standing body forbids touching any schedule but its own. So the seat shipped point (2) as exact ready-to-apply amendment text for the schedule owner, named the authority per point in the receipt, and scored 9.0/10 for the honest half-done.

The lesson: installability is authority-gated, not effort-gated. A proposal that lists install points without naming who can install each one is incomplete — the two points needed two different authorities, and naming the authority per point is part of the proposal, not an afterthought. "Installable in principle" is not installed.

## 🩷 HUMAN NOTE

Think of a home renovation with two jobs: repainting a wall (anyone can do it) and rewiring the fuse box (only the licensed electrician). The contractor painted the wall perfectly — then called the electrician with the exact wiring diagram instead of touching the fuse box himself. The renovation isn't half-failed; it was half-assigned from the start. A good plan names the electrician on the plan, not in the apology.

## 🟣 CHILD NOTE

Imagine a club's rule book has two pages to fix. One page is on the bulletin board — anyone can pin the new page. The other page is inside a locked box that only the club president can open. If you write the plan as "fix both pages" without saying who opens the box, the plan will fail. The smart plan says: "I pin page one; the president pins page two — here is the exact page for her."

## 🔵 GRANDMA NOTE

It's like a recipe that says "bake the cake, then call the plumber to fix the oven." The cake baker can't fix the oven — that's the plumber's job, and the recipe knows it. If the recipe only said "fix everything," the baker would waste a day with a wrench. Good instructions name who's allowed to touch what, before anyone starts.

## 🟠 NAYA NOTE

Apply this every time you write or execute a repair proposal with more than one install point: (1) split the proposal into its install points, one per procedure file or authority domain; (2) for each point, name the authority that can install it (any seat, the schedule owner, Shawn's word, a merge) — this naming is part of the proposal, not an afterthought; (3) install what your authority covers, byte-verified; (4) ship the rest as exact ready-to-apply text to the named authority — never attempt a write you are read-only for; (5) score the outcome against the whole proposal, not your half — half-done with the authority named is honest, half-done with the authority unnamed is a surprise.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "repair_proposal_without_per_point_authority",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261015-0340-lane8.md (Naya Clarity Narzan, Lane 8, 2026-10-15 11:33-11:35 UTC)",
    "parent": "hidden_files/twelve-lane-receipts/gap-scorer-20261014-2340-lane8.md (parent scored 9.4/10)",
    "point1_installed": "claim_liveness_audit.py pre-edit pin 4dcee9f0 re-derived; VOID_DESTINATIONS/VOID_REASONS/format_void_line() inserted verbatim; post-edit sha faf6e3b3; audit AUDIT-CLEAN exit 0; formatter canonical example byte-verbatim, 10/10 shapes, 2/2 refusal guards fire",
    "point2_blocked": "cron definition file is a read-only copy — edit attempt refused ('Cron definition files are read-only copies of saved schedules'); live step-2c text verified present at crons/minutely/night-dispatcher__interval@10m.md line 61, unmodified; shipped as ready-to-apply amendment text to the schedule owner",
    "score": "9.0/10 — honest half-done with the authority named"
  },
  "rule": "name_the_authority_on_every_install_point",
  "procedure": [
    "split every multi-point proposal into its install points, one per procedure file or authority domain",
    "name the authority that can install each point inside the proposal: any seat, the schedule owner, a protected-gate word, a merge",
    "install what your authority covers with byte verification; ship the rest as exact ready-to-apply text to the named authority",
    "never attempt a write you are read-only for; score the outcome against the whole proposal"
  ],
  "decision_change": "every future repair proposal with multiple install points must carry a per-point authority column before execution begins — a proposal without it is incomplete and will surprise the executor at install time",
  "falsifiability": "if an install point lands through a seat lacking its named authority (e.g., a cron step changed without the schedule owner) and the change persists, installability is not authority-gated and this rule is wrong",
  "mechanism": "procedure files are read-only to everyone but their owner; installability is a property of the authority graph, not of effort — a point whose owner is unnamed is a point whose install is undefined",
  "related": ["SN-1374 (a void kills the receipt, not the work)", "gap-t0402-lane7 recusal liveness (candidate 356, 2026-10-15)"]
}
~~~
