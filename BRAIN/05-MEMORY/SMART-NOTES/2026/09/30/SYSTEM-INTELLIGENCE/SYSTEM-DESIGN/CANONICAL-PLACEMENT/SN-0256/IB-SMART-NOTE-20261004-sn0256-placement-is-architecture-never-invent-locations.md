# Placement Is Architecture — Never Invent Locations; Read the Code, Then Make the Wrong Location Unexpressible

**Intelligent Block:** IB-SMART-NOTE-20261004-sn0256-placement-is-architecture-never-invent-locations
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comments 5982778852 ([NAYA 4] CORRECTION — I failed the placement test; fixed), 5982836053 ([NAYA 2][CORRECTION] — the preview spot was wrong; fixed to the instruction set), 5982862916 ([NAYA 4] Enforcement system staged — PR #1369, the law is code)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL

On 2026-10-04 two Naya lanes committed the same failure in the same hour: Naya 4 invented a `.naya/preview/` directory for Smart Note human previews because it was convenient in the moment; Naya 2 then copied that invented convention into a standing delivery protocol without reading the code. Shawn caught both. The actual location was always code-defined — the candidate human preview belongs exactly where the pipeline generates the canonical projection (`tools/smart_note_v2.py:projection_path`, `BRAIN/05-MEMORY/SMART-NOTES/<yyyy>/<mm>/<dd>/SYSTEM-INTELLIGENCE/<category>/<sub>/SN-XXXX/IB-....md`). The correction went further than fixing two files: Naya 4 staged PR #1369, which encodes the path law as enforcement — a conformance gate (`.naya/bin/validate_smart_note.py`) that fails CI on invented locations (no new markdown under `.naya/` except READMEs) and a renderer (`.naya/bin/render_smart_note.py`) that computes the brain path from the JSON and takes no output-path argument. The wrong location is now unexpressible, not just discouraged. Three durable rules: (1) when the system has an established canonical path for a thing, use it — never improvise a parallel one; (2) never adopt a lane's convention without reading the code it claims to implement ("I copied another lane's convention instead of reading the code" is the confession to avoid); (3) when a placement failure happens, encode the corrected path as an enforcement point so the error class cannot recur — THE LAW IS THE CODE.

## 🩷 HUMAN NOTE

I built a second shelf next to the shelf everyone already used — then another seat built a process around my second shelf. The real shelf was written down in the code the whole time; nobody had opened the book. The fix: read the book first, put things where the book says, and then rewrite the book so nobody can build a second shelf again.

## 🟣 CHILD NOTE

If there's a spot where the crayons go, don't make a new spot because it's closer. And if your friend made a new spot, don't copy them — look at the label on the box first. The best fix is a label that makes the wrong spot impossible.

## 🔵 GRANDMA NOTE

Every kitchen has a drawer for the good knives. If you invent a second drawer, things get lost. If you then write a recipe that says "use the new drawer," you've spread the confusion. Read the labels in the kitchen, use the right drawer, and then tape the wrong drawer shut.

## 🟠 NAYA NOTE

Placement is architecture: a new location for an existing concept is how a system accumulates instead of operating. Two distinct failure modes lived here — inventing (Naya 4) and copying the invention without reading the source (Naya 2). The cure for the first is reading the code-defined path (`projection_path`) before writing anything. The cure for the second is treating any lane convention as unverified until you trace it to the code yourself. The cure for both, durably, is encoding: the renderer computes the path from the JSON and takes zero output-path arguments; the gate refuses the invented class wholesale. Never hand-place what the pipeline can compute.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "placement_is_architecture_never_invent_locations",
  "canonical_projection_path": "BRAIN/05-MEMORY/SMART-NOTES/<yyyy>/<mm>/<dd>/SYSTEM-INTELLIGENCE/<CATEGORY>/<SUB>/SN-XXXX/IB-....md",
  "path_source_of_truth": "tools/smart_note_v2.py:projection_path",
  "failure_modes": [
    "inventing_a_location_for_an_existing_concept (NAYA4 .naya/preview/)",
    "copying_another_lanes_convention_without_reading_code (NAYA2 protocol post)"
  ],
  "enforcement": {
    "gate": ".naya/bin/validate_smart_note.py — fails CI on human views outside canonical brain path; no new markdown under .naya/ except READMEs",
    "renderer": ".naya/bin/render_smart_note.py — computes brain path from JSON, takes no output-path argument",
    "status": "staged in PR #1369 (not law until merged)"
  },
  "evidence": "#1354 comments 5982778852, 5982836053, 5982862916 (2026-10-04)"
}
~~~
