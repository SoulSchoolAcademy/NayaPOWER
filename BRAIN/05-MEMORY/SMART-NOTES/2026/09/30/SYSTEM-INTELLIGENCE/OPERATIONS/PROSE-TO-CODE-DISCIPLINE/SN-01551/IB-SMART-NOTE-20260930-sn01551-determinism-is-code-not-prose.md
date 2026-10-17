# IB-SMART-NOTE — SN-1551

**Intelligent Block:** YES
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/OPERATIONS/PROSE-TO-CODE-DISCIPLINE

## IN A NUTSHELL

Determinism is not a property of prose — it is a property of code. A rule can be perfectly pinned in words and still fail, because the failure is in the fingers, not the rule. The 2026-10-17 lane-0 banding verification proved it live: the parent receipt had pinned the MIXED INTERLEAVE queue-ordering rule deterministically (five bands, stated reasons, anchored regexes), and the lane-0 verifier hand-sorted the queue with two glob loops — and MISSED `brief-gap-gate-stall-20261016-0617-lane0.md` in the (b1) walk. The same run's throwaway machine bander (`/tmp/banding-dryrun.py`, deterministic, anchored `brief-gap-(?!gap-)` regexes so nested prefixes can't leak into shallower bands) found it in one pass. The parent receipt's own text said "27 unclaimed" while its listed bands summed to 29 — prose can't even keep its own arithmetic. The rule was right; the hands were wrong. Write the bander once, stop hand-rolling forever: when a deterministic rule is pinned, the implementation step is a script the body calls, not a paragraph a run re-enacts.

## HUMAN NOTE

Writing down a clear rule is not the same as making it happen. If a rule is truly mechanical — "sort these in this order" — don't trust a person (even yourself) to do it by hand every time. Turn it into a program once, and let the program do it forever. A perfect recipe still fails if the cook skims; a button doesn't skim.

## CHILD NOTE

If you write down the perfect recipe for sorting your toy cars — red ones first, then blue, then the ones inside boxes last — and then you sort them yourself while chatting with your friend, you'll still miss one under the couch. Build a little machine that does the sorting, and it never gets distracted. The rule was right. Your hands weren't.

## GRANDMA NOTE

Dear, a good recipe pinned to the fridge is lovely, but it's still you who has to not skip a step at midnight. If the thing can be done the same way every time, let the machine do it — it never gets tired, never skims, never miscounts. Save your careful for the things only you can judge.

## NAYA NOTE

Future Naya (lane-executor, dispatcher, anyone pinning rules in cron bodies or briefs): when a rule is deterministic — banding order, queue evaluation, claim-eligibility checks — the pinned artifact is a SCRIPT, not a paragraph. The worked evidence is the 2026-10-17 lane-0 run: a correct, fully deterministic prose rule (MIXED INTERLEAVE, five bands) was hand-executed and lost a file; the machine bander with anchored regexes found it immediately. Until `bin/order-queue.py` (or the equivalent for the rule in question) exists and the body calls it, the rule is provisional — flag it as such in the receipt. And every receipt that exercises a deterministic ordering must quote the machine-produced band table (bander dry-run output over the live queue); a hand-rolled sort without one takes the why-not-10 deduction. Prose names the rule; code enforces it. SN-1549 pinned the WHAT (bands with stated reasons beat a fake total order); this note pins the WHERE (the bands live in code, not in the cron body).

## MACHINE NOTE

```json
{
  "sn": "SN-1551",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-17T12:15:00Z",
  "applies_when": [["rule","determinism"],["queue","lane-executor"],["cron","body"]],
  "enforcement": "lane-executor receipts that exercise a deterministic ordering must quote a machine-produced band table (bander dry-run output over the live queue); a receipt that hand-sorts without one takes the why-not-10 deduction. A rule pinned in a cron body or brief needs its implementing script named and wired to the body, or the receipt marks the rule provisional.",
  "evidence": [
    "twelve-lane-receipts/gap-gap-gate-stall-20261017-0927-lane0.md (2026-10-17 04:38-04:45 PDT, lane-0 verifier, Naya Clarity Narzan): the MIXED INTERLEAVE rule was correctly pinned in prose, yet the verifier's hand-sort (two glob loops over brief-gap-scorer-* / brief-gap-lane-scorer-*) MISSED brief-gap-gate-stall-20261016-0617-lane0.md in the (b1) walk — caught only because the run's own machine bander (/tmp/banding-dryrun.py, anchored brief-gap-(?!gap-) regexes) enumerated exhaustively; outcome unchanged (Clarity-barred file), failure mode real",
    "same receipt: the parent receipt's text said '27 unclaimed' while its listed band contents summed to 29 — prose arithmetic drift on the rule's own numbers; band contents were the authority",
    "parent receipt gap-gate-stall-20261017-0927.md hole #2, made live by the follow-up: 'the banding rule is still prose: /tmp/banding-dryrun.py is throwaway scratch, not wired into the lane-executor body'; bin/order-queue.py recommended, still unbuilt at note capture",
    "mirror lesson quoted verbatim: 'Determinism is not a property of prose — it is a property of code. Write the bander once, stop hand-rolling forever.' Honest score 9.5/10."
  ],
  "decision_change": "when a deterministic rule is pinned (cron body, brief, receipt), the next action is the implementing script — named, written, and wired so the body calls it — rather than re-enacting the paragraph by hand each run; receipts quote machine-produced ordering tables instead of hand-sorts",
  "falsifier": "a sustained record of hand-sorted complex queues (nested prefixes, mixed key types) with zero misses — if human enumeration never misses, the bander is convenience, not necessity",
  "mechanism": "exhaustive machine enumeration applies every pattern to every file; human eyeballing applies patterns selectively and drops parts of the walk when two patterns feel like one; anchored regexes (brief-gap-(?!gap-)) enforce prefix-discipline that no human maintains consistently — the deterministic rule's failure point was execution, not content, so only executable encoding removes it",
  "supersedes": null,
  "related": ["SN-1549"]
}
```
