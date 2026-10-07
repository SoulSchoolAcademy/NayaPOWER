# Intelligent Block: SN-0450
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
Tap-feedback gaps are measurable by selector scan; the contract-conformant repair is press compression plus white indicator, never color.

## HUMAN NOTE
The ratified design contract says hover ignites color but active/selected is a subtle white indicator only — no permanent color glow. The standing mobile-first law says taps must feel alive. A regex scan of the shipped Hub build found 23 of 28 hoverable bases had no :active/:focus feedback at all — touch users got nothing on press. The repair form that satisfies both laws: press compression (scale .97, translateY reset) plus a faint white inset shadow. Never color on active. Additive-only CSS block, no existing rule touched.

## CHILD NOTE
When you poke a button with your finger, it should squish a little and whisper "got it" — in white, never in party colors.

## GRANDMA NOTE
If it lights up when you hover, it should answer when you tap. A quiet little nod, not fireworks.

## NAYA NOTE
This reconciles two standing laws that look like they conflict: mobile-first ":active mirrors :hover" vs contract "active = white indicator only." The resolution: active exists on every hoverable (mobile law), but in white (contract law). Both hold. Record the reconciliation so no future seat re-fights it.

## MACHINE NOTE
{"sn":"SN-0450","category":"SYSTEM-DESIGN","sub":"INTERACTION-STANDARDS","evidence":["HUB/app/index.html @ 0a1353bc","28 hover bases, 5 with :active/:focus, 23 repaired","PR #1591, commit 14f07813"],"related":["SN-0449"],"admission":{"durable":true,"new":true,"signal":true,"evidence_backed":true}}
