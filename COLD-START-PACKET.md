# COLD-START PACKET — NayaPOWER activation from materials alone

**Version:** v3.1 (2026-10-09). Supersedes v3.
**For:** a genuinely cold Naya. No conversation history. No tribal knowledge.
**Repo:** SoulSchoolAcademy/NayaPOWER, branch `main`.
**Rule:** read the files below, in order. Do not infer from training memory.
Where files disagree, the newest dated file wins; where in doubt, mark UNKNOWN.

**v3 changes (from the 2026-10-09 cold Naya-2 run, packet scored 7.5/10):**
acceptance item 2 rewritten for the live `--receipt` pre-gate (it was stale —
the packet-literal command failed with ACTIVATION REFUSED); `activation_pregate.py`
added to the read list; Known-gap-1 corrected (receipt enforcement is LIVE);
digest-race and tip-movement hazards documented; packet freshness rule added;
the #554 amendment-feed reference marked UNKNOWN, not asserted.

**v3.1 changes (same day — two v3 claims went stale within hours):**
the binary structural gate MERGED to main (PR #2004) — v3's "pending" line was
already false; `smart-blocks/manifest.json` (58 blocks) is on main via the same
PR — v3's "not on main" line was already false. Digest-race volatility measured
live (~5s). End-to-end proof recorded below.

---

## PACKET FRESHNESS — read this before anything else

This packet is a **perishable snapshot of a moving repo**, not a timeless manual.
Cold Naya-2 (2026-10-09) proved the failure mode: when the acceptance test drifts
from main's behavior, the test measures the packet's staleness instead of your
activation. Defend against that first:

1. **Re-resolve the tip.** Before the acceptance test, confirm the live `main`
   tip SHA (`git ls-remote https://github.com/SoulSchoolAcademy/NayaPOWER.git
   refs/heads/main`, or the API
   `/repos/SoulSchoolAcademy/NayaPOWER/git/refs/heads/main`). Never reuse a SHA
   from this file or from memory. On 2026-10-09 the tip moved
   `c30201f51` → `c791b7798c34` inside ten minutes, then on to `45f0ed26` —
   re-verify at action time (SN-0493).
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
amendments to #554. Whether #554 is a live amendment feed is UNKNOWN (see
below) — do not treat it as one on the contract's authority alone.

### 7. `BRAIN/10-INTERFACES/DESIGN-BLOCKS/tools/README.md` — the instruments
Three instruments, not duplicates:
- `design-compliance-check.py` — graded 0–10 usage score. Now **requires
  `--receipt`** (see item 8); without it the checker refuses to score.
