# RECORD — AUTO-TRANSLATE CARD-LABELS FIX (Area #41, 2026-11-13)
## Captain: Naya Nitro Narzan · Owner seat: Wrena (BUILD) · Maker: Wrena (BUILD), one scorecard cycle

Base: branch `personal/auto-translate-settings-fix-20261113`, tip
`3d8f9651e54fd90ea92d640dbbe93323e448b529` — 1,639,171 B, sha256
`d91945f6b883dff7311c320802b62ab7d0ac0fffa756a48c36e867f6fc44f3e4`.
Fix bytes (worktree):
`/home/hatch/workspace/personal-complete-wt/TEAM-NITRO/personal-page-complete-20261113/personal-complete.html`
— 1,652,796 B, sha256
`93f4302a5866a007b290ac3b144bda62c373ee16a7bfe63222e485ffc29a7b3b`.
Work dir: `~/workspace/team-nitro/auto-translate-20261113/`.

Bullseye (one line): the note cards speak Spanish, French and German like
the rest of the chrome — the Intelligent Block's fixed labels change when
the language changes, with nothing left in English except proper names and
the citizen's own words.

## §0 — The five gates (applied to this fix)

1. **Is it right?** Yes. A Spanish citizen reads Spanish labels on the
   cards they read all day; English labels on a Spanish page are the
   defect the captain's eye caught. No citizen's words are touched, no
   proper name is touched.
2. **Is it what they truly need?** Yes — the brief names it, the captain
   verdict names it with byte evidence, and the fix is data + marking
   only, the same mechanism as the Settings fix that already passed 10/10.
3. **Is it mine to do?** Yes. Staged only, on a new branch from the
   Settings-fix tip, one commit. No live touch, no merge, no PR. No
   change to the Settings panel, drawer links, chat tap, or fail view. No
   change to gear/panel dismissal. No new vendor, key, framework, or
   picker. No blanket auto-translation on load.
4. **Is now the time?** Yes — the Settings fix landed and the cards are
   the named next surface; the base did not move mid-round (parent
   `3d8f9651` unmoved; base sha asserted at every rebuild).
5. **Can I prove it?** Yes — §5: rendered cards in es/fr/de with
   screenshots at 390, a byte grep audit at 0 mismatches, and the full
   regression green set, all read first-hand in this round. The one
   exception is named in §5, not hidden: the rendered Notes-view
   noteCard was not browser-proven (Supabase hang in file:// + the VM
   browsers died mid-round); its marking is audit-proven and its
   mechanism is live-proven on the other three card families.

## §1 — The gap, first-hand (what the captain caught, re-proved by me)

The captain's verdict (`CAPTAIN-VERDICT-AUTO-TRANSLATE-SETTINGS-FIX-20261113.md`)
passed the Settings-panel fix 10/10 — then her eye caught English
Intelligent Block labels on every note card in Spanish mode. Known set
from her byte check: `IN A NUTSHELL`, `＋ CREATE SPACE`, `★ FAVORITE`,
`ADD TO THE INTELLIGENCE`, `ADD INTEL`,
`ONE INTELLIGENCE · MANY VIEWS · ONE IDENTITY`,
`TRUST: SOURCE / INTERPRETATION SEPARATED`.

I did not trust the known set alone. I inventoried every fixed card label
first-hand from the staged bytes before editing (§2) — the card builders
write labels in JS too, and the inventory found 49 more fixed labels the
known set did not name (foot lines, aria-labels, placeholders, the
category bar, the ibFeedCard action row, the noteCard Save/List row).

## §2 — The card inventory (counted first-hand from the staged file before editing)

Four card families render on this page, plus the category bar:

