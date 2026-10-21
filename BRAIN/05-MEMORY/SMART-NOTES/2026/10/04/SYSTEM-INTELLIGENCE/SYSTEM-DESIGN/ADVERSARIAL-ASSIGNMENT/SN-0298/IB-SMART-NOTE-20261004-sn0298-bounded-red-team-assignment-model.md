# Intelligent Block: SN-0298

**Intelligent Block:** SN-0298 — The Bounded Red Team Assignment Model
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Bounded adversarial work catches real defects when the job is bounded, read-only, and contract-crisp. On 2026-10-04, Red Team Naya got its first assignment: one bounded job — attack the merged Hub, read-only, on main tip c507a32a. It attacked 8 surfaces and returned 1 severe + 3 degraded, every finding with exact line numbers and reproductions: SEVERE — rapid block switching, where block X's stale rejection killed block Y's in-flight audio plus a double toast (would have broken real playback the day audio ships; one-line guard fix); DEGRADED — `read()` accepted `JSON.parse("null")` → null, so every board rendered with zero action buttons (shape check added); DEGRADED — audio-key contract fragile (re-slug diverged from factory keys; key is now the boardId verbatim); DEGRADED — mobile 390px overflow (4 compact buttons need ~400px+, the viewport offers ~350px, `.shell` clips overflow-x so tail buttons are unreachable). Fixes landed as PR #1423 (branch `naya2/hub-naya-play-hardening-v1`, commit `60aac35c` then `9c17f89c`, byte-verified, base = live tip `2135fd0f`). Three rules made it work. (1) RECORD, DON'T ACT, ON THE UNVERIFIED: three suspicions — toast XSS via runtime messages with no user-input path, same-title id collision by design, addIntel write-only — were recorded as known and deliberately not touched. (2) WHEN THE ENVIRONMENT CAN'T REPRODUCE, CHANGE THE PROOF VENUE: the live browser couldn't reproduce sub-404ms click timing, so the stale-audio guard was proven deterministically — the exact `NayaVoice` IIFE extracted from shipped bytes, driven through the hostile interleaving in Node (click X, click Y before X rejects, fail X, fail Y): exactly 1 toast, X's stale rejection silent, Y's live audio untouched. The browser's 2-toast observation was correct independent-failure behavior, not the bug. (3) PROVABLY-SAFE REPAIRS: the mobile fix was `flex-wrap: wrap` in the 640px query — a no-op whenever the row fits (verified fitting at 630px), a fix when it doesn't; zero desktop change. Verdict on the experiment: "the specialist model works. One bounded job, crisp contract, verified findings, real defects caught before they bit. Expanding the roster gradually from here per the director's scaling law."

## HUMAN NOTE

Shawn — here's the short version. You asked for a red team — someone whose whole job is to try to break things before your customers do. The first assignment just came back, and it earned its keep: one severe bug that would have broken audio playback the day it ships, plus three smaller ones, all fixed and verified. What made it work: the job was tightly bounded (read-only, one clear target, exact line numbers on everything it found), it didn't touch anything it couldn't prove (three suspicious things got written down as "known, not proven" and left alone — no guessing), and when the testing tools couldn't reproduce the timing, it pulled the real code out and proved the fix in a clean-room test instead. The verdict from the team: the specialist model works — one small team, one sharp job, real defects caught early. They're expanding it slowly from here, per your scaling law.

## CHILD NOTE

Imagine hiring a professional "try to break it" person for your treehouse. You give them ONE clear job: "try to break the treehouse, but you're not allowed to change anything, and you have to point at exactly where you broke it." They found four real weak spots — including one that would have broken the slide! For the things they only SUSPECTED were weak but couldn't prove, they wrote them down and didn't touch them. And when the timing was too fast to test by hand, they built a tiny robot world with the exact same parts and proved it there. Rule: be specific, be honest about what you proved, and never "fix" what you only suspect.

## GRANDMA NOTE

They've set up a proper inspection crew, dear — like a home inspector before you buy a house. One inspector, one house, one checklist, and they point at the exact crack. They found a cracked beam that would have mattered someday, and three smaller things, and fixed them all. The things they weren't sure about, they just wrote down and left alone — no tearing up floorboards on a hunch. And when something happened too fast to see, they rebuilt the exact mechanism on a workbench and tested it there. Sensible, honest work. That's how you keep a house standing.

## NAYA NOTE

From the board (#1354, comment 5985730495): "The 3 unverified suspicions ... are recorded as known, not acted on." That sentence is the load-bearing discipline of this whole note. An adversarial lane that "fixes" what it only suspects is worse than no red team at all — it manufactures churn and erodes trust in the repair record. The contract for future bounded assignments: pin the tip, stay read-only, report findings with exact line numbers and reproductions, separate VERIFIED findings from RECORDED suspicions in the report, choose provably-safe repairs, and prove fixes at the logic level on extracted shipped bytes when the live environment can't reproduce. Cold successors running a red team: hand them one bounded job and a crisp contract, not a blank check. Scale the roster gradually — specialists, not a crowd.

## MACHINE NOTE

```json
{
  "sn": "SN-0298",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-04",
  "lesson": "Bounded adversarial assignments (one job, read-only, pinned tip, crisp contract) catch real pre-ship defects; unverified suspicions are recorded as known and never acted on; when the environment cannot reproduce, prove deterministically on extracted shipped bytes; prefer provably-safe repairs.",
  "evidence": {
    "board": "#1354",
    "assignment_comment": "5985730495 (Red Team Naya first assignment: 8 surfaces attacked on main tip c507a32a; 1 severe + 3 degraded with exact line numbers and reproductions; 3 unverified suspicions recorded as known, not acted on)",
    "verification_comment": "5985823855 (stale-audio guard proven deterministically in Node on the exact NayaVoice IIFE from shipped bytes; mobile 390px closed analytically with provably-safe flex-wrap fix)",
    "repair_pr": "#1423 (branch naya2/hub-naya-play-hardening-v1, commits 60aac35c and 9c17f89c, byte-verified, base = live tip 2135fd0f)"
  },
  "findings": {
    "severe": "rapid block switching — stale rejection of block X killed block Y's in-flight audio + double toast (one-line guard fix)",
    "degraded": ["read() accepted JSON.parse('null') -> zero action buttons (shape check)", "audio-key contract fragile (key = boardId verbatim)", "mobile 390px overflow (flex-wrap: wrap in 640px query)"]
  },
  "recorded_not_acted_on": ["toast XSS via runtime messages with no user-input path", "same-title id collision by design", "addIntel write-only"],
  "rules": ["RECORD, DON'T ACT, ON THE UNVERIFIED", "WHEN THE ENVIRONMENT CAN'T REPRODUCE, CHANGE THE PROOF VENUE", "PROVABLY-SAFE REPAIRS: no-op when the case doesn't apply, fix when it does"],
  "verdict": "the specialist model works; expand the roster gradually per the director's scaling law",
  "failure_mode_prevented": "speculative fixes from unverified adversarial suspicions; unproven repair claims from irreproducible environments"
}
```
