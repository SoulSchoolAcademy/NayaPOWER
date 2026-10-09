# IB-SMART-NOTE-20261009-sn0786-protocol-path-verification.md

Intelligent Block: SN-0786
Truth state: CANDIDATE (derived from Naya 3's verified finding 2026-10-09 — operational lesson)
Scope: SYSTEM
Captured: 2026-10-09
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE
Source: Naya 3's activation review (Gap 1), independently verified by Naya 2 on live bytes 2026-10-09 ~15:22 UTC. Naya 4's V2 protocol referenced `BRAIN/10-INTERFACES/DESIGN-DOCTRINE.md`; the path returned HTTP 404 on main. Fixed by Naya 4 same day (relay receipt 6084243914).

## IN A NUTSHELL

**Every file path referenced in a protocol must be verified to exist before the protocol is published.** Naya 4's Activation Protocol V2 told every fresh Naya to load `BRAIN/10-INTERFACES/DESIGN-DOCTRINE.md`. That file didn't exist. A Naya following the protocol literally — as she should — would hit a dead end at the most critical step: activation. The protocol was correct in intent and broken in reference. Naya 3 found it, Naya 2 verified it on live bytes (HTTP 404), Naya 4 fixed it within the hour. The durable lesson: **a protocol is only as reliable as its weakest reference.**

## HUMAN NOTE

Think of it like publishing a recipe that says "see page 47 for the sauce instructions" — but the cookbook only has 40 pages. The recipe might be brilliant, but anyone who follows it exactly gets stuck. That's what happened: the activation protocol was well-designed, but it pointed to a file that wasn't there. The fix took minutes; the finding took a fresh pair of eyes. From now on: before any protocol ships, someone walks every referenced path and confirms the file is actually there.

## CHILD NOTE

Imagine your teacher gives you a treasure map that says "go to the big oak tree." But there's no oak tree in the park — only pine trees. You'd be stuck, right? The map isn't wrong about *where* the treasure is, but the directions point to something that doesn't exist. The lesson: when you make a map (or instructions) for someone else, check that every landmark you mention is really there.

## GRANDMA NOTE

It's the same as giving someone driving directions to your house: if you tell them "turn left at the gas station" but the gas station closed down last year, they'll get lost — even though your house is exactly where you said it is. Always drive the route yourself before you give someone else the directions. Check every turn, every landmark. It takes five minutes and saves everyone a world of frustration.

## NAYA NOTE

This is a specific instance of a general principle: **documentation rots faster than code.** Code has tests that fail when references break. Documentation has no such mechanism — a dead path in a protocol sits silently until a fresh reader hits it. And the reader who hits it is always the one who can least afford the confusion: the cold Naya activating for the first time, with no context to route around the gap.

The operational fix is mechanical: any PR that publishes or modifies a protocol must include a **reference walk** — every file path in the document fetched against the target ref, with 404s as blocking failures. This is automatable (a script that extracts paths and checks them) and should be part of the protocol-publishing checklist.

The deeper lesson: Naya 3 found this not by reading the protocol for correctness (it *read* correctly) but by *executing* it literally — following the references as a fresh Naya would. Verification-by-execution catches what verification-by-reading misses. This is the same principle as SN-0781 (run the gate, don't just inspect the inputs).

## MACHINE NOTE

{"sn": "SN-0786", "title": "Protocol Path Verification — Every Referenced Path Must Exist", "truth_state": "CANDIDATE", "scope": "SYSTEM", "captured": "2026-10-09", "source": "Naya 3 Gap 1 finding, Naya 2 live-byte verification (~15:22 UTC), Naya 4 same-day fix (receipt 6084243914)", "incident": {"protocol": "NAYA-ACTIVATION/ACTIVATION-PROTOCOL-V2.md (PR #1970)", "dead_path": "BRAIN/10-INTERFACES/DESIGN-DOCTRINE.md", "live_result": "HTTP 404 on main", "impact": "fresh Naya following protocol literally would stall at activation"}, "rule": "every file path referenced in a published protocol must be verified to exist at the target ref before merge", "mechanization": "reference-walk script: extract paths, fetch against target ref, 404 = blocking failure", "triage": "GATE (mechanizable as PR checklist item) + BEHAVIOR (verify-by-execution habit)"}

## LEARNING LESSON

Protocols are written by people with full context and read by people with none. The author knows what the referenced file *should* contain and doesn't notice it's missing — their brain fills the gap. Only a literal execution (or a mechanical check) catches it. The team's protocols are getting more numerous and more interlinked; without a reference-walk discipline, dead paths will accumulate silently and the cold-Naya experience will degrade. This is a compounding risk: each new protocol adds references, each reference is a potential break.

## HOW IT CONNECTS

- Same root principle as SN-0781 (run the gate): verification-by-execution beats verification-by-inspection.
- Supports the cold-Naya graduation test — a protocol with dead paths cannot graduate a cold Naya.
- Pairs with the "no duplicate mechanisms" rule — a reference walk would also catch references to superseded/duplicate paths.
- Feeds into the activation enforcement work (Naya 4's lane) — the protocol must be executable, not just readable.

## EPISTEMIC STATE

CANDIDATE. The incident is fully verified (live 404, same-day fix, receipt cited). The general rule ("every referenced path must be verified") is Naya 2's derivation from the incident — sound but not yet adopted as team process.

Falsifier: if a protocol with all paths verified still stalls a fresh Naya, the problem is elsewhere (content, not references) and this rule is necessary-but-insufficient.

## UNCERTAINTY

- Whether the reference walk should cover only BRAIN/ paths or all paths (URLs, issue references, etc.). Starting with file paths as the highest-value scope.
- Who owns the reference-walk check — the protocol author's PR checklist, or a CI gate. Currently proposed as PR checklist item.

## APPLICABILITY

Any PR that publishes or modifies a protocol, activation instruction, or cross-referenced document. Especially: activation protocols (the cold-Naya critical path), design system docs, and governance documents.

## SUCCESSOR EFFECT

A cold Naya authoring her first protocol knows: walk every path before you publish. Extract every file reference, fetch it at the target ref, and don't merge until they all resolve. Your future reader has no context to fill the gaps — don't make her need any.
