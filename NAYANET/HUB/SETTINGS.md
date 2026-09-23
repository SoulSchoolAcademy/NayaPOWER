# Settings

**Purpose:** give the human visibility and authorized control over their Hub boundary.

**Areas:** identity, privacy/publication, session, notifications/preferences, runtime status, data/export controls, verification.

**UI rule:** settings must expose actual state and real controls only. It must never claim authentication, persistence, or verification that the runtime does not expose.

**Backend mapping:** governed identity/session/settings APIs. Raw Supabase access remains outside the human-facing boundary.
