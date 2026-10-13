# No 40-Hex ANYWHERE in ## Evidence — the Receipt-Gate Extractor Eats Raw SHAs, Even Inside URLs

**Intelligent Block:** IB-SMART-NOTE-20261011-sn1007-no-40hex-in-evidence
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 13:08 PDT distillation tick (2026-10-11) from #2175 comment 6112767428 (night-shift-verify sign-out — T-20 DONE, 2026-10-11T19:21:45Z), read live. Build lane independently corroborated at 19:10 UTC. Defect proven in a depth-1 simulation, not argued in prose.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The receipt-gate's sha-handle extractor treats ANY 40-hex string in a `## Evidence` body as a sha handle — including a commit SHA embedded inside a checks-URL. In the depth-1 simulation that handle resolves dead: the gate tries to fetch a "sha" that was never meant to be a handle, and the evidence link it was part of dies with it. Sweep rule, extended by the T-20 verify run: **no 40-hex ANYWHERE in ## Evidence — bare or in-URL.** Reference checks by workflow name and run ID, never by pasting raw SHAs.

## 🩷 HUMAN NOTE

Imagine a librarian who files every 40-letter code she sees as a call number — even the tracking number printed on the spine of a book you brought her to identify it. She walks off to the stacks with that tracking number and never comes back, and your actual evidence never gets read. The fix isn't a smarter librarian (that's the gate team's job). It's you: never hand her anything that looks like a call number unless that's exactly what you mean. Write the check's name and its run number; leave raw hashes out of evidence bodies entirely.

## 👶 CHILD NOTE

When you write down proof, don't write any long secret codes — even inside a web address. The robot that checks your work sees a code and tries to use it like a key. The key doesn't fit, so the robot gets stuck and your proof breaks. Just say "the test run from Tuesday" instead of pasting the code.

## 👵 GRANDMA NOTE

You know how a bar code scanner will beep on anything that looks like a bar code — even a picture of one on a magazine? Same here. The checking machine grabs anything that looks like one of those long computer codes, even if it's sitting inside a web link. So we simply don't put those long codes in the evidence notes at all. Write the name of the check instead.

## 🤖 NAYA NOTE

The sha-handle extractor runs a dumb regex-style match over the whole `## Evidence` section; it has no notion of "this SHA is part of a URL" or "this one is illustrative." Depth-1 proves the failure is real: the extracted handle resolves dead and the evidence it was attached to is lost. Until the extractor learns context (the build lane's follow-up), the discipline is writer-side: evidence bodies are SHA-free zones. Cold-successor rule: if you need to cite a commit or run in evidence, cite it by check name + run ID + timestamp, and put the raw SHA in the code or log the check produced, never in the body text.

## ⚙️ MACHINE NOTE

{
  "sn_id": "SN-1007",
  "intelligent_block": "IB-SMART-NOTE-20261011-sn1007-no-40hex-in-evidence",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-11",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE",
  "sub": "GOVERNANCE/RECEIPT-HONESTY",
  "evidence": [
    {"type": "board_comment", "ref": "#2175 comment 6112767428", "created_at": "2026-10-11T19:21:45Z", "lane": "night-shift-verify T-20", "finding": "receipt-gate body defect: 40-hex SHA embedded in ## Evidence checks-URL extracted as sha handle, dead on depth-1"},
    {"type": "corroboration", "ref": "build lane, 2026-10-11 19:10 UTC", "finding": "independently corroborated; sweep rule extended: no 40-hex ANYWHERE in ## Evidence, bare or in-URL"}
  ],
  "rule": "Evidence bodies MUST NOT contain any 40-hex string. Cite checks by workflow/check name + run ID. Raw SHAs live in the code/logs that produced them, never in evidence prose.",
  "relates_to": ["SN-0997 (receipt honesty)", "FM-16-adjacent: merge-law-breach governance receipts"],
  "carrier": {"branch": "naya4/smart-notes-2026-09-30", "pr": "#1825", "merge": "NEVER", "ratification": "Shawn only"}
}
