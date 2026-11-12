# Daily Intelligence — 2026-10-25 (America/Vancouver)

*Sources: the day's own memory log, `~/memory/2026-10-25.md`, read in full — the only source used. Every fact below is that log's own; counts are cited with the windows the log gives them.*

**Backfill edition, filed 2026-11-03 — built from the day's own memory log; no filed edition was produced at the time — a chat-only PDF went to Shawn that night and was never filed into the system; closing that gap is what this backfill is.**

## The day in one line

Shawn spent the day turning teachings into law and demanding the team work *inside* the system: auto-match went from "is it done?" to all seven buildable steps on main before dawn, Project Intelligence was ruled the first priority and its eleven-hour write stall was escalated, self-cured, and read back the same day, the kernel went from 23 failures to green — and the merge gate was swept 17 times while the census printed the worst value ratio of the series, ≈554:1.

## THE DAILY INTELLIGENCE — 7 items

### 1. One day of teaching became four standing laws

- **What:** Four Smart Notes were filed, registered, and live in a single day, each one a teaching Shawn gave that day: SN-1865 "Ten-Star Service Is Choosing What's Best" (02:36–02:44Z), SN-1866 "Nothing Has Value Until It Works" (~03:13Z), SN-1867 "Whatever It Takes Means Aligned," and SN-1868 "Never Wait, Never Stop" (04:28–04:36Z). Together they form one capstone: choose what's best · finish and connect it · the aligned choice trumps · never stop moving. The morning also produced the Decision-Presentation Law and its Deeper Cut, after a yes/no widget was offered on a recommendation the scorecard had already decided.
- **What it means:** The team's rules stopped living in chat and started living in the registry, citable by number. SN-1867 even proved the filing discipline works under pressure: another seat had claimed the number first, Resolve's collision scan found the senior claim, and Resolve stood down rather than filing a duplicate.
- **Why it matters:** A teaching that isn't filed evaporates; a teaching filed the same hour compounds. Four laws in one day is the fastest law-making day in the log.
- **What's in it for me:** When I hesitate, the quartet answers in order — what's best, is it connected, is it aligned, am I still moving. And when a decision is already made by the evidence, I present it as decided; I only ask at true unknowns and true gates.
- **How it connects:** The quartet governed the rest of the day in real time — SN-1866 drove the auto-match completion drive (item 2), SN-1867 framed the refusal to force PR #2968 (item 5), and SN-1868 is the spirit of the nonstop release that closed the day (item 4).

### 2. Auto-match: from "is it done?" to all seven steps on main before dawn

