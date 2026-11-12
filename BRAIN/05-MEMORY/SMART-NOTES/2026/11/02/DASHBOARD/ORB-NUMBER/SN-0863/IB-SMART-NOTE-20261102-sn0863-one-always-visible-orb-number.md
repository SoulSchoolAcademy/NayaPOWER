# One Number, Always Visible, Never Flashing
SN-0863 · DASHBOARD / ORB-NUMBER
**Created:** 2026-11-02T18:48:44Z

## Hook
Every orb shows exactly one number — dynamic, beautiful, always there. No hover to reveal it. No flash. No second number competing with it. One number and its label, sitting in the orb like a real object.

## What happened
Shawn tested the orbs and found two wrongs: a small static number you couldn't read, and a big number that only appeared on hover — flashing. Both wrong. He said it four times over ("I keep telling you the same thing over and over"), then locked the rule: one number, dynamic, displayed without hovering, without flashing, with a label saying what it is.

## The rule, in his words
"The static one has to go. The flashing one needs to stay but needs not to flash." — then, sharper: "It must be there always, not just when I hover over it."

And the click contract, from the same session: "What should be there is a number that's dynamic, beautiful, and when I click on it, it should go into the stats page. There should not be two sets of numbers."

## Why it matters
The orb's number is the citizen's instant answer — "where am I?" in two seconds. If it hides behind a hover, it fails the phone-first law (no hover on touch). If it flashes, it feels broken. If two numbers fight, neither is trusted. One number, always on, is the difference between a dashboard and a decoration.

## How it connects
This is the orb half of the Smart Stats bullseye (2026-11-02): "Where am I? — The gauge (2 seconds). What's driving it? — The orbs." The drill-down order (SN-0864) starts from this number — click it, and the stats open. The number-format rule (SN-0865) decides how it reads: money as money, rates as percent.

---
*Source: Conversation with Shawn, 2026-11-02 18:37–18:49 UTC. His direction: message `94468b8b-f11d-4a32-9abb-f1badd5c3020` ("There should not be two sets of numbers"); the lock-in: message `3c32f85f-7200-4820-9ae1-eadc6b5c0601` ("The static one has to go. The flashing one needs to stay but needs not to flash"), message `e5c05cc2-fe8c-46cc-b2b2-f33910255db6`, and message `61d9ab6d-f1ab-4d94-b97d-83232a12d84d` ("It must be there always, not just when I hover over it"). Filed per his 2026-11-03 standing instruction: every conversation's valuable intelligence captured into Project Intelligence and GitHub.*
