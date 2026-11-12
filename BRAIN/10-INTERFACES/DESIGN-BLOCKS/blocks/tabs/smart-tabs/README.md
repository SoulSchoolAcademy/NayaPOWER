# Smart Block: `smart-tabs`

The feed-navigation tab bar: horizontal scroll (scrollbar hidden), per-tab `--tc` theming, popover editor shell. Feed tabs are navigation intent, never storage.

## Why

The feed’s navigation is intent, not storage. A horizontal-scrolling tab bar with per-tab theming and a popover editor — your feed, organized the way you think.

- **Type:** tabs
- **Source:** `Naya Smart Hub Design.html` (extracted verbatim, never rewritten)
- **CSS:** `smart-tabs.css`
- **Specimen:** `specimen.html`
- **States found:** :hover, .active, mobile
- **Dependencies:** smart-tabs.js (selection), tokens.css

## Use it

1. Include `tokens.css` (once per page).
2. Include `smart-tabs.css`.
3. Copy the HTML from `specimen.html`.
4. Include `smart-tabs.js` for single-select behavior.
5. Set `--tc` per tab for its glow color.

## Selectors in this block

```
.smart-tabs
.smart-tab
.smart-tab:hover
.smart-tab.active
.smart-tab .sn-label
.smart-tab .sn-mark
.smart-tab .sn-more
.tab-pop
.tab-pop-title
.tab-pop-list
.tab-pop-row
.tab-pop-add
.tab-pop-del
.tab-pop-name
```
