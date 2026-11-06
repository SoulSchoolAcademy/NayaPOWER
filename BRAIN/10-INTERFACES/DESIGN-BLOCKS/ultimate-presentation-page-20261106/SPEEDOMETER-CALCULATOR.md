# THE SPEEDOMETER CALCULATOR — Named Factory Part
## Filed 2026-11-06 with The Ultimate Presentation Page (blind-verified PASS 10/10, 199/200)

**What it is:** a live earnings calculator built into a pricing page — pick a plan + a pace, see what you'd make — and the result drives a speedometer gauge: the needle moves as the reader plays. The speedometer is the signature piece (SN-2076, "Naya — The High Performance Machine"). The calculator is a real control, not a picture.

**Code:** `speedometer-calculator.html` in this folder — **16,401 bytes, sha256 `c817c4ba5a205b49b5f1c9d7d64669ea8be8e1c2e234a2f738e0ca86d349f2e2`**. Extracted verbatim from `pricing-table-DRAFT-v4.html` (sha256 `9c42eff8…`) by exact line slice; nothing retyped or restyled. Fragments, by source line number:

| Fragment | Source lines |
|---|---|
| `:root` vars | 11–16 |
| `.lit-section` (cosmetic) | 130, 461 |
| `.calc-*` CSS | 345–387 |
| `.calc-cinema` CSS | 438–441 |
| Calculator HTML (`<section class="calc" id="calculator">`) | 669–749 |
| Calculator script | 750–802 |

Discrete block by design: remove the section + its CSS (`.calc-*`) + its script to take it out. The Cinema image beside it is `HUB/app/banner-assets/pricing-supercharger-alt-cinema.webp` (PR #3271); the extract keeps the page's local `src` and names the GitHub copy in its header comment.

---

## The controls

- **Your package** — three buttons: POWER ($25/mo · $12.50 a sale) · PRO ($50/mo · $25 a sale) · MAX ($100/mo · $50 a sale). Default: Pro.
- **Your pace** — − / + steppers, 1–10 sales, per day or per month (toggle buttons).
- **Try it — the worked examples** — three preset buttons that set plan + pace + unit in one tap:
  - "3 Max a day → $4,500/mo" · "1 Pro a day → $750/mo" · "3 Max a month → $150/mo"
- **The gauge** — SVG speedometer, dial ticks $0 / $1,250 / $2,500 / $3,750 / $5,000. The needle (`#calc-needle`) rotates as the readout changes; the readout sits beneath it with the math line under that.

## The math — honest, computed from the reader's own inputs

**Rule: 50% of plan price per sale, recurring monthly.** Per-sale share: Power $12.50 · Pro $25 · Max $50.

```
monthly = share × pace × (30 if per-day else 1)
yearly  = monthly × 12
needle angle = -90° + min(monthly, 5000) / 5000 × 180°
```

**Blind-verified presets (clicked live, read from `#calc-amount`, `#calc-math`, `#calc-needle`):**

| Preset | Readout | Math line | Needle |
|---|---|---|---|
| 3 Max / day | **$4,500** / month, recurring | *3 Max sales a day × $50 × 30 days = $4,500 a month ($54,000 a year)* | rotate(72deg) |
| 1 Pro / day | **$750** / month, recurring | *1 Pro sale a day × $25 × 30 days = $750 a month ($9,000 a year)* | rotate(-63deg) |
| 3 Max / month | **$150** / month, recurring | *3 Max sales a month × $50 = $150 a month ($1,800 a year)* | rotate(-84.6deg) |

Needle angle is monotonic with the readout (−84.6° → −63° → 72° as $150 → $750 → $4,500). Stress test (10 Max/day): readout **$15,000** a month ($180,000 a year), needle pegged at 90°, math line appends the pegged note — the computed figure stays $15,000.

## The honesty rule — never break it

- **NEVER print $5,000/month or $60,000/year as a computed figure.** $5,000 is the dial's cap: a scale marking on the dial, and the pegged note (*"off the dial; the needle is pegged at $5,000"*) which only fires when monthly > $5,000. $60,000 occurs **0×** in the page.
- The section carries its own disclaimer, in the copy: *"Potential, not a promise. Computed from your inputs — plan price × 50%, recurring monthly. Nothing here is promised earnings."*
- Shawn's spoken figures for the same example ($5,000/month, $60,000/year) are his voice in dictation. The page prints only computed numbers. Do not "fix" the calculator to match the spoken figure — the calculator is the authority, and the authority is the math.

## The copy around it (part of the part — the pitch, his words)

- **"NOT network marketing."** — "No downline, no upline — just the potential to get paid every day." (Note: the page carries the line with an em-dash continuation, not a final period — one-character near-miss, recorded in the page manifest.)
- **The Mercedes line:** "Imagine working for Mercedes — a high-end, high-tech company, epic products, solid, amazing — and you get a commission for promoting them. But instead of 5% or 10%, you are getting 50% of the revenue — not the profit, straight up."
- **"As soon as we get paid, you get paid. No hold back. No games."**
- **The Bugatti:** "Try the new Bugatti of the internet — name's Naya." + "everything the whole of everything the internet is — smart mail, social networking, intelligence, everything all in one — an AI operating system for the internet, the new layer, the new intelligence layer. And you get paid for referring everybody to it — and you get to use it, which is the greatest gift."
- **The auto-hire:** "Imagine getting paid from a high-tech intelligence company — not having to apply for the job, you automatically get the job. Something truly extraordinary — absolutely solid and beautiful and effective and useful. 50% of the revenue straight up. No games, no catch, no bullshit. Money in your account. Everybody gets a trial for free."
- **The proof:** "You know it is solid because you tried her for nine days. You cannot say it is not good — it is good, it is more than good, it is awesome."

## Use it for

Any page that shows earnings potential from the reader's own inputs — pricing pages, ambassador pages, membership pages. Re-skin the plan buttons (change `data-share` / `data-plan` and the labels); the formula, the needle, and the honesty rule travel with it unchanged. The dial cap ($5,000) is the one number to re-set if the product's price ladder changes.
