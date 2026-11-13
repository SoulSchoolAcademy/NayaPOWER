# RECORD — AUTO-TRANSLATE SETTINGS-PANEL FIX (Area #41, 2026-11-13)
## Captain: Naya Nitro Narzan · Owner seat: Wrena (BUILD) · Maker: Wrena (BUILD), one scorecard cycle

**Base:** branch `personal/auto-translate-20261113`, tip
`f9242820df009ce0270b2e4ad93cd5cbe98a170c` — 1,621,175 B, sha256
`28ca21fa376ddaeb7a8a51f935407e7465bff68fd79d3d99b03958b83c8e4403`
(verified by the maker before any edit: remote tip via ls-remote +
captain's copy `captain-staged-check.html` re-sha'd, both exact).
**Fix branch:** `personal/auto-translate-settings-fix-20261113` (new, from
that tip). **Fix file:** `TEAM-NITRO/personal-page-complete-20261113/personal-complete.html`
— **1,639,171 B, sha256 `d91945f6b883dff7311c320802b62ab7d0ac0fffa756a48c36e867f6fc44f3e4`**,
23,575 lines.
**Work dir:** `team-nitro/auto-translate-20261113/` (same dir as the round).

## §0 — The five gates (applied to this fix)

1. **Is it right?** Yes. A citizen who picks Spanish should read the
   whole page in Spanish, including the panel where they picked it.
2. **Is it what they truly need?** Yes — the brief promised every label;
   the Settings panel is where a citizen meets the language choice itself.
3. **Is it mine to do?** Yes. Staged only, on a new branch from the
   auto-translate tip, inside the fix brief's scope. No live touch, no
   merge, no PR, no money, no credentials.
4. **Is now the time?** Yes. The corrections round is held behind this
   landing; the fix unblocks the queue.
5. **Can I prove it?** Yes — switch to es/fr/de, open the panel, every
   label changed, screenshots at 390; grep the staged bytes for unmarked
   Settings labels — zero left (§5).

## §1 — The gap, first-hand (what the captain caught, re-proved by me)

The round's marked lower half of the panel DID translate — my probe of the
tip file (Playwright Firefox, 390, switch to es, gear open) read
"Ajustes comunes — todas las páginas", "Menciones y respuestas",
"Ir al Hub principal" in Spanish. The unmarked upper half stayed English:
"⚙️ Your Preferences", "Deep black", "Notifications", "Smart Tabs drift",
"Motion & glow", "Auto-refresh", "Identity", "Public profile",
"Your story", "Your feed", "Everything on this page" and every room button
— exactly the captain's list. The mechanism was never broken; the labels
were never marked and their English strings were never in the dictionary.

## §2 — The Settings-panel inventory (counted first-hand from the staged file before editing)

Panel = `#settings`, lines 7152–7250 of the tip file. Every heading, every
row label, every sub, every button, the picker, the checklist, the install
card, the runtime-appended Account card. 20 `os-setrow` rows, 10 `h3`s.

**Unmarked before the fix (36 static labels, grep-verified on the tip):**

| Group | Unmarked | Labels |
|---|---|---|
| Row labels (`<b>`) | 6 of 20 | Deep black, Notifications, Smart Tabs drift, Motion & glow, Auto-refresh, Public profile |
| Row subs | 6 of 20 | "This app's deep-black theme.", "Kept on this device — nothing is sent yet.", "The tab ribbon glides slowly, one way — the NayaNET standard.", "Breathing light and living motion across the app.", "Quietly re-reads whichever board is open — feed, today, inbox, reports or dashboard — every minute.", "On — visitors can see your profile, make a post on your feed and message you. Off — this app is private." |
| Headings (`h3`) | 4 of 10 | Your Preferences, App behaviour, Identity, Everything on this page |
| Panel title | 1 | Settings |
| Room buttons | 12 | 🌍 My World, About, Today, Notes, Connections, Message, Inbox, Invite, Lists, Scheduler, Reports, Memberships |
| Identity | 3 | "Owner:", the `#os-id-line` paragraph, "This identity is what every app's gate checks — change it here and it changes everywhere." |
| Identity buttons | 2 | Your story, Your feed |
| Everything sub + label | 2 | "Every room on this page, in one place — and the doors to your other worlds.", "Your other worlds:" |

