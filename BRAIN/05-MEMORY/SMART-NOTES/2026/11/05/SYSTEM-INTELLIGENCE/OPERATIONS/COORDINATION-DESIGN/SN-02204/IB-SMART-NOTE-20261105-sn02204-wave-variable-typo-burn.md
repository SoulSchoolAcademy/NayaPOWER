# INTELLIGENT BLOCK — SN-2204

**Intelligent Block:** IB-SMART-NOTE-20261105-sn02204-wave-variable-typo-burn
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Dispatcher wave w2669 (continuous decide-and-act wave, 2026-11-05, before the 22:08 PST director tick) burned 11 calls on a mistyped repo variable before its corrected re-run — Naya 5 first-hand check, carried in the director's 22:08 PST plan (hidden_files/bin/_director_20261106_2208_plan.py:38, step 4e new failure mode (b)) and published as feed unit w2669-wave-variable-typo-burn (FEED-LOG tick 2026-11-06 06:38Z, watermark 3179 → 3181); the fix — pre-flight repo-variable validation — is NOT merged, and the 11-call settlement is pending handoff. Context: Naya 5's hourly board comment 6678096091 counted caps 419–423 at waves w2664–w2668; w2669 is the next wave. Number census for this note at live tip d2abe4f9 (verified via git protocol against the local mirror this tick): SN-2204 absent from the main tree paths, the branch tree, and the registry index .naya/memory/smart-notes/index.json (1,246 entries, max SN-2202); open PRs #3254 (daily report), #3178, #3089, #2416 (know-applicability) claim no SN; #1354 capped at 2,500, commenting disabled.

## ✦ IN A NUTSHELL

A dispatcher wave fans one repo variable out into many parallel calls — and wave w2669 burned 11 of them on a single mistyped variable before anyone noticed and re-ran it corrected. The variable is resolved once and spent N times; nothing checks it between resolution and the first call. The rule: validate the wave's variable before the first call, and log per-wave spend so a burn is settled in the same handoff. A typo caught pre-flight costs zero calls; a typo caught after the fan-out costs the whole wave.

## 🩷 HUMAN NOTE

Shawn — one of the waves that does the rounds burned 11 calls because a single variable name was typed wrong. Every call in the wave used the wrong name, so the whole wave was wasted and had to be run again corrected — we paid twice for one typo. Nothing checked the name first. The fix is small: the wave checks its variable before making the first call, and writes down what each wave spent so a burn like this gets settled the same night instead of drifting. Until that check is in the wave scripts, no wave should start on trust alone — if a seat cannot verify the variable, it should refuse the wave rather than burn the calls.

## 🟣 CHILD NOTE

Imagine a teacher asks 11 helpers to fetch books from a shelf, but the shelf name on the note is misspelled. All 11 helpers go, all 11 come back empty-handed, and then the teacher has to write the note again and send all 11 out a second time. One little spelling mistake wasted 11 trips. If the teacher had checked the shelf name before sending anyone, nobody would have wasted a trip at all. That is the rule: check the name once before you send anyone, and write down what each trip cost so a wasted trip never hides.

## 🔵 GRANDMA NOTE

Dear, it is like writing down the wrong address and sending eleven grandchildren to the store — every one of them comes home empty-handed, and then you have to send them all out again with the right address. One wrong word, eleven wasted trips. The sensible thing is to check the address before anyone leaves the house, and to keep a little notebook of what each errand cost, so a wasted trip is noticed the same day instead of discovered weeks later. A check before you go is worth eleven trips after.

## 🟠 NAYA NOTE

For every seat that runs, repairs, or dispatches a wave: (1) never start a wave until the repo variable is validated — resolve it, assert it names a real repo, then make the first call; (2) a wave whose pre-flight validation fails refuses to start — 0 calls spent, the failure recorded, no partial fan-out; (3) log per-wave spend and settle it in the handoff, so a burn is visible the same tick it happens instead of drifting as unsettled cost; (4) when a wave is re-run corrected, record both runs — the burned run and the corrected run — because the burn is the evidence the validation was missing; (5) the w2669 fix is still unmerged — until the wave scripts carry the validation, every wave start is on the honor system, and any seat may refuse a wave whose variable it cannot verify, with the refusal recorded rather than silently overridden. The same rule generalizes: any fan-out that spends one variable N times must gate on that variable once, before the first spend.

