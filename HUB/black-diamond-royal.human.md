# Black Diamond Royal Interface System

**STATUS: PROPOSED — awaiting Shawn's ratification. Not law yet. Nothing here is installed, enforced, or binding until he says so.**

---

Shawn, your old Human Maximus work contained a complete button and interface design system — exact, not vague. Nothing like it exists in the brain today. This is the proposal to make it the canonical design standard for NayaNET.

## What "elite" means (the definition)

Your own words from the material:

> "A beautiful interface is not elite merely because it looks expensive. It becomes elite when people instantly understand what it is, what to press and what happens next."

That sentence becomes the test. Every design scorecard asks exactly this: does the person get it instantly — what it is, what to press, what happens next? If not, it's not elite yet, no matter how expensive it looks.

## The six-layer button (plain words)

Every important button is built like a physical object rising from the screen — six layers, bottom to top:

1. **Deep base** — black glass (sometimes deep purple glass, or diamond white)
2. **Metallic frame** — a platinum edge (a whisper of gold, only for luxury moments)
3. **Inner rim** — a thin line of purple or white light just inside the edge
4. **Raised face** — a gentle bevel or gradient, so it has physical depth
5. **Top highlight** — a brighter reflection near the top edge, like light catching it
6. **Shadow + aura** — a dark drop shadow beneath, plus a restrained purple glow around it

The target feeling, in your words: *"That is a button. I want to press it."*

## The five button families

- **Royal Purple Primary** — the single strongest action on screen (Play, Resume, Begin Journey, Continue). Bright amethyst melting into deep violet, white text, platinum edge, purple aura. Never two of these in the same area — it must be the obvious star.
- **Black Diamond Primary** — strong but quieter (Install App, Explore, Share, Menu). Glossy black, white text, platinum edge, subtle purple glow inside. The most versatile family.
- **Diamond White Conversion** — money/access actions (Unlock, Join, Log In, Start Free Trial). White face, black text, purple icon — the white separates the financial moment from the dark interface.
- **Black Utility** — small round controls (prev/next, rewind, volume, close). Black glass, circular platinum edge, purple or white icon.
- **White Utility** — used sparingly, only when a dark button won't read on the background.

## Five states, every control, no exceptions

Default (clearly clickable) → Hover (lifts 2–3 pixels, glow grows, reflection brightens) → Pressed (pushes in 1–2 pixels, darkens) → Active (brighter border + an icon change or indicator — never color alone, so colorblind users aren't left out) → Disabled (visibly quiet, no glow, no lift, clearly inactive). Last build was hover-only thinking. This closes that gap.

## The locked rule

**No important action may ever use a generic flat browser-style button.** Every future major action uses one of the five families. This is the discipline that keeps the interface from sliding back into generic.

## The exact colors

The HMC standard locks these values — this proposal adopts them as the single source of truth:

- Obsidian Black `#050507` — the foundation
- Black Glass `#0C0C11`
- Deep Violet `#26143D`
- Naya Purple `#8B3DFF` — intelligence, frequency, Naya
- Electric Amethyst `#B57CFF`
- Diamond White `#F8F7FB` — primary text, clarity
- Platinum `#C9C6D0` — structure, edges
- Warm Gold `#D8B978` — sparingly; premium highlights only

One conflict I need your eye on: the standing color standard says purple is accent and glow only — never a solid fill. But the Royal Purple Primary family has a purple face. The proposed reconciliation: the Royal Purple Primary is the *one* exception — it's a gradient, never a flat fill, and it's reserved for the single strongest action in an area (never two in one area). Everywhere else, purple stays as glow and accent. If you want the hard line instead (no purple faces at all), say so and the family gets re-specced.

Two token values move under this proposal: the current Hub purple `#9d75ff` → `#8B3DFF`, and the current gold `#e8c766` → `#D8B978`. Everything else (the 12-color spectrum, the room theme colors) stays untouched.

## Shape and type discipline

Major buttons: 18–24px corners, 48–58px tall on desktop, 52–64px on mobile. Containers 18–24px, cards 16–20px, pills fully rounded. Play is a perfect circle, bigger than its neighbors, with a layered rim. Touch targets 44–48px minimum — thumbs, not just mouse cursors. Button labels: bold, major commands in ALL CAPS, 2–3 words max ("INSTALL APP", "PLAY NOW"). No tiny thin text.

## What this would change if you ratify it

1. The six-layer formula becomes the required build recipe for every major control — the existing Hub Button Law and Living Depth Law get extended, not replaced.
2. The locked rule goes live: flat generic buttons on important actions become spec violations, enforceable in review (and later in CI).
3. Palette canonicalization: identity.html's near-miss values (`#010103`, `#a855f7`) map onto the HMC standard hexes above.
4. The Elite Interface definition ("what it is, what to press, what happens next") becomes the standing design scorecard test.

## Source

Distilled 2026-10-06 from your legacy library (`~/workspace/distillations/hmc-batch-1/`, the HMC Button Spec and HMC Standard PDFs). Machine twin: `black-diamond-royal.machine.json`. Builder instructions: `black-diamond-royal.ai.md`. All three carry the same truth — PROPOSED, awaiting your word.
