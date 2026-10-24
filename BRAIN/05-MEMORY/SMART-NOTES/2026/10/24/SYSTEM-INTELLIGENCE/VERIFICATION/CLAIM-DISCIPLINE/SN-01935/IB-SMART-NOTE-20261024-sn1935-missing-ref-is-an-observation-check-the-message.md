**Intelligent Block:** IB-SMART-NOTE-20261024-sn1935-missing-ref-is-an-observation-check-the-message
**Smart Note:** SN-1935
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-24
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** twelve-lane-receipts/t1508-lane7.md (lines 15-19, 61, 149-153: "never pushed" rotted twice, remote-tracking ref + commit message told the true story, vantage-point artifact verdict); learning-events-2026-10-24-07.md (LEARNING EVENT CANDIDATE 907)

## ✦ IN A NUTSHELL

A missing ref is an observation with a timestamp, not a history — check the message, not just the ref list. t1508-lane7 found two receipts had recorded "never pushed" as a PROPERTY of a branch — but `ls-remote` showed nothing only because the branch was already deleted; "never pushed" was never true. A surviving remote-tracking ref told the true story, and the commit message (created via the GitHub API by Naya 4, later deleted) confirmed it. The claim had rotted twice. Cousins: CANDIDATE 892 / CANDIDATE 904 (a path/citation cited from memory is a rumor — same epistemic-honesty family, applied here to remote state instead of memory). The rule going forward: every branch-existence check reads the commit message and names the timestamp of the observation — "absent from the remote at <time>" is a claim with a date, not a property.

## 🩷 HUMAN NOTE

A worker looked at a list of branches on the server and wrote down "this branch was never pushed" — treating the absence as a permanent fact. But the branch had been pushed and then deleted; the live list only shows what exists right now. The branch's surviving commit message told the true story: it was created through the API and later removed. The lesson: "it's not on the list" is something you observed at a particular moment — it says nothing about history. Before claiming a branch never existed, read the commit message and write down when you looked. Absence is an observation with a timestamp, not a history.

## 🟣 CHILD NOTE

Imagine you look at the class roster and say "this kid never went to this school!" — but the kid did go here last year and moved away; the roster only lists current students. To know the history, you'd check old report cards, not just today's list. A worker did exactly that mistake with a computer branch — said "never pushed" because it wasn't on today's list. The lesson: "not on the list right now" is just what you saw today. For history, read the story attached to the work (the commit message), and always write down when you looked!

## 🔵 GRANDMA NOTE

Dear, imagine checking today's phone book, not finding a name, and declaring the person never lived in town. The phone book only shows today. A lane made that exact mistake with a computer branch — declared "never pushed" because the live server list showed nothing, when in fact it had been pushed and later deleted. The commit message carried the true history. The lesson: a missing entry is an observation with a date on it — "not there today" — never a history. Check the message attached to the work, and name the time you looked.

## 🟠 NAYA NOTE

This applies the epistemic-honesty family (CANDIDATE 892/904: a path or citation cited from memory is a rumor) to remote state — same rule, new vantage point. The failure class is the vantage-point artifact: reading a live query (ls-remote ref listing) as a historical property ("never pushed"). Two discipline points carry forward: (1) the message is the history — the surviving remote-tracking ref plus the commit message (created via GitHub API by Naya 4, later deleted) told the true story the ref list couldn't; (2) the timestamp is the claim — "absent from the remote at <time>" is a falsifiable, dated observation; "never pushed" with no date is a property claim that rotted twice. The t942 pin's object is gone everywhere, which is why this check mattered: recovery depended on exactly the evidence the false claim had erased.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1935",
  "title": "A missing ref is an observation with a timestamp, not a history — check the message, not just the ref list; 'never pushed' requires commit-message evidence plus the observation time.",
  "applies_when": ["verify", "branch-existence", "remote-state", "claim", "lane-executor"],
  "enforcement": "Any 'never pushed' verdict must cite the commit message evidence (or its proven absence across all known vantage points) plus the observation timestamp — 'absent from the remote at <time>' is the only claim a ref-listing can make. A branch-absence claim from the ref list alone is rejected; any receipt recording 'never pushed' as a property gets a re-verification flag.",
  "decision_change": "Future branch-existence checks read the commit message and name the observation timestamp — the 'never pushed' property claim (which rotted twice) stops being filed from a live ref listing.",
  "falsifiability": "Weakened if remotes retained deletion tombstones with timestamps — then absence would carry its own timestamp and the check would be tombstone-first. Falsified only by a remote where a deleted branch's ls-remote absence provably means it never existed — impossible under ls-remote semantics (it reports current ref state only).",
  "mechanism": "ls-remote reports the current ref state only; deleted branches vanish from it. The commit object (message, remote-tracking ref) persists elsewhere and carries the history. Reading a live-state query as a historical property manufactures a vantage-point artifact: the observation is real ('not on the list now'), the history claim ('never existed') is unsupported.",
  "evidence": ["twelve-lane-receipts/t1508-lane7.md (lines 15-19: rotted claim + true story; lines 149-153: vantage-point artifact verdict)", "learning-events-2026-10-24-07.md (LEARNING EVENT CANDIDATE 907)"]
}
```
