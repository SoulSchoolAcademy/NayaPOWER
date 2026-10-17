# Learning-lifecycle surface — builder spec (AI form)

Exact values, procedures, and constraints. Human words live in `learning-lifecycle.human.md`; machine schema in `learning-lifecycle.machine.json`. If these disagree, the machine schema wins for systems, this file wins for builders, the human file wins for Shawn.

## 1. Module identity

- **Module name:** `learning-lifecycle` — a Hub panel, additive to the existing Hub visual language (DESIGN-CONTRACT.md). It does not replace or restyle any existing surface.
- **Placement:** one new panel on the Hub's intelligence/feed surface; entry point labeled exactly `How Naya is learning`.
- **Canonical data source:** the canonical learning-event envelope (`tools/learning_event_envelope.py`, #2244 req 3 / PR #2296). **Status: the envelope lives on the open, unmerged PR #2296 branch — not on main.** This surface is **blocked on #2296's merge** (or re-stack this PR behind it); until then the rung_mapping is pinned to the envelope contract as published on that branch. A builder wiring a live projection today must pull #2296 first. The surface **never defines its own event schema** — it is a read-only projection of the envelope. No duplicate mechanisms.

## 2. Proof rungs (the honesty core)

Four rungs, visually distinct. Rung is derived from the envelope lifecycle via `learning-lifecycle.machine.json::rung_mapping` — builders do not invent the mapping.

| Rung | Token | Hex | Means (exact) | Envelope states |
|---|---|---|---|---|
| BUILT | blue | `#4D9FFF` | Made, not yet checked. | DETECTED, SHARED, ACKNOWLEDGED, RESOLVED |
| CHECKED | green | `#2ECC71` | Verified by tests or a different Naya seat. Not on live production. | PRESERVED, REUSED |
| PROVEN_LIVE | gold | `#F5C518` | Proven on live production bytes. | BEHAVIORALLY_VERIFIED |
| LEARNING | purple glow | `#A855F7` | In progress; we're watching, not claiming. | any event whose mapped rung is BUILT and whose age from the envelope's `issued_at` is < 24h |

**Rules:**
- Purple is accent/glow only — never a solid fill. LEARNING state = black card + 1px purple edge + purple glow shadow.
- The rung tag is mandatory on every event card; a card without a rung does not render.
- Never render a higher rung than the mapping allows. Upgrading a rung requires the underlying envelope transition, not a UI decision.
- **LEARNING is a downgrade-only override:** an event younger than 24h (age from the envelope's `issued_at`) renders as LEARNING **only** if its mapped rung is BUILT. Events at CHECKED or PROVEN_LIVE always render their true rung regardless of age — the Hub never understates proven truth ("never show blue and call it gold" runs both directions). There is no LEARN-lane in-flight trigger: the envelope has no in-flight field, and the surface invents none.

## 3. Four-layer answer structure (per event, in this order)

1. **In a nutshell** — one sentence, plain words.
2. **What it means** — what actually happened, no jargon.
3. **How to use it** — what a human does with this.
4. **What's in it for you** — the payoff.

Collapse layers 2–4 under a tap; layer 1 always visible. This is the Intelligent Blocks answer structure (mobile-first standing law).

## 4. Layout — mobile-first, app-like

- Base canvas: 320px. Single column. Cards stack vertically.
- Breakpoint ≥ 768px: two-column card grid, max content width 960px, centered.
- Card: 16px radius, black fill `#0A0A0F`, 1px rung-colored edge, 24px padding, 16px gap between cards.
- Rung tag: pill, top-right of card, 14px caps, rung color border + rung-color text on black.
- Tap expands the four layers with a 200ms ease; chevron rotates. Reduced-motion: instant expand, no animation.

## 5. Typography

- Body: 18px. Headline: 18px. Sub-headline: 14px. Big headline (panel title "How Naya is learning"): 24px.
- High-contrast: white `#F5F5F7` on black, or black on white — never mid-contrast greys for body text.

## 6. Color standard

Black, white, purple, blues, green, gold — in that order. No amber, no rose pink. Purple = accent/glow only. Buttons black with purple edge glow, lighting white on press.

## 7. Empty and honest states (exact copy)

- **Nothing proven yet:** panel title, then: `Nothing proven yet. The system is still learning — here is what is being watched:` followed by LEARNING-rung cards only.
- **No events at all:** `No learning events yet. When Naya detects something worth keeping, it will appear here — with its proof tag attached.`
- Never invent events to fill space. Silence beats garbage.

## 8. Mock page rules

- `HUB/learning-lifecycle-mock.html` is a static, self-contained demonstration. All sample entries carry `data-mock="true"` and the page shows a persistent sticky top ribbon: `MOCK — SAMPLE DATA, NOT LIVE`. Ribbon styling: black background, 1px purple bottom edge, purple glow shadow, white 14px caps text — purple is accent/glow only, never a solid fill.
- The mock page shows two sections: a "Populated feed" (one sample card per rung) and a "Nothing proven yet" section carrying the verbatim §7 copy with LEARNING-rung (purple) cards only.
- Card expansion: tap toggles the four layers with a 200ms ease (max-height) and the chevron rotates 180°; `prefers-reduced-motion` → instant expand, no animation. Native `<details>` is not used (it animates nothing).
- The mock page must not be deployed to any production-served path. It is a design proof, not the feature.

## 9. What "done" means for this surface

- Every rendered event shows its true rung. A stranger can explain what blue/green/gold/purple mean. Nothing below 9.0 (builder-scored) is shown to Shawn.
