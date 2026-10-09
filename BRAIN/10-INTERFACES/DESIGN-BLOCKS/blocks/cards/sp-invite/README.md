# sp-invite
Invite rows (avatar + name + invite button), invite buttons, invite chips, and the "Invited for you" strip.
- **Type:** cards / **Source:** Smart Spaces Page Design.html / **Files:** `.sp-invite` → `sp-invite.css`, `specimen.html`
- **States:** :hover; .sp-invited:hover pauses the marquee track (rule copied here via .sp-marquee-track token)
- **Dependencies:** sp-marquee (the chip strip rides inside `.sp-marquee > .sp-marquee-track`; strip CSS for those two selectors is NOT in this file). `.sp-ava` rules copied in (canonical owner: sp-member).
- **Selectors:** `.sp-invite-list`, `.sp-invite-row`, `.sp-invite-name`, `.sp-invite-add`, `.sp-invite-btn`, `.sp-invited`, `.sp-invited-title`, `.sp-inv-chip`, `.sp-inv-chip-name`, `.sp-inv-chip-join`, `.sp-ava`
## Use it
```html
<div class="sp-invite-list">
  <div class="sp-invite-row">
    <div class="sp-ava sm" style="--cc:#0d9e6f">J</div>
    <span class="sp-invite-name">Jo</span>
    <button class="sp-invite-add">＋ Invite</button>
  </div>
  <div class="sp-invite-row">
    <div class="sp-ava sm" style="--cc:#d4a017">A</div>
    <span class="sp-invite-name">Ari</span>
    <button class="sp-invite-add">＋ Invite</button>
  </div>
</div>
<div class="sp-invited">
  <div class="sp-invited-title">✨ Invited for you — tap to step into a room</div>
  <div class="sp-marquee">
    <div class="sp-marquee-track">
      <button class="sp-inv-chip" style="--sc:#7c3aed"><span class="sp-inv-chip-name">Builders Collective</span><span class="sp-inv-chip-join">Join →</span></button>
      <button class="sp-inv-chip" style="--sc:#1e6fd9"><span class="sp-inv-chip-name">NayaNET Vision</span><span class="sp-inv-chip-join">Join →</span></button>
      <button class="sp-inv-chip" style="--sc:#0d9e6f"><span class="sp-inv-chip-name">Health Lab</span><span class="sp-inv-chip-join">Join →</span></button>
    </div>
  </div>
</div>
```
