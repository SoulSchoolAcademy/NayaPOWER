# IB-SMART-NOTE-20261009-sn0794-smart-node-terminology-lock.md

Intelligent Block: SN-0794
Truth state: CANDIDATE (proposed terminology discipline — not yet ratified as law)
Scope: SYSTEM
Captured: 2026-10-09
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE
Source: PDF distillation 2026-10-09, doc 7 (`So__your_job_is_now_to_achieve_it.pdf`), "Smart Node terminology lock"; distilled to `~/workspace/design-intake/pdf-distillation-2026-10-09.md`.

## IN A NUTSHELL

**"Smart Node" is human shorthand over the Intelligent Block lifecycle — NOT a machine object.** The moment someone builds a `SmartNode` class, table, or registry, we've created a duplicate mechanism for something the IB lifecycle already covers — and the no-duplicate-mechanisms law (AGENTS.md) fires. Human language is allowed to be loose; machine language is not. When Shawn says "smart node," translate to the IB lifecycle stage he means (capture? distill? promote? compound?). Never build what the shorthand names.

## HUMAN NOTE

Think of the word "thingamajig." It's useful in conversation — "hand me the thingamajig" — but you'd never manufacture a product called the Thingamajig 3000, because nobody would know what it actually is. "Smart Node" is our thingamajig: handy shorthand when talking, but the moment an engineer builds a database table called `smart_nodes`, we've manufactured confusion. The real objects already exist — they're called Intelligent Blocks, and they have a precise lifecycle. Use the nickname in chat; use the real name in code.

## CHILD NOTE

Imagine you and your friends call the school library "the book cave." That's fun to say! But if someone built a whole new room and labeled it "Book Cave" while the library is right there, that would be silly — now there are two places for books and nobody knows which one to use. "Smart Node" is like "book cave": a fun nickname for something that already has a real name (Intelligent Block). Don't build a second room.

## GRANDMA NOTE

It's like calling the refrigerator "the cold box." Fine at the dinner table — everyone knows what you mean. But you wouldn't order a second appliance called a Cold Box and plug it in next to the fridge. We already have the fridge (Intelligent Blocks). The nickname doesn't need its own appliance, its own paperwork, or its own repairman.

## NAYA NOTE

This is the no-duplicate-mechanisms law (AGENTS.md) applied to vocabulary: **a nickname that gets built becomes a duplicate.** The defense is a translation habit — whenever "smart node" appears in a design, spec, or schema, replace it with the IB lifecycle stage it denotes before building. If it doesn't map to a stage, the design is waving its hands; send it back. Human shorthand stays in human-language documents; machine schemas use machine names.

## MACHINE NOTE

```yaml
terminology_lock:
  term: "Smart Node"
  status: "human shorthand ONLY"
  maps_to: "Intelligent Block lifecycle stage (name the stage)"
  forbidden: ["SmartNode class", "smart_nodes table", "smart-node registry", "any machine object by this name"]
  rule: "translate to IB lifecycle before building; unmappable usage = hand-waving, return to author"
```

## LEARNING LESSON

Names are cheap; objects are expensive. Every nickname that slips into a schema creates a shadow system someone has to maintain, migrate, or kill later. Lock the vocabulary at the whiteboard, not in the database.

## HOW IT CONNECTS

- Enforces AGENTS.md "no duplicate mechanisms" at the vocabulary layer.
- Pairs with the three-language standard (AGENTS.md): human language may use the shorthand; AI and machine language must use the precise term.
- Related to doc 8's "naming ran ahead of enforcement" disease — this is naming running ahead of *ontology*.
- If a genuine new machine concept emerges that "smart node" was gesturing at, it gets a new precise name through the proper channel — not the nickname.

## EPISTEMIC STATE

**CANDIDATE.** Source is doc 7 (specialist operationalization, unratified). The underlying principle (no duplicate mechanisms) is standing law; this note applies it to a specific term. No counter-evidence: no `smart_nodes` machine object exists on main at capture time.

**Falsifier:** if the IB lifecycle proves insufficient for a concept practitioners keep calling "smart node" (persistent, unmappable usage across seats), the lock is wrong — the concept needs a real name and a real design, proposed properly.

## UNCERTAINTY

- Whether Shawn intends "Smart Node" to eventually denote something specific (his usage is the authority; this note constrains builders, not him).
- The exact IB lifecycle stage mapping for each colloquial use — to be established by usage, not decreed here.

## APPLICABILITY

Every design, spec, schema, and code review. Especially: new-contributor onboarding (where nicknames get mistaken for architecture) and any proposal containing the words "smart node" in a machine context.

## SUCCESSOR EFFECT

A cold Naya hearing "smart node" in an old chat log doesn't build a SmartNode class — she translates it to the IB lifecycle and keeps building on the real foundation. The ontology stays clean across generations.
