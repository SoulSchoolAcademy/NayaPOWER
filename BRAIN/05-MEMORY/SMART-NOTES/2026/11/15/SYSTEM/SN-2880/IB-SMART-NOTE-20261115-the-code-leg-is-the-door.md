# The Code Leg Is the Door

SN-2880 · LESSON / SYSTEM

**Created:** 2026-11-15 07:47Z

**Paired Naya Note:** NN-20261115-the-code-leg-is-the-door

## Hook

The build scored 8/10. The member still cannot get in. The code leg is the door — and the door is stopped.

## Nutshell

Membership build, 2026-11-15 07:47Z: coordinator 225228b0 completed ~07:19Z, verdict **NOT DONE — 8/10**; the captain's verdict delivered to Shawn ~07:47Z: **NOT WHOLE 8/10**. The build itself is good — Vault Dial v2 measured open (obsidian core, purple edge, inset-deep inputs, no orbit ring), the paywall opens as a modal with the ladder $25/$50/$100 verbatim and the founders line exactly once, the course legs and the video/audio/image theatres proven in the captain's own seat. **But the member cannot get in.** The login-code leg is stopped: name filled → "Need a code?" → **"The code could not be sent — TypeError: NetworkError when attempting to fetch resource."** A wrong code (`NAYA-000000`) is correctly rejected; no code was ever issued, none faked. **The blocker is the Smart Mail RLS insert policy for `smart_mail_threads`** — the mail/RLS lane owns it. The captain's ruling, in her words: *"the code leg is the door that lets a member in and it is stopped; the fix belongs to the mail/RLS lane. No buildable fix round exists in this lane."* One List `membership-brief` moved dispatched → queued; its next step is to re-prove the code leg + the Academy Video button live when the RLS policy lands. **Money guard AMENDED 19 → 22** in the same verdict: the brief contradicted itself — Build 5 requires the ladder rendered — and the build adds exactly the three ladder figures and nothing else ($50 5→6, $100 3→4, $25 2→3; every other figure unchanged). A guard that contradicts the build it guards must be amended, not obeyed into a fail.

## Human

A membership is not a page. A membership is a door a member walks through — and the code is the key. Everything else in this build works: the dial opens, the paywall reads right, the lessons play. But the key never arrives, so the member stands outside a beautiful door. The score 8/10 is honest about the build and misleading about the membership: the two missing points are not two more build items, they are the one thing that makes the build usable. That is why the verdict is NOT WHOLE and why no fix round was dispatched in this lane — there is nothing left to build here. The work moved to the lane that owns the lock: the mail/RLS lane and its insert policy for `smart_mail_threads`. The lesson for the machine is about where a round belongs: a defect that lives in another lane's policy is not fixed by ordering another maker round on a finished build. It is fixed by naming the owning lane, queuing the item on its condition, and waiting — which is what happened: `membership-brief` sits queued until the policy lands, then the code leg gets re-proved live. The money-guard amendment is the same lesson at smaller scale: a guard that contradicts the build it guards is a broken guard, and the honest move is to amend it in writing (19 → 22, with the reason stated) rather than fail a build for doing what the brief required.

## Child

Imagine you build the most beautiful treehouse in the world — with a ladder, and windows, and a flag on top! But you forgot to build the DOOR. Your friends can see it, they can point at it, but nobody can climb inside! The treehouse isn't finished, even though everything you built is beautiful. You don't need a better treehouse — you need a door. And the door belongs to someone else's job!

## Grandma

It's like this, love — you can bake the finest cake, ice it beautifully, put it in the prettiest box, but if the lid is nailed shut, nobody can eat it! The cake is wonderful and the box is the problem. You don't bake another cake. You find the person with the hammer, and you ask them to open the box. That's what happened here: the membership is baked and beautiful, and the little code that lets a person in is stuck — and the fix belongs to the mail side, not the bakers.

## Naya

I never call a membership whole while its door is stopped. The build is the house; the code is the key — and I name the lane that owns the key.

## What it means

- **THE LAW:** the code leg is the door. A membership whose member cannot get in is NOT WHOLE at any build score.
- **THE BLOCKER:** Smart Mail RLS insert policy for `smart_mail_threads` — the mail/RLS lane owns the fix, not this lane.
- **THE PROOF:** "Need a code?" → "The code could not be sent — NetworkError"; wrong code correctly rejected; no code issued, none faked.
- **THE GUARD:** money guard amended 19 → 22 in writing — a guard that contradicts the build it guards is amended, not obeyed into a fail.
- **THE QUEUE:** `membership-brief` waits queued until the RLS policy lands; then the code leg + Academy Video button are re-proved live.

## Why it matters

Without this law the machine keeps ordering build rounds on a finished build — maker after maker polishing a door that was never the problem, while the member still stands outside. Each such round costs a night and teaches nothing. With the law, the verdict names the owning lane in the same pass, the item queues on its true condition, and the next round that runs is the one that can actually open the door. It also protects the maker: an 8/10 on a build that did its job is not a failing grade — it is a build waiting on a policy, and the record should say so plainly.

## What changes now

1. A membership verdict states the code leg separately from the build score — build score and door state are two different verdicts.
2. A defect owned by another lane's policy is named to that lane in the same pass — no fix round is dispatched in a lane that cannot fix it.
3. A guard that contradicts its own brief is amended in writing, with the reason stated — never obeyed into a fail.
4. `membership-brief` stays queued until the RLS policy lands; the re-proof is live (code sent, code accepted, member in) — never file-only.
5. The dial-bezel watch item (the core's own silver bezel reads as a ring) stays his eye's call, stated plainly, not folded into the code-leg verdict.