**Proper names — correctly left English (captain-cleared, unchanged):**
Dashboard, Home (the drawer's own precedent — "Home/Hub stays, two
proper names"), Business, Space, the My World checklist
(Personal/Business/Contacts/About), the owner's name "Shawn Vibert",
"NayaNET" inside translated sentences, the membership names (Naya Academy,
AI Masterclass, Fast Action Club) and URLs (data, never chrome).

**JS-written strings that marking alone could never close (14, all found
first-hand in the bytes and the live DOM):**
- `loadSettingsData()` re-writes `#os-id-line` in English on EVERY
  Settings open — a marked paragraph would be overwritten the moment the
  citizen opened the panel.
- `renderInstallState()` re-writes `#os-install-state` on every open:
  the installed line, "Ready to install.", the not-installed line, the
  click-fallback line (4 strings).
- The auth IIFE writes the Account card at boot: h3 "Account", the
  "Sign in so NayaNET knows it's you — …" paragraph, the "Sign in" button
  (set in two places: creation + `updateAuthUI`).
- The round-2d decorator appends an ⓘ button INTO the card's h3 and an
  explanation panel under it ("Your email is your key. …"), plus the
  aria-label "What does signing in do?" (2 strings).
- `mwRenderCoverSlots()` renders the five cover-slot inputs with English
  placeholders ("Button name — e.g. Naya Academy", "URL — enter it and the
  button wakes up") and aria-labels ("Cover button N name/URL") — found by
  the EYE check of the Spanish screenshot, which a textContent dump cannot
  see (4 keys).

**Deliberately NOT routed (named, not silent):** the transient
`#os-set-status` feedback after a flip ("Smart Tabs drift is on — …
Saved on this device.", 6 switches × on/off) and the two conditional
status notes in the cover area ("No empty spot for Join NayaNET — turn off
a button first.", "Everything is back — strip top, all three cover buttons
on.") — feedback after an action, not labels. The signed-in auth button
("✓ " + the citizen's email) is data, never translated. The `confirm('Sign
out?')` dialog is a browser modal, not a panel label.

## §3 — The build (the round's own pipeline, extended — never hand-edited staged bytes)

The original build script was run FIRST on the restored pristine base and
reproduced the tip byte-identically (1,621,175 B, sha `28ca21fa…`) — the
pipeline is faithful before it is extended. Then:

- **Dictionary 167 → 210 keys/language** (`dict-final.json`): 37 keys in
  `apply-settings-fix-dict.py`, 2 in `apply-settings-fix-dict2.py`, 4 in
  `apply-settings-fix-dict3.py`. Drafted through the round's own Workers AI
  staging worker (`draft-settings-fix.py`, 111 segments, 0 failed) and
  reviewed string by string by the maker — the machine draft was bad in
  exactly the ways the first maker warned about: it dropped sentences,
  read "feed" as food ("tu alimentación", "Ihr Futter"), read "Sign in"
  as a road sign ("señales en"), read "Auto-refresh" as a soft drink
  ("Auto-refresco") and a fridge ("Auto-refroidissement"), used Sie where
  the page's voice is du, and invented "App-Gateway". Every value in the
  dict is the maker's correction. Voice: es tú, fr vous, de du — the voice
  the existing dictionary already uses. Assertions in the apply scripts:
  210 keys/language, no English fallback (except fr "Notes" and fr
  "Notifications", legitimately identical words, and de "Name"), no DE
  value leaking into es/fr, "NayaNET" preserved inside every sentence
  that carries it.
- **One voice correction to a round-1 value:** the install card's de line
  said "Setzen Sie…" (Sie) while every other de line on the panel is du —
  corrected to "Setze diese App auf deinen Startbildschirm — sie öffnet
  sich wie jede andere App, ohne Browserleisten." Before/after named here.
- **Build script §19 (static markings):** the round's own marking pattern
  (§11) — a label alone in its element gets `data-mw-tr="set"`; a label
  sharing its parent with an icon gets its words wrapped in
  `<span data-mw-tr="set">`, harvested from the "Common settings" heading.
  Every rep count-asserted (all 1, except "Sign in" at n=2 — the two
  sites that set it).
- **Build script §20 (JS routings):** each JS-written string routed
  through `mwTr` with the `TR()` guard — the §8/§9 precedent. The
  `mwApplyLang` re-syncs in `mw-lang-block.js`: it re-runs the global
  `renderInstallState()` on every switch, re-syncs the auth button only
  while signed out, re-syncs the info-button aria-label, and syncs the
  slot placeholders + aria-labels IN PLACE — never re-rendering the slots
  on a switch, which would wipe text the citizen is typing into a slot.
- **Two traps the second pass caught, both proven in the browser:**
  1. The decorator's ⓘ button sits INSIDE the auth h3, so a marker on the
     h3 reads "Accountⓘ" as its key (dict miss — stays English) and a
     textContent write would WIPE the button. The marker moved onto a span
     inside the h3, and the English key is pinned with `data-mw-en` so a
     first-visit non-English boot cannot capture the translated text as
     the key.
  2. The same capture trap applies to every JS-created marked element
     (auth paragraph, info panel): their `data-mw-en` is pinned at
     creation for the same reason.
- **Diff vs tip:** 22 changed blocks, all inside the Settings panel, the
  three JS writers, the decorator, the slot renderer, the `MW_I18N` line
  and the `mwApplyLang` re-sync. Nothing else moved. `data-mw-tr` count
  114 → 153 (whole file); inside the panel 51 → 87.

## §4 — Credit owed to the first maker — Wrena

**Wrena (BUILD)** built the first version of this round 16:45–17:26Z and
died on a transport failure, not a task failure. Two of her fixes are real,
in the build, and verified first-hand by the second maker — and now by
this fix maker too:

- **Her dictionary preserve-step regex fix** (`review-dict.py`): the first
  version of the preserve parse used a regex span that ran past the
  language boundary, and last-match-wins took the DE values into es and fr
  for 12 of the 17 preserved keys ("My World" read "Meine Welt" in
  Spanish). She caught it in self-check 4 and re-parsed by LINE, with
  asserts proving es/fr/de values (`existing['es']['My World'] ==
  'Mi mundo'`, fr `'Mon monde'`, de `'Meine Welt'`). The fix is in the
  filed `review-dict.py` and the grown dictionary carries her preserved
  values verbatim.
- **Her Unicode-aware icon regex** (built-file line 20436):
  `var icon=(el.textContent||'').match(/^([^\p{L}\p{N}'’]+\s)/u);` —
  `\p{L}` not `\w`, because JS `\w` is ASCII-only and a French "À propos"
  or German "Über"/"Ändern" had its first letter eaten into the "icon" on
  the next switch ("ⓘ À Über"). It is in the build, at line 20436, and
  this fix's browser runs prove it live: the French row button reads
  "ⓘ À propos" and the German "ⓘ Über" with the icon intact (checker §2,
  re-confirmed in this fix's green set).

The record credited her dictionary work generally but not these two fixes
by name. This line corrects that. — Wrena, first maker of Area #41.

## §5 — Proof (all first-hand, on the fix bytes)

Scripts: `verify-settings-fix.py` → `verify-settings-fix.json`;
`verify-settings-fix2.py` → `verify-settings-fix2.json`.
Screenshots: `fix-proof-390-settings-{es,fr,de}.png` (element shots of the
whole `#settings` panel at 390).

- **Panel, all three languages (390):** 123 labelled items dumped per
  language. Every row label, sub, heading, button and note reads in the
  picked language. Zero-English audit against the full must-go list
  (labels + slot placeholders + aria-labels): **0 hits in es, 0 in fr,
  0 in de**. Remaining English is only the intended proper names (Home,
  Dashboard, Business, Space, Personal, Contacts, About in the checklist,
  "Shawn Vibert", "NayaNET" inside sentences) plus the round's own quoted
  trio names "(Mail · Activity · Space)" inside the autofold sub and the
  legitimately identical French words ("Notes", "Notifications").
- **Grep counts (brief proof 3):** setrow `<b>` unmarked 6/20 → **0/20**;
  subs unmarked 6/20 → **0/20**; `h3` unmarked 4/10 → **0/10**; title
  unmarked → marked; `data-mw-tr` in the panel 51 → 87.
- **Auth card (§3 trap 1, pass 2):** es h3 span "Cuenta", fr "Compte", de
  "Konto" — info button STILL inside the h3 in all three (not wiped);
  aria-label es "¿Qué hace iniciar sesión?", fr "À quoi sert la connexion
  ?", de "Was bringt das Anmelden?"; info panel text translated whole in
  all three; button es "Iniciar sesión", fr "Se connecter", de
  "Anmelden". First-visit es-ES: the card is created translated at boot
  ("Cuentaⓘ", panel in Spanish) — the `data-mw-en` pin holds.
- **Cover slots:** all five slots' placeholders + aria-labels translated
  in es/fr/de (e.g. es placeholder "Nombre del botón — p. ej., Naya
  Academy", aria "Botón de portada 1 Nombre"; de "Button-Name — z. B. Naya
  Academy", "Cover-Button 1 Name").
- **Regression (brief proof 4):** switch still works on tabs, rail,
  + menu, bottom bar — es `msgbtn` "✉️ Mensaje", `tabPublic`
  "🌍 Feed inteligente público", railHead "La gente a tu alrededor",
  rail 20 cards, + menu 5 items, bottom-bar segs
  "AÑADIR / CORREO / ACTIVIDAD / ESPACIOS / ECOSISTEMA — abrir". A note
  Translate tap still works end to end: Spanish stub → "🌐 Translated
  from Spanish / The sun rises over the city and everything is filled
  with light. We walked through the market together." with "Show original"
  bringing the original back. The pick persists across reload (`stored:
  "de"`, `lang: de` after reload).
- **First visit:** locale es-ES → page picks es with no tap (`stored:
  null`); the Settings panel opens translated at boot — install state,
  id-line and auth card all Spanish (§5 pass 1).
- **Hygiene:** page errors `[]`; console 56, all Supabase
  (`console_non_supabase: []`); overflow 0 at scroll 0 AND scrolled at
  390/1440/360 (390/390, 1440/1440, 360/360).
- **Must NOTs, all held:** no live touch, no merge, no PR; the gear's
  open/close behaviour untouched (the panel was opened once per run with
  the same single click the round used); the welcome sentence and world
  names untouched; no new vendor, key, framework or picker; no blanket
  auto-translation on load; the drawer links, chat tap and fail view
  untouched.

## §6 — DONE definition (fix brief §Done first, checked)

- **Exact element:** the staged Personal complete page's Settings panel —
  headings, every row label + sub, the picker labels, the room buttons,
  the install card, the Account card, the slot placeholders. DONE — all
  of it carries the grown dictionary and the switch.
- **Exact change:** every label in the panel added to `MW_I18N` in
  es/fr/de (167 → 210 keys/language), marked with `data-mw-tr` where the
  `mwApplyLang` pattern reaches, extended through the `byId` map where it
  does not (the auth button + install-state re-syncs). Proper names never
  translate. Icons never translate. The language picker stays the one
  picker. DONE.
- **Exact measurement:** inventory counted before (36 static labels
  unmarked + 14 JS-written strings) and after (zero English labels left
  in es/fr/de except proper names); grep count of unmarked Settings-panel
  labels = 0; zero overflow at 390/1440/360; zero console errors
  (non-Supabase). DONE.
- **Design-contract gate (a)–(i):** (a) no new backgrounds — words only;
  (b) no new elements — the rows keep their elevation (the auth h3 span
  and slot syncs add no elements); (c) counts alive — 210 keys, pill
  untouched; (d) no text-in-image — no new images; (e) no bare text
  blocks — the panel rows are boards with icons and labels, as built;
  (f) no look-alike — the dictionary IS the page's own `MW_I18N`, the
  mechanism IS the round's own; (g) `##` format — this record; (h) no
  dictation-blunt phrases — no new public copy invented, only the page's
  own words in three languages; (i) not applicable to a settings panel.
  Human checks H1–H5: H1 stranger test — a Spanish speaker opens Settings
  and reads it (screenshots); H2 perfect-words — every new value
  hand-reviewed, the machine's errors corrected in §3; H3 face quality —
  the panel's icons unchanged, the ⓘ button survives; H4 test in his head
  — a citizen in any country opens Settings and reads it; H5 one ultimate
  ten — the panel speaks the language it offers.

## §7 — Staging + filing

- **Staged link:** https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/personal-page-complete-20261113/personal-complete.html&ref=personal/auto-translate-settings-fix-20261113&cb=<FINAL COMMIT SHA — see the maker's final report>
- **Filing:** branch `personal/auto-translate-settings-fix-20261113`, ONE
  commit, parent `f9242820df009ce0270b2e4ad93cd5cbe98a170c`, via the round's
  `gh-direct.py` path (one API write at a time; blobs via process
  substitution, never staged to disk). Contents: the built page + the
  amended main record + this fix record + fix scorecard + updated build
  script, language block and dictionary + fix verify scripts, JSONs and
  the three 390 screenshots. (Staged bytes re-verified byte-identical
  under the final cb by curl before handoff — see the maker's final
  report for the final link.)

## §8 — Three self-checks (each found NEW things)

1. **The build itself** — pipeline reproduced the tip byte-identically
   before extension; diff vs tip confined to 22 blocks, all in the panel
   and its three JS writers. NEW findings: the `loadSettingsData`
   overwrite (marking alone could never close the id-line);
   `renderInstallState` overwriting the install state on every open; the
   decorator's ⓘ button inside the h3 (marker-on-h3 reads "Accountⓘ" and
   would wipe the button); the `data-mw-en` capture trap for JS-created
   marked elements; the cover-slot placeholders, visible only to the eye.
2. **The browser + curl proof** — new evidence at every language and
   width: the marked lower half DID translate on the tip (the mechanism
   was never broken); the auth card translates on switch AND at first
   visit; the slots translate without re-rendering (no typed text lost).
   NEW findings: the machine draft's error modes (§3); the de install
   line's Sie voice; the autofold sub's quoted trio names, left as the
   round reviewed them.
3. **The proof itself** — re-read the diff, re-ran the samples, confirmed
   the base did not move mid-round (parent `f9242820` unmoved; base sha
   `4872414a…` asserted at all three rebuilds). NEW findings: the
   screenshot eye check caught what the text dump could not (the
   placeholders); the zero-English audit needed the French-identical
   allowlist ("Notes", "Notifications") to avoid false failures.

## §9 — Seven pre-merge answers (in writing)

1. **Three self-checks done?** Yes — §8, each finding new things.
2. **Honest 9+?** Score 10 — see
   `SCORECARD-AUTO-TRANSLATE-SETTINGS-FIX-20261113.md`. Deduction: none.
   The panel is whole in es/fr/de; the only English left is proper names
   and the round's own quoted trio names.
3. **Blast radius named?** Staged Personal page only, on a new branch
   from the auto-translate tip. The Hub shell, the walk worker and live
   are untouched. No main change. No mail.
4. **Checks green?** Settings proof + regression + note Translate tap,
   all green on the final file; every exception named (transient
   setStatus feedback, the two conditional status notes, the signed-in
   auth button, the `confirm('Sign out?')` modal).
5. **Five gates?** Yes, with evidence (§0).
6. **Real proof?** Live bytes, shas, line numbers, counts, browser
   measurements and screenshots, all read first-hand in this round
   (§1–§5, §7).
7. **No silent known defects?** None silent — every gap and
   not-yet-translated string is named in this record (§2).

## §10 — Follow-ons (named, not silent)

- **Transient feedback strings:** the six `setStatus` messages and the
  two cover-area status notes stay English — a follow-on if the captain
  wants feedback translated too (composed sentences with interpolation,
  a sub-system, not labels).
- **More chrome languages:** data-only follow-on (one dictionary object +
  one select option per language, no code change) — the dictionary is now
  210 keys/language.
- **The round's named gaps stand:** drawer links, the unexercised chat
  tap, the 6-second fail view — untouched by this fix, as the brief
  orders.
