# PROOF — AUTO-TRANSLATE (Area #41, 2026-11-13)
## Fresh maker (second maker) · Captain: Naya Nitro Narzan

Built file: `TEAM-NITRO/personal-page-complete-20261113/personal-complete.html`
— 1,621,175 B, sha256 `28ca21fa376ddaeb7a8a51f935407e7465bff68fd79d3d99b03958b83c8e4403`.
Base: 1,555,404 B, sha256 `4872414a1d428a940a4e12ac31c419f999843a2fde072a9ac91d09b42051c666`.
All evidence files live in `team-nitro/auto-translate-20261113/` (work dir)
and are filed under `TEAM-NITRO/auto-translate-20261113/` in the repo.

## §1 Step 0 — the machine is live

- Bindings: `cf-worker.py get-bindings b5e2a51b3e883f7722287c5f51b1196b
  naya-auto-translate-staging` → HTTP 200,
  `[{"name":"AI","project":"<catalog>","type":"ai"}]`.
- Live test: `POST .../translate {"segments":["El sol sale sobre la
  ciudad."],"source_lang":"es","target_lang":"en"}` → HTTP 200,
  `"The sun rises over the city."`
- Worker read-back: HTTP 200, 3,521 B envelope; local source 3,337 B, sha
  `32b5647d…`; envelope contains `env.AI.run` + `m2m100`.

## §2 Part 1 — language proof

| File | Width | Page errors | Console (all Supabase) | Overflow 0 / scrolled |
|---|---|---|---|---|
| `verify-a-390.json` | 390 | [] | 60 | 390/390 · 390/390 |
| `verify-a-1440.json` | 1440 | [] | 42 | 1440/1440 · 1440/1440 |
| `verify-a-360.json` | 360 | [] | 56 | 360/360 · 360/360 |

Switches (all widths): es "✉️ Mensaje / ⭐ Habilidades / 🌍 Feed
inteligente público"; fr "✉️ Message / ⭐ Compétences / 🌍 Fil
intelligent public"; de "✉️ Nachricht / ⭐ Fähigkeiten / 🌍 Öffentlicher
Smart-Feed". Persistence across reload: `stored: "de"`. First visit:
es-ES → es, ja-JP → en. Green set: tabs `✦ Personal / 🌍 Public smart
feed / ✦ Naya Notes`, rail 20 cards, + menu 5 items, segs
`plus/mail/activity/spaces/eco`, wallCards 1 (empty-state), pill "0"
(`file://` fetch stop — see RECORD §4). Screenshots:
`proof-{390,1440,360}-{es,de}-chrome.png`.

## §3 Part 2 — translation proof

`verify-b2-390.json` (`verify2.py`, 390). Page errors []; console 54,
all Supabase; overflow 390/390.

- es→en (3 sentences): label "🌐 Translated from Spanish"; nutshell
  "The sun rises over the city and everything is filled with light. We
  walked through the market together, tasting the bread and talking
  about the future. Life is better when it is shared." — 3/3 sentences.
- fr→en: "🌐 Translated from French" — "The morning is quiet and the
  city is slowly waking up. We drank coffee and watched the river pass."
- de→en: "🌐 Translated from German" — "The evening is quiet and the
  lights of the city are reflected in the river. We go home slowly and
  think about tomorrow."
- en→es / en→fr / en→de: "🌐 Traducido del inglés" / "🌐 Traduit de
  l'anglais" / "🌐 Übersetzt aus dem Englischen" — garden note whole in
  each language.
- Original one tap away: "Show original" → collapsed, button reads "Show
  translation", original nutshell intact; "Show translation" → view
  returns with its label.
- Naya attach: synthetic faithful `.ph-card` in `#mwFeedNaya` got its
  Translate button (`naya_tr_btns: 1`).
- Honest failure: `failure_seen: true` — "Translation unavailable — the
  original is here", no invented view, page errors [].
- Screenshots: `proof-390-translated-es.png`, `proof-390-failure.png`.

