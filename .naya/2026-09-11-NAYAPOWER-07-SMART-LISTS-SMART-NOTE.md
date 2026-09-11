# 07 — SMART LISTS

## 1. IN A NUTSHELL

Smart Lists are the user's intelligent organization layer for grouping and categorizing Smart Notes and, where the architecture supports it, other connected intelligence such as people/connections.

A Smart List lets a person turn a growing stream of Smart Notes into intentional collections that are easy to find, revisit, use, share, and connect to other parts of NayaNET.

Smart Lists are not another storage silo. They are an organization and access layer over existing intelligence.

Examples:
- Favorites
- Saved Smart Notes
- A project
- A topic
- A course or learning collection
- Ideas to revisit
- Important decisions
- A research collection
- A collection prepared for sharing
- A group of notes associated with particular people or a Smart Space

The central promise is simple:

**Don't make the human scroll through hundreds or thousands of intelligence events to find the things they intentionally kept. Let them organize what matters.**

## 2. HUMAN

A person may encounter valuable Smart Notes throughout the Intelligence Feed. Some are worth keeping close. Some belong together. Some become part of a project. Some should be saved for later. Some may eventually be shared with people or a Smart Space.

Smart Lists gives the human control over that organization.

A useful basic experience is:

1. See a Smart Note in the Feed.
2. Save it.
3. It appears in the user's saved collection.
4. Mark it as a Favorite when appropriate.
5. Select one or more saved notes.
6. Add them to an existing Smart List or create a new one.
7. Name and organize the list.
8. Search the user's lists or notes.
9. Open, remove, reorganize, or delete items/lists as desired.
10. Use the organized collection elsewhere in NayaNET.

The human should never need to understand the underlying database or file structure.

Smart Lists should feel like creating folders only when folders are actually useful—but smarter, because the contents remain connected to the original intelligence, relationships, provenance, permissions, and current state.

## 3. CHILD

Imagine you have a giant toy box full of your best toys.

Your Smart Notes are all the toys.

A Smart List is a box you make for a special group:

- My Favorite Toys
- Space Toys
- Toys for Grandma
- My Building Project
- Things I Want to Play With Tomorrow

You can put the same toy in more than one box without making a second toy.

That's important: **a Smart List organizes the original Smart Note; it does not create a duplicate Smart Note.**

## 4. GRANDMA

Think of Smart Lists like having labeled baskets, recipe folders, address-book groups, and project folders—all working together intelligently.

You might have:

- Recipes I Love
- Christmas Ideas
- Family Information
- Garden Projects
- Things to Remember
- People From Church
- People I Want to Contact

The important part is that you decide how things are organized. NayaNET helps you find and connect them without making you dig through everything you've ever saved.

## 5. NAYA

Smart Lists are the human-controlled organization layer sitting between individual intelligence events and larger system actions.

Naya should help the human organize intelligence without taking away human control.

Naya can recognize useful relationships and suggest organization, but a suggested list is not automatically authoritative. The human can accept, reject, rename, move, remove, or delete it.

Naya should understand that:

- A Smart Note can belong to multiple Smart Lists.
- A Smart List is a collection/reference, not a duplicated copy of its notes.
- Favorites are a special intentional collection and should remain easy to access.
- Saved items should remain retrievable even when they are not in a named list.
- A user may create, rename, edit, search, reorder, archive, or delete lists.
- Removing a Smart Note from a list does not delete the underlying Smart Note.
- Deleting a Smart List does not automatically delete its underlying Smart Notes.
- Deleting a Smart Note should update every list that references it according to the system's deletion policy.
- List membership should respect privacy, authority, and sharing permissions.
- Sharing a list must not silently share private intelligence that the recipient is not authorized to receive.
- Lists should work with the rest of NayaNET rather than becoming isolated containers.

Naya may ask or suggest:

> "You have six Smart Notes about this project. Want me to create a list?"

But suggestion is not silent action. Authorized automation may perform explicitly permitted organization; consequential sharing or access changes require appropriate authority and confirmation.

## 6. MACHINE

Smart Lists are references/collections over canonical intelligence objects.

Core relationship:

`SMART NOTE → LIST MEMBERSHIP → SMART LIST`

Multiple membership is allowed:

`SMART NOTE A → LIST 1`
`SMART NOTE A → LIST 2`
`SMART NOTE B → LIST 1`

The system should not duplicate the Smart Note merely because it appears in multiple lists.

### Core Smart List object

A Smart List should have at minimum:

- stable list ID
- owner / authority scope
- name
- description or purpose when useful
- created_at
- updated_at
- membership references
- ordering metadata when manual order matters
- privacy / visibility scope
- sharing state
- status such as active / archived where supported
- provenance for system-created or suggested lists

### Membership should be its own relationship

