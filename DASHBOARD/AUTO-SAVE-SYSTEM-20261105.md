# AUTO-SAVE SYSTEM — Never Go Backwards
## Shawn's Order, 2026-11-05: "Everything in GitHub, auto-save it. Users need it too."

### THE PROBLEM
Work was lost because:
1. Changes were made to live workers directly, never saved to GitHub
2. No backup existed when something broke
3. Users' work in NayaNET has the same risk — if they build something and it's lost, that's catastrophic

### THE SOLUTION — TWO LAYERS

#### Layer 1: Builder Auto-Save (for Nayas building NayaNET)
**Rule: GitHub is the source of truth. Always.**

1. **Before any change:** Pull the current version from GitHub
2. **During work:** Save progress to GitHub every 15 minutes (or on every significant change)
3. **After work:** Commit to GitHub with a clear message, verify the commit landed
4. **Never:** Patch a live worker without first committing to GitHub
5. **Backup pattern:** Every deploy creates a dated backup file in GitHub (e.g., `index-20261105-backup.html`)

**Enforcement:**
- Deploy scripts check: "Is this version in GitHub?" If no, refuse to deploy
- Every worker deploy logs the GitHub commit SHA it came from
- Daily audit: list all workers, verify each has a matching GitHub source

#### Layer 2: User Auto-Save (for citizens using NayaNET)
**Rule: Users never lose work. Ever.**

1. **Every keystroke saves:** When a citizen types in any field, it saves to their account within 2 seconds
2. **Every action saves:** Creating a page, adding a note, changing a setting — saved immediately
3. **Version history:** Every save creates a version. Users can go back to any version from the last 30 days
4. **Offline protection:** If connection drops, work saves locally and syncs when back online
5. **No "Save" button needed:** Saving is automatic and invisible. The user never has to think about it.
6. **Visual confirmation:** A small "Saved ✓" indicator shows the save status, with timestamp

**Technical design:**
- Frontend: Debounced save on input (2s delay after last keystroke)
- Backend: Supabase row update on every save, with version history table
- Conflict resolution: Last write wins, but version history preserves all versions
- Recovery: "Restore" button in settings shows version history, one-click restore

### IMPLEMENTATION ORDER
1. ✅ Dashboard original saved to GitHub (2026-11-05)
2. Builder auto-save protocol documented (this file)
3. Deploy scripts updated to enforce GitHub-first
4. User auto-save: Frontend debounced save component
5. User auto-save: Backend version history table
6. User auto-save: Restore UI in settings

### SHAWN'S LAW
"Build everything in GitHub with auto-save so nothing is ever lost. You should never have to go back in time."
