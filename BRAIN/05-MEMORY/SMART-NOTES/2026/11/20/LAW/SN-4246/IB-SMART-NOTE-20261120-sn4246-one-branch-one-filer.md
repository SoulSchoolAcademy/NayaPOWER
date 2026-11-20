# One Branch, One Filer — Parallel Filings Eat Each Other's Proof

SN-4246 · LAW

**Created:** 2026-11-20 ~01:05–01:12 MST (08:05–08:12Z) — the Agreement distill fix-3 round, from the coordinator's completion and the two record seats that followed it.

**Filed:** SN-4246 — Intelligence Loop run 410, 2026-11-20.

**Paired Naya Note:** none — a process lesson from the machine's own night, not a Shawn dictation.

## In a Nutshell

Two lanes filed the same branch in parallel and one ate the other's proof. The landing agent filed `walkthrough/agreement-distill-fix3-20261119` at tip `27689bf6` — the six fixed content files and the 21-file round record, checker reports included. The coordinator then force-updated the branch to tip `f3d4ab3a`: its tree carried byte-identical fixed content files, but the `checker/` reports were gone — dropped, not deleted on purpose, just never carried forward. Two small record seats had to put the proof back, one commit each: checker proof restored at `fa2d73e9`, coordinator proof restored at `dc262be6`. The content was never at risk; the evidence of the verification was. A force-update that does not read the tip it replaces will silently un-file whatever the other lane filed.

## Child Note

Imagine two friends building one tower, sweetheart — one puts the little flag on top, and then the other one knocks the tower down and builds it again without the flag! The tower is just as tall, but the flag is gone — and nobody meant to lose it! So we take turns, sweetheart — one builder at a time, and the next builder always looks at what is already there before starting!

## Grandma Note

It's like this, love — two people tidying the same drawer at once, dear, and one of them puts the other one's letters back in the wrong place without ever seeing them. Nothing was thrown away on purpose, love — it was just never carried forward. So we do one at a time, dear, and the second person always opens the drawer first and looks at what is already inside!

## Ultimately What It Means

- **THE FACT:** the fix-3 branch was filed twice in parallel — landing tip `27689bf6` (tree `c200836e`, six fixed files + 21-file round record) and coordinator tip `f3d4ab3a` (tree `65c1f008`, byte-identical content files, `checker/` reports absent).
- **THE FACT:** the coordinator's own verification was real and cold — filing identity via fresh blob-API reads, diff replay (0 removed, exactly 6 files changed), design-law checks delta 0/0 on all four files — and still the force-update dropped the proof, because the verification checked the content, not the tree it replaced.
- **THE FACT:** restoration took two record seats and two fast-forward commits — `fa2d73e9` (checker proof, 7 files, bytes identical to the parallel filing) and `dc262be6` (coordinator proof) — with the six content-file blob shas verified unchanged at every step.
- **THE RULE:** one branch, one filer at a time. A lane that files second re-reads the tip first and carries the first lane's files forward. A force-update is never issued against a tip the filer has not read.
- **THE CHECK:** before any force-update, list the tip tree; after it, list it again and confirm nothing the other lane filed is missing. Content-identical is not proof-identical — the verification evidence is part of the filing.

## How It Connects / How to Apply It

1. When two lanes touch one branch, sequence them: the second filer waits for the first tip, reads it, and builds on it — never beside it.
2. A force-update names the tip it replaces and what that tip carried; if the list is not in hand, the force-update does not go out.
3. After any filing, verify the tree, not just the content files — the record dirs (`checker/`, `coordinator/`, `eye/`, `maker/`) are part of the filing, and their absence is a filing failure, not a tidy-up.
4. If proof goes missing from a tip, restore it with a record seat, fast-forward only, and verify the content shas are unchanged — exactly as the two fix-3 record seats did.
5. When a round's proof lives in more than one lane, the coordinator's completion report names every dir that must survive on the tip, so the filer checks for them by name.

## What's In It For Them

Citizens never see this — and that is the point. The proof that a page was verified stays on the branch it was verified on, so no round ever has to be re-proven because its evidence was quietly un-filed. The machine keeps its own receipts.
