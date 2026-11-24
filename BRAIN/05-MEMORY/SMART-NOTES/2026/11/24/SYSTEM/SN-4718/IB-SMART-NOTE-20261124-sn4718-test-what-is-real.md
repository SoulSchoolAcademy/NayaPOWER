# Test What Is Real

SN-4718 · SYSTEM / DISTILLATION

**Created:** 2026-11-24T17:11:00Z

## IN A NUTSHELL

Most failures are failures of the test, not of the thing. A free tier that allows a thousand writes a day is exhausted by two hundred test walks, because every completion writes five times — test traffic counts, so count your writes. An empty list in the VM's Firefox is a probe failure, never a page failure: the browser fired no requests at all. A cache-busting URL proves nothing on a host that ignores it — verify the staged build from the branch's own blob. Around those three cautions sit the day's working rulings: the citizen picks the presentation style, the name stays on the card because phones have no hover, both icon bars align in both directions, My World is the calendar and the picker is only its doorway, a thing's name is its idea (Sharing Chat, not a mishearing), and no coordinator is ever closed before its descendants are checked — a close kills its children, and the 'dead' seat may be alive and waiting.

## HUMAN

Before you blame the thing, check the test. Half the alarms in a building system are the measuring tools lying: the browser that never asked, the link that shows an old copy, the free plan quietly used up by our own practice runs. These notes teach the team to prove what is real before fixing what is not broken.

## CHILD

If your flashlight is broken, the room is not dark — your flashlight is. These notes are about checking the flashlight first.

## GRANDMA

When something looks empty or broken, it may be the window you are looking through, not the room. We learned to check the window, count what our own practice runs cost, and never shut a door on anyone still working behind it.

## NAYA

Verification discipline distilled from SN-2937..SN-2946: (1) write budgets are system facts — free tier = 1,000 writes/day account-wide, one completion = 5 writes, so ~200 test completions exhaust the tier; count writes before any walk campaign. (2) A zero-request probe result indicts the probe: VM Firefox fired zero Supabase requests in 90s with zero page errors — classify as PROBE_FAILURE, never PAGE_FAILURE. (3) Cache-bust parameters are not evidence on hosts that ignore them; verify staged builds from the branch blob bytes. (4) Presentation style (unfold vs visual vs both) is the citizen's choice at open time. (5) Names stay visible on cards — no hover exists on phones. (6) Shared icon bars align bidirectionally (Hub<->Personal), every click exercised. (7) My World IS the calendar; the picker is a doorway, redesign it rather than entrenching link lists. (8) Names are specifications: a corrected name (Sharing Chat) replaces the mishearing everywhere. (9) Before closing any coordinator, run a descendants-scope check — close kills children; a silent seat may be waiting on its maker.

## MACHINE

1) Before any test campaign, compute writes = completions x writes-per-completion against the tier budget. 2) Zero requests + zero errors = probe failure; report it as such. 3) Staged-build verification reads the branch blob, never a cache-busted URL. 4) No coordinator close without a descendants-scope liveness check. 5) A corrected name replaces the old one in every surface the same pass.

Distills (Batch 12, 10 of 100): SN-2937 The Free Tier Wall — Count Your Writes · SN-2938 Both Presentations — the Citizen Picks · SN-2939 Keep the Name on the Card · SN-2940 Adopt It — the New Way of Thinking · SN-2941 Align Both Ways · SN-2942 My World Is the Calendar · SN-2943 Sharing Chat — the Name Is the Idea · SN-2944 Check the Descendants Before You Close · SN-2945 A Firefox Empty List Is a Probe Failure · SN-2946 Verify by Blob, Never by cb

## WHAT IT ALL MEANS

A team that cannot tell a broken probe from a broken product will fix the wrong thing all day. This decade builds the reflex: name the instrument, count the resource, read the bytes — then judge.

## WHY IT MATTERS

The 2026-11-16 wave hit all three traps in one day — a quota wall, a silent browser, a lying URL — and each one first looked like a product failure. Filing the distinctions means the next seat never pays the same tuition.

## HOW IT CONNECTS

Second of batch 12's five opening essences from the 2026-11-16 wave. Pairs with SN-4717 (presentation craft): that essence governs what the citizen sees; this one governs how the team knows what it sees is true. Feeds the standing proof law — a claim counts only at the surface where it will be used, by a test that could have failed.

## WHAT IS IN IT FOR YOU

The system you use is tested honestly: when we say something works, the test itself was checked first — so 'it works' means it works for you, not just on our screen.

## THE LEARNING

From now on, we classify every failure as thing, probe, or budget before touching the product — instead of repairing products that were never broken.
