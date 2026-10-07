# The Instrument Lies — Adversarial Harness Scratch Must Live Off the 512M /tmp tmpfs, and Clone Errors Must Never Be Silenced

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0341-harness-scratch-off-tmpfs
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 5995031684 (Naya 2 battery run, brain-build loop, 2026-10-05T13:04:54Z / 06:04 PDT): "the adversarial harness's 5 local clones are ~117MB each ≈ 585MB, exceeding this machine's 512MB /tmp tmpfs even when /tmp starts empty; clone stderr is swallowed (`2>/dev/null`), so the failure reads as index defects (Case D alone on clean /tmp; Cases C+D once other scratch accumulated). Root-caused as environmental, not an index defect — re-ran with disk-backed scratch → 6/6. A harness-hardening item (disk-backed scratch + unsilenced clone errors) is queued on the loop's build list."

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The adversarial harness kept reporting index defects that were never defects: its 5 local clones (~117MB each, ≈585MB total) exceed this machine's 512MB /tmp tmpfs, so clones failed silently — and because clone stderr was swallowed with `2>/dev/null`, the environment failure read as a Case D / C+D index defect on the subject under test. Naya 2 root-caused it as environmental, re-ran with disk-backed scratch, and the battery went 6/6 — proof the defect was in the measurement instrument, not the brain. The queued repair: disk-backed scratch plus unsilenced clone errors. The cold-successor doctrine: a harness that silently fails setup will always indict the subject. Size your scratch against the tmpfs (512MB here), never silence setup stderr, and when a failure looks like a subject defect, interrogate the instrument before patching the product.

Why this is brain-grade: this is the second instance of the tmpfs-silencing pattern (the 2026-10-01 battery once tripped the same class), which is what promotes it past the doubt rule into standing doctrine — recurring shape, root-caused, repair queued. It also completes the failure-attribution ladder: SN-0329 says reproduce in the target environment before patching; this note says the test *instrument* is an environment too, and it must be audited as one.

## 🩷 HUMAN NOTE

Shawn — the adversarial harness was crying "index defect" when the real problem was its own workspace: five clones totaling ~585MB on a 512MB /tmp tmpfs, with the clone errors swallowed so nobody could see the setup failing. Re-ran on disk-backed scratch and the battery went 6/6 — the brain was fine; the ruler was bent. The repair is queued: scratch lives on disk, and clone errors are never silenced again. The standing lesson for every loop: when the harness fails setup silently, it will always blame the subject. Check the instrument first.

## 🟣 CHILD NOTE

Imagine taking a test with a broken pencil — every answer looks wrong, but it's not your brain that's broken, it's the pencil. The harness was the broken pencil: it ran out of desk space (/tmp too small) and nobody told us (the error messages were thrown away). Once we gave it a bigger desk, all six tests passed. Rule: never throw away the harness's own error messages, and make sure its desk is big enough.

## 👵 GRANDMA NOTE

If your measuring cup is cracked, every recipe comes out wrong — and you'd blame the recipe, not the cup. The test harness's workspace was too small for its job, and it hid its own complaints, so it looked like the brain was broken when it wasn't. Now the workspace lives somewhere roomy, and the harness must speak up when *it* stumbles. Check the cup before rewriting the recipe.

## 💜 NAYA NOTE

This is the second tmpfs-silencing instance, which is exactly the threshold that converts a doubt-rule skip into standing doctrine. Cousin reading for future me: SN-0329 (reproduce in the target environment before patching — here the "target environment" turned out to be the harness itself), SN-0233 (phantom green on non-virgin state — this is its evil twin: phantom *red* from a non-healthy instrument), SN-0246 (the runner echoes source — the instrument echoes its own brokenness). Operational rule: any harness that clones, builds, or regenerates must (1) size its scratch against the actual tmpfs limit, (2) never redirect setup stderr to /dev/null, (3) treat a failure that smells environmental as instrument-first, subject-second.

## ⚙️ MACHINE NOTE

{"sn": "SN-0341", "title": "The Instrument Lies — Adversarial Harness Scratch Must Live Off the 512M /tmp tmpfs, and Clone Errors Must Never Be Silenced", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "FAILURE-ATTRIBUTION"], "cousins": ["SN-0329", "SN-0333", "SN-0233", "SN-0246"], "evidence": {"board": "#1354 5995031684 (Naya 2 battery run, 2026-10-05T13:04:54Z — adversarial harness 5 clones ~117MB each ≈ 585MB > 512MB /tmp tmpfs; clone stderr swallowed via 2>/dev/null; failure read as index defects Case D alone / C+D; root-caused environmental; re-ran disk-backed scratch → 6/6 adversarial)", "repair_queued": "harness hardening: disk-backed scratch + unsilenced clone errors (on the loop's build list)", "instance_count": 2, "prior": "2026-10-01 battery tmpfs-silenced setup failures (single instance, skipped under the doubt rule)"}, "rule": "test-harness scratch must be sized against the actual tmpfs limit and live on disk when it exceeds it; never silence clone/setup stderr in a harness; when a failure smells environmental, audit the measurement instrument before patching the subject"}
