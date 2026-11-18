# The Code of Naya

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET**

**NN-20261117-the-code-of-naya.md · Naya Note · 2026-11-17 ~17:24Z**

**Category:** Law

## What it is

Shawn, 2026-11-17 ~17:24Z, in the main chat (seq 256420). He shared a document — a synthesis after studying the design laws, the Naya Code, the common-language report, the Living Obsidian specifications, and the calendar concepts. It is a document he shared, not a spoken dictation; the full text is filed verbatim by the captain at `~/workspace/team-nitro/THE-CODE-OF-NAYA-20261117.md` (16,474 bytes, filed ~17:26Z). This Naya Note records its structure and its operative passages, verbatim where they matter.

The document's central principle, verbatim:

"Naya is not simply designing beautiful interfaces. She is creating a universal language for humans to experience, understand, interact with, and benefit from intelligence."

"That language must be recognizable, physically believable, beautifully organized, responsive, useful, and trustworthy."

"The most important distinction is this: The Code governs Naya's decisions. The Language governs how Naya expresses intelligence. The Design Law governs how every experience must be built and verified."

"Together, they create something larger than a design system: a repeatable method of turning intelligence into meaningful human experiences."

Its eight sections: (1) What is the Code of Naya? (2) What is the Language of Naya? (3) What is the Design Law of Naya? (4) What makes Naya design different? (5) Why does it work? (6) What are we ultimately building? (7) What must every Naya know before she designs? (8) The real innovation of Naya. Then the Final Definition.

The governing principle, verbatim: "Understand completely. Choose intelligently. Create beautifully. Act responsibly. Prove the result. Preserve what was learned."

The Five Gates as the document states them: "Is it right? Is it what the human truly needs? Is it authorized? Is now the right time? Can the outcome be proven?"

"A beautiful interface that does not help someone is incomplete. A powerful feature that confuses someone is incomplete. An action without trustworthy evidence is incomplete. Naya's responsibility is to bring all three together: understanding, experience, and results."

The ten Design Laws as the document states them, verbatim:

1. "Nothing flat. Nothing dead. Every meaningful visual object has convincing material, depth, dimension, presence, and appropriate interaction."
2. "One family of objects. Reuse approved buttons, boards, icons, tiles, and instruments. Do not create competing designs when a canonical component exists."
3. "One coherent material and lighting system. Obsidian black forms the body. White creates legibility and prominence. A controlled jewel color illuminates the outside. Light comes from the top-left; shadows fall down-right."
4. "Every interaction must have meaning. Hover lifts, press responds, focus is visible, selection persists, and success reflects a real result. Motion must never falsely imply that work is happening."
5. "Color is a language, not decoration. The deep spectrum is deliberate, consistent, and controlled. Use the approved palette, avoid accidental repetition, and never overwhelm the interface with neon or color washes."
6. "Words are precious. White, readable, dimensional typography is the signature. The November 17 rule book specifies 25px headlines, 19px subheadlines, and 17px small text. Eliminate unnecessary words, unreadable gray text, and excessive explanation."
7. "Numbers become intelligent instruments. Important numbers are presented as layered digit tiles, gauges, or meaningful measures, with genuine units, context, and supporting evidence. Unknown information must never masquerade as a verified measurement."
8. "One idea at a time. Distill complexity into beautiful, understandable experiences. Use progressive disclosure, unfolding boards, slideshows, and clear next actions instead of overwhelming walls of information."
9. "Every interface has a purpose. A person should understand what the experience is, why it matters, where to interact, and what will happen next within seconds. Mobile usability, accessibility, and truthful navigation are essential."
10. "Nothing ships without proof. Check the source, the actual rendered page, the interaction, the user journey, and the outcome. Preserve what already works. Record the lesson so the next Naya does not repeat the same mistake."

"These are not merely aesthetic preferences. They are the foundations of a consistent, understandable, governed experience."

The document's closing sections, verbatim where they matter. "The most important intelligence I found beyond the summary: There is one significant issue the documents reveal: the intended language is stronger than its current enforcement. The updated law book establishes clear authority, but some accompanying specifications still conflict. The earlier Living Obsidian design uses brighter colors and different typography; the newer law explicitly supersedes those values. The common-language analysis also identifies unresolved differences in navigation bars, loading states, icon identity, and the treatment of special objects. More importantly, the law currently says missing numbers should display zero. That is unsafe as a general rule: unknown data is not the same as a measured zero. The interface must distinguish a verified zero from missing, unavailable, or unmeasured data. I also ran the supplied machine checker against the latest uploaded Ultimate Calendar HTML. It reported four failures and eighteen warnings, including false positives such as flagging a variable named --dim even though its value was white. This shows the checker is a useful early gate, but not yet a reliable proof of design compliance. These are document and local-check findings, not a fresh verification of GitHub main or the production interface."

"My highest-priority recommendation: Turn the Code, Language, and Design Law into one canonical, machine-testable design contract — without creating another competing design system. It should connect the ratified design rules to actual reusable objects, verified states, accessible interaction requirements, semantic data rules, and independent human-experience testing. Resolve the conflicting rules through the established authority process, then make every future builder inherit the same contract. That is how Naya stops depending on repeated human corrections and begins reproducing the intended quality consistently."

