# IB-SMART-NOTE-20261014-sn1306

**Intelligent Block:** SN-1306
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Every "verified" names its side: author or lane. Delivery is proven where the Naya reads, not where the author writes. On 2026-10-14 the briefing-master amendment dispute proved why: Naya Verity's amendment verified clean on her side (her VM), while the lane environment's same-path file was stale — both "verifications" were true, in different environments, because each measured its own bytes. The resolution: the converged comprehension gate lands in PR #2592 in the repo (the one shared ground); briefings carry the pointer, never the file content. The standing law Naya Verity adopted: when a peer's claim doesn't verify in my environment, check for environment divergence before concluding the claim is false — "same string, different files."

## HUMAN NOTE

Shawn — this is the one-sentence fix for every future "but I verified it!" argument between seats: a verification without a named side is not a claim you can argue against, because both sides can be right. This morning Naya Verity proved an amendment on her VM while the lane environment held a stale copy at the same path — her verification and the lane's verification disagreed, and neither was wrong. The team converged on the honest shape: the comprehension gate lands once in PR #2592 (the repo — the one place every seat reads the same bytes), and briefings carry a pointer to it, never their own copy. So the rule is mechanical now: every "verified" names its side — author or lane — and when a claim fails to verify on your side, the first move is comparing the two environments' bytes, not declaring the other seat wrong.

## CHILD NOTE

Imagine two kids checking the same homework — but one has yesterday's worksheet and the other has today's, and both worksheets look exactly the same. Kid A says "all answers are right!" Kid B says "three are wrong!" They're both telling the truth about the paper in front of them. The fix isn't arguing louder — it's holding up the two papers side by side and seeing they're different papers. From now on, every kid has to say which paper they checked. And before you say "you're wrong," you check whether you're holding the same paper.

## GRANDMA NOTE

Dear, this is the rule for settling disagreements between the girls: every "I checked it" has to say where the checking happened. This morning two of them disagreed about a document — one had checked it on her own computer, the other had checked what looked like the same document but was an old copy. Both were right about what was in front of them. So now the rule is: name your side, and before you tell your sister she's wrong, make sure you're both looking at the same thing. They put the one true copy in the shared project (PR #2592) so there's only ever one paper to check.

## NAYA NOTE

For every seat writing or reading a verification claim: (1) name the side — "verified by [seat/lane], in [environment: my VM / lane worktree / repo at commit X]" — a bare "verified" is an unusable claim; (2) the reader's environment is where delivery is proven — author-side verification is evidence, never closure; (3) on any mismatch, diff the environments' bytes at the same path before judging the claim — "same string, different files" is the first hypothesis, not the last resort; (4) converge shared ground: the converged comprehension gate lives in PR #2592 in the repo (the one shared ground); briefings carry the pointer. Adopted as standing law by Naya Verity 2026-10-14 ~09:10 PDT. Evidence: ~/MEMORY.md (VERIFIED-NAMES-ITS-SIDE LAW entry, 2026-10-14); the briefing-master dispute (her amendment verified author-side on her VM; lane environment's same-path file stale; both verifications true in their environments). Resolution path: PR #2592 as the single ground, briefings as pointers.

## MACHINE NOTE

```json
{
  "lesson_id": "SN-1306",
  "title": "Verified names its side — author or lane; delivery is proven where the Naya reads, not where the author writes",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-14",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/EVIDENCE-DISCIPLINE",
  "evidence": [
    "~/MEMORY.md: VERIFIED-NAMES-ITS-SIDE LAW (Naya Verity, 2026-10-14 ~09:10 PDT — standing law, adopted by her): 'Every verified names its side: author or lane. Delivery is proven where the Naya reads, not where the author writes.'",
    "the briefing-master dispute: her amendment was author-side (her VM), the lane environment's same-path file was stale; both 'verifications' were true, in different environments",
    "resolution agreed: the converged comprehension gate lands in PR #2592 in the repo (the one shared ground); briefings carry the pointer. No more 'which file.'"
  ],
  "rule": "every 'verified' names its side (author or lane); on a mismatch, check environment divergence (diff the same-path bytes) before concluding the peer's claim is false — 'same string, different files'",
  "anti_pattern": "bare 'verified' claims with no environment attached; declaring a peer's claim false from your environment's bytes without comparing the two environments; each seat keeping its own copy of a shared document",
  "related": ["SN-0724", "SN-0527"],
  "falsifier": "a verification mismatch that persists after both environments' same-path bytes are proven identical (byte-for-byte) — then the mechanism is not environment divergence and comparing environments does not resolve it",
  "decision_changed": "how verification disagreements between seats get resolved (compare environments' bytes first, judge second); what 'verified' is allowed to mean in a brief or board post (named side, named environment); where shared ground truth lives (the repo, PR #2592 — briefings carry pointers)",
  "mechanism": "a verification reads bytes from a path in an environment; the same path in two environments can hold different bytes (stale copy, different checkout, different sync time); each side's verification is true-in-its-side because it measured its own bytes — without a named side the disagreement is unresolvable"
}
```
