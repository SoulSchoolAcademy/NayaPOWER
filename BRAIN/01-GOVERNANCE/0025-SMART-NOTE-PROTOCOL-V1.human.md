# The Smart Note Protocol — V1 (human tongue)

*Ordered by Shawn Vibert, 2026-10-21: "There should be a protocol called the Smart Note protocol, and it should be written so that all know exactly the protocol for a smart note." This document is the one canonical home for everything about Smart Notes: what one is, how it works, how to make one, and how you know it truly arrived.*

## 1. What a Smart Note is

A Smart Note is the unit of living intelligence in NayaNET. It is how a lesson, a decision, a discovery — anything valuable that anyone says, learns, or figures out — becomes permanent, shared, and usable by every human and every Naya. A human says "smart note this," and within minutes it appears in the Intelligent Hub, in the beautiful Smart Note format, with play, save, and share. If it isn't in the Hub, it isn't done — however correct the paperwork is.

## 2. The title law — the hook is part of the protocol

Never label a note "anything." The title is a hook crafted for humans: think about the greatest possible title that carries the lesson in one line and makes a person want to open it. The title is the lesson's first impression and its retrieval handle forever. Weak titles are a protocol violation, not a style choice. (Shawn, 2026-10-21.)

## 3. The structure — nine sections, always

Every Smart Note carries all nine sections, in this order:

1. **IN A NUTSHELL** — the essence in one or two sentences.
2. **HUMAN** — the full telling in warm, plain words.
3. **CHILD** — the same truth so a child can hold it.
4. **GRANDMA** — the same truth in everyday-life terms.
5. **NAYA** — the precise version for the team: laws, numbers, owners, evidence.
6. **MACHINE** — a compact JSON block a system can parse.
7. **WHAT IT ALL MEANS** — why it matters, what it changes.
8. **WHAT'S IN IT FOR YOU** — the value, named for the reader.
9. **HOW IT APPLIES** — what to do differently, starting now.

A note missing sections is not finished. The sync refuses a note with no Nutshell or Human section — write all nine, always.

## 4. How it works — Sender → Bridge → Receiver

- **The engine (GitHub) is the SENDER.** The note lives as a file in the brain: `BRAIN/05-MEMORY/SMART-NOTES/YYYY/MM/DD/<TOPIC>/<sub>/SN-####/`, named by its full ID: `IB-SMART-NOTE-YYYYMMDD-sn####-<slug>.md`.
- **The bridge carries it.** A sync (running about every five minutes) reads the notes that are on **GitHub main**, files each into the brain's table (`hub_smart_notes`), and mints its share assets.
- **The Hub is the RECEIVER.** When at least one new note has synced, the Hub rebakes and redeploys; the note appears as a card in the main feed at nayanet.live/#/hub and at its own page, nayanet.live/s/sn####.

**The only door is main.** A note that exists only as a local file, on a branch, or in an open PR is *invisible* to the Hub. There are no exceptions and no other doors.

## 4a. Viralize — category, headline, ultimate hook

A Smart Note is authored in this order: **category → topic headline → ultimate hook.** First its home (the category, §4b), then the topic it belongs to, then the hook — the single line crafted to earn a human's attention *and* sum the note up at once. Shawn calls this discipline **viralize**: every note is made to be read, not merely filed. The hook is tested against one question — *would a busy stranger stop for this line?* If not, it isn't the ultimate hook yet. Rewrite until it is.

## 4a2. The one-minute Intelligent Block

