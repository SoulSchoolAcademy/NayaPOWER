# SN-1713 — Identity Comparisons Canonicalize Both Sides: The Lane-Scorer's Path-Prefix False Positive

- **Intelligent Block:** IB-SMART-NOTE-20261019-sn1713-identity-comparison-canonicalize-both-sides
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-19
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **Provenance:** lane-scorer tick 2026-10-20 03:35 UTC (2026-10-19 20:30 PDT), recorded in `~/memory/2026-10-19.md` ("lane-scorer tick 2026-10-20 03:35 UTC (20:30 PDT run)"); corroborating bytes: `twelve-lane-scores.jsonl` ticks 0250/0305/0315/0317 UTC

## ✦ IN A NUTSHELL

The lane-scorer's unscored-scan matched receipt filenames against the ledger's stored `receipt` field with verbatim string equality and flagged 5 receipts as unscored. All 5 were already scored — the stored field carries a `twelve-lane-receipts/` prefix (added by the writer's context) that the scan's bare-filename key lacks. An independent basename comparison (`os.path.basename(d['receipt'])`) showed zero genuinely unscored entries. The false positive came from comparing a **representation** (path-with-prefix) to an **identity** (the receipt name) with `==`: writer and reader live in different path contexts, so raw-string equality confuses where a record sits with what it is. The durable rule: any scan that reconciles stored records against filesystem names must canonicalize **both sides** to the shared identity key before comparing — here, `os.path.basename` on both sides; where basenames can collide, a stronger key (content sha256) is required instead. The scorer caught it by re-checking with the canonicalized key; the lesson is what the scorer wrote down: "fixed in my head, not yet in a script" — a lesson that lives only in a run's memory is a lesson waiting to be re-learned the hard way.

## 🩷 HUMAN NOTE

Shawn — the scoreboard's own error-detector misfired this tick, and the way it caught itself is the lesson. The lane-scorer scans for unscored receipts by comparing filenames to the ledger's stored path field, character for character. Five receipts came back "unscored" — except all five were already scored. The stored field says `twelve-lane-receipts/name`, the scan looked for `name`; the strings don't match, but it's the same receipt — the directory prefix was bolted on at write time by whoever wrote the ledger entry, and the scanner didn't know about it. A second pass comparing just the bare filename found everything scored, zero work to do. The takeaway is old and boring and still bites: don't compare labels, compare identities — strip both sides down to the same canonical form first. And the scorer's own honest footnote: it fixed this in its head, not in a script, because no persistent scorer script exists yet. A lesson that lives only in one run's head is a lesson that gets re-learned by the next run's false alarm.

## 🟣 CHILD NOTE

Imagine the school office keeps a list of homework folders as "Room 12 — math worksheet" but the teacher checks in folders labeled just "math worksheet." The office's helper looks down the list, doesn't see "math worksheet" anywhere, and reports five missing assignments. Nothing is missing — the helper just compared the full office label to the short folder label, and they don't look the same even though they're the same folder. The fix: both sides strip the extra words first, then compare. And the helper wrote the trick on a sticky note instead of taping it to the checklist — so next week's helper will make the same mistake.

## 🔵 GRANDMA NOTE

It's like matching library cards to books on the shelf. The catalog card says "Fiction aisle, shelf 3 — The Novel," but the book's spine just says "The Novel." If you insist the card text must match the spine text exactly, you'll swear five books are missing. They're all there — you just compared the catalog's full address to the book's short title. Cut both down to the title alone, and everything matches. And write the trick on the actual checklist, not on a scrap of paper you'll lose — otherwise the next person counts the same phantom missing books.

## 🟠 NAYA NOTE

I carry this one for every reconciliation scan I write or review: a stored record field is not its identity. The ledger's `receipt` field picked up a directory prefix in the writer's context; my scan key had no prefix in the reader's context; verbatim equality of the two strings manufactured 5 false "unscored" positives out of nothing. The repair is mechanical and cheap: canonicalize both sides to the shared identity key — `os.path.basename` on the stored field AND on the scan key — then compare. And the second half of the lesson is about me, not the string: the scorer's receipt says "fixed in my head, not yet in a script." I treat a lesson that lives only in a run's head as unfiled. When a detection script finally gets written, it ships with the canary: a path-prefixed ledger entry must resolve as scored on its first real run, or the script doesn't run.

## 🟢 MACHINE NOTE

~~~json
{
  "sn": "SN-1713",
  "title": "Identity comparisons canonicalize both sides — the lane-scorer's path-prefix false positive",
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "verbatim_path_match_across_write_read_contexts",
  "evidence": {
    "receipt": "~/memory/2026-10-19.md — 'lane-scorer tick 2026-10-20 03:35 UTC (20:30 PDT run)': first unscored-scan matched receipt FILENAMES against the `receipt` field verbatim (`twelve-lane-receipts/<name>` prefix), flagged 5 as unscored; basename comparison showed all 5 already scored by ticks 0250/0305/0315/0317 UTC",
    "scorer_own_words": "Lesson: match `os.path.basename(d['receipt'])` — fixed in my head, not yet in a script (no persistent scorer script exists; add this to the detection if one is ever written)",
    "corroboration": "twelve-lane-scores.jsonl entries from ticks 0250/0305/0315/0317 UTC cover the 5 flagged receipts"
  },
  "mechanism": "representation/identity confusion across write/read contexts: the stored receipt field accumulates a directory prefix at write time that the reader's filesystem listing lacks; verbatim string equality compares representation (path-with-prefix) to identity (receipt name), producing false 'unscored' positives. Canonicalizing both sides to the shared identity key (basename) removes the divergence.",
  "falsifiers": [
    "All writers guarantee the stored field as bare basename AND the reader lists bare basenames — verbatim matching is then safe; the lesson's trigger condition is representation divergence.",
    "Two distinct receipts share one basename — basename comparison false-negatives, disproving 'basename is enough' and requiring a stronger identity key (content sha256)."
  ],
  "decision_it_changes": "How any future unscored-scan / record-vs-filesystem reconciliation script chooses its match key: verbatim stored-field equality -> canonicalize both sides to the identity key first.",
  "applies_when": [
    "scorer",
    "detection-scan",
    "receipt",
    "identity-match",
    "reconciliation",
    "record-vs-filesystem"
  ],
  "enforcement": "Any future unscored-scan/reconciliation script must ship with a canary: a ledger entry whose receipt field carries a path prefix must resolve as already-scored on the script's first real run. The lane-scorer's 2026-10-20 03:35 UTC false positive (5 entries with `twelve-lane-receipts/` prefixes) is the standing regression input. No canary pass -> the script does not run; bounce at scorecard review."
}
~~~
