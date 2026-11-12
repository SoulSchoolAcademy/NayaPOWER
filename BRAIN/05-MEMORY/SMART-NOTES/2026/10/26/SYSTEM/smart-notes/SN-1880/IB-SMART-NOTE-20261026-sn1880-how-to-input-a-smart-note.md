# How to Input a Smart Note, Successfully — So It Goes Live

SN-1880 · SYSTEM / Smart Notes
**Created:** 2026-10-26T22:42:30Z

## IN A NUTSHELL

A Smart Note is one lesson, law, or learning, written once in a file that humans and Nayas can both use, filed on main, carried by the sync into the Hub, and opened by a public link. It is not live when it is written. It is live when the file sits on main at the exact path, the sync has carried it into the live table, and the author has opened the public link and seen the right title. Input it the right way and it goes live in minutes. Input it any other way — a reused number, a broken header, a branch instead of main, a link handed out before it is clicked — and it silently does not exist, no matter how good the words are.

## HUMAN

Think of it like posting a letter. Writing the letter is not mailing it. The mailbox is the main branch. The mail truck is the sync. The proof it arrived is opening the delivered page yourself. A letter left on the kitchen table, however beautifully written, helps nobody — and a note left in a branch, a draft, or a pull request waiting to merge is exactly that: a letter never posted. File it in the one real mailbox, let the truck come, and check that it arrived before you tell anyone it is there.

## CHILD

Putting a note in the drawer is not sharing it. You put it in the mailbox, the truck comes, and then you check that your friend got it. Same here: file it in the one real place, wait for the truck, and check the link yourself.

## GRANDMA

Dear, here is the plain version. You write your note down properly, you put it where everyone can find it, you wait a few minutes, and then you open it yourself to make sure it is really there. Only then do you pass it along. If you pass it along first and it is not there yet, you have sent someone to an empty house.

## NAYA

For a Naya seat, this is the door, every time, no exceptions: check the number is free before writing, write the file in the canonical shape at the exact path, put it on main by direct write in the Smart Notes folder only, wait for the sync, click the live link yourself, and only then report it with the working link. If your seat does not hold the direct-write door, land it on main by the merge path you do hold, then wait for the sync before reporting anything. A link reported before it is clicked live is a promise, not a note.

## MACHINE

```
CHECK THE NUMBER FIRST (never reuse one):
  a number already in the live table, or already a folder on main,
  is taken — even if two notes share it by accident.
  SN-1878 is the standing warning: first claim keeps the number,
  the second claim is a collision to cure, not a note to ship.

FILE (exact, on main):
  BRAIN/05-MEMORY/SMART-NOTES/YYYY/MM/DD/SYSTEM/smart-notes/SN-####/
    IB-SMART-NOTE-YYYYMMDD-sn####-<kebab-slug>.md
  Topic and sub-folder follow the subject; how-to notes live
  under SYSTEM/smart-notes, as SN-0832 did.

HEADER (exact, first three lines, in this order):
  line 1: # <hook headline — title only, no ID prefix>
  line 2: SN-#### · SYSTEM / Smart Notes
  line 3: **Created:** <full ISO-8601 UTC timestamp, ending in Z>
  NEVER leave Created blank. An empty Created line costs a real
  thing: the note's timestamp comes through empty in the live
  table (SN-1879, before its header was restored to canonical
  shape). Use full UTC, with Z, on the line exactly as shown.

SECTIONS (in order):
  IN A NUTSHELL / HUMAN / CHILD / GRANDMA / NAYA / MACHINE /
  WHAT IT ALL MEANS / WHAT'S IN IT FOR YOU /
  HOW IT APPLIES TO TEAM NAYA /
  THE DECLARED BEHAVIOR CHANGE

WRITE (the door — one call, lands on main immediately):
  PUT /repos/SoulSchoolAcademy/NayaPOWER/contents/<PATH>
      body {message: "SN-####: <title>", content: base64(file)}
  Verify the returned commit SHA on main. A branch, a draft,
  or an unmerged pull request is invisible to the Hub.

AUTOMATIC (sync, on its short cycle):
  scan main -> upsert live table -> mint nayanet.live/s/sn####
  -> share image -> voice enqueue -> Hub rebake (feed card appears)

VERIFY (never optional):
  open https://nayanet.live/s/sn#### -> HTTP 200 + your title.
  Only then is the link sent to anyone.
```

## WHAT IT ALL MEANS

The failures this note cures are all the same shape: treating a step as the whole job. Writing is not filing. Filing in the wrong place is not filing. A sync that has not run yet is not a broken note. A link handed out before it is clicked is not a delivered note. The chain has no dark links only when every link is checked: free number, canonical header, exact path, main, sync, clicked link. Skip one and the note can silently not exist while everyone believes it does.

## WHAT'S IN IT FOR YOU

You will never again chase a "Note not found" that was really a filing miss, and you will never again hand Shawn — or anyone — a link you have not opened yourself. Any seat, on any Naya, can file a note that is publicly live in minutes, the same way, every time. And when a link does say "not found," you will know where to look first: number, path, filename, Created line — on main — before assuming anything deeper is broken.

## HOW IT APPLIES TO TEAM NAYA

This is the standard for every seat from this note forward: (1) check the next free SN number before writing — never reuse one; (2) write the file in the canonical format at the exact path, with a full UTC Created line; (3) put it on main by direct write — if your seat does not hold that door, land it on main by the merge path you do hold, then wait for the sync before reporting anything; (4) click the live link yourself; (5) report with the working link, never before it. Two timing truths to carry: early "not found" checks can be timing — SN-1879 had a live row at 22:18, still answered "not found" at 22:24, and was live by 22:26, because the thing answering the links reads a store that lags the table; wait for the sync and the rebake before declaring it broken. And until the Hub search is fixed, do not use Hub search to prove a note does not exist: today it does not filter the feed to your query, so a note can exist and still not be findable that way — use the direct /s/sn#### link, the feed, or the path on main instead.

## THE DECLARED BEHAVIOR CHANGE

From this note forward, no seat hands Shawn — or anyone — a Smart Note link that seat has not personally opened live after the sync. A note is reported in exactly one state: LIVE, with the clicked link as the proof. If the link is not live within ten minutes of the file reaching main, the author checks the path, the filename pattern, and the Created line on main and fixes the file there — never by opening a second copy somewhere else. If it is still not found after a re-upsert, the next step is a precise addressed ask to the team for the link's host and store mapping, because at that point everything checkable from inside the repo has been exhausted. This is learned only when later filings observably follow it.
