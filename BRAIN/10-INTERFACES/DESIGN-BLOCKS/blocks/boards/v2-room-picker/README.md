# Smart Block: `v2-room-picker`

Room picker. Jewel room buttons in a responsive grid with an aria-live detail panel; JS swaps the story on tap.

- **Type:** boards
- **Source:** `Open_This_NayaNET_Design_V2.html`
- **Files:** `v2-room-picker.css`, `specimen.html`, `v2-room-picker.js`
- **States:** :hover, :focus-visible, [aria-pressed="true"]
- **Dependencies:** `tokens.css`, `jewels/v2-facet-gem`, `v2-room-picker.js`

## Use it

1. Copy `v2-room-picker.css` into your page or component folder.
2. Include the shared `tokens.css` on the page plus: `tokens.css`, `jewels/v2-facet-gem`, `v2-room-picker.js`.
3. Paste the markup from `specimen.html` where the component should live.
4. Give each button a unique `data-room` key and matching entry in the `rooms` map in `v2-room-picker.js`. Keep the `.ref` honesty line under the detail.

## Selectors

```css
.room-grid
.room
.room .jewel
.room b
.room small
.room:hover,.room:focus-visible,.room[aria-pressed="true"]
.room-detail
.room-detail h3
.room-detail p
.room-detail .ref
```
