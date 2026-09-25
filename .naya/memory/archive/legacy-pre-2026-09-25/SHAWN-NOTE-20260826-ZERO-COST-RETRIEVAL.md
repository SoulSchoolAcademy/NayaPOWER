# SHAWN / SMART NOTE — THE ZERO-COST BRAIN IS GETTING REAL

We made an important product decision concrete: **do not wait for vectors to make the first customer Superbrain useful.**

The current GitHub-native brain now has a stronger zero-cost retrieval layer. It can combine exact matching, BM25, TF-IDF, metadata filters, query expansion, recency, authority/verification, and relationship traversal. That means a user can ask natural questions and the brain has multiple independent signals for finding the right memory instead of relying on one simple text search.

### Why this matters for customers
This gives us a practical 1.0 story:

**Give Naya the knowledge → activate the repository → search the knowledge intelligently.**

We can later add Supabase/vector infrastructure as a 2.0/scale upgrade without throwing away the foundation. Canonical memory stays the truth; vectors become an additional derived signal.

### What we are proving now
The new retrieval benchmark measures precision@5, recall@5, MRR, and token coverage. We also added deliberate failure behavior so nonsense queries do not manufacture arbitrary answers.

### Business principle
Start with what can be genuinely excellent at zero infrastructure cost. Use intelligence and architecture to maximize value first. Add paid/cloud infrastructure only when it creates enough additional value to justify itself.

### Customer activation direction
The next product problem is not "make customers configure a vector database." It is the opposite: **make knowledge activation nearly invisible.** The eventual target is a small set of official PDFs that can seed the user's brain automatically, with GitHub as the 1.0 delivery mechanism and hosted/vector infrastructure as a later convenience/scalability layer.

Current retrieval hardening is implemented but still pending authoritative CI on the exact current main.
