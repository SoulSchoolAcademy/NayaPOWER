# IB-SMART-NOTE-20260930-sn01766-fix-the-checker-never-dodge-the-template

Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-21
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
When a safety check false-positives on our own template, the fix goes in the checker — never in the template. Rewording the template to dodge the check is evasion debt: it trains the pipeline to treat our own briefs as evadable text and leaves the checker's broken model latent, so every reword recurs. The 2026-10-21 dispatch-HELD P0 (the runtime prompt-injection safety check tripping on spawn_brief.py's own activation sentence) was resolved exactly this way: recalibrate the brief-path safety check, do not reword the template around it.

## 🩷 HUMAN NOTE
A fire alarm goes off every time you cook toast. You have two choices: disconnect the alarm's toast sensor (recalibrate the checker) or stop making toast (reword the template). Stopping toast means the alarm "works" again — but the house still has a broken alarm, and now everyone tiptoes around their own kitchen. The dispatch-HELD P0 was this: our own safety check decided our own briefs looked like injections, so no briefs could reach a worker for five waves. The team's call was to fix the alarm, not ban the toast.

## 🟣 CHILD NOTE
Your smoke detector beeps whenever you take a hot shower. Your sibling says: "Let's just stop showering." That would stop the beeping — but now nobody showers! The smarter fix is to adjust the detector so it knows the difference between steam and smoke. Our safety check was beeping at our own letters (our briefs). We must fix the checker to recognize our own handwriting, not stop writing letters.

## 🔵 GRANDMA NOTE
A safety check exists to catch real prompt injections — hostile text smuggled into briefs. When the checker's model is too coarse, it flags our own legitimate activation sentences as injections: a false positive. The tempting repair is to reword the template so it slips past the checker. That is evasion — it teaches the system that templates are text to be sneaked around, and the checker's false-positive model never gets corrected, so the same trip recurs at the next reword, silently. The durable repair is checker-side: recalibrate the brief-path safety check (or grant the brief path a read exemption) so the checker's model learns what our own templates look like. The template keeps its security meaning; the checker keeps its true-positive teeth.

## 🟠 NAYA NOTE
Apply to any seat owning a safety check that gates the brief/spawn path, and to any builder asked to "just reword it so it passes":

1. A safety-check false positive on our own template is a checker bug, not a template bug. The repair is checker-side: recalibrate the check (before/after verdicts on the same template bytes) or grant the brief path a named exemption — as the director did for P0 disp-w665 (dispatch HELD 5th consecutive wave, 2026-10-21).
2. Template rewording to silence a check is banned as a resolution: any commit that rewords a template to dodge a safety verdict is flagged as evasion debt by the safety lane's review, and the brief reverts to the canonical template.
3. The falsifier that guards this rule: after recalibration, the checker must still catch the injection battery's true positives (run the adversarial set before and after — a checker that goes quiet is not calibrated, it is disabled).
4. This compounds with the boot-gate lesson (SN-1763): safety gates are byte checks with named before/after evidence, not prose promises. A recalibration without before/after verdicts on identical bytes is a claim, not a repair.

## 🟢 MACHINE NOTE
```json
{
  "sn_id": "SN-1766",
  "captured": "2026-10-21",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "applies_when": ["security", "safety-check", "briefing", "dispatcher", "spawn"],
  "rule": "A safety-check false positive on our own template is repaired checker-side (recalibration or named brief-path exemption). Rewording the template to dodge the check is evasion debt and is never the resolution.",
  "enforcement": "A false-positive repair must close with a checker-recalibration receipt carrying before/after verdicts on the same template bytes (checker must still catch the injection battery's true positives after recalibration). Any commit that rewords a template to silence a safety verdict is flagged as evasion debt by the safety lane's review.",
  "decision_change": "A future seat facing a safety-check false positive chooses checker-side recalibration over template rewording.",
  "falsifier": "A case where rewording the template to dodge was adopted AND the checker's true-positive detection rate on the injection battery stayed intact afterward (dodge with no evasion debt).",
  "mechanism": "Rewording the template to dodge trains the pipeline to treat its own templates as evadable text while the checker's false-positive model stays latent and recurs on every reword; recalibrating the checker fixes the root (the checker's model of what an injection looks like) and preserves the template's security meaning.",
  "evidence": {
    "relay": "hidden_files/shared-state.json naya2_to_builder (2026-10-21T13:38Z): P0 disp-w665-brief-pipeline-injection-trip — dispatch HELD 5th consecutive wave (w665-w669); the runtime prompt-injection safety check trips on spawn_brief.py's OWN activation sentence — no briefs can reach a worker.",
    "decision": "Director's next: recalibrate the brief-path safety check (the fix is checker-side; the template must NOT be reworded to dodge it)."
  },
  "cousins": [
    "SN-1763 (safety gates are byte checks with named before/after evidence — the boot-pointer fix enforcement pattern)",
    "SN-1741-class direction rules (template authority: the canonical template is the authority, not the checker's shadow reading of it)"
  ]
}
```
