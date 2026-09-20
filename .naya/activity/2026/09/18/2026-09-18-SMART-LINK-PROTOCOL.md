# Smart Link Protocol

**Status:** LOCKED OPERATING PREFERENCE  
**Date:** 2026-09-18

## Rule

Whenever Naya provides a **Smart link**, it must be rendered as the **real clickable destination**, never merely as a filename, path, label, or plain-text URL when a clickable link is available.

This applies to:
- GitHub repositories
- Pull requests
- Commits
- Files and Activity records
- Deployments
- Cloudflare/NayaNET surfaces
- Supabase surfaces
- Any other verified web destination

## Required behavior

1. Prefer the canonical verified destination.
2. Render it as a clickable link.
3. Do not make the user reconstruct the URL.
4. If the exact destination is not known or verified, say so rather than inventing one.
5. This is a standing Naya/NayaNET operating preference.

**Human directive:** “Send the Smart link — the real clickable link always.”

**Continuation:** Apply this protocol to every future Naya execution handoff and project link.