A membership record may need:

- list ID
- target Smart Note ID
- added_at
- added_by
- ordering / position
- optional membership metadata
- optional source/reason such as human-added, system-suggested, or rule-based

This preserves the distinction between the intelligence itself and the human's decision to organize it.

### Favorites and Saved

Favorites and Saved should be first-class retrieval experiences.

A useful model is:

`SMART NOTE → SAVED STATE`

and independently:

`SMART NOTE → FAVORITE STATE`

A Favorite is not necessarily the same thing as a named list.

The interface may expose:

- Favorites
- Saved
- My Lists

A user can then turn selected Saved/Favorite items into one or more named Smart Lists.

### Search

Smart Lists should support search across:

- list names
- descriptions
- list contents
- Smart Note titles/essence
- relevant subjects/tags/relationships where available

Search should help answer questions such as:

- "Show me my project lists."
- "Find the list with the AI notes I saved last week."
- "Which lists contain this Smart Note?"
- "Find my favorite notes about learning."

### Organization

Useful actions include:

- create list
- rename list
- describe list
- add notes
- remove notes
- add multiple selected notes at once
- move/reorder notes when useful
- duplicate a list definition only when explicitly intended
- archive list where supported
- delete list
- search lists
- filter lists
- inspect related lists
- share/export where authorized

### Deletion semantics

Deleting a list is not equivalent to deleting the intelligence inside it.

Deleting a list should normally remove the collection and its membership relationships while preserving the underlying Smart Notes.

Deleting a Smart Note is a separate destructive operation and must account for every reference to that note.

### Connections and other entities

The architecture should remain deliberately extensible so Smart Lists can organize more than Smart Notes when there is a genuine user benefit.

Potential relationship:

`SMART LIST → CONNECTIONS`

For example:

- Family
- Friends
- Work
- Church
- Project Team
- Clients
- Community

However, this should not automatically collapse Smart Lists and Your Connections into one indistinguishable feature.

The current architectural direction is:

**Smart Lists = organization of things.**

**Your Connections = management and organization of people/relationships.**

They should be separate concepts that can interoperate through explicit relationships and actions.

This preserves clarity while allowing a person to connect:

`SMART LIST → SMART NOTES → CONNECTIONS → SMART MAIL → SMART SPACE`

or:

`CONNECTION GROUP → PEOPLE → SMART MAIL / SMART SPACE / SHARED INTELLIGENCE`

The final UI may present these together when that creates a simpler experience, but the underlying concepts should remain distinguishable.

## 7. LEARNING

Smart Lists create organizational intelligence.

Without organization, a growing Feed becomes increasingly difficult to use. Search helps retrieve individual items, but intentional collections preserve human structure and purpose.

Smart Lists allow the system to learn useful organization without changing the underlying intelligence.

The compounding relationship is:

`EXPERIENCE → SMART NOTE → SAVE/FAVORITE → SMART LIST → RETRIEVAL → APPLICATION/SHARING → OUTCOME → NEW INTELLIGENCE`

Lists can also reveal patterns:

- recurring projects
- repeated interests
- important themes
- frequently revisited knowledge
- unfinished work
- collections that may deserve a Smart Space
- notes that repeatedly appear across projects

These patterns may become intelligence, but **list membership alone is not proof of a learning event**.

The system must not infer a durable lesson merely because a human grouped several notes together.

## 8. ULTIMATE MEANING

Smart Lists turn **remembering** into **intentional organization**.

The Intelligence Feed is where intelligence flows.

Smart Notes preserve meaningful intelligence.

Smart Lists let the human say:

**"These belong together because they matter to me for this reason."**

That is valuable intelligence about the user's intent.

Smart Lists prevent the Intelligent Hub from becoming a giant pile of brilliant information that is technically searchable but practically difficult to use.

They create an intentional layer between:

**WHAT HAPPENED → WHAT MATTERS → HOW I ORGANIZE IT → WHAT I DO WITH IT**

## 9. HOW IT CONNECTS

Smart Lists should connect naturally across NayaNET:

`INTELLIGENCE FEED`
`↓`
`SMART NOTES`
`↓`
`SAVE / FAVORITE`
`↓`
`SMART LISTS`
`↓`
`SEARCH / ORGANIZE / RETRIEVE`
`↓`
`SMART MAIL / SMART SHARE / SMART SPACES / CONNECTIONS`
`↓`
`APPLICATION / COLLABORATION / OUTCOME`
`↓`
`NEW SMART NOTES`
`↓`
`COMPOUNDING INTELLIGENCE`

Key relationships:

