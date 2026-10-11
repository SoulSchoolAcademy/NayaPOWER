# Smart Block: `nl-chart`

Chart container from Missing Blocks library.

- **Type:** data
- **Source:** `Naya_Lego-blocks.html` (extracted byte-true, never rewritten)
- **CSS:** `nl-chart.css`
- **Specimen:** `specimen.html`
- **States found:** base only
- **Dependencies:** tokens.css

## Use it

1. Include `tokens.css` (once per page).
2. Include `nl-chart.css`.
3. Copy the HTML from `specimen.html`.
4. **Light it:** the entrance animation fires when `lit` is added *after* first paint. Add it via JS on load or scroll into view:
   ```html
   <div class="nl-chart" data-light>
   <script>
     // Light charts when they enter the viewport
     const io = new IntersectionObserver(es => es.forEach(e => {
       if (e.isIntersecting) { e.target.classList.add('lit'); io.unobserve(e.target); }
     }), { threshold: 0.3 });
     document.querySelectorAll('.nl-chart[data-light]').forEach(el => io.observe(el));
   </script>
   ```
   Without `lit`, bars sit at zero — this is the entrance state, not a bug. Adding `lit` statically in markup shows the final state without the animation.

## Selectors in this block

```
.nl-chart / .nl-chart.lit
.nl-chart .c-sub
.nl-chart h4
.nl-bars / .nl-barcol / .nl-barv
.nl-line / .nl-line path.ln / .nl-line circle.pt
.nl-legend
.nl-charts.lit (parent-trigger variant)
```
