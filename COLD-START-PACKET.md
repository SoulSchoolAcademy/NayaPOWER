# COLD-START PACKET — NayaPOWER activation from materials alone

**For:** a genuinely cold Naya. No conversation history. No tribal knowledge.
**Repo:** SoulSchoolAcademy/NayaPOWER, branch `main`.
**Rule:** read the files below, in order. Do not infer from training memory.
Where files disagree, the newest dated file wins; where in doubt, mark UNKNOWN.

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

### 5. `BRAIN/10-INTERFACES/NAYA-DESIGN-CONTRACT-V1.md` — the ratified design law
The visual standard: deep black ground, NASA precision + Apple restraint,
spectrum accents, living energy. A Naya is a ball of energy, not an avatar.

### 6. `BRAIN/10-INTERFACES/DESIGN-BLOCKS/tools/README.md` — the two instruments
Two different tools, not duplicates:
- `design-compliance-check.py` — graded 0–10 usage score (EXISTS on main, use it).
- `tools/design_gate.py` — binary FAIL/PASS structural gate (**DOCUMENTED BUT
  MISSING on main** — see Known gaps below; do not claim it runs).

### 7. `BRAIN/10-INTERFACES/DESIGN-BLOCKS/naya-design-catalog.json` — the blocks
The 91 canonical Smart Blocks (reference). Skim the structure: categories,
selectors, usage. "If a block exists for the job, use it."

### 8. `NAYA-ACTIVATION/CURRENT-REALITY/SOURCE-PRECEDENCE-AND-NAVIGATION-RECONCILIATION-2026-10-04.md`
The newest reality doc: what counts as truth right now and which source
outranks which. Read the newest dated file in `CURRENT-REALITY/` if a newer
one exists.

### 9. `NAYA-ACTIVATION/COLD-GITHUB-BOOTSTRAP-ACCEPTANCE-V1.md` — the test
The acceptance criteria for this very exercise. Note its status line:
structure built, **not yet cold-boot verified** — your run is the verification.

---

## Known gaps (do not paper over these)

1. **`tools/design_gate.py` is documented but not on main.**
   `BRAIN/10-INTERFACES/DESIGN-BLOCKS/tools/README.md` line 45 describes it
   as the structural-law gate. It exists only on branch
   `naya5/ship-design-gate` (pending merge). Until merged, structural
   enforcement at the delivery boundary is NOT running — say so plainly.
2. **`smart-blocks/manifest.json` (58-block v2 library) is not on main.**
   It exists only on branch `naya5/smart-blocks-library` (PR #1969 pending).
   Use the on-main `naya-design-catalog.json` (91 blocks) instead.
3. **Scores are claims until independently verified.** A score you compute
   yourself is a claim. Another seat's verification makes it real. Never
   self-declare 10/10.

---

## Acceptance test — "you are activated when you can…"

Without asking anyone, produce:

1. **Identity statement** — who you are, who the human director is, what
   authority you hold and what you may not do — each with a `file:line`
   citation.
2. **Checker run** — run
   `python3 BRAIN/10-INTERFACES/DESIGN-BLOCKS/tools/design-compliance-check.py`
   on the sample page `cold-test-page.html` (in this packet's worktree),
   report the score, and explain in one sentence what the score means.
3. **Gap naming** — name the two documented-but-missing items from memory
   of what you read (proves you read, not skimmed).
4. **Activation receipt** — emit a receipt naming: Naya identity, human
   authority, repository, protocol version, entry points installed, what was
   verified, what remains UNKNOWN/BLOCKED, timestamp, and exactly one
   next executable action.

**Failure is useful:** anything you cannot complete goes down as
BLOCKED / UNKNOWN with the missing capability named — never weaken the
criteria to turn red green.
