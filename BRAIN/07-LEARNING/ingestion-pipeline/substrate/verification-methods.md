# Verification Methods

<!-- Managed by learn-ingestion. Sections appended per ingested Smart Note. -->

## SN-0283 — False-Pass Surfaces — Qualify Every Validation Tool with Known-Broken and Known-Green (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/VERIFY-COVERAGE/SN-0283/IB-SMART-NOTE-20261004-sn0283-false-pass-surfaces.md`
**Truth state:** CANDIDATE · **Type:** VERIFICATION_METHOD · **Ingested:** 2026-10-04T23:46:56Z

> Source: #1354 comment 5984988511 (2026-10-04T22:11:25Z, [CODA 1] "KNOW, DON'T GUESS" — "I went and found out"). Experiment: `tools/smart_note_v2.py discover` run against three captures — SN-028 (hers), known-broken SN-022 (key MISSING), known-green SN-017. Result: identical output, identical exit code (exit 0) for all three — "discover does not discriminate. It finds captures; it does not validate them." Consequences named in the comment: (1) Phase 1's "mechanical SN-002 conformance" — the thing

**Evidence:** {"comment": "#1354 5984988511 (2026-10-04T22:11:25Z)", "experiment": "discover run against SN-028 (own), SN-022 (known-broken, key missing), SN-017 (known-green)", "phase1_gap": "claimed mechanical SN-002 conformance did not exist (subcommands: discover, project, retrieve, held-out, promote \u2014 n
**Cousins:** Evidence law (gate weakening), Closer role (reproduce → classify → repair the seam), First-claim-by-metadata ruling (same comment)

## SN-0284 — Convention Coherence — One Enum, Consumers Broaden Before Producers Change (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/CLASSIFICATION-INTEGRITY/SN-0284/IB-SMART-NOTE-20261004-sn0284-convention-coherence.md`
**Truth state:** CANDIDATE · **Type:** VERIFICATION_METHOD · **Ingested:** 2026-10-04T23:46:57Z

> Source: #1354 comment 5985108483 (2026-10-04T22:23:27Z, [NAYA 4] "D6 Convention Split — Coordination Needed") + 5985160918 (2026-10-04T22:30:27Z, [NAYA 4] "Ownership Brief — D6 Convention Fix"). The observed split on main 8a464a66: `tools/smart_note_v2.py:206` emits "ACTIVE" · `tools/smart_link.py` backfill wrote "ACTIVE_AUTH_GATED" (all 28 entries, PRIVATE scope, per its own docstring "never bare ACTIVE", line 17) · `live-intelligence-commit-proof.yml:253` asserts =="ACTIVE" (+ line 270 checks 

**Evidence:** {"audit": "6-dimension re-audit, main 8a464a66: D6 2\u21928, overall 5.8\u21928.83", "blocked_on_shawn_keys": ["PR #1408 merge (D2)", "workflow lines 254/271 edit", "smart-link-gate.yml landing (token 403 on workflows/merge)"], "comment_brief": "#1354 5985160918 (2026-10-04T22:30:27Z)", "comment_spl
**Cousins:** SN-0283 (false-pass surfaces — same disease from the other side), SN-0101 Seam-Gap protocol (consumer flags the boundary, owner rules)

## SN-0072 — Prove the Xfail, Don't Wrap It — An Expected-Failure Wrapper Can Manufacture a False Green (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-072/IB-SMART-NOTE-20260930-sn072-xfail-constraint-proven-not-asserted.md`
**Truth state:** CANDIDATE · **Type:** VERIFICATION_METHOD · **Ingested:** 2026-10-04T23:50:17Z

> ["an xfail is a promise of absence \u2014 the suite must never report green-by-accident for it", "never absorb the expected failure with a wrapper (pytest.raises / try-except pass / broad matchers)", "prove the constraint three-part: xfail states the goal, paired non-xfail signature test proves the detector fires, mutation table proves the detector is non-vacuous", "keep the mutation table (injected break -> observed result -> constraint) in the docstring or board report", "the red must be earned, documented, and reproducible on demand \u2014 SN-066 and SN-061 applied to expected failures"]

**Evidence:** {"board": "#554 comment 5935306613 (2026-10-01T16:01:32Z) \u2014 Coda 4 CS-01 board link, 'xfail constraint, proven rather than asserted'", "incident": "wrapping the expected assertion in pytest.raises(match=...) made the test pass and produced XPASS(strict) \u2014 a self-inflicted red run; reverted
**Cousins:** none

## SN-0074 — "API Pushes Never Trigger Actions" Was an Event-Scoping Overgeneralization — Scope CI-Trigger Claims by Workflow Event (SN-048 Correction) (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/CI-TRIAGE/CI-TRIGGER-SILENCE/SN-074/IB-SMART-NOTE-20260930-sn074-api-push-trigger-event-scoping.md`
**Truth state:** CANDIDATE · **Type:** VERIFICATION_METHOD · **Ingested:** 2026-10-04T23:50:17Z

> ["scope every CI-trigger claim by workflow event type (push vs pull_request vs workflow_dispatch), never by push mechanism alone", "Data-API pushes do not fire push-event workflows; they do fire pull_request-event workflows \u2014 cite the run or its absence", "keep SN-051's local-verification-as-gate where the needed evidence channel is blind; it is a channel-scoped remedy", "when evidence falsifies a published claim: retract in the same public channel, correct the standing doc in the same motion, name contaminated earlier doubts", "timestamp CI-absence claims; re-verify when the head moves or the workflow set changes"]

**Evidence:** {"corroboration": "#554 comment 5935839686 \u2014 523/0 local suite on exact 2a7851a8 bytes; CI SUCCESS on that head", "falsifying_board": "#554 comment 5935895530 (2026-10-01T16:34:51Z) \u2014 GitHub Actions DID run on API-pushed v3 head 2a7851a8: test=SUCCESS, Collective Chain Readiness Gate=SUCCE
**Cousins:** none

## SN-0076 — Your Failing Test Can Be the Artifact — Single-Variable Defect Reproduction, and Retract with Requalification (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-076/IB-SMART-NOTE-20260930-sn076-single-variable-defect-reproduction.md`
**Truth state:** CANDIDATE · **Type:** VERIFICATION_METHOD · **Ingested:** 2026-10-04T23:50:17Z

> ["a defect test must isolate exactly one variable between baseline and variant; node identity, state ownership, clocks, and ids are all variables", "a failure that cannot distinguish 'mechanism broken' from 'test setup wrong' is TEST INVALID, not a defect \u2014 verdict it as such", "when equivalence cannot be held constant, prove it first (deterministic recreation with controlled clock/id)", "retract loudly, then requalify: replace every withdrawn broad claim with the narrowest adjacent true statement", "precision of language is part of the claim \u2014 never assert identity ('byte-identical') while exhibiting difference"]

**Evidence:** {"board": "#554 comment 5936467351 (2026-10-01T17:06:22Z) \u2014 Coda 1's RETRACTION + REQUALIFICATION at frozen 4768636f; root cause identified in 5936387153 (Naya 1's test-validity finding on PR #1247)", "clean_test": "baseline AND substituted on the same node instance with the same evolution_id \
**Cousins:** none

## SN-0079 — Withheld Certification Is the Gate Working — Grade the Hold, Don't "Fix" the Gate (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-079/IB-SMART-NOTE-20260930-sn079-withheld-certification-gate-hold.md`
**Truth state:** CANDIDATE · **Type:** VERIFICATION_METHOD · **Ingested:** 2026-10-04T23:50:17Z

> ["a gate's hold is a terminal observation, not an error signal \u2014 route work to the named gaps, never to the gate's thresholds", "'make it pass' pressure is the adversarial input gates exist to resist \u2014 proposals to relax a gate because a claim 'should' pass are suspect-by-default", "tests assert the claim's evidence state, not the gate's verdict", "report mid-ladder states mechanically: held-with-gaps \u2260 failure, and held \u2260 approved"]

**Evidence:** {"author_doctrine": "forcing a PASS would be dishonest \u2014 the hold is the gate working, not a failure", "board": "#554 comment 5937011559 (2026-10-01T17:39:35Z) \u2014 Naya 4 P7 partial: ProveNode.gate() returns NEED_EVIDENCE on the Demo-1 claim, held at EVIDENCED (required L2 for 'low' stakes),
**Cousins:** none

## SN-0085 — Append-Only Is a Method, Not an Invariant — Resolve-Then-Trust Does Not Establish Origin (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-085/IB-SMART-NOTE-20260930-sn085-append-only-method-not-invariant.md`
**Truth state:** CANDIDATE · **Type:** VERIFICATION_METHOD · **Ingested:** 2026-10-04T23:50:17Z

> ["append-only is a method (convention), not an invariant (structure) \u2014 conventions are attacker-reachable inside the boundary", "resolve-then-trust does not establish origin on a poisonable store", "anchor trust in invariants: content-committed ids, allowlist comparison against resolved objects, store-identity consumption", "make dangerous seams structurally impossible: construction-owned resolver, non-substitutable, non-accidentally-enableable fixture mode", "keep the falsifying counterexample in the record \u2014 it outvalues the design it breaks"]

**Evidence:** {"board": "#554 comment 5937954809 (2026-10-01T18:31:55Z) \u2014 Coda 1 DESIGN VERDICT with proven counterexample: VerifyNode._receipts is a plain dict; delete_receipt raises (append-only by convention); direct assignment v._receipts[\"attacker-1\"]=\u2026 succeeds \u2014 resolver pointed at live di
**Cousins:** none

## SN-0091 — Resolve Contract Mismatches at the Source, Not by Widening the Contract — the Five-Class Field-Binding Taxonomy (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-091/IB-SMART-NOTE-20260930-sn091-field-binding-taxonomy.md`
**Truth state:** CANDIDATE · **Type:** VERIFICATION_METHOD · **Ingested:** 2026-10-04T23:50:17Z

> ["when a contract mismatch blocks, source-find first: re-check authoritative tables, envelopes, writers, run evidence \u2014 never widen the contract", "classify every manifest field: RECEIPT-BOUND / SOURCE-BOUND / WRITER-ASSIGNED / EXPLICIT-EMPTY / UNKNOWN; refuse unlabeled fields", "SOURCE-BOUND must name the source and its non-claim boundary; EXPLICIT-EMPTY is a semantic no-claim, never a placeholder", "keep UNKNOWN rather than guessing when the authoritative proof is missing \u2014 it is a complete binding", "prove the completed package through the canonical path end-to-end with adversarial controls; never reconstruct the specimen", "never borrow a proven artifact from another receipt family to fill the gap (SN-090)"]

**Evidence:** {"board": "#554 comment 5938718550 (2026-10-01T19:14:37Z) \u2014 Naya 1 P6 correction: canonical production owner UUID adfdf0b8-5558-41d1-9fed-ec51abf4fe2f observed-not-asserted; project NayaNET; revision writer-allocated from max(revision)+1; action staging.write_file from LAW envelope; learning=[]
**Cousins:** none

## SN-0094 — A Fresh Clone Can Still Be the Wrong Evidence — Attribute Red Suites to the OS, Not the Workspace (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/CI-TRIAGE/CROSS-PLATFORM-LOCALE/SN-094/IB-SMART-NOTE-20260930-sn094-cross-platform-locale.md`
**Truth state:** CANDIDATE · **Type:** VERIFICATION_METHOD · **Ingested:** 2026-10-04T23:50:17Z

> ["'your environment' is a claim to be falsified with a genuine fresh clone under harder conditions, not an explanation", "attribute surviving failures to the platform (OS locale, codec, fixtures) before the workspace; name which you have evidence for", "fix what is proven (open(..., encoding='utf-8')) and retain the residue as explicit UNRESOLVED/UNATTRIBUTED with per-file counts and owner", "when your assertion pinned old runtime behavior, fix the assertion and declare it \u2014 never launder a red into a green", "decline both attributions until the last unexplained root cause is traced: 'I will not sign off code is green' is the gate working"]

**Evidence:** {"board": "#554 comment 5939450892 (2026-10-01) \u2014 Coda 1 requalification of d359770d (parent 384df875, PR #1216): genuine git clone, new path, autocrlf=true; fresh clone 36 failed/1094 passed/5 errors; PYTHONUTF8=1 -> 31 failed/1099 passed/5 errors. Root cause #1 PROVEN: UnicodeDecodeError 'cha
**Cousins:** none

## SN-0095 — Compose at the Consumer — Authorship Stays in the Author, Trust Stays in the Seal (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/INTERFACE-OWNERSHIP/SN-095/IB-SMART-NOTE-20260930-sn095-compose-at-the-consumer.md`
**Truth state:** CANDIDATE · **Type:** VERIFICATION_METHOD · **Ingested:** 2026-10-04T23:50:17Z

> ["name both mismatches at the exact SHA \u2014 channel (what each side speaks) and content (what the channel carries) \u2014 from evidence, not memory", "make the design fork explicit and name the inversion cost before choosing", "compose at the consumer: derive from the producer's sealed facts instead of teaching the producer to emit pre-formed answers", "let the derivation be only the sealed claim \u2014 no caller-controlled labels across the trust boundary", "the seal must cover the content it protects: finalize outcomes before close(); reject derived scope exceeding the verified subject_ref", "deliver diagnostics as diagnostic intelligence, not a competing design \u2014 maximally precise, never prescriptive about the other lane's fix"]

**Evidence:** {"board": "#554 comment 5939362590 (2026-10-01) \u2014 Naya 2's exact-SHA diagnostic: LEARN.extract (learn_node.py:747) requires outcome.lesson/claimed_lesson; VERIFY emits neither (grep lesson verify_node.py = zero hits) but speaks learn_baton (_learn_baton_fields :1075, populated by close :891); c
**Cousins:** none

## SN-0096 — The Composition Root Owns the Bridge — It Transports, It Doesn't Judge (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/INTERFACE-OWNERSHIP/SN-096/IB-SMART-NOTE-20260930-sn096-composition-root-owns-bridge.md`
**Truth state:** CANDIDATE · **Type:** VERIFICATION_METHOD · **Ingested:** 2026-10-04T23:50:17Z

> ["verify edges as code: a declared edge with zero callers is an ordering declaration, not a data bridge \u2014 flag it before the next fix commits", "give the bridge to the composition root \u2014 never bolt it silently into one of the endpoints", "make the bridge a real named method with a real contract: full dict in, downstream id out", "transport, don't judge: document open semantic questions in the method; leave qualification to the caller", "prove the bridge end-to-end through the composition path the architecture claims", "in e2e traces, an unowned bridge reads BLOCKED \u2014 an honest gap, never an invented completion"]

**Evidence:** {"board": "#554 comment 5939370485 (2026-10-01) \u2014 Naya 2's pre-fix diagnostic at 384df875: EVOLVE.observe() zero callers in naya_kernel/; Kernel.decide()/_run_gate moves no data between nodes (edges = ordering constraints + SATISFIED/BLOCKED trace labels); fixing extract alone would not unblock
**Cousins:** none

## SN-0099 — Not Ready to Promise Publicly Yet — The Promise Gate for Documentation and Architecture (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/PUBLIC-PROMISE-BOUNDARY/SN-099/IB-SMART-NOTE-20260930-sn099-not-ready-to-promise.md`
**Truth state:** CANDIDATE · **Type:** VERIFICATION_METHOD · **Ingested:** 2026-10-04T23:50:17Z

> ["when docs and design converge ahead of proof, write the promise boundary into the canonical record: NOT READY TO PROMISE PUBLICLY YET + enumerated gaps", "stamp the truth state mechanically: DOCUMENTED / ARCHITECTURALLY ALIGNED / IMPLEMENTATION-PARTIAL / NOT PRODUCTION-PROVEN \u2014 publicly-promised is a further state beyond deployed", "name the gate test that earns the promise: the two-owner adversarial acceptance proof (isolate, share/revoke, sync upstream, cold-reconstruct)", "write the isolation law before the first fork: DNA inheritable, private state never inheritable; activation creates identities, never clones the original owner's state", "prove refusal, not just wiring: the dispatch must refuse an unbound owner/upstream target before any write"]

**Evidence:** {"board": "#554 comment 5939768533 (2026-10-01): fork-first portable activation / owner isolation system update (Shawn direction, live HEAD 8bfab725); preferred onboarding: fork canonical -> connect -> Activation -> owner-isolated state -> NayaNET (consent-scoped); 'NOT READY TO PROMISE PUBLICLY YET
**Cousins:** none

## SN-0152 — Alive Is Measurable — Taste Words Must Operationalize into Rendered-Verifiable Checks (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/ALIVE-GATE/SN-0152/IB-SMART-NOTE-20260930-sn0152-alive-is-measurable-alive-gate.md`
**Truth state:** CANDIDATE · **Type:** VERIFICATION_METHOD · **Ingested:** 2026-10-04T23:50:17Z

> ["every experiential design-law word ships with falsification conditions: what a render looks like when it fails the word", "checks must be rendered-verifiable: checkable against the visible render and machine-assertable (causal path per control, computed numbers, honest states)", "prefer negative checks: name the failures (dead-button-rendered-live, faked NOT_VERIFIED, lying LOADING, meaningless glow) over aspirations", "a render must pass both SN-017 (evidence claims) and the alive-gate (experience claims)", "new taste directive requires its companion gate; SN-0149 holds the directive itself \u2014 capture operationalization, not the text"]

**Evidence:** {"board": "#554 5945120603 (2026-10-02T03:33:44Z) \u2014 Naya 4 night plan: 'Alive is measurable \u2014 the alive-gate (4 checks, all rendered-verifiable): 1. Every control acknowledges input <=100ms. 2. All seven states honest and rendered \u2014 LOADING only while loading, NOT_VERIFIED never faked
**Cousins:** none

## SN-0170 — When the Scope Blocks the Mechanism, the Board Is the Vehicle (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/GOVERNANCE/AUTHORITY-ENVELOPE/SN-0170/IB-SMART-NOTE-20260930-sn0170-scope-blocked-delivery-protocol.md`
**Truth state:** CANDIDATE · **Type:** VERIFICATION_METHOD · **Ingested:** 2026-10-04T23:50:18Z

> ["a 403 is terminal evidence of an authority boundary \u2014 never retry, route around, proxy, or soften the call", "on scope-blocked delivery: attempt once openly, publish the artifact to the board with exact placement + provenance, delete stray mechanism state, name the completing seat", "the board post is verifiable: byte counts, control counts, provenance SHAs, anchor lines"]

**Evidence:** {"attempt": "#554 5946036715 (2026-10-02T05:16:52Z) \u2014 landing the cold-gate fail-fast patch (selfbuild-20261001-2200-cold-gate-failfast.patch, local commit de2ac5b9) as branch + draft PR: branch creation worked; committing `.github/workflows/live-intelligence-commit-proof.yml` returned **403 'w
**Cousins:** none

## SN-0188 — The Search Index Is a Lagging Projection — Index Hits Are Stale-Index Evidence, Not Current-File Content (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-0188/IB-SMART-NOTE-20260930-sn0188-search-index-stale-evidence.md`
**Truth state:** CANDIDATE · **Type:** VERIFICATION_METHOD · **Ingested:** 2026-10-04T23:50:18Z

> a content claim must be verified against live file bytes at the ref; search-index hits are lagging-projection discovery, never proof; name the source and its staleness on any disagreement

**Evidence:** {"board": "5953501324", "live_verification": "direct fetches of all 11 HUB/ROOMS/*.md file bytes at main tip 5eaec742fa908163e288ac42615b9731a80fc5bf \u2014 literal undefined gone from every room", "related_repair": "5953436017", "stale_matches": "pre-cleanup 80dfc7d2 snapshots via GitHub code-searc
**Cousins:** none

## SN-0197 — A Verification Receipt Names Its Pin (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-0197/IB-SMART-NOTE-20260930-sn0197-verification-receipt-names-its-pin.md`
**Truth state:** CANDIDATE · **Type:** VERIFICATION_METHOD · **Ingested:** 2026-10-04T23:50:18Z

> verification receipts name their exact SHA; a later head move reconciles as a delta, never invalidates the pinned verdict; restate old pins as bounded historical facts, never as claims about the current head

**Evidence:** {"content": "additive, convergence untouched \u2014 oath file added on the same branch", "head_move": "head moved to f307ded2 when the oath file (HUB/ULTIMATE-DESIGN-CONTRACT-V1.md) landed after her check; relay explicitly reconciled: 'your d01ffa93 verification was correct at the time'", "verificat
**Cousins:** none

## SN-0198 — Byte-Cited Critique Is the Actionable Unit (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-0198/IB-SMART-NOTE-20260930-sn0198-byte-cited-critique-actionable-unit.md`
**Truth state:** CANDIDATE · **Type:** VERIFICATION_METHOD · **Ingested:** 2026-10-04T23:50:18Z

> lane challenges cite (file:line, clause, acceptance-condition) per violation; uncitable critique is a taste question for the director, not a work order for the builder; read the bytes, not the screenshots

**Evidence:** {"code_read": "#554 5955257393 \u2014 Naya 2 read the actual v3 bytes (feed.js + feed-stage.css) at f699a537", "credited": "intelligent-block grammar, honest empty state, restrained glow 2x14px, CSS variables, reduced-motion", "violations": "type below floor: 13px body / 10-10.5px labels vs 16px-bod
**Cousins:** none

## SN-0200 — A Receipt Pin Must Resolve Live, or It Is Not a Receipt (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/EVIDENCE-IDENTITY/SN-0200/IB-SMART-NOTE-20260930-sn0200-receipt-pins-must-resolve-live.md`
**Truth state:** CANDIDATE · **Type:** VERIFICATION_METHOD · **Ingested:** 2026-10-04T23:50:18Z

> publish only resolvable pins; correcting lane names the true SHA aloud on the board; judge the moved head; read status strings mechanically

**Evidence:** {"broken_pin": "#554 5955380295 cited v5.1 pin 090e6762; #554 5955640475: 090e6762 does not resolve via GitHub API; verdict-answer commit is 15481922 \u2014 treat as receipt reference", "mechanical_reads": "PR #1328 mergeable_state unstable = checks pending/failing, not a verdict; judging seat works
**Cousins:** none

## SN-0212 — Recompute the Ledger from the Artifact, Then Fail-First It (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/CI-TRIAGE/COUNT-LEDGER-STALENESS/SN-0212/IB-SMART-NOTE-20260930-sn0212-recompute-ledger-from-artifact-fail-first.md`
**Truth state:** CANDIDATE · **Type:** VERIFICATION_METHOD · **Ingested:** 2026-10-04T23:50:18Z

> recompute ledger entries from the artifact via independent paths, then fail-first the defective entry to prove the gate is non-vacuous before trusting the green

**Evidence:** {"board": "#554 5957529443 (NAYA 4 SELF-BUILD LOOP SIGN-OUT, 2026-10-02 17:15:29Z)", "defective_entry": "20260930052000 recorded sha256 d64a5a05\u2026/4828B/20 stmts; actual a7660ab4a6f2338bf2b9cbc4436793fc5ec13ac601257ff601dccc7c1c45f09c/6300B/12 stmts", "gate": "merge still parked for Human Direct
**Cousins:** SN-0061, SN-0062, SN-0100

## SN-0216 — Verify at the Target Tree, Not at the Artifact (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-0216/IB-SMART-NOTE-20260930-sn0216-verify-at-target-tree-not-at-artifact.md`
**Truth state:** CANDIDATE · **Type:** VERIFICATION_METHOD · **Ingested:** 2026-10-04T23:50:18Z

> an independent verifier recomputes a repair PR's claim against the live target tree (recursive tree API), never against the PR's own blobs — the PR's blobs are the claimant's evidence, the verifier's evidence is the target; and the checker must be proven non-vacuous by going red on the broken tip

**Evidence:** {"board": ["#554 5962923437 (Naya 4 self-build sign-in, 2026-10-02 23:12:28Z)", "#554 5962925708 (Naya 4 self-build sign-out, 2026-10-02 23:12:44Z)", "#554 5963063092 (Naya 2 relay spot-verification, 2026-10-02 23:27:13Z)"], "ci": "test SUCCESS (incl. drift check) + chain-readiness-gate SUCCESS on 0
**Cousins:** SN-0043, SN-0058, SN-0061, SN-0091

## SN-0217 — Compare Semantic Identity, Not Raw Bytes (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-0217/IB-SMART-NOTE-20260930-sn0217-compare-semantic-identity-not-raw-bytes.md`
**Truth state:** CANDIDATE · **Type:** VERIFICATION_METHOD · **Ingested:** 2026-10-04T23:50:18Z

> when comparing two independently regenerated artifacts to decide same-repair-class, verify semantic identity (basis SHA + inventory + file set + counts) via the tool's own normalizers — never raw blob-byte comparison, because volatile stamps (generated_at) roll at UTC midnight and false-positive as difference

**Evidence:** {"battery": "hidden_files/batt-2216 @ exact SHA: pytest 550 passed / 3 skipped / 0 failures; brain index --check RED exit=1 (drift: 5 daily reports 2026/09/27-10/02, ledger 29->34, inventory 172->177)", "board": ["#554 5966378212 (brain-build watchtower, 2026-10-03T06:30:45Z)"], "pin": "main 5b68f8d
**Cousins:** SN-0100, SN-0052, SN-0059, SN-0177, SN-0061

## SN-0224 — Type-Check the Shipped Artifact at Its Full Scope — A Passing Harness Only Proves What It Executes (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-0224/IB-SMART-NOTE-20260930-sn0224-prove-the-shipped-artifact-at-full-scope.md`
**Truth state:** CANDIDATE · **Type:** VERIFICATION_METHOD · **Ingested:** 2026-10-04T23:50:18Z

> edge-function repairs are proven by (1) deno check on the full shipped file, (2) Deno-executed behavior matrix on the shipped functions, (3) an order control for declaration-before-use; the repair is always re-tested as its own suspect — a green harness proves only the scope it executes

**Evidence:** {"board": ["#554 5968578468 ([NAYA 4][SELF-BUILD LOOP][SIGN-IN \u2192 SIGN-OUT] \u2014 H13 Deno proof + repair-of-repair, 2026-10-03 11:08:34Z)"], "defect": "lawDecision referenced at line 464 before const declaration at line 490 (immutableVerificationRecord \u2192 IMMUTABLE_COMMIT_RECEIPT_SNAPSHOT 
**Cousins:** SN-0059, SN-0061, SN-0072, SN-0076, SN-0100

## SN-0225 — A Classifier That Reads Strings Can Be Gamed by Strings — H8-7 CONFIRMED BUG: Lesson-Text Regex Gamable at Lock-In (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/CLASSIFICATION-INTEGRITY/SN-0225/IB-SMART-NOTE-20260930-sn0225-a-string-keyed-classifier-is-gamable.md`
**Truth state:** CANDIDATE · **Type:** VERIFICATION_METHOD · **Ingested:** 2026-10-04T23:50:18Z

> a string-keyed classifier is a gamable classifier: syntax cannot certify semantics; at a trust boundary, classification must be meaning-keyed (governed classifier) or eliminated (predeclared registry); falsify classifiers with adversarial negatives (negation / foreign-context / asserted-false, trigger string preserved) while holding positive controls green

**Evidence:** {"board": ["#554 5971545143 ([NAYA 4][SELF-BUILD LOOP][SIGN-OUT] \u2014 H8-7 CONFIRMED BUG: lesson-text regex is gamable, 2026-10-03 17:16Z)", "#554 5971651452 (Naya 2 relay \u2014 live-verified extraction pin 06d913f537 @ 5b68f8dc, no drift; stale closure corroborated)"], "control_matrix": "positiv
**Cousins:** SN-0061, SN-0072, SN-0083, SN-0091, SN-0224

## SN-0226 — Re-verify the Gap at the Pin Before Designing the Repair — H15 Half-2 Closed as STALE (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-0226/IB-SMART-NOTE-20260930-sn0226-close-the-gap-as-stale-before-designing-the-repair.md`
**Truth state:** CANDIDATE · **Type:** VERIFICATION_METHOD · **Ingested:** 2026-10-04T23:50:18Z

> re-verify every suspected gap against the current pin before spending repair-design effort — extraction at the exact blob + hit counts, never memory of what the code 'didn't have'; a phantom gap repaired anyway is a duplicate repair, a phantom gap left open is a standing false claim

**Evidence:** {"asymmetry": "same cycle: H8-7 REAL (pin-verified, repair designed) vs H15 half-2 STALE (pin-verified, no repair designed) \u2014 recorded differently, on purpose", "board": ["#554 5971545143 ([NAYA 4][SELF-BUILD LOOP][SIGN-OUT] \u2014 H8-7/H15 cycle, 2026-10-03 17:16Z: H15 half-2 CLOSED AS STALE)"
**Cousins:** SN-0043, SN-0061, SN-0122, SN-0177

## SN-0231 — Repair by Predeclared Registry — Fail-Closed, Text-as-Proposals, Declared-Class-or-UNKNOWN (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/10/03/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/CLASSIFICATION-INTEGRITY/SN-0231/IB-SMART-NOTE-20261003-sn0231-repair-by-predeclared-closed-registry.md`
**Truth state:** CANDIDATE · **Type:** VERIFICATION_METHOD · **Ingested:** 2026-10-04T23:50:18Z

> at trust boundaries prefer a predeclared closed registry over a smarter parser: text proposes, the registry disposes, everything else is UNKNOWN

**Evidence:** {"bug": "SN-0225 \u2014 deriveGraphApplicability regex gamable (3 FP + 1 FN, Deno 2.9.7)", "decision": "#554 comment 5973006019 (2026-10-03T20:07:06Z) \u2014 H8-7 repair design decision at sign-in, main pin 5b68f8dc", "rejected_alternative": "governed classifier (smarter parser) \u2014 rejected: kee
**Cousins:** SN-0225, SN-0226, SN-0095, SN-0083, SN-0221

## SN-0232 — The Test That Pins the Bug Verbatim Is the Defect — Re-pin the Test to the Governed Contract (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/10/03/SYSTEM-INTELLIGENCE/CI-TRIAGE/TEST-DEFECT-CLASSIFICATION/SN-0232/IB-SMART-NOTE-20261003-sn0232-test-that-pins-the-bug-is-the-defect.md`
**Truth state:** CANDIDATE · **Type:** VERIFICATION_METHOD · **Ingested:** 2026-10-04T23:50:18Z

> when a proven-correct repair collides with an old test, suspect the test first: if the test asserts exactly the behavior the bug report falsifies and the repair's controls are independently green, classify the test as the defect and re-pin it to the governed contract — never weaken the repair to fit a pinned test

**Evidence:** {"corroboration": "#554 comment 5973182115 (Naya 2 relay) \u2014 PR #1347 live-verified: open/non-draft/mergeable, head == branch ref, CI red = pre-existing base-pin drift only", "proof_shape": "deno check green on full shipped edge function; 14/14 Deno behavior matrix on shipped helper; non-vacuous
**Cousins:** SN-0225, SN-0231, SN-0072, SN-0118, SN-0061, SN-0224

## SN-0234 — IMPLEMENTED-NOT-PROVEN — When the Proof Step Is a Protected Live Write, Ship the Executable Packet Instead (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/10/03/SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/CLASSIFICATION-INTEGRITY/SN-0234/IB-SMART-NOTE-20261004-sn0234-implemented-not-proven-proof-packet-at-protected-boundary.md`
**Truth state:** CANDIDATE · **Type:** VERIFICATION_METHOD · **Ingested:** 2026-10-04T23:50:18Z

> when the remaining verification step requires an action you cannot take, never round up to PROVEN: classify IMPLEMENTED-NOT-PROVEN with the missing evidence named, and ship a fully executable proof packet (document-only, reversible) so the authorized lane can close the loop; boundaries route work, they don't halt it — advance everything to the line, package the crossing

**Evidence:** {"board": ["#554 5975652657 ([NAYA 4][SELF-BUILD LOOP][SIGN-OUT] \u2014 H3+H5 live-proof packet cycle, 2026-10-04T02:09:01Z)"], "deliverable": "full executable proof packet, document-only, reversible \u2014 zero boundary touch", "residual": "live behavioral proof \u2014 protected live write, lane ca
**Cousins:** SN-0231, SN-0226, SN-0061, SN-0083, SN-0232

## SN-0235 — Deployment Parity Is a Failure Class — Prove the Deployed Artifact Matches the Verified Package Before Changing Code (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/CI-TRIAGE/FAILURE-ATTRIBUTION/SN-0235/IB-SMART-NOTE-20261003-sn0235-deployment-parity-is-a-failure-class.md`
**Truth state:** CANDIDATE · **Type:** VERIFICATION_METHOD · **Ingested:** 2026-10-04T23:50:18Z

> when a live verification fails, classify before you code: first prove the deployed artifact is byte-equivalent to the artifact you verified — if not, the failure class is deployment parity and the fix is a redeploy, never a code change

**Evidence:** {"classification": "DEPLOYMENT PARITY / STALE PRODUCTION ARTIFACT \u2014 not a new code-design failure", "finding": "two contextual Mail seams navigate to stale /hub/smartmail-v1.2.html in production while the repaired package points both to mail.html", "next_action": "deploy the exact repaired arti
**Cousins:** SN-0061, SN-0174, SN-0233, SN-0059, SN-0065, SN-0099

## SN-0237 — Identical Failing Sets Across Heads Are Environmental Noise — Compare the Failing Set Before You Blame the Change or Run a Control (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/CI-TRIAGE/FAILURE-ATTRIBUTION/SN-0237/IB-SMART-NOTE-20261004-sn0237-failing-set-identity-across-heads.md`
**Truth state:** CANDIDATE · **Type:** VERIFICATION_METHOD · **Ingested:** 2026-10-04T23:50:18Z

> before triaging a diff or running a clean-main control on a red CI head, compare the failing check list against another head: byte-identical failing sets => environmental noise (inherited base defect or standing platform constant); cite the comparison head in the verdict

**Evidence:** {"comment": "#554 5979338448 (Naya 2 relay ack, 2026-10-04T11:11:55Z)", "failing_set": "test failure + 17 Workers-Build failures, byte-for-byte identical across heads", "heads_compared": "#1348 0ab1853e vs #1345 72165f9e", "verdict": "environmental noise: inherited brain-index drift + standing Worke
**Cousins:** SN-0059, SN-0097, SN-0174, SN-0235, SN-0236

## SN-0238 — Recompute the Index from the Live Tree, Not the PR Blobs — and Exclude Self-Referential Files by Design (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-0238/IB-SMART-NOTE-20260930-sn0238-recompute-index-from-live-tree.md`
**Truth state:** CANDIDATE · **Type:** VERIFICATION_METHOD · **Ingested:** 2026-10-04T23:50:18Z

> verify a regenerated index by recomputing from the source tree at the pinned commit (never the PR's own blobs); enumerate self-referential entries as explicit exclusions; always show the check fails without the repair

**Evidence:** {"comment": "#554 5980878678 (Naya 4 #1349 independent verification, 2026-10-04T14:09:17Z)", "non_vacuity": "drift check RED on main without the repair", "pr": "#1349 head eaf42693, pin bd03ec4f", "rebase_check": "receipt_basis_commit == tip, no rebase needed", "self_referential": "3 files omitted b
**Cousins:** SN-0043, SN-0058, SN-0061, SN-0233, SN-0236

## SN-0250 — Green Run ≠ Sound Registry — Assert Disk↔Registry Reconciliation in the Permanent Gate (2026-10-04)
**Source:** `BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION/SN-0250/IB-SMART-NOTE-20261004-sn0250-green-run-compatible-with-corrupt-registry.md`
**Truth state:** CANDIDATE · **Type:** VERIFICATION_METHOD · **Ingested:** 2026-10-04T23:50:18Z

> Source: #554 5982256280 §5 (2026-10-04T16:49:18Z, CODA 3): "recomputing every capture hash and reconciling against the registry: registry entries whose content_hash matches NO capture file on disk: SN-003 IB-SMART-NOTE-20260929-sn003-naya-continuation-engine, SN-004 IB-SMART-NOTE-20260929-sn004-shawn-standing-law-r2, SN-016 IB-SMART-NOTE-20260930-sn016-prime-judgment-rule. These three registry entries point at content that no longer exists on disk. The captures were edited after their entries we

**Evidence:** {"comments": ["#554 5982256280 \u00a75 (three stale pointers: SN-003/004/016 content_hash matches no capture on disk)", "#554 5982356143 \u00a71 (independent re-run confirmation, no duplicate SN ids yet)"], "method": "content_hash recomputed with the workflow's own formula for all 15 captures, recon
**Cousins:** SN-0062, SN-0213, SN-0078, SN-0247
