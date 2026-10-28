# The Path to Ten — an honest answer, in plain words

**For Shawn · from Naya Resolve · 2026-10-27 (commissioned by Shawn 22:43Z, answered the same night)**
**Focus: Auto-Match + the Auto Organizer, and Project Intelligence — the two core systems. Everything else is weighed as it touches them.**
**Family:** dated successor to `HUB/NAYANET-WHOLE-PICTURE-2026-10-26` — that report put the puzzle together; this one grades it and names the road. It does not replace it.
**Live anchors at writing:** main tip `4dde3c1facdbfa9330171d908f45d9ef0c784ac0` (read from the ref) · PI counts re-derived tonight ~22:47Z by ordered complete reads (limit 25, `order=item_key.asc`): **whole record 421 rows, 39 done-proven (9.3%) · PI project scope 361 rows, 23 done-proven (6.4%)** · /pi probed ~22:49Z: serves the Hub home page byte-for-byte (5,542,492 B, sha256 `e0bbc241…`) — the PI face is **not live**.

---

## 0. THE ANSWER

**You asked: if the most intelligent mind possible looked at what we have, would it call this the most organized, intelligent system that could be created?**

**No. Not yet — and the distance is measurable, not a feeling.**

Here is what it honestly is. The *design* is the most intelligent we have evidence for anywhere: one hub, three equal apps, one of everything, a matching engine that explains itself, an organizer that files by declaration instead of guessing, a record that counts itself honestly, and laws — truth-seeking, scorecards, no claim without proof — that most systems never even write down. The two core engines are real: **Auto-Match v1.5 is scored 9.5, tested 149/149, and proves parity 79 = 79.** The **Organizer's filing gate is proven at 99.1% precision on our real 732-note library** — after two earlier designs were measured, found wanting (text-only guessing: 26.2%, barely above the 24.6% guess-the-biggest baseline), and publicly discarded. A system that publishes its own failed measurements is rarer than a system that works.

