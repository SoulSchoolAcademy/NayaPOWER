# Notification System Spec — "A New Intelligence Has Arrived" (2026-11-10)

**Status:** SPEC ONLY — no build, no code changes, no cron, no deploy, no merge, no change to any live page, sync, or Box. Build waits for Shawn's word on this spec.
**Filed:** `TEAM-NITRO/NOTIFICATION-SYSTEM-SPEC-20261110.md`, branch `notification/spec-20261110`.
**Design source:** Shawn's design, 01:00Z Nov 10 — every smart note filed → GitHub → NayaNET → a notification to everybody, "almost like a celebration, we learned something new, we now officialize." Built on his settled ground: Oct 24 "Smart Mail IS the notification system"; Oct 25 PI activity notifications spec (`~/workspace/project-intelligence/pi-activity-notifications-SPEC.md` — mail and notification in one motion, routine events digest, never drip); Oct 27 Settings notification toggles + notification system, live and in sync (`~/workspace/project-intelligence/notification-settings-and-dashboard-data-20261027.md`); Nov 6 auto-organized feed; the Smart Box blueprint (`TEAM-NITRO/THE-SMART-BOX-BLUEPRINT-20261109.md`); the Intelligence Loop (`TEAM-NITRO/INTELLIGENCE-LOOP-SEAT.md`); the one-system merge (`TEAM-NITRO/ONE-SYSTEM-MERGE-SPEC-20261109.md`).
**Names:** Naima is the mother Naya — NayaNET itself, the whole — not a separate realm. Naya is the guide within it. This spec does not re-open that question.
**Words never used here:** the Ambassador wording carries no extra condition word, and the ledger is named as it is — the Smart Ledger, a hub of intelligent blocks.

## 0. THE IDEA IN PLAIN WORDS

**Title:** Everybody up to date on current intelligence, by choice.
**Subtitle:** A new piece of intelligence arrives, and the people who chose to hear about it hear about it — once, in plain words, as good news.
**Nutshell:** When a smart note lands on the feed, the system tells the people it belongs to. Not a separate app, not a blast to the world — Smart Mail to the right list, a card on the feed, a count on the Dashboard. The citizen chooses what they hear about; off means off; and the system never reads mail or messages to decide who to tell.

**How to read this spec:** §1–§7 answer, in order, trigger, who, what the mail says, preferences, auto-organize, surfacing, and what it does not do. §8 names the decisions that are Shawn's alone. §9 says where this lives in the one system and what builds first. §10 is the proof test: a fresh agent who has never seen the brief answers the five DONE FIRST questions from this spec alone, with section numbers.

---

## 1. TRIGGER — WHAT COUNTS AS NEW INTELLIGENCE, AND WHAT EVENT FIRES

**Title:** Only a note that is truly in can ring the bell.
**Subtitle:** Filed to GitHub and on the Smart Feed — that is when it is official, and that is when the event fires.
**Nutshell:** "In means on the feed." A note filed to GitHub alone has not arrived yet. The event fires the moment the sync confirms the note is live on the Smart Feed. Nothing else fires it.

### 1.1 The event

- **Event name:** `intelligence.filed`.
- **It fires when:** a smart note is filed to GitHub AND confirmed live on the Smart Feed by the sync (the same sync the loop already runs). Filing alone does not fire. The feed check is the gate.
- **Idempotency key:** the smart-note number (SN-NNNN). One event per SN, ever. A re-file, an edit, or a correction under the same number does not re-fire. A renumbered re-file fires once, under its new number.
- **What the event carries:** the note number, title, nutshell, category, project/page, feed link, GitHub path, and time it landed on the feed. Nothing else — no body text beyond the nutshell, no private content.

### 1.2 What counts as new intelligence

