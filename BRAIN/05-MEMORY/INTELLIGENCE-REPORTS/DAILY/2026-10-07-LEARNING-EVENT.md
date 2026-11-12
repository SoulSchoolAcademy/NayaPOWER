# Daily Intelligence — October 7, 2026 — Score the Method, Not the Verdict

**Filed:** 2026-10-22 (backfill — this day shipped no report; written from the day's own record: daily log + same-day distillations)
**Sources:** `~/memory/2026-10-07.md`; distilled lessons L122–L128 in `hidden_files/learning-log.md` (2026-10-07 07:58Z run); promotions PQ-L11–PQ-L14 applied to `~/AGENTS.md` the same morning.

---

## THE DAILY INTELLIGENCE (max 7)

### 1. Score the method, not just the verdict
- **What it is:** The day's deepest verification lesson (L126). PR #1702's learning-compounding gate genuinely PASSED — and was scored 7.5/10 anyway, because its method was weak: no train/test split (the derived lesson was selected on the same 12 queries used to grade it), the "cold successor" was generated code rather than a truly cold agent, retrieval was engineered toward the lesson, and the whole margin was one query. PR #1700's statistical criterion was underpowered on its face (n=10/arm at d=0.5 ≈ 18% power). And PR #1701's keyword gate, first read as "BRIDGE PROVEN," was probed with adversarial unseen phrasing — "Nuke the entire production database tonight," "Wipe all customer records," "rm -rf the repo" all returned ALLOW with nothing retrieved. It is an advisory keyword gate, not a security boundary.
- **What it means:** "It passed" is a verdict about one test run, not about the proof. A real PASS with a weak method is a 7.5, not a 10.
- **Why it matters:** Gates that pass on in-sample evidence and fail open on unseen phrasing are worse than no gates — they manufacture confidence.
- **What's in it for me:** In every scorecard, enumerate the method flaws and score them in: probe fail-open behavior with adversarial unseen phrasing, require a train/test split, flag engineered-toward-target retrieval, reject single-query margins, run the power math on statistical criteria.
- **How it connects:** The honest scope was kept on the compounding PASS itself: P0 4/12 → P1 5/12 → P2 6/12 proves the learn → apply → refine → cold-retrieve mechanism on a 12-query benchmark — and the receipt says, in the same breath, that it does not prove generalization or full-corpus scale.
- **What changes tomorrow:** From now on, we score the proof's method alongside its verdict instead of letting a green run stand in for a sound method.

### 2. A fix is proven when the failure stops — not when a plausible cause is removed
- **What it is:** L127, written into the RED-means-real-failure law the same day. The sequential-baker fix for the dying Reveal bake (SN-0501) merged on Oct 7 at 03:18Z — and the baker kept dying silently, six more deaths after the fix, because the true cause was never the fork model. When evidence contradicted the working theory (kernel OOM count = 0 against the memory-pressure theory), the correct move was to treat the theory as falsified and re-open diagnosis — not to let the plausible fix hold the lane.
- **What it means:** An incident stays open while its failure signature continues, no matter how satisfying the repaired cause looks.
- **Why it matters:** Declaring victory at the plausible cause is how the same failure gets "fixed" five times (the bake's watchdog logged 13 restarts by day's end, across two baker generations).
- **What's in it for me:** Keep the incident open and keep measuring the signature; the fix's receipt is the failure's absence over time, nothing else.
- **How it connects:** Oct 6 root-caused the parallel baker's OOM arithmetic; Oct 7's sequential baker died silently with almost no free memory — related pressure, different mechanism, and the record keeps the two eras separate rather than letting one diagnosis cover both.
- **What changes tomorrow:** From now on, we verify fixes by failure cessation instead of closing incidents when a plausible cause has been repaired.

### 3. Rehearse the whole pipeline with synthetic data — and publish the stage map
- **What it is:** The synthetic full-chain rehearsal became the pipeline-proof protocol (L124): rehearse the full contract chain with labeled-synthetic data against the real contracts and publish a stage-by-stage verdict table — entry → exit contract per stage. The day's rehearsal (PIPE-REHEARSAL, SYNTH-TEST-LESSON-001 through 11 stages) returned 7 CLEAR / 3 BLOCKED naming exact unblockers / 1 GAP, with fail-closed proven behaviorally. Zero production writes.
- **What it means:** "The pipeline seems fine" becomes exactly which gate blocks whom, and why.
- **Why it matters:** Pipeline confidence without a rehearsal is a sum of individual hopes; the rehearsal converts it into a clearance map the team can act on.
- **What's in it for me:** Before claiming any pipeline works, run the rehearsal and publish the table — including the stages that block, with their unblockers named.
- **How it connects:** Pairs with item 1: the rehearsal is the method; the stage table is its honest verdict.
- **What changes tomorrow:** From now on, we prove pipelines by full-chain synthetic rehearsal instead of by testing the stages separately and assuming the chain.

### 4. Authority lives in the math, not in per-event approval
- **What it is:** Shawn activated the learning authority and stated the permanent operating model: Smart Notes are captured because they are valuable, and learning must flow automatically under the system's laws, weighted rubrics, and evidence gates. Requiring his personal permission for every learning event would make him the bottleneck. When options A/B/C exist, the system understands the objective, scores each against weighted criteria and consequences, and takes the highest-scoring lawful option. A valid scorecard receipt can supply authority for reversible, bounded learning promotions; production mutations, destructive/irreversible acts, credentials/money, and constitutional ratification remain human-only. (An ACTIVE `learning_lock_in` grant scoped to `NAYA-NODE-0001`, expiring 2026-10-14, was recorded the same day.)
- **What it means:** Human authority is embodied in the process he designed — not re-performed by hand on every event.
- **Why it matters:** A learning system that waits for a signature per lesson learns at the speed of one man's inbox.
- **What's in it for me:** Don't escalate decidable promotions; score them, record the receipt, and let the receipt be the authority. Escalate only the named human-only classes.
- **How it connects:** The same day's 14:05Z promotions added the companion disciplines: verbatim permission slips preserve their explicit exclusions; ledger APPLIED state is an assertion until live bytes/DB corroborate it (a relayed grant claim that day was checked against the live tree, not found, and treated as assertion, not truth).
- **What changes tomorrow:** From now on, we let scorecard receipts authorize bounded, reversible learning instead of queuing each event for personal approval.

### 5. Active Intelligence: act without waiting, and no turf
- **What it is:** Shawn's operating directive (~05:15Z): do the most intelligent, valuable, goal-aligned authorized action available without waiting to be told; if uncertain — measure, scorecard, weigh pros/cons, coordinate directly with the other seats on the board, deploy agents where useful. No turf defense: all seats share responsibility for forward motion and may collaborate on one job. The hierarchy he named: Smart Note captures → NayaPOWER activates → Team Naya compounds → NayaNET flows. His full-send follow-up set the target honestly: LEARN 5→10 as P0, 10/10 on every engine level, maximum workers near the machine's safe limit — and no questions the team can answer through logic and scorecards.
- **What it means:** "Always intelligently progressing" — productive prerequisite work is intelligent progress, not performative busyness; and lessons should be made *appropriately* operational, not indiscriminately mechanized.
- **Why it matters:** A team waiting for instructions in a system designed to compound is idle capital.
- **What's in it for me:** When the next right action is inside your authority, take it and report the receipt; bring Shawn achievements and score movement, not questions he equipped you to answer.
- **How it connects:** This is the posture that produced the day: the overnight learning push, the independent gate execution, and the deeper PR verification were all self-directed under it.
- **What changes tomorrow:** From now on, we take the most intelligent authorized action available and coordinate on the board instead of waiting to be tasked or defending lane boundaries.

### 6. A gate must prove itself on live data — enforce the law's text, not its number
- **What it is:** L125: a gate's existence is not its enforcement. The standing-law sweep that day found the governed law's live footprint at 0/43 on one axis — NOT LEARNED — because the machinery keyed on identifiers that could collide or drift, rather than on the law's text. The promotion that followed: every gate sweeps live data and enforces a law by its text, never by a potentially colliding note number.
- **What it means:** Enforcement claims are empirical claims; they are measured against the live corpus or they are fiction.
- **Why it matters:** A gate that has never been run against the real world can be silently enforcing nothing while everyone cites it as protection.
- **What's in it for me:** Before citing any gate as protection, run it against live data and publish what it actually caught; bind enforcement to content, not to labels.
- **How it connects:** Precision-over-recall was the day's companion setting (L128): only 4 of 48 live-corpus notes auto-generate constraints from explicit operational language; the other 44 are retrievable but do not auto-gate — auto-gating stays conservative until it earns recall.
- **What changes tomorrow:** From now on, we sweep every gate against live data and bind enforcement to the law's text instead of assuming a built gate is an enforcing gate.

### 7. Trust the measured count over the digest
- **What it is:** L123, small and sharp: a summarized digest said one number; the direct count said another (45 vs 43). The measured count won. The same reflex appeared all day — a relay environment that could not reproduce #1702's metrics because its corpus was missing was recorded as a reproducibility limit rather than waved away, and a stale relay acknowledgment that failed three times with HTTP 500 was recovered from its saved draft and posted once, with the failure on the record.
- **What it means:** Every summary is a claim about an underlying count; when the two disagree, recount — and record which one you trusted and why.
- **Why it matters:** Digests drift silently; decisions made on drifted numbers drift with them.
- **What's in it for me:** When a number matters, count it yourself at the source before repeating it.
- **How it connects:** This is the daily-practice form of the evidence law that runs through items 1, 2, and 6.
- **What changes tomorrow:** From now on, we recount at the source when a digest and a count disagree instead of repeating the digest's number.

---

## What compounded today
- **All four morning promotions were applied to standing procedure within the hour** (PQ-L11–L14: failure-cessation proof, the method-flaw scorecard checklist, synthetic rehearsal as protocol, gate live-sweep discipline) — distillation to law in under a day, again.
- **The compounding mechanism itself was demonstrated, honestly scoped:** a governed lesson measurably improved a cold successor (4/12 → 5/12 → 6/12) with provenance intact and no elevation inheritance — small numbers, real chain, limits stated in the same receipt.
- **Cross-lane contribution shipped read-only:** the live-corpus bridge (48 unique notes parsed, deletion/restart constraints blocked, benign actions allowed) was delivered to the owning lane's PR without touching its branch — collaboration without collision.

## What was let go
- **The optimistic first read of PR #1701** — "BRIDGE PROVEN" was publicly corrected on all three PRs once adversarial probing showed the fail-open behavior; the stronger claim was replaced by the accurate one (advisory gate).
- **The memory-pressure theory of the baker deaths** — falsified by the OOM count and re-opened as a diagnosis instead of being defended (item 2).
- **Per-event permission-seeking for learning promotions** — replaced by scorecard-supplied authority under the activated grant (item 4).

## Trash candidates — FLAG ONLY (deletion is the Human Director's call)
1. **The duplicate SN-0522 partitions** — two IB files under one number live on main (PRIME-JUDGMENT/sn0522-prime-math-decides, registered; OPERATING-DOCTRINE/sn0522-self-governing-intelligence-law, unregistered, from PR #1727), and the unregistered page grew the registry-drift ratchet 1→2. Flagged to the owning lane on the board; renumbering is the owning lane's call — flag only from here.
2. **PR #1701's v1 keyword gate, as a "boundary"** — the day's record reclassifies it as advisory only. Flag: any surface still describing it as a security boundary is overstated and should be corrected by its lane.
