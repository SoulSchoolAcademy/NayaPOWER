# CAPTAIN DOUBLE-CHECK — AUTO-TRANSLATE SETTINGS-PANEL FIX (Area #41, 2026-11-13)
## Captain: Naya Nitro Narzan · Verdict: PASS 10/10 — the fix round's bullseye is met

**One line:** The Settings panel now speaks Spanish, French and German like the rest of the chrome — every label changes, nothing left in English except proper names. The gap I sent back is closed, proven three ways plus my own eye.

## What I verified first-hand

- **Staged == maker == checker.** My own curl of the staged link: 1,639,171 B, sha256 `d91945f6b883dff7311c320802b62ab7d0ac0fffa756a48c36e867f6fc44f3e4`. Branch tip via ls-remote: `3d8f9651e54fd90ea92d640dbbe93323e448b529`, one commit, parent `f9242820` (the auto-translate tip). Both exactly as claimed.
- **Checker verdict read in full.** Independent and thorough — the checker opened the panel themselves in es/fr/de at 390 and 1440, read their own screenshots, re-ran the grep (row `<b>` 0/20, subs 0/20, `h3` 0/10), confirmed staged == local == filed, confirmed the tip, confirmed the first-maker credit line in the main record by name (Wrena). I accept every finding. The checker's lesson from last round — open the panel — was applied.
- **Cloud-browser eye check (task 45750c38, 19:14–19:16Z).** Page loads clean, pill "✦ 75 pts". The page loaded already in Spanish (persisted choice); the browser toggled to English and back — both switches re-rendered the whole page including the panel. Panel in Spanish, read with its eyes: "Tus preferencias", "Comportamiento de la app", "Identidad", "Todo en esta página", "Idioma para esta página", "Ajustes comunes — todas las páginas", "Botones de la portada — tus membresías", "Notificaciones de esta página", "Plegado automático de la barra inferior", "Mi mundo - qué páginas aparecen", "Audio - La voz de Naya", "Umbral de coincidencia % — Conexiones", "Instala esta app". Note translation still works end to end: picker asks "¿En qué idioma está esta nota?", label "🌐 TRADUCIDO DEL INGLÉS", "Mostrar original" brings the original back.
- **Must-NOTs re-confirmed:** no live touch, no merge, no PR, main untouched at `aca7b075`; drawer links, chat tap and fail view untouched; no new vendor/key/framework/picker.

## Cleared, not defects (adjudicated with evidence)

- **"Home" / "Dashboard" / "Ir al Home Hub" / the "(Mail · Activity · Space)" trio staying English in the panel** — proper names and the round's own reviewed value, as the checker names in §2. The brief says proper names never translate; page names are proper names.
- **Gear button "Settings" and avatar "Change picture"** — the gear is icon-only (⚙️) and the avatar button shows 📷 only; the words exist solely in aria-labels, not visible text. Both strings ARE in the dictionary. Not visible defects.
- **"newest-first" → "los colores más recientes"** — the same machine-translation quibble as last round: labelled, original one tap away. Not a defect.
- **Gear second click still does not close the panel** — confirmed by the checker by observation, explicitly out of this fix's scope; the corrections round owns panel dismissal. The browser also notes Escape does not dismiss the panel (same family, same owner).

## Score: 10/10

The bullseye was one thing — the Settings panel speaks es/fr/de like the rest of the chrome — and it is true by my own measurement. No deduction is available on this round's scope. Maker 10/10 agreed; checker PASS agreed.

## BUT — one more surface, found by the same eye (follow-on, not a fail of this round)

The cloud browser's eye caught visible English chrome **outside** the panel, on every note card in Spanish mode: the Intelligent Block's fixed labels — "IN A NUTSHELL", "＋ CREATE SPACE", "★ FAVORITE", "ADD TO THE INTELLIGENCE", "ADD INTEL", "ONE INTELLIGENCE · MANY VIEWS · ONE IDENTITY", "TRUST: SOURCE / INTERPRETATION SEPARATED". I confirmed them in the staged bytes first-hand: they are visible template strings (`<p class="ph-nutshell">IN A NUTSHELL</p>`, `<span class="ib-nutshell-label">IN A NUTSHELL</span>`, `btn('ADD INTEL', …)`, etc.), unmarked, and "IN A NUTSHELL" is not in `MW_I18N`. The brief's Part 1 promised "every label on the page" and the inventory's scope line names "feed cards" — these are the page's own words, not the citizen's, and not proper names. This is the same miss class as the Settings panel, found the same way.

**Call:** the fix round passes — its bullseye is met. The auto-translate project as a whole is NOT shown to Shawn yet, because the whole-page rule says a project comes to him whole: a Spanish page with English headings on every note card is not whole. One more small fix round, same shape as the Settings fix (dictionary + marking for the card's fixed labels), then the captain re-checks and the whole page goes to his eye.

**Fix brief: `BRIEF-AUTO-TRANSLATE-CARD-LABELS-FIX-20261113.md`.**
