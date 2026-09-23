# Smart Feed — Activity Feed

**PURPOSE:** Area-scoped activity and handoff feed for the Smart Feed project.

## What belongs here
Record meaningful work on this area: sign-in/work context, discoveries, decisions, implementation actions, blockers, observations, verification receipts, state changes and successor handoffs.

## What does not belong here
This folder is NOT a second event store. Activity records/projections must trace back to canonical NayaPOWER events or explicitly identify a documented project-workspace record when no canonical event exists yet. Never invent an operational event merely to populate the feed.

## Standard record
Use: YYYY/MM/DD/YYYY-MM-DDTHH-MM-SSZ__TOPIC.md

Each record should state: timestamp; actor/session; area; what happened; why; canonical event/reference when applicable; evidence; current truth; what changed; next action; successor/handoff.

## Relationship
NayaPOWER canonical event → Main Activity → NayaNET project Activity → Smart Feed Activity

Team Naya communication remains separate under NAYA-TEAM/ACTIVITY-FEED.md and NAYA-TEAM/YYYY/MM/DD/.