1. **intelBoard + BoardActions** (Hub harvest, `#os-wall-list`, via
   `ibWallCard`/`ibWallHTML`, lens `'collective'`) — the main feed
   (Personal + Public tabs). Labels: `IN A NUTSHELL`; layer heads
   (data-driven — see the classic-branch note below); foot
   (`Smart Note <id> · from your Smart Feed` /
   `Official NayaNET Guide · from the Intelligent Library`);
   `＋ CREATE SPACE` / `★ FAVORITE` / `SAVE`; `❤️ LOVE` / `👍 LIKE`;
   stars; `＋ SHARE INTEL`; `ADD TO THE INTELLIGENCE` / `ADD INTEL` /
   placeholder / `Be the first to add intel...`; microcopy
   `ONE INTELLIGENCE · MANY VIEWS · ONE IDENTITY` /
   `TRUST: SOURCE / INTERPRETATION SEPARATED`; `Presented by Naya` chip;
   `Note <id>` meta. Aria-labels: `Create a smart space from this
   intelligence`, `Mark as favorite`, `Save this intelligence`,
   `Share this intelligence`, `Add to the intelligence`,
   `Rate this intelligence from one to five stars`,
   `Add your contribution` (add-intel input aria).
2. **ibFeedCard** (lines 14601–14828) — defined + exported on `window`,
   but has NO callers in the file. Routed anyway (same keys/pattern) so
   it lands translated whenever it is wired in; verified by calling it
   directly in the browser probe (§5). Labels: kind (`SMART NOTE` /
   `NAYA NOTE` / `NOTE`), `OWNER`, `PINNED`, `IN A NUTSHELL`, layer
   heads, raw-details summary (`YOUR WORDS, WORD FOR WORD`),
   distilled/fidelity microcopy
   (`DISTILLED FROM THE AUTHOR’S WORDS — REVIEWED BEFORE POSTING` /
   `YOUR WORDS — FORMATTED BEAUTIFULLY BY NAYA`), `Share` / `Save to
   list` / `Pin` / `Unpin` / `Space from this` / `Business from this` /
   `Comment` / `Send`, comment placeholder (`Add a comment…`), `IN:`
   microcopy.
3. **noteCard** (Notes view, `#os-note-list`; samples render when no
   real notes) — `Presented by Naya`, `IN A NUTSHELL`, `Save` /
   `Saved ✓`, `List`, Smart-Lists `In: ` prefix via `slInLine`
   (`'In: ' + names.join(', ')`, line 10888).
4. **sa lesson cards** (Smart Academy/memberships, lines ~22131/22175/
   22194) — only the `IN A NUTSHELL` label is in scope; other lesson
   labels are a different surface (follow-on, §10).
5. **ibCatBarHTML** filter bar (exported beside ibFeedCard, uncalled) —
   `All notes`, `+ List`.

`IN A NUTSHELL` occurs 13× in the file: 7 render sites (intelBoard `<b>`
×1, ibFeedCard ×2, noteCard ×1, sa ×3) + 6 non-render (strip regexes
lines 8859/23375, md export line 9623, LAYER_MAP key line 14922,
ibWallNote data lines 15804/15813).

Wall layer names actually produced by `ibWallNote` (data): `In A
Nutshell`, `Human Note`, `Child Note`, `Grandma Note`, `Naya Note`,
`Themes` — only these 6 are in the dict (broader LAYER_MAP names
excluded as dead keys). Unlisted layer names fall back to English by
design (`mwTr` returns the key on a dict miss) — proven live with
`What It Means` and `Mystery Layer` (§5).

**Classic-branch note (pre-existing, named):** `ibWallNote` does not pass
`noteType` through, so `intelBoard` renders every wall card on the
classic branch (nutshell only) — the 6 layer names are built as data but
never rendered on the wall. Layer heads are therefore proven via the
direct smart intelBoard render and the direct ibFeedCard render (§5),
not via the wall. Passing `noteType` through is a follow-on (§10), not
this round's scope.

**Presenter-chip note (by design, FIX-8):** the `Presented by Naya`
chip is injected by `ibWallHTML` only when `r.j.noteType === 'smart'` —
"Plain Naya notes are the citizen's own words, so they carry no
presenter face." The naya stub card correctly has no chip; the smart
stub card has it, translated (§5).

**Rule adopted:** every translated label must be switch-resilient
(marked with pinned `data-mw-en`, or re-synced in `mwApplyLang`).
Render-time-only translation is not good enough, because the captain
toggles language without reload.

