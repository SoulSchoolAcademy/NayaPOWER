# COLD-START PACKET — NayaPOWER activation from materials alone

**Version:** v3.5 (2026-10-09). Supersedes v3.4. **Status: candidate on the
branch tip — NOT on `main`** (the v3.4 "Now on `main`" headline was false;
see the v3.5 status correction below).
**For:** a genuinely cold Naya. No conversation history. No tribal knowledge.
**Repo:** SoulSchoolAcademy/NayaPOWER. This file lives at the tip of branch
`naya5/successor-ingest-r1r2-polish` (it 404s on live `main` — the branch
was never merged).
**Rule:** read the 11 files below, in order. Do not infer from training memory.
Where files disagree, the newest dated file wins; where in doubt, mark UNKNOWN.

**v3.5 status correction (2026-10-09 — the independent cold retest refused
R1-4 over the false headline):** the retester verified the machinery
end-to-end — activation 10.0/10 from the packet alone, R2-2 met (4/4
eligible lessons retrieved with seam-stamped provenance, NAYA-NODE-0001
honestly refused), fail-closed proven (exit 3 `STORE_UNREACHABLE`),
freshness proven both directions — but **refused R1-4 as literally
specified**, because the criterion requires the kit ON main and this packet
404s there. The branch-tip truth: the packet and the whole kit
(`tools/successor_ingest/` with the portable `read.py` + `retrieve.py` +
`COLD-RETRIEVAL.md`, this pin + the freshness tool, the AGENTS.md step-13
link) live at the tip of `naya5/successor-ingest-r1r2-polish` (built on
`naya5/successor-ingest-r1r2` @ `92dc707a`). The kit is **PR-ready**.
Landing = Naya 4 opens the PR (Naya 5's PAT 403s on PR ops — the standing
lane rule is Naya 5 pushes branches, Naya 4 opens PRs), team consensus on
the #1354 feed, merge — and then a later seat runs the literal R1-4 re-run
against `main`. This packet invents no merge and fakes no landing. The
v3.4 pin receipt (`COLD-START-PACKET.pin.json`) is unchanged except
`packet_version` moving to v3.5 — the 7 enforcement files' sha256 are
byte-identical at this branch tip to the pin (re-verified 2026-10-09).
Everything the v3.4 design intended about landing at the repo root still
stands as the merge target; what changed is the status language, because
the status is what was false.

**v3.4 changes (2026-10-09 — the E1 standing trigger fired again: live main
moved past the v3.3 pin `dad16076`, and 1 of the 7 enforcement files changed
with real semantic drift):**
- **Landed on main — v3.5 STATUS CORRECTION: NOT landed.** The v3.4 intent
  was the design goal, but the merge never happened: this packet is
  `COLD-START-PACKET.md` at the tip of branch
  `naya5/successor-ingest-r1r2-polish`, and it 404s on live `main`. A cold
  agent arriving via main does NOT find the kit today. The design intent
  below (packet at the repo root, acceptance running from main's files at
  the pinned tip — the branch-tip files are byte-identical to the pin, so
  acceptance runs identically from the branch tip meanwhile) remains the
  merge target; landing happens via the PR lane, not by assertion.
  Vendoring is retired:
  the v3.2 lesson ("a packet whose acceptance test needs live-main files
  isn't a cold-start packet") is satisfied as far as files go because the
  acceptance test runs from main's files at the pinned tip below — and this
  branch tip's enforcement files are byte-identical to the pin (verified at
  v3.5 build) — the same property the branch vendoring provided, with no
  duplicate copies. What the v3.4 text got wrong was the *landing*, not the
  files: the packet is not at the repo root on live main, so a cold agent
  arriving via main does not find it until the PR lands.
