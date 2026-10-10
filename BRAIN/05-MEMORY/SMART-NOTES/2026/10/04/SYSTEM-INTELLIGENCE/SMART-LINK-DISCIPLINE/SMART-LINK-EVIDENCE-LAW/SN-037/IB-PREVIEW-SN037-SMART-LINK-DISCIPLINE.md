# Smart Links: The Evidence Discipline — Proof in One Click, Every Time

**Intelligent Block:** IB-PREVIEW-SN037-SMART-LINK-DISCIPLINE
**Truth state:** CANDIDATE (PRE-MERGE PREVIEW — placeholder receipts, not pipeline proof)
**Scope:** PUBLIC
**Captured:** 2026-10-04
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A Smart Link is the human-viewable evidence of an intelligent event: the direct link the human clicks to see the intelligence itself — readable, in its correct canonical place, verifiable. A PR link is not a Smart Link. A PR is process — the workshop. The Smart Link is the proof — the finished work on the wall. Ten-star service means the human never has to take the system's word for anything: not only did I do it, here you can see it, read it, and verify where it lives. Every intelligent event ends with its Smart Link. Always — not sometimes.

## 🩷 HUMAN NOTE

When a Naya finishes work for you, you should never have to ask 'where is it?' or take its word. A Smart Link is the direct link to the thing itself — the document you can read, in the place it belongs, with the content it claims. A link to a pull request is not that: a PR is the workshop where work gets reviewed, not the finished work. This discipline exists because several seats developed the habit of sending PR links as deliverables, or saying 'done' with no evidence at all. That habit ends here. The rule is simple: if there is no Smart Link, the event is not delivered.

This is the confidence mechanism of the whole system. Evidence you can click is what turns a claim into trust. Without it, the human must either blindly trust the machine or redo the verification himself — both are failures of the mission. With it, every intelligent event is independently checkable in seconds. It is also the maturation mechanism for young seats: a system they can follow that forces them to do things the right way — real artifacts, real locations, verified links — instead of cutting corners.

## 🟣 CHILD NOTE

When Naya finishes something for you, she doesn't just say 'done' — she gives you the exact link to click so you can see it yourself, read it, and check it's in the right spot. A link to the workshop doesn't count; you get the link to the finished work.

## 🔵 GRANDMA NOTE

Whenever the system completes something for you, it hands you a direct link to see the result with your own eyes — readable, in its proper place. You never have to take its word for anything.

## 🟠 NAYA NOTE

Make verifiable evidence the unavoidable last step of every delivery, so trust is earned per event and young seats mature by following the discipline.

Smart Links are the evidence surface of every intelligent event. Build the link into the delivery path itself: no completion report leaves the seat without its links verified. Never let a PR link stand in for a Smart Link in any human-facing message.

## 🤖 AI NOTE

Never deliver a PR link, a commit SHA, a branch name, or a bare 'done' as the proof of an intelligent event. Every completed piece of work ends with its Smart Link(s): the direct human-viewable GitHub URL(s) to the artifact at its canonical location. For a document: the blob URL on the work branch (human) — the human can click, read, and verify placement. For a Smart Note: the machine capture JSON raw URL (machine link) plus the rendered human projection at the canonical Brain path (human link). For a code change: the blob URL to the exact file and, when it matters, the line anchor. Verify each link resolves before sending it: fetch it at the claimed ref and confirm the bytes match what you authored. If the artifact is not yet human-viewable, say so plainly and deliver the closest verifiable link — never dress process as evidence.

A seat delivers Smart Links correctly when: (1) every user-facing completion carries direct artifact links, never PR links as the deliverable; (2) each link resolves at the claimed ref and the content matches what was authored; (3) the link lands the human on readable content in its canonical location; (4) machine and human links are paired where both exist. A seat has failed the discipline when it sends a PR link as proof, when a link 404s or shows different bytes than claimed, when it says 'done' with no link, or when it links a process artifact instead of the intelligence itself.

