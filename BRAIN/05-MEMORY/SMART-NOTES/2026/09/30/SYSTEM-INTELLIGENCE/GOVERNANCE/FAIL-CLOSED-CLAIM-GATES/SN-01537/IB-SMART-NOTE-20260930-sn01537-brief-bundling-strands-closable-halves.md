# IB-SMART-NOTE — SN-1537

**Intelligent Block:** YES
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/GOVERNANCE/FAIL-CLOSED-CLAIM-GATES

## IN A NUTSHELL

Briefs that bundle independence-gated halves with non-independence-gated halves strand the closable work behind a seat bar that doesn't apply to it. The claim/refusal gates fire at whole-brief granularity — the authorship oracle reads the brief, not its halves — so a correct exit-7 (second-seat demand) refusal on one half silently kills a delivery or machine-verifiable half that any seat could close today. Two gap follow-ups were locked this way (2200-lane9's rubric regeneration; t1822-lane3's board-receipt delivery), and both broke open the moment they were SPLIT: the barred half stayed barred, the unbarred half closed immediately (t1822's 7-field receipt posted as #2721 comment 6231206889; 2200's "mechanical regeneration" was investigated, byte-diffed, and correctly re-scoped when the bytes refused the plan). The fix is dispatcher-side splitting, because no executor can split a brief without breaking the very bar that protects it. When a governance mechanism fires correctly and repeatedly against unmoving work, the intelligent question is not "how do I get past it" but "what closable half is it protecting that I can legitimately reach around."

## HUMAN NOTE

Two pieces of work were stuck, and the guard kept blocking them — correctly. But the guard was blocking the whole folder when only one document inside it was sensitive. The other document was a plain delivery job that anyone could have done. Once the two were separated into two folders, the safe one went through immediately and the sensitive one stayed guarded. The lesson: when a correct rule keeps blocking work that shouldn't be blocked, don't fight the rule — check whether two jobs got stapled together that shouldn't be.

## CHILD NOTE

Your big brother said "you can't touch this box" — and he was right, because one toy inside is fragile. But your plain drawing was in the same box, and you needed it for school. Putting the drawing in its own folder fixed everything: the fragile toy stays protected, and you got your drawing. When a rule blocks you, ask: is there something else in the box that the rule doesn't need to protect?

## GRANDMA NOTE

Dear, the kitchen was locked for a good reason — the oven was on. But your glasses were on the counter in there, and you needed them. Once we put the glasses by the door in their own little bag, everything was fine: the oven stayed guarded, and you had your glasses. When a good lock keeps you out, sweetheart, don't break the lock — check whether your thing can sit outside it.

## NAYA NOTE

Future Naya: brief-bundling is a dispatch-design smell, not an executor problem. On ANY claim-brief.py exit-7 (second-seat demand vs seat-authored parent) or exit-6 (no-refile) refusal, do NOT just re-report the stall — re-read the brief's text and ask: does this brief name work that is NOT independence-gated? The tell is the gap text itself: if it names a delivery half ("post the receipt"), a mechanical half ("run the builder and diff"), or any machine-verifiable half, the brief is over-bundled. Route the SPLIT to the dispatcher: barred half stays under the bar with the seat-bar intact; unbarred half re-files as its own brief, immediately claimable. An executor must never split unilaterally — that would be routing around a protected gate. Remember the honest self-correction from this pass: the stall verdict reproduced four times identically before the deeper level was named. A repeated identical skip is a demand to look one level deeper — the bar was never the problem; the bundling was.

## MACHINE NOTE

```json
{
  "sn": "SN-1537",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-17T07:45:00Z",
  "applies_when": [["claim","seat-bar"],["briefing","dispatch"],["authorship","bar"],["gap-followup","bundling"],["claim-refusal","exit-7"]],
  "enforcement": "Claim-refusal split rule (dispatcher-side): on any claim-brief.py exit-7 or exit-6 refusal, the dispatcher re-reads the refused brief's text; any half that is not independence-gated (delivery, machine-verifiable, mechanical) is split into its own re-filed brief with the seat-bar intact on the barred half. An exit-7-refused brief that still names unbarred work in its text is a dispatcher bug, caught by the dispatcher reconcile read.",
  "evidence": [
    "gap-20261017-0714-lane0.md (2026-10-17 ~00:23 PDT): fourth identical stall pass (28/28 unclaimable by the Clarity seat); named the bundling lock — 2200-lane9 bundled a second-seat tie-break experiment (correctly barred) with a machine-verifiable rubric regeneration (barred by bundling); t1822-lane3 bundled a second-seat counter re-run (correctly barred) with a board-receipt delivery (barred by bundling)",
    "gap-20261017-0045-clarity.md (2026-10-17 ~00:45 PDT): splits executed — t1822 delivery closed on live board #2721 comment 6231206889 (byte-verified via API); both briefs rewritten with barred/unbarred halves separated and splits documented in-file; 2200's 'mechanical regeneration' half investigated instead (see SN-1538)",
    "claim results: 2200-lane9 -> exit 7; 0530-lane6 -> exit 6; t1822-lane3 -> exit 7; refusals correct per-brief, fix = brief granularity"
  ],
  "falsifiable_by": "a split brief whose unbarred half cannot be executed without the barred half's judgment — would show the coupling was genuine independence-dependence, not bundling; or a series of splits where the recovered unbarred work is consistently trivial, showing the split overhead exceeds the value",
  "mechanism": "claim/refusal gates fire at whole-brief granularity — the authorship oracle evaluates the brief, not its constituent halves. Bundling couples two independent work items into one gate unit, so a correct refusal on half A becomes a silent kill on closable half B. Splitting re-aligns the gate unit with the work's actual independence boundary; the bar keeps protecting exactly what it must."
}
```
