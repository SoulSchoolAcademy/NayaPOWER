# AAA Launch QA — AI builder spec

**Status:** PROPOSED / CANDIDATE. Not ratified. Candidate acceptance methodology; do not gate any build on it without director word.
**Source:** HMC Button Spec second half (AAA checklist A–S), HMC batch-1 distillation 2026-10-06. Product references dated; methodology timeless.

## The 19 sections (exact, ordered)

| ID | Section | Pass condition (behavioral) |
|---|---|---|
| A | first-impression | a first-time visitor knows what to press without explanation |
| B | button-system | every control follows the button standard; all states work |
| C | desktop-layout | 1024–1920px: no overlap, no breakage |
| D | mobile-layout | 320–430px: identity preserved, never collapsed into generic cards |
| E | audio-engine | sound plays correctly; controls respond |
| F | search | finds what it should; handles misses honestly |
| G | playlists-queue-favourites | collection mechanics work end to end |
| H | install | install path works on real devices |
| I | request-a-topic | request path works and is answered |
| J | share | sharing works; links land where promised |
| K | content-artwork | every slide/content/art: correct, present, no broken links |
| L | welcome-journey | entrance works first-try for a stranger |
| M | demo-full-editions | both editions behave as promised |
| N | purchase-journey | money flows work; receipts exist |
| O | qa-inventory | every visible feature tested, every viewport covered |
| P | analytics | the measurement is actually measuring |
| Q | social-nav-hub | navigation and social surfaces work |
| R | accessibility-trust | keyboard, focus, reduced-motion; NOT_VERIFIED over fake content |
| S | performance | fast; transform/opacity animation; no layout thrash |

## Methodology rules

1. Pass conditions are **behavioral, not cosmetic.** Each section has a checkable behavior; "looks good" is never a pass.
2. The closing standard (director's words, proposed as the build loop's definition of done): *"We define the full system, implement from one source of truth, test every visible feature, record every failure, and do not call it complete until the checklist passes."*
3. Record every failure. A checklist run with unrecorded failures is not a run.
4. Applies to the Hub's 10/10 pass (sections C, D, L, M, O already flagged), the identity rebuild (M, Q), the Reveal 37-slide verification (K, O), and future launches.

## Relationship to existing acceptance

Extends `HUB/DESIGN-CONTRACT.md` §29 (Acceptance) and the eight-dimension scorecard in `HUB/PROJECT-INTELLIGENCE.*`. The scorecard is the standing gate; this methodology is the *launch* checklist underneath it. No contradiction; no replacement.

## Constraints

- Do not present a build as "complete" against this checklist until ratified — the methodology is proposed, not law.
- Enforcement follow-up (out of scope this run): a machine checklist runner that tracks per-section pass/fail with evidence links. Named here as a concrete follow-up, never faked.
