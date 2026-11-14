# RECORD — AUTO-TRANSLATE F4 MICRO-FIX (Area #41)

**Seat:** the auto-translate repair seat (Wrena's lane) — maker of this round
**Branch:** `personal/auto-translate-f4-fix-20261113` (parent = repair tip `8cbc69ee2d499dce33a1a5d8db200d801b4605ed`)
**Base:** repair build, staged sha `b98d2f5c9545c14735f450cbeecbd0ebf4670ca7b1ee12e2b488587f1715f51a`, 1,821,490 B, 26,091 lines — fetched from GitHub raw CDN on the repair branch, sha asserted before any edit (Step 0 PASS). The local worktree file is 0 bytes (EPERM damage) and was NOT edited or trusted.
**Brief:** `~/workspace/team-nitro/auto-translate-20261113/BRIEF-AUTO-TRANSLATE-F4-FIX-20261113.md` (check-brief 9/9)
**Verdict this round closes:** `CHECKER-VERDICT-AUTO-TRANSLATE-REPAIR-FIX-20261113.md` — FAIL, 8/10 for the build, 0 for the close. Nine of ten F-sites closed; F4 fails as rendered.
**Built file:** `f4-fixed.html` in this work dir — sha256 `aea38f65e4bdfbba167d723da38e020223016bfc15c97dbece6b67b2c863eb3f`, git blob `3396a3ae2e0142c13b40cd78f78ff43fc661b305`, 1,821,074 B, 26,094 lines.
**Staged link:** `https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/personal-page-complete-20261113/personal-complete.html&ref=personal/auto-translate-repair-fix-20261113&cb=20afd32c41fb2975adb23888f65bffa54e1d7bd1` (repair) → F4 fix staged on `ref=personal/auto-translate-f4-fix-20261113&cb=3396a3ae2e0142c13b40cd78f78ff43fc661b305` (filed in the same commit as this record; staged sha re-verified after filing — see §7).

## §1 — The defect (verdict §2, re-verified on the base bytes)

`KIND_META` (base line 12089) is a top-level `var` in the `<script id="os-dash-script">` block (starts line 11704). `window.mwTr` is defined at line 22877–22888, in the `<script id="mw-script">` block (starts line 19970). Script blocks execute in document order, so at line 12089 `window.mwTr` is `undefined` and every `(window.mwTr?window.mwTr('…'):'…')` in `KIND_META` takes the English fallback branch. `meta.subject` and `meta.quiet` are therefore baked English on every load in every language. Nothing rebuilds `KIND_META` on language change. The `renderBars` call site (line 11837) routes through `(quiet||mwTr('The next post, note, message or invite lights the first bar.'))` — but `quiet` is always a truthy English string, so the `mwTr` branch never fires. The byte inventory classifies the site GUARDED because the `mwTr` call is textually present; the render proves the guard is dead. The same mechanism covers the `Busiest:` branch (`subject||mwTr('Posts, notes, messages and invites together.')`).

Two structural facts found first-hand while grounding the fix (they decide the shape):
- The whole `os-dash-script` block is wrapped in an IIFE (opens line 11730 `(function(){`, closes line 12856). That is why `window.KIND_META` and `window.renderWeekFront` do not exist in the page — a direct-call forced render is impossible; the `Busiest:` branch must be exercised with **data** through the page's own `loadDashboard → renderWeekFront → renderBars` path.
- `window.osRerenderDashboard` (line 12779) calls `renderWeekFront(d)` on every language switch — `mwApplyLang` calls it at line 23027. The switch path DOES re-render; it re-rendered with baked-English meta values. A render-time fix therefore closes BOTH paths with no extra wiring.

## §2 — The fix (shape (a) from verdict §7)

Store the English keys in `KIND_META` and apply `mwTr` at the `renderBars` call site, so the values are never baked from a `mwTr` that does not exist yet.

**Hunk 1 — `KIND_META` (base lines 12089–12095, 5 kinds × subject/quiet):** all ten `(window.mwTr?window.mwTr('…'):'…')` expressions replaced by plain English string literals, with a 3-line comment naming the defect class so no later seat "fixes" it back to `mwTr` calls. `KIND_META` now has **zero** `mwTr(` calls inside it. No key was added or removed; the ten strings are the dictionary keys themselves.

**Hunk 2 — `renderBars` note line (base line 11837):** the two fallbacks now translate the passed value at render time: `(window.mwTr?window.mwTr(subject||'Posts, notes, messages and invites together.'):(subject||'Posts, notes, messages and invites together.'))` and the same shape for `quiet`. The `Busiest: ` prefix and the `A quiet stretch so far — the chart is waiting.` lead were already render-time `mwTr` calls and are untouched.

**Diff totals:** 3 hunks (+9/−6 lines: 1 renderBars line replaced, 1 comment block added, 5 KIND_META lines replaced), all inside the F4 region. Nothing else changed. The other renderBars (line 8201, the 6-param engine) already evaluates `mwTr` at render time and is untouched — it is a different engine, not an F4 site.

**Dictionary:** unchanged. Embedded `MW_I18N` parses as JSON: de/es/fr **807 keys each, 0 empty values, key sets identical** — byte-identical to the base. All ten F4 strings exist as keys in all three languages with correct values (verified first-hand before the edit — e.g. es quiet `La próxima publicación, nota, mensaje o invitación enciende la primera barra.`). No new keys were needed.

**Script parse:** all **36/36** inline `<script[^>]*>` blocks compile under node `vm.Script`, 0 failures.

**Guard sites:** `window.mwTr?window.mwTr(` count 631 → **621** (−10: the ten `KIND_META` calls removed, net of the two new render-time calls in `renderBars`). `data-mw-tr` markers unchanged at 371.

## §3 — The rendered proof (the re-proof the verdict demanded)

Method: Playwright VM Firefox (alive since the 23:02Z probe), probe `f4-probe.py` in this work dir. The `Busiest:` branch is exercised with **data**: Playwright route interception on Supabase `rest/v1/**` returns synthetic rows through the page's own `loadDashboard → renderWeekFront → renderBars` path (3 wall rows + 1 note row + 1 thread + 1 message + 2 invites, all with recent timestamps; every other table `[]`). The quiet branch is exercised with **empty** interception (all tables `[]`) — the same no-data state the checker proved the failure in. Both paths per case: **Path A** fresh load with the language preset (`ctx.add_init_script` + `JSON.stringify(lang)` — the checker's working preset method) and **Path B** switch-after-load from a clean context (true EN start, Settings select, `osRerenderDashboard` re-renders). Widths 390 / 1440 / 360. The note text is read from `#os-dash-week-note` verbatim.

