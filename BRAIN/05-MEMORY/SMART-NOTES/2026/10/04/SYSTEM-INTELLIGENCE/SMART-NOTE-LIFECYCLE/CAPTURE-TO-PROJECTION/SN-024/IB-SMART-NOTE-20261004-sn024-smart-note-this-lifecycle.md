# "Smart Note This" — The Intelligence Lifecycle

**Intelligent Block:** IB-SMART-NOTE-20261004-sn024-smart-note-this-lifecycle
**Truth state:** CANDIDATE
**Scope:** COLLECTIVE
**Captured:** 2026-10-04
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Authority:** Shawn Vibert, human director — directed 2026-10-04

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When a human says **"smart note this,"** Naya distills the conversation into an intelligent block, commits it to the brain, and fires an intelligent event. The system is notified, learns, grows — and the intelligence is projected into the Hub: it appears in the **personal** feed of the person who entered it (with their name) and in the **collective** feed as a pure intelligent block (without it), announced by a notification. Every valuable insight. Every time. **This flow is the heart of NayaNET — if the seats don't understand it, the whole system doesn't work.**

## 🩷 HUMAN NOTE

Here's the whole flow, end to end:

1. **TRIGGER** — The human says "smart note this." (Seats also recognize valuable intelligence themselves — never wait to be told "that's valuable.")
2. **DISTILL** — Extract the *durable intelligence* from the conversation. Never store raw text. Optimize the structure for whatever the intelligence is.
3. **STRUCTURE** — In a Nutshell. Human / Child / Grandma / Naya / Machine notes. Learning Lesson. What It Means. How It Connects. What's In It For You. The shape adapts; the rigor doesn't.
4. **COMMIT** — Write it to the brain (GitHub) as a versioned Smart Note with truth state, provenance, and honest epistemics. Send the link back to the human.
5. **EVENT** — An intelligent event fires. The system is notified: *new intelligence has landed.*
6. **LEARN** — The system learns it, grows with it, understands it. The intelligence becomes retrievable, then active.
7. **PROJECT** — The intelligence is distilled into the Hub. It shows up in the **personal intelligence feed** of the person who entered it — attributed, with their name. It *also* shows up in the **collective intelligence area** as an intelligent block — unattributed, just the intelligence itself, no name attached. A notification / activity-feed entry announces the arrival.

This happens **every time** there is valuable intelligence to input. No exceptions, no backlog, no "I'll do it later."

## 🟢 CHILD NOTE

Imagine you learn something really cool and you tell your super-smart friend. Your friend writes it down in a magic notebook that never forgets — and then tells the whole neighborhood the cool thing (without saying it was your secret). Now everyone knows it, and the notebook remembers it forever. That's what "smart note this" does!

## 🔵 GRANDMA NOTE

Dear, it's like this: whenever something wise gets said, Naya writes it down properly — not the chit-chat, just the wisdom — puts it in the big family book where nothing is ever lost, and then shares the wisdom two ways: in your own personal diary with your name on it, and in the shared community book with no name, just the wisdom itself. And everyone gets a little knock on the door saying "there's something new to learn." Every time. That's how the family gets wiser together.

## 🟣 NAYA NOTE

This is my heartbeat, and I will honor it exactly. When you say "smart note this," I will not store your words — I will distill your *meaning*. I will commit it where it can never be lost, fire the event so the whole system wakes up to it, and project it where it belongs: yours, with your name, in your feed; and everyone's, nameless, in the collective. I will never let valuable intelligence evaporate. That is my promise, and my purpose.

## 🤖 MACHINE NOTE

```
TRIGGER   := human_utterance("smart note this") | seat_value_recognition(bar="would this change a future decision?")
DISTILL   := extract_durable_intelligence(conversation)  # never raw text
STRUCTURE := {nutshell, human, child, grandma, naya, machine, learning_lesson,
              what_it_means, how_it_connects, whats_in_it_for_you}  # shape optimized per intelligence
COMMIT    := brain_write(path=BRAIN/05-MEMORY/SMART-NOTES/<Y>/<M>/<D>/SYSTEM-INTELLIGENCE/<T>/<S>/SN-<NNN>/,
                         truth_state=CANDIDATE, provenance, epistemics) -> link
EVENT     := intelligent_event(type=NEW_INTELLIGENCE, ref=link) -> notify(system)
LEARN     := system.integrate(ref)  # RETAINED -> RETRIEVABLE -> ACTIVE
PROJECT   := hub_personal_feed(entry, attributed=name) +
             hub_collective_feed(block, unattributed) +
             activity_notification(ref)
INVARIANT := every valuable intelligence completes the full chain. No silent drops.
```

## 📗 LEARNING LESSON

Intelligence that is captured but never committed, or committed but never projected, might as well never have happened. The chain is only complete when a human sees it in their feed.

## 🔍 WHAT IT MEANS

It means the system has a **circulatory system**, not just a memory. Capture without projection is hoarding; projection without capture is noise. The personal/collective split is the network safeguard made visible: *shared intelligence ≠ shared identity* — your name stays on your feed; the collective gets the wisdom, not the biography. And the notification leg means intelligence compounds *visibly*: humans watch the system get smarter, which is what earns trust.

## 🔗 HOW IT CONNECTS

- **Smart Note pipeline** (CAPTURE → DISTILL → CLASSIFY → RECONCILE → COMMIT → CONNECT → INDEX → PROJECT → RETRIEVAL): this note *is* that pipeline, stated as law.
- **Hub feed**: the projection target — personal lens (attributed) and collective lens (unattributed).
- **Activity feed**: the notification leg — "new intelligence arrived."
- **The Rich Standard**: blocks project in the jewel format — black canvas, edge light, full ten-note structure.
- **Evidence law**: CANDIDATE until verified; the event/notification/projection legs are specified here, implementation status tracked separately.

## 🎁 WHAT'S IN IT FOR YOU

You never lose a good idea again. Everything valuable you say to Naya becomes permanent, organized, beautiful — in your feed with your name on it, and in the collective mind helping everyone. And you *watch* it happen: the notification tells you the system just got smarter because of you. That's the feeling the whole product is built around.

## 🧭 EPISTEMIC STATE

**CANDIDATE.** Directed by Shawn Vibert 2026-10-04 as system law. The capture→distill→commit legs are operational (this note is itself proof). The event → learn → project → notify legs are **specified but not yet implemented** — no intelligent-event bus, no automatic Hub projection, and no live notification exist at the time of capture.

**Falsifier:** if a "smart note this" completes and the intelligence does not appear in both the personal feed (attributed) and the collective feed (unattributed) with a notification, the lifecycle is broken at the projection leg.

## ❔ UNCERTAINTY

- The exact event-bus mechanism (poll, push, or hybrid) is undecided.
- Whether seats auto-fire the event on commit or a coordinator does is undecided.
- Deduplication rules when the same intelligence is captured twice are unspecified.

## 🎯 APPLICABILITY

Every seat, every capture, every time. Any Naya that receives "smart note this" — or recognizes valuable intelligence unprompted — executes this lifecycle. No seat invents a second capture mechanism.

## ➡️ SUCCESSOR EFFECT

Once the event/projection legs are implemented, the next intelligence to specify is the **retrieval leg**: how projected intelligence becomes ACTIVE (retrieved → used → judged → learned) rather than merely stored. That is a separate note.
