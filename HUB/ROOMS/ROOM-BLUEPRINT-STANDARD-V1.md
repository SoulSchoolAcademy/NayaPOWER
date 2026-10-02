# Room Blueprint Standard V1

Every room blueprint MUST define the screen before code.

Required sections:

1. **Purpose** — one sentence human job.
2. **Entry state** — what the user sees in the first 3 seconds.
3. **Desktop composition** — exact top-to-bottom / left-to-right regions.
4. **Primary instrument** — the unique object that makes this room useful.
5. **Controls** — every visible button/control, placement, and why it belongs there.
6. **Data contract** — what canonical data the room consumes and from whom.
7. **States** — loading, empty, ready, blocked, unauthorized, not verified, verified, error, offline, unknown.
8. **Cross-room handoffs** — exact destinations and object identity rules.
9. **Naya behavior** — what contextual help is useful here.
10. **Mobile transformation** — how the composition changes without becoming generic.
11. **Accessibility** — keyboard/focus/labels/zoom.
12. **Visual law** — room theme, density, depth and hierarchy.
13. **Acceptance journey** — click-by-click human test.
14. **Do not** — room-specific anti-patterns.
15. **Proof** — what evidence demonstrates the room works.

No room is implementation-ready until its blueprint is complete enough that a cold builder can reproduce the intended interface without inventing layout, controls, state, or feature scope.