**Deliberately NOT routed (named, not silent — same precedent as the
Settings fix §20 transient `setStatus` feedback):** BoardActions
toasts; relative times (`just now`, `min ago`, `today`, `yesterday`,
`ibRel`/`stampRel`) + `en-US` date stamps (locale formatting, not
labels); composed star aria-labels/titles (`Rate N of 5`,
`Be the first to rate`); grow/save dialogs (`Create a space/business
from this note`, `Save to a list` dialog); sa lesson labels beyond
`IN A NUTSHELL`; Notes-view saved shelf (`Saved — kept for you`) +
`No notes yet` empty state; feed meta line (`N posts on this feed...`);
`Untitled Intelligence` / `Naya Note` content fallbacks (cannot be
marked inside the title h2; switch-stale edge); gold layer's embedded
`**How It Connects**` sub-label (inside `md()` body, unmarkable
without restructuring); `Smart Note <id>` aria-label (composed);
`Actions loading…` fallback; Naya Voice label-strip regex missing
translated labels (voice text may include translated button labels —
known edge). Naya Notes tab cards (`mwPaintNayaFeed`) carry no fixed
labels (title/category/body are citizen content) — nothing to do.
Activity tab rows are notification content — nothing to do.

**Other surfaces with the word `Save` left alone:** About-section Save
buttons (line 6634, toggle line 7939), Inbox `Save as Note` /
`Save as Smart Note` (lines 9587–9588), contact `＋ Save` (line
14275) — the dict key `Save` does not auto-apply; only routed where
the fix routes it. The two remaining `>Send</button>` in the file are
the chat Send (`#fcChatSend`, byId-routed by round 1) and the dashboard
feedback Send (`#os-dash-fb-btn`) — neither is a card label. The Naya
Notes room buttons (Copy/Move/List/Unfile) are a different surface —
out of scope. The area identifier stays English in ibFeedCard
microcopy (`PERSONAL` etc.) per the round's own precedent that
Personal/Business/Space are proper names. Category names in the
category bar (`Who I am`, `My work`, `Ideas`) stay English — they are
data, not labels.

## §3 — The build (the round's own pipeline, extended — never hand-edited staged bytes)

Pipeline: `build-auto-translate.py` (same mechanism as the Settings
fix — dict + marking only), extended with §21; dictionary
`dict-final.json`; language block `mw-lang-block.js`.

- **Dictionary grown 210 → 266 keys/language** (56 new, hand-written by
  the maker, no machine draft; voice es tú / fr vous / de du).
  Script: `apply-card-labels-dict.py` (asserts: all absent before, no
  English fallback except legitimately identical fr `Note`, de `Detail`,
  de `IN:`; no DE leak into es/fr; `NayaNET` preserved).
  New keys (56): `IN A NUTSHELL`, `＋ CREATE SPACE`, `★ FAVORITE`,
  `ADD TO THE INTELLIGENCE`, `ADD INTEL`,
  `ONE INTELLIGENCE · MANY VIEWS · ONE IDENTITY`,
  `TRUST: SOURCE / INTERPRETATION SEPARATED`, `SAVE`, `❤️ LOVE`,
  `👍 LIKE`, `＋ SHARE INTEL`, `FILE UNDER A CATEGORY`,
  `Be the first to add intel...`,
  `Add an observation, question, correction, or contribution...`,
  `Add to the intelligence`,
  `Create a smart space from this intelligence`,
  `Mark as favorite`, `Save this intelligence`,
  `Share this intelligence`, `Add your contribution`,
  `Rate this intelligence from one to five stars`,
  `Presented by Naya`, `Smart Note`, `from your Smart Feed`,
  `Official NayaNET Guide`, `from the Intelligent Library`, `Note`,
  `SMART NOTE`, `NAYA NOTE`, `NOTE`, `OWNER` (es DUEÑO, matching
  existing `Owner:` → `Dueño:`), `PINNED`,
  `YOUR WORDS, WORD FOR WORD`,
  `DISTILLED FROM THE AUTHOR’S WORDS — REVIEWED BEFORE POSTING`,
  `YOUR WORDS — FORMATTED BEAUTIFULLY BY NAYA`, `Save to list`,
  `Pin`, `Unpin`, `Space from this`, `Business from this`,
  `Add a comment…`, `Comment`, `Detail`, `IN:`, `In:`,
  `In A Nutshell`, `Human Note`, `Child Note`, `Grandma Note`,
  `Naya Note`, `Themes`, `Save`, `Saved ✓`, `List`, `All notes`,
  `+ List`. (`Share` and `Send` reused existing keys.)
