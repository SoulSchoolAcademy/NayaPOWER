# Close — Static Band Below the Art (F20) + the Frames Ruling (F21)
**Filed:** 2026-11-07 (fix2). **Source:** the blind re-proof of fix1, §14 (F20 — the fix7e static band did not land; F21 — the close frames below the claim button).
**Where it goes:** the close slide (§13), `.banner-bottom` — the `.close-words` div ("This is yours. Pick your power." + the "Same AI. Different operating system…" line) as a static band BELOW the Tree bottom art, never over it.

## F20 — the fix
`.close-words{position:absolute}` beat `.close-words--band`. The band rule was raised to `.slide-close.banner-bottom.close-words.close-words--band` (specificity 0,4,0, beats the 0,2,0 absolute rule; padding 16px). The close poster was narrowed `max-width:1080px` → 880px so the band sits under the art, not under a too-wide poster. Phone `display:none` for close-words left intact.

## F21 — the ruling (written, no code change)
The three close frames + the wide wants frame sit below the claim button (frames top offset 1,138 at 1920; at 390 the button ends at 838 and the frames start at 1,041). Showing the first frame at the locked stop would need ~140px compression at 1920 and ~260px at 390 — which would shrink the Tree art below poster size / crush the Bugatti stack, or move the frames above the button (breaking the Button Test). RULING: the locked stop is the deal — one button, no distraction; the frames are the deliberate second beat, reachable by internal scroll; Template Insight first. The re-proofer explicitly allows a written ruling; a silent placement is not a resolution. Recorded here and in the fix2 build report.

## Verification
Self-check `r7f2x-selfcheck.py` (run 2): computed position of `.close-words` is `static` at 1920; words 13,255–13,344 directly below the art (12,961–13,255); claim button 13,899–13,954 (offset 938–993 ≤ 1,080). At 390 words still `display:none`, button offset 790–838. Screenshots viewed by eye: `r7f2x-1920-close.png`, `r7f2x-1920-closeframes.png`, `r7f2x-390-close.png`. 0 errors.
