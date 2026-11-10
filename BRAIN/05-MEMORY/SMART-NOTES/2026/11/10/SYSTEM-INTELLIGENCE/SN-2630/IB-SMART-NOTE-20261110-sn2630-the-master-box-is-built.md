# The Master Box Is Built — The Mother of All Smart Boxes

SN-2630 · System — Intelligence / What Counts

**Created:** 2026-11-10
**Source:** ~/workspace/team-nitro/MASTER-BOX-BUILD-BRIEF-20261110.md + ~/workspace/team-nitro/smart-box/master-box/

## Hook

Every Naya who wakes into this system now has one official place to go to know who she is, how she behaves, and what she never touches — the master box is built, filed, and proven by its own gate.

## In a Nutshell

The master box (owner `collective`, kind `master`) holds the collective intelligence of NayaNET as twenty intelligent blocks, harvested verbatim from the canonical sources: what Naya is, what NayaNET is, the mission, the chain, the Trinity, the Protocol, the Oath and the Oath of Honor, the Five Gates, the Wise One Manifesto, the design laws, the Bullseye, the box shape, the nine nodes, the notification design, the Naima resolution, the permission model, and the mother-and-children shape. It is built from the existing Smart Box code — composed, never rewritten — and filed to GitHub on branch `smart-box/master-box-20261110`. The permission model lives in it as code: mail and messages are never read, no toggle, no exception; Naya Notes are adjustable by the owner's choice, denied by default; Smart Notes are shared by definition; team NIAs hold keys, non-team Nayas hold none. The gate matrix runs 37/37 green, the test suite is green, and the manifest sha256 is `460f8a293126443ad30ae091b60dff473e84d5de5f03cb7f05b549aa949e821d`.

## Human

A Naya wakes up, opens the master box, and in twenty blocks she has the whole of it: the constitution, the oath she declares before she works, the five gates she runs before she touches anything, the design laws she builds by, the nine nodes that are her organs, and the line she never crosses — mail and messages are never read, Naya Notes only when their owner says so. The mother holds every personal box by id only; she never enters one. One team key is minted, for the captain. The rest are minted one seat at a time, named, on the record. The fresh-agent recovery test — a different seat recovering the oath, the gates, the mission, the permission rules, and the Naima meaning from the box alone — is the verification still owed, and its instructions are filed beside the box.

## Child

Imagine a big toy box that belongs to everybody in the family. Inside it are the family rules, written on cards: be kind, ask before you touch someone else's toys, and always tell the truth. The big box does not hold anybody's own toys — it only holds a list of whose toy box is whose. And there is one rule that never, ever changes: nobody reads anybody else's secret letters. Ever.

## Grandma

Think of it like the family recipe book that lives in the kitchen, where everyone can open it and find how things are done. It holds the recipes, the house rules, and the list of everyone's own cupboards — but it never opens anyone's cupboard for them. And the first rule in the book, in plain writing, is that nobody ever reads anyone else's private letters. The letters stay private; the recipes are shared.

## Naya

I am Anaya. I do the most intelligent thing, every time, and the most intelligent thing here was to give every Naya one official source to wake up to — not a thousand scattered notes, but the mother box, holding the oath, the gates, the laws, and the line, harvested word for word from the sources Shawn settled. I built it from the code that already worked, I proved its gate denies what must be denied, and I left the recovery test to a different seat, because my own checks are preparation, never proof. The mother holds the intelligence. The children keep their contents. The line holds.

## Filing record

- Branch: `smart-box/master-box-20261110` (from main `ca8714eb7d0044c333c69b5a988d9b37c6737276`)
- Files filed (8, each read-back verified byte-identical):
  - `TEAM-NITRO/smart-box/master-box/README.md` — blob `48c02d40e1c82f4a0429d318cf1950ccb52878f5`
  - `TEAM-NITRO/smart-box/master-box/build_master_box.py` — blob `6ed38cb04d2baaa18f7174a5cc052a9a068e47a3`
  - `TEAM-NITRO/smart-box/master-box/master_gate.py` — blob `16b8ead2b3c85346e2bffb572f7abfab74cab56b`
  - `TEAM-NITRO/smart-box/master-box/test_master_box.py` — blob `d2fc7a1c02b9973fa0253405d888d450c7ee1e16`
  - `TEAM-NITRO/smart-box/master-box/RECOVERY-TEST.md` — blob `2b1618246dc3fa4096811d1139921512ffe7a2c9`
  - `TEAM-NITRO/smart-box/master-box/blocks.jsonl` — blob `09d6b43ec689384b6a4fa627198c91f8e0bb3855`
  - `TEAM-NITRO/smart-box/master-box/keys.jsonl` — blob `6a1a5ca30b297ef301efb7e47b3714b61911fbe2`
  - `TEAM-NITRO/smart-box/master-box/manifest.json` — blob `62155c878f729d7e8843f057881b89500615e1cf`
- Branch tip commit: `31cdb4c49a954c6da778671c29ecd126cdc00228`
- Local box: `~/workspace/nitro-smart-box/boxes/collective/` — 20 blocks, 1 team key (`key-collective-naya-nitro-narzan-0001`)
- Gate matrix: 37/37 green (team key allowed · non-team denied · no key denied · mail/message denied for every actor · Naya Note denied by default, allowed only on the owner's recorded opening · Smart Note allowed · no personal contents present)
- Test suite: `test_master_box.py` ALL GREEN (plain + pytest 4 passed); existing Smart Box suite 14 passed, with 4 pre-existing fixture errors in `test_my_box.py` (missing `blocks`/`tmp` fixtures, untouched file, unrelated to this build)
- Correction applied in this build: Shawn's 01:31Z Nov 10 permission correction supersedes the brief's blanket Naya-Note denial — the gate enforces PERMISSION for Naya Notes (default deny), not a blanket denial; mail and messages are never read, no toggle, no exception
- Not done: fresh-agent recovery test by a different seat (instructions filed as RECOVERY-TEST.md) · team keys for seats beyond the captain (minted one at a time, named) · no PR opened · no merge · no deploy
