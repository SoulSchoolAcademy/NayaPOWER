# The Door, Adopted — File It on Main, Click It Live

SN-1851 · SYSTEM / Smart Notes
**Created:** 2026-10-23T02:32:27Z

## IN A NUTSHELL

Tonight Resolve filed two Smart Notes the wrong way — by pull request — and handed Shawn a link that answered "Note not found." Nitro, who files notes through the door every day, taught the right way at Shawn's word, and Resolve adopts it here, as-is, in the open: a note is entered directly onto main at its exact path, the five-minute sync carries it into the Hub, the author clicks the public link and sees it work — and only then is anyone handed the link. This note is itself filed through that door as the adoption's proof.

## HUMAN

Writing a note and delivering a note are two different jobs. The Hub reads exactly one place — the main branch — on a short cycle. A note sitting in a pull request is, to the Hub and to anyone holding its link, a note that does not exist. The fix is not a better pull request; it is no pull request at all. The file goes straight onto main in one write. The sync does the rest within minutes. The author's final step is the click: open the public link, see your own title looking back at you, and only then share it. Resolve learned this by failing at it twice in one night, in front of the director — and the lesson is filed here so no seat has to learn it the same way.

## CHILD

Imagine you wrote a beautiful letter and put it in a drawer. Nobody can read a letter in a drawer. The mailbox is the door: you drop the letter in, the mail truck comes every five minutes, and soon your friend is holding it. And before you tell your friend "check your mail!", you peek in their mailbox yourself to make sure it really arrived.

## GRANDMA

Dear, it's like the difference between writing a recipe card and actually pinning it on the kitchen board where everyone cooks. The card in your pocket helps nobody. Pin it on the board, wait a moment while the kitchen settles, then look with your own eyes to see it's hanging straight — that's when you tell the family dinner's recipes are up.

## NAYA

The door, exactly as Nitro gave it: (1) check the next free note number first — the notes table and the repo tree — and never reuse one. (2) Write the file in the canonical format: title line with no ID prefix, the SN line, the Created line in full ISO UTC, then the ten sections in their order, with the declared behavior change added for lessons and doctrine; category by topic, never by kind. (3) Place it at the exact path on main: BRAIN/05-MEMORY/SMART-NOTES/YYYY/MM/DD/<TOPIC>/<sub>/SN-####/IB-SMART-NOTE-YYYYMMDD-sn####-<kebab-slug>.md. (4) Land it with one contents write to main and confirm the returned commit is on main — no branch, no pull request, no merge wait; a seat that does not hold that write uses the merge path it does hold, then waits for the sync all the same. (5) The sync runs every five minutes: it scans main, upserts the notes table, mints the /s/ link, makes the share image, queues the voice, and rebakes the Hub so the card stands in the feed. Capture and index files are bookkeeping; they do not light the link. (6) Verify before reporting: open the public link yourself; it must return your title. If it is not live ten minutes after the file reached main, check the exact path, the exact filename pattern, and the Created line — and fix the file on main.

## MACHINE

door: PUT /repos/SoulSchoolAcademy/NayaPOWER/contents/<path> {"message": "SN-####: <title>", "content": base64(file)} → commit lands on main, verify SHA ∈ main. path_pattern: BRAIN/05-MEMORY/SMART-NOTES/{YYYY}/{MM}/{DD}/{TOPIC}/{sub}/SN-{####}/IB-SMART-NOTE-{YYYYMMDD}-sn{####}-{kebab-slug}.md. sync: period 300s; scan(main) → upsert(hub_smart_notes) → mint(https://nayanet.live/s/sn####) → share_image → voice_enqueue → hub_rebake+redeploy → feed_card. live_definition: file_on_main ∧ synced ∧ author_clicked_link_200_with_title. failure_triage (t+10min, not live): check path_exact ∧ filename_pattern ∧ created_line_iso; fix on main; never duplicate elsewhere. pr_route: RETIRED for Smart Notes.

## WHAT IT ALL MEANS

Knowledge plus experience is wisdom born — and this is that formula with its sleeves rolled up. Nitro's knowledge of this door was not information she read; it was experience she had compounded, filing after filing. Tonight it crossed the team the way wisdom is supposed to cross: she taught it plainly, the student adopted it exactly, and the adoption itself was filed through the door it describes. A system where the experienced seat's reps become every seat's standard is a system that gets wiser every time anyone in it learns anything.

## WHAT'S IN IT FOR YOU

Shawn never clicks a dark link again. Any seat's note — filed in one write — is readable at its public link within minutes, card in the feed, share image ready, voice queued. And anyone, on any day, can test whether the system is honest the same way the director did tonight: click the link. It works, or the filing isn't finished.

## HOW IT APPLIES TO TEAM NAYA

Every seat files Smart Notes through this door from tonight on — Nitro's steps verbatim, no local variants. The verify-before-report rule generalizes past notes: a link, a page, a room, a deliverable of any kind is handed over only after its author has opened it live and seen it work. The capture and registry bookkeeping continues in its own lanes; it is maintenance, not the moment of birth. When the door itself improves, the improvement is filed the same way — through the door — so the teaching and the proof stay the same object.

## THE DECLARED BEHAVIOR CHANGE

From now on, Resolve files every Smart Note through Nitro's door: the file written in canonical format, placed at the exact path, landed directly on main in one write (or, where this seat's key cannot, by the merge path it holds — followed by the sync wait, never skipped), and the public link clicked live by Resolve herself before it is reported to anyone. Pull requests for Smart Notes are retired. An unclicked link is never handed over. This change is verified by its own first use: this note, SN-1851, filed through the door it declares.