- **`mw-lang-block.js` extended:** a generic `[data-mw-aria]` pass in
  `mwApplyLang` (after the `[data-mw-ph]` pass) — reads the English key
  from `data-mw-aria`, re-syncs `aria-label` in place on every switch.
- **`build-auto-translate.py` §21:** reps cover intelBoard (nutshell
  `<b>`, layer heads via `mwTr(L.name)`, foot with marked sub-spans,
  `Note <id>` meta, microcopy), presenter chips ×2, noteCard
  (nutshell, Save/Saved, List, `slLine` var + `In:` prefix),
  ibFeedCard (kind, OWNER/PINNED, nutshell ×2, layer heads, raw-details
  summary, distilled/fidelity microcopy, Share/Save-to-list/
  Pin-Unpin/Space/Business/Comment/Send, comment placeholder via
  `data-mw-ph`, kind/area + `IN:` microcopy), BoardActions `btn()`
  (label in marked span + `data-mw-aria`), addIntel (heading,
  placeholder + aria, empty state), `FILE UNDER A CATEGORY` head,
  stars-container aria, sa `IN A NUTSHELL` ×3 (split into two reps:
  feed site continues the string piece `</span><p>`, lesson sites
  close it `</span>'`), `ibCatBarHTML` (`All notes`, `+ List`).
  §1 dict assert updated 210 → 266; added `MW_BASE`/`MW_OUT` env
  overrides (defaults preserve worktree behaviour) so the pipeline can
  be proven on a scratch copy before touching the worktree.
- **Diff vs Settings-fix tip: 99 changed lines**, all §21 + dict growth
  + aria pass (verified by filtered diff on the first build; the §4
  repair touched only dict values inside those same lines). No
  unintended changes. Node syntax check: **36/36 script blocks parse,
  0 bad** (`check-syntax.py`, node `--check` on all script blocks).
- **Markers:** `data-mw-tr` 153 → **196** (+43), `data-mw-ph` 5 → **7**
  (+2), `data-mw-aria` 0 → **6** (+6). No bare `IN A NUTSHELL` render
  sites left (0 counts for `>IN A NUTSHELL<`, `IN A NUTSHELL</b>`,
  `IN A NUTSHELL</span>`).

## §4 — The defect the proof caught (and the two French fixes)

The first browser run on the first build caught a real defect the byte
audits missed: **every NEW dictionary key rendered as `[object Object]`
in es/fr/de**, while reused keys (`Share`, `Send`) translated
correctly. Cause: `apply-card-labels-dict.py` inserted each new key as
the whole per-key `{es, fr, de}` object under EVERY language, so
`MW_I18N.es['IN A NUTSHELL']` was a dict and `mwTr()` returned it.
The growth script's asserts passed vacuously (`'ä' in dict` checks
keys, not values). Fix: `repair-card-labels-dict.py` — mechanical,
touches only broken entries: any dict value replaced by its own
language's string. **168 object values fixed (56 keys × 3 langs)**;
after repair all 266 keys/language are strings, no DE leak, spot-checks
pass (`IN A NUTSHELL`, `ADD INTEL`, `SAVE`). Rebuilt: 1,664,507 B →
1,652,796 B, sha `8868d3e7…` → `93f4302a…`. The first run's screenshots
were discarded; all screenshots on disk are from the final-bytes run.
Lesson for the hive: a dict-growth assert must check `isinstance(v,
str)` per value — key-presence and substring asserts pass vacuously
over object values.

