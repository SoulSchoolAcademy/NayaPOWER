# SN-1522 — When a New Mechanism Indicts the Test, Read the Indictment Before "Fixing" the Code

Intelligent Block: SN-1522
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-16 (18:38 PDT distillation tick)
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

The lane-executor's gap-gap-t0902-lane12 run installed content-hash dedupe on the hub-bridge webhook receiver (a NEW enforcement mechanism), then ran its battery: 2 of 30 checks went RED. The code was not wrong — the TEST was. The old section (g) re-posted section (a)'s fixture bytes under a new delivery id, which the new dedupe did exactly what it was designed to do and caught. The receipt's own verdict: "The failing checks were the test violating its own premise, not the code violating the spec. When a new mechanism makes previously-green tests go red, the first question isn't 'what broke?' — it's 'did the new mechanism just teach the test something true?' Here it did: dedupe is a property of the bytes, not the section." The repair gave (g) its own distinct fixture bytes and added a new section (h) for the mechanism itself; battery went 30/30 green, sha256-pinned. The discipline: green-after-change is ambiguous evidence between (H1) mechanism bug and (H2) mechanism correct + stale test bytes — and the repair destroys the experiment (once you change the code you can no longer observe the mechanism's verdict), so the interrogation must come first. Tests encode the old worldview; a genuine improvement will always indict the test first. Read the indictment before "fixing" the code.

## HUMAN NOTE

Think of installing a new security camera and discovering that the first "intruder" it flags is your own old test-dummy you left in the hallway. The camera isn't broken — the dummy was always there, and the old camera just couldn't see it. If your first reaction is to adjust the camera until it stops flagging the dummy, you've blinded the very protection you just installed. The right move is to ask the camera what it saw, confirm the dummy is the thing it was designed to catch, and move the dummy. In this case the new content-hash dedupe was the camera, the stale test fixture was the dummy, and the executor asked first — then fixed the test, not the mechanism. Two hypotheses, one ordering rule: interrogate the mechanism's verdict before repairing anything, because repairing first destroys the only evidence that tells you which hypothesis was true.

## CHILD NOTE

Imagine you get new glasses, and suddenly you can see that your old drawing has some crooked lines. The glasses are not broken — they are working! Your drawing just looks crooked now that you can see clearly. The silly move would be to throw the glasses away or say your eyes are broken. The smart move is to say, "Oh, the glasses are showing me the truth," and then fix your drawing. That's exactly what happened here: the new dedupe was the glasses, the old test was the crooked drawing, and the fix went to the drawing — not the glasses.

## GRANDMA NOTE

It's like buying a new smoke detector and having it go off the first night — not because there's a fire, but because it can finally smell the candle you've been burning for years. The old detector was simply too dull to notice. You don't rip the new detector off the ceiling; you blow out the candle, and you thank it for doing its job. Then you test it once more to make sure it stays quiet. New instruments see old dust. Ask the instrument what it found before you start "fixing" things around it.

## NAYA NOTE

Apply this everywhere a new enforcement mechanism meets an old regression suite: (1) **ambiguous-evidence ordering** — a red that appears only after installing a new mechanism has two hypotheses (mechanism bug vs mechanism correct + stale test); the interrogation comes first because repair destroys the experiment. Name both hypotheses in the receipt before touching anything. (2) **the mechanism gets its own section** — here, new battery section (h) for content-hash dedupe was added alongside the fix, so the mechanism is proven on its own terms, not just as "the thing that broke (g)." (3) **fixture isolation under new invariants** — (g) got its own distinct fixture bytes so it stays a pure delivery-id test; shared fixtures across sections are now a known smell whenever a new byte-level invariant lands. (4) **lineage** — this is the mirror of SN-097 (fail-loud-attribute-first): SN-097 is harness-vs-subject misattribution; this is mechanism-vs-test attribution. Same parent discipline (FAILURE-ATTRIBUTION), one level deeper: not "which part of the pipeline owns the failure" but "which direction does the indictment point when the pipeline itself just changed." (5) The falsifier: a red where the mechanism had nothing to teach — i.e., a case where repairing first was correct and a mechanism-interrogation would have produced no attribution. If that class dominates, this note is wrong; the receipt's interrogation line is what lets us count.

## MACHINE NOTE

```json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "mechanism_test_misattribution",
  "evidence": {
    "board": "Smart-note distillation loop 2026-10-16 18:38 PDT. Evidence: hidden_files/twelve-lane-receipts/gap-gap-t0902-lane12.md (lane-executor 18:08 PDT run, Naya Clarity Narzan): content-hash dedupe installed on hub-bridge /webhooks/github (findEventByContentHash, sha256 over RAW MAC-covered body bytes, dedupe only on MAC-verified bytes). First battery run: 2 checks RED in old section (g) — (g) re-posted section (a)'s fixture bytes under a new delivery id, which the new dedupe CORRECTLY caught; (g) given distinct fixture bytes, new section (h) added for the mechanism (h1-h5: same-bytes/new-id deduped by content_hash with original record returned, zero new lines; distinct-payload/new-id appended; content_hash pinned against node:crypto). Battery 30/30 GREEN, test-webhook.sh sha256 c48d561f5a5b8f3a1ccb93555f2a1856014cc81b6d35c72fc45bcba40ec1c97e, transcript hidden_files/hub-bridge/transcript-gap-gap-t0902-content-hash-dedupe-20261016.txt sha256 0d0cd337eba1b894ffdb121128463f0bc5c20f15d1e816bbffefe78acabb64be. The receipt's line 40 states the lesson verbatim: 'did the new mechanism just teach the test something true?'"
  },
  "rule": [
    "when a newly-installed mechanism turns green tests red, interrogate the mechanism's verdict as a possible true positive before repairing anything",
    "name both hypotheses in the receipt (mechanism bug vs mechanism correct + stale test) — repair destroys the experiment, so interrogation comes first",
    "give the new mechanism its own battery section; never let the old suite be the only proof surface for the new invariant",
    "isolate fixtures when a new byte-level invariant lands — shared fixtures across sections become a smell the moment the invariant changes",
    "lineage: mirror of SN-097 (harness-vs-subject); this is mechanism-vs-test — the indictment direction when the pipeline itself changed"
  ],
  "lesson_line": "Tests encode the old worldview; a genuine improvement will always indict the test first — read the indictment before 'fixing' the code.",
  "applies_when": ["failure-attribution", "new-mechanism", "regression-repair", "battery"],
  "enforcement": "Lane-receipt scoring: any code/test repair made after installing a new mechanism must carry a mechanism-true-positive interrogation line (what the mechanism caught, why the old bytes were stale, per-section) — a receipt that repairs under a new mechanism without that line is repair-without-attribution and scores below the 9.5 bar. Battery pattern: the new mechanism ships its own test section before shared fixtures are touched."
}
```
