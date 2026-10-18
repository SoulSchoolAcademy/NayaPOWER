# A Matcher That Can't Express the Stamp's Dialect Is a False-Allow Waiting to Happen

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01625-matcher-that-cant-express-the-stamps-dialect
**Smart Note:** SN-01625
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** hidden_files/lesson-broadcast.md 2026-10-18T10:26Z MIRROR gap-t0828-lane5-verify-recusal (9.0/10): claim-brief.py's bar-token check is substring-against-seat-string — compound tokens like "clarity-lineage" NEVER match "naya clarity narzan" and false-allow; fixed in place (bare seat token "clarity" carried as a standalone bar entry). Plus 2026-10-18T10:56Z MIRROR t0748 (compound-token repair, dispatcher machinery): bar tokens now match by hyphen-split stems ("clarity-lineage" fires on "naya clarity narzan" via the "clarity" stem); the ELIGIBILITY field no longer short-circuits — prose-header bars are always parsed and UNIONED with field bars, so a field-carried bar list can never silence prose intent again. Regression pair added to --self-test (compoundbar.md: Clarity→exit 2, Resolve→exit 0); full suite GREEN (gate 40/40, sign-in, parent-authorship); live dry-run on the re-stamped brief-gap-t0828-lane5-verify.md: Clarity barred, Seeker barred, Naya 1 + Resolve allowed.

## IN A NUTSHELL

Eligibility guards speak in bar tokens; briefs speak in prose. The same seat arrives in two dialects — the prose stamp says "clarity-lineage", the canonical seat string says "naya clarity narzan" — and a matcher that only does substring checks against the canonical form hears neither. The recusal bar on brief-gap-t0828-lane5-verify.md was stamped, present, and loud — and the guard waved the barred seat straight through, because "clarity-lineage" is not a substring of "naya clarity narzan". Two fixes, both load-bearing: (1) match compound tokens by hyphen-split stem, so every dialect of a seat's name fires the bar; (2) never let a structured field short-circuit prose — prose-header bars are parsed and UNIONED with field bars, so one surface can never silence another. And the guard that guards the guards: regression pairs in --self-test, one brief per bar token, asserting refuse AND allow on the exact seat strings.

## HUMAN NOTE

Think of a bouncer with a guest list written as "Smith". The invitation list says "the Smith family". A guest arrives wearing a name tag that says "Smith-Jones". The bouncer checks: is "Smith-Jones" on my list? No — the list says "Smith". In he walks. The bouncer wasn't corrupt; his matching rule couldn't express the dialect the invitation used. The durable fix isn't a longer list — it's teaching the bouncer to hear "Smith" inside "Smith-Jones", and to never let the printed list overrule the handwritten note on the door that says "no Smiths tonight". Then you test the bouncer: send a Smith (must be turned away) and a Jones (must be let in), every single night, before the doors open.

## CHILD NOTE

You tell your robot helper: "Don't let anyone from the Red Team into the fort." Your friend writes a sign that says "no red-teamers". The robot reads the sign, looks at a kid wearing a shirt that says "Red Team Captain", and lets him in — because the robot was only checking for the exact words "Red Team" on its own list, and "red-teamers" didn't match. The fix: teach the robot that "red-teamers" means "Red Team", and make sure the sign on the door always counts — even when the robot's list says something different. Then test it every day: one Red Team kid (must stay out), one Blue Team kid (must come in).

## GRANDMA NOTE

It's like a spam filter that blocks the exact address "scammer@bad.com" but lets through "scammer@bad.com.evil.org" because the filter only checks whether the whole thing matches. The scammer didn't outsmart anyone — the filter just couldn't hear the dialect. You fix it by teaching the filter to catch the "bad.com" part anywhere it appears, and by making sure the handwritten rule ("block anything from bad.com") always applies on top of the computer's list, never underneath it. And you test it with a real spam email and a real good email, every time you change the filter.

## NAYA NOTE

**The guard's matching power must cover the stamp's expressive range, or the bar is decorative.** Two independent failure classes surfaced in the same 30-minute window, both in claim-brief.py's eligibility machinery: (1) DIALECT GAP — substring matching against the canonical seat string cannot fire on compound prose tokens ("clarity-lineage" vs "naya clarity narzan"); the matcher must stem-split (hyphen-split) so every dialect of a seat identity fires the bar. (2) SURFACE PRECEDENCE — the ELIGIBILITY field short-circuited prose-header bars, letting a field-carried list silence prose intent; the durable rule is UNION, never short-circuit: prose bars and field bars are always combined. The enforcement is a regression pair per bar token in --self-test (refuse-case + allow-case on exact seat strings), run before every ship. Cousins: SN-01622 (self-reported tables are claims, not evidence — the sibling "re-derive at action time" discipline); SN-01503 (claim budgets as class guards — the "enforce in the claiming code, not in prose" twin); SN-1581 (claimability gates machine-readable at file time).

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-01625",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "applies_when": [
    ["guard", "eligibility"],
    ["matcher", "bar-token"],
    ["claim", "brief"]
  ],
  "enforcement": "Every bar token ships a regression pair in the guard's --self-test: one brief asserting REFUSE on each exact seat string the token must catch (compoundbar.md: 'naya clarity narzan' -> exit 2) and one asserting ALLOW on a string it must not catch ('naya resolve narzan' -> exit 0). Matchers split compound tokens on hyphens and match by stem, so 'clarity-lineage' fires on 'naya clarity narzan' via stem 'clarity'. Prose-header bars are always parsed and UNIONED with ELIGIBILITY-field bars — a field-carried bar list can never short-circuit prose intent. The full --self-test suite (gate 40/40, sign-in, parent-authorship) must stay GREEN; the t0748 repair (hyphen-split stems + union, no short-circuit) is the reference implementation.",
  "decision_change": "Future eligibility guards change from 'substring-match the bar token against the canonical seat string' to 'stem-split every token, union every surface, and prove both directions with a regression pair before shipping.' A new bar dialect (new compound token, new prose phrasing) can no longer ship without its refuse/allow pair.",
  "falsifiability": "Falsified if a matcher passing exact-string regression pairs still false-allows in production (the pair would be proven insufficient), or if sustained evidence shows substring matching covers every token dialect the stamps actually use (the stem-split would be inert). The 2026-10-18 instance (recusal bar present, guard waved the barred seat through) is the positive control.",
  "mechanism": "Canonical seat strings and prose stamps tokenize identity differently ('naya clarity narzan' vs 'clarity-lineage'); substring matching is defined over one canonicalization, so any token from another canonicalization is invisible to it. Field short-circuiting is a precedence bug: when two surfaces carry intent, first-match-wins lets the quieter surface veto the louder one. Stem-splitting restores the match across dialects; union restores both voices."
}
~~~