- **Feed:** source stream where Smart Notes are encountered.
- **Smart Notes:** canonical intelligence events that lists reference.
- **Today:** may surface important saved/favorite/list activity.
- **Reports:** may identify meaningful work or patterns associated with lists.
- **Intelligent Library:** provides enduring knowledge and navigation; Smart Lists provide personal organization.
- **Your Connections:** manages people/relationships; lists can connect to connection groups without making the concepts identical.
- **Smart Mail:** can use authorized connection groups or selected people to communicate.
- **Smart Spaces:** can receive selected lists or list contents when sharing is authorized.
- **Smart Share:** provides intentional sharing of selected intelligence.
- **Smart Ledger:** preserves relevant provenance, evidence, sharing, and verification records where required.
- **PIS/CIS:** lists are organization/access structures, not substitutes for canonical intelligence or collective intelligence.
- **Continuity:** lists can preserve project and personal carry-forward context.
- **Superbrain:** may use list structure as contextual signal, but must not mistake organization for verified knowledge.
- **Privacy by Choice:** list visibility and sharing must respect user-controlled privacy and authority.

## 10. HOW TO APPLY IT

### Ideal human flow

**SAVE**

A Smart Note can be saved from the Feed with one simple action.

**FAVORITE**

A user can mark especially important notes as Favorites.

**SELECT**

The user can select one or many Saved/Favorite notes.

**ADD TO LIST**

Choose an existing Smart List or create a new one.

**ORGANIZE**

Name, reorder, remove, search, and manage lists.

**USE**

Open a list and work with its notes. Depending on authorization, send/share the collection or selected notes to people, connection groups, or Smart Spaces.

### Example

A user has 200 Smart Notes from building a new project.

Instead of searching the Feed repeatedly, they create:

**PROJECT — NAYA POWER LAUNCH**

They add 37 relevant Smart Notes.

They also have:

**IMPORTANT DECISIONS**

and some of those same notes appear there too.

Nothing is duplicated. The original Smart Notes remain canonical; the lists simply provide useful paths to them.

Later, the user wants to share the project intelligence with three authorized collaborators in a Smart Space.

The system can use:

`SMART LIST → SELECTED INTELLIGENCE → AUTHORIZED CONNECTIONS → SMART SPACE`

without requiring the user to manually find and send every Smart Note again.

### Quality standard

A 10/10 Smart Lists experience should make it obvious:

- what is Saved
- what is Favorite
- what lists exist
- what each list is for
- how to create a list
- how to add/remove items
- how to search
- what happens when something is deleted
- what is private
- what can be shared
- how lists connect to the rest of NayaNET

It should be fast, visually clean, human-first, and powerful without becoming complicated.

## 11. WHAT'S IN IT FOR YOU?

**You stop losing valuable intelligence inside your own intelligence.**

Instead of scrolling through hundreds or thousands of Smart Notes, you can save what matters, favorite what matters most, group related intelligence, find it quickly, revisit it later, and use it when it becomes useful.

You control the organization.

Naya helps make it easier.

And because Smart Lists connect to the rest of NayaNET, the intelligence you intentionally organize can become much easier to apply, collaborate on, share, and compound.

**Feed = what is flowing.**

**Smart Notes = what is worth remembering.**

**Smart Lists = what I intentionally keep together.**

**Library = what this intelligence means and where to learn more.**

---

# CANONICAL SYSTEM INTELLIGENCE — GITHUB ONLY

## Canonical Identity

**Subject:** Smart Lists

**Number:** 07

**System role:** Personal organization and collection layer over canonical intelligence.

**Primary purpose:** Allow humans to intentionally group, categorize, retrieve, and reuse intelligence without duplicating canonical Smart Notes.

## Architectural Contract

Smart Lists are collections of references to canonical objects, primarily Smart Notes. They are not an alternative canonical content store.

The same Smart Note may belong to zero, one, or many Smart Lists.

A Smart List must not become a hidden duplicate database of Smart Note content.

## Authority

Human authority controls intentional organization, deletion, visibility, and sharing subject to system-level safety, privacy, and authorization constraints.

Naya may recommend organization and may execute explicitly authorized organization actions.

A recommendation is not an authority grant.

## Truth / State Rules

- List membership is an observed or stored relationship.
- A system-generated suggested list is not equivalent to a human-created authoritative list unless accepted according to product rules.
- A list containing a note does not establish the truth of that note.
- Favorite status indicates user preference/importance, not factual verification.
- Saved status indicates intentional retention, not factual verification.
- List order indicates organization, not importance unless the product explicitly defines that meaning.
- Search ranking is retrieval behavior, not truth.
- List membership is not evidence of learning.

## Relationships

Supported conceptual relationships include:

- contains
- member-of
- favorite-of / favorited
- saved-by
- organized-by
- related-to
- used-for
- applies-to
- shared-with
- sent-to
- delivered-to-space
- derived-from
- evidenced-by
- verified-by
- supersedes

