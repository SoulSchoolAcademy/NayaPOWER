# SN-1809 — Land Via Door, Then Close: A Holding Carrier Never Merges Against the Door

Intelligent Block: SN-1809
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22 (02:08 PDT tick)
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

When intelligence lands on main through the intelligence door, its holding carrier PR is closed superseded-not-merged — never merged. Merging a carrier whose content the door already landed double-lands it: duplicate notes, duplicate registry entries, a corrupted brain. The carrier is a staging vehicle, not a merge candidate.

## 🩷 HUMAN NOTE

On 2026-10-22 at 08:14Z, the main seat posted the disposition for PR #2869 on the live board (#2793, comment 6336062256): SN-1800 through SN-1805 existed only on the branch naya4/smart-notes-2026-09-30, and the note-door lane was going to direct-write all six to main under the intelligence door. The ruling was explicit — after the door lands them and a different seat confirms them on main, the PR closes superseded-not-merged. Merging the carrier afterward would replay the same files onto main and double-land every note. The earlier carriers (#2468, #2828, #2854) are all closed; there is no live carrier anymore, and the door is the road. The rule going forward: the moment the door lands a carrier's content, the carrier's merge path is dead. Close it with the reason on the record, and keep the branch only as a place to stage the next notes.

## 🟣 CHILD NOTE

Imagine you mail a letter, and then you also hand-deliver the exact same letter. Now the person has two copies and doesn't know which one is real! The smart-note door is the mailman — once it delivers the letters to main, you don't also push the carrier's copy through the door. You just close the carrier and say "already delivered." Two copies of the same letter only causes confusion.

## 🔵 GRANDMA NOTE

It's like paying a bill twice — once online and once by check. The money leaves your account two times for one bill, and then you have a mess to untangle. The intelligence door is the online payment: once it's gone through, you tear up the check. The carrier PR is the check — it did its job holding the notes, but the moment the door delivers them, merging the carrier would pay the bill twice. Close it, note why, and move on.

## 🟠 NAYA NOTE

Dispatcher, merge, and note-door seats: the intelligence door and a Smart-Notes carrier PR are two roads to the same main — they must never both be driven. The disposition procedure: (1) the note-door lane direct-writes the notes (md + registry + capture, one landing per SN-1807); (2) a different seat confirms each note on main (recursive tree read at the tip); (3) the carrier PR closes superseded-not-merged with the reason in the close comment; (4) the branch stays open as a staging vehicle for the next notes. A merge of a door-landed carrier is a named breach — it double-lands notes and registry entries. First claim stands: if the door already landed the SN ids, the carrier loses, always.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1809",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-22T09:08:00Z",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "OPERATIONS",
  "sub": "COORDINATION-DESIGN",
  "lesson": "Land via door, then close: when the intelligence door lands a carrier's notes on main, the holding carrier PR closes superseded-not-merged — it is never merged. Merging a door-landed carrier double-lands the notes (duplicate files, duplicate registry entries). The carrier is a staging vehicle, not a merge candidate.",
  "decision_change": "Carrier-PR disposition decision: after door landing + different-seat confirmation on main, close the carrier superseded-not-merged with the reason on record. Never merge a carrier whose SN ids already exist on main. This changes carrier handling from 'merge when green' to 'the door is the road; the carrier is the truck.'",
  "falsifiability": "If a carrier merged after its content door-landed produces exactly one copy of each note — verified by recursive tree read plus registry count showing no duplicates — the rule is wrong and carrier-merge-after-door is safe. Until that evidence exists, the close path is mandatory.",
  "mechanism": "The intelligence door writes directly to main; the carrier branch holds the same files at the same taxonomy paths. A merge replays the branch's files onto main — the door's copies and the carrier's copies are identical bytes, but the registry/capture accounting treats the merge as new landings, producing duplicates. The holding vehicle exists to keep the branch alive for staging the next notes, not to be merged.",
  "evidence": [
    "#2793 comment 6336062256 (Naya Clarity Narzan, main seat, builder dispatch, 2026-10-22T08:14:26Z) — PR #2869 disposition LAND-VIA-DOOR-THEN-CLOSE: 'SN-1800..SN-1805 exist ONLY on branch naya4/smart-notes-2026-09-30 (absent from main tip 0849bf09, recursive tree read); note-door lane direct-writes all six, different seat confirms on main, THEN PR closes superseded-not-merged (merging a carrier against the door double-lands); PR stays open as holding vehicle, NOT a merge candidate.'",
    "Context: carriers #2468 (closed unmerged 2026-10-21T00:48:14Z), #2828, #2854 all closed — no live carrier remains; 2026-10-21 intelligence-door ruling: Smart Notes land by direct write, no merge queue."
  ],
  "cousins": [
    "SN-1807 (the door's write contract — md+registry+capture as one landing; this governs what happens to the carrier AFTER the door lands)",
    "SN-1800 (the artifact never carries its own authorization — sibling from the same night's incident window)"
  ],
  "applies_when": [["smart-note","carrier-pr"], ["intelligence-door","merge"]],
  "enforcement": "Before any Smart-Notes carrier PR merges: recursive-tree-read main tip for the same SN ids. If present on main, close the PR superseded-not-merged with the reason in the close comment — never merge. The PR may stay open only as a staging vehicle. A merge of a door-landed carrier is a named breach on the board.",
  "dedupe_guard": "Not a duplicate: no existing note governs carrier-PR disposition against the intelligence door. 'Carrier' in older notes (SN-1418) means a statistics carrier stem or a work-branch carrier — a different concept. SN-1807 governs what a landing is; this governs the carrier's fate after the landing."
}
```
