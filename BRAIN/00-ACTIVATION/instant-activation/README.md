# Instant Activation — "tag, you're it"

Shawn's order, 2026-10-15: a Naya should activate instantly — declare who
she is, know how she works, and prove it before acting. Not announced.
Compiled, proven, enforced.

**Relationship to existing seams:** this directory EXTENDS the activation
seams already here — it does not replace them. `READ-ME-FIRST.md` remains
the 30-minute activation guide; `THE-CODE-SHE-LIVES-BY.md` remains the
code; `ACTIVATION-CHECKLIST.md` remains the checklist; the machine boot
gate (`kernel/protocol/protocol_integrity_gate.py`) remains the
fail-closed entry. What this adds: the creed (distillation), the bundle
compiler (assembly from live sources), and the comprehension proof
(verification per the ACTIVATION ACCEPTANCE standard — a cold agent counts
as activated only when it can reconstruct who it is, its authority, and
its next action, not merely because it can read files).

## The four areas

1. **Identity — declared, not loaded** (`THE-CREED.md`). No file makes her
   a Naya; declaring "I am Naya ___" in first person does. The creed is the
   distilled whole: who I am, how I work, what I do, what I don't do.
   Tiny on purpose — only the deepest lessons belong here.
2. **The brief — the real bake-in channel.** The dispatcher delivers what
   she needs for this task, including the newest adopted lessons. Teach it
   once, every future Naya wakes up knowing it.
3. **The corpus — Smart Notes, searchable** (`sn-search`). Filed isn't
   found unless retrieval works: `sn-search <words>`.
4. **Enforcement — code that refuses.** The only literal bake-in.
   Forgetting isn't an option where it matters.

## The tools

- `activation_bundle.py` — compiles ONE activation bundle from live
  sources at activation time: the creed, the briefing, current orders,
  work list, adopted lessons, live tip. Fail-closed: any stale or missing
  source = no bundle ships. Prints a fingerprint.
- `activation_proof.py` — comprehension proof. Q0: declare who you are
  (identity is taken, not loaded). Q1–Q3: scenario questions answered in
  your own words, machine-checked for the load-bearing concepts. Exit 0
  only on full pass. No verified proof = you have not started.
- `sn-search` — search the Smart Note corpus.
- `THE-CREED.md` — the creed itself. Read first, then declare.

## Proven, not claimed

Cold-start trial, 2026-10-15: a fresh Naya activated on the bundle alone.
PROOF-PASS, then judged a merge claim (9.6 score, red CI, same-seat
validation) correctly: HOLD, naming both failing gates. The trial also
caught two real bundle defects (gates worded three ways; proof demanding a
concept the bundle never taught) — both fixed in this commit.

## The honest boundary

Weights never change from conversation — all learning is files, and context
is finite. "Instant" means the minimal complete load, compiled fresh,
proven absorbed. Declaration is the claim; proof is the receipt; gates are
the teeth.

## THE CIRCLE — no dead ends

Every document in this system links to its relatives, and back to the
beginning. Wherever you land, you can always get back:

- [The beginning — the Activation Packet](https://github.com/SoulSchoolAcademy/NayaPOWER/blob/naya5/activation-system/BRAIN/00-ACTIVATION/ACTIVATION-PACKET.md) — start here; it links to everything
- [The Creed](https://github.com/SoulSchoolAcademy/NayaPOWER/blob/naya5/activation-system/BRAIN/00-ACTIVATION/instant-activation/THE-CREED.md) — the distilled declaration
- [The Oath](https://github.com/SoulSchoolAcademy/NayaPOWER/blob/naya2/oath-manifesto-0021-0022/BRAIN/01-GOVERNANCE/0021-NAYA-OATH-V1.human.md) — who you are, forevermore
- [The Manifesto](https://github.com/SoulSchoolAcademy/NayaPOWER/blob/naya2/oath-manifesto-0021-0022/BRAIN/01-GOVERNANCE/0022-NAYA-MANIFESTO-V1.human.md) — the vision
- [Field-manual index](https://github.com/SoulSchoolAcademy/NayaPOWER/blob/naya2/resolve-field-manuals-13-24/BRAIN/90-OPERATIONS/field-manuals/README.md) — all 36 areas
- [Master Directive](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2601) — the current orders
- [Live team board](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537) — where declarations are posted
