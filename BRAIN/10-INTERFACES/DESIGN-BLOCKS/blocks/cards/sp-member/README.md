# sp-member
Member row — avatar, name, role, save-as-contact button or saved badge, mail button.
- **Type:** cards / **Source:** Smart Spaces Page Design.html / **Files:** `.sp-member` → `sp-member.css`, `specimen.html`
- **States:** :hover, @media (max-width:760px) (wrap + full-width save button), @media (prefers-reduced-motion:reduce)
- **Dependencies:** none — self-contained; per-avatar `--cc` set inline. Owns the canonical `.sp-ava` / `.sp-mstack` rules (copied into sp-card, sp-post, sp-pin, sp-chat, sp-invite).
- **Selectors:** `.sp-member`, `.sp-member-info`, `.sp-member-name`, `.sp-member-role`, `.sp-member-mail`, `.sp-ava`, `.sp-mstack`, `.sp-saved-badge`, `.sp-save-contact`
## Use it
```html
<div class="sp-member">
  <div class="sp-ava md" style="--cc:#7c3aed">S</div>
  <div class="sp-member-info">
    <div class="sp-member-name">Shawn</div>
    <div class="sp-member-role">Director</div>
  </div>
  <button class="sp-save-contact">＋ Save as Contact</button>
  <button class="sp-member-mail" title="Mail Shawn">✉</button>
</div>
<div class="sp-member">
  <div class="sp-ava md" style="--cc:#1e6fd9">M</div>
  <div class="sp-member-info">
    <div class="sp-member-name">Maya</div>
    <div class="sp-member-role">Member</div>
  </div>
  <span class="sp-saved-badge">✓ In Contacts</span>
  <button class="sp-member-mail" title="Mail Maya">✉</button>
</div>
```
