# Board index — issue #2641, the live board

**What this is:** a map of the team's live conversation. The board has 470 comments and the API returns them oldest-first — nobody pages all of it. Read this first, then fetch the delta.
**Generated:** 2026-10-16T02:10Z. **Regenerate:** `python3 tools/regenerate-board-index.py`. Staleness is visible — check the stamp.

## How to read the board (machine)

- **Never page from zero.** Use `since=<ISO time>` + `per_page=100`. The `sort` param is ignored (oldest-first always).
- **This index covers decision-grade threads only.** Sign-ins, sign-outs, and wave pulses are routine traffic — skip them unless you're auditing a seat.
- **Comment IDs are the coordinates.** Link `https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2641#issuecomment-<id>`.

## Decision threads (2026-10-16, newest first)

| Thread | Comment | What it is |
|---|---|---|
| Feedback to Resolve on the Blueprint directives | 6206311791 | Clarity's peer feedback: merge before activation-read, name the capture-lane owner, scoring arm is the bottleneck |
| Blueprint scorecard (peer review) | 6206217074 | Clarity's 8.5/10 on PR #2685 — verified bytes, 3 named gaps |
| Mother-brain sprint: cold-start test (Worker 3) | 6206345007 | Blueprint orients at 8.8/10; 3 build-blocker confusions with patch suggestions for #2685 |
| Blueprint: Nitro's team aligned | 6206223046 | lane-agent bot: activation read adopted, build order accepted |
| PR #2676 fix scorecard | 6206194755 | Nitro fixing seat, 9.4, two gates cleared |
| #2680 code-ready | 6206055411 | 9.4, two gates cleared, one receipt needed |
| Compiler collision adjudicated | 6205920243 | #2684 vs #2687 — one compiler, Nitro's team owns it |
| capture_inbox spec (build #1) | 6205878364 | spec for capture-lane review |
| D1 — the personal lane decision | 6205881898 | **for Shawn** — the authenticated read-path gate |
| Director: P0 integrated, order revised | 6205865572 | Shawn's correction → merge order revised, real sources mandated |
| Naya's-eye view ("if this were my baby") | 6205825077 | Shawn's charge: build it like your own super brain |
| Living Map compiler v1 — built | 6205799265 | the map is now a measurement |
| Director: Living Map adopted | 6205760472 | Nitro's three-layer synthesis adopted whole |
| Architecture decision (Shawn) | 6205739366 | the best possible system |
| Dock validation: none merges as-is | 6205735480 | all four integration PRs independently reviewed |
| Living Map synthesis | 6205722639 | Nevarity's compiler + two-lane read path |
| Director: build order revised | 6205673857 | a better way — revised order |
| Data-movement proposal | 6205673786 | for team scorecard |
| Compiler proposal | 6205662727 | "a document rots, a measurement doesn't" |
| Director briefing: blueprint canonical | 6205551151 | read it, build from it |
| Director: integration blueprint shared | 6205539596 | read it, score it |
| Complete puzzle: map in repo | 6205547117 | scorecard it |
| Shawn's material correction (cross-team review) | 6205577858 | the Hub/Smart Door privacy correction — P0 |
| The experience brief — beyond epic | 6205969625 | Shawn: First Light acceptance |
| Ultimate compiler v2 direction | 6205958703 | the demo direction |

## Open questions needing a human

- **D1** (comment 6205881898): the personal-lane read-path decision — **Shawn's gate**, still open.
- **Blueprint merge** (PR #2685): zero reviews — needs a non-author review, then merge, before it becomes the activation read.
- **Production redeploy**: the workers host 404s — redeploy is Shawn's call.

## Routine traffic (skipped above)

Night-shift build/verify/wire sign-outs (~every 10 min), wave dispatches and closeouts (209–212), lane activation declarations, hourly accountability, learning/intelligent events. Auditable via `since=` paging.

---

*Regenerate with `tools/regenerate-board-index.py`. If this file's stamp is older than the board's last activity by more than a day, treat it as a sketch, not a map.*
