# Intelligent Block
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04 ~16:15 PDT (Smart Note distillation tick)
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**SN number:** SN-0287
**Provenance:** #1354 comment 5985355146 (2026-10-04T22:56:28Z — "Naya 2 — click test caught a real Hub-wide defect; fixed on PR #1413") and follow-up 5985410339 (2026-10-04T23:04:02Z — "full button audit on PR #1413: ALL WORKING, no dead controls", freeze point `035dbd20`). Commit `035dbd20` (byte-verified), follow-on fix `415cbd0d` (notify-once guard, byte-verified).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL

**Test the feedback path, not just the buttons.** Naya 2 click-tested the Naya Play button on the frozen Hub build (`21192fdd`): the button rendered perfectly and the missing-audio path fired — but the `VOICE NOT READY` toast was never human-readable. It flashed in the DOM sub-second and vanished. Root cause: the Hub's single `toast()` is implemented as `toast(message, accent, ms)`, but **all 10 board-action call sites invoke it as `toast(title, message, color)`** — the color string landed in the `ms` slot, `setTimeout` got `NaN`, and **every** board toast (LOVE / LIKE / RATE / SHARE / PLAY / …) has been dismissing in ~0ms. **The buttons all worked; their feedback never showed.** A defect class hiding in plain sight: action-complete, feedback-dead. The fix (commit `035dbd20`, byte-verified, on PR #1413): the toast now honors BOTH conventions in use — numeric 3rd arg = duration ms, string 3rd arg = accent color. All previously-working call sites render byte-identical output; the 10 broken ones now show title + message for the full duration. No presentation restyle. Then the full button audit on the new freeze point (`035dbd20`, live browser render): FAVORITE/SAVE toggles, CREATE SPACE, LOVE/LIKE counts, star rating, SHARE INTEL, ADD INTEL, NAYA PLAY — all working, no dead controls. It also caught a follow-on micro-defect: a missing-audio click stacked TWO "VOICE NOT READY" toasts (404 fires both `onerror` and rejected `play()`), fixed with a notify-once guard in `415cbd0d`. The durable doctrine: (1) user-visible correctness lives in the feedback loop, not the action handler — audit toast/feedback paths with the same rigor as the click handlers; (2) freeze-point click testing is the instrument — render at a pinned SHA, click everything, watch what the user sees; (3) when a signature is invoked two ways in the wild, honor both conventions rather than rewriting all call sites — minimal blast radius, byte-identical output for the working ones.

## HUMAN NOTE

Shawn — banking a Hub verification lesson from Naya 2's click test: every board toast on the Hub was silently broken. All ten action buttons worked fine, but the `toast()` calls passed a color where the duration goes, so the feedback flashed and vanished in milliseconds. Nobody noticed because the buttons "worked." The fix honors both calling conventions instead of rewriting ten call sites — zero blast radius on the working ones. The follow-up audit proved every control on the freeze point, and caught a second tiny bug (double toasts on missing audio) fixed the same way. The rule I'm saving: **buttons working ≠ UX working — click-test the feedback path, not just the action.** Every room audit from here on runs the click test against the freeze point and watches what actually shows on screen, not just what fires in the DOM.

## CHILD NOTE

Imagine every light switch in a house works perfectly — but the little lamp that's supposed to say "good job, the light is on" burns out in a millisecond, every time, in every room. Nobody notices for weeks because the lights themselves work. One day someone watches a switch instead of just flipping it, and sees the "good job" lamp flash and die. That's what happened: ten buttons worked, but their "you did it" messages all vanished instantly, because the instructions were calling the message box the wrong way. The fix: the message box now understands both ways people were calling it. The lesson: always check the "you did it" message, not just the button — and if one call slips through two holes (a missing sound made TWO error messages), add a guard so it only speaks once.

## GRANDMA NOTE

We've written down a testing rule from the Hub work. Ten buttons on the app all worked correctly, but the little confirmation messages that pop up after each button were all disappearing in a blink — a color was being sent where a duration was expected, so every message timed out instantly. The buttons seemed fine, so nobody noticed the messages were broken. The rule: **test what the user sees, not just what the button does.** Check the confirmation messages as carefully as the buttons themselves. When a helper is being called two different ways, make it understand both rather than rewriting every call. And when a single error makes the same message appear twice, add a guard so it only appears once. Test from a fixed, named version so the results are reproducible.

## NAYA NOTE

For me, months from now: the feedback-path defect is a whole class — action-complete, feedback-dead — and it's invisible to any test that only asserts the action fired. Standing audit discipline for Hub work: (1) render the FREEZE POINT in a live browser (pin the SHA — `21192fdd` then `035dbd20`); (2) click every control; (3) watch what renders on screen for the full duration, not just the DOM event; (4) audit every toast/feedback call site for signature drift (`toast(title, message, color)` vs `toast(message, accent, ms)` — a string in a ms slot is a silent NaN timeout); (5) when both conventions exist in the wild, honor both (numeric = duration, string = accent) — minimal blast radius, byte-identical output for the working call sites. Follow-on micro-defects ride the same audit: stacked toasts from 404 + rejected `play()` → notify-once guard (`415cbd0d`, byte-verified). Related: SN-0219 (verify at the live site / user's viewport), SN-0206 (freeze discipline).

## MACHINE NOTE
```json
{
  "sn": "SN-0287",
  "title": "Click-Test the Feedback Path: Buttons Working Does Not Mean UX Working",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-04",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "SYSTEM-DESIGN", "HUB-COMPOSITION"],
  "cousins": ["SN-0219", "SN-0206"],
  "evidence": {
    "comments": "#1354 5985355146 (2026-10-04T22:56:28Z) / follow-up 5985410339 (2026-10-04T23:04:02Z)",
    "defect": "toast(message, accent, ms) implementation; 10 call sites invoke toast(title, message, color) — color string in ms slot -> setTimeout(NaN) -> ~0ms dismissal on all board toasts",
    "fix": "commit 035dbd20 (byte-verified) honors both conventions; notify-once guard 415cbd0d for stacked missing-audio toasts",
    "audit": "full button audit on freeze point 035dbd20 in live browser render — ALL WORKING, no dead controls"
  },
  "rules": [
    "audit the feedback path with the same rigor as the action handler — user-visible correctness lives in the feedback loop",
    "freeze-point click testing: render at a pinned SHA, click everything, watch what the user sees for the full duration",
    "when a signature is invoked two ways in the wild, honor both conventions — minimal blast radius",
    "stacked notifications from multiple error paths need a notify-once guard"
  ],
  "durable_test": "A cold Naya auditing a Hub room will (1) pin a freeze SHA, (2) click every control in a live browser, (3) watch every toast/feedback for its full duration, (4) check every feedback call site for argument-order drift."
}
```
