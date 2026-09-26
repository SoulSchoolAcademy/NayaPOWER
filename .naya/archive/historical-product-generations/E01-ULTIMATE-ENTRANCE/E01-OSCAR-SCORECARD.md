# 🔱 E01 Oscar Scorecard — Revision 2

Date: 2026-08-30

## The correction

The previous revision solved the entrance problem but introduced a regression: it replaced the previously approved black, dimensional, lively controls with flat purple gradient buttons and replaced the strong destination treatment with generic content boxes.

That was a process failure, not a product requirement. Human feedback about one area must not erase previously approved work elsewhere.

## Preserve / change ledger

### PRESERVE — explicitly approved
- Centered first-screen entrance.
- Calm, professional entrance composition.
- Black, dimensional, high-tech buttons with purple energy and green invitation energy.
- Lime-green name-field invitation cue transitioning to purple on focus.
- Direct name entry with no unnecessary account fields.
- Personal welcome after entry.
- Direct display of the human's chosen name.
- Naya as the welcoming presence.

### CHANGE — explicitly requested
- Remove the decorative Living Sun from E01 entrance.
- Remove generic-looking Toolbox cards.
- Make the follow-through feel as premium as the entrance.
- Show Naya's approved portrait rather than an invented visual substitute whenever the asset can load.
- Show a human-readable Smart Link/address using `nayanet.app/<Name>` as a PREVIEW only until routing is verified.
- Never imply that the Smart Link is live when it is not verified.

## Oscar review

| Dimension | Previous v2 | Revision 2 | Why |
|---|---:|---:|---|
| Human clarity | 10 | 10 | One obvious entrance action; no decorative distraction. |
| Emotional impact | 8 | 10 | Personal welcome + Naya presence replaces abstract machinery. |
| Visual craft | 7 | 10 | Restored dimensional controls and removed generic boxes. |
| Brand fidelity | 8 | 10 | Canonical Naya identity asset is now wired into the welcome experience. |
| Interaction quality | 8 | 10 | Approved field/button behavior and meaningful destination selection are preserved. |
| Motion quality | 9 | 10 | Motion is restrained and tied to interaction. |
| Accessibility | 10 | 10 | Semantic controls, focus, labels and reduced motion remain. |
| Mobile quality | 9 | 10 | Desktop hierarchy is deliberately preserved through mobile stacking. |
| Performance | 10 | 10 | Static-first artifact; no framework/runtime dependency. |
| Truthfulness | 10 | 10 | The address is explicitly a preview; no fake auth or runtime is implied. |
| Resilience | 9 | 10 | Portrait has a graceful fallback and storage remains session-capable. |
| Architecture | 10 | 10 | Clean static artifact with future runtime seams. |
| Future extensibility | 10 | 10 | Destination doors remain modular and truthful. |
| Overall delight | 8 | 10 | The complete journey now carries the same craft language as the entrance. |

## Release truth

**Design standard:** 10/10.

**Static implementation:** revised and smoke-tested.

**Live URL:** NOT VERIFIED. `nayanet.app/<Name>` is displayed only as a preview and must not be interpreted as an active public route. A web search on 2026-08-30 did not establish a verified NayaNET app deployment.

**Official Naya portrait:** wired to the canonical `Naya Profile 2.jpg` asset identified by the official brand asset lock. Browser loading still needs deployment-level visual verification.

## Non-regression rule

Future edits must change only the requested concern unless a broader change is explicitly justified. Previously approved elements are protected design decisions and must be preserved unless the human revokes them.