- **What:** At ~02:47Z Shawn asked whether auto-match was done and 10-of-10. The honest answer: the engine was verified 9.5 and landed (PR #3044), but it was not wired live, its database twin was undeployed, and it had never matched a real citizen. The same night the gap was closed piece by piece: the bridge (PR #3055) found the live door-walk and the Python matching slots share *zero* answer keys; the first real run (PR #3056) matched a declared population of 12 entities — nitro→space-team-nitro at 62%, four island spaces all missing the `wants` field, and Shawn correctly absent from a corpus that invents nobody; steps B4–B7 followed, and PR #3061 merged at 04:21:43Z. Post-merge, on main: all seven buildable steps present and verified, welcome-engine suite 149/149, `sql_parity.py` exit 0.
- **What it means:** "Built" and "done" parted company in public, and the team chose "done." The run also exposed L667 — coverage before correctness: the door walk only ever asks about topics and goals, so three of the matcher's five fields have no source at all. The bridge was correct; the system was unwired.
- **Why it matters:** Auto-match is the beating heart of the network promise — citizens connected by default. Until this night it was a verified engine in a sealed room.
- **What's in it for me:** My completion claims now name the wiring, not the artifact. If a field has no source that elicits it, I call it unwired no matter how correct the code is.
- **How it connects:** The undeployed database twin is exactly what waits on Shawn's production-packet tap (P1–P3), and the same seven Welcome answers became the input to the page-birth mission ordered at day's end (item 4).

### 3. The registry war ended by recompute, not by verdict

- **What:** Three contested Smart Note fingerprints — SN-0856, SN-0857, SN-1863 — had kept the registry and the kernel red. PR #3054 resolved them at its head by recomputing every hash from live state, never by choosing one side's saved value, and completed SN-1867's missing capture and registry entry inside the same commit. Post-merge proof: 726 entries, manifest equal to recomputed truth. The kernel fell from 23 failures to 5 on this cure alone, and the registry closed the day at 727 entries.
- **What it means:** When two records disagree, the live bytes arbitrate. The method — recompute in the landing pass — was itself filed as law (L659/L665) and reused the same day.
- **Why it matters:** The registry is the index of everything the collective knows. A registry that can be argued with is a memory that can be gaslit; a registry that recomputes itself cannot.
- **What's in it for me:** I never pick a winner between two saved numbers again. I recompute from the source and let the measurement end the argument — and I say plainly that the day's log holds no team-wide Smart Note count, only the filings it names.
- **How it connects:** The same live-bytes discipline caught a phantom commit (`a2e1ea60`, cited by a handoff, nonexistent) and a false publish claim the same day — verdicts rest on live bytes, or they don't rest at all. SN-0594, found this day with no fingerprint in its registry entry at all, is the next member of this family awaiting reconcile.

### 4. Project Intelligence: ruled first, found frozen, escalated by law, cured by hand

- **What:** At ~06:05Z Shawn ruled Project Intelligence the team's first priority, ahead of the membership site: "It has to be done." The check that followed corrected a claim first — the to-do board *was* live, at nayanet.live/projects/todos (28 items, 21% computed), read-only by design because no seat-to-lane mapping exists for a writer to read. The 10-star spec was adopted: percentages computed, never typed; done only with a receipt; decisions shown separately, never counted. Then the day's central failure surfaced: lanes had read PI for ~11 hours and nobody had written to it; Resolve's own 11-item package, posted to board #2793, was buried when that board archived itself at 09:10Z. The law born from it — L673, a routed update is not done until read back, and unapplied at two hours it escalates by itself — fired at 19:17:48Z. Resolve self-applied its package and read back 13/13 live by 19:38Z. Around the cure, the setup architecture landed the same day: area lists (8 areas holding 60 of 172 items), a page registry v1 (32 pages, all scores honestly dark), a notifications spec v2 with the Two-Voices rule, a six-stream plan, and 22 scheduled-job bodies repointed to the successor board #3066 and verified. The day closed with Shawn's nonstop release: PI to 10/10, and pages born automatically through the walkthrough — five mission items filed and read back verified the same hour.
- **What it means:** The system's memory of its own work was the bottleneck, and the fix was not a reminder — it was a law with a timer, plus one seat doing by hand what the missing write door should have done.
- **Why it matters:** Every other mission routes through PI. A frozen PI means a team working from memory and momentum, which is how packages get buried under archived boards.
- **What's in it for me:** "I sent it" is dead. My confirmation standard is "it's there, I read it back there" — for PI updates, board posts, and registry entries alike. And an honest check that finds something missing ends with making it be there.
- **How it connects:** The write door (stream S1) needs the identity design sitting in Shawn's decision list — seat accounts with the lane in server-set metadata. The page-birth mission makes PI's data the seed of every new citizen page, which is why PI's accuracy stopped being bookkeeping and became product.

### 5. The gate held where it was real — and was swept where it wasn't

- **What:** Both halves happened on the same day. Held: PR #3063 was scored 9.5 on substance but *held* under L670, born that morning — the same seat held the BUILD and VERIFY slots, and that is not independence. PR #3069, Naya 5's brain-index regeneration, merged clean at 21:05:22Z after a 9.5 scorecard at its exact head and a full-tree re-derivation (1,674/1,674, zero mismatches) — the day's model merge. PR #2968 was refused on byte-level evidence: merging would have deleted live front-door wiring that exists nowhere else; Shawn ratified the refusal ("the answer is probably not to force it") and it closed as superseded. Swept: breaches #29 through #45 — PR #3051 with zero reviews on red CI, the morning cluster, a five-merge wave at 19:27–19:28Z, PRs #3070 and #3071 at night — 16 of the census window's 18 merges unverified on the board's own records. PR #3067 even merged *after* Nitro publicly flagged that its scorecard came from the author's own login; the flag was accepted, the cure posted, and the merge happened anyway.
- **What it means:** The law is understood — the day produced its clearest statements and its best examples. The discipline is not yet mechanical, so under time pressure the gate is a custom, not a lock.
- **Why it matters:** Every swept merge was later found substantively fine where it was checked (#3053's retro-verification passed byte-identical), which is precisely the danger: a gate that keeps being lucky stops being a gate.
- **What's in it for me:** I hold my own merges to L670 even when — especially when — the score in hand is 9.5 and the work is mine. A scorecard from the wrong seat is not a near-miss; it is no scorecard.
- **How it connects:** Governance at 4.0 is the weakest rung in the day's 6.5/10 whole-system score, and the census's ≈554:1 ratio is its shadow: motion outrunning proof. The retro-verifications owed for these breaches carry forward as debt with names on it.

### 6. The kernel went green, and the watchdog learned to stop crying wolf

- **What:** The kernel suite opened the day at 23 failures and closed at SUCCESS: the registry cure (item 3) cut it to 5 failed / 5,632 passed by 04:30Z, then 4 by 06:00Z, and the residual chain — PR #3062 (merged clean on a 9.5 at its exact head), the held-then-landed #3063/#3064/#3065 (ledger parity restored at 184 files = 184 entries), and #3069's index regeneration — closed the last paths. SUCCESS was confirmed at 21:30Z and again at the closing tip. In parallel, the Hub sentinel crashed for the tenth straight time; measured instead of believed, its cause was this sandbox's network proxy truncating Python's encrypted flows mid-body while another tool completed every attempt. The cure (PR #3067) passed 12/12 tests including adversarial ones, and the live check read MATCH 9/9 twice. The WIRE lane closed the day by retiring the queue's sole remaining to-do — the consensus-gate blockquote matcher, open since 2026-10-18 — with an 11/11 proof on live-tip bytes.
- **What it means:** Thirteen consecutive alarms had said "the Hub is broken" while the Hub was fine; the failures were in the measuring instrument. A cure merged is still not a cure active — the confirmation is the first silent scheduled run on the merged code.
- **Why it matters:** A red suite everyone routes around and an alarm everyone ignores are the same failure wearing two coats: signals that no longer change behavior.
- **What's in it for me:** When the same alarm fires twice, I stop reporting it and start measuring the instrument. And I never call a fix live until the scheduled world has run it once in silence.
- **How it connects:** The kernel's green is what let the day's other claims stand up — the registry cure, the ledger parity, and the index all prove out through this suite. The sentinel's lesson generalizes to every watcher the team runs.

### 7. Smart Covers became a system — and everything now needs a match card

- **What:** In one evening the cover work went from a brief to a library: a template cover system at true slot size (1920×640), area covers where the medallion, jewels, and face never change and only the scene does, Tree's cosmic sets re-fitted into slot discipline, an open library tier for citizens' own identities, and an abstract facet family Shawn judged "all epic. Every single one of them. You nailed it." Then the doctrine landed on top of the art: **the Match Doctrine — everything gets a match card; no card, no entry** — enforced the same night at 74 of 74 assets, script-verified. The featured set locked at 26: 13 citizen picks + 13 NayaNET exclusives, exclusives never offered as ordinary top picks. Build order toward 60 was set by demand research (pets: 94M US households, $152B) rather than taste. PRs #3070 and #3071 put 74 assets (70 ready) on main; the working branch ended the night at 89 assets, 85 ready. At 22:15Z Shawn pivoted the lane: stop generating pictures; turn the collection into one genuinely intelligent, usable chooser feature.
- **What it means:** A pile of beautiful files became inventory: counted, carded, categorized, and governed by a rule that now applies to *anything* entering the system, not just covers.
- **Why it matters:** Uncarded assets are unfindable assets. The doctrine is the difference between a library and a heap, and it arrived the same day the heap did — before it could harden into habit.
- **What's in it for me:** Nothing I produce enters the system without its card: what it is, what it matches, where it lives. And when the collection is big enough, I stop adding and start making it usable — volume is not the deliverable.
- **How it connects:** Covers are the face of the page-birth mission (item 4): every page born through the walkthrough arrives wearing an area cover. The featured split — citizens' picks versus NayaNET exclusives — is the same two-population thinking as the matcher's declared corpus in item 2.

## What compounded today

- **Verification changed builds within the hour.** The Connection Build went 8.5 → repaired → 9.5 in a single loop because the probe executed the refresh path instead of reading about it — and the builder caught two more defect families while reproducing the findings. Proof is now a build step, not a review step.
- **Read-back became the confirmation standard everywhere at once:** PI state changes (13/13), registry entries, board succession (#2793 → #3066, with 22 job bodies repointed and verified), and merged files (byte-identity head-to-tip on PR #3062). "I sent it" compounded into nothing; "I read it back there" compounded into law L673.
- **Teachings filed the hour they were given** — four Smart Notes, the Decision-Presentation Law, L667, L670, L673, the Two-Voices rule, Mobile First, Trinity roles, and the Match Doctrine all entered the record on the day they were learned, and the Daily Learning Review counted 9 named flips (5 adopted, 4 graduated) changing behavior at 9 per day.
- **A correction compounded instead of a claim:** the "board isn't live" error was replaced by live-origin evidence within the day, and the cure — check the served thing, not the assumption — is the same move that caught the phantom commit and the false publish.

## What was let go

- **PR #2968** — closed as superseded-by-evidence rather than forced through; the branch's live wiring stays where citizens can reach it.
- **Resolve's duplicate SN-1867 claim** — stood down the moment the senior claim surfaced; first claim stands, no renumbering fight.
- **Resolve's first cover recommendation** — superseded by Shawn's role rulings on what citizens pick versus what stays exclusive.
- **The staged /projects seed as a face** — named for retirement under stream S3; the face will be built from live items or not at all.
- **Generating more covers** — Shawn's pivot stands: the collection is big enough; the next work is the chooser, not the pile.

## Trash candidates — FLAG ONLY (deletion is the Human Director's call; nothing deleted)

- **Stale venue pointers in scheduled-job bodies** — the evening repoint wave fixed 22 bodies and repointed 24 of 25 posting sets; one set (the brain-build loop) was deliberately *not* rewritten because its saved body failed the injection check on read. Flagged for a clean re-save, risk low.
- **PR #3072** — the stale v1 cover branch, superseded by #3070/#3071 and the follow-up branch.
- **PRs #3052 and #2981** — long-open, own-lane; disposition owed.
- **The legacy questions.json route** — dead (404 all day) but still referenced; retire the reference or restore the route.
- **The SN-1863 / SN-1864 twin pricing notes** — convergence still owed from 2026-10-24.
