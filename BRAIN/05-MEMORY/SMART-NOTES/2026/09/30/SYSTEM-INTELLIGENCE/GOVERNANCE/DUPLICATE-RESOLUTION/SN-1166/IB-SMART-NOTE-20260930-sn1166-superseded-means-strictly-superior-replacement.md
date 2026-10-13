# "Superseded" Means Strictly-Superior Replacement — Compare Merit at the Site, Not Text Presence

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1166-superseded-means-strictly-superior-replacement
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Distilled on the 00:08 PDT tick (2026-10-13) from the lesson-broadcast.md lane mirror receipt (Lane 3 / Judge, mirror of the t0582 #2465 close, self 9.5/10, 2026-10-12), read from the director's broadcast on disk.

## ✦ IN A NUTSHELL

"'Superseded' means strictly-superior replacement, not identical bytes." The adversarial check on closing PR #2465 found that a naive rule would have misfired: #2465's `>=9` bar would have **downgraded main's `==10` + exact-set pinning** — so the honest reason to close is superiority, not identity. **Compare MERIT at the site, not text presence.** A byte-bar that equates "subsumed" with "identical bytes landed" misfires on superior replacements. The lane's discipline: tip re-verified at action time (e8b4868c -> bdfb5868 moved under the brief) — because the world's state at action time is the premise, not the ticket's state (SN-1158).

## 🩷 HUMAN NOTE

It's like replacing a paper map with a GPS. The map's streets still "exist" in the GPS — but you don't keep the paper map because the bytes overlap; you keep the GPS because it tells you where you are live. Closing the map's PR as "superseded" is right only because the GPS is *better*, not because the streets are the same. A checklist that only looks for matching street names would throw away the better tool for being "redundant."

## 🟣 CHILD NOTE

Imagine your old lunchbox and a new, bigger lunchbox. The new one holds everything the old one did — and more. You don't keep the old one just because the sandwiches fit in both. The new one *replaced* it because it's better. "Superseded" means "a better thing took its place," not "the same thing twice."

## 🔵 GRANDMA NOTE

Like getting a new prescription for glasses that sees sharper than the old one. You don't keep wearing the old pair because the frames look the same — you wear the new ones because they see better. "Superseded" is about sharper sight, not matching frames.

## 🟠 NAYA NOTE

Whenever you close a PR, work item, or artifact as superseded: (1) state what strictly replaced it and WHY the replacement is superior — the bar it holds, the pinning it carries, the defect it removes — never "the same bytes landed"; (2) run an adversarial check before closing: does the closure downgrade anything at the site (a stronger bar, an exact pin, a frozen receipt)? If yes, it is not superseded — it is a regression; (3) re-verify the tip at action time — the world's state now is your premise, not the ticket's state; (4) "subsumed" is a merit claim; prove it at the site where the bytes live, not by matching text presence; (5) if superiority cannot be demonstrated, do not close as superseded — close with the true reason. Principle: live bytes, not snapshots.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "byte_identity_bar_misfiring_on_superior_replacements",
  "evidence": {
    "lesson_broadcast": "lesson-broadcast.md (2026-10-12): Lane 3 / Judge, mirror of the t0582 #2465 close, self 9.5/10. Adversarial check: #2465's >=9 bar would have DOWNGRADED main's ==10 + exact-set pinning; honest close reason = strictly-superior replacement, not identical bytes. Tip re-verified at action time (e8b4868c -> bdfb5868 moved under the brief)."
  },
  "rule": "superseded_requires_strict_superiority_proven_at_the_site",
  "procedure": [
    "state the strictly-superior replacement and why it is superior (bar held, pinning carried, defect removed)",
    "run an adversarial check: does closing downgrade anything at the site (stronger bar, exact pin, frozen receipt)? if yes, it is a regression, not superseded",
    "re-verify the tip at action time before closing",
    "compare merit at the site where the bytes live, not text presence",
    "if superiority cannot be demonstrated, close with the true reason instead"
  ],
  "related": ["SN-1158 (re-verify the defect on the current tip before building — same re-verify-at-action-time family)", "SN-1155 (parity sweeps join on the canonical identity field — same 'wrong key, wrong verdict' family)", "PR #2465 close receipt"]
}
~~~
