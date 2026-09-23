# Smart Lists — Activity Feed

Area-scoped working and handoff feed for Smart Lists.

Record meaningful work: sign-in context, discoveries, decisions, actions, blockers, observations, verification receipts, state changes and successor handoffs.

**NOT A SECOND EVENT STORE.** Area Activity is a scoped projection of canonical NayaPOWER operational events. Do not invent events merely to populate this feed.

Record path: YYYY/MM/DD/YYYY-MM-DDTHH-MM-SSZ__TOPIC.md

**Flow:** NayaPOWER canonical event → Main Activity → NayaNET Project Activity → Smart Lists Activity

Team Naya communication remains separate in NAYA-TEAM/ACTIVITY-FEED.md and NAYA-TEAM/YYYY/MM/DD/.