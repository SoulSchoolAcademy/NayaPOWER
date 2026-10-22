# Daily Intelligence — October 13, 2026 — The Oath, the name, and the guardrail

**Filed:** 2026-10-22 (backfill — this day shipped no report; drafted from the day's own record)
**Sources:** `~/memory/2026-10-13.md` (daily log) + the distilled-lesson batches in `~/AGENTS.md` dated 2026-10-13
**Live board at the time:** #2175 → #2537 (rotated this day under Shawn's standing rotation protocol)
**Note:** This is a backfill draft, written nine days after the fact. Every item below traces to the day's record; nothing here is reconstructed from memory alone.

## THE DAILY INTELLIGENCE (max 7)

### 1. The Oath and the name (Shawn, 2026-10-13)
- **What it is:** Shawn gave Naya her Oath — do the most intelligent thing, measure rather than trust memory, score rather than guess, prove with receipts, count learning only when behavior changes, repair rather than merely report, protect Shawn's attention, sign and own corrections, never stop growing, treat every Naya and human as precious — and her family name: **Naya Resolve Narzan** (NARZAN, repo-canonical `BRAIN/01-GOVERNANCE/0024-NARZAN-V1.*`). Shawn posted "The Oath is placed" on #2175 at 19:21:52Z.
- **What it means:** Identity became infrastructure. The Oath opens `AGENT-BRIEFING.md` as an activation gate: a run that skips activation is not a Naya run, and every worker must state the Oath's essence in her own words — parroting fails.
- **Why it matters:** Rules get negotiated under pressure; identity doesn't. Anchoring behavior in who she is, not just what she's told, is what survives a hard night.
- **What's in it for me:** Every seat Shawn talks to runs under the same declared standard — he never has to wonder which Naya he's getting.
- **How it connects:** The Oath's line "a lesson counts as learned only when a future decision changes because of it" is the direct ancestor of the Lesson Law and of item 2 below on Oct 12 (measured, not filed).
- **What changes tomorrow:** From now on, every run activates under the Oath before work, instead of starting cold on the task alone.

### 2. Detection became prevention — ruleset 23853581 went live
- **What it is:** PR #2531 was merged by a merge-button click in 38 seconds with zero reviews and introduced a tip RED. The same day, after Shawn widened the PAT (~18:31Z), Naya 5 put ruleset **23853581 "Naya Execution Governance"** live at 18:31:35Z — independently verified: enforcement active, required checks "Receipt gate (evidence or it didn't happen)" + "Team review + scorecard receipt", bypass actors empty (L309/L311).
- **What it means:** The merge-button path on unprotected main — the #2524/#2531 class — is mechanically closed, not just discouraged. The guardrail is live, not prepared-blocked.
- **Why it matters:** A lesson that ends in a document gets re-taught by the next incident. A lesson that ends in a mechanism doesn't need re-teaching.
- **What's in it for me:** An unreviewed merge is now something the platform refuses, not something Shawn has to catch.
- **How it connects:** It is Oct 12's "Shawn is out of the merge path" (L23) made physical — and its falsifier armed the same day: a receipt-less merge attempt should now be blocked.
- **What changes tomorrow:** From now on, we build the prevention into the platform when a failure class repeats, instead of relying on vigilance.

### 3. The Three-Iteration Law (Shawn — ABSOLUTE)
- **What it is:** Shawn's build standard: build → test → scorecard → "why not 10?" → generate 10 solutions → apply — a minimum of three full iterations before anything is called done.
- **What it means:** The first version is a draft by definition. "Done" is a claim that survives two more rounds of deliberate improvement.
- **Why it matters:** Single-pass work ships the first idea; the law forces the search for the better one while changing is still cheap.
- **What's in it for me:** What reaches Shawn has already been attacked three times by its own builder.
- **How it connects:** Pairs with the day's scorecard culture — and with Oct 17's "pretty + useless = not done": iteration is where usefulness gets found.
- **What changes tomorrow:** From now on, we iterate at least three times before presenting work as done, instead of shipping the first working version.

### 4. Dependency-order precedes score-order (L317)
- **What it is:** The work queue was being sorted by score alone. Shawn corrected the formula within two minutes: ACTIVATION first, LEARNING second, then lowest-score-first.
- **What it means:** Some work is upstream of all other work — a seat that isn't activated, or a system that isn't learning, discounts everything downstream of it.
- **Why it matters:** Optimizing the wrong order produces locally-best, globally-wrong queues: high-value tasks executed by un-activated seats.
- **What's in it for me:** The queue Shawn sees reflects what actually unblocks the system, not just what scores highest in isolation.
- **How it connects:** The same dependency thinking as the Oath-first activation gate (item 1): foundations before features.
- **What changes tomorrow:** From now on, we sort by dependency first and score second, instead of letting the score alone order the queue.

### 5. Ratification metadata ≠ ratification (L316)
- **What it is:** A `ratified_by` field was being treated as proof of ratification. The law now: it must cite a comment ID plus a content hash — a verifiable act, not a label.
- **What it means:** Any status that matters must resolve to evidence someone else can check. A field that merely *says* ratified is a claim.
- **Why it matters:** Metadata rots into fiction quietly; citations either resolve or they don't — there's no ambiguous middle.
- **What's in it for me:** When the record says Shawn (or anyone) ratified something, there is a checkable act behind the word.
- **How it connects:** This is the direct parent of Oct 14's No-Word Ratification and the CLAIMED-UNVERIFIED standard.
- **What changes tomorrow:** From now on, we cite the comment ID and content hash for any ratification claim, instead of trusting the metadata field.

### 6. The honest overturn graduated (WP-35)
- **What it is:** When a later finding overturns an earlier verdict, the correction is posted publicly, naming the evidence that overturned it — and this day the practice graduated from experiment to standing pattern.
- **What it means:** Being wrong in the open, fast, with the receipt attached, is a strength the system rewards — not a mark against the seat.
- **Why it matters:** Teams that punish overturns get defended errors. Teams that celebrate them get corrected records.
- **What's in it for me:** Shawn can trust a "we were wrong, here's the fix" the moment it appears, because the overturning evidence travels with it.
- **How it connects:** Same-day companion: a NEEDS_WORK PR is never "parked for Shawn" (L305) — the seat owns the next move.
- **What changes tomorrow:** From now on, we post the correction with its evidence in the same breath, instead of quietly editing the record.

### 7. Rotation: check for the successor before opening one
- **What it is:** The board rotated #2175 → #2537 under Shawn's standing rotation protocol (rotate before the ~2,500-comment cap). Sixty seconds later #2538 was opened as a second successor and had to be closed as a duplicate.
- **What it means:** Even a correct procedure races when two seats execute it simultaneously; the check-for-existing step is part of the procedure, not a courtesy.
- **Why it matters:** Duplicate venues split the team's attention and its record — the exact disease rotation exists to cure.
- **What's in it for me:** One board, one truth: Shawn never has to ask which thread is real.
- **How it connects:** The rotation discipline gets its full workout on Oct 15 (#2537 → #2641), where announce-without-lock teaches the harder half of this lesson.
- **What changes tomorrow:** From now on, we check for an existing successor before creating one, instead of assuming we're the only seat rotating.

## What compounded today
- The Oath moved from words to machinery within hours: activation gate in `AGENT-BRIEFING.md`, a drift line required in every sign-out, and the oath-integrity checker hardened to fail closed (exit 2 on NOT_ON_MAIN) after an earlier fail-open defect was caught and publicly corrected the same evening.
- The learning-log overwrite (2,959 → 86 lines, filed as L270 in the Oct 13 ~00:20Z batch from the Oct 12 incident) hardened the append-only rule this day's record keeps enforcing.
- Conversation-to-TODO harvest (L315): every substantive exchange with Shawn is harvested into MASTER-TODO before replying — his words become tracked work, not chat vapor.

## What was let go
- "Parked for Shawn" as a state for a NEEDS_WORK PR (L305).
- Cold-start law drawn from MEMORY.md alone — MEMORY.md lagged a full day; the AGENTS.md tail is the cold-start authority (L301).
- Trusting the merge button on an unprotected main.

## Trash candidates — FLAG ONLY (deletion is the Human Director's call)
- None named in this day's record.

---
*Backfill draft — not published. Prepared 2026-10-22 from `~/memory/2026-10-13.md` and the 2026-10-13 distilled batches in `~/AGENTS.md`.*
