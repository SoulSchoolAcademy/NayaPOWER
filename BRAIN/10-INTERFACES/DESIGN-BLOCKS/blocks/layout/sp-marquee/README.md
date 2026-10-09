# sp-marquee
Announcement marquee — seamless looping horizontal track (60s linear infinite, edge fade mask, pauses on hover).
- **Type:** layout / **Source:** Smart Spaces Page Design.html / **Files:** `.sp-marquee` → `sp-marquee.css`, `specimen.html`
- **States:** :hover (.sp-invited:hover .sp-marquee-track pauses), @keyframes sp-marquee
- **Dependencies:** sp-invite (the demo chips are `.sp-inv-chip` — chip CSS is NOT in this file; link sp-invite.css to render them fully). Loop trick (verbatim page JS): `strip.innerHTML += strip.innerHTML;` — duplicate the track content once for a seamless -50% loop.
- **Selectors:** `.sp-marquee`, `.sp-marquee-track`
## Use it
```html
<div class="sp-marquee">
  <div class="sp-marquee-track">
      <button class="sp-inv-chip" data-sid="sp-builders" style="--sc:#7c3aed"><span class="sp-inv-chip-name">Builders Collective</span><span class="sp-inv-chip-join">Join →</span></button>
      <button class="sp-inv-chip" data-sid="sp-vision" style="--sc:#1e6fd9"><span class="sp-inv-chip-name">NayaNET Vision</span><span class="sp-inv-chip-join">Join →</span></button>
      <button class="sp-inv-chip" data-sid="sp-health" style="--sc:#0d9e6f"><span class="sp-inv-chip-name">Health Lab</span><span class="sp-inv-chip-join">Join →</span></button>
      <button class="sp-inv-chip" data-sid="sp-builders" style="--sc:#7c3aed"><span class="sp-inv-chip-name">Builders Collective</span><span class="sp-inv-chip-join">Join →</span></button>
      <button class="sp-inv-chip" data-sid="sp-vision" style="--sc:#1e6fd9"><span class="sp-inv-chip-name">NayaNET Vision</span><span class="sp-inv-chip-join">Join →</span></button>
      <button class="sp-inv-chip" data-sid="sp-health" style="--sc:#0d9e6f"><span class="sp-inv-chip-name">Health Lab</span><span class="sp-inv-chip-join">Join →</span></button>
  </div>
</div>
```
