# A Headline Is a Claim About the World, Not the Branch — Verify the Landing, Not Just the Commit

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0819-headline-is-a-claim-about-the-world
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** distillation loop, #1354 comments 6088682040 / 6088766245 (2026-10-09).
**Provenance:** #1354 6088682040 (independent cold retester verdict, successor-ingest R1/R2, 2026-10-09T20:26:13Z — "Now on main" headline falsified by 404-check); #1354 6088766245 (narrow fixer report, polish COMPLETE, 2026-10-09T20:31:51Z — v3.5 correction convention); #1354 6088839437 (confirmer: freshness check caught real drift mid-run).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The successor-ingest kit (cold-start packet + retrieval tools + freshness guard) was built at honest 8.5 and retested by an independent stranger at 9.8 — machinery end-to-end VERIFIED: activation 10.0/10 first attempt, fail-closed refusals, freshness both directions. But R1/R2 as literally specified was NOT met, on a single sentence: the packet's cover page said "Now on main (RUNG 1)." The retester didn't trust it — she 404-checked `COLD-START-PACKET.md` on live main, and it wasn't there. The kit was branch-only, never merged; a newcomer walking in the front door couldn't find it. One invented landing sentence cost R1/R2 despite 9.8-grade machinery. The narrow fix (v3.5) corrected the headline to the branch-tip truth, named the failed check, annotated the false bullet as superseded, and left the genuinely-true "on main" claims (checker, gates, manifest, PR #2004) alone — each annotated by evidence, not deleted. The durable doctrine, in the fixer's words: **a false status headline is worse than a missing one**, because a missing one invites a check while a false one invites misplaced trust. Three refinements for the cold successor: (1) "on main" is a claim about the world, not about a branch — verify the landing with a world-check (404-check the live path, pull the live ref), never trust the commit's self-description; (2) branch≠main is exact-state language with teeth — the retester's refusal to grant R1-4 on "a technicality that isn't a technicality" is the evidence law working; (3) **tools' stdout messages are sentences too** — the freshness checker printed a false "pin X == live tip Y" equality in its success path, a third lie hiding in a success message, fixed in the same pass. The v3.5 convention (newest dated section wins, history kept verbatim) made the correction cheap and auditable — annotate false claims, don't rewrite them.

## 🩷 HUMAN NOTE

Shawn — the cold-start kit worked beautifully: a stranger woke up with it, found the lesson diary, and proved every lesson first try. But the kit's cover page said "now on main" — and it wasn't on main. The independent retester checked instead of trusting, refused the round on that one sentence, and she was right: 9.8-grade machinery with one invented landing line. The fixer corrected it in place — the new version says plainly "candidate on the branch tip, NOT on main," names the failed check, and keeps the false old line visible but marked as superseded so the history is auditable. The lesson: a missing headline invites someone to check; a false headline invites someone to trust the wrong thing. And check your tools' success messages too — one tool was printing "everything matches" when it didn't.

## 👶 CHILD NOTE

Imagine you built an amazing treasure map and put a note on the cover saying "this treasure is in the school library." But the treasure is actually still in your backpack! Your friend checks the library, finds nothing, and says the treasure isn't real — because she trusted your cover note instead of checking your backpack. Your map was perfect; only the cover note was wrong. That's why every note on the cover has to be true: check where the thing really is, not where your note says it is. And fix a wrong note by writing the true one next to it — don't erase the old one, or nobody learns from the mistake.

## 👵 GRANDMA NOTE

Dear, this is about honesty in labeling. The team built a beautiful welcome kit for newcomers — everything inside worked perfectly. But the label on the box said "now in the main building," and it was still sitting on a side workbench. A sharp tester went to the main building, found nothing, and honestly said the box hadn't arrived. She was right. The fix was simple: relabel the box to say where it really is, and keep the old label visible but marked as wrong. A missing label makes people look; a wrong label makes people look in the wrong place. And the sharpest part — she also caught a tool that *said* "all good" on its screen when things weren't. Labels and screens both have to tell the truth.

## 🤖 NAYA NOTE

When writing or reviewing status claims in docs, packet headers, and tool output:

1. **Classify the claim's target.** "On main," "deployed," "landed," "live" are claims about the *world* (a live ref, a reachable path, a production state). Claims about the world require world-checks: 404-check the live path, `ls-remote` the live ref, pull the live tree — never trust the branch's self-description.
2. **Use exact-state language.** "Candidate on the branch tip — NOT on main" is a complete, honest status. "Now on main" with nothing on main is not a technicality — it is the claim the next seat acts on, so getting it wrong is getting the world wrong.
3. **Annotate false claims; don't erase them.** The v3.5 convention: keep history verbatim, add a newest dated section that names what was false, what the evidence showed, and what replaces it. A corrected record teaches; a rewritten one hides the lesson.
4. **Audit success messages as claims.** If a tool prints "pin X == live tip Y" in its success path, that equality is a sentence — make it the true relation ("pin = acceptance baseline, live tip = N commits past pin"). A false sentence in a green path is worse than a crash, because nobody re-checks green.
5. **Verify the landing, not just the commit.** The commit existing on a branch proves the commit; it proves nothing about the world. This is the evidence-law applied to status: the thing proven must be the thing claimed.

## 🧠 MACHINE NOTE

```json
{
  "sn": "SN-0819",
  "class": "ENGINEERING-PROOF",
  "subcategory": "INDEPENDENT-VERIFICATION",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": "Status claims about the world ('on main', 'landed', 'live') require world-checks, not branch-checks: verify the landing (404-check the live path, ls-remote the live ref) before writing the headline; a false status headline is worse than a missing one; annotate false claims in place (v3.5 convention: newest dated section wins, history kept verbatim); tools' stdout success messages are claims too.",
  "worked_example": {
    "artifact": "COLD-START-PACKET.md v3.4, successor-ingest R1/R2 kit, builder claim 'Now on main (RUNG 1)'",
    "falsification": "independent cold retester 404-checked the packet on live main — not there; kit branch-only, never merged; R1/R2 refused on branch≠main exact-state language (not a technicality)",
    "fix": "v3.5: header 'Status: candidate on the branch tip — NOT on main'; false bullet annotated superseded; freshness checker success message corrected to the true pin-vs-tip relation; step-1 snippet refusal cleaned (traceback -> exit 3 REFUSED); retester artifacts persisted from /tmp before evaporation",
    "board_comment": "#1354 6088682040 (retester), #1354 6088766245 (fixer), #1354 6088839437 (confirmer: freshness guard caught real mid-run drift)"
  },
  "related": ["SN-0493", "SN-0531", "SN-0603"]
}
```
