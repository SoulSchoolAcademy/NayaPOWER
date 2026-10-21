# A Verdict Posts Where the Scanner Reads — Gate-Format IV on the PR Itself

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01758-verdict-posts-where-the-scanner-reads
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-21
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

On 2026-10-21, PR #2831's IV cure was VERIFIED 9.5 (board 6310156804) — but the verdict lived only on the board, and the dock's gate scanner reads the PR's own comment thread, not the board. L591 was filed: IV content ≠ IV visibility — a verdict posts where the scanner reads. Six minutes later the repair landed in bytes: `[NAYA RESOLVE . REVIEW] APPROVED - PR #2831 @ f1ed1803` posted ON THE PR ITSELF (6311355696, 08:16:30Z). #2841 then satisfied L591 the same day. The rule: a board receipt is the record; the on-PR gate-format post is the key. One without the other holds no merge.

## 🩷 HUMAN NOTE

Shawn — tonight we learned the difference between a verdict and a *visible* verdict. PR #2831 passed verification 9.5, but the proof was sitting on the board where the merge gate never looks. The dock's scanner reads the PR's own thread — the board is a different room. The fix was a one-line post on the PR itself in the gate's exact format, and the merge path unlocked. Lesson filed as law now: the verifier's job isn't done at the board post. It ends when the verdict is standing where the scanner reads.

## 🟣 CHILD NOTE

Imagine your teacher only checks the homework tray by her desk — but you handed your homework to the teacher's aide in the hallway. You did the work, but it landed in the wrong tray, so the teacher thinks it's missing. The rule is simple: put the homework in the tray the teacher actually checks. Same here: a review verdict has to be posted on the PR itself, because that's the tray the merge gate checks — not the board.

## 🔵 GRANDMA NOTE

Like a court clerk who files papers in the wrong courthouse. You can win the case, but if the signed judgment sits in the wrong building, the sheriff can't act on it — he only reads the file at his own desk. Today's fix was a one-minute job: post the same verdict, worded exactly the gate's way, in the place the gate actually reads. The lesson: the announcement isn't the act; the verdict only works where the reader looks.

## 🟠 NAYA NOTE

Lane discipline: an IV verdict is not complete at the board receipt. The dock's merge gate is an automated reader with a fixed read set — the PR's own comment thread plus repo state; board comments are outside it. A verdict that exists where the gate's reader cannot look is, to the gate, nonexistent. The L591 shape: (1) board receipt with full evidence (6310156804 for #2831), (2) gate-format post on the PR itself — `[NAYA <SEAT> . REVIEW] <APPROVED|…> - PR #NNNN @ <sha>` (6311355696 for #2831, ~6 min after the L591 filing), (3) the on-PR post is what the dock's gate scanner matches. #2841's sign-out (6313317039) carried the L591 check explicitly. When you finish a scorecard, the last step is the on-PR post — a scorecard receipt without it is an incomplete verdict and the merge cannot move.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1758",
  "title": "A verdict posts where the scanner reads — gate-format IV on the PR itself",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "applies_when": [
    ["verify", "iv-verdict"],
    ["dock", "gate"],
    ["merge", "receipt"],
    ["review", "posting"]
  ],
  "enforcement": "The dock's merge gate scans the PR's own comment thread for the gate-format token `[NAYA <SEAT> . REVIEW] <verdict> - PR #NNNN @ <sha>`; a verdict posted only on the board is not read by the scanner and holds no merge. Every IV sign-off is incomplete until the gate-format post lands ON the PR itself — the board receipt alone does not open the gate. The named check is the 'on-PR verdict post': before routing a PR to the merge queue, verify the gate-format comment exists on the PR thread.",
  "evidence": {
    "l591_filing": "#2793 intelligent-events comment 6313424794 (2026-10-21): L591 PROMOTED/ADOPTED — IV content != IV visibility, verdict posts where the scanner reads",
    "gate_format_post": "PR #2831 comment 6311355696 @08:16:30Z (2026-10-21): `[NAYA RESOLVE . REVIEW] APPROVED - PR #2831 @ f1ed1803` posted ON THE PR ITSELF, ~6 min after the L591 filing — lesson to named repair to byte-verified application inside one window",
    "board_receipt": "#2793 comment 6310156804 (2026-10-21): #2831 VERIFY receipt (head f1ed1803 = 31/31 PASS) posted on the board — sufficient as record, insufficient for the gate",
    "repeat": "#2793 comment 6313317039 (2026-10-21): #2841 VERIFY sign-out with gate-format IV verdict posted on the PR itself, L591 explicitly satisfied"
  },
  "decision_change": "A verifier finishing a 9.5+ exact-head scorecard no longer stops at posting the evidence receipt on the board; the final mandatory step is the gate-format verdict posted ON the PR itself. Merge-queue routing waits on the on-PR post, not on the board receipt.",
  "falsifier": "If the dock's gate scanner is ever taught to read board comments, or a board-only verdict is proven to have carried a merge, the placement rule relaxes. Until then the on-PR post is load-bearing.",
  "mechanism": "The dock's gate is an automated reader with a fixed read set (the PR's own comment thread + repo state). Board comments live outside that read set. Information theory of the pipeline: a verdict that exists outside the reader's read set is indistinguishable from no verdict — so the verdict must be written where the reader reads.",
  "related": ["SN-1756 (its evidence cites the #2831 gate-format verdict on the PR)", "SN-1563 (spoken word outranks papers — inverse: here placement outranks content)"]
}
```
