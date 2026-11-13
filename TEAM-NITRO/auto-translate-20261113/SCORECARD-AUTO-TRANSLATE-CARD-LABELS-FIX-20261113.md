# SCORECARD — AUTO-TRANSLATE CARD-LABELS FIX (Area #41, 2026-11-13)
## Captain: Naya Nitro Narzan · Owner seat: Wrena (BUILD) · Maker: Wrena (BUILD)
## One honest scorecard cycle. Score: **9 / 10**

The bullseye: the note cards speak Spanish, French and German like the
rest of the chrome — the Intelligent Block's fixed labels change when the
language changes, with nothing left in English except proper names and
the citizen's own words. Measured true everywhere except one place: the
rendered Notes-view noteCard was not browser-proven (§5.4 of the
record). One point off for that, and no higher until it is closed on
the staged link.

## 10 things I love

1. Every wall label translates in all three languages, switch-resilient,
   no reload needed — load en, switch to es, the whole card changes in
   place.
2. The first browser run caught the `[object Object]` dict bug before it
   could reach the captain's eyes. The proof did its job.
3. The grep audit v2 is a real zero: 43 marked-form checks, 13 dict
   checks, 24 unmarked-form checks, 0 mismatches — not a vacuous pass.
4. The direct-render probes prove the uncalled renderers too
   (`ibRender`, `ibFeedCard`, `ibCatBarHTML`) — no "it has no callers
   so we skipped it".
5. First-visit es-ES renders Spanish at creation with no stored pick —
   a new Spanish citizen meets a Spanish page.
6. The Translate tap still works end to end with the original one tap
   away — the citizen's words were never touched by this round.
7. The regression green set held everywhere: Settings, tabs, rail, +
   menu, bottom bar, persistence across reload, zero overflow at
   390/1440/360.
8. The es 390 screenshot reads right to a human eye — I looked at it
   myself, not just the text dump.
9. Two French voice errors caught and fixed by reading, not by a test:
   TES→VOS, de une→d'une.
10. The record names the one gap instead of hiding it. Done means
    proven, and unproven is written down.

## 10 things I don't love

1. The dict-growth script shipped object values — every new label
   rendered `[object Object]`, and the asserts passed vacuously.
2. The rendered noteCard was never browser-proven: Supabase hang in
   file://, then the VM browsers died.
3. The List button and `In:` prefix only render on real notes — no
   rendered proof exists for them even in principle in this context.
4. The wall builds layer data it never renders (classic branch) — the
   layer heads are proven by direct render, not by the feed the citizen
   sees.
5. The first verify run's screenshots were worthless (taken on broken
   bytes) and had to be re-taken.
6. The grep audit needed a v2 rewrite — v1 was misleading about what
   "bare English left" means.
7. Two French translations shipped wrong in the first build and needed
   a second pass.
8. The VM browsers died mid-round and I burned four launch attempts
   before stopping.
9. The Notes view can't even be opened in file:// context — the offline
   probe story is fragile (the `sb`/`getSb` dependency).
10. The not-routed list is long — toasts, times, dialogs, shelf, meta,
    fallbacks — the cards still carry English in those corners.

## 10 things to make it 10x

1. Assert `isinstance(v, str)` per value in every dict growth — the
   `[object Object]` bug can never recur.
2. Re-prove the rendered noteCard on the staged link (live Supabase)
   and close record §5.4.
3. Pass `noteType` through `ibWallNote` so smart wall cards render
   their layers — the feed the citizen sees, not a direct render.
4. Route the not-routed list in follow-on rounds, starting with the
   toasts and the grow/save dialogs — the most-seen English left.
5. Add a rendered-noteCard probe that works offline (a test seam for
   `noteCard`, or a stubbed `sb`) so the Notes view is provable in
   file://.
6. Translate relative times and date stamps via locale formatting
   (`Intl.DateTimeFormat` / relative-time) as its own round.
7. Add the sa lesson labels beyond `IN A NUTSHELL`.
8. Put the fr voice scan (tu-forms) into the dict-growth script as an
   automatic check.
9. Keep the screenshot discipline: a screenshot is only proof of the
   bytes it was taken from — re-take after every rebuild, automatically.
10. Fix the VM browser flake at its root (or route verification through
    the cloud browser by default) so a round never loses its last probe
    to a SIGSEGV.

## Score: 9 / 10

Nine because the bullseye is measured true on every surface the browser
could reach — wall, smart, feed card, category bar, Settings, tabs,
rail, + menu, bottom bar, Translate tap, persistence, overflow — in
es, fr and de, at switch and at first visit. One point held back for the
rendered noteCard, which is audit-proven but not browser-proven. When
the staged link closes §5.4, this round is a 10.
