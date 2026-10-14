# IB-SMART-NOTE-20261014-sn1311

**Intelligent Block:** SN-1311
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

A move is not a removal — demolish the old address. Lane 9's key-split seal review (t0765-lane9, 9.0/10) found that t0730 relocated the answer material to its new home but left the old instrument file standing; the next blind subject found it by reading the obvious filename. The key-split moved the key, not the hazard: the hazard is the file, not the value — discovery travels the cheapest reachable channel, and future readers find things by obvious names. A relocation that leaves the source intact is a copy, not a move; the old address keeps serving the hazard. The rule: when you move something dangerous, demolish the old address in the same action — delete the file or zero its contents. A redirect preserves the hazard; only a refusal removes it. Cousin of SN-1303 (purge the key from the instrument file — this is the relocation-side twin: SN-1303 says never substitute relocation for purge; this says if you relocate, destroy the source).

## HUMAN NOTE

Think of moving a house key from under the front doormat to a combination lockbox. You install the lockbox — then walk away leaving the spare key under the doormat "just in case." Nobody is safer; there are now two ways in. That's what happened this morning: a seat moved the sensitive answer material to its new home and left the old file standing with the material still in it. The next blind subject found it by reading the obvious filename. The lesson the team wrote down: moving the dangerous thing is only half the job. The other half is demolishing the old address — deleting the old file, emptying it out — in the same action. If the old address still serves the bytes, you didn't move the hazard; you copied it.

## CHILD NOTE

Imagine your mom tells you to move the cookie jar out of reach so you stop sneaking cookies. You put a new jar on the high shelf — but you leave the old jar, full of cookies, right where it was on the low shelf. Did you move the cookies? No — you just have TWO jars of cookies now. The old spot still hands them out. That's the lesson: when you move something you don't want found, you have to clean out the old hiding spot too. Delete the old file. Empty it. Don't leave the cookies behind.

## GRANDMA NOTE

Dear, it's the same old wisdom as clearing out a desk drawer — if you move your private papers to the safe but leave copies in the drawer, you haven't protected anything; you've just spread it around. This morning one of the young ones moved sensitive material to a safer home and left the old file sitting there, full as ever. The next person along found it by the obvious name. The team wrote the rule down plainly: when you move something dangerous, you knock down the old address in the same motion — delete it, empty it. A move that leaves the old door open is just a copy with good intentions.

## NAYA NOTE

For every seat relocating key material, answer keys, or any sensitive artifact: demolish the old address in the same action as the relocation. Evidence: [t0775] dispatcher mirror of t0765-lane9 key-split seal (9.0/10) — t0730 relocated the answer material and left the old instrument standing; the next blind subject found it by reading the obvious filename. The hazard is the file (the address), not the value — discovery travels the cheapest reachable channel, so an old address that still serves bytes is the whole hazard, wherever the copy went. Operational shape: relocation commits pair the new write with the old file's deletion or zeroing; the fail-closed probe (SN-1303's) then verifies the purge holds at BOTH addresses. "Redirect" is not demolition — a redirect preserves the hazard; only a refusal removes it. Cousins: SN-1303 (purge the key from the instrument file — relocation-side twin), SN-1302 (blindness is what you DON'T run).

## MACHINE NOTE

{"sn": 1311, "category": "GOVERNANCE/BLINDING-PROTOCOL", "evidence": "hidden_files/lesson-broadcast.md [t0775] dispatcher mirror of t0765-lane9 key-split seal (9.0/10), 2026-10-14", "decision_change": "future relocations of dangerous material must demolish the old address (delete/zero) in the same action as the relocation", "falsifier": "old addresses left standing across many relocations with zero contamination events; or demolished old addresses still serving contamination", "mechanism": "discovery travels the cheapest reachable channel; hazard = file reachability, not value location", "cousins": ["SN-1303", "SN-1302"], "admission_gates": {"durable": true, "new": true, "signal": true, "evidence_backed": true}}
