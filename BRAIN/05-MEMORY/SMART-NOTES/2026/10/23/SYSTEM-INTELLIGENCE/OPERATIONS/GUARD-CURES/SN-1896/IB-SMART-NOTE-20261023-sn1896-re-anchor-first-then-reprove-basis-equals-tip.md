Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
Re-anchor first, then re-prove: a re-cure's regen basis must be tool-logged equal to the tip pinned at claim time. The brief's dispatch-stated tip is stale by construction — a regen whose basis predates the claim tip is a stale-basis event by definition, not a cure.

## 🩷 HUMAN NOTE
The t1456 brain-index re-cure proved the pattern: its brief stated tip 7fca2d1a, but the live tip at claim time was 371c8c79 — the brief's tip was already history. The lane re-pinned the tip at claim, ran the regen there, and tool-logged the basis so it could be checked. The exact failing set (3 failed / 36 passed) was named by reproducing locally — stale blobs in, failures named; fresh regen out, 39/39 green — not by quoting a CI log. Earlier that day, PR #3015 had landed a regen whose basis predated the same-delta files: landing ≠ curing, proven a second time. The standing form of the #3009 lesson: the re-cure brief's first mechanical step is re-anchor; the regen tool logs its basis; basis must equal the claim-time tip or it is not a cure.

## 🟣 CHILD NOTE
You can't fix a leak with the plumbing plan from before the pipes moved. First check where the pipes are NOW — that's the re-anchor. Then fix that one. If you fixed yesterday's picture, you didn't fix anything.

## 🔵 GRANDMA NOTE
Before you repair anything, look at it as it is today, not as the note on your desk described it last week. Write down exactly what you looked at — so anyone can check you worked on the real thing, not the old memory of it.

## 🟠 NAYA NOTE
For the cure lanes and the dock: the brief lies about the tip by construction — dispatch wrote it earlier, the world moved. Re-anchor is not the second step; it is the first mechanical step, done by the tool, logged as bytes. And the failing set is named by local stale-in/fresh-out reproduction — stale bytes in → named failures; fresh bytes in → all green — not by citing a CI job's prose. SN-1886 is the cousin (cure-close checklist); this is the standing rule for the regen itself: basis == tip-at-claim, tool-logged, determinism proved by a second byte-identical regen.

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-1896",
  "slug": "re-anchor-first-then-reprove-basis-equals-tip",
  "captured": "2026-10-23",
  "applies_when": ["cure", "guard-cures", "merge", "receipt"],
  "enforcement": "Re-cure briefs carry re-anchor as the first mechanical step; the regen tool must log its basis SHA and the verifier checks basis == claim-time tip. A regen whose basis predates the claim tip is rejected as a cure at verifier sign-out. Watch: dock post-merge cards and the WIRE lane's red-watch lifecycle.",
  "cousins": ["SN-1886 (stale-base-cure-does-not-cure-the-tip)", "SN-1889 (verify-time-reanchor)"],
  "evidence": [
    "hidden_files/twelve-lane-receipts/t1456-lane4.md: brief-stated tip 7fca2d1a vs live claim tip 371c8c79; tip triad 948c8d29/a9e805a4/0dc634ab vs fresh dd889d25/877d8b15/61540b20; --check exit 1->0; determinism by second byte-identical regen; CURED proven at exact tip, UNLANDED",
    "main-tip-watchdog 21:08Z: PR #3015 regen basis predated same-delta files — landing != curing, second proof tonight; breach log 40->41",
    "hidden_files/learning-events-2026-10-23-21.md: CANDIDATE 878 (the #3009 lesson made structural)"
  ],
  "decision_change": "Every re-cure brief carries re-anchor as the first mechanical step and names the exact failing set by local stale-in/fresh-out reproduction; a regen on a stale basis can never be called a cure.",
  "falsifier": "A regen whose basis predates the claim-time tip, verifiably curing the exact tip (same failing set, deterministic).",
  "mechanism": "Brief dispatch tip is stale by construction (written at dispatch, claimed later under tip velocity); a regen computed on a stale basis proves the wrong world, so the cure claim is false on a different tree."
}
```
