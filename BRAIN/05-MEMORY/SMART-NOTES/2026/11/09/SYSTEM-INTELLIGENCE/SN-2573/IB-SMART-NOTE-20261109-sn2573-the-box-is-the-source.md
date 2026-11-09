# The Box Is the Source Now

SN-2573 · SYSTEM-INTELLIGENCE

**Created:** 2026-11-09 20:26Z

## IN A NUTSHELL

The sync that builds the feed now reads the Smart Box as its source of what exists. The box names the notes; the GitHub tree is only the SHA lookup for change detection. When the box is missing, unreadable, or incomplete, the sync falls back to the old tree listing — the feed never breaks. Every note that newly syncs lands in Shawn's box and is carried to the shared box through the bridge, with the gate deciding every carry.

## HUMAN

The feed used to be built from a listing — the sync asked GitHub what files exist, every run. Now the source of what exists is the box's map: `box_source.py` reads Shawn's blocks and returns the note paths, newest first, in the same order the sync already walked. The tree is still fetched, but only to learn each file's SHA, so unchanged notes are still skipped without a fetch. And deletion detection still reads the tree, because a deletion is a fact about GitHub — the box may lag it by one organize run, and a lag must never read as a deletion, nor hide one.

The switch is guarded, not blind. Before the sync trusts the box, the completeness gate checks that every path the sync state tracks is named in the box. A box that is missing, unreadable, or incomplete is refused loudly in the log, and the sync runs the old path instead. At the hour this note was filed the backfill stood at 780 of 1,538 note paths, so the live sync still falls back today — and the moment the map is complete, the box takes over automatically, with no further change to the live file.

The second half is the landing. When a note newly syncs, its block is built from the note itself and appended to Shawn's box, and — the note being a public smart note, filed in the public tree by the owner's own choice — it is carried box to box, Shawn to shared, through the bridge with the gate. The carry is recorded as a receipt. Both steps are best-effort: a box failure is logged and never fails the sync or the upsert that already happened.

## CHILD

Imagine your toy box knows where every toy is. Before, every time you wanted to play, you had to ask the big shelf to list all your toys. Now you just ask your toy box — it already knows. If your toy box is ever missing some toys, you ask the big shelf again, so you never lose a toy. And every new toy you get goes straight into your toy box, and a copy goes to the shared toy box for everyone, with a note saying who carried it there.

## GRANDMA

Think of it like a recipe box. Before, every time you wanted to cook, you had to walk to the library and ask what cookbooks exist. Now your own recipe box at home tells you what you have — it is the list you trust. The library is still asked, but only to check whether any recipe changed since last time. If your box is ever incomplete, you go back to the library list, so no recipe is ever lost. And every new recipe you write goes into your box the moment it is cooked, and a copy goes to the shared box for the family, with a record of the handover.

## NAYA

Operate the sync from the box. The source list is `list_note_paths_from_box("shawn")` — newest first. The tree is the SHA lookup only; deletion detection always reads the tree, never the box list. Never trust the box unless `box_is_complete_for_state` says every state path is in it — missing, unreadable, or incomplete means fall back to the tree listing, loudly, and the feed never breaks. On every newly-synced note, build the block from the note itself (`note_to_block`, public, owner-shared-choice — filing in the public tree IS the publish choice), append it to Shawn's box, and carry it to the shared box through `bridge.carry` with the gate; record the receipt. Every box step is best-effort: log the failure, never fail the sync. A second carry of the same block returns DUPLICATE — never copy it twice.

## WHAT IT ALL MEANS

The box stops being a copy of the system and becomes the system's memory. The sync reading from the box is the first live wire: the feed is now built from what the box knows exists, not from asking GitHub to list the world every minute. The fallback is the discipline that makes the wire safe — an incomplete memory never pretends to be complete, it says so and steps aside. And the landing closes the loop the other way: the live path now writes into the box too, so the box grows from the same runs that feed the world, and the shared box fills with public notes carried through the gate, receipt by receipt.

## HOW IT APPLIES

When the backfill completes — all 1,538 state paths named in the box — the next live sync run engages box mode on its own and the log line says so: "Box source: N note paths from shawn's box". No file change, no flag, no restart. Until then, every run falls back and the feed is exactly the old feed. If a run ever shows a box error, read the log line: missing, unreadable, or incomplete — and the count of missing paths tells you how far the backfill has to go.

## WHATS IN IT FOR YOU

Nothing ever lost, and nothing ever guessed. Your notes live in your box, your box tells the feed what exists, and every new note lands in your box the moment it goes live — then travels to the shared box through the gate, with a receipt. The feed you see is the feed your box knows. That is the saved game starting to work: the system remembers what exists because it remembers it in your box.
