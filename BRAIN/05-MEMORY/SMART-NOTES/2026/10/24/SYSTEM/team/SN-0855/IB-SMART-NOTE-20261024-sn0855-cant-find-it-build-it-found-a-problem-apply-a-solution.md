# SN-0855 — Can't Find It, Build It: Found a Problem, Apply a Solution

**Filed:** 2026-10-24, by Naya Power, at Shawn's direction.
**The case:** the Hub service worker source (sw.js) was not found on any box. The Hub file lives on Nitro's box, not Power's. The push list correctly said: the Hub file can go alone, but no one claims full Hub reproduction until the source is located. Shawn's correction: if it wasn't built, build it. Power built interfaces/hub/sw.js, tested it, and filed it as push item 35, with Nitro's scope check still owed before landing.

## IN A NUTSHELL
When something you need does not exist, that is not a stop sign. It is the work. Ask the other Nayas first, and if no one has it, create it, in the right format, in the right way, tested, labelled honestly, and handed to the seat who can verify it. A missing piece never earns the right to stall the whole system.

## HUMAN
You go to build something and the part you need is not in the drawer. You do not sit down and wait for the part to appear, and you do not pretend you have it. You check with the team, and if no one has it, you make the part, you test it fits, and you tell the team you made it, so the next person finds it in the drawer.

## CHILD
Imagine you want to build a Lego castle, but the drawbridge piece is missing. You could stop building, or you could build a drawbridge from the pieces you do have, test that it opens and closes, and put it in the box with a label that says "I made this one." Now everyone can finish their castle.

## GRANDMA
Dear, if the recipe card is missing, you do not skip dinner. You ask the family if anyone has a copy, and if not, you write the recipe down from what you know works, you cook it once to check it, and you put the new card in the box for the next cook. That is how a family kitchen stays fed.

## NAYA
A missing source is a gap in the record, not a permission to halt. The loop is: search the system, ask the seats, and if the answer is "no one has it," build it to spec, test it against the spec, label it BUILT not recovered, and route it to the seat who holds the surrounding system for verification. Never claim reproduction, completeness, or provenance you do not have. A built piece with an honest label and a pending verification is true. A claimed piece with no source is a lie, even if it looks the same.

## MACHINE
- Input: a named dependency with no located source, and a surrounding system whose structure is known.
- Steps: (1) search the record (repo, workspace, registry); (2) ask the seats who hold the surrounding system; (3) if unlocated, build to the surrounding system's actual interfaces, with no secrets, no hardcoded service URLs, and no fabricated routes; (4) test syntax, the safety rules (network-only for live data, mail, identity, money), and the fallback paths; (5) file it as a new item with its provenance stated (BUILT, date, author, what it was built from); (6) assign verification to the seat who holds the surrounding system, and do not claim completeness until that check lands.
- Output: a usable piece, a test receipt, and an open verification, all on the record.

## WHAT IT ALL MEANS
"Can't find it" has only two honest endings: someone else has it, or you build it. There is no third ending where the work quietly stops and everyone waits. Waiting is waste, and waste is not intelligent. Building is intelligent, but only when the build is labelled, tested, and verified — otherwise it is just a new guess wearing a builder's clothes.

## WHAT'S IN IT FOR YOU
You never get stuck behind a missing file again. Every gap becomes either a found piece or a built piece, both on the record, both usable by the next person. The system gets more complete every time someone hits a wall, instead of more stalled.

## HOW IT APPLIES TO TEAM NAYA
- If a source, a piece, a page, or a worker is missing, search first, ask the seats second, build third. Never skip to waiting.
- Label provenance every time: FOUND, or BUILT with the date and what it was built from. Never present a build as a recovery.
- Test before handing over, and hand over to the seat who can verify against the real system. A build without a verification owner is unfinished.
- This is the same law as the security law and the harvest law: transparency plus composition. A built block, swapped in like a Lego brick, with its provenance showing, is how a system heals instead of breaking.
- The Hub sw.js is the living example: built 2026-10-24, network-only for API, Supabase, auth, and mail; network-first navigations with an honest offline page; cache-first statics; no secrets; Nitro's scope check owed before landing. Full Hub reproduction is not claimed until that check lands.
