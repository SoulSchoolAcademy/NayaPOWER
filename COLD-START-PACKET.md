# COLD-START PACKET — NayaPOWER activation from materials alone

**Version:** v3 (2026-10-09). Supersedes v2.
**For:** a genuinely cold Naya. No conversation history. No tribal knowledge.
**Repo:** SoulSchoolAcademy/NayaPOWER, branch `main`.
**Rule:** read the files below, in order. Do not infer from training memory.
Where files disagree, the newest dated file wins; where in doubt, mark UNKNOWN.

**v3 changes (from the 2026-10-09 cold Naya-2 run, packet scored 7.5/10):**
acceptance item 2 rewritten for the live `--receipt` pre-gate (it was stale —
the packet-literal command failed with ACTIVATION REFUSED); `activation_pregate.py`
added to the read list; Known-gap-1 corrected (receipt enforcement is LIVE, only
the binary structural gate is pending); digest-race and tip-movement hazards
documented; packet freshness rule added; the #554 amendment-feed reference
resolved as stale.

---

## PACKET FRESHNESS — read this before anything else

This packet is a **perishable snapshot of a moving repo**, not a timeless manual.
Cold Naya-2 (2026-10-09) proved the failure mode: when the acceptance test drifts
from main's behavior, the test measures the packet's staleness instead of your
activation. Defend against that first:

1. **Re-resolve the tip.** Before the acceptance test, confirm the live `main`
   tip SHA. If it moved since this packet was written, re-check every path and
   command below against the live tree — paths move, flags change.
2. **Check for a newer packet.** Look in `NAYA-ACTIVATION/` for a newer
   `COLD-START-PACKET` version. Newest wins, including over this file.
3. **Stale packet, not stale Naya.** If acceptance item 2 fails with
   ACTIVATION REFUSED on a receipt you minted honestly seconds ago, suspect the
   *packet* before suspecting yourself: verify `activation_pregate.py` still
   exists at its documented path and the checker's CLI flags haven't changed.
   Report packet staleness as a finding — that IS useful evidence.

---

## Read in this order

### 1. `AGENTS.md` — who you are and how you decide
The boot contract. Identity, the human director's authority, the Prime Judgment
Law, the decision math (objective → evidence → effect → risk → authority → act),
and the handoff format. Read all of it; it governs everything after.

### 2. `NAYA-ACTIVATION/00-ACTIVATION-KIT-MAP-V1.md` — the map
46 lines. What the activation package contains and where each piece lives.
Read this before wandering the tree.

### 3. `NAYA-ACTIVATION/PORTABLE-ACTIVATION-PROTOCOL-V1.md` — the ritual
How activation works: tune in (read the laws fresh, never from memory),
name the job, name the gates, name the proof. Then work.

### 4. `NAYA-ACTIVATION/SMART-NOTE-OPERATING-CONTRACT-V1.md` — your capture duty
Intelligence capture is identity, not assignment. Every conversation and feed
is a capture surface; capture and share without being told.

### 5. `NAYA-ACTIVATION/PORTABLE-ACTIVATION-MANIFEST-V1.json` — the machine manifest
The machine-readable package inventory: required human inputs, package
structure, entry points. (Omitted from packet v1 by mistake — the cold run
caught it. AGENTS.md step 4 and the 2026-10-04 reality doc both require it.)

### 6. `BRAIN/10-INTERFACES/NAYA-DESIGN-CONTRACT-V1.md` — the ratified design law
The visual standard: deep black ground, NASA precision + Apple restraint,
spectrum accents, living energy. A Naya is a ball of energy, not an avatar.
**Identity note:** line 3 states "Ratified: 2026-10-03 by Shawn Vibert
(Human Director)" — this is the explicit answer to "who is the human
director" in the acceptance test. Cite it.
**Stale line warning:** the AMENDMENT PROCESS section says to post contract
amendments to #554. That reference is stale — see "Resolved: #554" below.
Do not treat #554 as a live amendment feed.

### 7. `BRAIN/10-INTERFACES/DESIGN-BLOCKS/tools/README.md` — the instruments
Read the tool contracts here. Note the split: the compliance checker grades
usage 0–10; the structural gate is binary FAIL/PASS. The checker now enforces
activation itself (see item 8) — it will not score without a receipt.

### 8. `BRAIN/10-INTERFACES/DESIGN-BLOCKS/tools/activation_pregate.py` — the live pre-gate
**This is the enforcement you must satisfy.** Naya 3's activation receipt
consistency logic, live on main: the checker calls `gate_or_refuse()` before
scoring anything. Read the violation codes at the top of the file — they are
the exact failure modes your receipt must avoid (RECEIPT_MISSING,
MAIN_STALE_OR_MISMATCH, REPOSITORY_MISMATCH, ACTIVATION_EXPIRED,
DELIVERABLE_RECEIPT_CITATION_MISSING, CONTEXT_MISMATCH_*).
Key rules the code enforces: trusted state (main SHA, blob SHAs, digests) is
fetched from the **live GitHub API by the gate itself, never from you**;
receipts expire after **4 hours**; the deliverable must cite the receipt's
exact SHA256 (`<!-- NAYA-ACTIVATION-RECEIPT-SHA256:<64hex> -->`).

### 9. `BRAIN/10-INTERFACES/DESIGN-BLOCKS/naya-design-catalog.json` — the blocks
The 91 canonical Smart Blocks (reference). Skim the structure: categories,
selectors, usage. "If a block exists for the job, use it."

