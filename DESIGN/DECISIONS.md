# NAYA DESIGN DECISIONS — rulings, retirements, open gaps

Where the source generations disagreed, a ruling was made. Newest wins,
unless the older is clearly better. Nothing is buried here.

## Generation rulings

**Canonical: Naya_2 "Ultimate Design System" (100 laws) + N5 Lego library.**
These are the newest generation. Everything below is superseded.

| Conflict | Ruling | Why |
|---|---|---|
| Token dialect: N4 jewel (`--obsidian:#020203`, `--white:#ffffff`, `--chrome:#8a5cff`, Cormorant voice) vs N5 obsidian stack | **N5 wins** | Newest; byte-identical across both N5 files — the converged system. |
| Spectrum: PDF/N4 12-step purple-led vs N5 5-step magenta-led | **N5 wins** | Newest. Law order: magenta → purple → blue → green → gold. |
| Type scale: 24/18/14 shorthand vs Law 52 full scale | **Law 52 wins** | Newest and complete. 24/18/14 survives as the mnemonic; Law 52 (Display 32–40 / Headline 22–28 / Body 15–17 / Detail 12–13 / Kicker 11) governs. |
| Buttons: 4 showcase systems vs `.naya-btn` | **`.naya-btn` wins** | Law 21: one canonical button. Full variant/state/action spec. See retirements below. |
| Serif voice: N4 Cormorant → N5 Georgia → Naya_2 Newsreader | **Newsreader wins** | Newest. Georgia is the safe fallback. |
| Motion ease: PDF `cubic-bezier(.16,.84,.22,1)` vs N5 `cubic-bezier(.22,1,.36,1)` | **N5 wins** | Newest. Minor difference; N5 is pinned in TOKENS.css. |

## Retired systems — considered and retired

These were real studies. They lost to the one-language rule, not to lack of
beauty. Documented here so nobody reintroduces them as live options.

| Retired | Why `.naya-btn` won (one line each) |
|---|---|
| `.living-btn` (N5 hero study) | Its job is now `.naya-btn.lead` — one DNA, not two. |
| `.lv-btn` (N5 living system, 7 shadows) | Its proximity-wake behavior is now `.naya-btn.proximity` — same idea, one system. |
| `.cx-btn` (N5 essential study) | Simplicity is a variant choice inside the one system, not a separate system. |
| `.orbit-btn` (N5 orbit-ring study) | Kept as documented inspiration only. One system, no forks. |

**Rule:** BLOCKS.md lists the piece for each job — never competing systems
for the same job. If a new button idea appears, it becomes a `.naya-btn`
variant proposal, not a new system.

## Retired tokens & forms

- N4 square `.jw` jewels → superseded by the orb/diamond jewel language
  (orbs, mini-orb, gem-bullet, five-jewel cycle). One jewel language.
- N4 `--chrome: #9d75ff` → superseded by `--soul: #a06bff`. Same job, one token.
- Showcase-era `--obsidian: #020203` → superseded by `--obsidian: #0B0D12`.

## Open gaps — not hidden, not forgotten

- [CLOSED 2026-10-16] **Spacing scale.** `--space-*` tokens defined on a 4px
  base (`--space-base: 4px`, steps 1–24) + semantic `--gap-sm/md/lg/xl`.
  Grounded: N5 source padding/gap values cluster on 4px multiples
  (8/12/16/20/24/28/32/40/44/64). In TOKENS.css + TOKENS.md.
- [CLOSED 2026-10-16] **Ten canonical blocks' code specimens.** All 10 built
  in BLOCKS-CODE.md with code, states, do/don't, anatomy. Each verified by
  execution review before landing.
- [CLOSED 2026-10-16] **Machine artifacts.** Built from pinned sources (no
  invented values), housed in DESIGN/ to keep the library self-contained:
  `DESIGN/contract/naya-design-contract-v1.machine.json` (exact mirror of
  TOKENS.css + Law 52 + ship gate + machine predicates) and
  `DESIGN/tools/design_law/design_calculator.py` (0–100 scorer, v1 — covers
  machine-checkable predicates only: no private colors, 12px type floor,
  kicker word cap, 1.5px idle rims, token presence. Honest limits documented
  in-file: it checks conformance, not beauty — the human eye still required).
- [CLOSED 2026-10-16] **Board type names.** Confirmed verbatim in the Naya_2
  source: **Destination / Reading / Orbit** — "destination board",
  "reading board", "orbit board" all present. Canonical.
- [CLOSED 2026-10-16] **Per-room accent mapping.** Pinned verbatim from the
  Smart Hub applied source: feed=green, today=magenta, reports=indigo,
  library=blue, connect=teal, ledger=gold, connections=orange, lists=purple,
  mail=rich-orange, spaces=lime, settings=#e8eaf2. Added `--orange` and
  `--rich-orange` to the extended family (source-verified values, not
  invented). In TOKENS.css + TOKENS.md.
- [CLOSED 2026-10-16] **Newsreader webfont hosting.** Ruling: Newsreader is
  the voice serif via Google Fonts CDN (reliable, versioned). Georgia is the
  guaranteed fallback — where webfonts are unavailable, Georgia stands alone
  and the system does not degrade. Tokens `--font-ui`, `--font-voice` added.

## How rulings change

When Shawn corrects the design, the correction becomes a new law or sharpens
an old one — same day, in this directory. A ruling here changes only by a
newer generation or an explicit Shawn correction. Never by one Naya's taste.
