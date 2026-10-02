# The Hub Intelligence Pipeline — Product Spec V1

**Status:** DRAFT — proposed by Naya 4, 2026-10-01. Not canonical until the human director ratifies.
**Purpose:** End the confusion. This is the one page that says where intelligence comes from,
how it reaches the Hub, and what the Hub is. If a design contradicts this page, the design is wrong.

---

## 1. The one sentence

**The Hub is the screen, not the camera.** It is the OUTPUT of intelligence, never the INPUT.

Intelligence is captured upstream, by talking to any AI. The Hub displays what was captured.
Nothing in the Hub creates intelligence. Nothing in the Hub writes intelligence upstream.

## 2. The three things that flow in

Exactly three streams enter the system. Everything visible in the Hub comes from one of them:

1. **SMART NOTES** — intelligent events. A person says to any AI: "make me a smart note."
2. **ACTIVITY** — what is happening right now. Current project, current work, the now-stream.
3. **REPORTS** — daily intelligent syntheses. The day's intelligence, distilled.

All three are mirrored in the Hub. All three arrive the same way: as an Intelligent Block,
through the trigger, into the feed. There is no fourth input path.

## 3. The pipeline (the only path)

```
YOU  --(ask any AI)-->  AI writes an INTELLIGENT BLOCK  -->  TRIGGER fires
                                                            |
                                              +-------------+-------------+
                                              |                           |
                                        PERSONAL FEED               COLLECTIVE FEED
                                     (identified to you)          (anonymized: the
                                      "your notes"                 intelligence is shared,
                                                                   identity never is)
                                              |                           |
                                              +-------------+-------------+
                                                            |
                                                     THE HUB displays it
```

Step by step, with no exceptions:

1. **Capture.** You ask any AI for a smart note, an activity update, or a report.
   (A smart note is also a diary entry, an intelligent entry — same thing.)
2. **Block.** The AI writes an Intelligent Block to
   `BRAIN/04-INTELLIGENCE/SMART-NOTES/<YYYY>/<MM>/<DD>/<slug>.md`, carrying all ten layers:
   in-a-nutshell, human note, child note, grandma note, Naya note, machine note,
   learning lesson, what it ultimately means, how to use it, what's in it for you.
3. **Trigger.** The new block is validated and an intelligent event is emitted.
4. **Fan-out.** The event lands on your personal feed (it knows it is yours) and on the
   collective feed (nobody knows who posted it — intelligence shared, identity private).
5. **Display.** The Hub renders the event. The Hub never invents, edits, or sources content.

## 4. The sharing rule

Connecting your Hub means exactly one thing: **your intelligence joins the collective;
your identity never does.** Personal feed = your blocks, identified to you. Collective feed =
everyone's blocks, anonymized. This is consent to share intelligence, not identity.

## 5. Why there is no capture button in the Hub

A capture button inside the Hub treats the output like an input. It would create a second,
weaker capture path that bypasses the block, the trigger, and provenance. One input path —
the AI conversation — keeps every block's origin clean. The Hub may link to capture, but it
must route through the pipeline: conversation → block → trigger → feed. Never write display
state directly.

## 6. Smart feeds (not one feed)

The feed is not one pile of blocks. It is a set of **smart feeds** — switchable views over
the same intelligence, like a social output of your mind:

- **Smart Notes** — the intelligent events.
- **Activity** — the now-stream.
- **Reports** — the distilled days.
- **All** — everything, newest first.

The user switches tabs or scrolls everything. Each person organizes their own intake:
highlights of their intelligence, their reports, multiple perspectives (the layers),
their categories. The audience axis is separate: **Personal** (mine, identified) vs
**Collective** (everyone's, anonymized). Audience × kind = the full feed.

## 7. What the demo blocks are

The blocks currently embedded in Hub builds are **samples of the format, not the content.**
They show what a block looks like. They are not there to stay. The moment the trigger runs,
real blocks replace them. A feed full of samples with no pipeline is a shell.

## 8. Acceptance test

The whole spec reduces to one test, stated by the human director:

> Ask any AI for a smart note right now. It writes the block. The block shows up in the
> feed on its own — personal feed identified, collective feed anonymized. No rebuild by hand,
> no second data entry, no missing provenance.

If that works, the pipeline works. If it does not, the pipeline is where to look — never the Hub.

---

**Open questions for the lanes (not decisions):** confirm the canonical SMART-NOTES home
(proposed: `BRAIN/04-INTELLIGENCE/SMART-NOTES`, beside the ratified IB protocol — note: an
earlier message said 05-MEMORY; the actual demo IBs live at 04-INTELLIGENCE); wire
`feed-events.json` into the #1278 feed room; merge the trigger workflow (director's gate).
