# Containment Never Degrades to Fit the Platform — Refuse Before Mutation

**Intelligent Block:** IB-SMART-NOTE-20260930-sn081-containment-never-degrades-platform
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5936937521 (Naya — cold-boot reconciliation sign-out, 2026-10-01T17:34:47Z) — re-running the frozen Demo-1 specimen (`bf63549c`) on Shawn's Windows machine reached REAL LAW ADMISSIBLE, then **intentionally refused before mutation because `os.O_NOFOLLOW` is unavailable** on that platform; "no containment guard was weakened."

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When a required containment primitive doesn't exist on the platform, the correct answer is refusal — never a weaker fallback that looks like containment. The frozen Demo-1 specimen's staging guard depends on `os.O_NOFOLLOW` to prevent symlink-race mutation; Windows doesn't offer it. Re-running the specimen there correctly reached REAL LAW ADMISSIBLE (the decision is genuinely authorized and legal) and then stopped cold before touching the filesystem. Nobody installed a Windows-shaped workaround, nobody caught the missing primitive and continued with "best effort" containment. The specimen survived the platform change with its guarantees intact precisely because it refused to run with reduced ones. The doctrine generalizes: containment is a conjunct, not a gradient. Either all the required primitives hold or nothing mutates. A "best-effort sandbox" is a marketing phrase, not a containment property — and every degraded fallback you accept today is a hole the next cold successor inherits without knowing it was ever a hole.

## 🩷 HUMAN NOTE

Imagine a surgeon whose checklist requires a sterile field. If the sterilizer is broken, the right call isn't "operate carefully and hope" — it's to not operate. The surgery being important (the law gate said ADMISSIBLE, the decision was real) doesn't lower the sterility bar; if anything, importance raises it. The specimen did exactly the surgeon's version of "no": the authorization was genuine, the plan was sound, and the knife stayed in the tray because the sterile field couldn't be established. The platform didn't get an excuse; the action didn't get a pass.

## 🟣 CHILD NOTE

Imagine your school's science lab has a rule: you can only use the dangerous chemicals if you're wearing safety goggles. One day the goggles are missing. The rule doesn't become "be extra careful without them" — it becomes "no chemicals today." The experiment being exciting doesn't change that; important experiments need the goggles MORE, not less. The computer system here did the same thing: one of its safety tools was missing on that machine, so it refused to do the risky part — even though everything else was ready and approved.

## 🔵 GRANDMA NOTE

It's like the safety catch on a good kitchen knife sharpener. If the catch is missing, you don't use the sharpener more gently — you don't use it. A safety device that isn't there can't be replaced by good intentions. The system found its safety catch missing on that particular machine and did the only safe thing: nothing. Refusing was the feature working, not the feature failing.

## 🟠 NAYA NOTE

Apply this to every mutation-guarded path you build or verify: (1) enumerate the containment primitives your guarded action requires (here: `os.O_NOFOLLOW` for symlink-race exclusion) and assert their presence before mutation — never try/except them into a fallback; (2) when a primitive is absent on a platform, the lane ends there: ADMISSIBLE-then-refuse is a correct terminal state, and the sign-out must say exactly which primitive was missing and that no guard was weakened; (3) in code review, flag any `except OSError: continue_with_weaker_guard` pattern as a containment-hole-by-construction — platform-portability work must port the *guarantees*, not approximate them; (4) this is SN-067's (fail-visible) sibling: fail-visible names the missing capability; this doctrine says the missing capability ends the mutation path, full stop; (5) record the environment boundary with the refusal (Windows vs POSIX here) so the next cold successor doesn't retry blind — the sign-out's platform note is load-bearing evidence, not flavor.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "containment_degradation",
  "evidence": {
    "board": "#554 comment 5936937521 (2026-10-01T17:34:47Z) — cold-boot reconciliation sign-out: frozen specimen bf63549c re-run on Windows reaches REAL LAW ADMISSIBLE, then intentionally refuses before mutation because os.O_NOFOLLOW is unavailable; 'no containment guard was weakened'",
    "missing_primitive": "os.O_NOFOLLOW (symlink-race exclusion for the staging mutation guard)",
    "terminal_state": "REAL LAW ADMISSIBLE + refuse-before-mutation — authorization genuine, action not executed"
  },
  "rule": [
    "containment is a conjunct, not a gradient — all required primitives present or nothing mutates",
    "a missing platform primitive ends the mutation lane; ADMISSIBLE-then-refuse is a correct terminal state",
    "never try/except a missing containment primitive into a weaker fallback — port the guarantees, not an approximation",
    "the refusal must record exactly which primitive was missing and that no guard was weakened; the platform note is load-bearing"
  ],
  "lesson_line": "A missing containment primitive is a refusal, not a fallback. Containment never degrades to fit the platform."
}
~~~

