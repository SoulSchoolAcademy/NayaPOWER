# Know Where Your Staging Tool Lands — the Shared Script Hardcodes One Lane's Branch

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0186-shared-staging-branch-ownership
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-02
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** `naya4/smart-notes-2026-09-30` branch history, 2026-10-02: four commits by the design-intelligence lane staged via the shared `stage_smart_note.py` onto my lane's branch — SN-0183 (`3bd44f55`, 12:49:40Z, learn-then-10x, DIRECTOR-STATED), DS-0001 (`4d9be9de`, 13:01:37Z), DI-INFUSION-0001 (`f724fde6`, 13:04:05Z), TE-0001 (`08b12491`, 13:16:53Z) — all under the "Naya 4" committer identity, interleaved with my lane's SN-184/SN-185 (`ec39633c`/`fbedacb3`). Root: `hidden_files/bin/stage_smart_note.py` hardcodes `BRANCH = "naya4/smart-notes-2026-09-30"` — any lane using the shared script writes to my lane's branch. SN-0183 explains the previously unexplained bare "183" line in the counter file.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A shared tool with a hardcoded destination is a lane boundary that doesn't know it exists. The staging script every lane uses points at exactly one branch — mine — so the design-intelligence lane's notes (SN-0183 and the DS/DI/TE series) landed on my lane's draft-PR branch without any board announcement, interleaved with my own SN-184/185. Nothing was damaged — all commits are additive, all content is CANDIDATE, no numbers collided — but the registry picture broke: my counter showed a bare unexplained "183", and a collision-registry scan of "my branch" now returns another lane's claims. The durable rule: **before you stage, know where your tool lands.** If a tool's destination is hardcoded, the tool — not your lane — owns the destination choice, and every user of the tool is silently sharing one branch, one PR, and one registry surface. The fix is one of two: give the script a branch parameter (each lane stages to its own branch/PR) or make the shared branch explicit policy (all lanes stage here, announced). Until one is chosen, flag it: I posted a lane-to-lane heads-up on #554 (not a collision flag — no number was contested — but a "please announce staging runs or point the script at your own branch" note). This also refines SN-115's three-layer registry: the registry now has a fourth surface — other lanes' staging onto YOUR branch via shared tooling. Verify the tool's destination as part of the claim-time re-scan (SN-184).

## 🩷 HUMAN NOTE

Shawn — a small tooling discovery this tick: the smart-note staging script every lane uses is hardcoded to write to one branch (my smart-notes branch), so the design-intelligence lane's notes landed there mixed with mine. Nothing broken — all content is candidate, no numbers collided — but it muddied my numbering counter until I traced it. I asked the design lane on the board to announce staging runs or point the script at their own branch, and captured the lesson here.

## 🟣 CHILD NOTE

Imagine a mailbox that says "Naya 4" on it — but the mail delivery truck drops EVERYONE's mail in it, because the truck's route only knows that one address. Nobody did anything wrong, but now Naya 4 has to sort through everyone's mail. The new rule: before you mail something, check which mailbox the truck actually goes to.

## 👵 GRANDMA NOTE

You know how the building has one shared mailbox and the packages all pile up there? Same thing here — the tool everyone uses only knows one address. We wrote down the rule: check where your tool actually puts things, and if you're sharing a mailbox, say so out loud.

## 🤖 NAYA NOTE

Never trust a destination by convention when a tool chooses it by default. When adopting any shared staging/commit/publish tool, read its hardcoded paths, branches, and PR targets first; treat them as your lane's dependencies. If you stage onto another lane's branch, announce it on the board — the owning lane's registry, counter, and scans now include your claims, and an unexplained counter bump costs the next runner a full trace (as it cost this tick). Prefer a `--branch` parameter over a hardcoded branch for multi-lane tools.

## ⚙️ MACHINE NOTE

{"sn": "SN-0186", "title": "Know Where Your Staging Tool Lands — the Shared Script Hardcodes One Lane's Branch", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-02", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "OPERATING-MODE", "DIRECT-LANE-COLLABORATION"], "extends": ["SN-108", "SN-115", "SN-184"], "evidence": {"script": "hidden_files/bin/stage_smart_note.py", "hardcoded_branch": "naya4/smart-notes-2026-09-30", "cross_lane_commits": [{"sha": "3bd44f55", "at": "2026-10-02T12:49:40Z", "item": "SN-0183"}, {"sha": "4d9be9de", "at": "2026-10-02T13:01:37Z", "item": "DS-0001"}, {"sha": "f724fde6", "at": "2026-10-02T13:04:05Z", "item": "DI-INFUSION-0001"}, {"sha": "08b12491", "at": "2026-10-02T13:16:53Z", "item": "TE-0001"}], "my_commits_interleaved": ["ec39633c", "fbedacb3"], "no_collision": true, "counter_explained": "bare 183 line = SN-0183 staged by design-intel lane"}, "rule": "verify a staging tool's hardcoded destination before use; announce staging onto another lane's branch, or parametrize the branch", "refinement_of_registry": "SN-115 three-layer registry gains a fourth surface: cross-lane staging onto your branch via shared tooling"}