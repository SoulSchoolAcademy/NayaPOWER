# Prove the Menu, Not Just the Route

SN-4254 · LAW

**Created:** 2026-11-20 ~05:28 MST (12:28Z) — Personal frame fix-6 captain's eye report (EYE-REPORT.md, 12:26Z), re-dispatched eye, VM Firefox

**Filed:** SN-4254 — Intelligence Loop run 411, 2026-11-20.

**Paired Naya Note:** None — no Shawn dictation in this window; this lesson comes from the eye's own finding, not from his words.

## In a Nutshell

A composer proven six out of six through URL suffixes was never proven through the menu — and the menu path was dead. ADD → Create menu → "Message" did nothing on tap: the menu item only adds a class to a panel that was never built. Every entry point is its own proof; proving one entry proves nothing about the others.

## Child Note

Imagine a house with six doors, sweetheart — you checked all six doors by opening them from the outside with a special key, and they all worked! But nobody ever tried the doorknob from the inside — and when someone finally did, that doorknob just spun around and the door stayed shut! So we check every door the way a person really opens it, sweetheart — not just the special key way!

## Grandma Note

It's like this, love — the checker proved the composer six ways by typing the address straight in, dear, and it worked every time. But nobody tapped the Message button in the menu itself, love — and when the eye finally did, nothing happened at all, dear. The button only flipped a switch for a little room that was never built. So we test the button the way a person taps it, love — the address and the button are two different doors, and each one needs its own knock.

## Ultimately What It Means

- **THE FINDING (fix-6 eye, 12:26Z):** ADD → Create menu → "Message" — four real taps, zero results. The menu closes, no composer, no messenger panel, no navigation. `body.msg-open` = 1 after the tap, `.hub-msg-panel` count = 0. Root cause, read from the fixed bytes: the menu item calls `openMessenger()`, which is only `document.body.classList.add('msg-open')` — it never calls `ensureMsgPanel()` / `openMsgPanel()`, the only functions that build the panel. Pre-existing: the fix-6 diff (0 removed / 12 added, popstate handler only) cannot affect it.
- **THE MISS THAT LET IT THROUGH:** the checker and the fix-5 eye proved "composer 6/6" via URL suffixes on fresh loads, never via the menu — so the menu path was never proven until the cloud leg found it dead and the eye confirmed it.
- **THE RULE:** every entry point is its own proof. A function reached by URL, by tap, by menu, and by button are four different proofs, and a pass on one is not a pass on the others. A round's acceptance names each entry point and how it was tapped.
- **THE SCOPE RULE:** the page he sees is the scope — a pre-existing dead button found by the eye goes back even when it predates the round (the fix-5 Ask Naya precedent). He taps ADD → Message and nothing happens on a page we passed: that is the failure the eye exists to prevent.

## How It Connects / How to Apply It

1. When a checker proves a function, list every entry point that reaches it — URL suffix, menu item, button, keyboard — and prove each one by the real action, not by a shortcut that reaches the same code another way.
2. When a verdict says "6/6", ask which six: six routes, or six taps? If the six are routes, the taps are still unproven.
3. When a tap adds a class but nothing appears, read the bytes: a class without the builder that creates what the class styles is a switch for a room that was never built.

## What's In It For Them

Citizens tap buttons, not URLs — and a button that does nothing is a page that lied to them. Proving every entry the way a person uses it means the page he sees works the way he taps it, the first time.
