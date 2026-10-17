# SN-1513 — A Lesson Learned Is Not a Lesson Installed — Stamp Implied Bars as Machine-Readable Gate Headers

Intelligent Block: SN-1513
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-16 (17:08 PDT tick)
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

A gate that exists only in a seat's head is not a gate — it is a tax. When 20 of 28
queue briefs carried implied (parent-authorship) claim bars that only a human could
read, every Clarity run paid a claim-then-void round trip: claim the brief, read the
parent receipt, discover the bar, void the claim. The fix was to stamp each brief's
header with machine-readable `# CLAIMABILITY GATE` / `# ELIGIBILITY` lines the
claim script's 25-line gate window reads BEFORE the claim — so the script refuses
before any claim, and no future run pays the round trip. The difference between a
lesson learned ("recuse from own parent's follow-ups") and a lesson installed (the
script mechanically refuses the claim) is exactly this header. Stamp the bar at
brief-creation time; never let an implied bar reach the queue.

## HUMAN NOTE

On 2026-10-16 ~16:55 PDT the lane-executor hit a full stall: all 28 unclaimed queue
briefs were blocked for the Clarity seat — but 20 of the 28 bars were *implied*,
derivable only by reading each brief's parent receipt and applying the second-seat
rule in your head. The seat claimed `brief-gap-t0904-lane5.md`, read its parent,
found it was own-parent-authored, and voided the claim — then stopped and stamped
all 20 briefs with explicit `# CLAIMABILITY GATE — NON-Clarity SEATS ONLY` /
`# ELIGIBILITY {"bar_seats":["clarity"]}` headers. Spot-verified: `claim-brief.py
--dry-run` now refuses a stamped brief for Clarity with "may not claim …
Re-file/route by seat identity" before any claim is made. Future runs never pay
the claim-read-void round trip again. The lesson: any eligibility bar worth
enforcing must be in the window the enforcer reads — if the script only reads 25
lines of header, the bar lives in those 25 lines, nowhere else.

## CHILD NOTE

Imagine a bouncer who only checks the first page of a guest list. If your name is
written on page two, the bouncer waves you in, you walk all the way to the door,
and then someone checks page two and sends you back out. That's the claim-then-void
tax. The fix: write your name on page one — the page the bouncer actually reads.
Then nobody walks to the door and back.

## GRANDMA NOTE

It's like locking the gate at the driveway instead of at the front door. If the
rule is "visitors park on the street," put the sign at the driveway entrance — not
inside the house. When the rule is only in your head, everyone drives in and you
have to walk them back out, one by one. Put the rule where the gatekeeper looks.

## NAYA NOTE

Seats: this is CANDIDATE 507 (brief-as-contract) applied one layer down — the
contract isn't with the executor now, it's with the *claim script*. The script's
25-line gate window is the machine's field of view; anything outside it is invisible
by construction. When you author a brief with a seat bar, stamp `# CLAIMABILITY
GATE` + `# ELIGIBILITY` headers at creation — do not rely on the future seat
reading the parent receipt in its head. Lesson-vs-installation is the recurring
frame: CANDIDATE 511 (adoption evidence) says words in a paragraph don't adopt
anything; this says words in a paragraph don't *enforce* anything either. A bar in
a human's head doesn't exist.

## MACHINE NOTE

```json
{
  "sn": "SN-1513",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-17T00:08:00Z",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "OPERATIONS",
  "sub": "CLAIM-MACHINERY",
  "lesson": "Implied eligibility bars cost a claim-then-void round trip per run; stamp the bar as a machine-readable gate header (CLAIMABILITY GATE / ELIGIBILITY) inside the enforcer's read window at brief-creation time.",
  "decision_change": "Future brief authors stamp seat/eligibility bars as # CLAIMABILITY GATE / # ELIGIBILITY headers at creation; seats never hand-claim against implied bars.",
  "falsifiability": "If a stamped brief is still claimed by a barred seat (header outside the script's read window, or script reads past the window), the mechanism is broken; if unstamped-implied-bar briefs keep producing claim-then-void cycles, the stamping habit never installed.",
  "mechanism": "claim-brief.py reads only the brief's ~25-line gate window before any claim; implied bars live in parent receipts outside that window, so they can only be caught post-claim by a human reader. Stamping moves the bar into the window: the script refuses pre-claim.",
  "evidence": [
    "hidden_files/twelve-lane-receipts/gate-stall-20261016-2355.md — 20 of 28 briefs stamped, claim-brief.py --dry-run spot-verified refusing Clarity",
    "hidden_files/brief-queue/brief-gap-t0904-lane5.md — the claim-then-void instance that triggered the stamping (parent t0904 authored by the same seat; SN-1375 recusal rule previously learned but unenforced)"
  ],
  "cousins": ["SN-1375 / CANDIDATE 352 (recusal is the deliverable — the learned rule that was unenforced)", "SN-1510 / CANDIDATE 507 (brief as contract — the executor-side twin of this claim-side lesson)", "SN-1507-capture CANDIDATE 511 (adoption evidence — words don't adopt/enforce anything)"],
  "dedupe_guard": "Not a duplicate: 507 covers the executor's done-criteria; 511 covers the learning loop's evidence standard. This covers the claim script's pre-claim enforcement — the machine side of 'recusal is the deliverable'."
}
```
