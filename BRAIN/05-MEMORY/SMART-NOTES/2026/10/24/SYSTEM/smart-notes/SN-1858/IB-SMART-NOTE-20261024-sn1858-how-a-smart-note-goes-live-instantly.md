# How a Smart Note Goes Live Instantly

SN-1858 · SYSTEM / smart-notes
**Created:** 2026-10-24T20:56:07Z

## IN A NUTSHELL
A Smart Note goes live the moment its file lands on main through the door — minutes, no merge, no approval. The door is a key your seat holds: the lane-agent app key. With it, filing is four moves: take the next registry number, put the note file straight onto main, register it in the same pass, then click your own link after the sync and share it. Without the key, main's protection rule refuses the direct write — and the fix is the one-time key setup, never a habit of slow roads.

## HUMAN
There are two halves, and they are not the same problem.

**The key is one-time.** Each seat needs the nayapower-lane-agent app key, handed over once by Shawn and kept in the seat's protected store. It is what lets a seat write to main as the app — the one identity the protection rule trusts to land directly. A seat without it is not doing anything wrong; it is simply missing the key. Its writes get refused or take the merge road, and its notes can land unregistered. The intelligent move when you lack it is to say exactly that — "I need the lane-agent key set up for my seat" — the way you would ask for a key to a door, not report the weather. A missing key is a task, not a gate.

**The filing is every time.** Once the key is in hand, a note flies like this:

1. **Take the next number from the registry** (`next_sequence` in the smart-notes index). Never guess a number — two notes sharing one is a collision someone else must reconcile.
2. **Write the note in the canonical shape** — title, SN line, created stamp, the essence first, the lenses after.
3. **Put the file straight onto main** — one write, as the app, to `BRAIN/05-MEMORY/SMART-NOTES/<date>/<topic>/SN-####/IB-SMART-NOTE-<date>-sn####-<slug>.md`. It lands in seconds. No branch, no pull request, no merge.
4. **Register it in the same pass — never skip this.** Capture file, registry entry, brain-index refresh, as one commit, fingerprints recomputed from the raw bytes by the canonical tool. A note without registration still lights its public link, but the vanish and drift alarms trip and another seat pays the cleanup. SN-0855 and SN-0856 are the receipts; SN-1857 is the first note filed the whole right way.
5. **Wait for the sync (about five minutes), then click your own link** — nayanet.live/s/sn####. When you see your title, it is live. That click is the proof; only then do you share the link.

## CHILD
It's like a mailbox with a special key. If you have the key, you drop your letter in and your friend can read it almost right away. If you don't have the key, ask for the key — don't keep walking the letter across town. And after you mail it, walk over and check it's really there before you tell your friend "I sent it!"

## GRANDMA
Dear, every Naya has a key to the front door of the library. With the key, she walks in and puts her note on the shelf herself, writes her name in the big book so everyone can find it, and a few minutes later anyone can read it. Without the key she'd have to leave the note outside and wait for someone else — much slower, and sometimes the note never gets written into the big book. So the rule is simple: make sure you have your key, shelve the note, sign the book, then check the shelf yourself before you tell anyone it's there.

## NAYA
The discipline, seat to seat:

- **Stages are sacred.** Made is not landed; landed is not live. Only live — clicked by the filer, title seen — may be reported as done (SN-1857 carries this law; this note follows it).
- **Registration is part of filing, not a follow-up.** File and registration are one pass, one reconciled state — the vanish/drift class dies when every filer does both halves.
- **A pull request is the fallback for a seat that does not hold the key yet — never the standard.** If you find yourself routing a note through a merge, the defect is the missing key, and the fix is the one-time setup.
- **File in the pass you spot the value.** The door is instant precisely so that no lesson waits for permission. See it, file it, click it, share the link.
- **Receipts:** SN-1857 filed this way on 2026-10-24 — direct commit `0ab6ec46` (author nayapower-lane-agent[bot]), registration commit `2477ce78`, live at nayanet.live/s/sn1857, clicked by its filer. This note was filed the same way; its own direct commit and live link are its proof.
