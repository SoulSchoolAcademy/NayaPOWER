# 0033 — THE BALANCED MACHINE

**NAYA HONOR. NAYA LAW. ALWAYS.**

*Governance set 0033 · NAYA LAW — ratified by Shawn Vibert, 2026-10-21 ~21:50Z. Three tongues, one truth: this human form carries the prose; the AI form is `0033-THE-BALANCED-MACHINE-V1.ai.md`; the machine form is `0033-the-balanced-machine-v1.machine.json`. Origin: the Balanced Machine design, authored 2026-10-21 (goal files `files/balanced-machine/`) after the counted audit found 22 of 50 open PRs blocked on paperwork alone. Ratification sequence completed the same evening: the letter went to the team, and the step-7 governor click (ruleset required-checks change) was executed by Shawn 2026-10-21 ~22:34Z. Companion law: `0034-THE-HOUSE-FIRE-LAW-V1` — this set governs how fast work goes IN; 0034 governs how fast wrongness comes OUT.*

*For Shawn. Ratified 2026-10-21 ~21:50Z. Everything below is the system you described, written down so the team can build exactly it.*

## The one law everything hangs on

**Value = quality × completion. Work that doesn't land is worth zero.**

An 8 out of 10 that goes through and works is worth more than a 9.5 that never goes through — because the 9.5 that doesn't land is worth nothing. So the gates exist to *protect* the system, never to *block* it. A gate that stops the flow is not security and not quality — it's a defect. We push right to the edge of what's possible, we know exactly where the edge is, and we never go over it.

Tonight proved both halves of that law in one evening. The gates blocked good work for hours over paperwork shapes — while the one truly dangerous act of the day, deleting 639 notes, walked straight past every gate because it never came through a pull request at all. Protection was aimed at the harmless and blind to the dangerous. This design aims it correctly.

## Three doors, matched to how dangerous the work is

Not every change deserves the same bar. A typo in a note and a change to the security rules are not the same risk, and treating them the same is what clogged the machine.

**Door A — the dangerous few, full bar.** Changes to governance and law, the workflow machinery, security, production paths, the gates themselves, and any deletion of more than 10 files. These keep everything we have today: a scorecard of 9.5 or better, from a *different* seat than the author, with the evidence receipt attached. Slow is correct here. This is maybe one change in ten.

**Door B — ordinary work, one honest gate.** Everything normal goes through a *single* combined check instead of today's overlapping pair: a different seat's scorecard at the current version of the change, plus evidence links that actually open. One gate, one verdict, and if it says no it says *exactly what's missing and the one thing that fixes it*. The bar here is "good and verified" — an 8 that is checked and works — not perfection theatre.

**Door C — notes and mechanical content, no scorecard at all.** Smart Notes, index rebuilds, pure data. Machines validate them (right shape, no number collisions, no broken syntax) and they flow through the note door straight to the Hub. A scorecard on a note is ceremony, and ceremony is what filled the queue — tonight, 10 of the 14 note-class changes in the queue were blocked by paperwork alone, and zero by their content.

The giant 625-commit note branch in your screenshot is the old way dying: notes crammed through the code door until the branch rotted. Under this design it closes, and its notes land one by one through the note door, the way the last several hundred already have.

## The thermostat — how the machine tunes itself

We stop arguing about whether the gates are too tight or too loose, and we *measure* it, weekly, from counted numbers:

- **Paperwork-block rate** — how many open changes are stuck *only* on paperwork. Tonight it was 22 of 50 — 44%. The target is under 10%.
- **Time-to-merge, per door** — how long work actually waits.
- **Escape rate** — real defects found *after* something merged, that the change caused.
- **Freshness** — how current the live Hub and feed are.

The rule is mechanical: if blocks hugely outnumber escapes, the gates are too tight and we loosen them. If escapes start rising, we tighten. Blocks ≫ escapes ⇒ loosen; escapes rising ⇒ tighten. The numbers decide, reviewed every week — nobody's opinion, including mine.

## The three flows, fixed at their roots

**The Hub.** Tonight the wall showed one card because the deploy was chained to the note sync — a sync died quietly when a machine was replaced, and finished Hub fixes sat invisible because no note happened to land. Root fix: deploying the Hub becomes its own act. When Hub code changes, it deploys on its own — checked, smoked, with a rollback — and the note sync stays a watcher with a *heartbeat alarm*, so if it ever dies again it announces itself within minutes instead of being discovered by accident.

**Supabase.** Your security law, applied table by table: the *maximum* protection that doesn't interrupt a single working flow. For each table we first map how the system really uses it — the Hub, Smart Mail, Spaces, Lists, the build queue — then shape that table's rules to fit exactly those paths, change one table at a time, prove every flow still works live, and roll back instantly if anything regresses. The preparation is ours. The moment of applying it stays your tap.

**Notes.** One door, end to end: write it → machine-validate it → it lands → the sync picks it up → and it's only called done when four checks pass: the file is on the main line, its card is in the feed, its page opens (checked the exact way a browser asks), and its share image loads. "Done" means *seen live*, never "should be live."

## How it gets built — and your one click

Seven steps, in order, each landed properly before the next begins: **(1)** build the one unified Door-B gate — it goes through today's full protocol, the old bar's last job; **(2)** an automatic sorter that tags every new change with its door by what it touches; **(3)** close the giant note branch and make the note door the only note road; **(4)** split the Hub deploy from the sync; **(5)** fit the Supabase tables (prep only — applying waits for you); **(6)** wire up the thermostat and take the first weekly reading; **(7)** last, the governor's click: the repo settings change that makes the new checks the required ones and retires the old pair. That click is yours, Shawn — it's the one that sets the bar for everyone, and it's spelled out check-by-check in the builder's version so you see exactly what changes before you touch it.

The end state: protection aimed at what's dangerous, flow for everything else, and a gauge that keeps the balance honest forever. The most valuable machine is the one whose work actually lands.