**Result: 60 rendered note reads (3 languages × 2 branches × 5 kinds × 2 paths), ZERO English words in any of them.** Path A and Path B reads were identical in all 30 cases, so one set of 30 quotes covers both (each verified on both paths).

### Busiest branch (data mode) — verbatim

| kind | es | fr | de |
|---|---|---|---|
| all | Más activo: viernes: 5 eventos. Publicaciones, notas, mensajes e invitaciones juntos. | Le plus actif : vendredi: 5 événements. Publications, notes, messages et invitations ensemble. | Am aktivsten: Freitag: 5 Ereignisse. Beiträge, Notizen, Nachrichten und Einladungen zusammen. |
| posts | Más activo: viernes: 2 eventos. Solo publicaciones. | Le plus actif : vendredi: 2 événements. Publications uniquement. | Am aktivsten: Freitag: 2 Ereignisse. Nur Beiträge. |
| notes | Más activo: viernes: 1 evento. Solo Notas inteligentes. | Le plus actif : vendredi: 1 événement. Notes intelligentes uniquement. | Am aktivsten: Freitag: 1 Ereignis. Nur intelligente Notizen. |
| messages | Más activo: viernes: 1 evento. Solo mensajes recibidos. | Le plus actif : vendredi: 1 événement. Messages reçus uniquement. | Am aktivsten: Freitag: 1 Ereignis. Nur erhaltene Nachrichten. |
| invites | Más activo: jueves: 1 evento. Solo invitaciones registradas. | Le plus actif : jeudi: 1 événement. Invitations enregistrées uniquement. | Am aktivsten: Donnerstag: 1 Ereignis. Nur erfasste Einladungen. |