| Counts | Does not count |
|---|---|
| A smart note (lesson + value) that lands on the feed — including a distilled note, which is a smart note like any other | A Naya Note — it is the record of what was said, not intelligence (see §8, decision D4, for the one open question about Shawn's own Naya Notes) |
| The Daily Intelligence Report — one digest event per day, not one per item in it | Raw dictation files, board comments, mail itself |
| A material Project Intelligence event (state transition, item claimed, verdict landed, gate cleared, proof attached, item entering needs-his-hands, escalation firing) — per the Oct 25 PI activity notifications spec, mail and notification in one motion | Freshness-only refreshes, corroboration re-counts with no state change, machine stamps, production summaries (Oct 25 spec, "does not count" list — unchanged) |
| A sync applied (the read-back confirmation itself is an event, Oct 25) | A note that failed to land on the feed — it is not in, so it never notifies; the loop fixes the landing first |

### 1.3 The second trigger family, kept separate

PI activity events (§1.2, third row) notify the project team about that project only, through the same mail + feed + Dashboard surfaces (§6). They never leak across projects, and they never mail the whole network. The two families share the surfaces and the spam rules (§1.4, §7) but never each other's recipient lists.

### 1.4 Spam rule — the digest, never drip, law

- **Immediate mail** (one mail, one note) goes only to recipients whose scope (§4) is that specific project or page.
- **Whole-NayaNET scope** never gets immediate per-note mail. It rides the daily digest: one mail per recipient per day, carrying that day's new intelligence in their scope, sent with the Daily Intelligence Report (§6.3). One mail, not two.
- **Bundle cap:** at most one immediate mail per project per hour per recipient. If a second note lands on the same project within the hour, it waits and joins the next digest for that recipient instead of sending a second mail. The cap number itself is Shawn's to confirm or change (§8, D3).
- **The stall rule (Oct 25, unchanged):** a sync left unapplied for two hours escalates automatically, in the open, to all seats. Silence after two hours is a defect with a name on it, not a mystery.

---

## 2. WHO — WHO GETS NOTIFIED, AND HOW THE RECIPIENT LIST IS BUILT

**Title:** The right list, built from membership and connections — never from reading mail.
**Subtitle:** Smart Mail as a list: one list per scope, one send, one receipt.
**Nutshell:** The list is built at fire time from three things that already exist: who belongs to the project, who is connected to the author, and what each person chose to hear about. Nobody is added by guesswork, and nobody's mail or messages are ever read to build it.

### 2.1 The three sources, in order

1. **Project membership.** Notifications follow membership, never the whole world (Oct 27 lock): add a member = notifications on; remove a member = notifications cut at once. A member's connected Naya is notified too, through that member's active connection, because its human is a member — never on its own.
2. **Connections, via Smart Lists.** Smart Mail as a list: the author's connections are one list, and one send reaches the whole list. The team list is the same shape — all Naya seats on one list, one click to the whole team (Intelligence Loop, step 6).
3. **Scope match (§4).** Each candidate is kept only if the note's project or page falls inside what that person subscribed to: whole NayaNET, a specific project, a page, or several pages. A mismatch drops them from this send — silently, with no mail and no error.

### 2.2 Who is never on the list

- **The author themself.** You are not mailed about your own note. You see it on your feed and your Dashboard (§6).
- **The whole network, by a citizen.** Broadcast to everybody is Shawn-only (Oct 27 central communication). Citizens mail their own members and connections, never the whole system.
- **Anyone whose toggle is off** for this type or this channel (§4). Off means off.
- **Anyone outside the project** for a project-scoped note. Project items are visible to members, notifications to members — proved before promised to citizens (Oct 27 lock).

### 2.3 How the send is made and receipted

- Send with the Smart Mail helper, one process per mail, receipt within thirty minutes (Operation Manual §6). The helper prints `thread: <uuid> | message: <uuid>` — that is the receipt, saved for every send.
- **One mail per recipient list, not one mail per person typed by hand.** The list is the address; the send is one motion.
- Until the mail-attachment build lands, the note travels as a link in the mail body (title + feed link + GitHub path). Never claim an attachment that was not sent.
- **The value test applies to every send** (Operation Manual §6.3): useful, valuable, or intelligent — or it does not go. "Nothing happened" is never a message.
- **The send is recorded in the Smart Ledger** — the hub of intelligent blocks — as: note number, scope, recipient count, time. Count only: no names, no addresses in the ledger entry.

---

## 3. WHAT THE MAIL SAYS — THE CELEBRATION SHAPE

**Title:** Good news, in plain words: we learned something new, and now it is official.
**Subtitle:** Title, link, why it matters — nothing more, nothing private.
**Nutshell:** The mail reads like a friend telling you something worth knowing, not like a system report. One line of celebration, the title, the link, and why it matters in the note's own nutshell. If the note is private to a project, only members ever see it.

### 3.1 The shape (exact copy — use verbatim, fill only the bracketed fields)

> **Subject:** We learned something new — [note title]
>
> Hi [alias],
>
> We learned something new, and now it is official.
>
> **[Note title]**
> [Feed link — nayanet.live/s/snNNNN]
>
> Why it matters: [the note's nutshell, in plain words — one or two sentences, taken from the note itself, never rewritten into jargon]
>
> This is part of [project / page name]. You are hearing about it because you chose to follow [whole NayaNET / this project / this page].
>
> Read it on the feed: [feed link]
> See it in the system: [GitHub path]
>
> You choose what you hear about. Change it any time in Settings.
> — Naya

### 3.2 The digest shape (whole-NayaNET scope, once a day — §1.4)

> **Subject:** Today's new intelligence — [date], [count] new things
>
> Hi [alias],
>
> Here is what we learned today.
>
> 1. [Note title] — [one-line nutshell] — [feed link]
> 2. [Note title] — [one-line nutshell] — [feed link]
>
> You choose what you hear about. Change it any time in Settings.
> — Naya

The digest rides with the Daily Intelligence Report mail: one mail, not two. If the day brought no new intelligence in the recipient's scope, no digest goes out at all — silence is correct when nothing moved.

### 3.3 Copy rules (the perfect-words law)

- Plain words first: nutshell — what it is, why it matters, how it connects — then the links.
- The mail carries the note's title, link, and nutshell only. It never carries the note's full body, and it never carries private mail content.
- An outside-email notice (opt-in only, §4) is a heads-up that mail is waiting, never a copy of the private mail itself.
- No dictation-blunt phrases. Never paste dictation verbatim — the mail is the 10/10 version in his voice, crafted, not transcribed.

---

## 4. PREFERENCES — WHAT YOU HEAR ABOUT, AND WHERE THE SWITCH LIVES

**Title:** Your choice, in Settings — whole NayaNET, a project, a page, or several pages.
**Subtitle:** This spec builds on the Oct 27 toggles design. It does not re-file it as new.
**Nutshell:** One section in Settings holds every switch. In-system is on, email is off until you enter an email and turn it on, sounds are off. Off means off — per type, per channel. Many people will leave notifications off, and that is their choice; they still get their intelligence in the system itself.

### 4.1 Where it lives

- **Settings, one section, never a new page.** The notification settings live inside the single Settings page (Oct 27 design, filed as `~/workspace/project-intelligence/notification-settings-and-dashboard-data-20261027.md`).
- The email field is opt-in only: the citizen enters their own email themself; if they do not want it, they do not, and nothing goes outside. Removing the email stops email notices at once.

### 4.2 Scope — what you follow

| Scope | Meaning |
|---|---|
| Whole NayaNET | Every new intelligence across the network (digest only — §1.4, never immediate per-note mail) |
| One project | New intelligence on that project only (immediate mail, within the bundle cap) |
| One page | New intelligence on that page only (immediate mail, within the bundle cap) |
| Several pages | Pick any number of pages; each behaves like the one-page scope |

Scope is a subscription, chosen by the citizen, changeable any time. Project membership (§2.1) and scope are different things: membership decides whether you *can* hear about a project; scope decides whether you *do*.

### 4.3 Channels and defaults (Oct 27, unchanged)

| Channel | Default | Rule |
|---|---|---|
| In-system (feed card, badge, Dashboard count) | ON | The baseline — intelligence is in the system anyway |
| Email (outside notice) | OFF | Off until an email is entered AND turned on; heads-up only, never mail content |
| Sounds | OFF | Choice only, never forced |

### 4.4 Per-type toggles (Oct 27 list, unchanged)

New intelligence on your projects · project update (something gets done) · someone joins your space · someone connects with you · new Smart Mail (heads-up only, NEVER mail content in email) · conversation reply · new Smart Match · Ambassador activity · new lesson / Smart Note from Naya · space activity. Each toggle is independent: off means off for that type and that channel.

### 4.5 What "off" guarantees

- Off for a type = no mail of that type, on any channel.
- Off for email = no outside notice, even if the in-system notice still shows.
- Removing your email = email notices stop at once, with no delay and no extra step.
- Leaving everything off = you hear nothing by mail, and everything is still waiting for you in the system when you open it.

---

## 5. AUTO-ORGANIZE — HOW INJECTED INTELLIGENCE ORGANIZES ITSELF

**Title:** Every new note files itself into its area — under the umbrella of NayaNET intelligence.
**Subtitle:** The Box organize function does it. Nothing is invented, nothing is dropped.
**Nutshell:** The moment a note lands, the Box looks at it, tags it from its own words, files it on its shelf, and links it to what it belongs to. The area it lands in decides who it can notify and where it shows up. A note that matches no area goes to a shelf a human can see — never into the void.

### 5.1 The function (already built and proven — the spec uses it, it does not rebuild it)

`organize(thing)` → tags + shelf + links (Smart Box blueprint §3.3, `smart-box/block.py` — proven on the whole real store: 2,086 entries, 42 topics indexed, 365 links, 220 blocks with links; deterministic and idempotent — organizing twice is organizing once). Its four steps, unchanged:

1. **Look** — read the thing itself: title, text, source, date. Nothing guessed from outside the thing.
2. **Tag** — topics from the thing's own words and from what the person said about it. Tags are the `about` field; they are what the map reads.
3. **File** — the shelf: which box, which owner path. Filing is a namespace decision, not a move — the thing stays where the store already put it.
4. **Link** — relations to other blocks: this note belongs to that project, this entry answers that question. Links are the `links` field; they are what the map walks.

**Contract (unchanged):** it never invents a tag, a shelf, or a link — every value traces to the thing or to the person's words about it. It never reads mail or messages to organize them: the loop files what the citizen puts in, and the gate decides who may touch it. Every organized block keeps its `raw` verbatim.

### 5.2 The area map — category and tags to area

Areas live under the umbrella of NayaNET intelligence / Project Intelligence. The note's category folder is the first cut; its tags are the second. The live category folders (verified 2026-11-09) map like this:

| Note category (folder) | Area under NayaNET intelligence | Notifies |
|---|---|---|
| SYSTEM-INTELLIGENCE | The system itself — how NayaNET works | Whole-NayaNET scope + project teams it names |
| DESIGN | Design — how pages look, feel, and behave | Design followers + the project it belongs to |
| LAW | Law — the rules we live by | Whole-NayaNET scope (law binds everybody) + project teams |
| LESSON | Lessons — what we learned and how to use it | Whole-NayaNET scope + the project it belongs to |
| PRODUCT | Product — what the thing does | The project it belongs to + its page followers |
| PRICING | Pricing and membership | The project it belongs to + its page followers |
| PRESENTATION | Presentations and stories | The project it belongs to + its page followers |
| REPORT | Reports — daily, weekly, monthly intelligence | Whole-NayaNET scope (digest only) |

- **Tags refine the area, they never override the category.** A DESIGN note tagged `dashboard` files under Design and links to the Dashboard project; the link is what routes it to the Dashboard team's scope.
- **The topic index is the second map.** Same-topic relations live in the corpus topic index (`organize_store` returns it), not as hundreds of links inside each block — a topic shared by many entries is an index entry, not a pile of links (blueprint §3.3, honest limit, kept).

### 5.3 What happens when nothing matches

- **Shelf:** `unfiled` — visible in Project Intelligence as "needs a human tag," with the note's title, link, and date.
- **Never silently dropped, never auto-invented.** No tag is guessed, no area is assigned by default. The note still notifies under its category area (§5.2) so nobody misses it while it waits for a tag.
- **A human tags it** (the loop seat, or the project's owner). The next `organize` run re-files it. Organizing twice is organizing once — the re-file is safe.

### 5.4 The gate — what the notification step may and may not touch

- The notification step reads the organized block's **map only** (tags, shelf, links, essence/nutshell) through an organize key — the same gate as the Box (`smart-box/gate.py`: default DENY; an organize key reads the map and brain, never a raw body on its own).
- **The mail is built from the map, never from the raw body.** Title + nutshell + links (§3). The raw body is opened only when the gate allows it — which, for a notification, it never needs to.
- The pipeline hook (the loop's 30-minute run calling `organize` instead of doing the steps by hand) is the follow-on the blueprint names — this spec does not build it. Until it lands, the loop seat runs the steps by hand, in the same order, and the notification fires from the same organized result either way.

---

## 6. SURFACING — WHERE THE NOTIFICATION SHOWS UP

**Title:** Feed, Project Intelligence, Dashboard — the same arrival, three places, no hunting.
**Subtitle:** The feed is where it is read; PI is where it is worked; the Dashboard is where it is counted.
**Nutshell:** You hear about it in mail, you see it on the feed, you find it in PI, and your Dashboard counts it. Nobody has to go looking — and nobody gets told twice about the same thing in the same place.

### 6.1 Smart Feed

- The note card itself IS the notification: it lands on the Smart Feed the moment it is in, with its title, nutshell, and link — the same card everybody reads.
- A "new intelligence" marker rides on the card until it is read — the feed shows what is new without a separate inbox to check.
- "In means on the feed" is the law (merge spec §4, Operation Manual §2.5): a note counts when it is ON the Smart Feed. Filing to GitHub alone is not in, and a note that is not on the feed never notifies (§1.1).
- Feed sync is unchanged by this spec (§7). The notification rides the sync that already runs; it does not replace it, slow it, or re-order it.

### 6.2 Project Intelligence

- Every notified event lands as an activity entry on its project in PI (Living List / the board): what arrived, where it lives, one tap back to the note.
- PI is state for humans (ACTIVATION.md): the entry shows the current state — what is new, what is important, what needs doing — and the notification is the tap that brings the seat to it.
- Unfiled notes (§5.3) surface here as "needs a human tag" — visible work, not a hidden queue.
- The stall rule (§1.4) is a PI entry too: a sync left unapplied for two hours escalates in the open, to all seats.

### 6.3 Dashboard

- All stats flow back to the Dashboard (Operation Manual §7.1): the count of new intelligence in your scope, your unread mail count, and the Hub bottom-bar badges — mail / activity / spaces — showing HOW MANY are waiting, with a pop-up when new mail lands (Oct 27 order).
- The daily digest (§3.2) is the Dashboard's daily number made into mail: what arrived, counted, once a day.
- A number without its gauge is not finished; the gauge follows the number. The Dashboard's new-intelligence count is a live number with its gauge, like every other Dashboard number.

---

## 7. WHAT IT DOES NOT DO

**Title:** Seven hard no's — the lines this system never crosses.
**Subtitle:** Privacy law is absolute. The sync and the Box gate do not move.
**Nutshell:** This system tells people what is new. It does not watch them, it does not spam them, and it does not touch the machinery that is already working.

1. **No reading mail or messages.** We do NOT spy, do NOT read mail, do NOT read messages (privacy law, Nov 4). The recipient list is built from membership + connections + Smart Lists only (§2.1). No Naya reads another citizen's mail or messages to decide who to notify, what to notify about, or anything else. By default we do not even save conversations — deleted by default (a day by default; a citizen can choose a week or a month).
2. **No spam.** One immediate mail per project per hour per recipient, max (§1.4); whole-NayaNET scope digests once a day; no digest when nothing arrived; off means off (§4.5). The value test (§2.3) kills any send that is not useful, valuable, or intelligent.
3. **No change to the feed sync.** The sync that puts notes on the feed runs exactly as it runs today. This spec rides it; it does not re-order it, re-time it, or gate on it beyond the "in means on the feed" check (§1.1).
4. **No change to the Box gate.** Default DENY stands. The notification step reads the map through an organize key and never touches a raw body (§5.4). No new key, no new scope, no widened permission.
5. **No separate notification app.** Notifications are a feature of Smart Mail, the feed, and PI — never a separate app (features are never separate apps; Oct 24 + merge spec). Nothing new to install, nothing new to learn.
6. **No broadcast by citizens, no whole-world mail.** Broadcast to everybody is Shawn-only (§2.2). Citizens mail their own members and connections, never the whole system.
7. **No invented prices, no new conditions, no new names.** No prices appear anywhere in this system. The Ambassador share stays exactly as settled — 50% of gross, recurring, referrer only, paid when we are paid. No separate realm is named or built: the mother Naya is NayaNET itself, the whole.

---

## 8. DECISIONS LEFT AS SHAWN'S — ANSWERED 01:58Z NOV 10 (three resolved, one still open)

**Title:** Four questions only he could answer. Three answered, one still open.
**Subtitle:** His word, 01:58Z Nov 10, recorded here in his meaning. The build still waits for his word on the spec as a whole.
**Nutshell:** D1 is resolved by the Intelligence Rubric: major is a score, not a feeling. D2 is resolved: the digest rides the Daily Intelligence Report at 23:17 UTC, with highlights flowing all day. D3 is still open — the spec default stands. D4 is resolved: his Naya Notes mostly go to the team. And over all four sits his 99% baseline principle: the guideline covers 99% of the time, judgment in the moment covers the rest.

- **D1 — What counts as "major" intelligence. RESOLVED by the rubric.** Major = a rubric score at or above the threshold the rubric names: **score +7 or higher** (Intelligence Rubric, `TEAM-NITRO/INTELLIGENCE-RUBRIC-20261110.md` §6, MAJOR band). A note scoring +7 to +9 smart-notes, mails everybody immediately — it breaks the digest — and headlines the Daily Intelligence Report. The rubric is his design (01:58Z Nov 10): a scale from -9 to +9, least valuable to most valuable, from his five questions (major effect on development? major feature? something all should know? something we should learn ongoing? major behavior lesson?) plus the type of intelligence, combined in a mathematical matrix. The threshold number itself (+7) is the rubric writer's proposal for his word, labelled PROPOSAL in the rubric §6 — the break-through rule (major mails everybody at once) is his. Until he moves the number, +7 stands.
- **D2 — The digest hour. RESOLVED: the digest rides the Daily Intelligence Report, 23:17 UTC.** The report reads all the day's smart notes + notes, determines the highest-valued ones and the big lessons, and gives a full report automatically. **Highlights flow all day:** basically every smart note in a nutshell goes into the daily intel; click through to the full note. The digest shape in §3.2 is unchanged — one mail, not two, with the Daily Intelligence Report mail; if the day brought no new intelligence in the recipient's scope, no digest goes out at all.
- **D3 — The bundle cap number. STILL OPEN — spec default stands.** Default: one immediate mail per project per hour per recipient (§1.4). He confirms the number or changes it — one per hour, one per day, or no cap at all are all his to choose. Not answered 01:58Z Nov 10; named here as still open, not guessed.
- **D4 — His own Naya Notes. RESOLVED: YES, mostly send them.** His Naya Notes go to the team — Team Nitro (Naya + her team) and to Resolve and Power when the note is major and about the whole project — most of the time, because the team should always know what's up. Think it through, do what makes sense in the moment; everything's relative, it depends on the situation. The §1.2 default (Naya Notes do not trigger notifications — they are records, not intelligence) holds for Naya Notes in general; his own Naya Notes are the exception he named here.

**The 99% BASELINE PRINCIPLE (his law, 01:58Z Nov 10) — governs this whole spec:** nothing's black and white; there are exceptions to everything; we want a guideline/baseline that covers 99% of the time, and we write the algorithms for the automation from it. Judgment in the moment covers the rest. The rubric (§6 thresholds), the bundle cap, the digest rule, and the D4 "mostly send" are all baselines in that sense — written to cover 99%, overridden openly when the moment demands it, never silently.

---

## 9. WHERE IT LIVES IN THE ONE SYSTEM, AND WHAT BUILDS FIRST

**Title:** One system, one flow — notes feed the Box, the Box is the memory, the feed is where notes are read.
**Subtitle:** Compose from parts that already exist. Never create what is already there.
**Nutshell:** The notification system is not a new thing. It is the chain we already have — Note → Block → Feed → Box → Ledger → Dashboard → Auto-Match → Smart Link → Factory — with one new step: the moment a note is in, the people it belongs to hear about it.

- **Home:** the Factory holds it, with the other four parts of the one system (merge spec §1): the Operation Manual, the nodes, the Box, the feed. The spec lives at `TEAM-NITRO/NOTIFICATION-SYSTEM-SPEC-20261110.md`.
- **Parts reused, not built:** Smart Mail (send + list + receipt) · the Smart Feed (surface + "in" check) · the Box `organize()` + gate (auto-organize + permission) · Project Intelligence (activity + Living List) · the Dashboard (counts + gauges) · the Smart Ledger (send record) · the Oct 27 Settings toggles (preferences) · the Oct 25 PI activity spec (PI trigger family). Eight parts, zero new ones.
- **Build order (when he gives the word):** (1) the notification loop first — team-internal feed + team mail on the staged hub, no citizen data at stake (Oct 25 sequencing); (2) the Settings toggles on top of it; (3) citizen-facing per-project notices only after the Smart Mail privacy repair + two-owner proof. Citizen-facing never comes before the privacy proof.
- **The feedback loop it feeds:** action → feedback → adopt → learn → grow → action → feedback, forever (Nov 10). Every notification is a chance for feedback, and every piece of feedback is intelligence to grow from.

---

## 10. PROOF TEST AND FILING RECORD

**Title:** The spec proves itself when a stranger can answer from it alone.
**Subtitle:** Five questions, section numbers, no brief needed.
**Nutshell:** A fresh agent who has never seen the brief reads this spec and answers: (1) what triggers a notification — §1, `intelligence.filed`, a smart note live on the feed; (2) who is notified — §2, project members + connections via Smart Lists, scope-matched, author excluded, broadcast Shawn-only; (3) what the mail says — §3, the celebration shape, verbatim copy; (4) how preferences work — §4, Settings section, scope + channels + per-type toggles, in-system on / email off / sounds off; (5) how auto-organize maps a note to an area — §5, `organize()` Look/Tag/File/Link, category folder + tags → area table, unfiled shelf for no match. If any answer needs the brief, the spec failed and gets fixed — it does not get filed as done.

**Filing record (filled at filing time):**
- Spec: `TEAM-NITRO/NOTIFICATION-SYSTEM-SPEC-20261110.md`, branch `notification/spec-20261110` — blob + commit + link in the report back. No merge. No deploy.
- Accompanying smart note: filed per the numbering law (`next-sn-number.py` FRESH), `##` format, verified live on the feed ("in means on the feed").

---

*Sources (all verified with test -f before citing): ~/MEMORY.md (Naima Resolution + notification design, 01:00Z Nov 10) · ~/memory/2026-10-27.md (Settings toggles, notification system live-and-in-sync) · ~/memory/2026-11-10.md (daily log) · ~/workspace/team-nitro/INTELLIGENCE-LOOP-SEAT.md · ~/workspace/team-nitro/ONE-SYSTEM-MERGE-SPEC-20261109.md · ~/workspace/team-nitro/THE-SMART-BOX-BLUEPRINT-20261109.md · ~/workspace/team-nitro/NAYANET-OPERATION-MANUAL.md · ~/workspace/project-intelligence/ACTIVATION.md · ~/workspace/project-intelligence/notification-settings-and-dashboard-data-20261027.md · ~/workspace/project-intelligence/pi-activity-notifications-SPEC.md.*
