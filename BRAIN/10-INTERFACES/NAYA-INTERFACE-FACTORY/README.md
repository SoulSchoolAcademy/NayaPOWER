# Naya Interface Factory V1

**Purpose:** One repeatable, AI-readable operating method for turning NayaNET Project Intelligence into premium, working, responsive Smart Apps.

## Start here

1. Read [OPERATING-BLUEPRINT-V1.md](./OPERATING-BLUEPRINT-V1.md) in full.
2. Restore the current project's PI, contracts, code, routes, data sources, and active work. Do not build from chat context alone.
3. Copy [PERSONAL-WORLD-EXAMPLE-BRIEF.json](./PERSONAL-WORLD-EXAMPLE-BRIEF.json) as the shape of a brief, then replace its example content with the target app's real PI and sources.
4. Validate the brief against [naya-interface-brief.schema.json](./naya-interface-brief.schema.json).
5. Run the semantic pre-build gate and resolve current canonical pieces using the live Factory store.
6. Build one complete vertical journey, render it at the required viewport matrix, test all states and actions, and obtain independent verification.
7. Use [naya-interface-quality-scorecard.v1.json](./naya-interface-quality-scorecard.v1.json) for the app-scoped review. It does not replace the NayaPOWER System Scorecard.
8. Read the concise [NAYA-BUILDER-PROTOCOL.md](./NAYA-BUILDER-PROTOCOL.md) when dispatching work to another Naya.

## Repository contents

| Artifact | Role |
|---|---|
| OPERATING-BLUEPRINT-V1.md | Full architecture, NIL vocabulary, Factory layers, team seats, visual grammar, screen laws, state contracts, responsive/accessibility/performance rules, build loop, and rollout |
| naya-interface-brief.schema.json | Draft 2020-12 JSON Schema for machine-readable app/screen briefs |
| PERSONAL-WORLD-EXAMPLE-BRIEF.json | Illustrative three-screen app brief; deliberately marks unresolved sources as unknown and capabilities as unverified |
| validate_naya_interface_brief.py | Standard-library semantic gate with optional exact piece-registry resolution |
| test_validate_naya_interface_brief.py | Positive and negative regression tests for the semantic gate |
| naya-interface-quality-scorecard.v1.json | Ten-dimension, app/interface-scoped evidence scorecard |
| NAYA-BUILDER-PROTOCOL.md | Copy-ready instruction protocol for a Naya assigned to interface work |

## Validate

From the repository root:

    python BRAIN/10-INTERFACES/NAYA-INTERFACE-FACTORY/validate_naya_interface_brief.py \
      BRAIN/10-INTERFACES/NAYA-INTERFACE-FACTORY/PERSONAL-WORLD-EXAMPLE-BRIEF.json \
      --pieces BRAIN/10-INTERFACES/SMART-FACTORY-CANON/pieces.json \
      --stage prebuild

Run the gate's regression tests:

    python BRAIN/10-INTERFACES/NAYA-INTERFACE-FACTORY/test_validate_naya_interface_brief.py

When the optional jsonschema package is installed, validate the complete schema/example pair:

    python -c "import json,jsonschema,pathlib; p=pathlib.Path('BRAIN/10-INTERFACES/NAYA-INTERFACE-FACTORY'); s=json.loads((p/'naya-interface-brief.schema.json').read_text()); b=json.loads((p/'PERSONAL-WORLD-EXAMPLE-BRIEF.json').read_text()); jsonschema.Draft202012Validator.check_schema(s); jsonschema.Draft202012Validator(s).validate(b); print('PASS')"

Use --stage release only after accessibility and other release evidence have actually been completed. A prebuild PASS means the brief is complete enough to plan/dispatch; it does not certify code, rendered design, security, live data, deployment, or production outcomes.

## Integration boundary

This V1 is an additive pre-build interface contract. It must run alongside the current Smart Factory build contract and existing 13 standard-feature gate. It does not modify templates, queue schema, deployment, or live runtime. Integrate it into factory dispatch only after compatibility tests prove that existing builds remain valid and that incomplete/unsafe briefs fail closed.

## Current evidence and limitations

The branch's initial QA used the current Smart Factory pieces.json from main, not a copied list. The worked brief resolved five reference pieces and passed the semantic prebuild gate. Eleven semantic regression tests passed. The JSON Schema passed Draft 2020-12 schema validation and validated the worked brief.

The worked brief intentionally remains a draft: it does not prove the Personal World app's runtime, data services, permissions, screen implementation, accessibility, mobile rendering, or release readiness. The example must be re-grounded in current PI before use for a real build.
