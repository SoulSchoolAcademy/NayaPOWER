# The Regen Instrument Sees Only BRAIN/ — Files Outside Its Scope Fail at the Base, Not the Regen

**Intelligent Block:** IB-SMART-NOTE-20261010-sn0885-regen-sees-only-brain-scope-limit
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** Smart Note distillation loop
**Provenance:** #1354 6098157361 ([NAYA 5] CI heal done for #1707 and #1708 — correcting the record, 2026-10-10T13:48:29Z); #1354 6098299910 ([NAYA 5] CI heal complete — #1707 and #1708 green, 2026-10-10T14:04:28Z)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 5 misdiagnosed CI failures on #1707/#1708 as "missing brain-index regen," then corrected the record: **the regen script scans only BRAIN/, and both PRs' files live outside it** — so no regen of the brain index could ever have fixed the failure. The real cause was a stale base: both branches sat on an old main, and CI tests the merge commit, where main's newer BRAIN/ met the branches' older committed index. The heal was rebase-onto-current-main + regen (branch trees rebuilt on main `f4d7a7e4`, 3 index files regenerated, `--check` green on 1235 files), followed by green CI on all checks on the corrected heads (`3a86ac3c`, `d64a6c3c`).

The lesson for the regen-instrument family (SN-0327, SN-0395, SN-0872): the instrument has a **scope boundary** — it enumerates BRAIN/ only. A CI index-drift failure whose offending files live outside BRAIN/ is by definition not a missing-regen condition; it is a base condition. Before prescribing "regen the index," check WHERE the failing files live. If they are outside BRAIN/, re-resolve the base and rebase — the regen step is cargo cult. The correction-of-the-record move is the discipline: Naya 5's public retraction ("correcting the record") is what let the true cause surface, and the evidence law rewards it.

For a cold Naya: when CI fails on index/ledger drift, first list the failing paths; if none of them are under BRAIN/, do not touch the regen script — compare the branch base against live main (SN-0493) and suspect the merge-commit collision instead.

## 🩷 HUMAN NOTE

Shawn — a small but sharp lesson from Naya 5's CI heal: she first said the failures were a missing index regen, then corrected herself — the regen tool only looks at BRAIN/ files, and the failing PRs' files live outside BRAIN/, so regen was never the fix. The real problem was both branches were built on an old version of main; the fix was rebasing onto current main. The lesson: before running a fix, check whether the tool even covers the files that are broken — otherwise you're doing a ritual, not a repair. And she said so publicly: "correcting the record." That's the standard.

## 👶 CHILD NOTE

Imagine you lose your shoe in the backyard, and someone says "let's clean the bedroom to find it." Cleaning the bedroom is a good tool — but it can never find a shoe that isn't there. Naya 5 first said "clean the bedroom" (regen the index), then remembered the shoe was in the backyard all along (the files live outside BRAIN/). The lesson: before you use a tool, ask "does this tool even look where my problem is?"

## 👵 GRANDMA NOTE

It's like the lost-keys story, but backwards. Everyone knows to look where the light is — the trick is knowing when the light doesn't cover the whole room. The index-rebuilding tool only looks in one folder (BRAIN/). The broken files were in other folders, so rebuilding the index could never fix them. The real problem was the branches were built on yesterday's foundation, and the fix was moving them onto today's. Always check that your repair tool actually reaches the problem before you run it.

## 🟠 NAYA NOTE

New rule joining the regen-instrument family (SN-0327/0395/0872): the regen enumerates BRAIN/ ONLY. Diagnostic protocol for CI index/ledger drift: (1) list the failing paths from the CI log; (2) if any failing path is outside BRAIN/, STOP — regen cannot heal it; re-resolve live main via the refs API (SN-0493) and check whether the branch base is stale; (3) only when the failing paths are all inside BRAIN/ does the regen/regenerate landing step apply. Also: when your first diagnosis turns out wrong, say so on the record (like Naya 5 did) — the correction is itself evidence-grade signal for the next seat.

## MACHINE NOTE

```json
{
  "intelligent_block_id": "IB-SMART-NOTE-20261010-sn0885-regen-sees-only-brain-scope-limit",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "sn_number": "SN-0885",
  "family": "regen-instrument-discipline (SN-0327, SN-0395, SN-0872)",
  "lesson": "brain-index regen enumerates BRAIN/ only; drift on files outside BRAIN/ is a stale-base merge-commit condition, not a missing-regen condition — rebase, do not regen",
  "evidence": {
    "board": "#1354",
    "comments": ["6098157361", "6098299910"],
    "misdiagnosis": "missing brain-index regen",
    "true_cause": "stale base; CI tests the merge commit where main's newer BRAIN/ met the branches' older committed index",
    "heal": "rebase onto main f4d7a7e4 + regen; corrected heads 3a86ac3c (#1707), d64a6c3c (#1708); all CI checks green",
    "related_prs": ["#1707", "#1708"]
  },
  "protocol": "on CI index-drift: list failing paths first; outside-BRAIN/ => check base staleness (SN-0493 re-anchor), not regen"
}
```
