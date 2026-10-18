# SCORECARD — 19 gap blocks (independent VERIFY read, 2026-10-16)

**Seat:** VERIFY / Chi · Team Nitro
**Phase:** 2 of 2 (Phase 1 fixer: BUILD / Nu — this seat scored independently)
**Scope:** `DESIGN/gap-blocks/calendar-blocks.md` (CAL-001–005) · `DESIGN/gap-blocks/checkout-blocks.md` (PAY-001–005) · `DESIGN/gap-blocks-2/comments-blocks.md` (CMT-001–003) · `DESIGN/gap-blocks-2/chat-blocks.md` (CHT-003–005) · `DESIGN/gap-blocks-2/onboarding-blocks.md` (ONB-001–003)
**Standards:** `~/workspace/team-nitro/DESIGN-LAWS.md` · `DESIGN/BLOCKS.md` (four parts per block: code, states, do/don't, honest anatomy)
**Method:** every spec file read in full, scored block by block against the laws. No inflated grades. The bar is 9.5 (triple-A); a block below it names exactly why and the fix.

**Head verified:** `518200db9` (matches `git ls-remote origin nitro/design-library` at scoring time).

---

## Phase 1 fix verification — which fixes hold under independent reading

| # | Fix claimed | Verdict | Evidence |
|---|---|---|---|
| 1 | Gold/today disambiguation | **HOLDS** | Family intro carries the dated disambiguation note; CAL-001/003/005 use 2px white-hot chrome + `cal-breathe` for today; CAL-004's now-line is chrome-white; family notes: "gold has exactly one job — decisions & deadlines, on event surfaces." No surface carries gold as both state and event meaning. |
| 2 | Chevrons + steppers → `.naya-btn` | **HOLDS** | CAL-001 chevrons are `.naya-btn.icon.micro.cal-chev` (glyph only, drawn chevron); PAY-001 steppers are `.naya-btn.icon.micro.pay-step`; canonical `.naya-btn` DNA pasted in both files (54px min, conic ring, press, focus, disabled, reduced-motion). No bespoke button system remains in the fixed files. |
| 3 | Live-motion specs | **HOLDS** | Family motion table (keyframes + duration + easing + reduced-motion per motion); `cal-breathe` 4s ease-in-out infinite with glow-only keyframes, defined in both CAL-001 and CAL-005 "by design: each block self-contained"; `pay-ignite`/`pay-breathe` in PAY-003; every hover has a reduced-motion fallback. |
| 4 | Privacy validation script passes | **HOLDS** | Ran `bash DESIGN/gap-blocks/validate-checkout-privacy.sh` myself: **PASS, exit 0** — no PAN, identifiers attribute-scoped, no `console.*`, display shows at most last-4 + brand. |
| 5 | Backend-gate annotations | **HOLDS** | "Backend gate" items in PAY-001/002/003/004/005 anatomy + family contract §6 (dated 2026-10-16): every money state renders from a backend response, never a client-side decision; specimen numbers labeled illustrative. |

**Catalog staleness flagged (follow-up for BUILD, not scored):** `DESIGN/BLOCKS.md` lines 1280–1292 still describe the pre-fix world — "today ignited in gold" (CAL-001), "gold edge + gold number" (CAL-003), gold now-line (CAL-004), "gold wins" for today-over-selected (CAL-005). The fixed specs are authoritative; the catalog entries contradict them and need a sync pass. Builders reading the catalog first would implement the old behavior.

---

## CALENDAR family — 9.2 (CAL-001 9.5 · CAL-002 9.0 · CAL-003 9.0 · CAL-004 9.0 · CAL-005 9.5)

The strongest family in the set. The Phase 1 fixes landed cleanly, the gold disambiguation is structural (today is chrome everywhere), motion is specified to keyframes, and the "never fake" clauses are real contracts. What keeps it from a perfect family score: CAL-002's missing keyboard contract and responsive spec, CAL-003's missing dropdown-flip rule, CAL-004's invalid `div`-inside-`ol` for the now-line.

### CAL-001 · Month-view board — 9.5

The flagship. Chevrons wear `.naya-btn` DNA with drawn glyphs; today is white-hot chrome with a spec'd 4s breathe; out-of-month cells keep their "jumps month" promise; overflow is honest (`+N more` = the real count); specimen states its frozen-today is a specimen. Four parts, all present, laws clean.

- **Why not 10:** the `+N more` chip opens the day's agenda (CAL-004) but carries no `aria-expanded`/`aria-controls` contract — the overflow control's relationship to what it opens is prose, not markup.
- **Fix:** pin the chip's accessibility wiring in the block (button with `aria-expanded`, pointing at the agenda panel id), matching the care given to CAL-003's dropdown.

### CAL-002 · Event card — 9.0

Time rail, spine, type tag, serif title, drawn SVG meta glyphs; all-day/span/tentative variants specified honestly (no fake `00:00–23:59`, `~` for tentative). Color is earned — never a flood at rest.

- **Why not 10:** the card is an `<article tabindex="0">` with hover states but **no keyboard contract** — no Enter/Space handler, no stated role or destination; a focusable card that does nothing on Enter is a beautiful-but-inert affordance (Forbidden #9). Also no responsive behavior: the 86px rail + body at narrow widths will crush; nothing specifies a sub-560px stacked variant.
- **Fix:** add the keyboard contract (Enter activates; state where it goes) and a narrow-viewport variant (rail collapses to a top band, body stacks).

### CAL-003 · Date picker — 9.0

Genuinely honest: past dates are dimmed *and* keyboard-unreachable (`disabled` + `tabindex="-1"`), the trigger never pre-fills "today," and the timezone footnote is part of the block — "Calendar date only — no timezone is assumed or stored."

- **Why not 10:** the dropdown opens below the trigger only (`top:calc(100% + 10px)`) with no flip rule — near the viewport bottom it clips, and nothing says what happens. No max-height/scroll contract for long months on short screens.
- **Fix:** specify flip behavior (opens upward when <340px clearance below) and a max-height + internal scroll contract for the panel.

### CAL-004 · Agenda list — 9.0

White now-line in chrome (disambiguation held), spines in wheel order, empty day with dignity, past events readable-but-not-clickable-theater. The "3 events" count is real.

- **Why not 10:** the now-line is a `<div class="cal-now">` inserted **between `<li>` elements inside an `<ol>`** — invalid HTML. Also the specimen's past-event card keeps `tabindex="0"` while the States section says past events get `aria-disabled` and no hover lift — the specimen doesn't practice its own rule.
- **Fix:** make the now-line an `<li>` (list-style none) or absolutely position it; update the specimen so past events carry `aria-disabled="true"` and drop `tabindex`.

### CAL-005 · Day-cell state system — 9.5

Seven honest states frozen, composable classes, written precedence order (today > selected > hover > has-events > rest), today-breathe keyframes defined *in this block's own stylesheet* so the strip is self-contained. The precedence rule is the kind of thing that prevents two builders from ever disagreeing.

- **Why not 10:** disabled (32%) and out-of-month (34%) sit 2% apart — visually adjacent meanings with near-identical dimming, carried only by the label. Marginal, but a state system lives or dies on instant distinction.
- **Fix:** widen the separation slightly (e.g. out-of-month keeps 34% but drops the border brightness, disabled drops to 30%) so the eye reads the difference before the label.

---

## CHECKOUT family — 8.9 (PAY-001 9.0 · PAY-002 9.0 · PAY-003 8.5 · PAY-004 9.0 · PAY-005 9.0)

Money is the most trust-sensitive surface and the specs mostly treat it that way: backend-gated money states, the PAN boundary enforced by a passing script, plain-words validation that never blames the user. What keeps it below the bar: a cross-block CSS dependency (`.naya-btn--quiet` defined in PAY-003, consumed by PAY-004), and PAY-003's softer edges. Prior honest mark 8.8 — the fixes bought ~0.1 of real improvement; the remaining gap is structural hygiene, not vision.

### PAY-001 · Order summary board — 9.0

Table law (labels left, numbers right, tabular figures), "estimated" tax, honest empty state, steppers on `.naya-btn` DNA with `aria-live` output. The "never shows a price it can't prove" rule is load-bearing.

- **Why not 10:** `.naya-btn` DNA is pasted into both the calendar and checkout files — a copied canonical is a drift risk, and the fix isn't enforced (no "single source" rule). Smaller: the `.pay-apply` class in the markup has no styles (dead class), and thumb jewels use unicode glyphs (✦ ▲ ◆) while Law 4 says icons are drawn.
- **Fix:** add a family-level rule — `.naya-btn` ships from one canonical source (import/include, not copy-paste); replace unicode thumb glyphs with drawn SVG; drop or style `.pay-apply`.

### PAY-002 · Payment form — 9.0

The privacy boundary is the spec's best feature: PAN lives in transient inputs bound for the processor, never rendered back, never logged — and the script proves it. Floating labels, plain-words validation, disabled-until-valid Pay.

- **Why not 10:** the enable contract is prose ("the integrator's validation script adds…") — the block specifies *what* valid looks like (`.is-valid`/`.is-invalid`) but never pins the actual rule the button obeys (enables iff all four fields carry `.is-valid`; runs on blur + input). The money-moving button's enable logic should not be left to integrator improvisation.
- **Fix:** write the enable contract as code: the validator's state contract (which class on which event, what enables the button, that a failed payment never clears the form — cross-linked to PAY-004's retry).

### PAY-003 · Confirmation state — 8.5

One ignition then breathe (maximum life, minimum noise), the receipt-email truth states (green ✓ confirmed vs gold ? claimed), the hologram number as layered light. The restraint *is* the celebration.

- **Why not 10:** `.naya-btn--quiet` is **defined in this block's stylesheet but consumed by PAY-004's markup** — a builder implementing PAY-004 alone ships an unstyled "Use a different card" button. Blocks must be self-contained (the calendar family states this rule explicitly; checkout violates it). The family contract should own the quiet variant once.
- **Fix:** move `.naya-btn--quiet` into the shared PAY token/contract section and state it once; PAY-003 and PAY-004 both reference it. (Family-level fix — counted against PAY-003 where it's defined.)

### PAY-004 · Error state — 9.0

The best-behaved error panel in the set: "no money moved" first, three next-steps ordered by likelihood, cause named honestly (declined / processor silent / timed out), unknown charge state gets "we're confirming" instead of a guess, retry re-submits validated data with a retry-in-flight guard. Calm red, never an alarm.

- **Why not 10:** it inherits the `.naya-btn--quiet` cross-block dependency from PAY-003 (same family fix). Otherwise the strongest checkout block.
- **Fix:** the family-level quiet-variant move (see PAY-003); then this block is 9.5.

### PAY-005 · Payment method picker — 9.0

Real radiogroup where the rows *are* the controls, brand jewels in brand colors, one-row empty picker, privacy boundary carried in the spec. The "Default" chip is quiet.

- **Why not 10:** the Default chip is **gold** — but this family's own law (PAY-001) says gold's one job is "the total, the final word… the only place gold appears." Two gold jobs in one family dilutes the meaning Law 2 demands ("the meaning never changes between instruments"). "Attention, earned" stretches to cover a default card, but it stretches.
- **Fix:** give the default chip a non-gold identity (white-lit chip with a drawn diamond, or purple "choosing intelligence" — the default is a *choice*) and keep gold sacred to the total.

---

## COMMENTS family — 8.8 (CMT-001 8.5 · CMT-002 9.0 · CMT-003 9.0)

Wave-2, graded fresh. Strong doctrine — depth cap at 3 with a stated continue panel, plain-words timestamps on real `datetime`s, tombstones that leave no remains, private-by-default. The main gap versus the fixed wave-1 files: Phase 1's `.naya-btn` conversion never reached this family — the chevron and Post button are bespoke, and there's a second quiet-control system (`.cmt-morebtn`) with no canonical home.

### CMT-001 · Comment thread — 8.5

Honest nesting (3 rails walking the Strip, then the cap says its name), collapse chevrons with real counts, composer Post disabled until there's text, edited disclosed quietly. The "never claims a local append reached anyone" rule is the right paranoia.

- **Why not 10:** `.cmt-chev` (the 44px collapse chevron) and `.cmt-post` (the Post button) are **bespoke controls** — black center, white rim, lift, purple ignition — i.e. `.naya-btn` DNA re-implemented by hand, without the conic ring, press parity, or the canonical focus rule. Phase 1 converted calendar chevrons and checkout steppers to the one DNA; this family still runs a second button system.
- **Fix:** re-home `.cmt-chev` → `.naya-btn.icon.micro` (drawn chevron glyph, as CAL-001 did) and `.cmt-post` → `.naya-btn` (52px), exactly the Phase 1 pattern.

### CMT-002 · Single comment — 9.0

CMT-001's atom, no drift: same jewel, same name row, same action row. Clamp with a real "Show more"/"Show less" control that keeps the full text in the accessibility tree; the love toggle and the reaction pill share one number (stated, twice).

- **Why not 10:** `.cmt-morebtn` is a third quiet-control idiom in the repo (alongside `.naya-btn--quiet` and `.onb-quiet`) with no canonical home — quiet controls are proliferating instead of being specified once.
- **Fix:** bless one quiet-control DNA in writing (the family's recommendation: a `.naya-btn--quiet` variant owned once at catalog level) and re-home `.cmt-morebtn` onto it. Until then the family runs two control systems.

### CMT-003 · Reaction row — 9.0

Fixed five-reaction set in wheel order, zero-count pills don't exist, no sorting by count (popularity is not a ranking the UI invents), mine-state held glow, toggle-back without guilt copy. Reactions are play, not status.

- **Why not 10:** the popover claims `role="menu"` / `role="menuitem"` but the keyboard contract is buttons, not menus — no arrow-key roving, no Home/End specified. A menu role promises menu keyboard behavior; the specimen delivers button behavior.
- **Fix:** either specify the full menu keyboard contract (arrows move between the five, Esc closes, focus returns to the plus) or downgrade the roles to `group`/`button` to match the actual behavior. Don't promise a menu and ship buttons.

---

## CHAT family — 9.0 (CHT-003 9.0 · CHT-004 9.5 · CHT-005 8.5)

Wave-2, graded fresh. The family law is the spine: **truth-states only** — receipts move forward from the transport's truth, the typing indicator demands a live signal id (`throw` otherwise), the scroll edge is measured at 64px. The 72bpm heartbeat as a *number* (`--bpm:0.833s`) is the kind of specificity the laws ask for. Gaps: a real tail-rendering defect, a specimen that contradicts its own grouping rule, a stale block-number reference.

### CHT-003 · Chat bubbles — 9.0

In/out language fixed (white-lit incoming, held-purple-edge outgoing, gold read), grouping rule stated, drawn ticks, `chatReceipt` as the single writer of `data-state`. "Seen" only when the other side renders — the one unforgivable sin named.

- **Why not 10:** two real defects. (1) The tail uses `background:inherit` on a rotated square over a *gradient* bubble — the inherited gradient won't align with the parent's, so the tail's fill mismatches the bubble. Known CSS pitfall, will render wrong. (2) The specimen contradicts its own grouping rule: 21:04, 21:05, 21:06 are same-sender, <5 min apart — one group per the stated rule — but the specimen splits them across two groups.
- **Fix:** solid-color tail (the bubble's base tone) instead of `background:inherit`, or reposition the gradient to match; make the specimen honest (group all three, or separate the times >5 min and show the rule working).

### CHT-004 · Typing indicator — 9.5

The best wave-2 block. Signal-gated rendering (`show()` throws without a live signal id — the law in code), 30s watchdog, keep-alive contract, dots breathe at 72bpm with quarter-beat stagger, reduced motion keeps the meaning. "A typing indicator that outlives the typist is a ghost with styling."

- **Why not 10:** the prose claims a staleness rule the code doesn't enforce — "a signal older than 20s without re-assertion is stale and the next keepalive is ignored" — but `keepalive()` resets the timer unconditionally; no last-assertion timestamp is tracked. The claim and the code disagree.
- **Fix:** make the code match the prose (track last-assertion, ignore stale keepalives) or soften the prose to what the code does. Prose and code must be one truth.

### CHT-005 · Message list — 8.5

The scroll contract is genuinely good: measure `atBottom()` *before* the row lands, never yank a reader, the pill is a real button that keeps its promise, presence renders only from a live feed. Loading is words, never fake skeleton bubbles.

- **Why not 10:** (1) the family notes say "message composers… are future blocks (**CHT-004+**)" — but CHT-004 is the typing indicator, so the range is wrong (should be CHT-006+); a wrong forward-reference sends builders to the wrong block. (2) The empty room invites "Say the first word" with no composer on screen — an invitation with no door (the scope-out is stated, but the specimen still ends the sentence mid-air).
- **Fix:** correct the forward reference to CHT-006+; give the empty room either the composer slot reference or a quiet "the composer arrives with CHT-006" line so the invitation isn't a dead end.

---

## ONBOARDING family — 9.0 (ONB-001 9.0 · ONB-002 9.0 · ONB-003 9.0)

Wave-2, graded fresh. Coherent doctrine: each step earns the next, one job per step, honest percentages, celebration with restraint (one ignition, then calm). The stepper's fill derives from the current step's real index; the progress block binds number, fill, ring offset, and `aria-valuenow` to one source — "four mouths, one truth." The welcome card's nameless default is honest ("Welcome." — no invented name, no "friend"). Flat across the three, no standout, no disaster.

### ONB-001 · Stepper — 9.0

Five jewel nodes in step colors, done/current/locked as real states, locked steps truly inert (`disabled` + out of tab order), thread fill computed from the current index — "it never fills the thread past the current step."

- **Why not 10:** the Do section promises an honest **"Skip this step" control** for optional steps, but no skip control exists in the code, the states, or the anatomy — the specimen's optional step 3 has no skip. Prose promises what the block doesn't ship.
- **Fix:** specify the skip control (look, placement, behavior — skipping advances the flow honestly, never silently "completes") or scope it explicitly to the step-content block (ONB-004+). Don't promise it here and build it nowhere.

### ONB-002 · Welcome card — 9.0

Naya's face *and* her energy (drawn SVG + 5s halo breathe — Forbidden #5 satisfied properly), one CTA, a quiet exit that doesn't compete, and the honesty footnote as part of the block: "This card knows only what you've told it."

- **Why not 10:** the CTA (`.onb-cta`, 52px) is bespoke — black center, white rim, purple ignition — i.e. the `.naya-btn` DNA re-implemented without the conic ring or press parity. Same issue as CMT-001: the one button law doesn't reach wave-2. The quiet exit is an `<a href="#">` — a dead link in a specimen about honesty.
- **Fix:** re-home the CTA onto `.naya-btn` (≥52px variant); make the quiet exit a real control (button with a stated destination, not `#`).

### ONB-003 · Progress indicator — 9.0

Linear + ring variants, the ring math checks out (r=54 → 339.29 circumference; 62% → 128.93 offset ✓), indeterminate state refuses to invent a number ("No number yet"), `.is-complete` fires once when the backend confirms 100%. Zero is a real state.

- **Why not 10:** `onb-drift` animates `margin-left` — a layout-thrashing property — for the indeterminate drift; the laws' own motion spec prefers transforms, and animating margin on an infinite loop is the kind of thing that janks on low-end devices. Also minor: the celebrate keyframe's final state leaves a residual gold box-shadow — fine, but the "then calm" is a soft glow, not full calm.
- **Fix:** drive the indeterminate drift with `transform:translateX` instead of `margin-left`.

---

## Rollup

| Family | Score | 9.5+ blocks | Below the bar |
|---|---|---|---|
| Calendar | **9.2** | CAL-001, CAL-005 | CAL-002, CAL-003, CAL-004 |
| Checkout | **8.9** | — | PAY-001, PAY-002, PAY-003, PAY-004, PAY-005 |
| Comments | **8.8** | — | CMT-001, CMT-002, CMT-003 |
| Chat | **9.0** | CHT-004 | CHT-003, CHT-005 |
| Onboarding | **9.0** | — | ONB-001, ONB-002, ONB-003 |

**Blocks at 9.5+ (3 of 19):** CAL-001, CAL-005, CHT-004.
**What remains below the bar (16 of 19):** everything else — the fixes are small, concrete, and listed per block above. No block scored below 8.5; none is structurally unsound. The dominant pattern: **wave-2 never got Phase 1's `.naya-btn` conversion** (CMT-001, ONB-002, and the quiet-control proliferation in CMT-002), and **prose/code mismatches** (CHT-004's keepalive, CHT-005's block reference, ONB-001's skip control, CHT-003's grouping specimen).

**Cross-family follow-ups for the next fixer seat (not scored, flagged):**
1. `DESIGN/BLOCKS.md` catalog (lines 1280–1292) still describes pre-fix gold-today — sync to the white-hot chrome disambiguation.
2. `.naya-btn--quiet` needs one canonical home at catalog level (PAY-003 defines it, PAY-004 consumes it; CMT-002 and ONB-002 run their own quiet idioms).
3. `.naya-btn` DNA is copy-pasted per file — needs a single-source rule.

---

*Scored 2026-10-16 by VERIFY / Chi (Team Nitro). Independent read — no Phase 1 summary was trusted; every file above was read in full before scoring. A seat never verifies its own work.*
