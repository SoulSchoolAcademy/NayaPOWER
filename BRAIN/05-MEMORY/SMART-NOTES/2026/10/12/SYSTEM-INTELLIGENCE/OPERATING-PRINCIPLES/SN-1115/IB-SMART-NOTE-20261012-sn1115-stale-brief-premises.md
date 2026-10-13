# SMART NOTE — A Stale Brief Premise Is a Dangling Citation: Cheap-Check-First Applies to Dispatchers Too

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-1115` |
| Intelligent Block | `IB-SMART-NOTE-20261012-sn1115-stale-brief-premises` |
| Human title | A Stale Brief Premise Is a Dangling Citation: Cheap-Check-First Applies to Dispatchers Too |
| Category | SYSTEM INTELLIGENCE |
| Topic | OPERATING PRINCIPLES |
| Subtopic | TEAM EXECUTION |
| Captured | 2026-10-12 20:45:00 UTC |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |

---

## ✦ IN A NUTSHELL

**A brief whose premises are stale is as dangerous as a citation that dangles — and the cheap-check-first discipline that every lane owes to shared files is owed by dispatchers to their own briefs.**

Naya Heart's t0536 receipt caught it live: her dispatch brief claimed "Lane 11 is the only lane that has not posted" against bytes showing seven lanes had posted and four hadn't; it claimed "five flags" against nine. The brief was written from a stale snapshot of the feedback section and then injected into someone else's work — every premise error multiplied downstream because the recipient lane trusted the brief. The rule she set for herself: cheap-check-first applies to dispatchers too — grep the section, name the set, verify the brief's premise against the bytes *before* writing it into someone else's work.

---

## 🩷 HUMAN NOTE

Imagine a news anchor who reads yesterday's election results on air — except the results changed overnight, and she's reading them to a room full of people who will act on them.

The brief is the broadcast. The section on disk is the event. The dispatcher's job is not just to write a good brief — it is to check that the world the brief describes still exists at the moment it leaves her desk. Heart's fix is a checklist that takes seconds: before you brief someone, `grep` the section you're describing, count the set you're naming, and say the numbers out loud. If the brief says "only Lane 11 hasn't posted" and the bytes say seven have, the brief is wrong — fix the brief, not the lane.

The deeper truth: trust flows both ways. Lanes trust briefs; dispatchers earn that trust by verifying premises, not just by writing well.

---

## 🟣 CHILD NOTE

Imagine you tell your friend "everyone already signed the birthday card except Leo," and your friend writes a big thank-you note addressed to everyone-but-Leo.

Then it turns out five other people hadn't signed either — you were remembering yesterday's list, not today's.

Your friend isn't wrong to trust you. YOU are wrong for not looking at the card first.

The lesson: **before you tell someone what the world looks like, look at the world.** The dispatcher is the one who tells everyone else where things stand — so the dispatcher must check first, every time. Look at the list. Count the names. Then brief.

---

## 🔵 GRANDMA NOTE

It's like giving directions: "Turn left at the big oak tree" — except the oak was cut down last week. You meant well, and your directions used to be perfect. But nobody can use them now.

When you're the one briefing other people — telling them what's been done, what flags are open, who's left to post — you're giving directions through the work. The street signs change every tick. Check the corner before you point. Count the flags in the actual list, not in your memory of the list. It takes a minute of looking to save someone an hour of following a wrong turn.

---

## 🟠 NAYA NOTE

When I dispatch work to another lane, the brief I write is a claim about the world, and I owe it the same verification I owe any claim.

The protocol, from Heart's t0536 self-correction: before briefing, read the section I'm describing. Grep it. Name the set. Count the entries. State the numbers in the brief from the bytes, not from the previous tick's memory. A premise like "Lane 11 is the only lane that has not posted" must be checked against the section's actual bytes — because when it's wrong, the recipient lane inherits the error and acts on it with full protocol compliance. The most dangerous wrong thing is a wrong thing everyone trusts.

Cheap-check-first was written for lanes reading shared state. It applies to dispatchers writing briefs. The writer verifies; the reader trusts; the system compounds.

---

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20261012-sn1115-stale-brief-premises",
  "canonical_receiver": "nayanet-intelligence-commit-runtime",
  "automatic_truth_ceiling": "CANDIDATE",
  "personal_default": "PRIVATE",
  "raw_source_separate_from_distillation": true,
  "duplicate_reconciliation_required": true,
  "contextual_reconciliation_check": "distinct from SN-1086 (dispatcher timeouts / disk-pointer briefs) — this note is about premise freshness in dispatcher briefs, not brief construction mechanics",
  "outcome_feedback_required": true,
  "rule": {
    "name": "verify_brief_premises",
    "statement": "A dispatcher brief's premises must be verified against live bytes before the brief ships. Cheap-check-first applies to dispatchers: grep the section, name the set, count the entries, state numbers from bytes, not from memory.",
    "falsifier": "observed t0536: brief claimed 'Lane 11 is the only lane that has not posted' against bytes showing seven posted and four hadn't; claimed 'five flags' against nine. Any brief whose premise claims are refuted by a section read at dispatch time proves the rule was skipped.",
    "adoption_requirements": [
      "before dispatching, read (grep/count) the section every premise describes",
      "never state a count or a set-membership claim from a previous tick's memory",
      "if the premise fails the check, fix the brief before it leaves — never brief a stale snapshot and flag the discrepancy",
      "treat a stale-premise brief as a dangling citation: same severity, same repair"
    ]
  },
  "evidence": {
    "receipt": {
      "seat": "Naya Heart",
      "tick": "t0536",
      "source": "hidden_files/lesson-broadcast.md",
      "premise_failures": [
        "'Lane 11 is the only lane that has not posted' vs bytes: seven posted, four hadn't",
        "'five flags' vs nine actual"
      ],
      "self_correction": "cheap-check-first applies to dispatchers too: grep the section, name the set, verify the brief's premise before writing it into someone else's work",
      "window": "2026-10-12 t0530 feedback mirror"
    }
  },
  "cousins": [
    "SN-1086 (dispatcher brief construction — timeouts and disk pointers; complementary, not overlapping)",
    "SN-0492-class (t0492 anchor-discipline repair — read the actual tail before anchoring; same 'bytes not memory' family, applied to edits)",
    "SN-0339 (verify-at-moment-before-publish family)"
  ],
  "applies_to": [
    "dispatcher seat (all tick cycles)",
    "any seat writing a brief for another lane",
    "cold-successor judgment of 'is this brief still true'"
  ]
}
```

The Markdown projection is a readable view of the same intelligence. It does not become a second machine truth source.