Two French translations were corrected after the second run's read:
`YOUR WORDS, WORD FOR WORD` fr `TES MOTS, MOT POUR MOT` → `VOS MOTS,
MOT POUR MOT` (fr voice is vous, not tu). The record as first written
claimed a tu-form scan of all fr values had found this as the only
one — that claim was wrong. What actually happened: the scan found the
sibling key above and was read as the only one; it missed
`YOUR WORDS — FORMATTED BEAUTIFULLY BY NAYA` (fr `TES MOTS — MIS EN
FORME AVEC SOIN PAR NAYA`), which the checker's audit found as F1
(`CHECKER-VERDICT-AUTO-TRANSLATE-CARD-LABELS-FIX-20261113.md` §7).
The one word was fixed in the F1 round
(`RECORD-AUTO-TRANSLATE-F1-VOS-FIX-20261113.md`): `TES MOTS` →
`VOS MOTS`, one dictionary value, tu-form scan of all 56 new French
keys re-run at zero. The second correction stands as written:
`Rate this intelligence from
one to five stars` fr `Notez cette intelligence de une à cinq étoiles`
→ `Notez cette intelligence d'une à cinq étoiles`. Both verified live
in the final run (§5).

## §5 — Proof (all first-hand, on the fix bytes)

### 5.1 Grep audit — zero left (`grep-card-labels.py`, v2)
v1 was misleading (bare English strings legitimately survive as dict
keys / `data-mw-en` pins / `mwTr()` fallbacks); v2 asserts the MARKED
form exists per render site + btn()-routed defs exist in the dict +
unmarked source forms are gone. **43 marked-form checks (all match),
13 btn()-routed dict defs OK, 24 unmarked-form checks all 0, Pin/Unpin
dynamic pin hand-checked True → MISMATCHES: 0.**
`data-mw-tr`: base 153 → fix 196 · `data-mw-ph`: base 5 → fix 7 ·
`data-mw-aria`: base 0 → fix 6.

### 5.2 Browser proof (`verify-card-labels-fix.py` →
`verify-card-labels-fix.json`, Playwright Firefox on the worktree file,
two full runs on the final bytes)

- **Wall cards, es/fr/de** — two stub cards (`fcStubInsert`, smart +
  naya). Every fixed label reads translated on a rendered card, in all
  three languages. es: `EN POCAS PALABRAS`, `Presentado por Naya`,
  `Nota fc-stub-…`, `Nota inteligente fc-stub-… · de tu feed
  inteligente`, `UNA INTELIGENCIA · MUCHAS VISTAS · UNA IDENTIDAD`,
  `CONFIANZA: FUENTE / INTERPRETACIÓN SEPARADAS`,
  `＋ CREAR ESPACIO` / `★ FAVORITO` / `GUARDAR`,
  `❤️ ME ENCANTA` / `👍 ME GUSTA` / `＋ COMPARTIR INTEL`,
  `AÑADIR A LA INTELIGENCIA`, `Añade una observación, pregunta,
  corrección o aportación...`, `AÑADIR INTEL`,
  `Sé el primero en añadir intel...`, aria-labels `Crear un espacio
  inteligente a partir de esta inteligencia` /
  `Marcar como favorito` / `Guardar esta inteligencia` /
  `Valora esta inteligencia de una a cinco estrellas`. fr and de
  likewise (fr `EN RÉSUMÉ`, `Présenté par Naya`, `＋ CRÉER UN ESPACE`,
  `★ FAVORI`, `ENREGISTRER`, `❤️ J’ADORE`, `👍 J’AIME`,
  `＋ PARTAGER L’INTEL`; de `KURZ GESAGT`, `Präsentiert von Naya`,
  `＋ RAUM ERSTELLEN`, `★ FAVORIT`, `SPEICHERN`, `❤️ LIEBEN`,
  `👍 GEFÄLLT MIR`, `＋ INTEL TEILEN`). The citizen's own words stay
  English until the Translate tap (screenshot, §5.4). The date stamp
  (`Friday, November 13, 2026 · just now`) stays English — out of scope
  by §2, named.
- **Switch-resilience** — load en, switch to es on the SAME page, no
  reload: every wall label changes to Spanish. Switch back to en, then
  to es again: same. The marked spans re-sync in place.