- **Re-pinned to `1d73652231ac6127806640af5a31eb516c60738d`** (the live tip
  at build time). Measured drift since the v3.3 pin: `design-compliance-check.py`
  changed semantically (commit `2e96aa43b`, #2023 — the data: URI document
  "fourth perimeter": srcdoc/data: documents are now decoded and parsed
  recursively, new imports, new depth-budget machinery; scores on pages
  with nested documents will differ from v3.3's proof run). The other 6
  enforcement files are byte-identical pin→tip. "Vendored in this branch"
  language below now means "on main at the pinned tip".
- **Freshness is machine-enforced.** `COLD-START-PACKET.pin.json` records the
  pin, its timestamp, the 7 enforcement files' sha256 at the pin, and the
  SLA (PROPOSED, Naya 1 ratifies: >50 commits past pin, >24h old, or any
  enforcement file changed → STALE). `tools/cold_packet_freshness.py` runs
  the check against live main and FAILS CLOSED, naming the stale pin and
  the live tip. Run it before the acceptance test — the Packet Freshness
  section below points at it first.
- Read list unchanged: 11 items, every path re-verified to resolve on main
  at the new pin. Acceptance mechanics re-proven below against the new pin.

**v3.3 changes (2026-10-09 — the E1 standing trigger fired: live main moved
past the v3.2 pin `45f0ed26`, and 2 of the 7 vendored files changed with real
semantic drift, #1354 comment 6086538851):**
re-pinned to `dad160767b57cb5dab140583c86f418f41685bca` (the live tip at build
time, re-verified at acceptance); all 7 enforcement files re-verified
byte-identical to the new pin (5 unchanged since v3.2, 2 re-vendored). The
drift, understood before vendoring:
- `NAYA-ACTIVATION/ACTIVATION-RECEIPT-V2.json` — the template's `_comment`
  was rewritten for TRUSTED ISSUANCE (round-3, forgery A1): a receipt is
  authentic iff the trusted mint workflow
  (`.github/workflows/activation-mint.yml`, base code, trusted runner)
  minted its exact bytes; the delivery gate verifies the attestation via the
  live API (run exists, mint workflow, success, same repo, artifact bytes
  identical). **A self-minted receipt with perfect public data FAILS
  issuance at the delivery boundary** (`ISSUANCE_UNATTESTED` /
  `ISSUANCE_BYTES_MISMATCH`). New `attestation` block (run_id, run_attempt,
  workflow) and TRANSPLANT BINDING: `deliverables[]` lists every file the
  receipt covers, each with the sha256 of its canonical bytes (receipt
  marker stripped); deletions use `{"action":"delete"}` tombstones
  (round-3c). Repository identity is resolved from the runner-written event
  payload, cross-checked against `GITHUB_REPOSITORY`. The `loaded` skeleton
  is UNCHANGED (`design_contract`/`blocks_catalog`) — the v3.2 wart persists
  in the same shape (see item 8); mint acceptance item 2a with the
  pre-gate's four key names, not the template's skeleton.
- `tools/activation_gate.py` — ROUND 2 rewrite (352 → 1018 lines). Round-1
  was independently attacked (verdict STILL-LEAKING, 5.5/10); ROUND 2 closes
  all four reproduced bypasses: (1) the CI `paths:` filter let deliverable
  PRs dodge the gate — new `.github/workflows/activation-delivery-gate.yml`
  (`pull_request_target`: the workflow file and the gate code come from
  BASE, never from the PR); (2) the gate trusted a PR-editable env var for
  repo identity — now from the runner-written event payload, cross-checked
  against the env, disagreement fails closed; (3) a freestyle component
  passed with a valid receipt — delegate-and-verify to the design gate at a
  pinned commit, unavailable → REJECT; (4) receipt transplant (one job's
  receipt shipping another deliverable) — `deliverables[]` binding, the gate
  recomputes hashes from the PR's actual bytes. Plus: local-mode verdicts
  renamed to `LOCAL-REHEARSAL-UNVERIFIED` / `LOCAL-REHEARSAL-REJECTED` (no
  "PASS" substring anywhere) and local mode ALWAYS exits 3. New trusted-mint
  path: `.github/workflows/activation-mint.yml` + `tools/activation_mint.py`
  (run-attested issuance; the mint binds only what it is told, the delivery
  gate recomputes every hash from the PR's bytes).
- **Two enforcement layers — do not confuse them.** (1) The checker's
  pre-gate (`activation_pregate.py`, UNCHANGED) is your acceptance path: a
  self-minted receipt verified against live trusted state PASSES here —
  that is what acceptance item 2 proves. (2) The delivery gate
  (`tools/activation_gate.py` ROUND 2 + the delivery workflow, in CI) is the
  protected boundary: a self-minted receipt FAILS there with
  `ISSUANCE_UNATTESTED` — only the trusted mint workflow's run-attested
  receipt passes. Your acceptance proves layer 1. Layer 2 is CI's job, not
  yours; do not try to satisfy it by hand (a fabricated attestation fails
  the live-API check anyway).
- Read list unchanged: still 11 items, every path re-verified to resolve
  in-branch at the new pin. Acceptance mechanics unchanged (checker and
  pre-gate unchanged) — re-proven below against the new pin.

**v3.2 changes (2026-10-09 — the independent cold retest scored v3.1
ACTIVATED-WITH-GAPS 7.7/10, #1354 comment 6086149614):**
the retester's durable lesson — *a packet whose acceptance test needs
live-main files isn't a cold-start packet* — is now encoded as vendoring.
The enforcement files the acceptance test invokes are vendored **in this
branch** at the pinned main tip (the live tip at build time, re-verified at
acceptance): `BRAIN/10-INTERFACES/DESIGN-BLOCKS/tools/activation_pregate.py`
(retest gap G1 — was missing in v3.1), the `--receipt`/exit-3-capable
`design-compliance-check.py` (G2 — the v3.1 branch's copy predated the
pre-gate), `NAYA-ACTIVATION/ACTIVATION-RECEIPT-V2.json` (G3 — acceptance
item 2a's template, was missing), plus the rest of read item 7
(`tools/design_gate.py`, `tools/activation_gate.py`,
`.github/workflows/design-gate.yml`) and read item 9's
`smart-blocks/manifest.json` (58 blocks) — all three were named "on main"
but absent from the v3.1 branch. The acceptance test now runs literally from
this branch, no live-main rescue. The vendored copies are a **pinned
snapshot, not live main**: if the freshness check (above) shows the
checker's CLI or the receipt schema changed on live main, the snapshot may
be stale — report that as a packet finding per freshness §3, exactly as
before. File-count audit (G4): the read list enumerates **11 items**, and
the count is now stated explicitly below; every read-list path was
re-verified to resolve in-branch at v3.3.

---

## PACKET FRESHNESS — read this before anything else

This packet is a **perishable snapshot of a moving repo**, not a timeless manual.
Cold Naya-2 (2026-10-09) proved the failure mode: when the acceptance test drifts
from main's behavior, the test measures the packet's staleness instead of your
activation. Defend against that first:

0. **Run the machine freshness check.** `python3 tools/cold_packet_freshness.py`
   (from the repo root). It reads `COLD-START-PACKET.pin.json`, resolves the
   live `main` tip, and FAILS CLOSED when the pin is stale — naming the stale
   pin and the live tip. STALE reasons: the pin is >24h old, live main is
   >50 commits past the pin, or any of the 7 enforcement files changed since
   the pin (SLA proposed by the builder seat; Naya 1 ratifies). A STALE
   verdict means the acceptance test below measures packet staleness, not
   your activation — stop, report it as a finding, and wait for a re-pinned
   packet. Do not work around it.
1. **Re-resolve the tip.** Before the acceptance test, confirm the live `main`
   tip SHA (`git ls-remote https://github.com/SoulSchoolAcademy/NayaPOWER.git
   refs/heads/main`, or the API
   `/repos/SoulSchoolAcademy/NayaPOWER/git/refs/heads/main`). Never reuse a SHA
   from this file or from memory. On 2026-10-09 the tip moved
   `c30201f51` → `c791b7798c34` inside ten minutes, then on to `45f0ed26`,
   then to `dad16076`, then to `1d7365223` — re-verify at action time (SN-0493).
2. **Check for a newer packet.** Look at the repo root and in `NAYA-ACTIVATION/`
   for a newer `COLD-START-PACKET` version. Newest wins, including over this file.
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
  enforcement point (ONE receipt schema, ONE protected truth provider, ONE
  locked door). **ROUND 2 (2026-10-09, on main at the pinned
  tip):** 1018 lines; closes four reproduced round-1 bypasses (CI
  `paths:`-filter dodge, PR-editable trust root, freestyle component,
  receipt transplant) and settles forgery A1 as RUN-ATTESTED ISSUANCE — the
  delivery gate verifies via the live API that the trusted mint workflow
  (`.github/workflows/activation-mint.yml` + `tools/activation_mint.py`)
  minted the receipt's exact bytes; a self-minted receipt FAILS issuance
  (`ISSUANCE_UNATTESTED`). The locked door itself is
  `.github/workflows/activation-delivery-gate.yml` (`pull_request_target`:
  base code judges the PR; the PR's bytes are data, never the judge).
  Context only: the protected boundary is CI's job, not yours. Your
  acceptance path is the checker + pre-gate below — and remember the
  two-layer warning above: a self-minted receipt passes the checker's
  pre-gate but FAILS this gate's issuance check. Do not confuse the layers.
**Warning:** the README's "Usage" block still shows the old checker command
without `--receipt` and lists only exit codes 0/1/2. That block is stale —
trust the checker's own header/`--help` (exit 3 = ACTIVATION REFUSED).
**v3.4:** the checker, both gates, and the CI workflow live on main at the pinned tip — run the repo copies at the pin, not a stale snapshot's.

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
**v3.4:** on main at the pinned tip (unchanged since v3.2). Import it from the repo path above.
**Pinned-tip finding (honest, do not paper over — persists in v3.3
unchanged):** the vendored v2 template's `loaded` skeleton uses
`design_contract`/`blocks_catalog` (matching `tools/activation_gate.py`'s
unchanged `CANONICAL_SOURCES` registry), but the checker invokes *this*
pre-gate, which enforces `design_blob`, `blocks_blob`, `goals_digest`,
`feed_digest`. Mint with the four key names in acceptance item 2a — they
are what this gate checks. The template file is the schema shell; the key
names below are the enforced contract. (The template's round-3 `_comment`
rewrite did not touch the `loaded` skeleton — verified by diff.)

### 9. `BRAIN/10-INTERFACES/DESIGN-BLOCKS/naya-design-catalog.json` — the blocks
The 91 canonical Smart Blocks (reference). Skim the structure: categories,
selectors, usage. "If a block exists for the job, use it."
**Note:** `smart-blocks/manifest.json` (58-block v2 library) is also on main
now (merged 2026-10-09 via PR #2004). The checker still scores against the
91-block catalog by default; the v2 manifest is the forward library.
**v3.4:** on main at the pinned tip (unchanged since v3.2).

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

**End-to-end proof (verified 2026-10-09 against live main `dad16076`,
this packet on its v3.3 branch — superseded):**
stale form (no `--receipt`) → exit 3 `ACTIVATION REFUSED: no --receipt
provided.`; atomic mint via `activation_pregate.fetch_trusted_state()` +
`--receipt` → exit 0, **10.0/10 PASS**, `activation: VERIFIED` in the JSON
output, receipt SHA256 cited in the deliverable matching the exact receipt
bytes. A deliberately stale `feed_digest` → exit 3
`CONTEXT_MISMATCH_*` — the gate catches forgery. First attempt, no digest
race on the mint path this run.

**v3.4 re-proof (2026-10-09, builder seat, against the new pin
`1d7365223`, this packet on the branch tip — the v3.4 text's "this packet
on `main`" was false; the branch was never merged):**
machine freshness check → FRESH (pin == live tip at build time, 0 commits
7/7 enforcement files match); stale form (no `--receipt`) → exit 3
`ACTIVATION REFUSED: no --receipt provided.`; atomic mint via
`activation_pregate.fetch_trusted_state()` + `--receipt` → exit 0,
**10.0/10 PASS**, `activation: VERIFIED`, receipt SHA256 cited in the
deliverable matching the exact receipt bytes. An earlier attempt with a
receipt missing the identity fields (`session_id`, `naya_identity`,
`human_authority`, `repository`) → exit 3 `IDENTITY_INCOMPLETE` — the
pre-gate catches it, which is the gate working correctly. First attempt
at the full run, no digest race on the mint path this run. Independent
cold retest still to come (Naya 1's rung judgment).

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
      gate will refuse, correctly. **Mint with these four `loaded` key names**
      (the pre-gate's enforced contract — not the template's
      `design_contract`/`blocks_catalog` skeleton; see item 8).
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
