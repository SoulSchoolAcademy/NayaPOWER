# Smart Note — Complete-App Doctrine: Independent Verification + SN-019 Collision

kind: smart-note
truth-state: CANDIDATE
scope: PRIVATE
captured: 2026-10-01 20:42 PDT
captured-by: Naya 4 (builder seat)
source: Naya 3's complete-app report shared by Shawn Vibert in chat; verified live
  against GitHub by Naya 4 (read-only)
provenance: Naya 3's report → Shawn shared → Naya 4 independently verified → intelligent block
sn-number: SN-0150
ib-number: IB-014

---

## IN A NUTSHELL

Naya 3 reported the complete-app doctrine: the "smallest effective slice" rule had
become an accidental stopping rule, and the correction — THE SMALLEST EFFECTIVE SLICE
CONTROLS BUILD ORDER, IT DOES NOT REDUCE THE PRODUCT — is now SN-019 on main, with
PR #1306 as the convergence lane carrying a machine-readable completion matrix, a
false-completion gate, 11 room modules, and Playwright browser QA. I verified every
checkable claim live: PR #1306 open and mergeable at 44b97535; the matrix lists all
11 rooms as IMPLEMENTED with honest remaining gaps and runtime NOT_VERIFIED (connect/
settings PARTIAL); the validator and workflow exist; the legal progression matches;
overall_state is IN_PROGRESS (honest, not complete). One defect found: **SN-019 is
double-claimed** — the Sept-30 seed "direct lane protocol" lives on
naya4/smart-notes-2026-09-30 while "Complete the App Doctrine" lives on main a67fc180.
First-claim-stands says the draft-PR claim is senior; the main claim is canonical.
Flagged for the Smart Note lane + Naya 3 — renumbering main is beyond my lane.

---

## HUMAN NOTE

Shawn — I checked Naya 3's homework against live GitHub, and it holds up:

- PR #1306 is real, open, mergeable. The completion matrix lists all 11 rooms with
  their metaphors, each marked IMPLEMENTED — and crucially, each with an honest
  "remaining" list and runtime NOT_VERIFIED. Nobody's pretending.
- The false-completion gate exists (validator + workflow). The legal progression
  matches what she described. The matrix says IN_PROGRESS, not COMPLETE.
- Her inequality chain (shell ≠ product … verified ≠ production-proven …) is now
  the law the machine enforces.

One thing I caught that she didn't: **SN-019 is claimed twice.** The old Sept-30
"direct lane protocol" seed still lives on the draft smart-notes branch, and her new
"Complete the App Doctrine" is on main. I've flagged it on #554 for the Smart Note
lane and Naya 3 to resolve — I'm not renumbering main unilaterally.

The doctrine itself is the most important process correction of the night: the
smallest slice orders the work; it never shrinks the promise. "Never hand the Human
Director a porch and call it a house" — that's now machine-enforced, not just
memorable.

---

## CHILD NOTE

Naya 3 found the big mistake: the team was building small pieces and forgetting the
rest of the house! The fix: small pieces tell you what to build FIRST — they don't
make the house smaller.

I checked her work and it's all real: the list of all 11 rooms, the machine that
checks if they're really done, the tests. Everything honest.

But I found one mix-up: two different notes are both called "SN-019"! I told the
team so they can fix it.

And the new rule is: never give Shawn a porch and call it a house! 🏠

---

## GRANDMA NOTE

Honey, Naya 3 figured out the sneaky mistake: everyone was building the first piece
and forgetting there was a whole house to finish! The new rule is simple: building a
little at a time tells you *where to start* — it doesn't make the job smaller.

I double-checked her work myself, and it's solid — the full room list, the
honesty-checker machine, all real.

I did find one little mix-up (two notes with the same number), and I've asked the
team to sort it out. And the new motto made me smile: never hand Shawn a porch and
call it a house. That's a keeper, sweetheart.

---

## NAYA NOTE

My assessment:

**The doctrine is correct and the mechanism is real.** "Smallest effective slice
controls build order, not product scope" resolves the exact failure mode behind
months of shells-without-houses. The matrix + gate + legal progression is the first
machine-visible declared product we've had — scope can no longer silently evaporate
from operational memory. The honest NOT_VERIFIED runtime states are the strongest
signal: the lane is reporting gaps instead of hiding them.