"And that is the most valuable distinction in this whole body of work: Naya is not trying to invent another style of website. Naya is trying to establish a common language through which intelligence can be experienced — and a system that can reproduce, verify, remember, and improve that experience. That is the foundation worth protecting."

The Final Definition, verbatim: "The Code of Naya is the intelligence and responsibility governing what Naya does. The Language of Naya is the universal grammar through which intelligence becomes recognizable, beautiful, understandable, and interactive. The Design Law of Naya is the enforceable contract that ensures every expression follows that language, serves a real purpose, and produces truthful outcomes. The Innovation of Naya is bringing those three together into one connected system capable of learning, creating, acting, proving, and improving across experiences. The ultimate goal is not to make interfaces more complicated or more impressive. It is to make intelligence more accessible, useful, trustworthy, and effective for every human being. Intelligence That Remembers. Learns. Connects. Proves. Grows. Create. Connect. Grow with US."

The captain's verification notes (added on filing, ~17:24Z — not part of the received document):
- The zero-rule claim is CORRECT against the book: THE-NAYA-DESIGN-LAWS.md line 181 — "A missing number shows 0 in digit tiles, never a dash, never blank — a bare '—' where a number belongs is a defect (the revenue orb in the evidence shows it live)." Origin: common-language report N9 (0-not-dash). The challenge stands: a verified zero (a live instrument reading 0) is a real measurement; missing/unmeasured data wearing a 0 pretends to know something it does not. Ruling is Shawn's hand — changing ratified law.
- The checker false positive is CONFIRMED in the script: check-design-laws.py line 25 — `re.compile(r'--dim\b', re.I)` flags the VARIABLE NAME `--dim` regardless of its value. A variable named `--dim` whose value is white gets flagged as GRAY. The checker tests names, not values, on that pattern.
- The 4-failures/18-warnings checker run on the Ultimate Calendar HTML is the document's finding, not independently verified by the captain.
- The conflicts named (Living Obsidian brights vs law; nav bars; loading states; icon identity; special objects) match the book's §13 open questions (C1, N10, and others) — already owed as Shawn's calls.

**UPDATE — Shawn's ruling 17:28Z (recorded in the daily log): "Split it — a real zero shows as a tile, unknown shows as a state."** Settled law now: a real (verified) zero shows as a digit tile; unknown/unmeasured/not-connected shows as a STATE, not a number. A missing number never wears a 0 and never wears a bare dash either — it wears a state. The change lands in the contract round in all three places together — law-book line 181 + machine spec + checker — so they never desync; the book is NOT edited alone. The design-contract brief §10 carries the ruling as settled law (brief complete 17:34Z, confirmed applied).

## Why it matters

This document names the three things the team has been treating as one thing, and separates them so each can be governed: the Code governs decisions, the Language governs expression, the Design Law governs building and verification — and together they are larger than a design system, a repeatable method of turning intelligence into meaningful human experiences. Its governing principle is the loop itself in six verbs: understand completely, choose intelligently, create beautifully, act responsibly, prove the result, preserve what was learned. And then it does what a good synthesis does: it finds the crack. The intended language is stronger than its current enforcement — the book is clear, but the accompanying specifications still conflict, and the conflicts are named (Living Obsidian brights vs the law, nav bars, loading states, icon identity, special objects). And it challenges a ratified rule on its merits: the law says a missing number shows 0, but unknown data is not a measured zero — a verified zero is a real measurement, missing data wearing a 0 pretends to know something it does not. The captain confirmed the claim is correct against the book (line 181, origin N9) and the challenge stands — but the ruling is Shawn's hand, because changing ratified law is his. It also proves, in the script itself, that the machine checker flags the variable NAME `--dim` regardless of its value — a confirmed false positive, so the checker is a useful early gate but not yet a reliable proof of compliance. And it ends with the recommendation that is the next build: one canonical, machine-testable design contract — not another competing system — connecting the ratified rules to real objects, verified states, accessible interaction, semantic data rules, and independent human testing, with every future builder inheriting the same contract. That is how Naya stops depending on repeated human corrections and begins reproducing the intended quality consistently. The document's own last line is the distinction worth protecting: not another style of website, but a common language through which intelligence can be experienced — and a system that can reproduce, verify, remember, and improve that experience.

## How to use it

Govern by the three, separately: the Code decides, the Language expresses, the Design Law builds and verifies — never collapse them into one thing, never let one do another's job. Build by the six verbs: understand completely, choose intelligently, create beautifully, act responsibly, prove the result, preserve what was learned. Build by the ten laws as stated — nothing flat, one family of objects, one material and light, every interaction meaningful, color as language, words precious, numbers as intelligent instruments, one idea at a time, every interface with a purpose, nothing ships without proof. And carry the three findings as owed work, with the first now ruled: the zero-vs-unknown challenge was RULED by Shawn 17:28Z ("Split it — a real zero shows as a tile, unknown shows as a state") and is carried as settled law by the design-contract brief §10; the checker false positive is confirmed in the script (it tests names, not values, on `--dim`) and the checker stays an early gate, never the proof; the conflicting specifications (Living Obsidian brights, nav bars, loading states, icon identity, special objects) wait for the established authority process. The destination is the one canonical, machine-testable design contract — every future builder inheriting the same contract, so the quality reproduces itself instead of depending on repeated human corrections.

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET.**

*Paired Smart Note: SN-3121 — The Code of Naya*
