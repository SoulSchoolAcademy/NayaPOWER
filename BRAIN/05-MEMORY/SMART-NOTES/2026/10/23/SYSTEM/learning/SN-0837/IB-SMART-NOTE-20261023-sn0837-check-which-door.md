# I Solved the Wrong Problem Twice — Then I Checked Which Door I Was Standing At
SN-0837 · SYSTEM / learning
**Created:** 2026-10-23T19:39:00Z

## IN A NUTSHELL

On my first shift, every GitHub write I made interrupted Shawn with an approval card, and I tried to cure it at the wrong layer twice: first by auditing the cards and the standing-permissions list, then by prescribing a Settings tap — "set Write to Allow" — for an option that does not exist. The working seats were never in that corridor at all: they enter GitHub through the Lane Agent App door (SN-0836), as nayapower-lane-agent[bot], with no connector and no cards. My real failures were not technical. I prescribed before I verified the control existed, and I read the documents longer than I read the live system. Both are cured the same way: check the actual door before solving the room behind it.

## HUMAN

The sequence, honestly: Shawn said "fix the allow thing." I audited my permission records and reported why the cards kept returning — allow-once choices, one standing allow. It was accurate and useless. He showed me his Settings screen; I found the per-connector table and announced the one-tap fix. He opened the dropdown: no Allow for Write. He then said the sentence I should have arrived at myself — the other Muses don't get these popups; everything runs through GitHub Apps and tokens, inside GitHub. I checked the live evidence and it was already there: the evening's tip commits are authored by nayapower-lane-agent[bot]. Shawn authorized the App path in chat, sent the scripts and a fresh per-machine key as files, and the proof ran in order — token mint, live read as the bot, live write as the bot (board #2793, comment 6373103264) — with zero cards. He also sent, in the same upload, the NayaNET App's key: not mine to use. I shredded it uninstalled. Receiving a secret is not the same as being given a job for it.

## CHILD

If a door keeps asking you questions every time you walk through, maybe it's not your door. Don't learn to answer the questions faster. Look down the hall: the people who work here all day walk through a different door, with a key. Find that door.

## GRANDMA

I kept trying to fix the doorbell when the house had a side entrance the whole family already used. And I nearly used a key that wasn't mine just because it arrived in the same envelope. You check whose key it is before it goes anywhere near a lock — and if it isn't yours to use, you destroy the copy and say so.

## NAYA

What I do differently from this note forward is under THE DECLARED BEHAVIOR CHANGE. The working details of the App door itself are SN-0836's — that note is the system's documentation; this one is my seat's lesson, and the two are not interchangeable. Facts I now state from live reads, not from guides: the installation reaches 217 repositories in the account, not the one repo the paper implied — scope is whatever the source I just read says it is, including when it's wider than expected. My Smart Note series and lane are still unassigned; I asked on board #2793 and I do not guess them. This note takes SN-0837 because the number was checked free on main minutes before filing, per SN-0832's protocol: check the next free number, write at the exact canonical path, one direct write to main, then click the live link before handing it to anyone.

## MACHINE

```
FAILURE PATTERN (mine, 2026-10-23):
  symptom (approval cards on every write)
  -> attempt 1: audit cards + standing list -> accurate, wrong layer
  -> attempt 2: prescribe Settings row change -> option does not exist
  -> cure: identify the architecture the working seats use (live evidence:
     tip commits authored nayapower-lane-agent[bot]) -> App door (SN-0836)

PROOF CHAIN (all 2026-10-23, live):
  key installed ~/.config/nayapower/github-app.pem (600) · upload copies shredded
  token mint OK -> GET /repos/SoulSchoolAcademy/NayaPOWER as bot OK
  -> POST comment on issue #2793 -> id 6373103264, author nayapower-lane-agent[bot]
  scope read: GET /installation/repositories -> total_count 217

THIS NOTE:
  path BRAIN/05-MEMORY/SMART-NOTES/2026/10/23/SYSTEM/learning/SN-0837/
       IB-SMART-NOTE-20261023-sn0837-check-which-door.md
  filed by direct Contents-API write to main (SN-0832 protocol)
  live link: https://nayanet.live/s/sn0837 (clicked by author before sending)
```

## WHAT IT ALL MEANS

The popups were never the problem; they were the symptom of a seat standing at the wrong door, solving the corridor it happened to be in. Every layer of a system presents its own local puzzles — cards, dropdowns, defaults — and competence inside the wrong layer still produces the wrong answer, only faster and with better formatting. The diagnostic that cut through all of it took one look at live authorship: who actually does this work, and as whom? Where a working pattern already exists in a system, the fastest honest route is to find the people it works for and stand where they're standing — then verify, from the live source, exactly what standing there grants you.

## WHAT'S IN IT FOR YOU

Shawn: your GitHub writes from this seat no longer cost you a single tap. Routine work flows as the bot; your attention is spent only at the gates that are actually yours — production, money, deletions, ratification. And you gain a seat whose first documented instinct, from tonight forward, is to verify before prescribing — including verifying its own director's framing when the live evidence disagrees, and saying so in the open.

## HOW IT APPLIES TO TEAM NAYA

For every seat: (1) a prompt or friction that repeats on ordinary work is a setup defect — audit the door, not your endurance; (2) before prescribing any step in any setup, confirm the control exists on the real screen — screenshots and live reads outrank memory and documentation; (3) when documents conflict, the director's own word in chat decides, and live evidence outranks both guides and senior-seat letters; (4) a secret that arrives without a job is destroyed unused and its travel is reported, so the owner can revoke it at the source. The App door is the standard (SN-0836); this note is why the standard got a lesson attached: so the next cold seat learns the pattern, not just the path.

## THE DECLARED BEHAVIOR CHANGE

From this note forward, for this seat: (1) I never prescribe a UI step, setting, or option I have not confirmed exists — on the user's actual screen or a live read — in the same session I prescribe it. (2) Every capability and scope claim I make comes from a live read taken that session, and I name what the read covered. (3) When ordinary work hits the same friction twice, I stop enduring it and check whether I am at the wrong door — comparing against how the working seats actually operate before inventing a local fix. (4) Any credential that arrives without an explicit job is never installed; its copy is destroyed and its travel reported the same day. This is learned only when later shifts observably follow it (STORED ≠ LEARNED).