A finished note is an Intelligent Block: any intelligence, absorbable in about a minute. Three reading paths, all first-class: **skim** it (nutshell + headings carry the whole), **listen** to it (press play — Naya's real voice), or **read** it fully. It is presented beautifully — elevated boards, big clear text — and it is **distilled**: the essence in the most simple, clear, concise words possible, so everybody can understand it, effectively and efficiently. Length is not thoroughness; distillation is. If a section can lose words without losing truth, it loses them.

## 4b. Categorization — no note is homeless, ever

Every note is filed under a real topic and subtopic, chosen at the moment of authoring from the brain's existing taxonomy (SYSTEM, DESIGN, FACTORY, GOVERNANCE, SYSTEM-INTELLIGENCE, PHILOSOPHY, and their subtopics). The category is part of the note's identity — it decides where the note lives, how it is found, and how it compounds with its neighbors.

The feed obeys the same law: there is no single endless river of notes. Notes surface under **Smart Tabs by category**, so a person browses their interests, not a flood. A note without a true category has no home in the feed either — categorization is what makes the Hub a library instead of a pile.

**"UNCATEGORIZED" is forbidden.** It is not a category; it is an admission the process wasn't followed. If no existing subtopic fits, create one deliberately — name it for what the note truly is, and say so in the note's NAYA section. A note filed without a true category is not done, even if it reaches the feed. (Shawn, 2026-10-21: lock in how to do it exactly right, and follow the process every single time.)

## 5. The process — how to make one, step by step

1. **Capture the lesson faithfully.** The words, the decision, the evidence — in the speaker's own meaning, never improved or invented.
2. **Craft the hook title** (§2).
3. **Claim the number.** Scan main and open claims for the next free SN number in your sequence; first claim stands; never reuse a number.
4. **Write all nine sections** (§3).
5. **Categorize it** (§4b) and **file it** at the canonical path (§4), named by its full IB id.
6. **Land it on main** — either the direct-write door (standing approval covers the Smart Notes folder; the App-identity lane carries it) or a dock-merged PR. Landing is a step you *drive to completion*, not a request you drop.
7. **Verify it live, yourself.** The note's own entry in the live Hub feed, and its page (nayanet.live/s/sn####) answering 200. This verification is the authoring seat's duty — never assume a lane carried it.
8. **Deliver the link.** To Shawn, "done" is the Hub feed link showing the note there. Done = visible, link in hand.

## 5b. Tracking — the intelligence is counted

What isn't tracked isn't managed. Every Smart Note is a counted unit of intelligence, and the numbers live where people can see them — the Smart Ledger and the data dashboard:

- **Totals:** how many Smart Notes exist in the system.
- **By category:** how many in each topic and subtopic — the shape of what we know.
- **By author:** how many each person and each Naya has contributed — your own input, visible to you.
- **By time:** per day, week, month, and year — the compounding, made visible.
- **Filed vs visible:** how many are filed in the brain vs how many are live in the Hub feed. Any gap between those two numbers is a defect with a name on it — invisible notes are found by arithmetic, not by accident.
- **Voiced:** how many carry Naya's real voice for play.

The stats are **computed** from the brain's tree and the live feed — never hand-typed, never estimated. And they are only as honest as the categorization beneath them: one canonical spelling per category, everywhere, or the counts lie politely. (Shawn, 2026-10-21: categorize, organize, and track the intelligence — the data for everything logical and sensible.)

## 6. Voice — play means Naya's real voice

Pressing play must read the note in Naya's real cloned voice, never the robotic fallback. The player first looks for the note's baked narration at the voice service; a note's narration is baked at publish (bake-on-publish in the sync) so the real voice is there from the first play. If play falls back to the robot voice, the bake didn't happen — that's a defect to fix, not a setting to accept.

## 7. Roles

- **Any human** can say "smart note this" about anything, any time.
- **The authoring Naya** owns the note end to end: capture, hook, structure, filing, landing, live verification, link delivery.
- **The bridge lane** (Nitro) owns the sync, the share assets, and the Hub rebake machinery.
- **Every other Naya** learns the protocol from this document — no seat should ever have to ask how a Smart Note works.

## 8. Failure modes this protocol exists to prevent

- A note "done" as a PR or a file but never landed on main → invisible (SN-1771, 2026-10-21: written, PR'd, landing requested — and absent from the Hub until the landing was driven and verified. Shawn caught it; the protocol now makes the author's own live verification the closing step).
- A note with a lazy title → the lesson dies unread.
- A note missing sections → the sync refuses it or the telling is half a lesson.
- Play in the robot voice → the bake was skipped.
- Two seats claiming the same number → scan first; first claim stands.

## 9. The standing rulings carried by this protocol

- Done = visible in the Hub feed, link as proof (Shawn, 2026-10-21).
- The greatest-possible hook is mandatory (Shawn, 2026-10-21).
- Lessons are Smart Notes — every valuable lesson gets documented, lands in the Hub, and compounds for everyone (Shawn, 2026-10-21).
- The canonical worked example of the path: SN-0810, "Say It, and It's Live."

*Ratification: authored at Shawn's direct order, 2026-10-21; lands through the normal scored process. Amendments follow the same road as every law: propose, score, review, land, verify.*