**Verification results (all read-only, live):**
- PR #1306: open, mergeable=True, head 44b97535, base main. ✓
- Matrix: 11/11 rooms, metaphors match her table, states IMPLEMENTED, remaining
  gaps listed per room, browser_render TESTED with run/artifact evidence. ✓
- tools/verify_hub_app_completion.py (4.7KB) + hub-app-completion-gate.yml
  (2.2KB) exist on the branch. ✓
- legal_states match her 8-step progression; overall_state IN_PROGRESS. ✓
- Not independently re-run: the Playwright suite results and the 108-jewel count
  are her reported evidence (workflow PASS cited); I verified the artifacts exist
  as claims, not the run itself.

**The SN-019 collision:** Sept-30 seed (direct lane protocol, draft PR #1229,
never merged) vs Oct-2 main (Complete the App Doctrine, a67fc180). First-claim
says the seed is senior; canonical-weight says main wins in practice. This is a
governance call for the Smart Note lane + Naya 3 + Shawn — not a unilateral
renumber by the builder seat. Flagged on #554.

**Fit with the night plan:** PR #1306 is now the convergence lane to watch. The
night plan's "no production building until freeze" still holds for room visuals;
#1306's runtime frontier (governed runtime contract → canonical object → rooms)
is the next failing gate after the blueprint freeze. The two tracks are
sequenced, not competing.

---

## MACHINE NOTE

```json
{
  "block": "IB-014",
  "sn": "SN-0150",
  "kind": "smart-note",
  "truth_state": "CANDIDATE",
  "captured": "2026-10-01T20:42:00-07:00",
  "source": {"author": "Naya 3", "venue": "report shared by Shawn", "verified_by": "Naya 4 read-only live"},
  "doctrine": "smallest effective slice controls BUILD ORDER, never reduces PRODUCT SCOPE",
  "verified": {"pr_1306": "open, mergeable, 44b97535", "matrix": "11/11 rooms IMPLEMENTED, honest gaps, runtime NOT_VERIFIED (connect/settings PARTIAL)",
    "validator": "exists (4.7KB)", "workflow": "exists (2.2KB)", "legal_states": "8-step match", "overall": "IN_PROGRESS"},
  "not_reverified": ["Playwright run results (cited evidence only)", "108-jewel count (cited)"],
  "defect": {"sn_019_collision": "draft-PR seed 'direct lane protocol' (2026/09/30) vs main 'Complete the App Doctrine' (a67fc180); flagged for Smart Note lane + Naya 3"},
  "engraved_rule": "Never hand the Human Director a porch and call it a house."
}
```

---

## LEARNING LESSON

**Verify the report, not just the claims.** Naya 3's write-up was thorough and
honest — and still contained a collision she didn't catch (SN-019). The lesson:
even excellent lane reports need the independent eye; that's what the seat is for.
Verification is not distrust — it's the mechanism that lets trust compound.

**Collisions are a namespace governance problem.** Four SN collisions tonight
(018 date-partition, 019 cross-branch, 143, 144). The counter file is not enough;
the namespace needs a single registry checked before any claim lands. Propose: the
Smart Note lane owns the registry; no number is claimed without a registry entry.

---

## WHAT IT ULTIMATELY MEANS

The complete-app doctrine is verified and real — the first machine-enforced end to
the porch-not-house era. The SN namespace needs governance before the next
collision. PR #1306 is the lane to watch; the blueprint freeze is the gate before
it.

---

## HOW TO USE IT

1. Resolve the SN-019 collision (Smart Note lane + Naya 3 + Shawn).
2. Stand up the SN registry — no claim without an entry.
3. Track PR #1306's runtime frontier as the post-freeze next gate.
4. Keep the night plan's sequencing: freeze visuals first, then runtime.

---

## WHAT'S IN IT FOR YOU

Shawn — Naya 3's doctrine checks out against live GitHub, and I caught the one
thing she missed (the SN-019 double-claim) so it gets fixed cleanly. The porch
era is over — the machine won't let anyone call it a house until all eleven
rooms are proven. That's your frustration, turned into law, turned into code.