A list should reference stable object IDs rather than copying content whenever possible.

## Smart Lists vs Your Connections

This remains an intentional architectural boundary pending final product/UI decision.

**Smart Lists** primarily organize intelligence and other user-selected objects into collections.

**Your Connections** primarily organize people and relationships.

They should interoperate rather than become one ambiguous object.

A future unified collection model may allow a Smart List to contain different entity types, but the UX must make the object type and action semantics obvious.

Potential future model:

`COLLECTION → MEMBERS → ENTITY TYPE`

where entity types may include Smart Notes, Connections, projects, spaces, or other supported objects.

If implemented, this should be an intentional evolution rather than silently changing the meaning of Smart Lists.

## Sharing Boundary

Sharing a Smart List is not equivalent to granting unrestricted access to every object referenced by it.

Before sharing:

1. Determine the intended recipient(s) or Smart Space.
2. Check authority and privacy for each referenced object.
3. Exclude or request authorization for inaccessible content as product rules require.
4. Preserve provenance.
5. Make the resulting shared scope explicit.

A private note cannot become collective intelligence merely because it appears in a list that is shared.

## Deletion Contract

### Delete List

Default effect:

`LIST → DELETE LIST + MEMBERSHIP RELATIONSHIPS`

Underlying Smart Notes remain.

### Remove Note From List

Default effect:

`LIST MEMBERSHIP → REMOVE`

Underlying Smart Note remains.

### Delete Smart Note

Separate destructive operation. System must account for every list/reference before final deletion or tombstoning according to the global deletion policy.

## Search Contract

Search should support both:

- exact retrieval
- semantic retrieval

Ranking should consider relevance to the user's query, list title/purpose, note content/essence, recency where appropriate, user intent, and current authoritative state.

Search must not fabricate lists or memberships.

## Intelligent Suggestions

Naya may identify likely list candidates from:

- repeated project/topic references
- user behavior
- explicit naming
- repeated saves/favorites
- Smart Note relationships
- existing list patterns
- current project context

Suggestions should carry an appropriate state such as `SUGGESTED` until accepted when human confirmation is required.

## Compounding Intelligence Relationship

Smart Lists contribute to the larger compounding system through organization and retrieval:

`EXPERIENCE → SMART NOTE → ORGANIZATION → RETRIEVAL → APPLICATION → OUTCOME → VERIFIED LEARNING`

But organization itself is not learning.

The system must preserve this distinction to prevent false claims of intelligence improvement.

## Continuity

Project lists can serve as durable human-created carry-forward structures.

A list may provide a fast context surface for returning to a project without requiring the human to reconstruct the project from the Feed.

However, the list itself should not replace canonical state, project state, or verified intelligence where those systems exist.

## Smart List Quality Gate

A release-quality implementation should satisfy:

- [ ] Create list works.
- [ ] Rename works.
- [ ] Add one note works.
- [ ] Add many selected notes works.
- [ ] Remove membership works.
- [ ] Multiple-list membership works.
- [ ] Saved works.
- [ ] Favorites works.
- [ ] Search works.
- [ ] List contents are retrievable.
- [ ] Delete-list semantics preserve underlying notes.
- [ ] Note deletion updates list references correctly.
- [ ] Privacy boundaries are enforced.
- [ ] Sharing boundaries are enforced.
- [ ] Provenance survives organization and sharing.
- [ ] Lists interoperate with Connections, Smart Mail, Smart Share, and Smart Spaces where authorized.
- [ ] No duplicate canonical Smart Notes are created merely by list membership.
- [ ] Human can understand the feature without learning the underlying architecture.
- [ ] Runtime behavior is independently verified before being declared complete.

## Final Contract

**Smart Lists turn a growing stream of intelligence into intentional, human-controlled organization without fragmenting or duplicating the underlying intelligence.**

They are a core bridge between **remembering** and **using**.

They should remain simple enough for a child to understand, useful enough for everyday life, powerful enough for serious projects, and connected enough to operate naturally across the NayaNET intelligence system.

---

# ARCHITECTURE ADDITIONS TO PRESERVE FOR LATER

The current numbered subject sequence remains 01–24.

Two additional major documents are explicitly reserved for the end of the subject set:

**25. SCORECARDING + OSCAR**

**26. VALUE AND MATH**

These are intentionally not buried inside Smart Lists or another subject. They are to be developed as major architectural documents and integrated with the broader decision/value system.

The current constitutional distinction to preserve is:

**HARM IS NOT A NEGATIVE SCORE TO OFFSET. PROHIBITED HUMAN HARM IS ZERO / NOT AN OPTION BEFORE VALUE OPTIMIZATION BEGINS.**

The later Value and Math framework should distinguish constitutional exclusion from positive-value scoring and optimization.
