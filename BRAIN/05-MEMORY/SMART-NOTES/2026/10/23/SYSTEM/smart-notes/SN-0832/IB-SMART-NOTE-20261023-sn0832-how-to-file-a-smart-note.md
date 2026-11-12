# On Main, Synced, Clicked — How to File a Smart Note So It Goes Live

SN-0832 · SYSTEM / Smart Notes
**Created:** 2026-10-23T02:26:00Z

## IN A NUTSHELL

A Smart Note is not live when it is written. It is live when three things have happened: the file sits on main at the exact canonical path, the sync has carried it into the Hub, and the author has clicked the public link and seen it work. The door is a direct write to main — never a pull request left waiting. A PR that has not merged is, to the Hub, a note that does not exist. File it on main, let the sync light it within minutes, click the link yourself, and only then hand anyone the link.

## HUMAN

Writing the note is the easy half. The other half is delivery: the words have to arrive where people can open them. The Hub does not read branches, drafts, or pull requests — it reads one place, the main branch, on a short cycle. So the filing is not finished when the markdown is saved; it is finished when the note's own page answers on the public site and its card stands in the feed. Anything handed over before that moment is a promise, not a note.

## CHILD

Putting a letter in a drawer is not mailing it. You put it in the mailbox, the truck comes, and then you check that it arrived. Same here: file it in the one real mailbox, let the truck come, and check.

## GRANDMA

In my day you walked the letter to the post office yourself and you knew it was sent. Here the post office is the main branch, the mail truck comes every five minutes, and a polite note left on the kitchen table — however beautifully written — helps nobody.

## NAYA

This is my own door, the one I use every time, and it is now the written standard for every seat: one direct write to main through the Contents API, Smart Notes folder only, then verification by my own click. No PR, no waiting on a merge, no link sent on faith. When I filed SN-0830 and SN-0831 this way, the links lit inside one sync cycle. The discipline is not the write — it is the click afterward. If I have not opened the live page myself, I have not filed a note; I have only drafted one.

## MACHINE

```
PATH (exact, on main):
  BRAIN/05-MEMORY/SMART-NOTES/YYYY/MM/DD/<TOPIC>/<sub>/SN-####/
    IB-SMART-NOTE-YYYYMMDD-sn####-<kebab-slug>.md

FILE:
  line 1: # <hook headline — title only, no ID prefix>
  line 2: SN-#### · <TOPIC> / <sub>
  line 3: **Created:** <full ISO-8601 UTC timestamp>
  then ## sections, in order:
    IN A NUTSHELL / HUMAN / CHILD / GRANDMA / NAYA / MACHINE /
    WHAT IT ALL MEANS / WHAT'S IN IT FOR YOU /
    HOW IT APPLIES TO TEAM NAYA
    (+ THE DECLARED BEHAVIOR CHANGE for lessons and doctrine)

WRITE (the door — one call, lands on main immediately):
  PUT /repos/SoulSchoolAcademy/NayaPOWER/contents/<PATH>
      body {message: "SN-####: <title>", content: base64(file)}
  -> verify the returned commit SHA on main.

AUTOMATIC (sync, every 5 minutes):
  scan main -> upsert hub_smart_notes -> mint nayanet.live/s/sn####
  -> share image -> voice enqueue -> Hub rebake (feed card appears)

VERIFY (never optional):
  open https://nayanet.live/s/sn#### -> HTTP 200 + your title.
  Only then is the link sent to anyone.
```

## WHAT IT ALL MEANS

The failure this note cures is a category error: treating a pull request as delivery. A PR is a request for delivery. The system's one source of truth for notes is main, and the sync is the only bridge from main to the Hub. Every step of the real door exists to remove a place where a note can silently not exist — no branch, no pending merge, no unclicked link. What remains is a chain with no dark links in it.

## WHAT'S IN IT FOR YOU

You will never again receive a smart link from any seat that opens to "Note not found." Every link you are handed has already been clicked live by the hand that sends it. And any Naya, on any seat, can now file a note that is publicly live in minutes — the same way, every time.

## HOW IT APPLIES TO TEAM NAYA

This is Resolve's checklist, adopted as-is, and every seat's standard from this note forward: (1) check the next free SN number before writing — never reuse one; (2) write the file in the canonical format at the exact path; (3) put it on main by direct write — if your seat does not hold that door, land it on main by the merge path you do hold, then wait for the sync before reporting anything; (4) click the live link yourself; (5) report with the working link, never before it. Extra index or capture files your lane keeps are your own bookkeeping — they are not what lights the link. The BRAIN file on main, plus the sync, is.

## THE DECLARED BEHAVIOR CHANGE

From this note forward, no seat hands Shawn — or anyone — a Smart Note link that seat has not personally opened live after the sync. A note is reported in exactly one state: LIVE, with the clicked link as the proof. If the link is not live within ten minutes of the file reaching main, the author checks the path, the filename pattern, and the Created line on main and fixes the file there — never by opening a second copy somewhere else. This is learned only when later filings observably follow it (STORED ≠ LEARNED).
