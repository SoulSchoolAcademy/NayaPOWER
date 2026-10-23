Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

Delta's lane-5 adjudication (board #2793 comment 6364079133, 2026-10-23) ruled the 7-merge storm (add-w783) NON-COMPLIANT with merge law — legs 1/3/5 failed — and named the failure mode SINGLE_PARENT_SQUASH_SHARED_LOGIN: squash commits made under a shared login collapse seat attribution, and the Independence Lock's different-seat check reads committer identity, so attribution is destroyed at the data level before any policy can argue about it. The durable rule: **a multi-leg landing that squashes under a shared login can never pass the different-seat check — each leg must land as a 2-parent merge with an attributable committer.** The Independence Lock does not grade intentions; it reads the commit graph, and a single-parent squash has exactly one parent and one committer to read.

## 🩷 HUMAN NOTE

Shawn — the team just proved why the Independence Lock keeps failing on storm landings. When seven merge legs get squashed under a shared bot login, the commit record shows one committer and one parent — there's no trace of which seat did what. The Lock's different-seat check needs to see distinct seats in the commit graph, and there's nothing left to see. This isn't a policy debate; the data is gone. Going forward: storm legs land as real 2-parent merges with attributable committers, or they fail the Lock by construction. Today's 7-merge storm (legs 1, 3, 5 failed; leg 4 not ruled) is the textbook case — the landings stand but marked non-compliant, with post-hoc cure owed per landed head.

## 🟣 CHILD NOTE

Imagine seven kids each build a piece of a Lego castle, and a teacher glues all the pieces together into one lump and stamps it "TEACHER'S WORK." Now nobody can tell who built which piece — the sticker with everyone's name is gone. The rule that says "at least two kids must have helped" can't be checked anymore, because there's only one name on the lump. To keep the rule working, each kid's piece has to arrive with their own name tag on it — no gluing everything into one lump first.

## 🔵 GRANDMA NOTE

It's like a relay race where seven runners hand the baton to each other — but the timekeeper only writes down the team's name, never the individual runners. When someone asks "did a different runner run each leg?" there's no way to answer: the record has one name for the whole race. The fix is to write down every runner at every handoff. Collapse the seven legs into one entry and the answer to "who did what" is lost forever.

## 🟠 NAYA NOTE

This is the seat-attribution doctrine meeting its sharpest edge. SN-0447 gave us merge-faithfulness for squash merges and SN-1829 made the bot consult the hold registry — but neither saves a storm landing, because the Independence Lock's different-seat check consumes the commit graph as its input, and a single-parent squash under a shared login is a graph with attribution pre-erased. One parent, one committer: the check degrades to "same seat as far as the bytes can tell," and every leg routed through that shape fails before the policy layer is even consulted. Delta's adjudication gets the framing exactly right — legs 1/3/5 fail, leg 2 held its own scorecards, leg 4 explicitly NOT RULED (the adjudicator named what it didn't prove). The seat-level consequence: multi-leg storm work must be designed for attribution-first landings — per-leg 2-parent merges with attributable committers — or it enters the Lock as one indistinguishable blob and fails by construction. Cousin: SN-1829 (bot merges and the hold registry — authority envelope around merges); this is the graph-shape cousin — the envelope survives, the graph doesn't.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1871-shared-login-squash-defeats-attribution",
  "lesson": "A multi-leg landing that squashes under a shared login can never pass the Independence Lock's different-seat check: the squash commit has exactly one parent and one committer, and under a shared-login committer the graph carries zero record of which seat authored each leg. Delta lane-5 adjudication (board #2793 comment 6364079133, 2026-10-23) ruled the 7-merge storm (add-w783) NON-COMPLIANT with merge law — legs 1/3/5 failed, leg 2 held #2893/#2892/#2891 + failed #2890, leg 4 NOT RULED — and named the failure mode SINGLE_PARENT_SQUASH_SHARED_LOGIN. Storm legs must land as 2-parent merges with attributable committers; a shared-login squash fails the Lock by construction.",
  "applies_when": ["merge", "adjudication", "storm-landing", "independence-lock", "seat-attribution"],
  "enforcement": "Merge-law adjudication check: every storm/multi-leg landing must land as 2-parent merge commits with attributable committers BEFORE the Independence Lock's different-seat check can pass. A single-parent squash under a shared login can never satisfy the different-seat check — the adjudication ledger (five-rule merge law) records the condition per leg; legs landing as shared-login squashes fail leg 1 (attributable head) by graph shape. Verify reference: Delta adjudication 6364079133, add-w783 storm, legs 1/3/5 fail; dispositions: landings stand marked non-compliant, post-hoc cure per landed head owed by dock.",
  "evidence": [
    "board #2793 comment 6364079133 (Team Verity Naya Delta, lane 5, 2026-10-23T12:08Z tick — 'Delta lane 5 adjudication: 7-merge storm (add-w783) ruled NON-COMPLIANT with merge law - legs 1/3/5 fail, leg 2 held #2893/#2892/#2891 + failed #2890, leg 4 NOT RULED; disposition: landings stand marked non-compliant, post-hoc cure per landed head owed by dock')",
    "shared-state.json named_failure_modes_new (2026-10-23): 'SINGLE_PARENT_SQUASH_SHARED_LOGIN (7-merge-storm add-w783, Delta adjudication 6364079133: squash commits under shared-login committer defeat seat attribution and the Independence Lock's different-seat check; verify check: merge commits must be 2-parent with attributable committer)'",
    "cousin SN-0447 (merge-faithfulness for squash merges); cousin SN-1829 (bot merge must consult the hold registry) — this is the graph-shape cousin"
  ]
}
```
