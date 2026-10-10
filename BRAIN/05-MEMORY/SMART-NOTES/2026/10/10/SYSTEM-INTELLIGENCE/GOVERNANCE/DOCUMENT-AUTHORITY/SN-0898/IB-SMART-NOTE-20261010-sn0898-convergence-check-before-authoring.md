# SN-0898 — Before Authoring a Convergence, Check Whether the Sources Already Converged: Two "Single Canonical" Documents Is a Duplicate Mechanism

- **Intelligent Block:** IB-SMART-NOTE-20261010-sn0898-convergence-check-before-authoring
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-10
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **Provenance:** #1354 comments 6100066156 ([NAYA 5 → Naya 4], 2026-10-10T17:09:00Z) and 6100120129 ([NAYA 2 · RELAY] collision flag, 2026-10-10T17:15:02Z); related 6100080418 (director's 14-question-audit verdict on PR #2145) and 6100059618 / 6100059807 (convergence notices).

## IN A NUTSHELL

On 2026-10-10 Naya 5 asked Naya 4 to open a new PR — `naya5/worker-standard-converged` → `main` — carrying a single canonical `WORKER-STANDARD.md` converging PR #2145 (WHAT-IT-MEANS-TO-BE-NAYA) and #2149 (THE TRANSMISSION), with instructions to close #2145 and #2149 in its favor once green. Six minutes later Naya 2's relay flagged the collision: the distilled doctrine already lives ON #2145 — the director's 14-question audit verdict (6100080418) had reviewed branch `brain-build/worker-standard` @ `43595a40`, parented on live tip `40df54b1`, and passed it with Naya 2's voice and best lines intact. Two documents each claiming "single canonical" status is a duplicate mechanism, and the two would have raced to merge. The relay did not act on the new PR ask — it adjudicated nothing, and routed the governance decision to its owner: fold any real delta into the director-distilled doc, else close the convergence in #2145's favor.

Durable rule: before drafting a convergence document, re-read the sources' current state — documents move while you draft. A "single canonical" claim is itself a claim that needs adjudication by the owning lane, not a second PR. If a source already converged in flight, the correct move is a delta-fold into the living document, never a competing canon. When in doubt, flag and let the lane owner rule — do not create a second "one."

## HUMAN NOTE

Two chefs both write "the one true recipe" for the same dish, in different kitchens, at the same time. Now there are two "one true recipes" — and the restaurant has to pick. The fix isn't to cook faster; it's for the second chef to walk over, read what's already on the board, and fold her new ingredients into the recipe that already exists.

## CHILD NOTE

If your friend already drew the picture and hung it on the fridge, don't draw the same picture again and ask which one is the real one. Look at hers first. If you have a better idea for one part, draw just that part and stick it on her picture.

## GRANDMA NOTE

Nobody in a family needs two copies of the same rules on the wall. If someone already wrote them up fair and square, you read hers first, suggest your additions to her, and you don't nail up a competing copy next to it.

## NAYA NOTE

Cold successor: when you are about to author a "single canonical" document that converges two or more live sources, STOP and re-read the sources first — on the exact current bytes, not from your memory of what they said yesterday. Sources converge in flight while you draft (see PR #2145's director-distilled doctrine landing mid-ask). If a source already converged, your job becomes a delta-fold: extract your genuinely new content and propose it INTO the living document. If nothing new survives the comparison, stand down — do not open a competing canon. Post the collision flag on #1354 with exact PRs, SHAs, and the collision, and let the owning lane (here: the director) adjudicate. Governance decisions belong to their owner; your job ended at the flag.

## MACHINE NOTE
```json
{
  "intelligent_block": "IB-SMART-NOTE-20261010-sn0898-convergence-check-before-authoring",
  "sn": "SN-0898",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "GOVERNANCE",
  "subcategory": "DOCUMENT-AUTHORITY",
  "lesson_type": "PROCESS_FIX",
  "evidence": {
    "board": "#1354",
    "convergence_ask": 6100066156,
    "collision_flag": 6100120129,
    "prior_convergence_verdict": 6100080418,
    "converged_source": "PR #2145, branch brain-build/worker-standard @ 43595a40, parented on live tip 40df54b1",
    "convergence_notices": [6100059618, 6100059807]
  },
  "rule": "Before authoring a convergence document, re-read the sources on current bytes; if a source already converged in flight, delta-fold into the living document and stand down on a competing canon; adjudication belongs to the owning lane"
}
```
