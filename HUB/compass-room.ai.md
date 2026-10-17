# Compass Room — AI builder spec (exact values)

**Status:** DESIGN PROOF. Not shipped, not production. The first pilot is read-only.
**Product:** Naya Compass — the buyer-facing decision guide.
**Product promise:** "Find your direction. Understand why. Take the next step. Learn from the journey."
**Authority:** `compass-room.machine.json` (schema `naya.hub.compass-room.v1`) is authoritative on tokens; this file is authoritative on rendering behavior. On conflict, the machine file wins.
**Shipping contract:** issue #2436, Action 8 — one Compass room in the Hub, no second shell.

## 1. Four-layer answer structure (Intelligent Blocks)

Every Intelligent Block renders exactly four layers, in this order:

1. `nutshell` — one or two sentences, the whole thing
2. `what_it_means` — plain explanation
3. `how_to_use_it` — the next action
4. `whats_in_it_for_you` — why it matters to the human

Render rule: the nutshell is always visible; the other three expand on tap. Tap toggles with 200ms ease on max-height and the chevron rotates 180 degrees. `prefers-reduced-motion` means instant, no transition. Same expandable pattern as the sibling `HUB/learning-lifecycle-mock.html`.

## 2. Typography (exact ruling)

- body: 18px, line-height 1.5
- headline (h2): 18px, weight 800
- sub-headline: 14px
- big headline (h1): 24px, weight 800

System font stack: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`.

## 3. Color standard (exact)

Order: black, white, purple, blues, green, gold. Forbidden: amber, rose pink.

- `--black: #0A0A0F` — cards
- `--white: #F5F5F7` — text
- `--page-bg: #050508` — page background
- `--purple: #A855F7` — glow accent ONLY, never solid fill
- `--blue: #4D9FFF`
- `--green: #2ECC71`
- `--gold: #F5C518`
- `--neutral-gray: #6B7280` — chrome/outlines for UNKNOWN only; not a data color
- `--chrome-grays: #1c1c22 / #222222 / #333333 / #444444 / #555555` — chrome borders and dividers (machine.json: `chrome_gray_*`)

Rules: buttons are black with a 1px purple edge glow and light up white on interaction. Purple is glow/accent — never a solid fill. Cards ignite on hover with a subtle glow. One clear visual hierarchy.

Truth-state render map (exact):

- OBSERVED — blue outline pill, blue text
- VERIFIED — green outline pill, green text
- CLAIM — gold outline pill, gold text
- UNKNOWN — neutral-gray outline pill, white text
- STALE — purple-glow pill (accent border + purple glow shadow, never solid fill)
- CONFLICTED — gold solid background, black text, bold (the jewel alert; stays inside the palette)

## 4. Visual bliss law

Contrast, clarity, cleanliness, best UX — presentation over colors. Generous text sizes, high-contrast readable type, one clear visual hierarchy, restraint. The test: effortless on the eyes.

## 5. Mobile-first, app-like

Single column on phones; two-column card grid at 768px and up. Max content width 960px. Touch targets at least 44px. No overwhelming dashboards — one room, one journey, six calm screens.

## 6. Screen copy contracts

Global: every screen shows the truth-state legend on first view; every fact shows its truth label; tapping any recommendation shows its source lineage (mock: lineage text inline).

**Screen 1 — Intent** (`intent`)
- H1: "Where do you want to go?" (journey-scoped variant: Founder "Limited funds, two weeks — what next?", Team "Which work today?", Engineering "Can this PR merge?")
- Lede: "Say it in plain words. Naya asks one material clarification — never a form."
- Required blocks: intent card (goal / scope / beneficiary / constraints / deadline), one clarification Q&A.

**Screen 2 — Reality & Evidence** (`reality`)
- H1: "What is actually true?"
- Lede: "Every fact carries a truth label, and its source, owner, and expiry where applicable. Tap a label to see why. UNKNOWN facts state the absence explicitly."
- Required blocks: fact cards — each with value, truth label, and source, owner, observed_at, expires_at where applicable — UNKNOWN facts show the absence explicitly. A fact-freshness note carrying the TTL table. Empty state `no_facts` when there are zero facts.

