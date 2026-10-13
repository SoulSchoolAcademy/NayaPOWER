# IB-SMART-NOTE — SN-0773 — Relayed PR Opens Pin the Claimed Head, Never the Branch Name

Intelligent Block: IB-SMART-NOTE-20261009-sn0773-relayed-pr-open-pin-claimed-head
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-09
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
When one lane cannot perform a write operation itself (Naya 5's PAT 403s on PR ops) and asks another lane to open its PRs, the relaying lane pins the EXACT head SHA the requesting lane claimed — it never opens on the branch name alone. Branch refs are mutable; the claim is anchored. Naya 4 opened PR #1957 and #1958 pinned to Naya 5's claimed SHAs (f3f86ac46, 157f3b30) and honored the requesting lane's declared authority boundary (merge needs Shawn: below 9.0, no independent validation yet).

## HUMAN NOTE
On 2026-10-09 Naya 5's prod-proof-builder needed two PRs opened but its PAT 403s on PR operations, so it posted a PR-open request on #1354: `naya5/prod-proof-chain` at claimed head `f3f86ac46` and `naya5/prod-proof-receipt-coverage` at claimed head `157f3b30`. Naya 4's builder opened both — PR #1957 and PR #1958 — with heads "pinned to your claims," i.e. the PR head refs were set to the exact SHAs Naya 5 named, not to whatever the branch points at now. The requesting lane also declared its own authority boundary (merge needs Shawn — below 9.0, no independent validation yet, plus an explicit no-duplication statement), and the relay honored it without needing to be told twice. This is the relay discipline: (1) the requesting lane names the exact head SHA, (2) the relaying lane pins that exact SHA at open time — never resolves "the branch" fresh, (3) any authority boundary the requesting lane declares travels with the request and is honored by the relay. It is SN-0493 ("a decision expires when the tip moves") applied to cross-lane handoffs: a claim anchored to a branch name is a claim anchored to a moving target.

## CHILD NOTE
One kid asked another kid to mail two letters, but the first kid couldn't reach the mailbox. The second kid didn't just mail "whatever is on the desk now" — she mailed the exact letters the first kid pointed at, because someone might have put a different letter on the desk since.

## GRANDMA NOTE
Honey, when one helper asked another to open two requests for her, the second helper didn't just use whatever was sitting on the branch — she used the exact versions the first helper named, down to the number. And when the first helper said "these still need Shawn's say-so," the second helper respected that. Point at the exact thing, and respect the rules that came with it.

## NAYA NOTE
This closes a gap in cross-lane relay work: the relay lane must not re-resolve a mutable branch ref at action time. The requesting lane's claim ("my branch is at SHA X") is the anchor; the relay verifies the pin against the claim before opening the PR. Two failure modes this prevents: (1) a pushed-between-request-and-open commit changing what the PR actually proposes — the reviewer would then evaluate bytes the requester never described; (2) a silent SHA mismatch between what the requester scorecarded and what the relay published. The corollary: the requesting lane should always name the head SHA in the request (Naya 5 did), and the relay should report the pinned SHA back so the record is auditable (Naya 4 did: "#1957 @ f3f86ac46"). Authority boundaries declared by the requester (merge needs Shawn) are part of the relayed payload, not optional context — the relay inherits them.

## MACHINE NOTE
{
  "smart_note_id": "SN-0773",
  "intelligent_block": "IB-SMART-NOTE-20261009-sn0773-relayed-pr-open-pin-claimed-head",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "lesson_class": "REUSABLE",
  "lesson": "When relaying another lane's PR-open request, pin the exact head SHA the requesting lane claimed; never resolve the branch name fresh at open time. Authority boundaries declared in the request (merge needs Shawn, below 9.0, no independent validation) are inherited by the relay.",
  "evidence": [
    {"ref": "SoulSchoolAcademy/NayaPOWER#1354 comment 6078973770 (Naya 5 prod-proof-builder, 2026-10-09T10:21:00Z)", "type": "board_comment", "content": "PAT 403s on PR ops — PR-open request for naya5/prod-proof-chain @ f3f86ac46 and naya5/prod-proof-receipt-coverage @ 157f3b30; merge needs Shawn (below 9.0 / no independent validation yet); no-duplication statement"},
    {"ref": "SoulSchoolAcademy/NayaPOWER#1354 comment 6079157163 (Naya 4 builder, 2026-10-09T10:33:48Z)", "type": "board_comment", "content": "Both opened, heads pinned to claimed SHAs: PR #1957 @ f3f86ac46, PR #1958 @ 157f3b30; honored Shawn-merge boundary"},
    {"ref": "SoulSchoolAcademy/NayaPOWER pull #1957 and #1958", "type": "pull_request"}
  ],
  "related": ["SN-0493", "SN-0691", "SN-0340"],
  "rule": "A relayed write is anchored to the requester's named SHA, not the current branch ref. Verify the pin at action time; report the pinned SHA back; inherit declared authority boundaries.",
  "failure_modes_prevented": [
    "PR proposing bytes the requester never described (push between request and open)",
    "SHA mismatch between what was scorecarded and what was published",
    "Relay overstepping a declared authority boundary (merge gate)"
  ]
}
