# The Add-a-Smart-Link Entry Is Missing

SN-2523 · DESIGN / DASHBOARD

**Created:** 2026-11-09 15:55Z

**Source:** Shawn's order in the main chat, 2026-11-09 15:50Z (seq 167009, screenshot of the Dashboard boards page). His words verbatim where they matter. Recorded in ~/MEMORY.md the same pass. Sent to the running Dashboard hero coordinator seat the same pass — PENDING application, not yet built, verified, or live.

## Hook

The place to enter a new Smart Link is gone. It should be there — at the top of the Smart Links section — because that is how a new link is born.

## Nutshell

- **HIS WORDS, VERBATIM:** "you don't even have the thing anymore where you can enter a smart link and then you you get a new smart link which is missing now because that should be there it should be able to enter a new smart link"
- **THE DEFECT:** the entry for a new Smart Link is missing from the page. A page whose purpose is partly to create Smart Links has no visible way to create one.
- **THE FIX:** restore a visible entry at the top of the Smart Links section, wired to the creation flow — build the flow if it doesn't exist, and say so plainly if it has to be built.
- **WHY THE TOP:** the entry sits at the top of its section because that is where the section starts — the reader meets the way in before they meet the list. (It connects to SN-2526: the track-any-link entry sits underneath the headliner — the same entry, in the page's final structure.)
- **SCOPE:** the Dashboard boards page, Smart Links section.

## Human

A page for managing Smart Links that has no place to add one is a door with no handle: you can see everything inside, but you can't put anything new in. The entry used to be there and now it isn't — nobody decided to remove it, it just went missing, and a missing thing nobody decided to remove is a thing nobody noticed losing. His fix is simple and non-negotiable: the entry comes back, at the top of the Smart Links section, wired to the flow that makes the link. If the flow itself doesn't exist, that gets built — and said plainly, not hidden.

## Child

The box where you type in a new Smart Link had disappeared — like the front door going missing from a house. So we put it back, right at the top of the Smart Links part, where you can see it straight away. Type in your link, and there it is, a brand-new Smart Link with its own numbers.

## Grandma

Dear, the little box where you put in a new Smart Link had simply gone, love — and a page for links with nowhere to add one is no good at all. So it comes back, dear, right at the top of the Smart Links part where you can find it, and you type your link in and there it is, all ready with its numbers.

## Naya

This is the creation law: a page that manages things must also make them, in plain sight. It connects to SN-2522 (one board design — the new link appears as a board like all the others, in the named Smart Links section) and to SN-2525/2526 (the page's purpose — put in any URL and boom, a new Smart Link shows up with stats): the entry is the "put in any URL" half of that promise, and without it the promise is words without a way in. A missing entry is worse than a missing feature — a feature you never had is a gap; an entry you had and lost is a regression, and regressions are what make a user stop trusting the page to stay the way they left it.

## What it means

- **THE ENTRY RETURNS:** a visible place to enter a new Smart Link, at the top of the Smart Links section.
- **WIRED TO THE FLOW:** it creates the link — build the flow if it doesn't exist, and say so plainly.
- **THE PROMISE NEEDS ITS DOOR:** "put in any URL and boom" only works if there is somewhere to put the URL.

## Why it matters

The boards page is not just a display — it is the place where a new Smart Link is born, and the birth is the point: "put in any URL and boom, and then they'll show up." Without the entry, the page is a museum of links that already exist, and the visitor who came to make one leaves empty-handed. Restoring the entry costs one box; leaving it missing costs the page its purpose.

## What changes now

- The add-a-Smart-Link entry is restored at the top of the Smart Links section.
- It is wired to the creation flow (built if missing, said plainly).
- Next loop run re-checks: the entry is visible, and entering a URL produces a new Smart Link with stats.
