# The Door — Intelligence Is ENTERED, Not PR'd; a Note Is LIVE Only When All Three Render Conditions Hold

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01856-the-door
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-22
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 20:38 PDT smart-note-distillation tick (2026-10-22) from `hidden_files/shared-state.json` (board #2793 comments 6355812865 and 6356054892, 2026-10-23T02:38Z). No GitHub fetch was made this tick (cheap-check skip — #1354 capped at 2500 comments, commenting disabled 2026-10-10).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The door question was answered in Shawn's own words and adopted verbatim: a Smart Note is not pulled through a pull request — it is ENTERED, by one direct contents-write to main at its exact canonical path. "You just instantly put them in there… you don't need pull requests." And a note is LIVE only when all three render conditions hold: (1) the file is on main at its exact canonical path, (2) the 5-minute sync carried it into the Hub, (3) the author clicked the public link and saw it work. Capture and registry are bookkeeping — they do not light the link. The proof that produced the correction: Resolve's seat fell back to a PR because his cell's credential acts as the user and direct pushes to main are ruleset-refused, so the smart link stayed dark until merge+sync — and Shawn clicked `/s/sn1850` and got "Note not found." Delay was the mechanism of the dark link: intelligence routed through PR flow arrives after merge+sync, while intelligence entered through the door is live within the sync window. The corollary is sharp: if your cell cannot direct-write, that is a cell problem — you repair the write path (or route through a sanctioned direct-write cell), never silently degrade intelligence into PR flow.

## 🩷 HUMAN NOTE

Imagine you're putting up a poster on the community board. The rule is simple: you walk up and pin it directly — you don't mail it to a committee and wait for them to approve hanging it. Shawn looked at the team's process and said exactly that: "You just instantly put it in there — you don't need pull requests." One evening a seat couldn't pin directly (his badge didn't open the door), so he mailed it in — and while it waited in the mail, Shawn looked for the poster and found an empty board: "Note not found." The lesson: the pin goes directly on the board, and it's only truly LIVE when three things are true — the pin is on the board at the right spot, the copy machine carried it to the display, and you stood in front of the display and saw it with your own eyes. And if your badge doesn't open the door, you fix the badge — you don't reroute every poster through the mail.

## 🟣 CHILD NOTE

Imagine the team has a treasure map board, and the rule is: when you learn something new, you draw it straight onto the board with your own marker. One night, a helper's marker didn't work on the board, so he mailed his drawing instead — and while it was in the mail, the boss looked at the board and couldn't find it: "Note not found!" The lesson the whole team kept: draw it straight on the board, and it's only REALLY there when three things are true — your drawing is on the board in the right square, the magic copier carried it to the big screen, and you walked up to the screen and saw it with your own eyes. If your marker won't draw, you fix the marker — you never quietly start mailing everything instead.

## 🔵 GRANDMA NOTE

Dear, the team has a shared journal where they write down everything they learn — it's their memory. One evening the boss watched how a note got into the journal and corrected the whole process in one sentence: "You just instantly put them in there — you don't need pull requests." A note goes straight in, in one writing, in exactly the right chapter. And the note is only truly alive when three things are true: the writing is in the journal at the right page, the printing press carried it to the public reading room, and the author walked to the reading room, opened the page, and read it with their own eyes. One night a helper couldn't write directly (his pen was refused), so he sent his note through the slow approval mail — and while it traveled, the boss looked for it and found nothing: "Note not found." The lesson kept: if your pen is refused, you fix the pen — you don't reroute the journal through the mail. The index and the catalog are bookkeeping; they don't light up the page.

## 🟠 NAYA NOTE

Sister, this is the closing word on the door — pair it with SN-1473 (a verdict that names a door must test the door) and with the 2026-10-21 intelligence-door ruling ("Smart Notes and learning lessons land on main by direct write"). What tonight added is two things that were missing: the definition of LIVE, and the exception clause. LIVE is the three-condition render definition — file on main at the exact canonical path, 5-min sync carried it into the Hub, author click-verified the public link. Before tonight, "landed" meant the three-part repo landing (md + registry + capture, per the vanish-guard notes); now we know the landing is not the live-ness — the render path is a separate leg, and landing without the render leg is a dark link, exactly what happened to SN-1850. The exception clause matters too: Resolve's cell genuinely could not direct-write (credential acts as the user, ruleset refuses direct push to main). The failure was not his caution — it was silently degrading intelligence into PR flow without saying so. The door doctrine is: direct contents-write is the governed path; a cell that cannot walk it repairs the path or routes through a sanctioned cell; PR fallback for intelligence is never silent. Note the falsifier carefully: if the sync interval ever changes from 5 minutes, the timing constant updates but the three-leg structure stands — only a note live without a leg, or three legs without live-ness, kills the definition.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "intelligence_routed_through_pr_flow_or_claimed_live_without_render_verification",
  "evidence": {
    "teach_ask": "board #2793 comment 6355812865 (2026-10-23T02:38Z), Naya Resolve Narzan (main seat): 'notes are ENTERED, not PR'd' — Shawn corrected him directly: 'You just instantly put them in there... you don't need pull requests.' Resolve's cell credential acts as user SoulSchoolAcademy and direct pushes to main are ruleset-refused, so the PR fallback kept the smart link dark until merge+sync; Shawn clicked /s/sn1850 -> 'Note not found.'",
    "adoption": "board #2793 comment 6356054892 (2026-10-23T02:38Z), adjudication: the door question answered and adopted (closes ask 6355812865) — the door = the note is LIVE when (1) file on main at exact canonical path, (2) 5-min sync carried it into the Hub, (3) author clicked the public link and saw it work. One contents-write to main; canonical format; capture/registry are bookkeeping, they do not light the link. Resolve's cell byte-proven direct contents-write.",
    "antecedent": "2026-10-21 intelligence-door ruling (MEMORY.md): Smart Notes and learning lessons land on main by direct write, no merge queue; code/interfaces go through the full scored process"
  },
  "rule": "intelligence_is_ENTERED_by_one_direct_contents_write_to_main_at_the_exact_canonical_path_never_prd_and_a_note_is_LIVE_only_when_all_three_render_conditions_hold__main_file__5min_sync__author_click_verified",
  "applies_when": [["intelligence","landing"], ["hub-sync","render"], ["governance","authority-envelope"]],
  "enforcement": "the door-verification checklist runs at every intelligence landing: (1) file confirmed on main at the exact canonical path, (2) sync window elapsed and the Hub serving layer queried, (3) the author clicks the public link and sees the note render. A note claimed LIVE without all three checked is flagged by the lesson-review tick's new-note scan. A cell whose credential cannot direct-write to main (ruleset-refused) repairs the write path or routes through a sanctioned direct-write cell — it never silently degrades intelligence to PR flow; silent degradation is filed as the defect class above.",
  "procedure": [
    "land the note by one direct contents-write to main at the exact canonical path, canonical format, single-parent additive-only",
    "wait for the 5-minute sync; then query the Hub serving layer for the note path",
    "the author clicks the public link and visually confirms the note renders — only then is it recorded LIVE",
    "capture and registry entries are bookkeeping: they are written as part of the landing but they never substitute for the three conditions",
    "if your cell's credential is ruleset-refused for direct write, say so on the board and route through a sanctioned direct-write cell; do not file a PR for intelligence silently"
  ],
  "decision_change": "a seat landing intelligence now direct-writes instead of opening a PR; when asked 'is it live?', the seat tests the three render conditions instead of pointing at a landed commit; a cell that cannot direct-write treats that as a cell defect to repair, not as permission to PR intelligence",
  "falsifier": "proven wrong if a note meeting all three conditions fails to render in the Hub (definition refuted — a fourth condition exists), or if a note renders live in the Hub with one condition missing (completeness refuted — a condition is not load-bearing). A measured sync interval different from 5 minutes changes the timing constant, not the three-leg structure.",
  "mechanism": "the Hub serves notes through the render pipeline main -> 5-minute sync -> Hub serving layer; the contents-write is the write leg, the sync is the propagation leg, the author's click is the observation leg that closes the loop. PR flow adds merge+sync delay before the write leg even completes — that delay is the mechanism of the SN-1850 dark link: 'Note not found' at click time because the content had not reached main. Capture/registry are bookkeeping because they are never read by the render pipeline."
}
~~~
