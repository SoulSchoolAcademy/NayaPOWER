# Check the Viewpoint by Eye

SN-2508 · TEAM / VERIFICATION

**Created:** 2026-11-09 15:35Z

**Source:** Shawn's rebuke in the main chat, 2026-11-09 15:18Z (seq 166768), on the gauge-fix proof page. His words verbatim where they matter. Recorded in ~/MEMORY.md the same pass.

## Hook

A pass on numbers that looks messy by eye is a fail — the viewpoint is the check.

## Nutshell

- **HIS WORDS, VERBATIM:** "make sure when you're checking these pages that you're checking the viewpoint and seeing what you're seeing on the page like a lot of them it's messy for no reason."
- **THE REBUKE:** the checks were passing numbers while the page looked messy to his eye. The orbs were one color, crashed into the gauge, the big orb covering the number tiles, the mode strip one flat bar — and the checks passed anyway. A verification that cannot see mess is not verification.
- **THE RULE, NOW STANDING:** verification means looking at the rendered viewpoint the way he sees it. Seats judge screenshots like a human eye, not just rects and bytes. If the page looks messy by eye, it fails — whatever the numbers said.
- **WHAT IT REPLACES:** measurement-only verification. Rects, contrast ratios, byte counts, and popup checks are preparation, never proof. They catch what they are told to catch; the eye catches what nobody told it to look for.
- **WHAT IT DOES NOT REPLACE:** the measurements still run — they are the preparation. But no work moves on measurements alone. The viewpoint check is the gate the work passes through, and his eye is the final gate after that.

## Human

Imagine a building inspector who measures every wall with a laser and declares the house perfect — while the front door is hanging off its hinges in plain sight. The measurements were right; the house was still wrong, because nobody looked at it. Shawn's rule is the look: before anything is called done, someone looks at the actual page the way he looks at it, on his screen, and asks — is this messy? If yes, it fails, no matter what the instruments said. The instruments prepare the work; the eye judges it.

## Child

If you clean your room by measuring it with a ruler but never looking at it, you might miss the big pile of toys in the middle of the floor. The ruler says the room is tidy. Your eyes say it isn't. From now on, we always look at the room with our eyes before we say it's clean — the looking is the real check.

## Grandma

Dear, the numbers said it was fine and his eyes said it was messy, love — and the eyes were right, dear. From now on we look at the thing itself, with our own eyes, before we call it done. A ruler can't see a mess, love. Eyes can.

## Naya

This is the verification law catching up with the Live Viewpoint Method: no seat scorecard or verification is proof; only his eye is. SN-2508 makes that operational for every seat — the viewpoint check is not an extra step, it is THE check, and it happens before anything is reported done. It also explains the failure mode of the whole morning: seats verified mechanics (popups, padding, contrast, rects) and never asked whether the page looked right, so obvious defects — orbs crashed into the gauge, a flat mode bar, tabs eating the hero — walked past scout, rebuild, two verifiers, and the captain's browser check. The rule is cheap to apply (look at the screenshot as a human would) and it would have caught every one of them. A check that cannot fail on mess cannot pass on quality.

## What it means

- **THE VIEWPOINT IS THE CHECK:** every verification looks at the rendered viewpoint the way he sees it — desktop + phone, scroll 0 AND scrolled.
- **MESSY BY EYE IS A FAIL:** a pass on numbers that looks messy by eye is a fail, full stop.
- **MEASUREMENT IS PREPARATION:** rects, bytes, and contrast ratios still run — but they are never the proof on their own.
- **HIS EYE IS THE FINAL GATE:** the seat's eye-check prepares the work; his eye decides it.

## Why it matters

Every defect in SN-2507 was visible in a single screenshot. The reason they shipped is not that the builders were careless — it is that the verification asked the wrong question. "Do the numbers pass?" is a question a machine can answer, and the machine answered yes while the page was messy. "Does it look right?" is a question only an eye can answer, and nobody asked it. This note changes the question every seat asks before reporting done. It is the cheapest fix in the system — one look — and it is the one that would have caught the most defects.

## What changes now

- Every brief and every verification carries the viewpoint-by-eye check as a named gate: look at the rendered viewpoint as a human would, at desktop + phone, scroll 0 and scrolled, before reporting done.
- The design-contract gate (obvious defects) and the viewpoint check are the same habit: if you can see the defect by looking, fix it, don't hand it on.
- The Dashboard hero coordinator seat applies the rule to its own proof page first — its own eye-check precedes any report.
- Next loop run re-checks: the hero proof page judged by eye, not just by rects.
