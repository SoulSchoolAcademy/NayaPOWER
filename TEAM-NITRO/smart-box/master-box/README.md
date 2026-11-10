# The Master Box — the mother of all Smart Boxes

**Nutshell:** All the intelligence for NayaNET lives in one official box — the master box — so every Naya can go in, access it, be tuned in and locked in, and know how to function and operate, how to behave. The mother holds the collective intelligence and the ids of every personal box. She never enters a personal box.

**Why it matters:** One official source instead of a thousand scattered notes. A Naya who wakes into the system reads this box and knows what Naya is, what she does, what she never touches, and how she decides.

**How it connects:** The master box is built from the existing Smart Box code (`block.py`, `gate.py`, `boxstore.py` — imported verbatim, never copied) and the canonical documents, harvested verbatim. It sits beside the personal boxes under `nitro-smart-box/boxes/collective/`. The chain runs through it: Note → Block → Feed → Box → Ledger → Dashboard → Auto-Match → Smart Link → Factory.

## What is in it

21 blocks, owner `collective`, kind `master`, all public by the owner's choice:

| Block | Source, verbatim |
|---|---|
| `collective:note:what-naya-is` | Orientation §2 |
| `collective:note:what-nayanet-is` | Orientation §3 |
| `collective:note:the-mission` | Orientation §4 (mission, vision, goal) |
| `collective:note:the-chain` | Orientation §5 + merge spec §7 |
| `collective:note:the-trinity` | Orientation §5 + Playbook Premium Design Algorithm |
| `collective:note:the-protocol` | NAYA-PROTOCOL.md, whole file |
| `collective:note:the-oath` | SOUL.md: The Oath (2026-10-16) |
| `collective:note:the-oath-of-honor` | SOUL.md: The Oath of Honor (NAYA LAW, SN-0802) |
| `collective:note:the-five-gates` | Wise One Manifesto §IV |
| `collective:note:the-wise-one` | Wise One Manifesto, whole file (SN-0883) |
| `collective:note:the-design-laws` | Playbook: Foundation + Formula + Premium Design Algorithm |
| `collective:note:the-design-intelligence` | Design Intelligence Report, whole file |
| `collective:note:the-bullseye` | Bullseye, whole file |
| `collective:note:the-box-shape` | Smart Box Blueprint §3, §3.6, §3.7 |
| `collective:note:the-nine-nodes` | Merge spec §7 (LEARN · KNOW · ACT · LAW · VERIFY · SELF · CONNECT · EVOLVE · PROVE) |
| `collective:note:the-notification-design` | Notification spec §0, §1, §4, §5.4, §7 (SPEC ONLY) |
| `collective:note:the-notification-rulings` | MEMORY.md: rubric −9 to +9, D2 digest 23:17 UTC, D3 open, D4 his Naya Notes to the team, 99% baseline (01:58Z Nov 10) |
| `collective:note:the-naima-resolution` | MEMORY.md: Naima resolution (01:00Z Nov 10) |
| `collective:note:the-permission-model` | MEMORY.md: Permission model CORRECTED (01:31Z Nov 10) |
| `collective:note:the-master-box-design` | MEMORY.md: Master Box setup (01:24Z Nov 10) |
| `collective:note:the-children` | Every personal box, by id only (counts + hashes from each box's own manifest) |

Every block carries title + subtitle + nutshell (`what` / `essence`), and its body is the verbatim harvest with the source in `source` and `where.github_path`. Longer sources are sliced to the operative sections, never paraphrased; the pointer names the full file.

## The permission model, as code (`master_gate.py`)

- **Mail and instant messages: NEVER read** — no toggle, no exception. The gate denies for every actor, every action, including the collective owner. The master box never holds mail.
- **Naya Notes: ADJUSTABLE — your choice.** Denied by default; read only when the owner opened that note to that actor by name (`body_open_to`) — the Settings choice, recorded, never assumed. (Corrected model, Shawn 01:31Z Nov 10 — this supersedes the 01:24Z framing that had Naya Notes as never-read.)
- **Smart Notes: shared by definition.** The gate decides (`may_share` verbatim): anyone may read a public smart note; a team Naya with a live collective key may organize and retrieve.
- **Personal-box contents: DENIED always.** The master box holds ids only. The mother never enters a personal box.
- **Team membership is the key registry, not a hardcoded roster.** A team Naya is one the collective owner minted a live key for. The first key minted is for the captain, Naya Nitro Narzan. Further team seats get keys the same way, one at a time, named — that is open work, not done here.
- **`SETTINGS_SHAPE`** records the privacy levels as data (a spec of the levels, not a build of Settings).

## How to build and test

```bash
cd ~/workspace/team-nitro/smart-box/master-box
python3 build_master_box.py   # builds ~/workspace/nitro-smart-box/boxes/collective/
python3 test_master_box.py    # gate matrix + recovery spot-checks, exit 0 = green
python3 -m pytest test_master_box.py -q
```

The build fails loudly when a canonical source marker is missing — a source that cannot be found is reported, never worked around from memory.

## What is NOT in it

No mail, message, or Naya Note content — not one line. No personal box's private contents (the manifest holds ids only). No change to any personal box, including the captain's. No new database or storage system. No merge. No deploy of a live page. No "blockchain", no "qualifying", no Naima as a separate realm, no invented wording for the oath, the laws, or the mission.