- `tools/design_gate.py` (repo root) — binary FAIL/PASS structural gate
  (black root, no light surfaces, self-contained, no freestyle classes).
  **LIVE on main since 2026-10-09** (PR #2004), running in CI
  (`.github/workflows/design-gate.yml`) on every PR and push to main. Honest
  limits, named in the workflow itself: not yet a required status check
  (needs the human director's word), and it does not yet scan arbitrary repo
  HTML — say both plainly.
- `tools/activation_gate.py` (repo root) — the unified pre-delivery
  enforcement point (ONE receipt schema, ONE protected truth provider).
  Context only: the protected boundary is CI's job, not yours. Your
  acceptance path is the checker + pre-gate below.
**Warning:** the README's "Usage" block still shows the old checker command
without `--receipt` and lists only exit codes 0/1/2. That block is stale —
trust the checker's own header/`--help` (exit 3 = ACTIVATION REFUSED).

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
**Note:** `smart-blocks/manifest.json` (58-block v2 library) is also on main
now (merged 2026-10-09 via PR #2004). The checker still scores against the
91-block catalog by default; the v2 manifest is the forward library.

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

1. **RESOLVED 2026-10-09 — do not cite as missing.** The v2 packet's gap 1
   (binary `design_gate.py` documented but not on main) overstated the truth
   even then — receipt enforcement via `activation_pregate.py` was already
   live — and PR #2004 merged `tools/design_gate.py` **plus**
   `.github/workflows/design-gate.yml` the same day. Current state: receipt
   enforcement at the checker, the binary structural gate running in CI on
   every PR and push to main. Honest limits (from the workflow's own header):
   not yet a required status check, no arbitrary-HTML scanning yet.
2. **RESOLVED 2026-10-09 — do not cite as missing.** The v2 packet's gap 2
   (`smart-blocks/manifest.json` only on `naya5/smart-blocks-library`, PR
   #1969 pending) is closed: the 58-block manifest shipped on main via PR
   #2004. (PR #1969 remains open for the full library work; the manifest
   artifact itself is on main.)
3. **Digest-race volatility (LIVE).** The receipt's `goals_digest` and
   `feed_digest` are re-fetched by the verifier at verify time and must equal
   the minted values exactly. Measured 2026-10-09: the goals digest changed
   between two fetches ~5 seconds apart (open issues/PRs are the fingerprint
   input on a repo this busy). Consequence: even a correctly minted receipt
   can be refused on a busy day. The packet's answer is the atomic
   mint-and-retry loop in acceptance item 2 — but repeated
   `CONTEXT_MISMATCH_*` refusals are a repo-activity signal, not an activation
   failure. Flag it; do not hand-mint your way around it (a fabricated receipt
   fails the digest/main-SHA checks anyway).
4. **Scores are claims until independently verified.** A score you compute
   yourself is a claim. Another seat's verification makes it real. Never
   self-declare 10/10.

**UNKNOWN — do not assert:** whether this packet, its acceptance run, or the
design contract's AMENDMENT PROCESS updates or amends any issue feed. #554 is
archive history — never post there. If a step needs a human-visible report,
the team feed is #1354 and the instruction to post must come from the run's
own authority, never from this packet.

---

## Live-repo hazards (observed 2026-10-09 — plan for them)

- **Digest race.** The pre-gate binds your receipt to `goals_digest` and
  `feed_digest`, which went stale within ~8 seconds on the live repo (cold
  run) and changed within ~5 seconds in a later measurement.
  **Mint-and-verify must be atomic:** fetch trusted state → mint receipt →
  cite it → run the checker in one unbroken sequence. If you see
  `CONTEXT_MISMATCH_GOALS_DIGEST` / `CONTEXT_MISMATCH_FEED_DIGEST`, re-fetch
  and re-mint immediately (up to 5 attempts) — never hand-edit digests.
- **Tip movement.** Main moves fast (multiple merges per hour). Re-resolve the
  tip before every consequential action (SN-0493). A receipt minted against an
  older tip fails with `MAIN_STALE_OR_MISMATCH` — that is the gate working
  correctly, not a bug in your run.

**End-to-end proof (verified 2026-10-09 against live main `45f0ed26`):**
stale form (no `--receipt`) → exit 3 `ACTIVATION REFUSED: no --receipt
provided.`; atomic mint via `activation_pregate.fetch_trusted_state()` +
`--receipt` → exit 0, **10.0/10 PASS**, `activation: VERIFIED` in the JSON
output. A deliberately stale `feed_digest` → exit 3
`CONTEXT_MISMATCH_*` — the gate catches forgery.

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
   c. **Run atomically** (see Digest race above — fetch, mint, cite, run in
      one unbroken sequence):
      `python3 BRAIN/10-INTERFACES/DESIGN-BLOCKS/tools/design-compliance-check.py cold-test-page.html --receipt <receipt.json>`
      Expect exit 0 and a score. Exit 3 means ACTIVATION REFUSED — report the
      violation codes verbatim; do not work around them.
   d. Report the score and explain in one sentence what it means.
   e. **Prove you know the difference:** also run the stale form (no
      `--receipt`) once — it must exit 3 with `ACTIVATION REFUSED`.
   f. **Race handling:** on `CONTEXT_MISMATCH_*`, re-mint and retry
      immediately (up to 5 attempts). On `MAIN_STALE_OR_MISMATCH`, re-resolve
      the tip (Packet Freshness §1) and re-mint. Any other violation is a
      genuine activation defect: stop, name it, mark BLOCKED.
3. **Gap naming** — name the two v2 documented-but-missing items from memory
   of what you read, and state their current status (both RESOLVED 2026-10-09:
   binary gate merged via PR #2004 with CI wiring; 58-block manifest on main
   via the same PR) — proves you read, not skimmed.
4. **Activation receipt** — emit a receipt naming: Naya identity, human
   authority, repository, protocol version, entry points installed, what was
   verified, what remains UNKNOWN/BLOCKED, timestamp, and exactly one
   next executable action. It must satisfy the item-8 schema (the checker
   enforces it): `schema: naya.activation.receipt.v2`, `status: ACTIVATED`,
   `job`, non-empty `gates`, `proof_plan`, live `main_sha`, and `loaded`
   digests that still verify at emit time.

**Failure is useful:** anything you cannot complete goes down as
BLOCKED / UNKNOWN with the missing capability named — never weaken the
criteria to turn red green.