EN baselines (Path B, true EN start): `Busiest: Friday: 5 events. Posts, notes, messages and invites together.` — the switch re-renders it into the three columns above.

### Quiet branch (empty mode) — verbatim

| kind | es | fr | de |
|---|---|---|---|
| all | Un tramo tranquilo por ahora — el gráfico está esperando. La próxima publicación, nota, mensaje o invitación enciende la primera barra. | Une période calme pour l’instant — le graphique attend. La prochaine publication, note, message ou invitation allume la première barre. | Bislang eine ruhige Phase — das Diagramm wartet. Der nächste Beitrag, die nächste Notiz, Nachricht oder Einladung lässt den ersten Balken leuchten. |
| posts | Un tramo tranquilo por ahora — el gráfico está esperando. La próxima publicación enciende la primera barra. | Une période calme pour l’instant — le graphique attend. La prochaine publication allume la première barre. | Bislang eine ruhige Phase — das Diagramm wartet. Der nächste Beitrag lässt den ersten Balken leuchten. |
| notes | Un tramo tranquilo por ahora — el gráfico está esperando. La primera Nota inteligente enciende la primera barra. | Une période calme pour l’instant — le graphique attend. La première Note intelligente allume la première barre. | Bislang eine ruhige Phase — das Diagramm wartet. Die erste intelligente Notiz lässt den ersten Balken leuchten. |
| messages | Un tramo tranquilo por ahora — el gráfico está esperando. El próximo mensaje enciende la primera barra. | Une période calme pour l’instant — le graphique attend. Le prochain message allume la première barre. | Bislang eine ruhige Phase — das Diagramm wartet. Die nächste Nachricht lässt den ersten Balken leuchten. |
| invites | Un tramo tranquilo por ahora — el gráfico está esperando. La próxima invitación enciende la primera barra. | Une période calme pour l’instant — le graphique attend. La prochaine invitation allume la première barre. | Bislang eine ruhige Phase — das Diagramm wartet. Die nächste Einladung lässt den ersten Balken leuchten. |

EN baselines (Path B, true EN start): `A quiet stretch so far — the chart is waiting. The next post, note, message or invite lights the first bar.`

### Widths, overflow, console

- 390px: overflow `sw == iw` at scroll 0 AND scrolled, in every run (Busiest + quiet, es/fr/de).
- 1440px: `sw == iw` scroll 0 and scrolled (es data run).
- 360px: `sw == iw` scroll 0 and scrolled (es empty run).
- Console errors: **0** in every run; pageerrors: **0** in every run (with route interception — no Supabase traffic reaches the VM, so the known VM CORS noise is absent). Without interception the VM still shows the known Supabase CORS errors (environmental, as the checker documented in verdict §5 item 6); the page's own code threw zero page errors in every session here.

## §4 — F1–F10 rendered battery re-run (on the staged bytes)

Run after filing, with the checker's own probes pointed at the F4 staged link (copies in this work dir: `f4-battery.py` from `checker-probe-390.py`; `f4-translate.py` from `checker-probe-e.py`; `f4-translate2.py` from `checker-probe-f.py`), 390px unless noted.

