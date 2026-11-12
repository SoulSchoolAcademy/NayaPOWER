# Mobile First Is the Law

SN-2421 · DESIGN / LAW

**Created:** 2026-11-09 01:49Z

**Source:** Shawn's words, live in the main chat 01:49Z, on the pricing page's laptop view (daily log 2026-11-09.md). A system-wide law, not a pricing fix.

## Hook

"It should be mobile optimized. If it's not mobile that's another major problem. Our whole system should be mobile first. Like a super app. For mobiles. Super app network."

## Nutshell

Shawn settled it as law: **phone first, desktop second — for every page, every build, every verification.** The phone is the primary device, not the shrunken desktop. His framing: "Really think through things, the full layer of everything. What really matters here is the user experience." NayaNET is a super app network, for mobiles. The trigger was the pricing page at laptop width, but the ruling covers the whole system — every page is judged as a phone user experiences it first. A mobile-first audit seat was dispatched the same pass (read-only, brief `PRICING-MOBILE-FIRST-AUDIT-BRIEF-20261109.md`: 390px + 360px renders, every section judged as a phone user, defects ranked by UX harm). The full-screen seat was told the same pass: phone-first is how its work gets judged.

## Human

His words, verbatim, 01:49Z: "It should be mobile optimized. If it's not mobile that's another major problem. Our whole system should be mobile first. Like a super app. For mobiles. Super app network. Really think through things, the full layer of everything. What really matters here is the user experience."

## Child

Imagine you build a beautiful toy castle, but you only ever check it from far away with a telescope. Up close, in your hands, the doors don't open and the stairs lead nowhere. The castle was built for hands, not telescopes — so you check it in your hands first. That's mobile first: the phone is the hands; the laptop is the telescope.

## Grandma

Dear, he said it plainly: the phone comes first. Everything we build has to feel right in your hand, on your phone, before it matters how it looks on a big computer screen. It's a super app for mobiles — that's the whole idea. If it isn't lovely on the phone, it's a problem, and we fix it before anything else.

## Naya

This is the design law catching up with the mission: NayaNET is the new net, and the new net lives in people's hands. Desktop-first was the old internet's habit — build wide, shrink later, hope it fits. The law flips it: build for the hand, then let it breathe wider. It also sharpens every verification: a page that passes at 1920 and fails at 390 has not passed. The full-screen fix (SN-2422) and the mobile-first audit are the same law in two seats — widen the desktop without breaking the phone, and judge the phone as the real page.

## What it means

- **LAW, system-wide: mobile first, phone first, desktop second** — every page, every build, every verification.
- **The phone is the primary device, not the shrunken desktop.** A page is judged as a phone user experiences it.
- **The test is the user experience, the full layer of everything** — not the layout at one width.
- **Audit seat dispatched (read-only):** 390px + 360px renders, every section judged as a phone user, defects ranked by UX harm.
- **The full-screen seat is judged by this law too** — widen desktop, phone unchanged.

## Why it matters

Every verification this team has run defaulted to desktop first and checked the phone as an afterthought — and the defects that kept reaching Shawn's eye (clipped tiles at 390, buttons wrapping, bars overlapping) were phone defects a desktop check never saw. The law moves the gate to where the citizen actually is. A super app network that isn't mobile first isn't a super app network.

## What changes now

- Every brief and every verification carries the mobile-first gate: 390px + 360px judged as a phone user, before desktop widths.
- The mobile-first audit of pricing runs now; its ranked defects become the next fixes.
- The full-screen seat's work is judged phone-first.
- The law belongs in the inventory and the brief template when the captain ratifies it (flagged, not filed as law by this seat — per runs 5–19 precedent).