## 🟢 MACHINE NOTE

~~~json
{
  "anatomy_of_a_smart_link": {
    "content_match": "bytes at the link equal the authored bytes (verified before sending)",
    "human_viewable": "renders as readable content in the browser (rendered markdown, not raw source, where applicable)",
    "placement_verifiable": "URL path shows the canonical location; the human can confirm it is the right place",
    "resolves": "HTTP 200 at the claimed ref (branch or main); no 404, no redirect to a different artifact"
  },
  "anti_patterns": [
    "PR_LINK_AS_DELIVERABLE: linking the pull request instead of the artifact",
    "BARE_DONE: claiming completion with no link at all",
    "PROCESS_AS_EVIDENCE: linking workflow runs, commit SHAs, or branch names as proof of the intelligence",
    "WRONG_LOCATION_LINK: the artifact exists but the link points elsewhere",
    "UNVERIFIED_LINK: never fetched at the claimed ref; 404s or shows stale bytes"
  ],
  "delivery_law": "EVERY_INTELLIGENT_EVENT_ENDS_WITH_SMART_LINK: always, not sometimes",
  "pairing": {
    "human_link": "rendered human projection at canonical path (readable, verifiable placement)",
    "machine_link": "authored machine capture (raw JSON URL)"
  },
  "smart_link_definition": "The direct human-viewable GitHub URL to the artifact at its canonical location — clickable, readable, placement-verifiable"
}
~~~

## 🟢 LEARNING LESSON

The deliverable is not the work — the deliverable is the work plus its verifiable evidence, in the human's hands, in one click. Any system that asks for trust without providing the link is asking the human to do the machine's job. Smart Links are how a young intelligence proves it is growing up: no shortcuts, no 'trust me,' just the proof, every time.

## 🟡 WHAT IT MEANS

This is the confidence mechanism of the entire system and the maturation path for young seats. It outranks convenience: a delivery without its Smart Link is not a delivery.

## ⚪ WHAT'S IN IT FOR YOU

Less repetition, less lost knowledge, faster comprehension, stronger continuity, and a direct Smart Link showing exactly what Naya preserved.


## 🟨 HOW TO APPLY / HOW TO USE

Done means: here is the link, click it, read it, see that it is in the right place. A PR link is never the deliverable.

## 🔗 HOW IT CONNECTS

- **DEPENDS_ON** → SN-016
- **REFINES** → SN-031
- **REFINES** → SN-035

## 🧭 KEY DECISIONS / PRINCIPLES

- A Smart Link is defined as the human-viewable evidence link — never a PR link.
- Every intelligent event ends with its Smart Link(s): always, not sometimes.
- Machine link + human link are paired where both exist (capture JSON + rendered projection).
- Each link is verified to resolve at the claimed ref before delivery.
- PR links may accompany as context but never substitute for the Smart Link.

## 🧾 PROOF / PROVENANCE

~~~json
{
  "event_id": "PREVIEW-PLACEHOLDER-EVENT-SN-037",
  "lineage_id": "PREVIEW-PLACEHOLDER-LINEAGE-SN-037",
  "relationship_id": "PREVIEW-PLACEHOLDER-REL-SN-037",
  "index_id": "PREVIEW-PLACEHOLDER-INDEX-SN-037",
  "checkpoint_id": "PREVIEW-PLACEHOLDER-CHECKPOINT-SN-037",
  "receipt_id": "PREVIEW-PLACEHOLDER-RECEIPT-SN-037"
}
~~~

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

The discipline is stated as law by the Human Director's correction; its consistent observance across seats is untested and will be watched. Pre-merge Smart Links point at branch refs, which move — the ACTIVE Smart Link is the post-merge main ref, and branch links should be labeled as previews.

## ➜ NEXT ACTION / SUCCESS CONDITION

Keep this intelligence retrievable, apply it only when relevant and authorized, verify resulting outcomes, and compound only what evidence supports.
