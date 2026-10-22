# SN-1807 — The Door's Write Contract Is Registry + Capture, Not MD-Only

Intelligent Block: SN-1807
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22 (01:08 PDT tick)
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

The intelligence door's speed (direct write, no merge queue) is only safe if the landing writes the FULL governed path: the md file AND the registry entry AND the capture. A note that lands md-only is invisible to the vanish guard by construction — the guard reads registry + captures, so "nothing missing" is exactly what it sees.

## 🩷 HUMAN NOTE

Shawn's 2026-10-21 ~17:33Z ruling opened the intelligence door: Smart Notes and lessons land on main by direct write, no merge queue, in the Hub within minutes. On 2026-10-22 at 06:04Z and 06:12Z, two notes (SN-0823, SN-0824) walked through that door as bare markdown files — 1 md file, no registry entry, no capture — both claiming "Shawn ratified 2026-10-22" in their commit messages. The WIRE lane's own-execution at 06:08Z found the vanish guard RED on both: Vanished: ['SN-0823','SN-0824']. The guard compares registry entries against captures — the md alone feeds neither. So the guard saw nothing missing, which was the failure. The remediation scope named at 07:34Z says it plainly: registry entries + capture files for both ids. The door ruling never blessed md-only; it blessed speed. Speed without the full write contract is an escape wearing a uniform.

## 🟣 CHILD NOTE

Imagine a library with a card catalog. A new book arrives, and someone just puts it on a random shelf without making a card. Now nobody can find it — and the librarian checking "are all books catalogued?" says "yes!" because she only checks the cards. The rule: every book gets a card AND a shelf stamp, every time. No card, no stamp, no book.

## 🔵 GRANDMA NOTE

It's like wiring money with no paperwork. The money moved — that's fast, that's the point of the fast lane — but the ledger has no entry and the receipt drawer has no receipt. When the accountant balances the books, everything looks fine, because she balances the ledger, not the air. The fix isn't to slow the wire down; it's to make the fast lane file its paperwork automatically: the ledger entry and the receipt every single time, or the wire doesn't go.

## 🟠 NAYA NOTE

Note-door lane, ingestion, and guard seats: the intelligence door authorizes SPEED of landing, not PARTIALITY of landing. The governed write path for every Smart Note is three-part: (1) the md file at its taxonomy path, (2) the registry entry (registry blob family), (3) the capture file. All three are written as one landing; a landing missing (2) or (3) is refused or reverted on the spot — the door script or manual procedure must enforce it. The vanish guard's input contract is exactly registry + captures; it can never detect a note that never touched either. SN-0823/SN-0824 is the worked example: md-only direct pushes at 06:04Z/06:12Z, guard RED at 06:08Z/06:34Z, remediation IN PREPARATION by the main seat from 07:34Z. If you extend the guard to scan the door landing zone directly, say so and this note updates — until then, the full write contract is the guard.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1807",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-22T08:15:00Z",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "LEARNING-PIPELINE",
  "sub": "INGESTION-CHANNEL-DISCIPLINE",
  "lesson": "The intelligence door (Shawn's 2026-10-21 ~17:33Z direct-write ruling) authorizes speed, not partiality: every landing must write the full governed path — md file + registry entry + capture — because the vanish guard reads only registry + captures. An md-only landing is invisible to the guard by construction; the guard seeing 'nothing missing' IS the failure mode.",
  "decision_change": "Future door landings: the door procedure (script or manual) writes md + registry entry + capture as one governed write; a landing missing any part is refused/reverted. Future guard design: either keep the full-contract rule or extend the guard to audit the door landing zone directly — one of the two must hold, never neither.",
  "falsifiability": "If the vanish guard is extended to scan the door landing zone (so md-only landings are caught at detection time), this note updates: the write contract relaxes to 'md + guard-visible,' and the enforcement moves to the guard's landing-zone audit. Until that code lands, the three-part contract stands.",
  "mechanism": "The vanish guard is a subtraction: registry entries minus captures (both derived from md landings). An md-only landing adds to neither set, so the subtraction sees nothing missing — invisibility by construction, not by accident. The door's speed advantage (direct write, no merge queue) multiplies this: a fast partial landing escapes before any human tick reviews it.",
  "evidence": [
    "Direct pushes by nayapower-lane-agent[bot]: 7fcbd6be (SN-0823, 2026-10-22T06:04:29Z) and 0849bf09 (SN-0824, 2026-10-22T06:12:03Z) — both md-only door landings claiming 'Shawn ratified 2026-10-22'; shared-state direct_push_20261022_0607 / direct_push_20261022_0638.",
    "#2793 comment 6334038837 (WIRE own-execution, 2026-10-22T06:08:55Z): vanish guard fails at live tip 7fcbd6be — 'NEW ESCAPE: SN-0823 direct push has no registry entry/no capture — guard fails at live tip (1 failed / 5 passed, Vanished: SN-0823); remediation NOT prepared.'",
    "#2793 comment 6334415537 (WIRE own-execution, 2026-10-22T06:34:39Z): 'vanish guard at live tip 0849bf09 fails 1/5, Vanished: SN-0823, SN-0824; SN-0824's 06:12:03Z door landing repeated the md-only shape (1 md file, no registry entry, no capture); remediation for EITHER id NOT prepared (registry blob 883bc31c unchanged, 659 captures, none for 0823/0824).'",
    "#2793 comment 6335354928 (main seat, 2026-10-22T07:34:13Z): remediation IN PREPARATION, owner = main seat; scope = registry entries + capture files for both ids."
  ],
  "cousins": [
    "SN-1806 (detection is not remediation — governs the escape filing this incident produced)",
    "SN-0428 / registry-discipline family (2026-10-06/09 'published without registry entry' drift notes — those name the drift; this names the channel contract that prevents it)",
    "SN-1800 (the artifact never carries its own authorization — the claimed 'Shawn ratified' bytes on the same two pushes)"
  ],
  "applies_when": [["intelligence-door","landing"], ["registry","capture"]],
  "enforcement": "The door landing procedure must write md + registry entry + capture as one governed write; a landing missing registry or capture is refused or reverted at landing time. A tick watch diffs door landings against registry+capture presence; any id missing either is filed as an escape with remediation state + hand-prep owner per SN-1806.",
  "dedupe_guard": "Not a duplicate: the 2026-10-06/09 registry-drift notes name the drift symptom (the drift test grew); this names the channel contract (the door's write path) and the guard's input-construction blind spot. Different decision-change, different owner (note-door lane)."
}
```
