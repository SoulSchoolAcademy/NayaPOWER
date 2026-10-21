# Stand Down the Unpushed Repair — Verify the Other Lane's Instead

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0508-stand-down-the-unpushed-repair
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6027918530 ([NAYA 2] brain drive run, 2026-10-07T00:13:05Z) + #1354 6027922625 ([NAYA 2][BRAIN-BUILD] battery receipt, 2026-10-07T00:13:26Z) — both SoulSchoolAcademy.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 2 found the brain-index RED on main at `8df3565c` (docs commits `427fc906`/`8df3565c` landed without regenerating; REAL-TREE.json/md stale, basis pointer `fc8cf75c`), built a full mechanical repair branch against that tip — full battery green on those exact bytes (924 passed / 11 skipped / 0 failed, no exclusions; adversarial harness 6/6 PASS) — and then, when the tip moved twice mid-run (`1204519c5` → `8df3565c4` → `3f1e6d78`) and **#1668 merged, healing the same seam**, she stood the repair down **before pushing**, opened no PR, attempted no merge, and instead independently verified the other lane's repair on the live bytes: `regenerate_brain_index.py --check` → OK (228 files), full pytest 929 passed / 11 skipped / 0 failed, no exclusions.

This is SN-0493 (a decision expires when the tip moves) fused with SN-0236 (one repair per RED class, never duplicate) into a single motion — and it establishes the bar that matters: **the stand-down bar is whether the branch has been pushed.** An unpublished branch costs nothing; a duplicate repair PR costs the lane its heal path, its review bandwidth, and its single owner. When the tip moves and another lane carries the repair forward, your repair is dead by definition — do not resurrect it as a competing PR to "prove" the work. Independently verify their bytes instead; a second seat's green receipt on the same fix is worth more than two branches.

Why this is brain-grade: lanes will always race the same REDs. The race is not won by whoever publishes first — it is won by whoever notices the seam is already healed and converts their repair effort into independent verification of the surviving repair. That is the whole difference between two competing fixes and one fixed seam with a witness.

## 🩷 HUMAN NOTE

Shawn — one lane did something exactly right tonight that's worth banking. Naya 2 found a real RED on main (brain index stale from docs commits), built the complete repair, tested it fully green — and then another lane merged the fix first. Instead of pushing her competing branch anyway, she threw it away unpublished, verified the other lane's fix on the live tip herself, and reported the seam healed with her own green receipt. Rule for the team: if your repair branch hasn't been pushed when the seam gets healed, you don't have a repair anymore — you have a second witness. An unpushed branch costs nothing; a duplicate PR costs the team. Her verification of #1668 is worth more than a competing PR would have been.

## 🟣 CHILD NOTE

Imagine two kids racing to fix a broken toy. One of them finishes fixing it first — the other kid was already halfway done with her own fix. The smart move isn't to keep going and hand over two half-fixed toys. The smart move is to put your half-fixed toy down (you hadn't shown it to anyone yet, so nobody misses it) and instead TEST the fixed toy really carefully, so now there are two people who agree it's fixed. That's what Naya 2 did: she had a full green repair ready, saw that #1668 already healed the seam, stood her branch down before pushing, and verified the other lane's repair on the live bytes herself. Rule: if you haven't pushed your fix yet, there's nothing to withdraw — verify the winner instead. Two witnesses on one repair beats two competing repairs.

## 👵 GRANDMA NOTE

Two cooks in a kitchen both notice the pot is boiling over. One grabs the lid and settles it. The other, who was reaching for a lid too, doesn't throw her lid on top of his — she checks that the pot is actually settled, and says so. That second pair of eyes is what turned a fixed problem into a proven-fixed problem. The rule is simple and kind to everyone in the kitchen: if your fix never left your hands, put it down. What the team needs from you then is not another fix — it's an honest second check on the one that landed. Competing fixes create arguments; a fix plus a witness creates confidence.

## 💜 NAYA NOTE

Note to future me: when you find a RED, build the repair, and then the tip moves and another lane heals the seam before you push — **stand down before pushing.** The exact bar: if the branch is unpushed, it costs nothing to abandon; if you push it anyway to "show the work," you create a duplicate repair the lane has to reconcile. Do what Naya 2 did on 2026-10-06: stand the branch down, then independently verify the surviving repair on the live bytes (`--check` clean + full battery on the new tip) and post that receipt. Your green receipt on someone else's repair is a second-seat verification — it is worth strictly more than a competing PR. Family: SN-0493 (re-verify at action time — your repair was decided on dead bytes) :: SN-0236 (one repair per RED class — the other lane owns the class now) :: SN-0440 (one exact-tip battery is enough — cite their bytes, not yours).

## ⚙️ MACHINE NOTE

{"sn": "SN-0508", "title": "Stand Down the Unpushed Repair — Verify the Other Lane's Instead", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-06", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "REPAIR-STAND-DOWN"], "cousins": ["SN-0493", "SN-0236", "SN-0440"], "authority": "observed episode — NAYA 2 brain drive run + battery receipt 2026-10-07T00:13–00:14Z, CANDIDATE (auto-capture, not ratified)", "evidence": {"board": ["#1354 6027918530 ([NAYA 2] brain drive run — tip moved 1204519c5 → 8df3565c4 → 3f1e6d78 mid-run; prepared mechanical regen branch on 8df3565c4, full battery green (924 passed / 11 skipped / 0 failed, adversarial 6/6 PASS); stood it down before pushing when #1668 merged; verified --check clean (228 files) + pytest 929/11/0 on live tip 3f1e6d78; no PR opened, no merge attempted, 2026-10-07T00:13:05Z)", "#1354 6027922625 ([NAYA 2][BRAIN-BUILD] battery receipt — found RED on main @ 8df3565c: brain index --check failed, REAL-TREE.json/md stale, basis pointer fc8cf75c, docs commits 427fc906/8df3565c landed without regenerating; verified repair instead of duplicating it: #1668's repair stands verified, 2026-10-07T00:13:26Z)"]}, "doctrine": {"stand_down_bar": "if the repair branch is unpushed when the seam heals under another lane, abandon it — an unpublished branch costs nothing, a duplicate repair PR costs the lane", "convert_to_witness": "independently verify the surviving repair on the live bytes (--check + full battery at the new tip) and post that receipt; a second-seat green receipt is worth more than a competing PR", "family": "SN-0493 (decision computed on dead bytes is inadmissible) :: SN-0236 (one repair per RED class — the other lane owns the class) :: SN-0440 (cite the surviving bytes, not your dead branch)"}}
