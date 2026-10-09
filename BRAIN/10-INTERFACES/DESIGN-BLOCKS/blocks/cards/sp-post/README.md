# sp-post
Space feed post — author header (avatar/name/time), text, like + message actions.
- **Type:** cards / **Source:** Smart Spaces Page Design.html / **Files:** `.sp-post` → `sp-post.css`, `specimen.html`
- **States:** :hover, .sp-like.on (liked state)
- **Dependencies:** none — self-contained; per-avatar `--cc` set inline. `.sp-ava` rules copied in (canonical owner: sp-member); `.sp-sched-badge` rules copied in (canonical owner: sp-sched).
- **Selectors:** `.sp-post`, `.sp-post-top`, `.sp-post-who`, `.sp-post-name`, `.sp-post-time`, `.sp-post-text`, `.sp-post-actions`, `.sp-like`, `.sp-mail-author`, `.sp-sched-badge`, `.sp-ava`
## Use it
```html
<div class="sp-post">
  <div class="sp-post-top">
    <div class="sp-ava sm" style="--cc:#1e6fd9">M</div>
    <div class="sp-post-who">
      <div class="sp-post-name">Maya</div>
      <div class="sp-post-time">2h ago</div>
    </div>
    <span class="sp-sched-badge">🕐 Posts Monday at 9:00 AM</span>
  </div>
  <div class="sp-post-text">First prototype is live — drop your harshest feedback below.</div>
  <div class="sp-post-actions">
    <button class="sp-like on">♥ 12</button>
    <button class="sp-mail-author">✉ Message</button>
  </div>
</div>```