**F1–F10 battery (switch path, es + de):**
- **F1** — es `🔌 Conectado a este mundo` ✓ · de `🔌 In dieser Welt eingesteckt` ✓. Verdict G7 (German eye-read) CLOSED.
- **F2 cap** — empty in both languages (no reading-state caption renders without spine data; zero English, not a failure — same as the checker's run). Carried as before.
- **F3 links note** — no note element renders without data (the selector finds nothing; the empty state does not render in this VM). Byte proof stands. Honestly carried.
- **F4 week note** — es quiet + de quiet fully translated ✓ (and the F4 probe proved Busiest + switch on staged — see §7).
- **F5 funnel** — es `Registrados · 00% de las invitaciones registradas se unieronSe unió · 0` ✓ · de `Erfasst · 00% der erfassten Einladungen sind beigetretenBeigetreten · 0` ✓.
- **F6 menu** — es `Publicar / Enviar un mensaje / Añadir un Smart Link / Añadir a una lista`, label `Añadir` ✓ · de `Posten / Nachricht senden / Smart Link hinzufügen / Zu einer Liste hinzufügen`, label `Hinzufügen` ✓.
- **F7 avedit** — es `Cambiar foto / Editar foto` ✓ · de `Bild ändern / Foto bearbeiten` ✓.
- **F10 dim btns** — `[]` (no Smart Link rows without data). Byte proof stands. Honestly carried.
- **Overflow** — scroll0 `390 == 390` in both runs; scrolled-to-bottom de `390 == 390`, es `420` (the checker's known transient — the Settings view is open at the end of that run, same as their v1 probe; the F4 probe's clean-load scrolled reads are `390 == 390` in every run).
- **Console** — TOTAL 136 console errors across the runs, **0 page errors**. Every console error is a failed Supabase `rest/v1` request (smart_links, smart_link_daily_stats, invites) — the VM cannot reach Supabase. The known environmental noise; the page's own code threw zero page errors.
- **Language persistence** — after reload, lang value es / de, localStorage `mw.set.lang` `"es"` / `"de"` ✓.

**Translate taps (fr, staged):**
- **Wall (Smart Note)** — view: `🌐 Traduit de l'anglais — Bonjour, ceci est un test écrit en anglais pour vérifier la traduction. — En résumé — Bonjour, ceci est un test écrit en anglais pour vérifier la traduction. — Une note humaine en anglais simple pour le chèqueur. — Afficher l'original` ✓ (probe-e E3 method).
- **Naya Note** — view: `🌐 Traduit de l'anglais — Vérifier les notes vocales — Ceci est un corps de notes vocales en anglais, parlé pour le vérificateur à traduire. — Afficher l'original` ✓ (probe-f F3 method: Naya tab clicked first; identical text to the checker's repair-build proof).
- **The Naya nulls, diagnosed honestly:** the first Naya runs returned `view: null` on the F4 build — and identically on the **repair-build control** (same probe, same null). The diagnostic (`f4-naya-diag.py`) proved the cause: the injected card is GONE 5s after the source-language click (`card=0`, `btn=0`) — the Naya feed repaints after the tab click (`mwLoadNayaFeed`), wiping the synthetic card before the EP returns. It is a race between the feed's async repaint and the probe's injection, not a defect and not a regression (identical on both builds). Letting the repaint settle (12s after the tab click) before injecting makes the tap render — the view above. The EP itself is healthy (direct curl: `ok:true`, returns exactly `Vérifier les notes vocales` / `Ceci est un corps de notes vocales en anglais, parlé pour le vérificateur à traduire.`).
- **Probe-e E4** times out because `#mwFeedNaya` is `hidden` until the Naya tab is clicked — a probe limitation, not a page defect; the checker's own Naya proof came from probe-f F3 (tab clicked first), the method used here.
- **F6 menu at 1440:** plusbtn rect `[0,0,0,0]` — `#pluswrap` is `display:none` on fresh load; the **repair-build control shows the identical state** (`pluswrap_disp: none`, same rect, same body class). Pre-existing, not a regression. The menu still opens via the `el.click()` fallback with translated items (probe-e E2: menu class `ph-plusmenu open`, fr items).

## §5 — Verdict §5 eye-check items: closed or honestly carried

- **F3 rendered empty state** — still carried: no note element renders without data in this VM; byte proof stands from the repair round (battery §4).
- **F8/F9 rendered display** — byte proof stands from the repair round (verdict §1); rendered display still owes a data-bearing environment (no media/wall notes render in this VM without Supabase data — the interception seeds Dashboard spine data only, not wall note rows for the media-notes display). Honestly carried, not claimed.
- **F10 rendered toggle** — same: no Smart Link rows render without data; byte proof stands. Honestly carried.
- **F2 quiet-state and birth-score captions** — the reading-state caption renders empty (zero English) without spine data in both languages; a populated-caption read still owes a data-bearing environment. Carried as before.
- **Translate tap on real citizen notes** — proven end to end on conforming synthetic cards of BOTH kinds on the staged bytes (battery §4: wall + Naya views verbatim, fr). A real-note tap still owes a data-bearing environment, as in the repair verdict.
- **Zero console errors in a real browser** — 0 page errors in this VM; the 136 console errors are all Supabase network failures (environmental). The captain's cloud-browser check closes it, as in the repair verdict.
- **F1 German eye-read** (verdict G7) — **CLOSED**: de `🔌 In dieser Welt eingesteckt` rendered on the staged bytes (battery §4).
- **Whole-page sense check** — the page reads as before in es/fr/de at 390/1440/360 (screenshots in the probe runs); the only visible change is the week-bars note now speaking the picked language. The full sense check with live data still owes the captain.

## §6 — What this round did NOT touch (brief Must NOTs, all held)

- No live touch, no merge, no PR. Staged only, new branch `personal/auto-translate-f4-fix-20261113` from the repair tip.
- No change outside the F4 region: the other nine sites hold (battery §4); the dictionary is byte-identical; the `dict-final.json` restore (0 bytes, EPERM damage) is still owed and is NOT this round's work.
- No change to the citizen's words, to proper names, to the Settings panel, the card labels, or the F1 word.
- No change to the follow-on surfaces in the checker verdict §4 (People view, Reports view, Smart Links view, message/inbox view, stats explainer).
- No new vendor, key, framework, or picker. No blanket auto-translation on load.

## §7 — Filing + staged verification

- Commit: `ab09ae3cf9a68f4a052dc9f7c3e6a08e8dbdfc61` on branch `personal/auto-translate-f4-fix-20261113`, parent `8cbc69ee2d499dce33a1a5d8db200d801b4605ed`, 1 commit ahead, 0 behind. Files in the commit: the page + this record + the scorecard + `f4-probe.py` + `file-f4-fix.py`. (Record §4/§7 were filled after the first filing; this completed record rides the amended branch tip — the tip sha is in the maker's final report to the captain.)
- Staged link: `https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/personal-page-complete-20261113/personal-complete.html&ref=personal/auto-translate-f4-fix-20261113&cb=3396a3ae2e0142c13b40cd78f78ff43fc661b305`
- Staged re-verification (after filing): curl of the staged link → sha256 `aea38f65e4bdfbba167d723da38e020223016bfc15c97dbece6b67b2c863eb3f`, 1,821,074 B, git blob `3396a3ae2e0142c13b40cd78f78ff43fc661b305` — MATCHES the filed bytes.
- F4 probe re-run on the staged link (es data + es empty, 390px): all 5 kinds, both paths, zero English words — Busiest `Más activo: viernes: 5 eventos. Publicaciones, notas, mensajes e invitaciones juntos.` and quiet `Un tramo tranquilo por ahora — el gráfico está esperando. La próxima publicación, nota, mensaje o invitación enciende la primera barra.`; overflow `390 == 390` scroll 0 and scrolled; console errors 0, pageerrors 0.

## §8 — The lesson this defect teaches (for the hive)

The byte inventory cannot catch this defect class: a `mwTr` call that is textually present but never fires reads GUARDED. The guard is dead when the call runs before the function exists (script-block order) or when a truthy baked value short-circuits the fallback (`subject||mwTr(...)` with `subject` always truthy). The re-proof must read the RENDERED text, not the guard — and the fix must move the evaluation to render time, not add another guard around a baked value. Any future `var X = {…mwTr(…)…}` at the top of an early script block is the same defect until proven rendered.

## §9 — Scorecard

See `SCORECARD-AUTO-TRANSLATE-F4-FIX-20261113.md` — maker claims 8/10, 2 points withheld for the checker/captain to award on the staged rendered re-run.
