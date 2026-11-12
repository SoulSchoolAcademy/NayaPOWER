# Composable Templates — contract spec v1 (assembler v1.3)

Templates are composable starting points, not either/or picks. A customer
contract names MULTIPLE templates; the assembler merges them into one app —
the hub + rooms model: each template contributes its sections (rooms) and its
feature declarations, and they sync into a single build.

This spec is the MECHANISM for the composition law the contract already
declares (`composition`: multi_template, "hub plus rooms, all in sync").
It builds on that declaration — not a parallel system.

## Contract keys

`"templates"` — the composition request. Two grammars, shape-disambiguated:
- string: `"templates": "template-personal"` (single template; backward compat)
- list of strings: `"templates": ["template-personal", "template-business"]`
- The contract-page contracts keep `"templates"` as the display list of
  `[badge, name, desc]` triples — resolve_templates() passes those through
  untouched. Mixed shapes are a structured refusal.

`"template_shapes"` (optional, required when a composition is requested) —
the contract declares every template it composes. Design decisions come from
the contract, never the assembler:

```json
"template_shapes": {
  "template-personal": {
    "name": "Personal page",
    "sections": {
      "hero":  {"title": "Hero",  "blurb": "..."},
      "about": {"title": "About", "blurb": "..."}
    },
    "features": {"smart_mail": true, "smart_spaces": false}
  }
}
```

`"overrides"` (optional) — explicit per-section winner:
`"overrides": {"hero": "template-business"}`.

## Template ids

Canonical form: `template-<slug>`. The twelve canonical slugs come from the
builder's own template list (`smart-builder-v1.json` → `templates`):

| id | display name |
|---|---|
| template-personal | Personal page |
| template-business | Business landing |
| template-booking | Booking page |
| template-product | Product page |
| template-portfolio | Portfolio |
| template-event | Event page |
| template-menu | Menu / price list |
| template-community | Community hub |
| template-signup | Signup page |
| template-dashboard | Dashboard |
| template-creator | Creator page |
| template-cause | Cause page |

The resolver does NOT hardcode these — it resolves whatever `template_shapes`
declares. A contract may compose canonical ids, custom ids, or both.

## The merge law (deterministic)

1. **Sections union, in listed order.** Section names dedupe across templates;
   the merged section order is: first template's sections, then each later
   template's sections not already seen.
2. **Collision: first wins.** When several composed templates define the same
   section name, the FIRST template's content wins — unless `"overrides"`
   names another composed template for that section, which then wins.
3. **Features: prune wins.** Feature declarations follow the breaker grammar
   (`true` | `false` | `{enabled: bool}` | falsy = no opinion). Per feature:
   explicit `false` in ANY composed template disables it (the opt-out rule —
   the unchecked checkmark stays recorded in the contract as `false`, and the
   assembler's default-on three-state resolution reads explicit false as OFF);
   otherwise explicit `true` anywhere flips it on (still registry-gated);
   never mentioned anywhere means absent (the default-on policy decides). The
   merged result feeds the existing breaker pipeline, so the registry's
   fail-closed gate still binds every flipped feature.
4. **The contract wins over its templates.** Composed features fill only
   keys the contract's own `"features"` dict did not declare. (A features
   list — the contract-page grammar — cannot carry a composition: refusal.)

The resolved composition is recorded verbatim in the manifest under
`resolution.composition` (`templates`, ordered `sections` with per-section
`source`, merged `features`, `overrides_applied`). Section rendering for
customer apps belongs to the customer-app assembly stage — the contract page
has no customer-section slots, so v1.2 resolves, validates, and records.

## Refusals (fail closed — exit 2, structured JSON)

`empty_templates` · `bad_templates_shape` · `bad_template_id` ·
`missing_template_shapes` · `unknown_template` · `bad_template_shape` ·
`bad_section_shape` · `bad_overrides_shape` · `unknown_override_section` ·
`unknown_override_template` · `override_section_missing` ·
`bad_feature_declaration` · `features_shape_conflict`.

Unknown template ids and unknown override targets are never improvised —
an undeclared template is a refusal, not a guess.

## Determinism

`resolve_templates()` is a pure function of the contract: same contract bytes
→ same composition, byte for byte. The composition rides inside the build
identity (`build.id` hashes contract + index + template + assembler version).