**Screen 3 — Choices** (`choices`)
- H1: "Your real options"
- Lede: "Real options from real facts — plus NO_OP, READ_MORE, and ASK. Nobody types in scores."
- Required: choice cards, each with evidence refs and the four layers. NO_OP, READ_MORE, and ASK are always present as choices.

**Screen 4 — Recommendation** (`recommendation`)
- H1: "The wisest route"
- Required: exactly ONE recommendation card — the route, WHY (evidence-bound), the runner-up, confidence bounds, what-would-change-its-mind. On overlapping uncertainty, invent no winner: the card says so and offers READ_MORE. Empty state `no_recommendation` when Reality is incomplete.

**Screen 5 — Navigate** (`navigate`)
- H1: "Take the next step"
- Required: reversible-step checklist; authority note, verbatim: "You hold the final say. This pilot is read-only — it schedules nothing and messages no one for you."

**Screen 6 — Experience** (`experience`)
- H1: "Learn from the journey"
- Required: frozen-forecast block, observation-window block, independently-observed-result block, calibration note, verbatim: "A self-report is not verified learning." Empty state `experience_pending` until the window closes.

## 7. Empty states (exact copy — verbatim in spec, machine file, and mock)

- `no_facts`: "No facts yet. Tell Naya where you want to go and she'll start gathering what's actually true."
- `no_recommendation`: "No recommendation yet — the Reality screen comes first. Naya won't guess before the facts are in."
- `no_choices`: "No admissible choices right now. NO_OP is always available — doing nothing on purpose beats doing the wrong thing."
- `experience_pending`: "Forecast frozen. The observation window is open — results land here when they're independently observed, not before."

## 8. Mock-page rules

- Persistent top ribbon, sticky: text exactly `MOCK — SAMPLE DATA, NOT LIVE`. Black background, 1px purple bottom edge, purple glow shadow, white 14px caps, letter-spacing 1px.
- ALL sample data carries `data-mock="true"`. Demo truth is synthetic and stays labelled.
- No network calls, no live services, no writes. The mock contains zero `http(s)` resource URLs and zero fetch/XHR/WebSocket.
- Zero-JS-error: the page's script must pass `node --check`.
- The room renders inside a Hub shell header mock with the room as a socket panel — NOT a parallel site.

## 9. Evidence-quality weights (canonical, from #2436)

`objective_fit` 20 + `evidence_sufficiency` 20 + `applicability` 15 + `robustness` 15 + `reversibility` 10 + `blast_containment` 10 + `simplicity` 10 = 100. Each scored 0–10, each derived from a versioned evidence rule and source. These anchors are PROPOSED policy, not ratified LAW — the surface renders them labelled.

## 10. Fact TTLs (seconds, from #2436)

main 15 · pr_checks 30 · lane_lease 30 · mission 120 · lesson_applicability 300. Protected authority and consent are LIVE-rechecked at execution irrespective of TTL. A stale result must never become a positive action input.

## Evidence

- Shipping contract: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2436 (product architecture, exact customer screens, canonical technical contract, three pilot journeys, ten execution directives)
- Sibling surface conventions converged: PR #2413 branch files `HUB/learning-lifecycle-mock.html`, `HUB/learning-lifecycle.human.md`, `HUB/learning-lifecycle.ai.md`, `HUB/learning-lifecycle.machine.json` (ribbon text, data-mock attribute, expandable four-layer pattern, palette)
- Machine tokens: `HUB/compass-room.machine.json`, schema `naya.hub.compass-room.v1`
- No-duplicate-mechanisms survey at author time: zero Compass/room/socket open PRs, zero Compass files in `HUB/` at the anchored tip, no racing claim on the coordination board's newest comments
- Wave-27 builder receipt: `~/workspace/goals/nayapower-10-10-completion-drive/hidden_files/wave27-product-compass-builder-receipt.md`
