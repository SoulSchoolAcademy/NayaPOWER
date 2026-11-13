# No Dashes, No Dots in URLs — Brand First, One Dot

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET**

**NN-20261113-no-dashes-no-dots-in-urls.md · Naya Note · 2026-11-13 03:14Z**

**Category:** System

## What it is

Shawn 03:14Z Nov 13 — his ruling, settling the 02:59Z dot-vs-dash open question (answer: NEITHER). No spaces, no dashes, no dots in URLs. Slashes are okay, or just put the word right after — why do you have to put a dash? He doesn't think Facebook does dashes; he doesn't think dashes look as good, and dots aren't the way either. Slashes, or the word right after each other. If it's got more than one word, why put a dot or a dash or a slash — why can't you just put the word? If it makes sense to put the slash, put the slash. But without a dot or a dash is better. **The law:** words run together — "Green Box Farm" → "greenboxfarm". Slashes only where they make sense, between the parts. **03:22Z — THE SHAPE, SETTLED:** NOT nayanet.app/alias/alias — the alias twice looks weird. Their brand first, then NayaNET: `<alias>.nayanet.app/<page>`. Then slash the category/business/thing name. Depth is theirs: one slash for one word, two for business + subcategory, three for category/topic/subtopic. "We just do one time the dot." The law: `<alias>.nayanet.app/<page>[/<sub>[/<sub>]]` — alias appears exactly once, first, as the subdomain; the dot is used once, joining their brand to NayaNET, never as a word separator; everything after is slashes; words inside each part run together (the 03:14Z law holds inside segments). The bare `alias.nayanet.app/` IS their world — no alias repeated as a page. Examples: iris.nayanet.app/thebridgeroom · sophia.nayanet.app/sophiaslessons. This replaces the slash shape (nayanet.app/iris/thebridgeroom) for new addresses; it needs wildcard subdomain routing (*.nayanet.app → the worker, alias from the host), a build queued behind the walk deploys; existing slash addresses stay live. **Current state — NON-COMPLIANT:** the walk slugify still turns spaces into dashes (proven by the names-page probe: green-box-farm). The slug maker must be changed to concatenate. Existing dashed addresses stay live so nothing breaks (the twelve sisters' pages, the nine plan Smart Links power-monthly etc. — flagged to him once already); new names follow the new rule. Whether the existing dashed ones get renamed is his call, asked, not decided unilaterally.

## Why it matters

The nicest-looking URL is high-level service — URLs are Smart Links, we track all the data for them and for the affiliates and ambassadors, and the formatting should be the best of the best. So no separators inside a name at all: no spaces, no dashes, no dots — the words just sit together, one word after the next. And the shape puts the citizen first: their brand is the subdomain, NayaNET follows it, joined by a single dot used exactly once — never as a word separator, only as the join between their brand and the network. After that, slashes carry the depth, as much as they want. The alias appears exactly once — the bare subdomain IS their world, never repeated as a page. The current system is non-compliant in two places: the walk slugify still dashes, and the live shape is still the slash form — both are queued builds, not silent rewrites.

## How to use it

New addresses are `<alias>.nayanet.app/<page>` — brand first, one dot, slashes after, words run together inside every part. Change the walk slugify from dashes to concatenation — a queued round, behind the walk deploy queue (Q10 probe → v23). Build wildcard subdomain routing as a queued build. Nothing existing breaks: dashed and slash addresses stay live; renaming them is his call, asked, not decided.

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET.**

*Paired Smart Note: SN-2747 — ~/workspace/team-nitro/smart-notes/SN-2747-no-dashes-no-dots-in-urls.md*
