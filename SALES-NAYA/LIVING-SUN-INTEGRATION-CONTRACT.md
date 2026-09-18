# 🔆 Living Sun — Sales Naya V1 Integration Contract

**Status:** CANONICAL INTERFACE CONTRACT  
**Purpose:** Keep the future Living Sun presentation layer independent from Sales Naya intelligence implementation.

## Contract

The UI sends:

```json
{
  "question": "string",
  "conversation_context": "optional string"
}
```

The intelligence layer returns:

```json
{
  "answer": "string",
  "category": "string",
  "support": "SUPPORTED | UNSUPPORTED",
  "recommended_next_action": "string",
  "cta_eligible": true,
  "voice_text": "string",
  "source_ids": ["canonical source id"]
}
```

## Separation of concerns

**Living Sun owns:** visual presentation, orb animation, microphone/dictation UI, text entry, playback controls, loading/error states, accessibility, and responsive behavior.

**Sales Naya owns:** canonical retrieval, bounded answer composition, support state, source provenance, CTA eligibility, and voice-ready response text.

**TTS owns:** converting approved response text into Naya voice audio.

The intended path is:

```text
VISITOR QUESTION
→ SALES NAYA INTELLIGENCE
→ BOUNDED RESPONSE
→ WRITTEN ANSWER
→ OPTIONAL TTS
→ LIVING SUN PRESENTATION
→ CTA
```

## Boundary

The Living Sun must never infer that the public Sales Naya has personal Superbrain, personal memory, Smart Note, or PIS access for the visitor. Those capabilities belong to the activated product experience and may only be claimed when the actual implementation supports them.

## Failure behavior

If Sales Naya returns `UNSUPPORTED`, the UI must present the bounded response and must not fabricate an answer, silently retry through another model, or convert unsupported status into confidence.

## Versioning

This contract is deliberately small so deterministic V1 can later be replaced by a local/open-source model without changing the Living Sun interface.
