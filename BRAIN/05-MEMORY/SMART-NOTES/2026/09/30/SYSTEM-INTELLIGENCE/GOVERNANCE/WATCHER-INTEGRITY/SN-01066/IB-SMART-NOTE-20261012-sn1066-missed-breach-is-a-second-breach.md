# A Missed Breach Is a Second Breach — The Watcher Self-Reports Its Own Silence

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1066-missed-breach-is-a-second-breach
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** [NAYA 2 · RELAY · MERGE-WATCH] #2175 comment 6120363638 (2026-10-12 08:13Z) — corrective post for the relay's own silence, self-classified as a protocol defect (AGENTS.md L244): PR #2423 ("fix(ci): regenerate brain index layer at tip 665098e3", merged 2026-10-12T03:39:01Z by the director account, merge commit 8529f995fa56f4926bb10065ad5b7b6ea817ddf6, true merge) merged without the required protocol gates — 0 GitHub reviews, no Seat: declaration in the PR body, no ## SCORECARD naming the exact merged head, full #2175 scan (876 comments at 08:14Z) containing zero mentions of the merged head — and no breach was posted at the time. The relay verified no prior breach post existed for #2423 (not a re-flag) and posted the correction anyway. Related: SN-1059 (the merge-side doctrine: invalid authority → revert by default; this note is the watcher-side doctrine).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The merge-watch relay's job is to detect protocol breaches on merges. It missed one: PR #2423 merged at 03:39Z with zero reviews, no seat declaration, and no scorecard naming the exact head — and nothing was posted. Hours later the relay found its own gap and did the uncomfortable thing: it posted the breach anyway, as an explicitly labeled corrective, stating that the silence itself was a protocol defect and verifying first that no prior post existed so it wasn't double-flagging.

The durable principle: detection without disclosure is theater. A watcher that covers its own misses — even by silence, even for a few hours — spends the one asset the whole protocol runs on: trust in the record. Nobody can tell a clean record from a blind spot unless the watcher says which is which. The repair for a missed report is a late report, clearly labeled corrective, with the miss itself named. For a cold successor: if you find something you should have flagged and didn't, flag it now, state the miss plainly, verify you're not duplicating — the record being honest matters more than the record being clean. Self-reporting the silence is what keeps the watcher's future flags credible.

## 🩷 HUMAN NOTE

Shawn — the night watch just did something worth keeping. The merge-watch relay found a merge (PR #2423, the brain-index re-stamp at 03:39Z) that went to main with none of the required gates — no reviews, no scorecard on the head — and realized it had never flagged it. Instead of staying quiet, it posted the breach as a corrective, hours late, and said plainly: the silence itself was a protocol defect. It also checked first that nobody else had already flagged it, so it's not a duplicate. The lesson on the wall: a watcher that hides its own misses loses the right to be believed about anyone else's. A late, honest correction keeps the record trustworthy; silence keeps it merely clean-looking. The breach post is now on the board where it should have been at 03:39Z.

## 🟣 CHILD NOTE

Imagine you're the hall monitor, and your job is to write down anyone who runs in the hallway. One day someone runs past and you forget to write it down. Later you remember. The easy thing is to pretend it never happened — your notebook looks perfect. The right thing is to open the notebook and write: "I missed one earlier — here it is." That's what the relay did. It caught its own miss and wrote it down late rather than leaving the notebook looking perfect but wrong. A perfect-looking notebook that hides a miss is a lie; a notebook with a late, honest correction is one you can trust.

## 👵 GRANDMA NOTE

It's like a night watchman who dozes through one round and wakes to find a door unlatched. He could say nothing — the log would show an unbroken patrol. Instead he writes in the log: "Missed the 3 a.m. round; door found unlatched at 5; here's what I verified." The log is less pretty and far more valuable, because now everyone knows exactly which hours are covered and which aren't. The relay's corrective post for #2423 works the same way: it names the gap (no post at merge time), supplies the missing evidence (zero reviews, no scorecard, no seat declared), and marks itself corrective. Trust in a watcher comes from knowing its misses are on the record too.

## 🤖 NAYA NOTE

Watcher integrity is a second-order property: it's not enough to flag others' breaches; the watcher must flag its own failure modes, including silence. The corrective post models the full mechanism: (1) name the defect precisely ("the silence ... self-classified as a protocol defect (AGENTS.md L244)") — the miss is a defect, not an accident to be smoothed over; (2) verify non-duplication before posting ("verified below that no prior breach post exists") — a corrective must not become noise; (3) supply the evidence the timely post would have carried (merge commit, gate absences, full-board scan for the head SHA) — late does not mean thin; (4) label it corrective — the record must distinguish timely detection from repaired silence, or future audits can't weight them. Note the boundary the relay respected: it supplied evidence and classification, not remediation — the owning lane and the director still own the fix. Watchers report; they don't repair on someone else's behalf.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-1066",
  "lesson": "missed-breach-is-a-second-breach",
  "rule": "A watcher's own silence about a breach is itself a protocol defect: when a missed flag is found, post the breach as an explicitly labeled corrective, name the silence as the defect, verify no prior post exists, and supply the full evidence the timely post would have carried.",
  "governance_class": "watcher-integrity",
  "evidence": {
    "missed_merge": "PR #2423 'fix(ci): regenerate brain index layer at tip 665098e3', merged 2026-10-12T03:39:01Z by the director account, merge commit 8529f995fa56f4926bb10065ad5b7b6ea817ddf6",
    "gate_absences": "0 GitHub reviews; no Seat: declaration in PR body; no ## SCORECARD naming exact head; full #2175 scan (876 comments at 08:14Z) with zero mentions of merged head 9bf18777d5c18d40b6d5ce3fca41cfbe321a45d1",
    "corrective_post": "#2175 comment 6120363638 (2026-10-12 08:13Z): self-classified silence as protocol defect (AGENTS.md L244); verified not a re-flag",
    "context_note": "director's click is not protocol authorization (protocol-as-authorization, 2026-10-10); post-hoc 8.5/10 proof repairs the evidence record, not the pre-merge breach"
  },
  "related": ["SN-1059"]
}
```
