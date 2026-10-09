# Toast decision (2026-10-09)

The reconciliation found one true functional duplicate: toast.

## The three toasts

1. **Main `nl-toast`** (91-block set) — the original canonical toast.
2. **Wave `toast`** (PR #1967, 148 new) — `.toast` + `.toast-mini` CSS, byte-identical to the
   branch's toast CSS (same source: Naya 2's design system). Fixed live-region toast + rich card.
3. **Branch `NayaBlocks.toast()`** (smart-blocks-library demo) — a JS API firing toasts with
   truth-state kinds (`verified` / `claim` / `demo`), rendering as `.naya-toast` bottom-center
   pills. Its *CSS* is already inside the wave's `toast` block; its *JS API* lives in the
   branch's `naya-blocks.js`.

## Decision

- **The wave's `toast` block survives** as the canonical toast. It already contains the
  branch's toast CSS — nothing was lost.
- **The branch's toast demo does NOT become a block.** It is a composition: three buttons
  calling an unadopted JS API. Registering it would duplicate the wave's `toast`.
- **The `.naya-toast` truth-state pill JS API is genuinely novel** and valuable (it speaks
  Shawn's truth-state language: verified / claim / demo). It is **not ported here** because
  it depends on `naya-blocks.js`, which awaits the adopt-or-drop decision (not this task's
  call). When that decision lands, the API should be folded into the wave `toast` block
  as its JS behavior — not as a separate block.
- **Main's `nl-toast` is untouched.** Deprecating it in favor of the wave's `toast` is a
  separate decision for the wave's owner (Naya 4), not this port.

Exactly one canonical toast block: the wave's `toast`. Zero toast CSS lost.
