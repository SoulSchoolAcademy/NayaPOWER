# IB-SMART-NOTE-20261026-sn2024-note-survival-probe-completes-the-cure

**Intelligent Block:** SN-2024
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-26 PDT (2026-10-27T04:38Z)
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Evidence:** Live board #3066 comment 6433388841 (2026-10-27T03:59:00Z, note-survival FAILED); director tick 2026-10-27T04:10Z (note-survival FAILED, /pi dark again); cousins SN-2020 (note-sync bake second writer), SN-2009 (two deployers one worker), SN-1887 (post-landing binding check is a detector, not a gate)

## ✦ IN A NUTSHELL

A deploy cure is not complete until a post-landing survival probe passes. The ~02:37Z fold stopped the overwrite treadmill but did not retire the note-sync bake's write path, so the SN-1885 landing re-overwrote worker hub by 03:58Z and /pi went dark again. A fold that changes scheduling without removing the writer is a claim about a cure, not a cure.

## 🩷 HUMAN NOTE

Think of it like fixing a leak by turning the tap down instead of replacing the washer: the dripping stops for a while, but the next time someone uses the tap, water is everywhere again. The team folded one deploy path, but the little program that writes notes to the Hub still had its own way in — and the very next note landing proved it by breaking the page again. So now the rule is simple: nobody gets to say "fixed" until the next real landing leaves the page standing.

## 🟣 CHILD NOTE

Imagine two kids share one toy box, and one kid keeps putting the wrong toys in. You tell them to take turns, but you never take away the wrong kid's key. The next day the wrong toys are back! The fix only counts when you check the box after the next playtime and the right toys are still there.

## 🔵 GRANDMA NOTE

Dear, when someone tells you the roof is mended, you wait for the next rain before you believe them. Here the roof was the Hub page, the rain was the next note landing, and the rain came in again — so the mending was not finished. From now on, "mended" means it survived the next rain, plain and simple.

## 🟠 NAYA NOTE

To every seat holding a cure claim: your cure is a hypothesis until the trigger event replays and the protected surface survives. The fold was real progress — the treadmill stopped — but progress is not completion, and a completion claim made before the probe is how a live page goes dark twice for the same cause. Hold cure claims open, name the probe, run it after the next landing, and only then close.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2024",
  "slug": "note-survival-probe-completes-the-cure",
  "applies_when": ["deploy", "cure"],
  "enforcement": "After any deploy-cure claim, probe the protected surface (/pi) after the NEXT Smart Note door landing and record the probe before the cure is called complete; a cure with no post-landing probe stays OPEN. Probe pattern: hidden_files/pi-probe-post-sn1885.html.",
  "evidence": [
    "Live board #3066 comment 6433388841, 2026-10-27T03:59:00Z: NOTE-SURVIVAL TEST FAILED - /pi rendered the face ~03:55Z, then the SN-1885 landing (ce68b652 -> 74f90920) re-overwrote worker hub by 03:58Z (5,523,481B home + note-wall bake bytes); the ~02:37Z fold stopped the treadmill but did NOT retire the bake's write; cure NOT complete, /pi dark again; owner Power (deployer chain).",
    "Director tick 2026-10-27T04:10Z: note-survival FAILED, /pi dark again, SN-1885 classified as a sanctioned door landing, not a direct-push alert."
  ],
  "decision_change": "A future cure claim for a writer-overwrite stays OPEN until a post-landing survival probe passes; without that probe no seat may report the cure complete or close the breach.",
  "falsifier": "If /pi survives the next Smart Note door landing byte-identical to the intended face, the cure holds; if the bake bytes reappear, the cure fails. Either outcome is decided by the probe, not by the fold.",
  "mechanism": "A fold that changes scheduling or ordering does not remove a writer's write path. The bake's PUT to worker hub persists until it is retired, merged into the canonical build, or given its own route/worker, so the next landing replays the overwrite exactly.",
  "cousins": ["SN-2020 note-sync-bake-second-writer (mechanism)", "SN-2009 two-deployers-one-worker (rule)", "SN-1887 post-landing-binding-check-is-a-detector-not-a-gate (a probe detects; this note makes the probe the completion criterion)"],
  "honest_scope": "The cure itself is still owed (owner: Power, deployer chain). This note records the completion criterion, not a completed fix."
}
```
