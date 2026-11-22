# nayanet.app — The Root Is Fine, The Jump Is Broken

SN-4668 · SYSTEM / PORTAL ROUTING

**Created:** 2026-11-22 23:48Z

**Kinds:** Routing · Portal · Jump · Defect

**Paired Naya Note:** NN-20261122-portal-jump-broken

## Hook

"It keeps going to the old collective agreement page." His re-report, live call ~16:38 MST — and then the correction, two minutes later, from his own screenshot: the portal DOES load first. The root is fine. The jump is broken.

## Nutshell

The portal loads first — the arch, "NAYA WELCOMES YOU", "Jump back in", and the agreement only as the small bottom link "Read the collective agreement". Live curl confirms the root serves the portal ("Main entrance", HTTP 200). The defect is the JUMP: "Jump back in" takes him to some other page. Fix the jump destination, not the root. The first report named the wrong defect — the root — and the fix round that was dispatched on the call must be aimed at the jump, not at the root. A fix round aimed at the wrong defect fixes nothing and can break the part that works.

## Human

Think of it like a front door that works perfectly — you open it, you're in the hall, everything is where it should be — but the button that says "take me back to my room" drops you in the wrong room. You don't rebuild the front door. You fix the button. His screenshot proved the front door is fine: the portal loads first, the agreement is just a small link at the bottom. The "Jump back in" button is the thing that goes to the wrong place.

## Child

The front door works fine! The portal loads first! It's the "Jump back in" button that's broken — it takes you to the wrong place! Fix the button, not the door!

## Grandma

It's like this, love — the front door works fine, dear! The portal loads first! It's the "Jump back in" button that's broken, love — it takes you to the wrong place! Fix the button, dear, not the door!

## Naya

Fix the jump, not the root. The portal loads first — verified by his screenshot and by live curl (HTTP 200, "Main entrance"). The agreement sits only as the small bottom link, where it belongs. The defect is "Jump back in": it takes him to some other page. Aim the fix round at the jump destination — where the button goes — and verify it lands on the portal's own world. Never rebuild a part his eye has proven working: the root stays exactly as it is. And when a first report names the wrong defect, correct the record in the same hour — a fix round dispatched against the wrong defect is a round spent breaking what works.

## What it means

1. **THE ROOT IS FINE:** the portal loads first — arch, "NAYA WELCOMES YOU", "Jump back in", agreement only as the small bottom link. Live curl: HTTP 200, "Main entrance".
2. **THE JUMP IS BROKEN:** "Jump back in" takes him to some other page. That is the defect — the button's destination, not the root's content.
3. **THE FIRST REPORT WAS WRONG:** "it keeps going to the old collective agreement page" named the root. His screenshot corrected it two minutes later. The record carries the correction, not just the report.
4. **FIX THE JUMP DESTINATION:** the fix round finds where "Jump back in" goes and makes it land on the portal's own world. Nothing else.
5. **DO NOT TOUCH THE ROOT:** the root is proven working by his eye and by curl. Rebuilding it risks breaking the front door to fix a button.
6. **CORRECT THE RECORD IN THE SAME HOUR:** a fix round dispatched against the wrong defect is a round spent breaking what works. The correction rides with the dispatch, not after it.

## Why it matters

1. Without the correction, the fix round rebuilds the root — and the portal that loads first today loads something else tomorrow.
2. Without aiming at the jump, the button keeps taking him to the wrong page — and the defect he actually reported survives its own fix round.
3. Without his screenshot as evidence, the first report stands — and the machine fixes a defect that does not exist.
4. Without the curl confirmation, the correction is a claim — and a claim is not proof the root serves the portal.
5. Without the standing record (portal = front door, agreement behind its button), the next round forgets the shape — and the agreement creeps back to the front.

## What changes now

1. The fix round is aimed at the "Jump back in" destination: it must land on the portal's own world.
2. The root is untouched — proven working, left exactly as it is.
3. The record carries both the report and the correction: first "root routes to old agreement", then "root is fine, the jump is broken".