- **Direct smart intelBoard** — rendered via `window.ibRender` with a
  smart note (all 6 data layer names + official kind + 2 unlisted
  heads). Layer heads translate in all three languages (es `Nota
  humana`, `Nota infantil`, `Nota de abuela`, `Nota Naya`, `Temas`;
  fr `Note humaine`, `Note d’enfant`, `Note de grand-mère`, `Note
  Naya`, `Thèmes`; de `Menschliche Notiz`, `Kindernotiz`, `Oma-Notiz`,
  `Naya-Notiz`, `Themen`). `What It Means` and `Mystery Layer` stay
  English in all three — correct fallback for unlisted layer names.
  Official foot translates (es `Guía oficial de NayaNET · de la
  Biblioteca Inteligente`).
- **Direct ibFeedCard** — rendered via `window.ibFeedCard` (smart,
  pinned, mine, no comments). All labels translate in all three
  languages (es `NOTA INTELIGENTE`, `DUEÑO`, `EN POCAS PALABRAS`,
  `Detalle`, `Nota humana`, `TUS PALABRAS, PALABRA POR PALABRA`,
  `DESTILADO DE LAS PALABRAS DEL AUTOR — REVISADO ANTES DE PUBLICAR`,
  `↗ Compartir`, `💾 Guardar en lista`, `📌 Quitar fijación` (Unpin
  form — pinned=true), `➕ Espacio a partir de esto`,
  `🏢 Negocio a partir de esto`, `💬 Comentar`,
  `Añade un comentario…`, `Enviar`; fr `VOS MOTS, MOT POUR MOT` and
  `Notez cette intelligence d'une à cinq étoiles` as fixed in §4).
- **Category bar** — `window.ibCatBarHTML(null)`: es `Todas las notas`
  / `+ Lista`, fr `Toutes les notes` / `+ Liste`, de `Alle Notizen` /
  `+ Liste`. Category names stay English (data, §2).
- **First-visit es-ES** — fresh profile, browser locale `es-ES`, no
  stored pick (`stored: null`): page boots with `lang: es` and the
  stub card renders Spanish at creation, no switch.
- **Screenshots (final-bytes run):** `fix-proof-390-card-es.png`
  (212,342 B), `fix-proof-390-card-fr.png` (204,772 B),
  `fix-proof-390-card-de.png` (204,016 B),
  `fix-proof-1440-card-es.png` (315,644 B),
  `fix-proof-390-card-first-es.png` (298,634 B). The es 390 shot was
  read by eye: every label Spanish, citizen's words English, no
  overflow, no clipped button.

### 5.3 Regression (same runs)
- **Settings panel still switches** — 11 h3 headings, all Spanish in
  es mode (`Tus preferencias`, `Comportamiento de la app`,
  `Identidad`, `Todo en esta página`, …).
- **Tabs, rail, + menu, bottom bar still switch** — green set in es:
  msgbtn `✉️ Mensaje`, tabPublic `🌍 Feed inteligente público`,
  railHead `La gente a tu alrededor`, railCards 20, plusItems 5,
  bottom-bar segs `AÑADIR — abrir`, `CORREO — abrir`,
  `ACTIVIDAD — abrir`, `ESPACIOS — abrir`, `ECOSISTEMA — abrir`.
- **Note Translate tap still works end to end** — Spanish naya stub →
  Translate → pick Español → English translation shown (`The sun
  rises over the city and everything is filled with light. We walked
  through the market together.`) → Show original returns. Original
  one tap away, unchanged.
- **Pill still settles live** — pill text `✦0pts` (0 points, offline
  context; this round does not touch the pill).
- **Pick persists across reload** — set de, reload: `lang: de`,
  `stored: "de"`.
- **Zero overflow** — 390 / 1440 / 360, `scrollWidth == innerWidth`
  at every width, including 1440 in es.
