# sp-pin
Pinned intelligence block — badge, category line, title, summary, like/comment/share/unpin actions, comment thread.
- **Type:** cards / **Source:** Smart Spaces Page Design.html / **Files:** `.sp-pin` → `sp-pin.css`, `specimen.html`
- **States:** :hover, :focus (comment input), .sp-pin-act.on (liked), .sp-pin-comments.open (thread expanded via 💬 button)
- **Dependencies:** none — self-contained; per-block `--sc` and per-avatar `--cc` set inline. `.sp-ava` rules copied in (canonical owner: sp-member).
- **Selectors:** `.sp-pin`, `.sp-pin-act`, `.sp-pin-actions`, `.sp-pin-badge`, `.sp-pin-cat`, `.sp-pin-cmt`, `.sp-pin-cmt-n`, `.sp-pin-cmt-t`, `.sp-pin-cmtin`, `.sp-pin-cmtrow`, `.sp-pin-comments`, `.sp-pin-label`, `.sp-pin-sum`, `.sp-pin-title`, `.sp-pin-zone`, `.sp-ava`
## Use it
```html
<div class="sp-pin-zone">
  <div class="sp-pin-label">📌 PINNED INTELLIGENCE</div>
  <div class="sp-pin" style="--sc:#7c3aed">
    <div class="sp-pin-badge">PINNED</div>
    <div class="sp-pin-cat">INTELLIGENCE · BUILDERS COLLECTIVE</div>
    <div class="sp-pin-title">Launch checklist v3</div>
    <div class="sp-pin-sum">The twelve gates every release passes — frozen, no exceptions.</div>
    <div class="sp-pin-actions">
      <button class="sp-pin-act on">♥ 5</button>
      <button class="sp-pin-act">💬 1</button>
      <button class="sp-pin-act">↗ Share</button>
      <button class="sp-pin-act">Unpin</button>
    </div>
    <div class="sp-pin-comments open">
      <div class="sp-pin-cmt">
        <div class="sp-ava xs" style="--cc:#0d9e6f">J</div>
        <div>
          <div class="sp-pin-cmt-n">Jo</div>
          <div class="sp-pin-cmt-t">Gate 7 saved us twice already.</div>
        </div>
      </div>
      <div class="sp-pin-cmtrow">
        <input class="sp-pin-cmtin" type="text" placeholder="Add a comment…">
        <button class="sp-pin-act">Send</button>
      </div>
    </div>
  </div>
  <button class="sp-pin-act">＋ Pin Intelligent Block</button>
</div>
```
