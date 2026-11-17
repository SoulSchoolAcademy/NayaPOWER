# INSPECTOR SWEEP #2 — Logic, Elegance, Size, Purpose
## 2026-11-17 · Inspector seat #2 · Standing sweep

**Charge (Shawn's words, 2026-11-17 03:35Z, governing):** go through ALL the pages and judge LOGIC, ELEGANCE, DESIGN, USEFULNESS, and high-level design quality — where things sit, how they fit, how they look, what they do. Name everything oversized and everything undersized, with the size it should be. Polish, fine-tune, rearrange, resize. Lock into the heart of what we're doing. PURPOSE TEST: every page must answer at a glance — what is this, what's its purpose, what do I do here. A page that leaves him asking "what is this" FAILS, whatever else it does right.

**This is a different lens from Sweep #1** (dispatched 03:04Z, language audit — its report is being verified; not redone here). Where a break is purely a language-law break already covered by Sweep #1, it is cited once as e.g. "(Sweep #1 B1)" and the lens moves on. My lens is the stranger's eye: read top to bottom, what does the page say it is, what does it ask me to do, what is too big, what is too small.

**New words that landed DURING this sweep (used as law here, not as afterthoughts):**
- **03:43Z — ONE BOTTOM BAR, THE FIVE, EVERYWHERE:** the Personal five (+ ADD purple · MAIL blue · ACTIVITY green · WORLDS gold · ECOSYSTEM purple) are the official bottom bar on EVERY page, same five, same colors, one bar. Every page having its own version is the mess. (CONNECT as a sixth on the Hub is his call — flagged, not decided.)
- **03:43Z — ALIVE LIKE A HIGH-TECH COMPUTER, NOT A VIDEO GAME:** aliveness is good, but the feel must read high-tech computer alive — intelligent, elegant, system alive — not arcade alive. Less text, more icons. Pages drift from each other; the inspector scores the drift; the Factory is the one language.
- **03:43Z — BEST OF BOTH, ONE SMART MAIL:** two Smart Mail presentations exist; make ONE, best of the best. Named items: F and D saved-list letters carry different colors of the same color — align to the one set exactly; the cover / no-cover / full-screen control is not understood — make it plain or remove it; flat buttons get real depth.
- **03:47Z — TODAY LIGHTS UP WAY MORE / THE WEEKDAY IS A ROYAL OBJECT / THE EYE, BALANCED:** on the calendar you must tell what day it is at a glance — today lights up WAY more than the rest, unmistakable. The weekday name is a real object in royalty, never plain text on black. The eye is too big, too much white, unbalanced — shrink it, balance it, less white; a jewel, not a white blob. The bar: clean, beautiful, elegant, easy to operate, high-tech — never low-end, cheap, elementary. His verdict on the vision day view (Monday 16): "it just looks like a mess… low end cheap, elementary tech."

**Method.** Filed bytes via the git blob API with FULL 40-char SHAs; served bytes via curl (browser UA) with sha256 verification. No live VM browser exists in this seat and no browser tasks can be launched from here, so nothing below is claimed as a live-eye check — EXCEPT the Ultimate Calendar artifact, judged from its own audit's real rendered captures (desktop + mobile, 03:40:45Z), marked EYE (capture). Everything else is byte-proven or marked UNPROVEN-BY-RENDER. Word/button/font counts are literal occurrences in the bytes I read. CSS source order is never treated as visual order.

**Branches moved while I worked.** Hub icons-fix tip moved 03:38Z to 6ce5b2af (Fix-5 landed — I judged the tasked Fix-4 blob fd802b03; Fix-5 is unjudged, noted). Smart Mail tip is 94ec9327 (Fix-3 round 2, checker PASS — I judged the tasked blob 3935e962 from commit 48d72031; see Mail note). Calendar tip moved to 03700ad1 (blob 50bfdadd, 78,881 B — I judged that tip). Walk tip is 12890208 (Fix 3). Dashboard Fix-3 and Hub Fix-5 and Mail Fix-3 round 2 are in-flight/landed-during-sweep and are NOT in these scores.

**Live drift found during the sweep:** the live Hub is NO LONGER the brief's bytes — served 2026-11-17 ~04:0xZ it is 4,830,033 B, sha256 bb380404, vs the brief's 4,678,679 B / bfbd895a (redeployed 22:25Z Nov 16). Live Dashboard (1,817,928 B, bb41114d) and live Pricing v77 (11,355,594 B, b043167b) still match the brief. The Hub live drift is unrecorded anywhere I could find — re-record it.

---

## SCORECARDS (0–10, vs logic / elegance / size / purpose)

| Page | Score | Purpose test | Why it is not 10 (nutshell) |
|---|---|---|---|
| Walk / entrance — staged | **4** | FAIL | The door exists but the 86-beat legal letter buries it: 8,650 words, 117 buttons, 277 images. First screen reads as a contract, not an entrance. |
| Dashboard — staged Fix-2 | **5** | FAIL | H1 is "Good morning." — a greeting, not a purpose. First visible text is a nav wall (282 buttons). Three giant numbers fight (168 / 96 / 88px). |
| Personal — facelift tip | **4** | FAIL | No h1 at all; title is a person's name; first visible text is a composer dialog. 407 buttons, 47 inputs, 5,068 words, 201 emoji. |
| Hub — staged Fix-4 | **5** | FAIL | Static first paint is "NayaNET needs JavaScript"; live title still says "Intel Today"; the h1 is a slogan ("This is the new internet."). |
| Pricing — staged v78 | **6** | FAIL at a glance | Opens with the founder's letter ("GET IN THE BUGATTI") — 5,358 words before the chart that is supposed to BE the page. 0 h1. |
| Pricing — /free | **7** | PASS | Clearest purpose in the network ("Enter free — no payment, no card. Claim your Smart Name."). Held back by 0 h1, a dangling "Certificate Nº ·", and an Install-App prompt competing with the ENTER button. |
| Pricing — /free/walk | **5** | PASS, hierarchy FAIL | The ten questions ARE the purpose and read clearly — but 20 h1s (one per slide) means no hierarchy at all, and 136 buttons. |
| Smart Mail — blob 3935e962 | **7** | PASS | Best purpose sentence in the network after the calendar ("Message anybody — by topic, not just by contact"). Held back by the cover control nobody understands, a colored-wash cover, and two jobs (mail + messenger install) on one page. |
| Calendar — obsidian rebuild tip 03700ad1 | **6** | PASS month / FAIL day view | Month view is strong (full Marcellus names, pearl "i" eye, digits shrunk, 13 doors with glimpses). Today does not light up WAY more, the weekday names are colored plain text (not royal objects), the eye is still a big white disc, and the day view is the one Shawn called "a mess". |
| Calendar — vision artifact `the-ultimate-calendar` (EYE, 03:40Z audit) | **5** | PASS as calendar / FAIL as day-planner | Full names + pearl "i" landed — but TWO trailing rows of empty cells are still there, every cell is an empty black void, mobile cells are tall vertical rectangles, two-digit dates are two-color confetti, Marcellus failed to load in the audit. |
| Formats — unfold 34c756ff | **6** | PASS | "Press the button, go to the next experience" is perfectly clear — but the 240px N disc (see suspect) sits on every beat and is bigger than the idea it introduces. |
| Formats — slideshow 21d08a88 | **6** | PASS | Same as unfold, sideways. Same N disc, same cages. |
| Intelligent Block Epic — staged | **5** | CONDITIONAL PASS | "Paste anything. It comes out beautiful." is clear — but the page's own right to exist standalone is questioned by Shawn's 03:35Z word (the Factory is the formatter), it has 0 h1, and the 240px N disc repeats on every beat. |

---

## 1. WALK / ENTRANCE — staged (score 4, purpose FAIL)

**Judged:** worker root, 938,546 B, sha256 e27c7fe1 (matches blob 11cfc233cdadff396846ce5325f76cc98d81a013, branch walk-end/entrance-welcome-20261116 tip 12890208, Fix 3). Live root is behind staged (Sweep #1: live 620,595 B, sha 0c8628d5) — cited once, not re-judged.

**Read as a stranger, top to bottom.** Topbar (62px): brandmark (logo + NAYA) + a 9-dot nav. First words: "Naya / Naya Welcomes You / Enter NayaNET → / Jump back in → / New user? Create a new account — click here". Then: "Read the collective agreement ◆", "Skip the agreement →", and the page becomes THE COLLECTIVE AGREEMENT — h1 "The Royal Unfolding", h1 "The Collective Agreement", 86 beats, "Nine pictures. One beautiful story." The entrance IS a door — but the door is a doormat in front of a legal letter, and the letter is the page.

- **Logic:** the agreement-first order is the design (trust before entry), but the page never tells the stranger the deal in one line — "what do I have to do to get in?" has three answers (Enter, Jump back in, Create) plus "Skip the agreement" plus "read the whole letter at once". Four ways in, one of them a skip. A stranger cannot tell which is the real door. The portal itself (.portal 459px square, .enter button 48px high) is a good size — the door is right, the hallway is wrong.
- **Elegance:** the front entrance is the standard Shawn holds the calendar to — and on its own terms it is the most finished surface in the network. But 277 `<img>` tags (most of them base64 brandmark/beat images) in a 938 KB file is heavy furniture for a front door.
- **Sizing — oversized:** the agreement letter, 8,650 visible words. A front door should say the deal in ~150 words and let the letter live one click away. The deal-seal (120px circle, 54px N) is proportionate — NOT the suspect. **Undersized:** the actual choice — "Enter NayaNET →" is a text link, not the 48px portal button; the most important action on the page is the smallest one on the first screen.
- **Usefulness:** "Jump back in" for returning citizens is genuinely useful and visible. "Also on this device:" is a nice touch. But nothing on the first screen says what NayaNET is in one sentence — the h2 "NayaNET is a world of connected intelligence" is beat 2, below the fold of the letter.
- **Purpose test: FAIL.** At a glance the page asks "will you read this contract?" — not "come in, this is your world." The door is there; the letter buries it.

**Breaks:**
- W1 — First screen, whole page: letter-first buries the door. Fix: door first (Enter / Create as the two big portal buttons, one sentence saying what NayaNET is), the agreement one click away — the letter is a room, not the hallway.
- W2 — 8,650 words / 117 buttons / 277 images on an entrance. Fix: cut the staged page to the door + the deal in ~150 words; the 86 beats live behind "Read the agreement".
- W3 — Three doors + a skip (Enter / Jump back in / Create / Skip). Fix: ONE door for new (Create), ONE for returning (Jump back in) — Enter and Create are the same action wearing two labels.
- W4 — "Enter NayaNET →" as a text link while the 48px portal button sits elsewhere. Fix: make the first-screen Enter the portal button itself, 48px+, full width on phone.

## 2. DASHBOARD — staged Fix-2 (score 5, purpose FAIL)

**Judged:** blob 3244de682944c6a6df8168fd1a06e2ae074bf19c, 1,943,088 B, sha256 e4e098be (commit fbea205c, PR #3387 open). Live (1,817,928 B, bb41114d) is the same family — the staged tip is +2,378 B of hero-name repair. Fix-3 is running — not judged.

**Read as a stranger, top to bottom.** Title "Smart Score Dashboard — NayaNET". First visible text: "✕ ← Back to board ⚙ ☰ Show navigation NAYANET AREAS Start Here Smart Feed Smart Factory Ask Naya Smart Spaces Today's Intel Smart Growth Your Reports Intelligent Library Smart Ledger Your Connections Smart Lists Smart Mail Settings NAYANET ECOSYSTEM ⌂ HOME ↗ 👥 ABOUT US ↗ 💼 YOUR HIRED ↗ 📄 WHITE PAPER ↗ 🎓 NAYA ACADEMY ↗ 🏆 "5" DAY CHALLENGE ↗ ⭐ AI MASTERCLASS ↗ ❤ LIFE WITH NAYA ↗ …" — a navigation dump, then the hero: a 72px orb with a 28px "N" beside "Good morning, Shawn." and a wisdom quote, then the score: 168px digits in 150px tiles. Then Reports, Smart Links, running feed, network stats, rooms, motto, story, Q&A. The page is a whole world — but it opens with its own index.

- **Logic:** the hero greets from the page's own profile name (Fix-2, checker-verified) — good. The ledger-sync line ("Ledger syncing…", `#os-dd-ledger`) is present — good. Reports are present (53 "Reports" occurrences). But the score, the points, and the leaderboard score are three different giant numbers with no sentence anywhere saying how they relate: is the 168px number my score, my money, or my points? A stranger cannot tell. The score IS the page — and the page never says so.
- **Elegance:** the digit tiles are real objects and are canonical — not counted against it (Sweep #1 T1). But three massive numbers on one page is not elegant, it is shouting in three voices: `#os-se-num` 168px (108px ≤768px) in 150px tiles; `.os-detail-points` 96px; `.os-ld-score b` 88px; plus an 84px stat number in the JS detail view. Pick ONE hero number.
- **Sizing — oversized:** the score digits, 168px / 150px tiles — a 3-digit score is 450px+ of tile before gaps (18px between reels). Should be ~120px digits in ~110px tiles: still the biggest thing on the page, no longer the only thing. The detail-points 96px and leaderboard 88px numbers should be ~48px and ~40px — supporting numbers, not rival heroes. The hero orb (72px, 48px on phone, rings to −20px = 112px footprint) with its 28px N is proportionate — NOT the suspect, and its rings spin at the correct 120s/180s. **Undersized:** the one-line answer to "what do I do here" — there is no such line at any size. The smallest text on the page (11px `.os-dd-wk` kicker, 9.5px gauge labels — Sweep #1 B5) carries the structure; the biggest text carries a greeting.
- **Usefulness:** Reports + ledger sync + running feed + Smart Links is the whole Dashboard promise, and it is all here. But 282 buttons and 21 inputs mean the page asks the stranger to operate a cockpit before it has said what the flight is.
- **Purpose test: FAIL.** "Good morning." is a greeting, not a purpose. At a glance: a nav list, a greeting, a huge number. What is this? A scoreboard that never says "this is your score."

**Breaks:**
- D1 — H1 "Good morning." + nav dump first. Fix: first screen = one line ("Your score, your world, your money — here's where you stand.") + the score + the ONE next action.
- D2 — Three rival giant numbers (168 / 96 / 88px). Fix: score 120px, detail 48px, leaderboard 40px.
- D3 — 282 buttons, 21 inputs, 149 emoji before the page has introduced itself. Fix: the Dashboard's first screen carries at most the score, the Reports button, and the next action — the rest is below, in sections a stranger can name.
- D4 — No sentence anywhere relates score / points / leaderboard. Fix: one line under the score saying what it is and what moves it.

## 3. PERSONAL — facelift tip (score 4, purpose FAIL)

**Judged:** blob ba628de3c9bb130eda6a0ca1818efde0be78e18a, 3,233,538 B, sha256 69b7235c (commit c7ccbd28, PR #3388 open). Formats tip 925a4340 is the same family (Sweep #1: 1,725 bright / 29 deep — cited once). The facelift itself (stars as jewel tiles, LOVE/LIKE/COMMENT lighting) is checker-PASS and is good jewel-work — it is not what holds the page back.

**Read as a stranger, top to bottom.** Title: "Shawn Vibert" — a person's name, not a page. There is NO h1 in the entire 3.2 MB file. First visible text: "✕ ✦ Naya note ✎ Make a post ✎ Naya note ✦ Smart note — Naya formats your words beautifully. Write it, dictate it with the microphone — Naya writing it for you is coming soon. 🖼 Add a photo Remove photo Preview — how it will look: Schedule Private ✦ Post my Naya note…" — a composer dialog is the first thing on the page, before the page itself. Then: cover, profile, "The course", "All your pages within your world", "Your world, day by day", "Notifications", "Smart notes in this world", "Joined pages & worlds".

- **Logic:** a Personal page that opens with a composer is a page that asks you to speak before it has said whose house you are in. The composer is a tool; the page leads with the tool and hides the world. 407 buttons and 47 inputs in one file — the page is a cockpit with no dashboard. The right rail / drawers / eco bottom bar are all present (the `.eco-bottombar` CSS is defined TWICE in this file, once z-index 350, once z-index 50 — the bar's own code disagrees with itself about where it sits).
- **Elegance:** the facelift stars ARE elegant (46×44px tiles, white at rest, deep gold lit, 0/5 digit tile — checker-verified). But they sit on a page whose top is a modal. Jewels on a page with no front door.
- **Sizing — oversized:** the composer block (a full dialog's worth of copy before any content); the JS detail view's 84px number + 72px jewel (a number bigger than the page's own title, which doesn't exist). **Undersized:** the person's own introduction — "My story", "My motto" are h3s buried below the feed; the profile picture's own scale is lost among 21 images and 201 emoji. The page's most important sentence — "this is my world" — appears nowhere at any size.
- **Usefulness:** everything a Personal page should do is here (post, notes, worlds, notifications, courses, joined pages) — but a stranger cannot find it because the page never says "this is your world, here is what you do here."
- **Purpose test: FAIL.** A stranger sees a name and a "post a note" box. What is this — a profile? a composer? a feed? The page does not answer.

**Breaks:**
- P1 — No h1; title is a name. Fix: h1 "Your world" (or the citizen's world, named) at the top, one line under it: "Post, connect, build — this is your home in NayaNET."
- P2 — Composer dialog is the first visible content. Fix: the composer is a button on the page ("Make a post"), not the page's first screen.
- P3 — 407 buttons / 47 inputs / 5,068 words / 201 emoji. Fix: the Personal page's first screen carries the person, the world, and the composer button — the 400 controls live in their sections, not in the stranger's face.
- P4 — `.eco-bottombar` defined twice (z-index 350 vs 50). Fix: one definition, the Five, per the 03:43Z law.
- P5 — 84px detail number + 72px jewel in a JS detail view vs no title anywhere. Fix: detail numbers 48px; give the page a title first.

## 4. HUB — staged Fix-4 (score 5, purpose FAIL)

**Judged:** blob fd802b03b01b35add806b040017ad376689cf7c8, 4,873,750 B, sha256 340b1326 (commit 959781c7). Fix-5 landed during the sweep (commit 6ce5b2af, 03:38Z) — NOT judged here. Live Hub has ALSO moved since the brief (now 4,830,033 B, bb380404 vs brief's 4,678,679 B / bfbd895a) — unrecorded drift, see header.

**Read as a stranger, top to bottom.** Title: "Smart Feed — NayaNET" — not "Hub". Static first paint (what the bytes show before JS): h1 "NayaNET needs JavaScript" + "NayaNET is a living application — please enable JavaScript to step through." + "Home Make a post Smart note Naya note Home Message Mail Create world". The real h1 lives in a JS template: "' + greet + (who ? ', ' + esc(who) : '') + '.'" and a second h1: "This is the new internet." The Hub — the citizen's eyes and hands, the one place everything connects — introduces itself as a JavaScript error and a slogan.

- **Logic:** a page that is 4.8 MB of JavaScript and shows a "needs JavaScript" h1 to any reader without it is a page that has no front door for a cold stranger — or for a search engine, or for Shawn's eye on a slow connection. The six-segment eco bar (CONNECT as sixth, 46px icons, 20px glyphs) is the bar — but the 03:43Z law says the Five, and whether CONNECT stays is Shawn's call, not the page's. The page carries its own title wrong in two places at once: live says "Intel Today — the daily digest of NayaNET's smart notes" (Sweep #1 B16, still true on the new live bytes — title verified again this sweep), staged says "Smart Feed". Neither says "Hub".
- **Elegance:** Fix-4's palette repair is real (Sweep #1: deep 420 / bright 29 — the best palette repair in the network, cited once). But elegance is not palette alone: the Hub's first screen is an error message.
- **Sizing — oversized:** 4,873,750 B for a feed hub — the largest single page in the network except Pricing. The eco icons at 46px with 20px glyphs are right-sized; the page around them is not. **Undersized:** the Hub's own name — it appears nowhere as a title. The word "Hub" as the page's identity is 0px: absent.
- **Usefulness:** the feed, the rooms, the six-segment bar, the Ask/Get Started actions are all in the code — but usefulness a stranger cannot reach is not usefulness. 33 static buttons vs 282 on the Dashboard: the Hub is quieter than the Dashboard, which is right for a hub — but quiet + "needs JavaScript" reads as empty, not calm.
- **Purpose test: FAIL.** "This is the new internet" is a claim, not a purpose. "Intel Today" is a different product's name. A stranger cannot say what the Hub is for from anything on its first screen.

**Breaks:**
- H1 — Static h1 is "NayaNET needs JavaScript". Fix: server-render the Hub's first screen (greeting + feed top + the Five) so the page exists before JS runs.
- H2 — Title wrong twice (live "Intel Today", staged "Smart Feed"). Fix: title the Hub as the Hub, live and staged, one name.
- H3 — H1 is a slogan ("This is the new internet."). Fix: h1 "Your Hub" + one line: "Everything in your world, in one feed — post, read, connect."
- H4 — Six-segment bar vs the Five (03:43Z). Fix: the Five; CONNECT stays only on Shawn's explicit word — flag it to him, don't decide it in a round.
- H5 — Live bytes drifted (4,830,033 B, bb380404) with no record. Fix: re-record the live Hub sha; nothing live moves without a record.

## 5. PRICING — staged v78 (score 6, purpose FAIL at a glance) · /free (7, PASS) · /free/walk (5, PASS with hierarchy FAIL)

**Judged:** v78 worker 11,360,503 B, sha256 ca2eafeb (matches brief); /free worker 310,212 B, sha256 dfe70a8c; /free/walk worker 3,292,257 B, sha256 2370eae2. Live v77 (11,355,594 B, b043167b) is v78 minus the free-entry groups (Sweep #1, cited once).

**v78 read as a stranger.** Title "Welcome to Naya World — NayaNET". NO h1. First visible text: "An Opening Letter from the founder of NayaNET, welcoming you in ◆ GET IN THE BUGATTI — OR STAY IN THE GOLF CART. The door's open. Welcome to NayaNET. You can keep doing the internet the old way. Another app. Another password. Another inbox…" Then the Top Ten pains, then "Choose your level." (h2), then the three level rectangles + nine-block chooser (Power / Pro / Max × monthly / quarterly / yearly). The pricing page is a sales letter with a chart in it — but the standing law says the chart IS the page, the letter closes it, prices shown once in the chart only. This page leads with the letter and buries the chart.
- **Sizing — oversized:** 5,358 words before a stranger reaches a price; 87 emoji; top font 48px for letter display type while the prices themselves sit in chooser tiles. The letter's display type (48px) is bigger than the prices. **Undersized:** the prices — the one thing a pricing page exists to show — are tiles inside a chooser below a 5,000-word letter.
- **Purpose test: FAIL at a glance.** "Welcome to Naya World" + Bugatti letter: a stranger knows this is a pitch, not what it costs. The price answer takes a scroll; the purpose test is at a glance.

**/free read as a stranger.** Title "NayaNET — Smart Identity Activation". NO h1 (only h2 "Install NayaNET"). 271 words, 7 buttons, 1 input — the lightest page in the network. First visible: "Sovereign Identity — Install App Certificate of Smart Identity … ENTER … Enter free — no payment, no card. Naya Free is the free way in: your Smart Name, your pages, your Hub — zero cost, zero risk. Step up any time in Settings. Claim your Smart Name — yours alone: one person, one route, forever. Your alias is your Smart Link route — alias.nayanet.app — your Smart Mail…"
- **Logic:** the deal is plain and it is the best deal sentence in the network. But two actions compete at the top: "Install App" and "ENTER" — install is not enter, and a stranger cannot tell which one gets them in free. And "Certificate Nº ·" dangles with an empty number — a certificate with no number is a form with a hole in it.
- **Purpose test: PASS.** The clearest purpose statement in the network. It just needs an h1 and one door, not two.

**/free/walk read as a stranger.** Title "The Official Welcome | NayaNET". TWENTY h1s — one per question slide ("Tell me who you are, in your own words", "What are you into, and why?", "What is your vision?" …). 136 buttons, 3 inputs, 1,578 words, top font only 26px. The ten questions ARE the purpose and they read beautifully — but when every slide is an h1, there is no hierarchy: the page shouts every question at the same volume, and the question text (26px max) is smaller than the pricing letter's display type (48px). (Correction to a first impression: the long dev note at the top of the file — "68px, near-black with white triangle…" — is an HTML comment, 1 of 11 in the file; it is NOT visible on screen. It is file hygiene, not a visual break, and it is not scored as one.)
- **Purpose test: PASS (purpose), FAIL (hierarchy).** A stranger knows what to do — answer the questions. But the page has twenty top-level headings and no single title that says "this is your welcome."

**Breaks:**
- PR1 (v78) — Letter leads, chart buried; 0 h1; 5,358 words. Fix: chart first (choose your level above the fold), letter after — the standing law, in that order. Prices at 48px display size; letter display at 30px.
- PR2 (v78) — 87 emoji standing in for icons (Sweep #1 B18, cited once). Fix: object-glyphs.
- PR3 (/free) — Two doors (Install App vs ENTER) + "Certificate Nº ·" with no number + 0 h1. Fix: one door (ENTER), h1 "Enter free", certificate number filled or the "Nº ·" line removed.
- PR4 (/free/walk) — 20 h1s, 136 buttons, question type max 26px. Fix: ONE h1 ("Your welcome — ten questions, your world"), the ten questions as h2s at 32px, one Enter per slide.

## 6. SMART MAIL — blob 3935e962 (score 7, purpose PASS)

**Judged:** blob 3935e96257d08c5d3f123bc8a29c05c0d30fa74a, 92,502 B, sha256 acab5ca1 (commit 48d72031). **Note on the label:** the task calls this the "Fix-2 tip", but commit 48d72031's own message calls it "Smart Mail fix-3 … checker FAIL items 3+5 on fix-2" — this blob already IS the Fix-3 round-1 build, and its cover rule (max-height min(25vh,290px); 140px ≤900px) is the Fix-3 fix. The newer tip is 94ec9327 (Fix-3 round 2, blob e59e09b7, 92,927 B, checker PASS) — landed after my read; scores here are against 3935e962. The unification round (03:43Z) holds for the Fix-3 eye verdict, then builds — so this page is about to be rebuilt once; these breaks are its input, not a second round.

**Read as a stranger, top to bottom.** Title "Smart Mail — NayaNET". H1 "Smart Mail". H2 "Message anybody — by topic, not just by contact". Sub: "Flip the format, pick a topic, tap a person. One tap and you are talking." Then: Cover / No cover / Full screen buttons; organizer tabs; search; world row; "Mail inbox — Personal"; "Conversations"; "Online in Design"; "Instant-message lists"; "Mail lists"; h2 "Install Smart Messenger"; "Personal activity"; "Choose what notifies you". 980 words, 28 buttons, 3 inputs, 4 emoji — the lightest full page in the network, and the only one whose second sentence tells a stranger exactly what to do.

- **Logic:** the purpose sentence is the best in the network. But the page has TWO jobs that fight: it is a mail inbox AND an install page for Smart Messenger ("Install Smart Messenger" is an h2, the same weight as the purpose). And the cover control — Cover / No cover / Full screen, 36px buttons, 12px type — is the control Shawn said (03:43Z) nobody understands: it asks the citizen to choose a view mode for a cover photo before they have read a single message. The saved lists are split into two panels ("Instant-message lists" / "Mail lists") saying nearly the same thing twice — "two worlds, connected but disconnected" is the file's own comment, and the stranger feels the split.
- **Elegance:** the best palette in the network (Sweep #1: 0 bright / 78 deep, cited once). The cover, though, is a purple/magenta/blue radial wash over a purple gradient (`.ph-cover`: radial 560px purple + radial 640px blue + 135° gradient `#1a1a3e → #2d1b4e → #4a2b7a → #0f3460 → #16537e`) — a colored background, the one thing the language forbids on a cover that should be the citizen's own image or obsidian. The F/D saved-list letters (Shawn 03:43Z: two shades of one hue) I could not isolate to single hexes in this blob — the TOPICS data carries per-person colors, and the unify round must prove the alignment in bytes; I record it as Shawn-named, byte-proof owed, not as my own finding.
- **Sizing — oversized:** the cover at 25vh/290px is fixed — but it is still the biggest thing on a mail page, bigger than any message. A mail cover should be a strip (~120px), not a billboard. **Undersized:** the message rows themselves — the inbox list is the page's work, and it sits below a 290px cover, a mode control, tabs, search, and a world row. The first message is a scroll away.
- **Usefulness:** mail by topic (not just by contact) is a real idea, and the page explains it in one line. The IM toggle is present in code. But the dock is its own bar — not the Five (03:43Z) — so the mail page's way home is different from every other page's way home.
- **Purpose test: PASS.** The only full page besides the calendar whose h1 + first line answer all three questions. It loses points for what surrounds the answer, not for the answer.

**Breaks:**
- M1 — Cover / No cover / Full screen control (Shawn 03:43Z: not understood). Fix: make it plain ("Show cover / Hide cover" as one toggle, in words) or remove it — one control, not three mystery modes.
- M2 — Cover is a 290px colored wash, bigger than any message. Fix: cover as a 120px strip, obsidian unless the citizen chose an image; the inbox list starts above the fold.
- M3 — Two jobs: inbox + "Install Smart Messenger" h2. Fix: install lives in Settings, not as a second h1-weight heading on the inbox page.
- M4 — Dock is not the Five (03:43Z). Fix: the Five, same as everywhere.
- M5 — F/D letters, two shades of one hue (Shawn-named 03:43Z; byte-proof owed by the unify round). Fix: one hex per hue, aligned to the Deep Palette set, proven in bytes.
- M6 — Flat buttons: the file's own comment records an elevation fix for six flat elements (`.format-note`, `.smart-note`, `.panel`, `.msg` family, `.install-later`, `.btn.ghost`) — Shawn 03:43Z says flat buttons still need real depth. Fix (unify round): verify each of the six has elevation on the rendered page, not just in a comment.

## 7. CALENDAR — obsidian rebuild tip 03700ad1 (score 6, purpose PASS month / FAIL day view)

**Judged:** blob 50bfdadd1f8234c239de27403098e5f1b06103a9, 78,881 B, sha256 abe86527 (commit 03700ad1, branch calendar/obsidian-rebuild-20261117). The rebuild HAS landed — this is not the "unlanded" case. The vision artifact is judged separately below.

**Read as a stranger, top to bottom (from the bytes + the artifact's captures, which share the design).** Static HTML shows almost nothing — 7 visible words ("NayaNET — Living Calendar ‹ Today ›"), h1 `#monthname` empty until JS fills it. That is the JS-app bargain, and the month view earns it back: full weekday names in Marcellus (`clamp(11px,2.2vw,20px)`), the pearl "i" eye bottom-right, digit tiles shrunk 54px → 40px in the day cell (36px/30px at narrower widths), 13 doors each carrying a live glimpse, no trailing next-month days in the grid code. The day view: day jewel, 13 doors, instruments (numbers on top, labels underneath), timeline, wisdom + Intel boards.

- **Logic:** the doors-with-glimpses idea is the best idea on this page — a door that shows you what's inside it. But three of the thirteen doors have no live source wired (news, weather, horoscope "say so honestly" per the file's own comment) — so a quarter of the day menu honestly tells you it has nothing to show you. Honest is better than invented; wired is better than honest. And the month grid's cells are empty black space — the month tells you nothing about any day until you tap the eye. A calendar that shows no trace of the days is a grid, not a planner.
- **Elegance — measured against Shawn's 03:47Z words, which are the newest law and the strictest test in this sweep:**
  - *Today lights up WAY more:* the rebuild's today treatment is `.cal-day.today` — a brighter halo (`0 0 22px rgba(dc,.38)`) and an 8px white dot top-right. A glow bump of degree, not the unmistakable "WAY more" he asked for — and the 8px dot sits top-right, where it competes with the number and reads as a second, unexplained mark. In the artifact's desktop capture, today (the 17th) is not distinguishable from any other day at a glance. **Not met.**
  - *The weekday name is a royal object:* the names ARE full and Marcellus now (`Sunday, Monday…`, white? No — rendered via inline `style="color:${w.color}"`, still in the day's color). Colored text on black is plain text in color, not a royal object — no elevation, no jewel, no depth. The 03:19Z elegance law asked for royalty; the 03:47Z word says plain text on black fails. **Not met.** And at ≤480px the names shrink to 9px with `white-space:nowrap` in ~49px cells — "Wednesday" at 9px is ~55px wide: it does not fit its cell. The size that fits and the size that reads are different sizes, and the code picks the one that fits.
  - *The eye, balanced — smaller, less white:* the eye is the harvested `.os-jewel-md`, 36px (30px ≤640px), a white disc with a black "i". In the artifact captures it reads exactly as Shawn described: a big white blob, too much white, unbalanced against the small dark cells. **Not met — shrink to ~24px desktop, less white face (jewel with a colored rim, white "i" on dark, or a smaller pearl), and prove it in a capture.**
- **Sizing — oversized:** the eye (36px white disc in a cell whose number is 40px — the door to the day's info is nearly as big as the day itself). **Undersized:** the weekday names at 9px on phone; the today marker (8px dot); the glimpse text under door names (11px, one line, ellipsis). **Caged:** the day view wraps at max-width 1060px (`.day-head`, `.view-wrap`, `.view-head`) — the day dashboard that should fill the land is caged to a column.
- **Usefulness:** booking works in code (book a time → appointment in the calendar, Smart Meet carried on the appointment). The day view has the instruments, the timeline, the boards. But the month gives no reason to open any day — no dots of "something is here" except one small record dot — so the usefulness is all behind a tap the stranger has no reason to make.
- **Purpose test: PASS for the month, FAIL for the day view.** The month says "this is your calendar" at a glance. The day view is the view Shawn scored 03:47Z — "it just looks like a mess… low end cheap, elementary tech" — and his 10-love / 10-don't-love scorecard rides into the v5 round. I carry his verdict; I did not render the day view myself (see Unproven).

**Breaks:**
- C1 — Today: halo bump + 8px dot. Fix: today unmistakable — the whole cell lit WAY more (brighter rim + filled presence + the number tile itself lit), so the 16th/17th jumps out from across the room. Remove the unexplained 8px dot or make it the record dot, one meaning only.
- C2 — Weekday names: full + Marcellus, but colored plain text, 9px on phone. Fix: the names as royal OBJECTS (elevated, jewel-rimmed, white) at a size that reads — and if "Wednesday" cannot fit a phone cell as an object, the month view on phone earns a different weekday treatment (abbreviated royal, or names above the grid), not a 9px squeeze.
- C3 — Eye 36px white disc. Fix: ~24px, less white, a jewel — and a capture proving it reads as a jewel, not a blob.
- C4 — 3 of 13 doors with no live source (news / weather / horoscope glimpses say "nothing yet"). Fix: wire the sources or the doors say what IS there (e.g. yesterday's weather pattern) — a door that opens onto "nothing yet" is a dead door.
- C5 — Month cells are empty black voids; no trace of the day's contents. Fix: each cell carries one small trace (a dot per thing, or the next appointment's time in 11px white) — the month should invite the tap.
- C6 — Day view caged at 1060px. Fix: the day dashboard fills the land (prime real estate — the whole land built on, his 03:35Z word).
- C7 — Static HTML is 7 words; h1 empty until JS. Fix: server-render the month name + the grid shell so the page exists before JS (same fix as the Hub's H1).

## 8. CALENDAR — vision artifact `the-ultimate-calendar` (score 5, purpose PASS as calendar / FAIL as day-planner)

**Judged:** artifact `the-ultimate-calendar`, index.html 61,579 B, sha256 a936b529 (CHANGED since Sweep #1's 45,340 B / 8b7295b0) + audit 2026-11-17T03-40-45Z (desktop 1440×900 + mobile 390×844 captures, read visually — EYE). The artifact is the vision, not the build; the rebuild already fixes most of it — but the artifact is still what Shawn was shown, and it still carries the breaks below in its newest capture.

**What the captures show (EYE).** Desktop: "NOVEMBER" in letterspaced Marcellus, year "2026" small and gray beside it; full day names (Sunday…Saturday) in their day's colors; digit tiles top-left in each cell (per-digit colors); a white "i" disc bottom-right in every cell; rims lit in the day's color. It is recognizably the calendar Shawn described — and it is still wrong in the exact places he named:
- **Two trailing rows of empty cells are STILL there.** Below Nov 29–30 there is a row of 5 empty cells, then a FULL row of 7 empty cells — 12 empty cells, two blank rows, the precise thing his 02:58Z word forbids ("no trailing blank row"). The grid does not end at the month's last day.
- **Every cell is an empty black void.** Number top-left, "i" bottom-right, nothing between. A month of black rectangles with numbers is a grid, not a planner — no trace of any appointment, note, or event anywhere on the month.
- **Mobile: the cells become tall vertical rectangles** (390px capture: each cell ~7x taller than wide) — the DNA §5 break Sweep #1 named, still present in the newest capture.
- **Two-digit dates are two-color confetti.** Each digit carries its own gematria color, so "10" is red-1 + white-0, "17" is red-1 + purple-7, "22" is orange-2 + orange-2. The date — the one thing the cell must say plainly — reads as rainbow noise. The tiles are canonical per digit (Sweep #1 T1, cited once) — but two canonical tiles side by side are still two colors fighting in one date. Elegance wants the date to read as ONE number.
- **The "i" discs are big white blobs** (EYE) — exactly Shawn's 03:47Z complaint. The year "2026" is gray (`#8b8b9c` family — Sweep #1 B8, cited once). Marcellus FAILED to load in the audit (fonts.googleapis.com blocked, ERR_SOCKS_CONNECTION_FAILED, twice) — the royalty in the capture is a Georgia fallback, so the "royal" reading is unproven on the real font.
- **Purpose test: PASS as a calendar, FAIL as a day-planner.** A stranger knows it is November. Nothing tells them what any day holds, or what to do here beyond tapping an "i" thirty times.

**Breaks (EYE unless noted):**
- A1 — Trailing blank rows: 12 empty cells in 2 rows. Fix: grid ends at the month's last day (the rebuild already does this in code — re-cut the artifact from the rebuild's grid).
- A2 — Empty black cells. Fix: one trace per day (see C5) — the artifact is a vision, and the vision must show the trace.
- A3 — Mobile tall vertical rectangles. Fix: cells keep their proportions at 390px (the rebuild's grid, not a stretched column).
- A4 — Two-digit dates as two-color confetti. Fix: the date reads as one number — one rim, one presence (the per-digit colors can live in the tile caps, not as two competing faces).
- A5 — Eye as white blob (EYE + 03:47Z). Fix: ~24px jewel, less white — same fix as C3, proven in a capture.
- A6 — Marcellus unproven (font failed to load in the audit). Fix: self-host Marcellus or prove the load; royalty cannot depend on a blocked Google Fonts request.

## 9. FORMATS — unfold 34c756ff (6, PASS) · slideshow 21d08a88 (6, PASS)

**Judged:** unfold blob 34c756fff6286c46a2ff61fa6224bc49e35d5abf, 32,079 B, sha256 70abc8e9; slideshow blob 21d08a88e0f2e63d3c30d8f5112a2479ecf52d59, 34,896 B, sha256 fcfa0c4c. Both canonical 2026-11-16, re-filed on branch personal/official-formats-bridge-20261116 (tip a456d270).

**Read as a stranger.** Unfold: h1 "The Official Unfold", "Press the button, go to the next experience — bits, not walls." 189 words, 3 buttons, 0 emoji — the best text discipline in the network (Sweep #1 B14, cited once). Slideshow: "The Official Slideshow — The same beats, sideways — one screen at a time." 195 words, 7 buttons, 0 emoji. The purpose is perfectly clear on both: press the button, get the next idea. One idea per board, three boards then the button — the law, kept.
- **Logic:** the formats are the grammar everything else is written in, and they are the clearest pages in the network. But the grammar has a hole in it: the `.face-mono` — see the named suspect. Every beat's top carries it, and the formats are the pages that teach every other page what a beat looks like. The hole is in the template, so it repeats everywhere the template is used.
- **Elegance:** clean, minimal, pro — the model for text discipline. Held back by bright-only palette (58 bright / 0 deep each — Sweep #1 B1, cited once) and the N disc.
- **Sizing — oversized:** the face-mono disc (240px — see suspect). The wrappers are caged at 980/940px (Sweep #1 B12, cited once) — a format that should fill the screen teaches every page to cage itself. **Undersized:** nothing — the formats' restraint is their virtue; the only undersized thing is the letter "N" itself (26px in a 240px disc).
- **Purpose test: PASS, both.** A stranger knows exactly what to do: press the button.

**Breaks:**
- F1 — The 240px N disc on every beat (see suspect). Fix: 56px, or the citizen's face.
- F2 — Max-width cages 980/940px (Sweep #1 B12, cited once). Fix: full width, the format fills the screen.
- F3 — Bright-only palette (Sweep #1 B1, cited once). Fix: the deepening pass the formats have been owed since the Deep Palette landed.

## 10. INTELLIGENT BLOCK EPIC — staged (score 5, purpose CONDITIONAL PASS)

**Judged:** blob 4319256de01d3a6454d427b701a50662ecfdeefc, 77,758 B, sha256 ff569709 (commit 3920de9f, branch intelligent-block/epic-20261117, PR #3390 open). Checker re-check: CONDITIONAL PASS on the code (hover override, textarea focus, distiller, image URLs) with the live leg open — cited, not re-judged.

**Read as a stranger, top to bottom.** Title "The Intelligent Block — Epic | NayaNET". NO h1. First visible: "NayaNET · The Intelligent Block · Epic / The Intelligent Block, Epic / The numbers are alive. / The buttons are the best. / Paste anything. It comes out beautiful. / or read the whole thing at once". Then the beats, each topped by the 240px N disc, then the studio: "Paste text / Paste a smart note / Paste an image", "Your beautiful block". 432 words, 16 buttons, 2 inputs — the second-lightest page in the network, and its sentence is clear.
- **Logic:** the engine works (checker-verified: paste text/note/image comes out beautiful; Shawn's eye PASSED it 03:34Z). But the page's existence as a standalone app is the question Shawn asked 03:35Z: "Why are you building another system? Build it into the Smart Factory, make it one." A beautiful standalone page for an engine whose home is the Factory is a page arguing with its own brief. The fold-in round (dispatched 03:36Z+) is the answer; this page is the before-photo.
- **Elegance:** the numbers-are-alive demo is genuinely delightful — tiles that lift and ignite. The 240px N disc on every beat is the opposite of delightful (see suspect). The 980/940px cages return here too.
- **Sizing — oversized:** the N disc, 240px × 3+ beats. **Undersized:** the paste studio — the page's actual job (paste anything) is a textarea + three buttons below the demo, smaller in presence than the demo of itself.
- **Purpose test: CONDITIONAL PASS.** "Paste anything. It comes out beautiful." answers the test — conditionally, because the page's purpose as a standalone destination is itself the open question.
- **Breaks:**
- E1 — Standalone vs Factory (Shawn 03:35Z). Fix: the fold-in — the Epic survives as the paste-anything engine inside the Factory/feed/pages, not as its own app. (Already dispatched; this page is judged as the before.)
- E2 — The 240px N disc on every beat (see suspect). Fix: 56px, or the citizen's face.
- E3 — 0 h1; cages 980/940px. Fix: h1 "Paste anything. It comes out beautiful."; full width.

---

## THE NAMED SUSPECT — the massive icon with the little N

**Found. It lives in the Intelligent Block family — the `.face-mono` disc — and it is exactly what Shawn described.**

| Where | Rule (byte-proven) | Size |
|---|---|---|
| Epic, blob 4319256d | `.face-mono{width:240px;height:240px;…font-size:26px;…}` + `@media(max-width:480px){.face-mono{width:168px;height:168px;font-size:20px}}` | 240px circle, 26px "N" (168px / 20px on phone) |
| Unfold, blob 34c756ff | identical `.face-mono` rule (byte-identical) | 240px / 26px (168px / 20px on phone) |
| Slideshow, blob 21d08a88 | identical `.face-mono` rule (byte-identical) | 240px / 26px (168px / 20px on phone) |

The markup, on every beat of all three pages: `<div class="ib-blocktop"><div class="face-mono" style="--tone:#8e24aa">N</div>…` — a 240px-diameter black disc with a 26px letter "N" sitting in its middle. The N is ~11% of the disc's diameter. The disc is ~9× the letter. And it repeats: every beat of the Epic, the unfold, and the slideshow carries one, so a stranger scrolling the Epic meets the same giant empty disc three or more times on one page.

**Judgment.** The icon itself (a black disc, own-color rim, white mark) is fine — the language is right. The size and the mark are the failure, exactly as Shawn said: "why just a little N in the middle and why so big, it makes no sense." A 240px disc says "look at me, I am the most important thing on this beat" — and what it contains is a 26px letter that says nothing. It is not a face (no photo — and the class is called "face"), not a logo (no wordmark), not a button (not clickable), not an identity (every beat shows the same "N"). It is a decorative void with a small letter in it, at the top of every idea, bigger than the idea it introduces — the beat's title sits beside it at 30px while the disc beside it is 240px. On phone it is 168px — still the biggest thing on the beat, still carrying a 20px letter.

**What should happen to it.** Shrink it to 56px — the `.face-mono-mini` size already built in the SAME files (56px circle, 14px mark), which is proportionate and already proven. Better: make it what its name says — a FACE. The photo variant already exists in the same files (56px round photo, own-color rim). The disc should carry the citizen's (or Naya's) actual face, 56px, at the top of the beat — or go away entirely, and let the jewel + the title carry the beat. The 240px disc should not survive on any page. One line: **240px → 56px, "N" → a face, or the disc goes.**

**Cleared — NOT the suspect (checked, proportionate):**
- Dashboard hero orb `.os-dd-orb`: 72px circle (48px on phone), 28px "N" (20px on phone), rings to −20px. The letter is 39% of the disc — a mark in a badge, not a speck in a void. It is the page's own mark beside its own greeting. Fine.
- Walk deal-seal: 120px circle, 54px "N" in Marcellus gold — the letter is 45% of the seal, a wax seal with a letter in it, exactly what a seal is. Fine.
- Epic/unfold/slideshow `.face-mono-mini`: 56px / 14px — proportionate, fine (and the size the big disc should become).

---

## RANKED WHOLE-NETWORK LIST — worst first

1. **The 240px N disc (Epic / unfold / slideshow)** — a 240px circle carrying a 26px "N", repeated on every beat of three pages. The named suspect, the single most visible sizing failure in the network. Fix: 56px, a face, or gone. (§ Suspect)
2. **Personal has no front door (no h1, title is a name, composer first; 407 buttons)** — the page a citizen lives on does not say what it is. Fix: h1 "Your world" + one line; composer becomes a button. (P1–P3)
3. **Dashboard opens with a nav wall + "Good morning." (282 buttons, three rival giant numbers 168/96/88px)** — the scoreboard that never says "this is your score." Fix: one purpose line + the score at 120px + one next action. (D1–D4)
4. **Hub's first paint is "NayaNET needs JavaScript" + title wrong twice (live "Intel Today", staged "Smart Feed") + h1 is a slogan** — the Hub has no front door for a cold stranger. Fix: server-render the first screen; title it the Hub. (H1–H3)
5. **Walk: the 86-beat letter buries the door (8,650 words, 117 buttons, three doors + a skip)** — the entrance reads as a contract. Fix: door first, letter one click away. (W1–W4)
6. **Artifact: two trailing rows of empty cells STILL there (EYE, 03:40Z) + every cell an empty black void + mobile tall rectangles** — the exact breaks Shawn named, still in the newest capture. Fix: re-cut from the rebuild's grid; one trace per day. (A1–A3)
7. **Calendar rebuild: today does not light up WAY more (halo bump + 8px dot), weekday names are colored plain text (not royal objects), eye is still a 36px white blob** — all three 03:47Z laws unmet on the tip judged. Fix: C1–C3.
8. **Pricing v78: the letter leads, the chart is buried (5,358 words, 0 h1, prices smaller than the letter's display type)** — the pricing page that makes you read a pitch to find a price. Fix: chart first, letter after. (PR1)
9. **Bottom-bar drift — five different bars where the law now says ONE (03:43Z): Hub six + CONNECT, Mail's own dock, Dashboard eco, Personal's duplicated eco definitions, Calendar none** — the mess Shawn named. Fix: the Five on every page; CONNECT only on his word. (H4, M4, P4)
10. **/free/walk: 20 h1s, 136 buttons, questions at 26px** — the purpose is clear but the hierarchy is flat. Fix: one h1, ten h2s at 32px. (PR4)
11. **Smart Mail: the cover control nobody understands + 290px colored-wash cover + inbox sharing the page with an install h2** — the best purpose sentence in the network, surrounded by confusion. Fix: M1–M3 (unify round input).
12. **Calendar day view: 3 of 13 doors with no live source + day view caged at 1060px + static HTML is 7 words** — a dashboard with dead doors in a cage. Fix: C4, C6, C7.
13. **/free: two doors (Install App vs ENTER) + "Certificate Nº ·" with no number + 0 h1** — the clearest deal in the network, with a hole in its certificate. Fix: PR3.
14. **Formats + Epic cages (980/940px) and bright-only palette** — the grammar teaches every page to cage itself. (Sweep #1 B1/B12, cited once.) Fix: full width + the deepening pass.
15. **Emoji standing in for object-glyphs (Personal 201, Dashboard 149–159, Pricing 87, Hub 34–43)** — (Sweep #1 B18, cited once.) Fix: white object-glyphs where emoji stand in for icons.

---

## UNPROVEN BY RENDER — what a live eye still needs to check

I did not see any of these pages render live (no VM browser in this seat; no browser tasks launchable from here). The artifact's captures are the only renders I judged. Everything below is unproven by MY eye and needs a live eye — at phone width first (390px), then desktop:

1. **First-screen composition, every page:** what a stranger actually sees at scroll 0 — the Hub's JS render (does the feed appear? does the greeting?), the Dashboard's hero (does the 168px score fit? does the nav wall dominate?), Personal's first screen (is the composer really open on load, or is it a dialog in the DOM?), the Walk's first screen (does the 9-dot nav overlap the brandmark at 390px — the file's own comment says it was fixed by showing the logo alone; prove it), Pricing's chart position (how far down is "Choose your level"?), Mail's first message row (does it clear the dock at scroll top — the Fix-3 claim?), the Calendar month at 390px (do the 9px weekday names fit or clip? does today read?).
2. **The calendar day view, rendered:** the whole day dashboard (doors, instruments, timeline, wisdom, Intel) — Shawn's 03:47Z "mess" verdict is his, carried here; the rebuild's day view needs a live eye to score it as built, including whether the 13 doors fill the land or sit in a 1060px cage.
3. **Hover / touch / alive:** lift, depress, orbit flow, the Dashboard orb rings (120s/180s in code — do they feel alive or dead?), the Hub eco bar lighting, the Epic tiles lifting on touch. Motion is code here; feel is eye-only.
4. **The five-icon bottom bar on every page (03:43Z law):** which pages actually show the Five, in which colors, at which size — the bytes prove the CSS exists in several places (and twice in Personal); only a render proves the bar a stranger sees.
5. **The eye, shrunk and balanced (03:47Z):** the fix for C3/A5 must be proven in a capture — a jewel, not a white blob — at desktop and at 390px.
6. **Hub Fix-5 (commit 6ce5b2af, landed 03:38Z) and Smart Mail Fix-3 round 2 (commit 94ec9327, blob e59e09b7, checker PASS) and Dashboard Fix-3 (running):** tips that moved during or after this sweep — none judged here; each needs its own byte + eye pass.
7. **The free walk's build step:** the ~6-minute stall with no progress/error/timeout and `/api/welcome/me` → `{"ok":false,"error":"unknown api"}` is carried from the eye's record (Sweep #1 B17) — not re-proven here, and it decides whether /free/walk works at all.
8. **Marcellus, actually loading:** the artifact audit shows the Google Fonts request FAILING (blocked) with a Georgia fallback rendering — whether Marcellus loads on the live Walk, Pricing, and Calendar is unproven until a render shows it.
9. **The F/D saved-list letters (03:43Z):** Shawn-named, two shades of one hue — I could not isolate the two hexes in the mail blob in this pass; the unify round must prove the alignment in bytes AND in a render.
10. **Clipping / overflow / duplication on narrow screens:** the Walk toolbar duplication from Shawn's screenshot batch, the Personal plus-button placement, the Hub drawer at 390px (Fix-5 claims one rail — unjudged), the Calendar two-digit fit at 481–1088px (the checker proved clipping in an earlier tip; the shrink in this tip needs a render to confirm the fix).

---

## THE HEART OF IT

**What the network is getting right at its heart.** The digit tiles are real objects — the one thing in the network nobody has to be told twice, harvested verbatim everywhere, and they work. The pearl "i" eye is the right IDEA (a door to the day's info, a real object coming off the page). The calendar's door-with-a-glimpse is the right IDEA (a door that shows you what's inside it). Smart Mail's second sentence — "Message anybody — by topic, not just by contact" — is the right SENTENCE (one line, the whole product). The formats' one-idea-per-board is the right DISCIPLINE (189 words saying more than the Walk's 8,650). The heart is sound: real objects, one idea per board, doors that show you what's inside. Nothing in this sweep says the heart is wrong.

**The one pattern that, fixed everywhere, lifts everything most.** Every page opens with the wrong first thing. The Dashboard opens with its own index. Personal opens with a composer. The Hub opens with "needs JavaScript." The Walk opens with a contract. Pricing opens with a letter. The Epic opens with a demo of itself. The Calendar opens with seven words and an empty h1. Only Smart Mail and /free open with the answer — and even they bury it under a cover and a second door. The fix is one pattern, applied nine times: **the first screen says what this is, what it's for, and what to do here — in one line, with one next action — and everything else lives below it.** Do that, and the purpose test passes everywhere at once; the scores above rise two points each without touching a single color, and the network stops reading as nine different designs and starts reading as one world. That is the heart of it: first screen first.

---

## ADDENDUM — 03:51Z: THE BEST BUTTONS IN THE SYSTEM (added before filing)

Shawn's word, 03:51Z, landed as this report was written: the Dashboard's PTS / % / MONEY mode pills are the best buttons in the whole system — THE button standard. Anatomy: obsidian black pill, bold white text, one deep color per button as rim + glow (purple PTS, blue %, green MONEY). Clean and bold, readable at a glance, each its own color, premium — "she should learn from that." They are harvested verbatim, never redesigned, never touched; every button in the system is measured against these three. He also likes the notifications on them — very clean and bold.

Inspector's note: this does not change the Dashboard's score (5) — the pills are right and the page around them is the problem (D1–D4 stand). It does add the button reference the whole network was missing: the pills are now the fourth reference object, beside the top-left +, the Smart Note board, and the X button. Every button break in this report should be fixed by measuring against the PTS / % / MONEY pills, not by inventing a new button. The cleanest proof of the standard is that the page holding it still fails the purpose test — a perfect button does not save a page that opens with its own index.

---

## RECEIPTS (what was actually read)

- **Standards read:** THE-NAYA-DESIGN-LANGUAGE.md (full), plus the Deep Palette hexes and day colors from the brief; Sweep #1's full report as the language baseline (cited, not redone).
- **Walk staged:** worker root 938,546 B, sha256 e27c7fe1 = blob 11cfc233cdadff396846ce5325f76cc98d81a013 (tip 12890208). 8,650 words, 117 buttons, 277 imgs, 2 h1s, top font 54px.
- **Dashboard Fix-2:** blob 3244de682944c6a6df8168fd1a06e2ae074bf19c, 1,943,088 B, sha256 e4e098be. 1,474 words, 282 buttons, 21 inputs, 149 emoji, 1 h1 ("Good morning."), top font 168px. Live: 1,817,928 B, bb41114d (matches brief).
- **Personal facelift:** blob ba628de3c9bb130eda6a0ca1818efde0be78e18a, 3,233,538 B, sha256 69b7235c. 5,068 words, 407 buttons, 47 inputs, 201 emoji, 0 h1, top font 84px (JS detail view).
- **Hub Fix-4:** blob fd802b03b01b35add806b040017ad376689cf7c8, 4,873,750 B, sha256 340b1326. 32 static words, 33 buttons, title "Smart Feed — NayaNET". Live now: 4,830,033 B, bb380404 — DRIFTED from brief's 4,678,679 B / bfbd895a.
- **Pricing v78:** worker 11,360,503 B, sha256 ca2eafeb. 5,358 words, 37 buttons, 87 emoji, 0 h1. **/free:** 310,212 B, dfe70a8c; 271 words, 7 buttons, 0 h1. **/free/walk:** 3,292,257 B, 2370eae2; 1,578 words, 136 buttons, 20 h1s, top font 26px. Live v77: 11,355,594 B, b043167b (matches brief).
- **Smart Mail:** blob 3935e96257d08c5d3f123bc8a29c05c0d30fa74a, 92,502 B, sha256 acab5ca1 (commit 48d72031 — message calls it Fix-3). 980 words, 28 buttons, 3 inputs, 1 h1. Newer tip 94ec9327 / blob e59e09b7 (92,927 B) noted, not judged.
- **Calendar rebuild:** blob 50bfdadd1f8234c239de27403098e5f1b06103a9, 78,881 B, sha256 abe86527 (commit 03700ad1). 7 static words, 24 buttons, 5 inputs. Weekday render `style="color:${w.color}"` + Marcellus clamp(11px,2.2vw,20px), 9px ≤480px; `.cal-day.today` halo + 8px dot; eye `.os-jewel-md` 36px (30px ≤640px); digits 54px → 40px in cell; doors DOORS array (13, Deep Palette, glimpses); day view max-width 1060px.
- **Calendar artifact:** index.html 61,579 B, sha256 a936b529 (changed since Sweep #1's 45,340 B / 8b7295b0) + audit 2026-11-17T03-40-45Z, desktop + mobile captures read visually (EYE), report.json (0 clipped, 0 overflow, Marcellus font load FAILED twice).
- **Formats:** unfold blob 34c756fff6286c46a2ff61fa6224bc49e35d5abf, 32,079 B, sha256 70abc8e9; slideshow blob 21d08a88e0f2e63d3c30d8f5112a2479ecf52d59, 34,896 B, sha256 fcfa0c4c. Both: `.face-mono` 240px/26px, 189/195 words, 0 emoji.
- **Epic:** blob 4319256de01d3a6454d427b701a50662ecfdeefc, 77,758 B, sha256 ff569709. 432 words, 16 buttons, 0 h1, `.face-mono` 240px/26px.
- **Checker verdicts read (as claims, then re-verified where I cite them):** Dashboard Fix-2 (CONDITIONAL PASS), Personal facelift (PASS), Hub Fix-4 context, Smart Mail Fix-3 round 2 (PASS), Epic re-check (CONDITIONAL PASS), Calendar amendment-2 checker (CONDITIONAL PASS, carried).
- **Branch tips verified via API during the sweep:** walk-end 12890208 · dashboard fbea205c · personal formats a456d270 · personal feed c7ccbd28 · hub 6ce5b2af (Fix-5, landed 03:38Z) · mail 94ec9327 (Fix-3 round 2) · calendar 03700ad1 · epic 3920de9f.
- **Shawn's words used as law:** 03:35Z (this sweep's charge + Factory-is-the-formatter + day view is a dashboard) · 03:43Z (one bottom bar / high-tech alive / one Smart Mail) · 03:47Z (today WAY more / royal weekday object / balanced eye / day view "a mess") · 03:19Z elegance law · 03:01Z/03:02Z day-menu and eye laws — all as cited in the sections above.
