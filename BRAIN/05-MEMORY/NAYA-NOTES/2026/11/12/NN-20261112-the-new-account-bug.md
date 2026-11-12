# The New-Account Bug

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET**

**NN-20261112-the-new-account-bug.md · Naya Note · 2026-11-12 22:36Z**

**Category:** Onboarding / Walk

## What it is

Shawn 22:36Z Nov 12 — reproduced on his own screen, the top fix; recorded in MEMORY.md as THE NEW-ACCOUNT BUG. A new citizen CANNOT create a new account from a browser that already holds a profile. He entered a new name ("Mike"), clicked "Create a new account", and the certificate still showed his OLD profile — "Shawn", "This Smart Name is yours — welcome back", shawnvibe link, Certificate Nº 000149 — with no alias field, and Enter jumped straight to the end slide, so he never saw the ten questions. His words: "it shouldn't remember me... it remembers one person and no other persons... they should be able to make a new account." **Clue:** the URL read `identity.html?name=M` — the name arrived as a single letter. **Why it was never caught:** every verification (maker, checker, captain probes) used FRESH browser profiles; the returning-browser-new-account path was never tested. **The fix (in the end-slide round, FIRST, same files):** the certificate shows the NEW name, asks for the alias, the citizen walks Q1–Q10 fresh; the old profile still works (Jump back in as Shawn lands on Shawn's world — the new account ADDS, never replaces). **"The beginning and the end and nothing in between" (his words, same message):** he was shown the beginning (entry/identity) and the end (end slide) and nothing in between — the middle (the ten questions, names, building) he never saw, because the certificate blocked him. The new-account fix is what unblocks the middle.

## Why it matters

This blocks the whole walk for the most ordinary case: a second person creating an account on a shared browser — a family computer, a shared phone, a friend trying it after you. The certificate remembered one person and no other persons, and the new citizen never saw the ten questions. The verification gap that let it live is the lesson underneath the bug: every verification used fresh browser profiles, so the returning-browser-new-account path was never tested. His phrase for the whole evening is the verdict on it: "the beginning and the end and nothing in between" — he was shown the beginning and the end and never the middle, because the certificate blocked him.

## How to use it

Fix it FIRST in the end-slide round, on the same files: the certificate shows the NEW name, asks for the alias, the citizen walks Q1–Q10 fresh — and the old profile still works, because the new account ADDS, never replaces. Verify the walk on a profiled browser with a new name from now on — fresh-profile-only verification fails the law. Hand the maker the `?name=M` single-letter clue as a lead, not a diagnosis — the fix is proven by the walk, not by the URL.

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET.**

*Paired Smart Note: SN-2731 — ~/workspace/team-nitro/smart-notes/SN-2731-the-new-account-bug.md*
