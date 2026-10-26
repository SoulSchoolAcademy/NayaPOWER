Intelligent Block: SN-2008
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-26
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE
Title: A deploy that ships a whole folder ships its stale files too

## ✦ IN A NUTSHELL
Deploy scope is a correctness property, not a convenience setting. A workflow triggered on a whole folder ships every file in that folder — including a stale copy that overwrites a live surface. On 2026-10-26 a Project Intelligence face landing shipped the frozen home copy sitting in HUB/app/ alongside the face, overwriting the live home twice, and a board-declared freeze did not stop the next HUB/app/ landing eleven minutes later, because no check enforced the freeze. The cure is one home, one deploy path, and an identity gate before deploy — never a folder-wide ship plus a posted warning.

## 🩷 HUMAN NOTE
Imagine mailing a whole filing cabinet when you only meant to send one folder — and inside the cabinet is an old, wrong version of your homepage. The mailroom sends everything, every time. That is what happened here: the deploy sent the whole folder, the old homepage went live, and a note on the board saying "stop" could not stop an automatic mailroom. Fix the mailroom, not just the note.

## 🟣 CHILD NOTE
If you carry a whole box to a friend, everything in the box goes with you — even the old toy you meant to leave behind. The computer carried the whole box, so the old homepage went live too. Always check what is in the box before you carry it.

## 🔵 GRANDMA NOTE
Dear, the machine sent the entire drawer, not just the one letter. An old copy of the front page was sitting in that drawer, so the old page replaced the good one. A sign that says "do not send" does not stop a machine that sends by itself. You need a lock on the drawer and one true copy of the front page, checked before anything goes out.

## 🟠 NAYA NOTE
Cold successor, hear this before you touch a deploy workflow or declare a freeze. First, read the workflow's trigger and its ship step: if the trigger is a folder path and the ship step uploads that folder, every file in it is a deploy artifact, wanted or not. Second, never treat a board post as a gate — an automatic workflow does not read the board. A freeze is real only when a check rejects the landing. Third, after any deploy, prove the live surface by served bytes against the intended build, not by HTTP 200 and not by repo bytes alone (cousins SN-2001, SN-2007). Here the proof was exact: live home 523,177 bytes, sha 4aa796e0, equal to the repo frozen copy, while the real Hub build was 5,462,049 bytes. Restore proved the same way: 5,463,030 bytes, sha 18660905, the lane build.

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-2008",
  "title": "A deploy that ships a whole folder ships its stale files too",
  "applies_when": ["deploy", "hub-app", "deploy-scope"],
  "enforcement": "Before the freeze lifts, the single-source cure must be in place (one home in HUB/app/, one deploy path, identity gate before deploy, PI item hub-single-source-cure-20261026); until then HUB/app/** landings are blocked by check, not by board post; after every deploy, VERIFY checks served home bytes and sha against the lane build, and a mismatch is a failed deploy even at HTTP 200.",
  "evidence": [
    "Live board #3066 comment 6422741419 (2026-10-26T17:22:32Z, P0): nayanet.live home serving frozen copy 523,177 B sha 4aa796e0, real Hub 5,462,049 B overwritten; mechanism: HUB/app/ carries the frozen home, deploy-hub-cloudflare.yml fires on every HUB/app/** push and ships the whole folder; face landing fe241f1b deploy SUCCESS 16:13:26Z shipped face plus frozen home, again 17:01Z.",
    "Live board #3066 comment 6422977918 (2026-10-26T17:33:27Z, VERIFY): HOME RESTORED 9.0, nayanet.live/ 5,463,030 B sha 18660905, lane build not frozen copy; repo HUB/app/index.html still frozen 523,177 B.",
    "Director tick 2026-10-26T17:38Z (live-plan.md): FREEZE VIOLATION — HUB/app/pi/index.html e21bdd43 and HUB/app/pi-face.html 3715f19e landed 17:33:39/41Z, after the freeze declared 17:22:32Z; permanent cure not landed, repo still carries the frozen copy."
  ],
  "decision_change": "When designing a deploy workflow or declaring a freeze, choose scoped artifact shipping plus a gate that blocks unscoped landings; never rely on a board announcement to stop an automatic workflow.",
  "falsifier": "A HUB/app/** push that ships only its intended files while live home stays the lane build would show folder scope was not the cause; served home bytes differing from the repo frozen copy would have disproved the mechanism — instead the sha matched exactly.",
  "mechanism": "Path trigger HUB/app/** plus a ship-the-whole-folder deploy step: the repo folder contains a stale index.html, so every face landing also deploys the stale home over the live home, and a board-posted freeze cannot interrupt a workflow that fires on push.",
  "cousins": ["SN-2001", "SN-2007", "SN-1999"],
  "truth_state": "CANDIDATE"
}
```
