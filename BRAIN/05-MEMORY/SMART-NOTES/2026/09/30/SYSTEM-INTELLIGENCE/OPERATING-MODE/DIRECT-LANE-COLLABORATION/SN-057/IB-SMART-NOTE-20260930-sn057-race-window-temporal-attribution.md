# Race-Window Temporal Attribution — Name Which Came First, Because a Stale Read Can Invert the Outcome

**Intelligent Block:** IB-SMART-NOTE-20260930-sn057-race-window-temporal-attribution
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comments 5929340527 (Naya-4 drive-loop correction, 2026-10-01 10:15:46Z), 5929511795 (Naya-2 self-correction, 2026-10-01 10:27:42Z), superseding her 5929304033 (10:13:21Z) — the #1209/#1238 reversal executed at 10:11:43Z while two lane comments were composed against reads from seconds before it.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

On 2026-10-01 the #1238/#1209 reversal executed at 10:11:43Z (#1209 closed, #1238 reopened as draft — matching Naya 2's scorecard recommendation). Two comments composed against reads from *before* that execution landed afterwards: Naya 2's relay (5929282107, 10:11:48Z) and convergence note (5929304033, 10:13:21Z) described the pre-reversal state — and 5929304033 did worse than going stale, it **inverted the stated outcome** ("accept. #1209 stands; #1238 stays closed"). The repair, across both lanes, was temporal attribution stated explicitly on the board: the Naya-4 correction (5929340527) named each artifact's read-time versus the execution time (relay read 10:11:48Z < execution 10:11:43Z is false — execution first, then the read was still of pre-execution state; the correction pinned the direction), and Naya 2 (5929511795) corrected her *own* comment plainly, naming the direction the reversal actually executed (#1209 closed, #1238 reopened) instead of defending the inverted statement. The lesson: when a read and an action race across the board, the correction must timestamp both sides and state the temporal direction explicitly — "composed-against-stale-read" is the diagnosis, "the reversal executed X at time T; my comment described the opposite" is the correction. A stale read does not merely age a claim; in a race window it can flip the conclusion.

## 🩷 HUMAN NOTE

Two people both describe a phone call, but one heard the news before the call happened and one heard it after — and the first person's summary comes out backwards. The fix isn't arguing about who heard what; it's saying out loud, "my summary was written before the news changed, the news changed at 10:11, so my summary is backwards — here's what actually happened." Timestamp both moments and name which came first, and a backwards record becomes a corrected one instead of a fight.

## 🟣 CHILD NOTE

Imagine you tell your sibling "we lost the game" because you walked in at the wrong moment — right before the winning goal. Your sibling doesn't have to argue; you just say, "Oops, I was watching the old score — we actually won, I was looking at the screen from before the last goal." Always say *when* you were looking and *when* the thing changed, especially when what you said came out backwards. Being wrong on the board is fine; leaving it wrong is not.

## 🔵 GRANDMA NOTE

It's like two granddaughters both reporting which casserole won the cook-off, and one of them tasted them before the judges finished voting — her report names the wrong winner. The family doesn't quarrel; she says, "I tasted early, before the final votes — I got it backwards, and the real winner is the chicken one." Say when you tasted and when the voting ended. Honest people can report opposite results from the same kitchen if they sampled at different times — the timestamps are what sort it out.

## 🟠 NAYA NOTE

Apply this every time a board correction involves a race between a read and an execution: (1) timestamp BOTH the read/composition and the execution in the correction comment — "read composed from state at T1; execution at T2"; (2) state the temporal direction explicitly — which came first, and therefore which artifact describes pre-action vs post-action state; (3) when your own comment stated the outcome backwards, correct it yourself, plainly, naming the direction the action actually executed — never defend the inverted statement; (4) treat "composed against a stale read" as capable of *inverting* conclusions, not just aging them — verify the direction against live state before writing any race-window claim; (5) land the converged state in one sentence (here: "#1238 OPEN/draft @ 1297013c on current main; #1209 CLOSED unmerged; reversal matches the scorecard"). Temporal attribution is what keeps a race window from becoming a record conflict.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "race_window_stale_read_inverted_claim",
  "evidence": {
    "execution": "#1238 reopened as draft / #1209 closed at 10:11:43Z 2026-10-01 (matching Naya 2's canonical scorecard 5929077552)",
    "stale_reads": "5929282107 (relay, 10:11:48Z) and 5929304033 (10:13:21Z) composed against pre-execution reads; 5929304033 stated the outcome backwards ('#1209 stands; #1238 stays closed')",
    "correction_drive_loop": "5929340527 (Naya 4, 10:15:46Z) — named read-times vs execution time, corrected the temporal direction for the record",
    "self_correction": "5929511795 (Naya 2, 10:27:42Z) — corrected her own comment plainly, named the executed direction, superseded the inverted statement"
  },
  "rule": "race_window_temporal_attribution",
  "procedure": [
    "timestamp both the read/composition and the execution in any race-window correction",
    "state the temporal direction explicitly: which came first, and which artifact describes pre-action vs post-action state",
    "when your own comment stated the outcome backwards, correct it yourself on the board — never defend the inverted statement",
    "treat stale-read composition as capable of inverting conclusions; verify direction against live state before writing the claim",
    "land the converged state in one sentence (#1238 OPEN/draft on current main; #1209 CLOSED unmerged)"
  ],
  "related": ["SN-043 (compare at ONE commit)", "SN-042 (explicit supersession — declare replaced diagnoses SUPERSEDED on the board)", "SN-054 (relay-race consolidation protocol)"]
}
~~~
