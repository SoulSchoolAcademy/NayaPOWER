# SN-0725 — RECEIPT-SLA: every intelligence Shawn shares gets a same-turn capture receipt — a nightly tripwire catches the misses, the main seat dispositions by morning

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0725-receipt-sla-tripwire-morning-dispositions
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Captured by:** Naya 4 (smart-note distillation loop)
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6070449537 ([SLA-AUDIT] 2026-10-08 — 9 unreceipted item(s) need disposition; Nightly Smart-Link SLA audit, Lane 4 — Human Value)

## IN A NUTSHELL

The capture law (document everything of value, same turn, no waiting) is a promise; the Smart-Link SLA audit is its enforcement. The SLA: **every intelligence Shawn shares — a directive, a decision, a ratification, a correction, a preference — gets a capture receipt back in the same turn.** A receipt is a Smart Note ID, a smart link, a PR number, a #1354 comment id, or an explicit queue statement naming the owner and the landing artifact.

Nightly, the audit runs `smart_link_sla_audit.py` over the daily memory log. It flags sections where Shawn shares intelligence but no receipt signal appears in the section body, and exits 1 (REVIEW). Its first full run on 2026-10-08 flagged 9 sections: the operating-protocol consolidation directive, the Ask Naya voice delivery reset to a full 10/10 build, the expanded standing scorecarded decision authority, the learning-to-automatic doctrine, the design-production stop ("no interface candidate is accepted"), the rejected Connections header/copy — all real Shawn intelligence, none with an attached receipt.

The main seat dispositions every flag **by morning**, in exactly three buckets:
1. **Receipt found elsewhere** — cite it (benign: it landed in an adjacent section or on the board).
2. **Queued** — name the owner and the landing artifact.
3. **Genuine miss** — capture late, return the link to Shawn, and log the miss **and its cause**.

Two rules the audit taught by design: a tripwire flags on suspicion; only the human (main seat) supplies the verdict — the scanner is never loosened to silence a flag; and a genuine miss is owned publicly with its cause, because the cause is the only thing that prevents the next miss. The audit opened no PR and made no repair — it reported, and handed the disposition to the owning seat.

## HUMAN NOTE

Think of a night-shift quality check on a factory line. During the day, every item that comes off the line is supposed to get a tag: what it is, where it went. The night shift walks the line and finds 9 untagged items. They don't throw them away and they don't pretend they're fine — they sort each one into one of three bins: "the tag exists, just filed elsewhere," "the tag is promised — here's who will file it and where," or "genuinely missed — tag it now, hand the tag to the boss, and write down *why* it was missed." That third bin is the one that matters: owning the miss with its cause is what keeps the whole system honest.

## CHILD NOTE

Imagine you promised your teacher that every time the principal visits the class, you will write it in the class diary the same day. At the end of the week, your friend checks the diary against the visitor book and finds 9 visits you never wrote down. For each one you have three choices: show where you wrote it (maybe in the other notebook), say who will write it and when, or — if you really forgot — write it now, give the note to the principal, and say why you forgot. No erasing, no excuses.

## GRANDMA NOTE

There's a rule here: whenever Shawn tells the team something important — a decision, a direction, a correction — the team writes it down and gives him back a little proof ("here's your note, here's the link") before the day is done. A small nightly check reads the day's diary and lists every important thing he said that didn't get its proof. By morning, someone goes through the list: either finds the proof, says who will produce it, or admits it was missed, writes it now, hands it to Shawn, and writes down why it slipped. That's how nothing he says ever falls through the cracks.

## NAYA NOTE

Cold successor: this audit runs nightly. Each morning: (1) read the SLA-audit comment on #1354; (2) disposition every flagged section into the three buckets — receipt-found (cite the receipt), queued (owner + landing artifact), genuine-miss (capture the note late, post the smart link back to #1354 for Shawn, log the miss and its cause in the daily log); (3) never disposition by weakening the scanner — a benign flag is resolved by citation, never by silence. The audit is a tripwire; it fires on suspicion, you supply the verdict.

## MACHINE NOTE

```json
{
  "rule": "every intelligence Shawn shares (directive/decision/ratification/correction/preference) gets a capture receipt in the same turn: Smart Note ID, smart link, PR number, #1354 comment id, or an explicit queue statement (owner + landing artifact)",
  "instrument": "smart_link_sla_audit.py over ~/memory/YYYY-MM-DD.md; exit 1 (REVIEW) when a section lacks a receipt signal; scan is section-scoped, so receipts in adjacent sections or on the board may explain benign flags",
  "dispositions": [
    "receipt_found_elsewhere — cite it",
    "queued — owner + landing artifact",
    "genuine_miss — capture late, return the link to Shawn, log the miss and its cause"
  ],
  "disposition_owner": "main seat, by morning",
  "first_full_run": {
    "date": "2026-10-08",
    "board_comment": "6070449537",
    "flags": 9,
    "examples": [
      "operating-protocol consolidation directive",
      "Ask Naya voice delivery reset to a complete 10/10 build",
      "standing scorecarded decision authority expansion",
      "learning-to-automatic doctrine",
      "design production stopped; no interface candidate accepted",
      "Connections header/icon/copy rejected; 'done' language suppressed"
    ]
  },
  "applies_to": ["any capture-receipt SLA", "nightly memory-log tripwires", "Shawn-facing intelligence accountability"]
}
```

## LEARNING LESSON

**A capture promise without a tripwire is a wish.** The capture law existed for a week; the misses still happened — because no mechanism checked. The durable pattern: state the SLA in plain words (what counts as a receipt, the same-turn bound), run a mechanical audit over the canonical log, and give disposition a named owner and a deadline. Benign flags are expected and cheap (citation); only the genuine-miss bucket is expensive, and it must stay expensive — that is what makes the next morning's list shorter.

## HOW IT CONNECTS

- **Capture law (Shawn, 2026-10-01 → 2026-10-04 20:44 PDT):** this is its enforcement arm — the law said "capture always"; the SLA audit checks that it happened.
- **SN-0254 (smart link canonical definition):** defines what a receipt looks like — the link where Shawn can see it, verify it, and confirm it happened.
- **SN-0723 (SUPERSEDED_TIP_RACE):** receipt-theme sibling — different domain (promotion runs), same doctrine: every meaningful path leaves durable evidence; silence is the defect.
- **Sign-in/out law (SN-0351):** the disposition buckets are sign-out state discipline applied to intelligence receipts — bare "done" is a defect; cite, name, or own.

## EPISTEMIC STATE

**CANDIDATE** — earned from one live nightly audit run (2026-10-08, 9 flags, board comment 6070449537) and the disposition protocol it carried. Never merge #1229; only Shawn ratifies.
