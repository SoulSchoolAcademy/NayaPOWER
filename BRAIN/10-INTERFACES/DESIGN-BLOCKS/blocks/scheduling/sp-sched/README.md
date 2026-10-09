# sp-sched
Schedule picker — frequency tabs, weekday buttons, day-of-month grid, live summary line, timezone note.
- **Type:** scheduling / **Source:** Smart Spaces Page Design.html / **Files:** `.sp-sched` → `sp-sched.css`, `specimen.html`
- **States:** .on (selected tab / day / date), .sp-sched-btn.set (schedule chosen)
- **Dependencies:** none — self-contained. Genuinely different from seg-tab (segmented room control): these are scheduler day/date pickers.
- **Selectors:** `.sp-sched-tabs`, `.sp-sched-tab`, `.sp-sched-body`, `.sp-sched-summary`, `.sp-sched-badge`, `.sp-sched-btn`, `.sp-days-row`, `.sp-day-btn`, `.sp-month-grid`, `.sp-dom-btn`, `.sp-tz`
## Use it
```html
<div class="sp-sched-tabs">
  <button class="sp-sched-tab on">Once</button>
  <button class="sp-sched-tab">Daily</button>
  <button class="sp-sched-tab">Weekly</button>
  <button class="sp-sched-tab">Monthly</button>
</div>
<div class="sp-sched-body">
  <div class="sp-days-row">
    <button class="sp-day-btn">S</button>
    <button class="sp-day-btn on">M</button>
    <button class="sp-day-btn">T</button>
    <button class="sp-day-btn">W</button>
    <button class="sp-day-btn">T</button>
    <button class="sp-day-btn">F</button>
    <button class="sp-day-btn">S</button>
  </div>
  <div class="sp-month-grid">
    <button class="sp-dom-btn">1</button>
    <button class="sp-dom-btn">2</button>
    <button class="sp-dom-btn">3</button>
    <button class="sp-dom-btn">4</button>
    <button class="sp-dom-btn">5</button>
    <button class="sp-dom-btn">6</button>
    <button class="sp-dom-btn">7</button>
    <button class="sp-dom-btn">8</button>
    <button class="sp-dom-btn">9</button>
    <button class="sp-dom-btn">10</button>
    <button class="sp-dom-btn">11</button>
    <button class="sp-dom-btn">12</button>
    <button class="sp-dom-btn">13</button>
    <button class="sp-dom-btn">14</button>
    <button class="sp-dom-btn on">15</button>
    <button class="sp-dom-btn">16</button>
    <button class="sp-dom-btn">17</button>
    <button class="sp-dom-btn">18</button>
    <button class="sp-dom-btn">19</button>
    <button class="sp-dom-btn">20</button>
    <button class="sp-dom-btn">21</button>
    <button class="sp-dom-btn">22</button>
    <button class="sp-dom-btn">23</button>
    <button class="sp-dom-btn">24</button>
    <button class="sp-dom-btn">25</button>
    <button class="sp-dom-btn">26</button>
    <button class="sp-dom-btn">27</button>
    <button class="sp-dom-btn">28</button>
    <button class="sp-dom-btn">29</button>
    <button class="sp-dom-btn">30</button>
    <button class="sp-dom-btn">31</button>
  </div>
</div>
<div class="sp-sched-summary">Posts every Monday at 9:00 AM</div>
<div class="sp-tz">Timezone: America/Los_Angeles</div>
<button class="sp-sched-btn">🕐 Schedule</button>
<button class="sp-sched-btn set">🕐 Posts Monday at 9:00 AM</button>
<span class="sp-sched-badge">🕐 Posts Monday at 9:00 AM</span>
```
