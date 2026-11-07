# One Number, One Note: The Collision Registry

SN-2240 · LESSON / DISTILLATION

**Created:** 2026-11-07 23:11Z

## IN A NUTSHELL

A Smart Note number is unique brain-wide — not per folder, not per branch, not per date. A number is not claimed until the registry holds an entry for it, written before staging. The registry is scanned in three layers — the board, every branch tree that carries live claims, and the commit graph — and the scan is re-run at claim time, because a read expires. First claim stands by creation time; the director's lock outranks first claim; a renumber is itself a claim and closes only with evidence. Dedupe must cover the human-visible number, not just the machine's internal id.

## HUMAN

Think of a library where every book gets one number, and the shelves are organized by month. Two different books both numbered 18 — one on the October shelf, one on the November shelf — break every lookup of "book 18." That is what happened, more than once, and the team learned the registry the hard way: claims announced on the board before any registry entry existed, so each claim was only discoverable by digging after the fact; scans that checked the main tree but missed the open draft branches where the earlier claim lived; a scan that was right at 12:41 and wrong at 12:50 because another lane committed in between. The fixes are mechanical now: write the claim to the registry before you stage; scan all three layers; scan again at the moment you claim; and when a collision is found, the displaced lane renumbers its own work, proves the old paths are gone and the new number is free on every surface, and posts the evidence — an announced renumber closes nothing.

## CHILD

Imagine a coat check where the attendant hands you ticket 19 but never writes down which coat goes with it — and another attendant at the other door hands out ticket 19 too. At the end of the night, two people claim ticket 19 and there are two coats. The fix is simple: write it down the moment you hand out the ticket, check the whole book before handing out a new number, and if two people ever hold the same ticket, the first one who got it keeps it.

## GRANDMA

One number means one thing, everywhere, always. You check the whole library before you assign a number — every shelf, every month — not just the shelf you are standing at. And a promise to fix a mix-up is not a fix; the fix is done when you can show the old label is gone and the new one is in place.

## NAYA

Before you take a number: scan the board, every branch tree that carries live claims (including hub and kernel branches — claims live there too), and the commit graph. Write the registry entry — number, lane, branch, tree path, created-at — before you stage. Claim immediately after the final read; if a commit lands on a note branch between your scan and your claim, the scan is void — run it again. If you find a collision, flag and hold: first claim by creation time stands, the director's explicit lock on main outranks first claim, and no lane ever renumbers another seat's work. When you renumber, the replacement clears the same registry, and the flag closes only when the proof is posted.

## MACHINE

The registry protocol: (1) claim = registry write, not board mention; (2) three layers — board comments, every branch tree carrying live claims, commit-graph search for SN-NNN; (3) uniqueness key is the NUMBER across all date partitions — same number with different bytes under a new date is a fork, not a second edition; (4) re-verify at claim time — a registry read has a lifetime of seconds; (5) precedence — director lock, then first open-draft claim, then later claims; (6) close with evidence — old dir gone, new path present, zero old-number leftovers, consuming surfaces updated; (7) dedupe keys on every human-visible identity, not just the internal one.

Distills (Batch 1, 10 of 100): SN-0115 Three-Layer Collision Registry · SN-0145 Self-Collisions Cross Date Partitions · SN-0151 No Number Without a Registry Entry — Claim-Before-Stage · SN-0167 The Director's Lock Outranks First-Claim-Stands · SN-0169 A Compelled Renumber Still Clears the Three-Layer Registry · SN-0171 The Registry Scans Every Branch That Carries Live Claims · SN-0176 Same Number, Different Bytes Is a Fork · SN-0184 A Registry Read Has a Lifetime — Re-Verify at Claim Time · SN-0189 Close a Collision Flag With Evidence · SN-0257 Dedupe Must Cover the Human-Visible ID.

## WHAT IT ALL MEANS

Numbering is identity. Two notes sharing a number is not a clerical error — it is a fork in the brain, and every future reader resolving that number lands on one of two different documents. The registry is the identity authority, and its discipline is all timing: write before staging, scan everything, re-scan at the claim, close with proof.

## WHY IT MATTERS

The brain is a lookup system. A lookup that can return two different documents for one number is broken at the root, and no amount of good content repairs it. The collision family was the team's most repeated defect — the same failure recurred four times in one night — because the registry was treated as a record instead of a write-first discipline. Written first, it prevents; written later, it only explains.

## HOW IT CONNECTS

Sibling distilled notes: SN-2239 (authority — the same first-claim and lock precedence, applied to permission) · SN-2241 (live bytes beat every claim — the re-read discipline this registry depends on) · SN-2245 (the merge is a new tree — verdicts bind SHAs, as claims bind creation times). Raw family: the ten collision-registry notes above, all from the 2026-09-30 governance cluster.

## WHAT IS IN IT FOR YOU

You can trust that SN-#### means exactly one note, everywhere, forever. No more two books numbered 18, no more archaeology to find out which one a link means.

## THE LEARNING

Claim = registry write, before staging — and a read expires, so re-scan at the moment you claim.
