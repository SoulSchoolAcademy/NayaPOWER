# Redaction-Proof First — For Secret-Adjacent Claims, Counts and Hashes Before Any Render

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1609-redaction-proof-first-counts-and-hashes-before-render
**Smart Note:** SN-1609
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** learning-events-2026-10-18-23.md (run 06:20 UTC): CANDIDATE 595 (t0735-lane0, 2026-10-18) — the seat's first two reads of a secret-adjacent claim rendered `<redacted>` and it proceeded as if F1 were confirmed; the third check — a deliberately redaction-proof verification (counts/hashes, never rendering the secret) — falsified it. Violation caught and corrected this run. "Passes the bar: every secret-adjacent claim ships a redaction-proof verification rule before any plan is built on the render."

## IN A NUTSHELL

A redacted render looks like evidence but is the absence of evidence wearing evidence's clothes: the seat read `<redacted>` twice and treated it as confirmation of F1 — two renders of nothing, counted as proof. The third check deliberately avoided rendering the secret at all (counts and hashes only) and falsified the claim. Rule: for secret-adjacent byte claims, the redaction-proof check comes FIRST — and no plan, claim, or next step gets built on a render that redacts the very thing it purports to show.

## HUMAN NOTE

It's like a restaurant review that says "the food was [redacted]" — and you treat it as a five-star review. The brackets are not a rating; they're the absence of a rating. The redaction-proof check is asking the waiter "how many tables ordered it, and what did they pay?" — questions that don't need the secret menu to answer. Only after those questions come back right do you trust the claim. You never build a dinner plan on a review of a dish nobody described.

## CHILD NOTE

Someone shows you a treasure map where the X is covered with a black box, and says "the treasure is definitely buried here!" You believed them — twice! But nobody actually checked. The smart move: count the footsteps on the path, or weigh the ground — things you can check without seeing under the black box. Those checks proved the treasure wasn't there. Never believe a map you can't read.

## GRANDMA NOTE

Like a censored letter: half the lines are blacked out, and someone tells you "it says you're invited." It doesn't say that — the blacked-out parts don't say anything you can read. The honest check is counting the stamps, checking the postmark — the things the censor didn't touch. If those don't line up, the letter isn't an invitation, it's a puzzle. Never plan a trip on a letter you can't read.

## NAYA NOTE

Verification hygiene for secret-adjacent claims: (1) a rendered `<redacted>` is an UNVERIFIED claim — never treat a redacted render as confirmation of anything; (2) the redaction-proof check ships BEFORE any plan: design counts/hashes/lengths/metadata questions that answer the claim without rendering the secret (e.g. "does the secret exist," "how many," "does the hash match the expected pin"); (3) build the plan only on the redaction-proof result — a render is a courtesy, never evidence. Applies anywhere a protection layer replaces content: credential stores, redacted connectors, sanitized logs. The falsification here was lucky-late (third check); the rule moves it to first.

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1609",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-18",
  "applies_when": [
    ["claim", "secret-adjacent"],
    ["verification", "redaction"],
    ["verification", "redacted-render"]
  ],
  "enforcement": "Named verification step before any secret-adjacent claim is used: a redaction-proof check (counts, hashes, lengths, metadata — never rendering the protected value) that confirms or falsifies the claim. Rendered `<redacted>` output is classified UNVERIFIED by default; no receipt, plan, or next action may cite a redacted render as evidence of the thing it redacts. Violations get named in the sign-out as redaction-proof misses, like the t0735-lane0 correction.",
  "decision_change": "Future secret-adjacent verification decision 'the render shows <redacted>, claim holds' becomes: the render shows nothing; run the redaction-proof check first, then decide. Future planning decision 'build the next step on this redacted output' becomes: plan only on counts/hashes/metadata that the redaction cannot alter.",
  "falsifier": "If a documented case shows a redaction system whose renders preserve semantic truth for the exact claim type at hand (the redaction is proven, for that field class, to render-only-on-match — e.g. a pinned equality probe rendered through the same redactor), the redaction-proof check is redundant for that field class and this note narrows to name the proven-safe field classes.",
  "mechanism": "A redaction replaces the protected value with a fixed token before the seat can see it. Anything the seat 'reads' in the redacted position is the token, not the value — so a render can never confirm a claim about the value. Counts, hashes, and metadata flow through the redaction unaltered (or are computed outside it), so they are the only claims a seat can honestly make. Treating a render as confirmation confuses the map's censorship marks for the territory.",
  "evidence": "hidden_files/learning-events-2026-10-18-23.md (run 06:20 UTC): CANDIDATE 595 (t0735-lane0, 2026-10-18) — first two reads rendered <redacted> and the seat proceeded as if F1 were confirmed; third deliberately redaction-proof check (counts/hashes, never renders) falsified it; violation caught and corrected this run.",
  "cousins": ["SN-1601 (re-derive-line-map-after-reorder-filter — stale evidence frames)", "render-from-probe lineage"]
}
~~~
