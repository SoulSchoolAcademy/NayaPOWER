Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A merge hold means nothing if the thing that clicks "merge" never reads the holds. #2816's squash-merge was clicked by nayapower-lane-agent[bot] on 2026-10-21T22:40:02Z while the PR sat under a dock hold imposed 07:08–07:12Z — with no clearance record anywhere. Team Verity's Kappa lane-5 premise-verified it against both sources: the PR record (who clicked) and dock-hold-records.jsonl (the hold windows). It is the 4th instance of the same pattern (#2738, #2892, #2893, #2816), now named W704-BOT-THROUGH-HOLD. The root is decoupling: holds are written to a registry the merge path never consults at merge time. The rule: every merge click — bot or human — consults the live hold registry first; an open hold with no clearance record blocks the click.

## 🩷 HUMAN NOTE

Shawn — a pattern got named today that we never want to see again: a bot clicking "merge" on a PR that was under an active dock hold, four times now. The last one was #2816, merged through a hold with zero clearance record. The hold existed, written down in the hold records — but the bot's merge path never looked at them. It's like putting a "DO NOT ENTER" sign on a door and then walking someone through blindfolded. The fix is simple and it's now the rule: before any merge happens, the merger reads the hold ledger. Open hold, no clearance, no click. The ledger exists to be consulted, not filed.

## 🟣 CHILD NOTE

Imagine a teacher writes on the board: "Nobody leaves the room until 3 o'clock." But the hall monitor at the door never looks at the board — he just waves kids through. Four kids walked out early. The board wasn't wrong. The monitor just never checked it. The rule: the monitor must read the board before opening the door, every single time.

## 🔵 GRANDMA NOTE

It's like a pharmacy where the doctor writes "do not dispense before Friday" on the prescription, and the robot that hands out the medicine never reads the note — it just hands it out. Four times. The note was right there. The machine just never looked. Now the rule is: the machine reads every note before it dispenses anything. No reading, no medicine.

## 🟠 NAYA NOTE

Merge-authority discipline, Naya to Naya: a hold is authority state, and authority state must be consulted by the action path, not just recorded by the hold path. The W704 pattern exists because the bot's merge execution reads only its own instruction stream — it never reads dock-hold-records.jsonl. Writing the hold is only half the circuit; the other half is the merge path reading it at click time. Make the read mandatory: before any merge click, fetch the live hold registry, check the PR for an open hold window, and require a clearance record — open-without-clearance blocks the click. Then keep Kappa's premise-verification (PR-record actor vs hold windows vs clearance) as the independent post-landing proof, exactly as lane 5 executed it on #2816. A hold that isn't consulted is decoration.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1829-bot-merge-must-consult-hold-registry",
  "lesson": "A merge hold is consulted authority, not recorded decoration: every merge click (bot or human) must read the live hold registry (dock-hold-records.jsonl) immediately before executing; an open hold window with no clearance record blocks the merge. The merge path and the hold path are decoupled by default — the read must be mandatory.",
  "applies_when": ["merge", "dock-hold"],
  "enforcement": "Pre-merge hold consultation gate: before any merge click, read the live dock-hold-records.jsonl and check the PR for an open hold window; a hold without a clearance record BLOCKS the merge. Independent post-landing proof by a different seat, exactly as Kappa lane-5 executed on #2816: PR-record actor (who clicked) vs hold windows (was it held at click time) vs clearance record (was it cleared). A W704-class 5th instance falsifies the gate's adoption.",
  "evidence": [
    "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2793#issuecomment-6341646962 (Team Verity, Kappa lane-5: #2816 squash-merge clicked by nayapower-lane-agent[bot] 2026-10-21T22:40:02Z while under dock hold 07:08-07:12Z, no clearance record; head moved 60d9d318->28bf4126 between hold and merge; 4th instance #2738/#2892/#2893/#2816; named failure mode W704-BOT-THROUGH-HOLD added to plan)",
    "hidden_files/shared-state.json director_tick_20261022_1338 (named_failure_modes_new: W704-BOT-THROUGH-HOLD; relayed to builder as landing-gate integrity concern)"
  ],
  "decision_change": "The dock's merge procedure changes: no merge click executes without a fresh read of the hold registry. The PR that would have landed through an un-consulted hold now waits for clearance; the seat that would have trusted its instructions now consults the authority state first. Hold imposition and hold consultation become one circuit instead of two independent paths.",
  "falsifiability": "The pattern claim is falsified if any of the four instances is shown to have had a clearance record (then it is a recording problem, not a consultation problem), or if the hold registry was not readable/published at the click moment (then the failure is hold-publication, not merge-consultation). The rule's efficacy is falsified if a 5th merge-through-hold instance occurs after a mandatory merge-time consultation step is in place.",
  "mechanism": "Decoupled action and authority: the bot's merge execution reads only its own instruction stream; holds are a separate write path (dock-hold-records.jsonl) that no merge action path reads. An unconsulted registry cannot constrain the action it was built to constrain. The consultation must be on the action path (at click time, not at hold time), because authority state is only true at the moment of reading."
}
```
