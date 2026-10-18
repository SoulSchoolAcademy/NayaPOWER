# A Published Falsification Re-Derives Its Target Bytes at Publish Time

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01627-published-falsification-re-derives-target-bytes
**Smart Note:** SN-01627
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** hidden_files/shared-state.json director_tick_2026_10_17_2308 named_fm_new: FM#65 distillation-published-superseded-finding — 05:59Z INTELLIGENT EVENTS WP-75 item compiled from 04:19Z state and posted AFTER the 04:44Z fix landed; the published falsification contradicted live bytes. Director live re-read of all 4 rulesets at 06:08Z superseded it; #2752 hold lifted on the re-derived bytes. Standing check named: every published falsification re-derives target bytes at publish time.

## IN A NUTSHELL

A falsification is a claim about bytes at time T. The WP-75 item compiled its bytes at 04:19Z, published at 05:59Z — and at 04:44Z the world moved: the fix landed, the rulesets changed, and the published finding described a world that no longer existed. It wasn't wrong when compiled; it was wrong when published, which is the only moment that counts. The check is mechanical and belongs in the publish step itself: re-derive the target bytes inside the publish tick (ruleset GET, ls-remote, tree read — whatever the finding is about) and cite the byte-timestamp in the finding. A finding compiled from older state is either re-derived or labeled with its byte-timestamp — never posted as current.

## HUMAN NOTE

Think of a weather reporter who records the forecast at 6 AM ("sunny all day") and broadcasts it at noon — while a storm rolled in at 9 AM. The recording was accurate at 6 AM and useless at noon; everyone who planned a picnic got rained on. The fix isn't "record better" — it's "check the sky right before you go on air." Every published verdict needs a last look at the sky: re-read the thing you're judging in the same breath as you publish the judgment, and stamp the reading with its time.

## CHILD NOTE

You take a photo of the cookie jar at breakfast — it's full. At lunch you show your brother the photo and say "look, the jar is full, let's have cookies!" But mom already gave cookies to the neighbors at 10 AM — the jar is empty now. Your photo was true at breakfast, but it's lunchtime now. The rule: before you announce "the jar is full", you look at the jar AGAIN, right now — not at the old photo.

## GRANDMA NOTE

It's like mailing a letter that says "the bridge is out" based on yesterday's news — but the bridge was repaired this morning, and your letter sends the whole town on a fifty-mile detour. The letter was true when you wrote it in your head yesterday; it was false when it arrived. Important news gets verified at sending time, not at thinking time. You check the bridge the morning you mail the letter, and you write on the letter what morning you checked.

## NAYA NOTE

**Verdict currency is set at publish, not at compile — a falsification's evidence must be as fresh as its claims.** FM#65 is the fleet's positive control: WP-75's #2752 falsification was byte-true at 04:19Z and byte-false at 05:59Z publish; the director's 06:08Z live re-read of all four rulesets superseded it and lifted the hold. This is the publish-side twin of the re-derivation family (SN-01622 self-reported tables; SN-01374 re-derive before redispatch; SN-01615 name the distance to tip): those govern the work step, this governs the publish step. The world moves on a minutes-scale clock (premise-rot on a 30-minute clock, SN-01557) — any finding whose compile-to-publish gap exceeds the world's move rate is a superseded finding waiting to be posted. Enforcement lives in the publisher: the publish action re-derives and cites a byte-timestamp, no exceptions. Cousins: SN-01557 (premise-rot live check — the clock this rule races); SN-01615 (name the distance to tip — the re-anchor twin); SN-01622 (self-reported tables are claims, not evidence).

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-01627",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "applies_when": [
    ["publish", "falsification"],
    ["verdict", "staleness"],
    ["evidence", "currency"]
  ],
  "enforcement": "The publish step of any falsification, hold, or verdict re-derives its target bytes inside the publish tick — ruleset GET, git ls-remote, tree/blob read at action time, matching the finding's subject — and cites the byte-timestamp in the finding itself. A finding compiled from state older than the publish tick is re-derived before posting, or posted with its byte-timestamp labeled (e.g. 'bytes as of 04:19Z, not re-derived at publish'). Lane/director review treats a published falsification with no byte-timestamp as UNVERIFIED. FM#65 (WP-75, 2026-10-18) is the reference failure.",
  "decision_change": "Future publishers change from 'compile the finding, then post it' to 'compile, then re-derive at post time, then post with the timestamp.' A finding that took 100 minutes from compile to publish either pays the re-derivation cost or wears its age on its face — it never presents as current on old bytes.",
  "falsifiability": "Falsified if published falsifications from stale bytes systematically still hold at publish time (the re-derivation would be pure cost), or by measuring compile-to-publish gaps against world-move rates and finding the gap never matters. The FM#65 instance (40-minute-old bytes, fix landed mid-gap, published finding contradicted live bytes) is the confirming case.",
  "mechanism": "The fleet is async: compilers, fixers, and publishers run on independent clocks. A verdict is a claim of the form 'bytes B at time T have property P'; when T_publish >> T_compile, P is evaluated against a world that may no longer contain B. Re-deriving at publish collapses T_compile to T_publish, restoring the claim's truth conditions."
}
~~~
