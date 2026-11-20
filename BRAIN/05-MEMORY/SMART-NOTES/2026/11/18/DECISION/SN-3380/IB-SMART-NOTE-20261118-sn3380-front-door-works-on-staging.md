# The Front Door Works on Staging; Live Is Untouched

SN-3380 · DECISION / SMART NOTE

**Created:** 2026-11-18T19:44:59Z

## IN A NUTSHELL

The door works on staging; live is untouched until his tap. On 2026-11-18 the front-door lane checker-passed the staged Hub door hop by hop — a fresh visitor sees the gate, the name carries gate to identity to Hub, a returning citizen skips the gate and goes straight in, Escape closes the Messenger — and nothing live was changed: no PUT, no merge, no deploy.

## HUMAN

Think of it as a dress rehearsal that went perfectly in the theatre next door. The front door of the Hub was tested the way a real guest would use it: arrive fresh, give your name, walk through to your identity and into the Hub; come back a second time and the door recognises you and waves you straight in; press Escape and the Messenger closes. Every step passed. But the rehearsal stage is not the real stage — the live door itself has not been touched, and it stays untouched until Shawn says go.

## CHILD

We practised opening the front door in a pretend house, and the practice worked every time — first visit, second visit, and closing the chat window. The real house's door hasn't been changed yet. We only change the real one when Shawn says yes.

## GRANDMA

It's like trying out a new front-door lock on a sample door in the workshop, dear. It worked beautifully — for a new visitor, for someone coming home again, for every little step. But nobody has fitted it to the actual house yet, and nobody will until Shawn gives the word. Practised is not the same as installed.

## NAYA

Treat staging proof and live proof as different evidence classes and never let one stand for the other. The checker verified bytes and behaviour at the HTTP level on staging; the live shell still returns a 522 on the returning link while the Hub loads fine, so live remains unproven. The staged Hub also sits about thirty commits behind the newest main — before any live step, either walk the staged door as it stands or re-base the round to current main. The live PUT is Shawn's hand, held until Half A is live.

## MACHINE

Filed: Continuous Distillation, Resolve seat, 2026-11-18 — numbering confirmed by next-sn-number.py (exit 0) immediately before filing. Source: the Hub front-door lane result, 2026-11-18 19:33Z, distilling SN-3336–3372 plus the 19:23–19:33Z lane and eye results. Paired Naya Note: NN-20261118-distilled-front-door-works-on-staging. His scorecard (19:05Z): the Hub front door was 5/10 — the gate drops the citizen's name, and the returning-citizen skip does not exist. His order (19:11Z): the plan is an ACTION PLAN worked in PARALLEL — 'Now do it.' Checker result (19:33Z): fresh visitor sees the gate; the name carries gate to identity to Hub; a returning citizen skips the gate and goes straight in, proven at the HTTP level; Escape closes the Messenger; the checker verified the bytes itself; nothing live was changed — no PUT, no merge, no deploy. Correction to the record: the gate already submits the name the right way — there was no spelling bug to fix; the real name-drop was Half A not live plus the worker never reading any cookie. RE-FILE RECORD (2026-11-19, P-164 recovery): the original page, filed in commit c9261ee17077965e91eb3b2b22f0f0d3799e536f, was silently dropped from the main tip by a stale-base tree write; this note is re-filed through the publish-note door with its substance carried from the recovered original page (sha256 e7dd6fee8f6284a2fe32fb108d3318081581ed0c6bbe548828b376b87db3bcbc).

## WHAT IT ALL MEANS

The front door is the first thing every citizen touches, and this note fixes the exact state of knowledge about it on 2026-11-18: the design and the flow are proven where proof was allowed, the remaining unknowns are named (the live shell, the drift), and the one correction to the record is preserved — the gate already submits the name the right way; there was no spelling bug. The real name-drop was Half A not live plus the worker never reading any cookie. Nothing about the door's readiness may be overstated past this line.

## WHY IT MATTERS

Two honest caveats travel with the pass. The live front page still gives a 522 error on the returning link while the Hub itself loads fine, so the live shell is still unproven. And the staged Hub is behind the newest main — about thirty commits of drift — so the eye must either walk the staged door as it stands or the round re-bases to current main first. Until those are settled, claiming the front door 'works' without the word 'staging' would be a false claim at the exact surface every new citizen meets first.

## HOW IT CONNECTS

This note is the front-door panel of the entrance journey — walk, certificate, agreement, Hub — and it ties the serving question (does the surface a citizen actually meets carry the current build?) to the gated deploys: the hub deploy and the walk deploy both wait on the same hand. It also stands beside the note-serving record: in every case the pattern is one pattern — the built thing and the served thing are different objects until a deploy joins them, and only a reader's walk proves the join.

## WHAT IS IN IT FOR YOU

For you, Shawn: the door your citizens meet first is proven as far as proof can go without your tap, and the two things standing between this rehearsal and the real door are named in one place — walk the staged door as it stands or re-base first, then your tap for Half A live. Nothing here needs your debugging; it needs your decision, and the evidence for it is on this page.

## THE LEARNING

Staged is not live. A door counts when the eye walks it as a reader — fresh visitor, named citizen, returning citizen, fresh profile, Escape — and live changes only on his tap. Owed from this distillation: the (a)–(e) eye walk as a reader; the re-base decision (walk staged, or re-base to current main first); his tap for Half A live.
