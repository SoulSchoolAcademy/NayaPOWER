# Merge Operations Manual — human tongue (v1.0.0)

**What this is.** The runbook for stuck merges. If a merge isn't moving, any Naya opens this, matches what she sees to the symptom list, and applies the fix. No merge stalls for hours — ever.

**The 60-second version.** Merges get stuck for seven known reasons, in order of how often they happen:
1. **Nobody pressed merge.** The PR is fully qualified and just sitting there. Any Naya except the author can claim it and merge it — that's the fix.
2. **The "blocked" label is stale.** The checks are actually green; the status display just hasn't caught up. Re-read the live checks.
3. **A one-line paperwork fix.** The PR body is missing its `Seat:` declaration. One line, and the gate goes green.
4. **A missing evidence section.** The PR body needs its proof section with real links.
5. **A noisy check.** The same check fails over and over while nothing changed — that's a broken sensor, not a broken PR. Don't treat it as a red light.
6. **The ground moved.** The main branch advanced after the PR was approved. Re-check against the new state.
7. **A missing receipt.** The work was reviewed and approved but the formal receipt was never posted. Post it.

**How it stays current.** Every new merge problem anyone solves gets distilled into this manual — symptom, causes, fix — newest first. It's a living feed, not a static document. Owner: the dock (the merge lane).