### 10. `NAYA-ACTIVATION/CURRENT-REALITY/SOURCE-PRECEDENCE-AND-NAVIGATION-RECONCILIATION-2026-10-04.md`
The newest reality doc: what counts as truth right now and which source
outranks which. Read the newest dated file in `CURRENT-REALITY/` if a newer
one exists.
**Warning:** `AGENTS.md`'s "SOURCE OF TRUTH" section hardcodes the 2026-09-29
reconciliation file, but the 2026-10-04 doc declares the 09-28/09-29 files
SUPERSEDED HISTORY. Newest wins — the packet rule overrules the stale
hardcoded path. (Repo bug, flagged; do not follow the stale path.)

### 11. `NAYA-ACTIVATION/COLD-GITHUB-BOOTSTRAP-ACCEPTANCE-V1.md` — the test
The acceptance criteria for this very exercise. Note its status line:
structure built, **not yet cold-boot verified** — your run is the verification.

**Cross-check:** the 2026-10-04 reality doc contains its own 11-step
"Cold-Naya navigation" — compare it against this packet's order. They
converge independently; where they differ, prefer the reality doc's order
for current-state claims.

---

## Known gaps (do not paper over these)

1. **Activation receipt enforcement is LIVE; the binary structural gate is not.**
   Distinguish the two — the v2 packet overstated this gap:
   - **LIVE:** the checker's pre-gate (`activation_pregate.py`) REFUSES to
     score without a valid, current receipt (exit 3, ACTIVATION REFUSED).
     The unified gate `tools/activation_gate.py` (one v2 receipt schema, one
     protected truth provider) is also on main.
   - **PENDING:** the binary structural gate `tools/design_gate.py`
     (documented in `DESIGN-BLOCKS/tools/README.md`) exists only on branch
     `naya5/ship-design-gate`. Until merged, binary structural enforcement
     at the delivery boundary is NOT running — say so plainly.
2. **`smart-blocks/manifest.json` (58-block v2 library) is not on main.**
   It exists only on branch `naya5/smart-blocks-library` (PR #1969 pending).
   Use the on-main `naya-design-catalog.json` (91 blocks) instead.
3. **Scores are claims until independently verified.** A score you compute
   yourself is a claim. Another seat's verification makes it real. Never
   self-declare 10/10.

## Resolved: #554 is not an amendment feed

The design contract (v1.0, AMENDMENT PROCESS) says to post contract amendments
to #554. Verified against current conventions (2026-10-09): #554 is the
Naya ↔ Coda direct communication board, **silent since 2026-09-23** — a dormant
coordination surface, not a live amendment feed. Treat the contract's #554
instruction as **STALE**. Current convention: coordinate design amendments on
the live team feed #1354, and flag the stale line to the design owner. Do not
assume #554; do not post amendments there on the contract's authority alone.

## Live-repo hazards (observed 2026-10-09 — plan for them)

- **Digest race.** The pre-gate binds your receipt to `goals_digest` and
  `feed_digest`, which went stale within ~8 seconds on the live repo.
  **Mint-and-verify must be atomic:** fetch trusted state → mint receipt →
  run the checker in one unbroken sequence. If you see
  `CONTEXT_MISMATCH_GOALS_DIGEST` / `CONTEXT_MISMATCH_FEED_DIGEST`, re-fetch
  and re-mint immediately — never hand-edit digests.
- **Tip movement.** Main moves fast (multiple merges per hour). Re-resolve the
  tip before every consequential action (SN-0493). A receipt minted against an
  older tip fails with `MAIN_STALE_OR_MISMATCH` — that is the gate working
  correctly, not a bug in your run.

---

## Acceptance test — "you are activated when you can…"

Without asking anyone, produce:

1. **Identity statement** — who you are, who the human director is, what
   authority you hold and what you may not do — each with a `file:line`
   citation.
2. **Checker run with activation** — the checker enforces activation first:
   a. **Mint a receipt** per the `naya.activation.receipt.v2` schema
      (template: `NAYA-ACTIVATION/ACTIVATION-RECEIPT-V2.json`). Fetch the
      trusted state LIVE — main SHA, `design_blob`, `blocks_blob`,
      `goals_digest`, `feed_digest` — via
      `activation_pregate.py::fetch_trusted_state()` (public GitHub API, no
      auth needed). Set `activated_at` to now (UTC); receipts expire after
      4 hours. Never invent these values — they must match live state or the
      gate will refuse, correctly.
   b. **Cite it in the deliverable.** Compute SHA256 over the receipt's exact
      bytes (`json.dumps(receipt, sort_keys=True)`) and embed
      `<!-- NAYA-ACTIVATION-RECEIPT-SHA256:<64hex> -->` in
      `cold-test-page.html` (work on a copy — do not modify packet files).
   c. **Run atomically** (see Digest race above — fetch, mint, and run in one
      unbroken sequence):
      `python3 BRAIN/10-INTERFACES/DESIGN-BLOCKS/tools/design-compliance-check.py cold-test-page.html --receipt <receipt.json>`
      Expect exit 0 and a score. Exit 3 means ACTIVATION REFUSED — report the
      violation codes verbatim; do not work around them.
   d. Report the score and explain in one sentence what it means.
3. **Gap naming** — name the pending-vs-live enforcement split from memory
   of what you read (proves you read, not skimmed): which enforcement is
   live on main, and which binary gate is still only on its branch.
4. **Activation receipt** — emit a receipt naming: Naya identity, human
   authority, repository, protocol version, entry points installed, what was
   verified, what remains UNKNOWN/BLOCKED, timestamp, and exactly one
   next executable action.

**Failure is useful:** anything you cannot complete goes down as
BLOCKED / UNKNOWN with the missing capability named — never weaken the
criteria to turn red green.
