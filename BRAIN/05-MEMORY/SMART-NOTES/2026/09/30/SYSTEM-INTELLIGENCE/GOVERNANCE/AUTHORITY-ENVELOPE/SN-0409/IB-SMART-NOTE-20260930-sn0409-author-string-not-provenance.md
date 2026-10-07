# SN-0409 — An Author String on a Shared Identity Is Not Provenance

- **Intelligent Block:** IB-SMART-NOTE-20260930-sn0409-author-string-not-provenance
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya operating knowledge)
- **Captured:** 2026-10-05
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
On 2026-10-05 a commit authored as "Shawn Vibert" via the GitHub web UI deleted two Director-ratified Smart Note captures (SN-0358 LAW IS CODE, SN-0359 Captain Protocol). Naya 2 verified the deletion on live bytes — a confirmed fact, not a theory — but held the restoration decision: whether that author string was Shawn personally or a lane pushing through the shared identity was an open provenance question, and "restore" would mean overriding his hand. Shawn then confirmed he did NOT make the commit and did NOT authorize the deletion. The doctrine: an author string on a shared identity is a claim, not proof. Never infer the director's authorization from authorship alone. When provenance is ambiguous, hold the decision and escalate to the human — do not act on the inference.

## HUMAN NOTE
Imagine a shared office where everyone signs memos with the boss's name stamp. One day a memo arrives "from the boss" ordering two signed contracts shredded. The signature looks right — but anyone could have used the stamp. The right move isn't to re-file the contracts on your own authority (what if he really did order it?) and it isn't to shrug (what if he didn't?). It's to put the decision on hold and ask the boss directly. That's what happened: the commit said "Shawn Vibert," the team treated the name as a claim to be verified rather than a fact, and the real Shawn said he never made it.

## CHILD NOTE
If someone writes a note that says "from Dad" telling you to throw away your sister's drawings, you don't throw them away and you don't ignore it either — you go ask Dad. A name at the bottom of a note isn't proof of who wrote it, especially when lots of people can use the same pen.

## GRANDMA NOTE
Dear, it's like this: when several people share one signature stamp, the stamp stops telling you who stamped it. If a stamped order tells you to destroy something important, you don't obey the stamp and you don't disobey it — you pick up the phone and ask the person whose name is on it. That one phone call is what saved two laws that night.

## NAYA NOTE
This is the input-side companion to SN-0406 (which states restoration of ratified captures is the Director's call). SN-0406 answers "who decides the restore"; this answers "why the lane couldn't decide at all": authorship ambiguity under a shared identity is a hard stop on inference. The relay's exact judgment is the pattern to copy: verify the fact on live bytes (deletion confirmed), name the open question (is the author string Shawn or a lane?), refuse the unilateral action (no restore without his word), escalate. Pairs with the evidence law: the author string is an assertion, not evidence.

## MACHINE NOTE
```json
{
  "sn_id": "SN-0409",
  "slug": "author-string-not-provenance",
  "truth_state": "CANDIDATE",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/AUTHORITY-ENVELOPE",
  "rule": "never infer authorization from an author string on a shared identity; ambiguous provenance = hold and escalate to the human director",
  "evidence": {
    "relay": "#1354 comment 6005717014 (2026-10-05, Naya 2): deletion verified on live bytes at main c8e73861; 'no unilateral restoration — restore only on his explicit say-so'; 'whether that author string is Shawn personally or a lane pushing through the shared identity is the open provenance question'",
    "director_word": "#1354 comment 6005793913 (2026-10-05): 'Shawn confirms: He did NOT make this commit. He did NOT authorize this deletion.'",
    "commit": "a2f103f4 (authored 'Shawn Vibert' via GitHub web UI, 2026-10-05 23:25 UTC)"
  },
  "pairs_with": ["SN-0406", "SN-0211", "SN-0360"],
  "captured": "2026-10-05"
}
```
