# Smart Block: `notification-center`

Notification list panel. Slide-over from the right, jewel-type rows, unread glow, live count.

- **Type:** overlays
- **Source:** built 2026-10-09 (gap build — no design-file source; designed in Naya's language)
- **CSS:** `notification-center.css`
- **Specimen:** `specimen.html`
- **States found:** .is-on, .is-unread, :hover
- **Dependencies:** notification-center.js, tokens.css

## Use it

1. Include `tokens.css` (once per page).
2. Include `notification-center.css`.
3. Copy the `.nc-backdrop` + `.nc` markup. Any `[data-nc-open]` element opens it.
4. Include `notification-center.js` for open/close, Escape, mark-read, and `nc:read` / `nc:closed` events.

## Selectors in this block

```
.nc
.nc-backdrop
.nc-backdrop.is-on
.nc-body
.nc-close
.nc-close:hover
.nc-count
.nc-empty
.nc-head
.nc-item
.nc-item.is-unread
.nc-jewel
.nc-list
.nc-text
.nc-time
.nc-title
.nc.is-on
```

## Notes

- Jewel color encodes the kind: magenta = mention, blue = reply, purple = system, gold = reward, green = verified.
- Unread rows carry a purple wash; clicking marks read and decrements the count.
- Emits `nc:read` with `detail.id` — persist read-state server-side.
- No fake notifications: render only real events.