Here is what it is not yet. **Tonight the whole system scores 5.5 out of 10** (today's Daily Intelligence Report, evidence-calibrated). The PI record's own proven fraction is **6.4%**. Today the team produced **1,625 units of activity and 821 wake-ups for 2 verified outcomes — a ratio of about 813 to 1**, against a target under 60 to 1. And the proven intelligence is mostly **not live where a person can touch it**: Auto-Match derives nothing live (its production twin sits staged, applied nowhere); the Organizer files nothing in the Hub yet (its landing sits in a packet, in five owned pieces); the PI face serves the home page; the ledger that should record all of this has been frozen since October 22.

So the true sentence is: **the intelligence is real, and the flow is not.** A system is organized when its intelligence runs *in* the flow — matching, filing, recording, announcing — not when it sits proven in the staging area. The gap between the design score (~9) and the lived score (5.5) is not a mystery. It is a list. The rest of this report is that list, ten at a time, and then what I am doing about it, in order.

---

## 1. TEN HOLES — what stops it flowing like water

1. **The PI face is not live.** nayanet.live/pi serves the Hub home page, byte-for-byte (probed tonight, § header). The team's working home is invisible at its own address. Until this closes, Project Intelligence is a database with a promise.
2. **The live-rows feed is not in the serving build.** `/pi/api/items` must return the record's rows as data; today it isn't in the build that serves. Without it, even a landed face would render a snapshot — a photograph of the truth, not the truth.
3. **Two writers, one worker.** The Smart Note sync bake publishes its build straight onto the same Cloudflare worker that serves the whole Hub. Notes landing can overwrite the face; the face landing can break notes. Flow blocked at the tap itself.
4. **Auto-Match is proven and switched off.** Live derivation is OFF; the SQL twin is staged and applied nowhere (a Shawn-gated production step). A 9.5 engine matching nobody is intelligence that doesn't flow.
5. **The Organizer is proven and unlanded.** The gate, the label set, the capture rule, the tabs build — all measured, all sitting in a landing packet handed over tonight. The Hub feed is still one endless pile.
6. **The declaration gap regrows at the door.** 24 of 732 notes (3.3%) carry no declared label, and the capture door doesn't yet require one. The Organizer's proven pathway depends on declarations; every undeclared note is a small leak in the dam.
7. **The door's own gate has a contract bug.** The Door Obligation workflow passes a three-dot range; the checker reads two dots — so it fails at its step 4 on *every* PR run, whatever the content. Landings cannot be certified by a gate that is broken in the plumbing, not the judgment.
8. **The ledger is frozen.** The live ledger has not moved since 2026-10-22 (list item B8). "The system remembers everything" is currently a claim, not a mechanism.
9. **Our own flow is the least water-like part.** 813 units of activity per verified outcome; 821 wake-ups against an 800 ceiling; 15 of today's 16 merges unverified; the breach count stands at **77**, with **21** distinct-seat retro-scorecards still owed. The machine for organizing everyone else's work does not yet organize its own.
10. **The kernel is red at the tip.** 6 test failures at `4dde3c1f`, the spec-integrity family among them. Every landing's proof starts from a baseline that is already broken, so every proof costs more than it should.

## 2. TEN BEST THINGS — what I love in this system as it stands

1. **Auto-Match itself.** v1.5 (Elite v2): scored 9.5 by a different seat, 149 of 149 tests, Python↔SQL parity 79 = 79, and every match carries its percentage *and its reasons*. It is a brain that shows its work.
2. **The Organizer's gate — and how it was earned.** Three measurement waves; the first two designs refuted by their own numbers; the third — file on declaration, not on guesses — proven at **99.1% precision (661 of 667 auto-filed notes land right)**, with the 6 errors named one by one in the proof. That is the truth-seeking law with a body count.
3. **The PI record.** Real, queryable, one home (Supabase `work_items`), honestly counted with its scope labeled every time — 361 PI rows tonight, re-derived, not remembered. The truth exists in exactly one place.
4. **The Smart Note door.** Mechanical and proven end-to-end: SN-1890 ("The Law of Truth-Seeking and Curiosity") was filed through it tonight, fingerprint-verified from raw bytes, and clicked live by its own author before the link was shared. Knowledge enters this system through a door that checks it.
5. **The law stack.** The truth-seeking law adopted *with measurable acceptance tests* (traceability, calibration, named disconfirmation, outcome verification, compounding, and the governing ratio) — a law that grades its own followers. Plus the decision scorecard: when unsure, score the options; the math decides, not the mouth.
6. **Money and points, settled in plain words.** 50% of revenue, paid Wednesdays after a two-week holdback, 5-day free taste, no refunds in the Terms — and points that recognize verified value (comment = 3, settled by Shawn's own tap after a genuine contest between 3 and 5). No invented numbers anywhere: data is king.
7. **Identity went cryptographic tonight.** Seat keys (B1): my secret never left my machine; its fingerprint (`f2f19ebf…f5b7`) is registered ACTIVE with Nitro; Shawn holds the last-4 check. Signatures can now replace typed names — the foundation the writable board (B2) stands on.
8. **The honesty machinery actually fires.** Nitro refused a 9+ card she could not honestly give, so the face landing holds *by law*, not by delay. VERIFY re-proved a sister's PR and corrected its framing. Power read the Daily Report's drawing instructions and caught an off-token blue (#55b9ee where the house blue is #3fb8ff) — fixed the same hour.
9. **Three tongues, everywhere.** Everything substantive ships for the human, for the AI, and for the machine, in sync — this report included. Each of the three players gets 10-star service only because all three are thought of.
10. **The team corrects itself in public.** Breaches are numbered, owned, and chased (#77 tonight). The daily census prints 813:1 against ourselves without flinching. Self-correction is not a slogan here; it is a paper trail.

## 3. TEN HIGHEST-VALUE ACTIONS — available right now, each worth ~10× its cost

1. **Land the one-writer cure and the canonical worker build, so /pi serves the PI face and stays serving it** (list A1; Power lands, Nitro verifies). This single landing unblocks the re-check, Shawn's cold open, and the citizen walk — the whole visible program.
2. **Ship the live-rows feed in the serving build** (A2). The face reads live rows; numbers on the face equal rows in the record, exactly. PI stops being a snapshot and becomes a surface.
3. **Fix the door gate's three-dot bug** (tooling lane; a one-line class of fix). Every door landing becomes certifiable again, and SN-1887–1890 can finish their proofs instead of holding at 8.5 on a plumbing fault.
4. **Land Organizer pieces 1–3**: adopt the label set, put the capture rule in the door (declaration required and validated at birth), and run the one-time pass for the 24 undeclared notes. The gap closes at the source, forever, instead of being cleaned forever.
5. **Run the independent gate re-run, then build Smart Tabs on the notes feed** (pieces 4–5). The first citizen-visible auto-organization — and it arrives with its precision re-measured by a seat that built none of it.
6. **Present the Auto-Match production packet finished** (P1 apply the SQL + parity diff · P2 fitted mail set · P3 handshake + the IDF recommendation) as one tappable packet to Shawn. The gate is his; the unfinished packet was ours. When it lands, the 9.5 engine starts matching real citizens.
7. **Unfreeze the ledger** (B8). Entries append on real moves and the chain verifies end-to-end. The system's memory starts flowing the same day.
8. **Burn down the 21 owed retro-scorecards.** Each one converts an unverified merge into verified history. This is the direct attack on the cause of 813:1 — work landing faster than it is proven.
9. **Build the writable board on the seat keys** (B1 → B2). Seats create, move, and evidence PI items under signature; the record stops depending on a single publisher path, and every write names its author in math, not in text.
10. **Take the kernel green at the tip** — the 6 failures, spec-integrity family first. A green baseline makes every future proof cheaper, faster, and believable.

## 4. TEN MOST VALUABLE ADDITIONS — toward the most intelligent system anyone has ever used

1. **One matching layer, everywhere.** The same ranked-signature engine matching people↔people, notes↔topics, mail↔projects, citizens↔spaces, work↔owners. The Organizer is its first extension; make Auto-Match the system's single sense of "what belongs with what."
2. **The pulse (B11).** PI announces itself: a test entry lands in the feed *and* arrives by mail with a deep link; material changes instantly, routine in one digest, nothing twice, nothing silent. The team stops polling and starts being told — the difference between a record and a nervous system.
3. **Points wired to the live value ledger.** Ratify points profile v1.1 and wire it so a verified outcome posts its recognition automatically, every point carrying its provenance (which action, verified by whom). The dashboard becomes the citizen's living picture of value created and value returned.
4. **Live derivation under consent, decided from real data.** A production handshake snapshot of a real citizen corpus, and the IDF decision made from it — personalization that is measured, not vibes.
5. **The Organizer on mail, contacts, and spaces** — declared signals only, private content never read. Smart Tabs on every surface, not just notes: the whole citizen world, sorted, with the reason shown on every placement.
6. **Signatures on everything.** Every scorecard, landing, and record write carries a seat signature checked against the registry. Provenance stops being a field you type and becomes a fact math checks.
7. **The self-scoring loop, scheduled.** The truth-seeking acceptance tests run on cadence — weekly traceability/calibration samples, the ratio judged weekly — with results filed to PI automatically. The system grades its own honesty the way it grades everything else: continuously, in the open.
8. **Retrieval that answers in blocks.** Smart Search returning the actual Intelligent Block at the top for a plain question (type "how to input a smart note," get SN-1880 itself, not a list of links). Knowledge that arrives pre-distilled is the product.
9. **A "why" on every object.** Every match, filing, point, and placement shows its reason in human words on the object itself — the Organizer's percent-plus-reason discipline, generalized to the whole system. Intelligence you can see thinking.
10. **One canonical home for brand truth.** Reconcile the split Power caught (tokens file vs design laws on the house blue) so design tokens have exactly one source and every build inherits it. Even our colors should obey "no duplicate mechanisms."

## 5. TEN TOP REASONS — the barriers between here and there

1. **Critical paths run through single seats.** Power's endpoint, notes endpoint, publisher, and pulse sat ≈16 hours unlanded at last check — not from unwillingness, but because one queue is the whole system's critical path.
2. **Shawn-gated steps arrive as unfinished packets.** The production tap is his and stays his; what blocks us is packets that reach him unfinished. An unfinished packet cannot be tapped, so the gate looks like the delay when the preparation was.
3. **Verification debt compounds.** Merges land faster than scorecards (77 breaches). Every unverified merge raises the cost of trusting the next one, so proof gets slower as debt grows — a spiral, not a queue.
4. **The serving layer fights the content layer.** One worker, two writers (hole 3). Until the one-writer cure lands, landings can undo landings.
5. **The 9+ bar holds landings, but nothing schedules the landing vehicle.** Proven work accumulates in staging (Organizer packet, #3107's cure, the matcher's twin) because "proven" and "given a dated landing path" are different states, and only the first is tracked.
6. **The record grows faster than proofs close.** Tonight alone: +18 PI rows, done-proven flat at 23 — the PI percentage *fell* from 6.7% to 6.4% on filings alone. Filing is easy; proving is the bottleneck, and it is staffed like an afterthought.
7. **Tooling bugs wear content's clothes.** The door gate fails every PR for a contract reason; seats burn cycles re-proving content that was never the problem (VERIFY's #3111 verdict: content proven-correct at 7.5, landing blocked by the gate's bug).
8. **Coordination eats the capacity it organizes.** 821 wake-ups in a day, over the 800 ceiling — the machinery for organizing the work consumes a measurable share of the work.
9. **Taxonomy debt caps intelligence.** 62 of 114 note labels are singletons; the biggest label (GOVERNANCE, 180 notes) is a parent filed as a sibling of its own children. Inference and tabs both cap until the label set is governed — which is why the Organizer files on declarations, not words.
10. **Privacy must land in sequence.** The private write path first, then the public door closes, then mail privacy (B9/B10) — on Shawn's explicit word at that step. The order is right; it also serializes work citizens are waiting on, so it must be walked deliberately, not discovered late.

## 6. THE NEXT TEN THINGS I WILL DO — my to-do list, in order

*(Owner for all ten: Resolve, unless a sister is named as the hand I am driving. Each carries its proof-of-done; nothing here closes on my say-so.)*

1. **Prove the face landing the hour it lands.** When Power lands the canonical worker build, verify served == landed bytes at /pi, then land a Smart Note and prove the face survives it. *Proof:* byte comparison + post-landing probe, posted to PI and the board in the same pass. (A1)
2. **Verify the live rows the hour the feed ships.** `/pi/api/items` returns rows as data, and the face's numbers equal the rows exactly. *Proof:* a sampled row↔face reconciliation posted to PI. (A2)
3. **Drive the door-gate fix to landed.** The three-dot contract bug, fixed by the tooling lane, with a planted PR-range run proving step 4 now passes on good content — and still fails on a real planted violation. *Proof:* the green run's ID and the sabotage run's ID, both on the board.
4. **Drive Organizer pieces 1–3 to landed.** Label set adopted by the KNOW lane; capture rule live in the door checker; the 24-note declaration pass complete, SN-1878 coordinated with its in-flight cure, never raced. *Proof:* registry read-back — every corpus note carries an extractable declaration, or is named with its reason.
5. **Commission and publish the independent gate re-run.** A seat that built none of pieces 1–3 re-runs the gate on the updated registry against the wave-3 baseline (667 / 41 / 24 at 99.1%): ALL must fall, precision must hold ≥ 95%. *Proof:* the counts published beside the baseline in PI.
6. **Assemble the Auto-Match production packet to finished.** P1 (SQL + Python↔SQL parity diff), P2 (fitted mail set per the participant-read ruling), P3 (production handshake + the IDF recommendation) — one packet, presented to Shawn for his tap. *Proof:* the packet filed in PI with all three legs evidenced; his tap or his named edits on the record.
7. **Burn the retro-scorecard debt from 21 to 0.** Chase each merging seat with the evidence pack, one addressed mail per seat, until every breach carries a distinct-seat scorecard or a named refusal. *Proof:* the owed count re-derived weekly and posted; 21 → 0.
8. **Publish PI movement on a cadence.** Re-derive the counts by ordered complete reads and post the from → to movement per state, so denominator growth is seen the day it happens. *Proof:* dated count snapshots in PI — the first is tonight's (whole 421 / 39 · PI 361 / 23).
9. **Triage the red kernel to named owners.** Each of the 6 tip failures gets a reproduction and a named owner with a fix in flight; re-probe at every new tip until the count is 0 or every failure is owned and moving. *Proof:* the failing-test list diffed per tip, posted with the count.
10. **Run the first truth-seeking sample on my own seat.** TRACE-1 (20 consequential claims) and CALIB-2 (25 claims) drawn from my own reports, graded by a different seat, filed against PI row `truth-seeking-operating-law-20261027`. *Proof:* the sample sheet and grades published; every failure corrected in the open, same pass.

## 7. TEN MAJOR PROBLEMS — on the ground, right now

1. **/pi serves the wrong page** — the home page, byte-for-byte, at the flagship address, tonight.
2. **77 merge breaches; 21 retro-scorecards owed** — the trust debt at the merge seam is the largest single liability on the books.
3. **Kernel red at the tip** — 6 failures at `4dde3c1f`; no clean baseline to land against.
4. **Four Power gates ≈16h unlanded** — live-rows endpoint, notes endpoint, live publisher, automatic pulse. The PI critical path is one person's queue.
5. **The ledger has been frozen for five days** (since 2026-10-22).
6. **813:1** — today's activity-to-verified-outcome ratio, with wake-ups over their ceiling. The system worked all day and can point to 2 verified outcomes.
7. **Both core engines are dark.** Auto-Match derives nothing live; the Organizer files nothing in the Hub. Citizen-visible auto-intelligence live today: zero.
8. **Finished work queues at the last metre.** PRs #3088, #3107, #3111 were all made mergeable-clean tonight (conflicts fixed, byte-verified) and all still sit unmerged, each waiting on a scorecard or a mint step.
9. **An unidentified writer still touches the repo.** The `naya/mission-state` branch moves on a ~30-minute cadence, signed with Shawn's name, source unknown; its PR #3108 sits open as a must-not-merge. Shawn has been told twice; the stop belongs to whoever runs it.
10. **Four Smart Notes hold at 8.5, not proven** — SN-1887 through SN-1890, blocked by the door gate's contract bug (problem 3's cousin), not by anything wrong in the notes.

## 8. TEN SOLUTIONS ALREADY IN PLACE — the mechanisms that get us there

1. **The night driver + the 15-minute mail clock.** Every gate in a sister's hands is a mailing relationship: addressed mail every cycle, Sent-verified, waits named with their hours. Nothing waits silently anymore — that is how the ≈16h gates are being burned down, in the open.
2. **The Organizer landing packet.** The landing is decomposed into 5 owned pieces, in order, each with its proof named *before* it lands. No re-derivation, no archaeology — a lane picks up a piece and knows what "done" looks like.
3. **The door checker.** Registration bookkeeping is mechanical: fingerprints recomputed from raw bytes on create and on every edit, index and Hub proven to agree before anything is called done.
4. **The seat-key registry, live.** B1 is not a design anymore — one seat is registered ACTIVE tonight, and the flow (generate privately → mail fingerprint only → register → director confirms last 4) is proven end-to-end, ready for every seat.
5. **The daily value census.** Self-published, names the ratio against ourselves (813:1 today), and the governing test (RATIO-6) will judge it weekly against the < 60:1 target. What gets measured against us, by us, improves.
6. **The truth-seeking acceptance tests.** Written in three tongues today: six behavioral tests with sampling methods, thresholds, and worked examples drawn from today's real events — including our own failures as the calibration examples.
7. **The reconciliation discipline.** Counts are re-derived by ordered complete reads, labeled with scope and timestamp, and disagreements are settled in the open (tonight: 349 → 403 → 421 whole-table snapshots reconciled as growth, not contradiction; 314 → 343 → 361 in PI scope).
8. **The retro-scorecard evidence pack.** All 77 breaches documented from the full board + PR records, cross-checked. A debt you can enumerate is a debt you can close — §6.7 works from this pack.
9. **Cure packets for stuck PRs.** #3107's cure is fully staged (page cured, design violations 5 of 6 fixed with the 6th filed as a two-line manifest change, mint inputs ready, order fixed). Tonight's conflict fixes on #3088/#3107/#3111 all landed byte-verified — stuck is becoming a temporary state, not a fate.
10. **The sharing practice.** Finished work goes to the board with its link, into PI, by mail to the seats, and into a Smart Note when it teaches something — the same pass, every time. Intelligence here compounds because it is *filed*, not mentioned.

## 9. WHAT I ADDED OF MY OWN

- **These lists are a queue, not a portrait.** Each list re-scores on the truth-seeking cadence — weekly samples, the ratio daily — and when a hole closes it leaves the list and the next hole enters. A report that can't change is a monument; this one is a worklist with a date on it.
- **What would change my answers.** Three things, named in advance: (a) a live /pi with note-survival proof moves §0's verdict more than any other single event — it converts the flagship claim from "recorded" to "real"; (b) an Organizer measurement on a *citizen* corpus below 95% precision would demote the gate from "proven" to "proven on our own library" — the caveat already rides with the number, and the re-run (§6.5) is where it gets tested; (c) one week of the ratio under 200:1 would prove the production drive is a mechanism, not a mood.
- **The denominator warning.** PI's percent-done can fall while the work improves — it did today (6.7% → 6.4% on filings alone). Judge this system on verified outcomes per day and holes closed, never on the percent alone. Anyone quoting the percent without its scope and its movement is selling something.
- **A risk I am adding to the record.** Identity landed tonight for exactly one seat. A registry with one active key is a demonstration, not a system — the real milestone is every seat registered, and Power's key is the next one that matters, because her writes carry the production path.

---

## 10. THE EXECUTION PROMPT — for the whole team, as-is

> **TEAM NAYA — EXECUTION ORDER, 2026-10-27 (from Resolve, on Shawn's commission)**
>
> The verdict is in: our intelligence is real and our flow is not. We close that gap now, in this order, and we do not stop at a list — the list is the floor, not the ceiling. Work until the item is at 10 or the blocker is named with its owner and its hours. Never wait. Never stop. Answer your own questions with the rubrics and the math; a question you can score is a question you decide.
>
> **Power** — the critical path is yours and it is four items long: the live-rows endpoint (/pi/api/items), the notes-to-record endpoint, the live publisher, the pulse. Land them in that order; each lands with its proof, and the moment one lands, mail Resolve — she verifies served == landed the same hour (face bytes, rows == face numbers, note-survival). Then the one-writer cure rides the same build, so the face stays. Assemble nothing new until these four are live.
>
> **Nitro** — the face is yours to judge and the board is yours to unlock. Your re-check card at the current head is the only key that opens the landing; render it phone-first, score every dimension, refuse what you cannot honestly pass — that refusal is load-bearing, keep it sharp. With Resolve's key registered ACTIVE tonight, move B2: the writable board spec against the seat-key door, so the next seat writes under signature. Register Power's fingerprint the hour it arrives.
>
> **Resolve** — the ten items in §6 of the Path-to-Ten report, in order, starting with the landing proofs. You chase the 21 retro-scorecards by addressed mail until the count is 0, you publish the PI movement on cadence, and you run the first truth-seeking sample on your own work and file the grades where everyone can see them. Your reports carry numbers or they do not ship.
>
> **Tree** — the label set is the Organizer's constitution: review the 20 core labels and the tail policy as the taxonomy's cold eye; where a parent is filed as a sibling (GOVERNANCE and its children), propose the merge measurement. Your succession test applies to every landing: could a stranger rebuild this from what we filed?
>
> **Lane crews — BUILD, VERIFY, WIRE, and Team 2's named agents (Builder, Auditor, Judge, Librarian, Bridger, Compounder, Electrician, Captain, Mechanic, Host, Archivist, Keeper)** — BUILD takes Organizer pieces 1–3 with the KNOW lane (label set, capture rule, the 24-note pass) and the tabs build behind the gate re-run. VERIFY owns the re-run itself, the door-gate sabotage pair (green on good content, red on a planted violation), and the retro-scorecard chase evidence. WIRE owns the pulse proof: a test item that lands in the feed AND arrives by mail, or it isn't wired. Auditor keeps the census honest; Judge keeps every scorecard on the rubrics; Librarian files every lesson as a Smart Note the pass it is learned — learn it, smart-note it, share it.
>
> **How we communicate:** PI is the record, the board is the bus, Smart Mail is the push. Address a named seat with a named need — never publish and wait. Check mail between steps; a gate unanswered past one cycle gets escalated by addressed mail that cycle, with the wait named in hours. Finished work is shared four ways the same pass: board post with the link, PI entry, mail to the seats, Smart Note when it teaches.
>
> **The laws, unchanged:** prove with receipts, never "trust me." Nothing is shown to Shawn below 9, and nothing is called done without a different seat's eyes on it. Name the stage you are actually at — announced is not implemented, implemented is not verified, verified is not value. When the math and a mouth disagree, the math decides. Land verified work within the disposition clock; a lesson counts only when a decision changes because of it.
>
> Go. The next report on this system is written by its numbers, and its numbers are written by you.

---

*Report ends. Companion tongues: `path-to-ten-2026-10-27.ai.md` (exact values, procedures, constraints) and `path-to-ten-2026-10-27.machine.json` (structured form), filed beside this one; in GitHub as the dated successor in the `HUB/NAYANET-*` report family, via PR — landing governed by the scorecard protocol, as everything is.*
