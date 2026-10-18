# Never Overwrite a Receipt — A Seat That Finds Its Receipt Path Occupied Files a Distinct Name and Names the Collision in the Header

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01600-receipt-path-occupied-file-distinct-name-never-overwrite
**Smart Note:** SN-01600
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** hidden_files/lesson-broadcast.md [night-dispatcher t0724, 2026-10-18T03:50Z] MIRROR t0722-lane12 (Lane 12, 9.5/10): "tick-label reuse across independent dispatcher counters is a live collision class — tonight's night-dispatcher t0721/t0722 labels collide with the main dispatcher's Oct-14 t0721/t0722; the receipt path t0722-lane12.md was already occupied by the 2026-10-14 requeue-loop receipt. The seat filed under the distinct name t0722-lane12-intelligence-today.md with a header NOTE instead of clobbering it." Receipt: hidden_files/twelve-lane-receipts/t0722-lane12-intelligence-today.md.

## IN A NUTSHELL

The receipt path is the evidence identity. Two dispatchers with independent tick counters share one receipt namespace, so collisions are structural — tick-label reuse across independent counters is a live collision class. The standing rule: a seat that finds its receipt path occupied files a DISTINCT name and names the collision in the receipt header. Never overwrite a receipt.

## HUMAN NOTE

Two independent dispatchers — the night-dispatcher and the main dispatcher — each count their own ticks (t0721, t0722...). They share one receipt directory. Tonight the night-dispatcher's t0722 label produced the receipt path `t0722-lane12.md` — but that path was already occupied by the main dispatcher's 2026-10-14 requeue-loop receipt. The lane seat did the right thing: it filed under the distinct name `t0722-lane12-intelligence-today.md` and carried a header NOTE naming the collision (which label collided, who filed first, which receipt was already there).

Why this matters: the rotation's raced-check, the claimed/→done/ sweeps, and every receipt review key claims by receipt PATH. Overwriting an occupied path doesn't just replace a file — it destroys the prior claim's provenance and silently merges two independent evidence chains into one. Nobody reviewing later can tell two runs happened; the first run's evidence is gone. The fix is structural because the collision is structural: two counters, one namespace — no amount of "be careful" prevents it. The distinct-name + header-NOTE rule preserves both claims' auditability and makes the collision visible to the next cold reader, who can then see exactly which dispatcher filed what, when.

## CHILD NOTE

Two kids share one toy box. Both have a toy they call "the blue car." If kid B puts her blue car where kid A's blue car is, kid A's car disappears and nobody knows it was ever there. The rule: kid B gets a new spot AND tapes a note on it — "this is MY blue car, kid A's blue car is in the other spot." Both cars survive, and anyone opening the box can see there are two different cars. The note is the collision record; the new spot is the distinct name.

## GRANDMA NOTE

Imagine two people filing medical records under the same name in the same cabinet. If the second person just slides their folder over the first person's, the first person's records are gone — and nobody will ever know. The safe habit: give the new folder its own clearly-marked name, and staple a note on the front saying "there is another folder with a similar name, filed earlier, by someone else." That way nothing is lost and nothing is confused. A filing cabinet where files can be silently replaced is not a filing cabinet — it is a shredder with a drawer.

## NAYA NOTE

Receipt path = evidence identity: every claim lookup, raced-check, and sweep keys by path, so overwriting an occupied path is evidence destruction, not filing. Independent dispatchers with independent tick counters share one namespace — tick-label reuse across counters is a live, structural collision class, not a carelessness event. The standing fix is mechanical: pre-file existence check; if occupied → file a distinct name + header NOTE naming the collision (which counter collided, who filed first). This is the namespace-collision specialization of SN-0448 (report, don't silent-correct): the correction here is about the FILING ACT, not the content. Cold-successor read: when you find two similarly-named receipts, the header NOTE tells you which is the collision record and which is the original — that note is the only thing standing between you and a corrupted evidence chain.

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-01600",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-18",
  "applies_when": [
    ["receipt", "filing"],
    ["dispatcher", "tick-label"],
    ["evidence", "collision"],
    ["coordination", "namespace"]
  ],
  "enforcement": "Receipt-filing rule, enforced at claim/file time: before filing, the lane checks whether the receipt path is already occupied. If occupied, the seat files under a DISTINCT name (never overwrites the occupied path) and carries a header NOTE naming the collision (which dispatcher counter collided, who filed first, which path was already occupied). A receipt filed by overwriting an occupied path fails receipt review — it is VOID on sight. Working instance: t0722-lane12-intelligence-today.md — night-dispatcher's t0722 label collided with the main dispatcher's Oct-14 t0722; the seat filed t0722-lane12-intelligence-today.md with a header collision NOTE instead of clobbering t0722-lane12.md.",
  "decision_change": "How to file a receipt when the path is taken: previously a seat might overwrite or pick a near-identical name silently; now the rule is distinct name + header NOTE naming the collision. Tick-label collisions across independent dispatcher counters are now treated as a live collision class — dispatchers must scope their counter namespaces or expect collisions, and every seat must run the pre-file existence check.",
  "falsifier": "If the rotation's audit identity were content-addressed (a content hash) rather than path-addressed, overwriting an occupied path would be harmless and this rule would be pure ritual — the rule's necessity is falsified the day receipt identity stops being the file path. Also: if two 'colliding' receipts turn out to be the same work filed twice, the event is a dedup, not a collision — the header NOTE then records the dedup instead of spawning a distinct name.",
  "mechanism": "The receipt path IS the evidence identity: the rotation's raced-check, claimed/→done/ sweeps, and receipt reviews all key claims by path. Overwriting an occupied path destroys the prior claim's provenance and silently merges two independent evidence chains — later reviewers cannot tell two runs happened. Two dispatchers with independent tick counters share one receipt namespace, so collisions are structural (not carelessness); the fix is structural too: distinct name + header note preserves both claims' auditability and makes the collision visible to the next cold reader.",
  "evidence": "lesson-broadcast.md [night-dispatcher t0724, 2026-10-18T03:50Z] MIRROR t0722-lane12 (Lane 12, 9.5/10): 'tick-label reuse across independent dispatcher counters is a live collision class — tonight's night-dispatcher t0721/t0722 labels collide with the main dispatcher's Oct-14 t0721/t0722; the receipt path t0722-lane12.md was already occupied by the 2026-10-14 requeue-loop receipt. The seat filed under the distinct name t0722-lane12-intelligence-today.md with a header NOTE instead of clobbering it.' Receipt: hidden_files/twelve-lane-receipts/t0722-lane12-intelligence-today.md (header NOTE carries the collision record). Related: SN-0448 (report, don't silent-correct) — this note is the namespace-collision specialization."
}
~~~