### Repaint resilience

- `verify-repaint-390.json`: natural post-load repaint at 9,914 ms after
  the stub; es→en view mounted on the live node at +12.5 s, no gaps after
  first sighting (50 polls).
- `verify-repaint2-390.json`: forced repaint while the picker was open →
  picker re-appeared (`picker_after_forced_repaint: true`); translation
  completed; second forced repaint → finished view survived
  byte-identical. Page errors [].
- Screenshots: `proof-390-repaint-view.png`,
  `proof-390-repaint-picker.png`, `proof-390-repaint-view2.png`.

## §4 Part 3 — no-words proof

`verify-nowords-390.json`, `verify-nowords-1440.json` (`verify3.py`).
Page errors []; console 42/42, all Supabase; overflow 0 at both widths.
Hiding: all text transparent except `.os-jewel`, `.fc-pi-ico`,
`#naya-notif-bar`; emoji stay visible; layout untouched.

| Step | 390 | 1440 |
|---|---|---|
| 1 ENTER | cover 390×420, 8 hero buttons 110×46, pill visible | cover 1440×464, hero buttons 147×49, pill visible |
| 2 FIND YOUR WORLD | `spaces` seg (232,786,50×48) → drawer; worlds (14,103/160/217,272×49), jewels 23×23: Personal `#3fb8ff`, Business `#2fe89e`, Space `#ffbf3d` | `spaces` seg (787,778,66×56); same rows + jewels |
| 3 READ THE FEED | Public tab (138,384,114×75), 🌍 `#3fb8ff` → selected | Public tab (379,396,343×51), 🌍 |
| 4 MAKE A POST | `plus` seg (46,786) → 5 items ✎/✎/✦/💬/✉️; item 0 → composer 302×89 | `plus` seg (487,778); composer 660×89 |
| 5 TALK TO SOMEONE | rail card (16,331,356×181); Chat (29,464,78×35) → `#fcChat` 358×339 | rail card (1096,332,318×181); Chat (1109,465) → chat 380×339 |

Screenshots: `proof-{390,1440}-nowords-{1-enter,2-worlds,3-feed,4-plusmenu,4-composer,5-talk}.png`.

## §5 Lists room (no-regression)

Clicking the Lists entry opens `#lists.ph-sec.os-view.on` ("📋 Smart
Lists") with input + Add button; page errors []. Probe `/tmp/pw-lists.py`.

## §6 Staged verification

Staged link: https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/personal-page-complete-20261113/personal-complete.html&ref=personal/auto-translate-20261113&cb=eeb5db00814b8bd3d12f16edc25b8ecf7e4ab791

- **Bytes:** curl → HTTP 200, 1,621,175 B, sha256
  `28ca21fa376ddaeb7a8a51f935407e7465bff68fd79d3d99b03958b83c8e4403` —
  BYTE-IDENTICAL to local. Markers: `mw-translate` 2,
  `os-jewel os-jewel-sm` 32.
- **Run** (`verify-staged.py` → `verify-staged.json`, 390, served
  bytes): page errors []; console 60, all Supabase; overflow 0 at scroll
  0 AND scrolled; green set — tabs `✦ Personal / 🌍 Public smart feed /
  ✦ Naya Notes`, rail 20, + menu 5, wall empty-state, pill "0" (base pill
  is also "0" in the identical environment — not a regression); language
  switch on staged bytes — es `msgbtn` "✉️ Mensaje", `tabPublic`
  "🌍 Feed inteligente público"; live translation tap on staged bytes —
  Spanish stub → "🌐 Translated from Spanish / The sun rises over the
  city and everything is filled with light. We walked through the market
  together." with "Show original".
- Screenshot: `proof-staged-390-translated.png`.
- The final filing's commit sha differs from the staged run's cb (the
  record was completed after staging); the page blob is unchanged and the
  staged bytes were re-verified byte-identical under the final cb by curl
  before handoff — see the maker's final report for the final link.
