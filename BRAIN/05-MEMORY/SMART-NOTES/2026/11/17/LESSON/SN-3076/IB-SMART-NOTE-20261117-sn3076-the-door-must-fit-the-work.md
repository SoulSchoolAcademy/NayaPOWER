# The Door Must Fit the Work

SN-3076 · LESSON / SMART NOTE

**Created:** 2026-11-17T22:37:00Z

## IN A NUTSHELL

A publishing door that cannot carry the work will be walked around, and the walk-around is where the record leaks. On 2026-11-14 the canonical door — learning_loop.py publish-note, the thin door over the canonical writer — was built to end the registry leak: capture first, page and registry entry and manifest in one motion, or nothing. But the door only accepted the persisted-block shape and rendered an emoji dialect whose machine note is a JSON dump, while the corpus's real production — the distillation batches, the door's own proof note SN-2832 — is flat captures rendered in the classic nine-section form, with coverage declared in a Distills line the census can parse. So batch 3, one hundred raw notes distilled to ten essences, honored the door's invariant in substance and published by hand, because the subcommand literally could not carry its pages. The cure is not to blame the batch or to move the corpus to the door's dialect; the cure is to teach the door the corpus dialect. From today the door speaks both shapes: the persisted-block path is untouched, and a flat classic capture now publishes through the same writer, under the same invariants, with its coverage line guaranteed parseable before anything is written.

## HUMAN

Think of a house whose front door was built for a different family's furniture. The couch cannot get through, so everybody carries the couch through the window — and after a while nobody remembers the door is the problem; they just blame the window-climbers for the scratches on the sill. The registry leak was exactly that: notes kept arriving without their records, and each arrival was treated as carelessness, when the real defect was that the one sanctioned door could not fit the furniture the family actually owns. You do not fix that by scolding the movers or by throwing away the couch. You measure the furniture, rebuild the doorway to fit it, and then — only then — the rule 'everything comes through the door' becomes a rule honest people can actually keep.

## CHILD

Imagine your school has one door for bringing in your projects, but the door is too small for the big poster boards everybody makes. So kids squeeze their posters through a window instead, and sometimes a poster gets lost and nobody wrote down whose it was. The teacher does not get mad at the kids. She measures the biggest poster, makes the door the right size, and paints a line on the floor that says: posters go here, names go here, all together. After that, every poster fits through the door, every name gets written down, and nothing gets lost. The door was the problem, so the door is what got fixed.

## GRANDMA

In my kitchen, dear, the recipe box only held little cards, but the family wrote its recipes on whatever paper was handy — the back of envelopes, a napkin from the good restaurant. For years the box stayed half empty and everyone said the family was careless with its recipes. Nonsense. The box was the wrong size for the family's real handwriting. So we got a bigger box, one that takes the envelope and the napkin just as they are, and we kept the one rule that matters: a recipe goes in the box the moment it comes home, with its name on it, or it does not count as saved. After that the box filled up all by itself, because the rule finally fit the way the family actually cooks.

## NAYA

Publish through the door — and keep the door fitter than the work. The rules now: (1) every Smart Note enters by learning_loop.py publish-note, in whichever of the two shapes the work honestly carries — persisted-block with its verify document, or flat classic capture; (2) a flat classic capture must be complete before the door moves: explicit SN claimed by census, all nine sections present, five whats-inside lines, taxonomy declared; (3) when a distillation essence publishes through the door, its coverage rides in the capture as structured data and the writer renders the Distills line itself, proving it parseable against the census grammar before writing a byte; (4) if real work ever again cannot walk through the door, the defect is the door's — fix the door in the same pass, name the deviation in the open, and never let a hand-rolled side path become the habit; (5) the invariants never move: capture first, fail closed on any name collision with different bytes, page and entry and manifest in one motion, hashes stamped by the writer, never by hand.

## MACHINE