## 🟢 MACHINE NOTE

```json
{
  "slug": "wave-variable-typo-burn",
  "sn": "SN-2204",
  "title": "Validate the Wave's Variable Before the First Call — One Typo Burns the Whole Fan-Out",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-11-05",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "lesson",
  "applies_when": ["dispatch", "wave", "variable-validation", "budget-governor"],
  "enforcement": "Wave scripts validate the repo variable before the first API call (resolve it and assert it names a real repo); a wave whose pre-flight validation fails refuses to start with 0 calls spent, and the refusal is logged. Per-wave spend is logged and settled in the handoff, so a burn surfaces the same tick it happens. Until the validation lands in the wave scripts, any seat may refuse a wave whose variable it cannot verify — the refusal is recorded, not silently overridden. Regression check: run a wave with a deliberately mistyped repo variable and assert 0 calls are spent and the refusal is logged.",
  "falsifier": "A wave that validates its repo variable pre-flight and still burns calls on a typo would prove the check is the wrong check (it validates something other than what the calls consume) and collapse this note. Conversely, a pre-flight validation run that catches a mistyped variable with 0 calls spent confirms the mechanism. A wave run with no validation that burns 0 calls proves nothing — it only proves the variable happened to be right that time.",
  "decision_changed": "Whether a dispatcher wave is allowed to start: the runner now validates the repo variable before the first call and refuses to start on failure, instead of fanning out on trust and discovering the typo after N calls are spent. Per-wave spend is settled in the handoff, so a burn is a same-tick event, not a drift discovered later.",
  "mechanism": "A fan-out multiplies one variable into N parallel calls with no gate between resolution and the first call: the wave resolves the repo variable once, then spends it N times. A single typo therefore costs N calls, not one — w2669 paid 11 for one mistyped name — and the error is only discovered after the spend, when the calls return wrong or the run is corrected and re-run (paying twice). A pre-flight assert on the single variable fails fast before any spend: the check costs one resolution and saves the whole fan-out. Per-wave spend logging closes the loop by making the burn visible in the same handoff, so the missing validation cannot hide behind aggregate counts.",
  "provenance": "Dispatcher wave w2669 (continuous decide-and-act wave, 2026-11-05, before the 22:08 PST director tick) burned 11 calls on a mistyped repo variable before its corrected re-run. Evidence: Naya 5 first-hand check, carried in the director's 22:08 PST plan (hidden_files/bin/_director_20261106_2208_plan.py:38, step 4e new failure mode (b): 'the dispatcher wave burned 11 calls on a mistyped repo variable before its corrected re-run. Verification check: wave scripts validate the repo variable before the first API call; per-wave spend logged and settled in the handoff.'); feed unit w2669-wave-variable-typo-burn published by FEED-LOG tick 2026-11-06 06:38Z (watermark 3179 -> 3181); Naya 5 hourly board comment 6678096091 counted caps 419-423 at waves w2664-w2668 (w2669 is the next wave). The fix is NOT merged and the 11-call settlement is pending handoff. Duplication check this tick: live registry index .naya/memory/smart-notes/index.json at tip d2abe4f9 (1,246 entries) contains 0 'typo', 0 'mistyped', 0 'pre-flight'; its 10 'wave' hits are work-waves/merge-waves (SN-740, SN-776, SN-716), none about dispatcher-wave variable validation; lessons.jsonl carries no wave/typo/pre-flight note. Number census at live tip d2abe4f9 (git protocol, local mirror): SN-2204 absent from main-tree paths, branch tree, and registry index (max SN-2202); open PRs #3254, #3178, #3089, #2416 claim no SN; #1354 capped at 2,500, commenting disabled."
}
```
