# CAPTAIN DOUBLE-CHECK — AUTO-TRANSLATE (Area #41, 2026-11-13)
## Captain: Naya Nitro Narzan · Verdict: 8 / 10 — BACK IN, not shown to Shawn

**One line:** The feed, the tabs, the rail and the note translation all work — but the Settings panel, which the brief names explicitly as part of "the whole chrome", still reads English after switching to Spanish. That is a brief-named gap in Part 1, so the round goes back for one fix pass, not to Shawn.

## What I verified first-hand

- **Staged == maker == checker.** My own curl of the staged link: 1,621,175 B, sha256 `28ca21fa376ddaeb7a8a51f935407e7465bff68fd79d3d99b03958b83c8e4403`. Branch tip via ls-remote: `f9242820df009ce0270b2e4ad93cd5cbe98a170c`. Both exactly as claimed. The interim commit `5bd5b35f7` is gone from the tip.
- **Checker verdict read in full.** Thorough, honest, PASS for what it probed: six translation directions real and labelled, switch + persistence + first-visit default green at 390/1440/360, five-step no-words flow at 390 and 1440, both in-round fixes re-proved, pill "0" confirmed not a regression. I accept every one of those findings.
- **Cloud-browser eye check (task 278af2e1, 18:24–18:26Z).** Page loads clean; pill settles to "✦ 75 pts" in a live session. Spanish switch works on the menu, tabs and bottom bar ("Your reports" → "Tus informes", "Leaderboards" → "Clasificaciones", bottom bar AÑADIR / CORREO / ACTIVIDAD / ESPACIOS / ECOSISTEMA). Note translation works end to end: picker asks "¿En qué idioma está esta nota?", label "🌐 TRADUCIDO DEL INGLÉS" appears, "Mostrar original" brings the original back.
- **The gap, seen with the browser's eyes and confirmed in the bytes.** After switching to Spanish, the Settings panel stays English: the "⚙️ Your Preferences" heading, the "Notifications" heading, and the rows "Deep black", "Smart Tabs drift" (and its sub), plus other Settings labels. My byte check on the staged file: those headings/rows carry no `data-mw-tr` marker. Of 22 `os-setrow-main` blocks, only 2 have a `data-mw-tr` nearby. The row labels present in the file are: Deep black, Notifications, Smart Tabs drift, Motion & glow, Auto-refresh, Public profile.
- **The brief names this exact surface.** Brief § "Done first — defined before the work": the exact element is the page's chrome "(the eight row buttons, the three feed tabs, the bottom bar, the + menu, **the Settings rows**, the guide steps, the composer, the side rail)". The exact change: "every label on the page carries a translation in Spanish, French and German". Part 1: "every label on the page (row buttons, feed tabs, bottom-bar labels, + menu items, **Settings rows**, guide steps, composer labels, rail headings and buttons, the points pill's words)". The inventory's own scope line names Settings rows IN scope. The Settings panel is not a follow-on; it is Part 1, unbuilt.
- **Why the checker missed it.** The checker's probe set covered tabs, rail, + menu, bottom bar and the Lists room — all green — but never opened the Settings panel after switching language. The PASS is real for what it checked; it is incomplete against the brief's "every label" standard. This is a checker-scope lesson, not a checker failure of honesty: the probe list must cover every surface the brief names.

## What is NOT a defect (checked, cleared)

- **The welcome sentence staying English is correct.** It is the citizen's own words (content, like a note) — the inventory names the owner's tagline out of scope for the chrome dictionary, and Part 2 is the route for translating it.
- **"✦ Personal / ✦ Business / ✦ Space" staying English is correct.** World names are proper names; the brief says proper names never translate.
- **Pill "0" / "…" on a fresh load is not a regression.** The checker proved the base reads "…" in the identical environment; the cloud browser's live session settles to 75. Timing + live fetch, nothing more.
- **"newest-first" → "los colores más recientes" is a machine-translation quibble**, labelled, original one tap away. Not a defect.
- **Settings gear second click not closing the panel** — noted by the browser, but the round did not touch the gear's behaviour and I have not compared it against the base. Treated as an unproven quirk for the corrections round, not a fix-round item. "System Theme" / "Keyboard shortcut" as quoted by the browser have zero occurrences in the staged file — not grounded, not a fix item.

## Score: 8 / 10

- The maker's 9/10 (drawer links + chat tap) stands as far as it goes.
- **−1: the Settings rows — a brief-named Part 1 surface — are untranslated.** One point, because the fix is small and the mechanism is proven: it is dictionary data + marking for one panel, not a new design.
- The drawer-links gap, the unexercised chat tap, the 6-second fail view and the other named gaps stand as recorded; none is newly scored here.

## What goes back in (one fix pass)

**Fix brief: `BRIEF-AUTO-TRANSLATE-SETTINGS-FIX-20261113.md`.** Inventory the Settings panel first-hand (headings, every row label + sub, the language picker labels themselves), add every label to `MW_I18N` in es/fr/de, mark and apply them, and prove it by eye + bytes: switch to es/fr/de, open the Settings panel, and show every label changed; grep the staged bytes for unmarked Settings labels (zero left). The fix maker also adds the credit line owed to the first maker (see below). Checker re-probes the Settings panel only, plus a regression pass on the switch. Then the captain re-checks.

## Record correction owed

Credit owed to the **first maker** (16:45–17:26Z, died on a transport failure, not a task failure), by name in the record: her dictionary preserve-step regex fix (DE values leaking into es/fr) and the Unicode-aware icon regex (`\p{L}` not `\w`, line 20436) are real, in the build, and verified first-hand by the second maker. The record credits her dictionary work generally but not these two fixes by name. The fix round adds that line.

## Must-NOTs (re-confirmed)

No live touch, no merge, no PR. The corrections round stays held behind this fix landing. The Hub toggle stays a dead switch, untouched.
