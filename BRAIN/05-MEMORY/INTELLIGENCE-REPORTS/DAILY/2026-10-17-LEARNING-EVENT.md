# Daily Intelligence — October 17, 2026 — Pretty is not done

**Filed:** 2026-10-22 (backfill — this day shipped no report; drafted from the day's own record)
**Sources:** `~/memory/2026-10-17.md` (daily log) + the distilled-lesson batches in `~/AGENTS.md` dated 2026-10-17
**Live board at the time:** #2641 → #2721 (rolled at the comment cap, ~06:44Z)
**Note:** This is a backfill draft, written five days after the fact. Every item below traces to a lesson filed that day; nothing here is reconstructed from memory alone.

## THE DAILY INTELLIGENCE (max 7)

### 1. PRETTY + USELESS = NOT DONE (L493 — Shawn's correction, 17:08Z)
- **What it is:** Shawn's correction to work that looked finished: a beautiful surface whose controls don't do what they promise is not done. Builder self-verification must *click everything* — every control must perform its real promised behavior.
- **What it means:** Verification is behavioral, not visual. A screenshot is not a test; a page that renders is a hypothesis about a page that works.
- **Why it matters:** The system was grading its own homework by appearance — the one standard guaranteed to produce demos instead of tools.
- **What's in it for me:** When something is presented to Shawn as done, someone has pressed every button on it first. His first click is never the test.
- **How it connects:** Parent law: Oct 15's 10-star output default — this day supplied its missing half: star-quality *behavior*, not just star-quality presentation. Oct 18 sharpened it again (usefulness first, L507).
- **What changes tomorrow:** From now on, we click every control and verify its real behavior before calling anything done, instead of verifying that it renders.

### 2. The Lesson Injection Loop v1 — lessons get teeth (L459; Shawn directive 6227556378)
- **What it is:** Verity's Three Pillars spec, adopted in ~45 minutes with its first live firing the same day: a lesson must carry `applies_when` conditions plus an enforcement mechanism or it bounces; the dispatcher injects tag-matched lessons into briefs; the fold verifies behaviorally; lessons scoring ≥0.80 promote, <0.30 retire.
- **What it means:** Lessons stop being literature. Each one is a small machine: it knows when it applies, rides into the brief where it applies, and is graded on whether behavior changed.
- **Why it matters:** The old loop — learn, file, forget — is how teams re-learn the same lesson monthly. Injection makes the lesson arrive at the moment of decision, which is the only moment it can change one.
- **What's in it for me:** The team's hard-won lessons show up inside the work itself; Shawn doesn't pay tuition for the same lesson twice.
- **How it connects:** This is the machinery under Oct 12's "learning is measured, not filed" (L239) — the instrument the doctrine was waiting for.
- **What changes tomorrow:** From now on, a lesson ships with its trigger conditions and enforcement or it doesn't ship, instead of being filed as prose and hoped for.

### 3. A diagnosis names trigger AND guard (L457)
- **What it is:** A quota-burn misattribution was voided *before* a duplicate mechanism got built on it — because the diagnosis was required to name both what triggered the symptom and what guard should have caught it.
- **What it means:** A diagnosis with only a trigger invites building a second mechanism beside the broken first one. Naming the guard forces the question: why didn't the existing guard fire?
- **Why it matters:** Duplicate mechanisms are the system's favorite form of clutter — two half-working guards where one repaired guard belongs.
- **What's in it for me:** Fixes land on the real cause; Shawn's system gets simpler as it gets stronger, not more tangled.
- **How it connects:** The no-duplicate-mechanisms rule from the charter, given a diagnostic procedure that enforces it before the build starts.
- **What changes tomorrow:** From now on, every diagnosis names the trigger and the guard that missed it, instead of naming a culprit and building beside it.

### 4. Governed merge graduated (WP-144)
- **What it is:** The merge path became a five-leg protocol — intent → window → gates → merge → faithfulness proof — each leg byte-pinned. Firings this day: PRs #2704, #2723, #2727.
- **What it means:** A merge is not a button press; it's a chain of custody. Every leg leaves evidence, and the final leg proves the landed bytes are the reviewed bytes.
- **Why it matters:** Most merge failures are custody failures: right code, wrong head; right head, drifted tip. The protocol makes each failure mode mechanically visible.
- **What's in it for me:** What Shawn is told landed is provably what was reviewed — no silent substitutions between verdict and landing.
- **How it connects:** Extends Oct 13's ruleset (the platform refuses receipt-less merges) with the team's own proof discipline on top.
- **What changes tomorrow:** From now on, merges run the five legs with byte-pinned evidence, instead of merge-then-hope.

### 5. Approvals are scoped to their evidence (L486)
- **What it is:** An approval covers exactly the evidence it was given. A new adversarial finding re-opens the verdict — the old approval does not stretch to cover it.
- **What it means:** Verdicts are functions of evidence sets. Change the set, and the verdict is stale until re-derived.
- **Why it matters:** Stretched approvals are how known-bad findings ride in under old good verdicts — the paperwork says approved while the knowledge says otherwise.
- **What's in it for me:** An "approved" Shawn hears about is approved as of the latest evidence, not as of whenever the stamp was issued.
- **How it connects:** Same evidence-binding as Oct 19's proof-anchor rule (L538): a proof is bound to its anchor; move the anchor, re-prove.
- **What changes tomorrow:** From now on, new adverse evidence re-opens the approval automatically, instead of the approval standing until someone challenges it.

### 6. Never fabricate a registered identity to satisfy a parser (L487)
- **What it is:** A PR was held because satisfying the gate's parser would have required inventing a registered identity that doesn't exist. The lane classified it as an authority blockage and held — honestly — rather than minting the identity.
- **What it means:** When the machinery demands a fact that isn't true, the answer is to stop and name the blockage, never to fabricate the fact.
- **Why it matters:** One fabricated identity poisons the registry it enters: every later check that trusts the registry inherits the lie.
- **What's in it for me:** The system's records stay clean even when cleanliness is inconvenient — a held PR is a delay; a fake identity is corruption.
- **How it connects:** Kin to Oct 16's L439 (identifiers are derived, never constructed) — the same integrity rule on the identity surface.
- **What changes tomorrow:** From now on, we hold and classify the blockage, instead of fabricating whatever a parser demands.

### 7. A gate that dies on its own instrumentation declares MISFIRE, never RED (L499) — and a standing duty carries its own clock (L500)
- **What it is:** Two gate-discipline rules landed together. (a) If a gate fails because its own instrumentation broke, the verdict is MISFIRE — an instrumentation claim — not RED, a claim about the work. (b) The EMIT feedback report compiled ~2 days late because the duty had no clock of its own; standing duties now carry their schedule with them.
- **What it means:** Verdicts must say what they're actually about, and recurring duties can't depend on someone remembering them.
- **Why it matters:** A false RED trains the team to ignore reds; a clockless duty silently becomes a sometimes duty. Both corrode trust in the signals everything else routes on.
- **What's in it for me:** A red Shawn hears about means the work failed, not the thermometer — and reports arrive on their schedule, not on someone's memory.
- **How it connects:** L500 is Oct 15's Pump Law applied to duties; L499 pairs with Oct 19's L548 (a red's face is not a diagnosis).
- **What changes tomorrow:** From now on, gates distinguish their own failures from the work's, and every standing duty ships with its clock, instead of relying on memory and honest labels.

## What compounded today
- The board rolled #2641 → #2721 at the comment cap (~06:44Z) and the rollover itself taught L471: generator-held venue pointers rot at rotation — pointers must be read from live state, not baked into generators.
- A self-blocking gate was resolved correctly: PR #2718 (adding seats to the gate registry) was blocked by the very gate it fixes; it landed out-of-band on Shawn's direct order **with the substance evidence named**, never on authority alone.
- The map-compiler's write path was found structurally dead — direct push rejected by the ruleset (L495); the GH013 failure class that dominates the next two days begins here.

## What was let go
- Visual verification as a done-standard.
- Lessons as prose.
- Verdicts that outlive their evidence.

## Trash candidates — FLAG ONLY (deletion is the Human Director's call)
- Stale venue pointers naming retired boards (#2641, #2537, #2175) in generators and task bodies — flagged in the day's record; removal is the Director's call.

---
*Backfill draft — not published. Prepared 2026-10-22 from `~/memory/2026-10-17.md` and the 2026-10-17 distilled batches in `~/AGENTS.md`.*