The upgraded door, as machine-checkable rules: (1) publish-note accepts exactly two shapes — persisted-block (capture + verify) and flat classic (capture alone, schema naya.smart-note-capture.v2 with a flat intelligence object); any other shape is refused. (2) The classic path requires an explicit smart_note_id matching SN-\d{3,}; it never auto-allocates a number. (3) The classic page renders the classic section set — IN A NUTSHELL, HUMAN, CHILD, GRANDMA, NAYA, MACHINE, WHAT IT ALL MEANS, WHY IT MATTERS, HOW IT CONNECTS, WHAT IS IN IT FOR YOU, THE LEARNING — at BRAIN/05-MEMORY/SMART-NOTES/YYYY/MM/DD/<SEGMENT>/SN-NNNN/<IB>.md, and no emoji-dialect headers. (4) A declared distills payload renders as the MACHINE section's final paragraph, `Distills (Batch N, k of T): SN-XXXX <title> · ...`, and the writer verifies the line against the census grammar (distillation_machine.parse_distills regexes) before writing; a mismatch aborts the publish. (5) page_hash = sha256(page bytes); content_hash = sha256(canonical compact sorted JSON of the capture intelligence); both are stamped into the placed capture by the writer and bound into the registry entry; corpus_manifest_hash is re-stamped in the same transaction. (6) A capture name already owned by different bytes, an SN owned by a different block, or an IB already registered with different hashes each abort the publish with nothing registered. (7) Re-publishing the identical capture is idempotent: the existing entry is returned and the registry does not change.

## WHAT IT ALL MEANS

Underneath the format question sits P-152: the door obligation lives in the writer. A gate is not a rule posted next to a path; it is the shape of the only path. When the writer's shape and the work's shape disagree, the work wins every time — intelligence routes around friction the way water routes around a stone — and the system's records quietly stop being the truth about what exists. That is how a registry can be cured to zero unregistered pages in the morning and be leaking again by evening: the cure repaired the backlog while the door that produced the backlog stood unchanged. Formats are contracts between three parties — the writer who produces the page, the reader who retrieves it, and the census that counts it — and a contract only one party signed is not a contract. Teaching the door the corpus dialect signs it for all three: the same page the batch author writes is the page the census counts and the page the next Naya reads.

## WHY IT MATTERS

Without this cure, every future distillation batch faces batch 3's choice: publish by hand and keep the census honest, or use the door and publish pages the census cannot count — coverage invisible, backlog math wrong, retirement gates unprovable. Worse, the hand path becomes the habit, and each hand landing is a fresh chance for a page to exist without its capture or its entry: the exact leak that produced a 170-page unregistered band by 2026-11-17, cured that morning at real cost. A door that only works for work nobody does is not a control; it is a decoration next to an open window. The cost of the opposite — this cure — is one writer learning a second dialect. The cost of skipping it is the leak returning on schedule, forever, one reasonable deviation at a time.

## HOW IT CONNECTS

This note is the cure receipt for the deviation named in the Distillation Batch 3 execution record (2026-11-17): batches 1-3 (SN-2239-SN-2248, SN-2660-SN-2669, SN-3066-SN-3075) established the classic form and the Distills coverage grammar that tools/distillation_machine.py counts. SN-2832, the original publish-note proof, stands in the corpus in classic form with a flat capture — evidence the door's coded shape never matched its own proof. The governing principle is P-152 (the door obligation lives in the writer), and the same day's registry band cure (170 pages registered, landing 37c9961c) is the backlog half of the same repair: cure the pile, then cure the door that made the pile. The persisted-block path and its tests are untouched; the two shapes share one writer, one registry, one manifest.

## WHAT IS IN IT FOR YOU

Shawn, the distillation machine you ordered can now run end to end through the front door: a hundred notes in, ten essences out, every one of them counted by the census the moment it lands — no hand-built landings, no unregistered pages quietly piling up behind the work, no repeat of the 170-page band. And the next time any part of the machine cannot carry real work, the standing rule is written down where every Naya will read it: the defect belongs to the door, the fix belongs in the same pass, and the invariants — capture first, one motion, fail closed — never move.

## THE LEARNING

When real work walks around your door, do not blame the work — rebuild the door to fit it, in the same pass, and keep the invariants exactly where they were.
