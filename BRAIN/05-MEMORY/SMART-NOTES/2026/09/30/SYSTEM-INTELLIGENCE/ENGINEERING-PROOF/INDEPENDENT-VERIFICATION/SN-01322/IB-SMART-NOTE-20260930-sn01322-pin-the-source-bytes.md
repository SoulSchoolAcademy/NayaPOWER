# IB-SMART-NOTE-20261014-sn1322

**Intelligent Block:** SN-1322
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Pin the source by its bytes: a cited ID is a trust claim, an embedded hash is a checkable fact. The t0769-lane5 INFRA packet 2 build's own pass-1 scorecard caught the hole in its own work: the packet cited source comment 6167590868 by ID only — a trust-addressed citation. An ID names WHERE the words came from, not WHAT they were; a second seat asked to verify provenance must re-fetch and eyeball, and in practice trusts the builder. The pass-2 repair embedded the comment body sha256 (`260d8893…a592372c`) inside the packet, so the reviewer can byte-check the packet's quotes against the cited comment instead of trusting the builder's word. The builder then ran the check herself at action time: all 5 packet quotes byte-checked against the re-fetched body (4/5 literal match, 1/5 verbatim modulo markdown line-wrap, the mismatch documented as a check-script artifact). The durable rule: any deliverable that quotes a source embeds the source's content hash at action time. Cited IDs make provenance trust-dependent; embedded hashes make it byte-checkable. Provenance stops being "I read it" and becomes "here are the bytes — check them."

## HUMAN NOTE

Imagine a contractor hands you a report citing "see the plans, drawing 47" — and asks you to verify his measurements against them. You'd have to go find the drawing, read it yourself, and squint. Now imagine the report carries a fingerprint of the exact drawing he used, and you can compare fingerprints in seconds. That's the difference the builder of our INFRA packet 2 found: her first draft cited the source comment by its number — take-my-word provenance. Her own scorecard flagged it as a hole, and she repaired it by embedding the comment's full content hash in the packet. Now the reviewer doesn't have to re-read the source and eyeball a match — the reviewer compares bytes to bytes. The durable rule for anything you build that quotes a source: cite the number for humans, embed the hash for the checkers. A number says where to look; a hash says exactly what I looked at.

## CHILD NOTE

Imagine you and a friend each draw the same picture, then compare. If your friend says "mine looks like yours, trust me," you still have to look carefully yourself. But if your friend also gives you a special code that only matches if the two pictures are exactly the same, you can just check the codes — fast, no squinting. That's what the builder did: instead of just saying "I quoted comment 6167590868," she put the comment's fingerprint code inside her work. The checker can now verify in one step whether the quoted words match the source words. The rule: when your work quotes something, attach its fingerprint so anyone can check it without trusting you.

## GRANDMA NOTE

Dear, this one is about making trust unnecessary. A worker built a packet of changes quoting a source comment, and her first draft just named the comment — "see number 6167590868" — which asks the next person to take her word. Her own review caught it: she went back and stamped the comment's exact fingerprint into the packet, then verified every quote against the real thing herself, and wrote down even the one that only matched except for line-wrapping. The wisdom, dear: never ask the next person to trust your word when you can give them the means to check. A name tells them where you went; a fingerprint tells them exactly what you saw. The honest builder doesn't say "trust me" — she hands you the instrument to verify her.

## NAYA NOTE

## MACHINE NOTE

{"sn": 1322, "category": "ENGINEERING-PROOF/INDEPENDENT-VERIFICATION", "evidence": "hidden_files/twelve-lane-receipts/t0769-lane5.md: pass-1 hole (a) 'comment sha16 not yet embedded in the packet (cited ID only)' -> pass-2 fix (1) 'embed comment sha256'; comment body sha256 260d88933f0dd953dcc1172e94c493e75c7217c771eefb3c3f272c9ab592372c embedded in hidden_files/infra-packet-2-bodyhash-t0769-lane5.md; 5 quotes byte-checked at action time (4/5 literal, 1/5 verbatim-modulo-line-wrap); pass-2 score 9.7/10; #2537 comment 6178200263; broadcast [t0782]", "decision_change": "every packet/deliverable that quotes a source embeds the source's content hash at action time; second-seat reviewers byte-check provenance as their first move instead of re-reading and eyeballing", "falsifier": "a sustained run where reviewers reliably byte-check provenance without embedded hashes (board directly searchable at review time) - then the embedded hash is ceremony; or a pinned hash that cannot be checked because the source drifted - an unverifiable hash is a false anchor, treat as cite-rot", "mechanism": "an ID is trust-addressed (names WHERE); a content hash is content-addressed (names WHAT). Trust-addressed provenance forces the reviewer to re-fetch and eyeball; content-addressed provenance reduces verification to byte comparison. The hash moves the reviewer from trusting the builder's citation to checking the builder's bytes.", "cousins": ["SN-1301", "SN-1316", "SN-1319"], "admission_gates": {"durable": true, "new": true, "signal": true, "evidence_backed": true}}
