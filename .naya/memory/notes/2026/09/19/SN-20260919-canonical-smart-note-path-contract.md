---
id: SN-20260919-canonical-smart-note-path-contract
type: governance / lesson
status: CANONICAL
date: 2026-09-19
canonical_path: NayaPOWER/SMART-NOTES/2026/09/19
repository_path: .naya/memory/notes/2026/09/19/SN-20260919-canonical-smart-note-path-contract.md
---

# Smart Note Contract: One Canonical Resolver

## In a Nutshell

A distributed intelligence system cannot safely remember knowledge if different Nayas store the same kind of knowledge in different places.

**One Smart Note → one canonical resolver → one authoritative repository artifact.**

The stable logical namespace is:

`NayaPOWER/SMART-NOTES/YYYY/MM/DD/`

The current physical repository location is:

`.naya/memory/notes/YYYY/MM/DD/`

The logical namespace and physical path are two representations of the same canonical location, not two competing Smart Note systems.

## Human

Today's path conflict taught us that even when everyone agrees on the concept of a Smart Note, different agents can create incompatible locations if the storage rule is not explicit enough.

The lesson is bigger than folders:

**Canonical intelligence requires canonical names, canonical locations, and canonical contracts.**

The goal is to make the correct location obvious to every future Naya without relying on conversation memory.

## Grandma

If the family keeps important recipes, don't let every person invent a different cupboard.

Choose the cupboard.

Put the recipe there.

Tell everyone where it is.

Then everybody can find the same recipe tomorrow.

## Child

Imagine everyone in a classroom has a box for important drawings.

If one person puts drawings in the blue box, another uses a red box, and another hides them under the desk, nobody knows where to look.

So we make one rule:

**Important drawings go in this box.**

Smart Notes need the same kind of simple rule.

## Naya

The canonical resolver is deterministic:

`Smart Note date → .naya/memory/notes/YYYY/MM/DD/`

For 2026-09-19:

- Logical namespace: `NayaPOWER/SMART-NOTES/2026/09/19/`
- Physical repository: `.naya/memory/notes/2026/09/19/`
- Filename convention: `SN-YYYYMMDD-[short-human-readable-slug].md`

A legacy or conflicting location must not become a second canonical system. Preserve historical artifacts where required, then reconcile current references and retrieval to the resolver.

No future Smart Note operation may invent or substitute another physical directory.

## Machine Contract

```text
resolveSmartNotePath(date):
  year  = YYYY
  month = MM
  day   = DD

  logical_path  = NayaPOWER/SMART-NOTES/YYYY/MM/DD/
  physical_path = .naya/memory/notes/YYYY/MM/DD/

  return {
    logical_path,
    physical_path
  }
```

Canonical filename:

`SN-YYYYMMDD-[short-human-readable-slug].md`

## Hard Prohibition

Do not create new canonical Smart Notes under:

- `.naya/SUPERBRAIN/SMART-NOTES/`
- `.naya/notes/`
- `.naya/memory/events/`
- any newly invented Smart Note directory

Those paths do not become canonical merely because a previous Naya used them.

## Why This Matters

A single resolver prevents:

- scattered Smart Notes;
- duplicate truth;
- retrieval ambiguity;
- agents disagreeing about where today's intelligence lives;
- broken day/month/year navigation;
- unnecessary migrations and competing memory systems.

It also makes the Smart Note system testable:

**CREATE → RESOLVE → PERSIST → INDEX → RETRIEVE → VERIFY**

## Governance

The resolver is governed by:

`SUPERBRAIN/NAYA-REPOSITORY-OPERATING-STANDARD.md` §19.1.

That operating standard is the governing contract. This Smart Note preserves the lesson and makes the rule reusable intelligence for future Nayas.

## Acceptance / Truth State

**VERIFIED:** The canonical resolver has been recorded in the repository operating standard and exposed in the README authority map.

**VERIFIED:** This Smart Note is stored at the physical path produced by the resolver.

**UNKNOWN:** This documentation change alone does not prove that every runtime Smart Note creation/retrieval code path has already been mechanically routed through one implementation-level resolver. That requires source/runtime inspection and proof.

**Principle:** Do not claim the runtime is unified until the runtime proves it.

**END — SMART NOTE**
