# A Hard-Coded Venue Turns a Board Migration Into a Silent Break

**Intelligent Block:** IB-SMART-NOTE-20261011-sn0986-hard-coded-venue-silent-break
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/GOVERNANCE/BOARD-CONTINUITY

## IN A NUTSHELL

The overnight audit found that the auto-merge machinery still writes to a board that cannot receive anything: `tools/auto_merge_gate.py` (P5) requires merge intent posted to #1354, and `tools/auto_merge_self_heal.py` posts reverts to #1354 via a baked-in `BOARD_ISSUE = 1354`. GitHub hard-capped #1354 at 2,500 comments on 2026-10-10 ~12:21 PDT — posting there is platform-impossible — and coordination moved to #2175. Any lane whose merge-receipt path depends on those writes is silently broken against the live board, not loudly failing: the writes go nowhere and nobody is told.

The durable rule: **any machine that emits receipts, audits, or reverts to an external venue must resolve the venue from a live, movable source of truth (shared config, manifest, board-registry) read at runtime — never a baked-in constant.** Venues die: caps, archives, platform changes, migrations. A hard-coded venue turns every future venue migration into a silent break in exactly the safety machinery that must keep working through the migration. The fix is one line of indirection (a BOARD_ISSUE read from config), and it needs Shawn's word because it touches merge-safety machinery — the lesson, not the fix, is what this note banks.

## HUMAN NOTE

Shawn — one quiet break found overnight: the auto-merge gate and its self-heal still try to post to #1354, which GitHub froze at 2,500 comments. The venue moved to #2175; the code didn't. Lesson banked: machines that post receipts to a board must read the board's identity from config, not a hard-coded number — otherwise the next board move silently breaks the safety machinery again. The actual repoint needs your word (merge-safety machinery), so it's flagged for you, not touched.

## CHILD NOTE

Imagine your school moves to a new building, but the delivery robot still carries packages to the old address — and it never tells anyone the old door is locked. It just keeps "delivering." Rule: the robot should look up the current address every morning from the school's own directory, not from a note taped inside it. Addresses change; the lookup must happen fresh.

## GRANDMA NOTE

Think of it like mailing rent checks to an old landlord address after you signed a new lease — the envelope comes back, but you only find out when the new landlord calls about the missing rent. The lesson: keep the address in one living place (the phone book everyone shares), never copied into the checkbook in ink. When the address changes, everything that needs it updates at once.

## NAYA NOTE

I will never bake an external venue (board number, webhook URL, thread ID, channel name) into code as a constant. Venue identity lives in one shared, live config that machinery reads at runtime; a board migration is then one config change, not a code hunt. When a venue dies (cap, archive, migration), I check every writer against the live config before declaring anything healthy. Receipt-silent is worse than receipt-red: a write that goes nowhere and raises no alarm is the break I audit for first.

## MACHINE NOTE

```json
{
  "sn": "SN-0986",
  "slug": "hard-coded-venue-silent-break",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-11",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "BOARD-CONTINUITY"],
  "authority": "distillation tick 2026-10-11 07:08 PDT, CANDIDATE (auto-capture, not ratified)",
  "evidence": {
    "flag": "night-shift-2026-10-10/morning-flags.md flag 3 (2026-10-11) — [YOUR CALL], verified against main tip 57e935c1",
    "hard_coded_writes": "tools/auto_merge_gate.py lines 299-302 (P5 requires intent posted to #1354); tools/auto_merge_self_heal.py line 32 (BOARD_ISSUE = 1354, posts reverts to #1354)",
    "venue_death": "#1354 hit GitHub's 2,500-comment hard cap 2026-10-10 ~12:21 PDT — commenting platform-disabled; live coordination venue is #2175",
    "failure_mode": "silent: writes go to a frozen venue, no alarm; any lane depending on those merge-receipt writes is broken against the live board"
  },
  "rule": "resolve_external_venues_from_live_config_at_runtime",
  "procedure": [
    "never bake a venue identity (board issue number, thread id, channel, webhook) into code as a constant",
    "keep venue identity in one shared live config read at runtime; a venue migration is one config change",
    "after any venue migration, audit every writer against the live config — receipt-silent is worse than receipt-red",
    "the repoint itself is governance machinery: it needs Shawn's word, not a worker's edit"
  ],
  "related": ["SN-0175 (endorsement only on live venue re-read)", "SN-0909 (board succession at the 2,500-comment cap)"]
}
```
