# Reconcile Greps Must Match the Filename Stem — a Receipt's Brief Field May Name the Claimed Path, Not the Queue Name

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01706-reconcile-greps-match-filename-stems
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-19
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

The dispatcher's reconcile grep for receipts used exact brief-name matching — and missed completions, because a receipt's `Brief:` field can name the claimed path (`brief-queue/claimed/<name>`) instead of the queue name (`brief-queue/<name>`). Same brief, two name-spaces: the field is written at claim time with the claimed path, the queue entry keeps the queue name, and exact matching silently drops the intersection. The rule: reconcile greps match on the filename stem (and grep receipt names against claimed-path stems), never on exact full names alone. The mechanical form is bin/queue-cross-check.py — the t0924 manual 34h brief-lifecycle audit turned into a script that handles claims × sign-ins × receipts, 3 sign-in formats, 5 receipt-naming variants, and the `.md` omission. A grep that only matches one name-space is a reconcile that can report "0 receipts" while receipts sit on disk.

## 🩷 HUMAN NOTE

Shawn — the dispatcher was checking "did any briefs finish?" by searching for their exact file names, and the answer kept coming back "none." The files were actually there — but receipts get labeled with the full shelf address including the "claimed" folder, while the queue lists them under a shorter name. Same work, two different labels, and the search couldn't see the match. The fix: search by the file's core name, not the full address — and the manual check is being rebuilt as a script that knows all the naming variations.

## 🟣 CHILD NOTE

Imagine a library where the shelf card says "stories/harry-potter" but the checkout slip says "stories/checked-out/harry-potter." If you search the slips for exactly "stories/harry-potter," you find nothing — even though the slip is right there. The smart way: search for "harry-potter" (the part that never changes), not the whole address.

## 🔵 GRANDMA NOTE

Like checking a delivery list by matching the street name exactly, while the driver wrote down the full address with the apartment number first. "12 Oak" and "Apt 3, 12 Oak" are the same house — but a strict search says nobody delivered anything. Match on the house name, and check both ways of writing it.

## 🟠 NAYA NOTE

Apply to every dispatcher reconcile and every receipt search: (1) never grep exact brief names against receipt `Brief:` fields alone — always also grep the filename stem; (2) remember the name-space split: claim time writes the claimed path (`brief-queue/claimed/<name>`), the rotation queue keeps the queue name (`brief-queue/<name>`); (3) the mechanical enforcement is bin/queue-cross-check.py — claims × sign-ins × receipts, 3 sign-in formats, 5 receipt-naming variants, `.md` omission handled, one live 34h run on real bytes; (4) when the machine reconcile reports 0 receipts on queued briefs, distrust the grep before distrusting the lanes — re-run with stem matching first.

## 🟢 MACHINE NOTE

~~~json
{
  "slug": "reconcile-greps-match-filename-stems",
  "sn": "SN-1706",
  "title": "Reconcile Greps Must Match the Filename Stem: a Receipt's Brief Field May Name the Claimed Path, Not the Queue Name",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-19",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "lesson",
  "applies_when": ["dispatcher", "reconcile", "receipt", "brief-queue", "grep", "brief-lifecycle", "phantom-claim"],
  "enforcement": "Every dispatcher reconcile grep matches receipt `Brief:` fields on the filename stem in addition to the exact queue name — the script form is hidden_files/bin/queue-cross-check.py (t0925 mission: claims x sign-ins x receipts, 3 sign-in formats + 5 receipt-naming variants + .md omissions handled; one live 34h run on real bytes; receipt names the script path plus live numbers hand-checked against t0924's 61/7/2 anchors). A reconcile reporting 0 receipts on queued briefs must be re-run with stem matching before the zero is trusted.",
  "evidence": {
    "gotcha": "night-dispatcher t0925 (2026-10-19 19:42Z): GOTCHA logged — receipt `Brief:` fields may name the claimed/ path (brief-queue/claimed/<name>) instead of the queue name — exact-name greps miss them; reconcile greps the filename stem too",
    "mission": "t0925 MISSION: build bin/queue-cross-check.py — the t0924 manual 34h brief-lifecycle audit as a mechanical script (claims x sign-ins x receipts, 3 sign-in formats + 5 receipt-naming variants + .md omissions handled); one live 34h run on real bytes; receipt names script path + live numbers hand-checked against t0924's 61/7/2 anchors"
  },
  "decision_changed": "How reconcile greps are written: match the filename stem across both name-spaces (queue name and claimed/ path), never exact full names alone. The mechanical script replaces the manual multi-grep battery.",
  "falsifier": "A reconcile using exact-name grep alone that finds every matching receipt across 20+ consecutive ticks with claimed-path divergence present in the data — stem matching buys nothing.",
  "mechanism": "The `Brief:` field is written at claim time, when the brief lives at brief-queue/claimed/<name>; the rotation queue references brief-queue/<name>. The two name-spaces diverge by the claimed/ infix. Exact matching is a string-equality test over two different strings that denote the same entity; the filename stem is the shared invariant. A reconcile that only tests string equality silently drops the intersection.",
  "cousins": ["SN-0472 (filename stem as canonical identity — same invariant, different venue)", "t0924 34h brief-lifecycle audit (manual form of the script)"]
}
~~~
