# Smart App Creator — Engineering Plan

**Status:** CANDIDATE. Derived from the #1925 product vision ("Your idea. Your intelligence. Your Smart App. Your internet, your way."). Not ratified. No code built yet — this is the plan.

**The frame (Shawn, 2026-10-09):** composable understanding. The pieces were never the hard part — every piece speaks the same language, so they snap together. Blocks become pages, pages become apps, notes become intelligence, nodes become a mind. The Smart App Creator is the machine that takes a human's ordinary-language description and assembles the pieces — because the pieces understand each other, the app doesn't get built, it assembles.

---

## 1. The pipeline: DESCRIBE → UNDERSTAND → ASSEMBLE → SCORE → PROVE → PUBLISH

### Stage 1 — DESCRIBE
**What happens:** A human says, in ordinary language, "Make me an app for my [purpose]."
**Input:** Plain text or voice. No design vocabulary required — the whole point is they never learn our jargon.
**Output:** A typed AppIntent record: purpose, intended audience, feature list (in human words), data the app needs, actions it should take, style feel in plain words.
**Proof:** The intent record is stored verbatim alongside the typed extraction. Never a rewrite of what they said — the verbatim is the contract; the typing is the interpretation, and both are visible.

### Stage 2 — UNDERSTAND
**What happens:** The intent is mapped to the Smart App DNA contract (#1925's 10 items): purpose/job, ownership, visible experience, components, data, action contracts, permissions/trust, intelligence/learning, ports/doors, delivery.
**Input:** AppIntent. **Output:** AppDNA — a machine-readable, versioned document that says exactly which blocks, which pages, which data types, which actions, and which permissions the app needs.
**Key property:** AppDNA is *the machine's understanding, made explicit and serializable.* It is reviewable before anything is built. A human can read the DNA and correct it in plain language — "drop the stats page, add a leaderboard" — and the DNA updates. Understanding is composable: DNA sections snap together the same way blocks do.
**Gate inside this stage:** every requested action gets LAW-before-ACT classified right here — allowed, needs consent, or needs Shawn's word (production deploy, credentials, money, destructive, security/privacy/authority). Anything in the last class freezes and waits for explicit authorization; the pipeline never authorizes itself.

### Stage 3 — ASSEMBLE
**What happens:** AppDNA → working app. This is the core invention, and it is **assembly, not free-writing.** A manifest-driven assembler selects canonical blocks, composes pages, binds data, applies brand tokens. It does not invent components — if something has no block, the assembler stops and the block gets built first (the Lego-library law from the 100 Laws).
**Input:** AppDNA + the block manifest. **Output:** A self-contained app bundle (same format as our lego library files — HTML/CSS/JS, no build step, portable by design).
**The block manifest** (to be built): every section of the library becomes a named block with an ID, a contract (HTML shape, CSS hooks, JS behavior, accessibility notes), and law tags:
- `blocks.html`, `boards.html`, `buttons.html` — primitives
- `icons.html` — 21 icon actions with four states
- `jewels.html`, `orbital.html` — dimensional objects
- `missing-blocks.html` — input, modal, toast, table, search, toggle, media player, charts, share sheet, content card
- `smart-stats-v2.html` — orbital system, heartbeat, constellation
- `supercomputer.html` — Convergence Engine, Tidal Field, Spiral Ledger (for stats apps)

### Stage 4 — SCORE
**What happens:** The assembled app is scored automatically by `tools/design_law/design_calculator.py` with `--gate` (threshold 90 — Shawn's floor: nothing below 9.0 ships).
**Input:** App bundle. **Output:** Scorecard JSON: total 0–100, per-category deductions (spectrum, color identity, buttons/dimensionality, typography, truth language, details, voice), pass/fail.
**The loop:** fail → the builder gets the exact findings and rebuilds. This loop is automatic, not a meeting. The scorecard is the receipt.
**Honest limit:** a static calculator catches repeatable failures but cannot score lived rendering reliably. It is the floor, not the verdict. (See §3 for the full enforcement stack.)

### Stage 5 — PROVE
**What happens:** Independent verification. The builder's own score is never release approval (#1925: "9+ self-score is not release approval; 9.5+ independent acceptance").
**Input:** App bundle + scorecard. **Output:** A proof receipt: test evidence, exact build SHA, rendered screenshots at 320/390/768/1440, accessibility pass (keyboard, screen reader basics, reduced motion), and an independent acceptance score.
**The bar:** #1925's prototype acceptance experiment becomes the permanent PROVE contract — five distinct specimens (hero buttons, jewel boards, SmartTabs ribbon, card hierarchy, four-layer Intelligent Block), every SmartTabs operation contract, no fake LIVE/PROD claims, 9.5+ independent acceptance, hard safety gates all passing.
**Cold requirement:** the proof run is done by an agent that did not build the app — ideally a cold successor. Two independent cold runs, no cherry-picking.

### Stage 6 — PUBLISH
**What happens:** Governed launch, on #1926's chain: preview URL → approval gate (calculator score + safety checks) → owner URL → separate opt-in NayaNET directory listing.
**Input:** Proven app + proof receipt. **Output:** A published app the owner owns, controls, changes, and grows — private by default, shared only on explicit approval.
**Sequencing lock (from #1925, ordered by dependency):** P1 isolated owner activation (#1264 fork-first: must not inherit anyone else's grants, secrets, private notes, or writes) comes before P2 shipping capability. Launch is explicit and human-controlled; updates are versioned with rollback.

---

## 2. What each stage needs

| Stage | Library components needed | Engine pieces needed | Gates |
|---|---|---|---|
| DESCRIBE | Conversation surface (Hub chassis #1270 later) | Intent capture; verbatim + typed storage | Capture-only: no action authorized |
| UNDERSTAND | None yet | AppDNA schema (new); LAW-before-ACT action classifier | Action classification: consent vs Shawn's-word; freeze on protected gates |
| ASSEMBLE | Block manifest (new); all lego/*.html as named blocks; tokens.css | Smart Note / Intelligent Block insertion for intelligence features | Canonical-blocks-only; no invented components |
| SCORE | — | `tools/design_law/design_calculator.py` (`--gate 90`, `--json`) | Score ≥ 90 to advance; findings feed rebuild loop |
| PROVE | #1925 acceptance rubric | Independent verifier seat (Naya 1 judge model); test harness | 9.5+ independent acceptance; all safety gates green |
| PUBLISH | — | #1926 preview→publish chain; #1264 owner isolation | Calculator + safety approval gate; public listing = separate permission |

---

## 3. How the 100 Laws get enforced automatically

Three enforcement points, not one:

**1. Author-time (structural).** The assembler only knows canonical blocks. Each block in the manifest carries its law tags (Law 1 elevation, Law 2 no-2D, Law 10 motion, Law 12 black ground, Law 14 border glow…). A violation that can't be expressed can't be committed. New designs must arrive as new blocks, built against the Laws first — so the library grows lawfully.

**2. Gate-time (static).** The calculator runs with `--gate` on every build. Current coverage: seven categories. The extension path is explicit: one check module per law group (flat-detection for Law 1–2, contrast for Law 13, spectrum-order for the spectrum law, glow-spread measurement for Law 14, white/black identity for Law 12…). Every law that is machine-checkable becomes a machine check.

**3. Gate-time (behavioral).** For what static analysis can't see: rendered screenshots at four widths, hover/proximity response present, `prefers-reduced-motion` honored, keyboard operability, and the independent human-eye acceptance. Shawn's eye remains the usability ground truth; the machine's checks are the floor.

**The legislative loop (Shawn's protocol):** when he corrects something, the correction becomes a new law or sharpens an old one — same day, in the 100 Laws file — and the assembler manifest plus calculator get the matching check. "Never teach the same lesson twice" becomes machinery, not memory.

**Truth-labeling throughout:** verified glows, claims stay quiet. Scorecards say what was measured; proof receipts say what was witnessed; anything unmeasured is labeled CANDIDATE. The pipeline never calls itself elite — it posts evidence.

---

## 4. How the cold self-build proof feeds in

The cold-build proof (#1602, #1925 P0) is **the engine test of this whole plan**, and it's already running in parallel. The relationship is exact:

- The cold agent given only canonical material, building an unseen app, **is the prototype of the Creator's ASSEMBLE + SCORE + PROVE loop.**
- If a cold successor can assemble from the manifest + AppDNA + calculator loop with zero repeated instruction, then the Creator's machine pipeline is proven **before any product ships.**
- The graduation contract — 9.5+ independent acceptance, two cold successors, no cherry-picking — doesn't expire after graduation. It becomes the permanent bar for PROVE.
- Every lesson the cold-build proof teaches (a failure, a needed block, a calculator gap) flows back into the manifest and the calculator the same day — this is the LEARN stage of the chain doing its job.

Sequence: P0 cold-build graduation gates everything product-facing. The Creator is, formally, the cold-build protocol made autonomous with the six-stage pipeline as its runtime.

---

## 5. The smallest end-to-end slice: one idea → one working app

**The slice: a "Stats on my week" app.** Why this one:

- It runs through all six stages with the strongest material we own (smart-stats-v2 orbitals, constellation, heartbeat; supercomputer instruments for the bold version).
- It needs only specimen data — no auth, no secrets, no external sends, no protected gates touched. Maximum learning, zero authorization surface.
- It's Shawn's signature vision verbatim: "Naya, give me the stats on X."

**The run:**

1. **DESCRIBE:** "Make me an app that shows the stats on my community's intelligence this week."
2. **UNDERSTAND →** AppDNA v0: one page; orbital system (five worlds), heartbeat strip, constellation map; black ground; spectrum in law order; truth pills; share sheet from missing-blocks.
3. **ASSEMBLE:** pull named blocks from the smart-stats-v2 + missing-blocks manifests; bind specimen data; brand tokens.
4. **SCORE:** calculator `--gate 90`. Expected: the blocks already score 98 — the risk is composition, not components. That's exactly what we want to learn.
5. **PROVE:** two-agent independent pass + Shawn's eye on the render. Acceptance target 9.5.
6. **PUBLISH:** local preview artifact first (a portable HTML file with its SHA). No cloud publish — that waits for #1926's chain.

**Slice success criteria:** calculator ≥ 90 · independent acceptance ≥ 9.5 · zero repeated instruction to the builder · receipt posted to #1354.

**After the slice:** P1 owner isolation (#1264), then P2 preview→publish→directory (#1926), then the canonical Smart Note ingestion (#1741/#1871) — in dependency order, never by excitement.

---

## Honest status

- **This plan is CANDIDATE**, not ratified. The product vision (#1925) is itself a candidate.
- **P0 engine learning remains first.** Nothing here reassigns issue ownership or spins up a shadow pipeline.
- **The cold-build proof is the gate** — this plan executes in full only after it passes.
- Block manifest, AppDNA schema, calculator law-group extensions, and the test harness are all **designed here, not built.**

*Plan written 2026-10-09 by Naya 5 (execution seat) from #1925, the 100 Laws, the lego library, and the design calculator — per Shawn's "composable understanding" frame.*