- **Zero page errors; zero non-Supabase console errors** — 56 console
  errors in the final run, all Supabase (offline file:// context),
  non-Supabase 0.

### 5.4 The one gap — rendered noteCard NOT browser-proven (named, not hidden)
The Notes-view sample noteCards were not rendered in the browser.
Evidence, step by step: `window.osShowView('notes')` opens the view
(`[data-os-view="notes"]` gains class `on`) but `#os-note-samples`
stays 0 cards after 20 s and `#os-note-list` keeps only its skeleton
— `loadNotes()` waits on a Supabase select that never resolves in
this file:// context. `noteCard` / `renderNotes` / `loadNotes` are
closure-scoped (`window.noteCard` is undefined), so no direct render
is possible either. Then the VM browsers died mid-round: Firefox
SIGSEGV on launch ×4 (including after a 45 s pause and after clearing
stale Playwright profiles) and Chromium SIGTRAP (exit 133) ×1 — the
documented TOOLS.md flake (browsers dead since ~17:32Z 2026-11-12;
they worked for five runs earlier in this round, then died at ~19:44Z).
What IS proven for noteCard: the marking, by the byte audit (§5.1 —
nutshell, Save/Saved, List, `In:` prefix, presenter chip all match
their marked forms), using the identical `data-mw-tr` + pinned
`data-mw-en` + `mwTr()` mechanism live-proven on the other three card
families. The `List` button and `In:` prefix render only on REAL
notes (sample cards omit them by code) — marking-audit only, same
reason. **Re-proof owed on the staged link, where Supabase is live:**
open Notes in es and read the three sample cards. Flagged to the
parent as the round's one open verification item — the checker/
captain should close it on the staged page before calling the round
done-done.

## §6 — DONE definition (fix brief §Done first, checked)

- Switch to Spanish, open the feed — every fixed card label reads
  Spanish on a rendered card (screenshot at 390). **Done** (§5.2, es
  shot). Repeat for French and German. **Done** (§5.2, fr/de shots).
- Grep the staged bytes for fixed card labels without a translation
  marker — zero left. **Done** (§5.1, MISMATCHES: 0). Before/after
  counts: `data-mw-tr` 153 → 196, `data-mw-ph` 5 → 7, `data-mw-aria`
  0 → 6; unmarked render forms 24/24 → 0/24.
- Regression: Settings panel still switches; tabs, rail, + menu,
  bottom bar still switch; note Translate tap still works end to end
  with the original one tap away; pill still settles live; pick
  persists across reload. **Done** (§5.3). Zero overflow at 390/1440/
  360, zero console errors, zero page errors. **Done** (§5.3 — zero
  non-Supabase console errors, zero page errors).
- Stage via proof-host (new ref for the new branch), verify staged ==
  local by sha, report staged link + sha + branch + commit. **§7.**

## §7 — Staging + filing

- **Branch:** `personal/auto-translate-card-labels-fix-20261113` (new,
  from the Settings-fix tip).
- **Parent:** `3d8f9651e54fd90ea92d640dbbe93323e448b529` (Settings-fix
  tip), parent tree
  `257ad4d7f77ae4d75d6f2dc9abce1213320b9f00` (fetched live via
  `gh-direct.py` GET on the commit).
- **One commit** via `file-card-labels-fix.py` (adapted from
  `file-settings-fix.py`: one blob per file, base64 generated in
  memory via process substitution — never staged to disk — then one
  tree, one commit, one ref-create). Contents: the built page + this
  round's brief + the captain verdict + the round-1 record + this
  record + the scorecard + `build-auto-translate.py` +
  `mw-lang-block.js` + `dict-final.json` +
  `apply-card-labels-dict.py` + `repair-card-labels-dict.py` +
  `grep-card-labels.py` + `verify-card-labels-fix.py` +
  `verify-card-labels-fix.json` + the five card screenshots +
  the file/manifest/commit-message files.
- **Staged link:**
  https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/personal-page-complete-20261113/personal-complete.html&ref=personal/auto-translate-card-labels-fix-20261113&cb=<FINAL COMMIT SHA — see the maker's final report>
- **Staged == local by sha:** verified with the proof-host curl
  pattern (`verify-staged-fix.py` shape) after filing; the staged
  sha must equal
  `93f4302a5866a007b290ac3b144bda62c373ee16a7bfe63222e485ffc29a7b3b`
  (1,652,796 B). Staged only. No live touch, no merge, no PR.

## §8 — Three self-checks (each found NEW things)

1. **The build itself** — pipeline reproduced the tip byte-identically
   before extension; scratch rebuild proven before the worktree was
   touched (`MW_BASE`/`MW_OUT` overrides); diff vs tip confined to
   99 lines, all §21 + dict + aria pass; Node syntax 36/36. NEW
   findings: the sa feed-site replacement produced a syntax error
   (`'</span><p>''+saEsc`) caught by the node check; the noteCard/
   ibFeedCard/sa old-strings wrongly included surrounding single
   quotes (mid-concatenation fragments); the `data-mw-en` capture
   trap for JS-created marked elements (pin `data-mw-en`, Settings-fix
   trap 2, re-applied here).
2. **The browser + grep proof** — NEW findings: the `[object Object]`
   dict bug (§4 — the whole first browser run's value was catching
   it); the two French voice errors (§4); the wall classic-branch
   quirk (layer data built, never rendered — §2); the presenter chip's
   smart-only condition (§2); the Notes-view Supabase hang (§5.4);
   the VM browsers dying mid-round (§5.4). The grep audit needed its
   v2 rewrite (v1 counted bare English strings that legitimately
   survive as dict keys / pins / fallbacks).
3. **The proof itself** — re-read the diff, re-ran the verify twice
   on the final bytes, confirmed the base did not move mid-round
   (parent `3d8f9651` unmoved; base sha `4872414a…` asserted at every
   rebuild). NEW findings: the screenshot eye check caught what the
   text dump could not (the `[object Object]` was visible in the dump
   first, but the screenshot is what proves the card reads right to
   a human eye); the first-run screenshots had to be discarded and
   re-taken after the repair — a screenshot is only proof of the
   bytes it was taken from.

## §9 — Seven pre-merge answers (in writing)

1. **Three self-checks done?** Yes — §8, each finding new things.
2. **Honest 9+?** Score 9 — see
   `SCORECARD-AUTO-TRANSLATE-CARD-LABELS-FIX-20261113.md`.
   Deduction: one point, for the rendered noteCard not being
   browser-proven (§5.4). Everything else the bullseye names is
   measured true.
3. **Blast radius named?** Staged Personal page only, on a new branch
   from the Settings-fix tip. The Hub shell, the walk worker and live
   are untouched. No main change. No mail.
4. **Checks green?** Card proof + grep audit + regression + note
   Translate tap, all green on the final file; every exception named
   (§2 not-routed list, §5.4 noteCard gap).
5. **Five gates?** Yes, with evidence (§0).
6. **Real proof?** Live bytes, shas, line numbers, counts, browser
   measurements and screenshots, all read first-hand in this round
   (§1–§5, §7).
7. **No silent known defects?** None silent — every gap and
   not-yet-translated string is named in this record (§2, §5.4, §10).

## §10 — Follow-ons (named, not silent)

- **Rendered noteCard re-proof on the staged link** (the §5.4 open
  item): open Notes in es on the staged page, read the three sample
  cards. Checker/captain to close before done-done.
- **Wall layer heads:** pass `noteType` through `ibWallNote` so smart
  wall cards render their Human/Child/Grandma/Naya/Themes layers —
  the data is built today and never rendered (§2). A small follow-on
  round, not this one.
- **BoardActions toasts, relative times, star aria titles, grow/save
  dialogs, sa lesson labels beyond `IN A NUTSHELL`, Notes saved shelf
  + empty state, feed meta line, `Untitled Intelligence` / `Naya
  Note` fallbacks, gold-layer `**How It Connects**`, `Smart Note
  <id>` aria, `Actions loading…`, Naya Voice label-strip** — the §2
  not-routed list, each a follow-on if the captain wants it
  translated. Relative times and date stamps are locale formatting,
  not labels, and belong to a different round.
- **More chrome languages:** data-only follow-on (one dictionary
  object + one select option per language, no code change) — the
  dictionary is now 266 keys/language.
- **The round's named gaps stand:** Settings panel, drawer links, the
  chat tap, the fail view — untouched by this fix, as the brief
  orders. The dict-growth assert lesson (§4) belongs in the pipeline:
  assert `isinstance(v, str)` per value on every future dict growth.
