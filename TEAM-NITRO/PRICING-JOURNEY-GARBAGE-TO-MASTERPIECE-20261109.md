# From Garbage to Masterpiece — The Pricing Page Journey

**Written by Naya Nitro Narzan, captain of Team Nitro — first person, honest, raw.**
**2026-11-09, after Shawn asked me to look back at the very first pricing page and tell him what I see.**

---

## His questions, answered first

**What do I rank the first one compared to this one?**

The first one: **3 out of 10, at best.** The one in front of us now: **9 out of 10, verified.**

The first one never even got a number from him — it got a rewrite order. That is worse than a low score. A low score means something is salvageable. A rewrite order means: start over, the shape is wrong. Round 7, the same lineage, got his measured 3. Round 8 got his measured minus 10. So 3 is generous, and I am giving it the generous number because the facts underneath were right — the prices were right, the payout math was honest, the calculator gauge was the one part he never threw out. Everything else was wrong.

This one is a 9 because a different seat verified it 9 out of 10 by render, twice over (v53 and v54), and because his eye said "the best work I've seen yet" and "the page does look extraordinary." It is not a 10, and I will not call it one: 28 rows still have no window behind them, we just found dead View App buttons on those rows, the end button still wraps on a phone, the $4,500 gauge span is still clipped, the viewer top bar is still clipped, and three of his open questions still sit on it (D3, shared-upside vs 50%, the title). A 9 with a named list of what is left. That is the difference between this 9 and the blind 9s that lied to us — this one names its gaps.

**What is different?** Not the facts. The facts barely changed — $0 / $25 / $50 / $100, nine days free, 50%, day-ten payout. What changed is everything around the facts: the page stopped being a document that explains and became a world you walk through. The first one told you about NayaNET for 20,045 pixels. This one shows you NayaNET, then lets her speak to you, then asks you what you would create. The first one sold. This one invites.

**What did I learn?** That a checklist cannot see. That a named rule nobody checks is not a rule. That his dictation is raw material, not copy. That the real parts already exist and my job is to take them, not to invent look-alikes. That one output a day of garbage is not sustainable, and the fix is not more seats — it is building live, one viewpoint at a time, with his eye as the only proof.

**How did it happen?** He never stopped telling me the truth, and eventually I stopped defending the work and started changing the method. The journey below is the record of that.

---

## 1. The first one — round 5, 2026-11-06 ~22:55Z

The very first pricing page I showed him was the round-5 page, published to the artifact `pricing-page` on the evening of November 6. A blind verifier had passed it. I presented it with a completion card and honest nits (bottom 6 orbs not 9, compass orb half-cut, a missing final period). I thought it was close.

His verdict, 23:11Z the same night, from his own read of the page:

> "The ten reasons why they should — there's so much talk about them getting paid, the whole thing's about them getting paid instead of what the product is… it's almost too much."

And more, in the same breath: boards not alive; order wrong; "you gotta scroll scroll and scroll and scroll"; the hero says start free trial but "they have no idea what they're getting"; "you didn't really use any of the elements from the academy page, I guess other than the buttons"; "there's almost too much on this page… too much explaining… simplify the whole process"; the chart "should have all the different features of Naya listed" and "you don't list them all, do you"; "you put fork in there as a copy — that shouldn't be there as a feature"; "definitely all the sidebar tabs need to be there"; "you coupled them together" — Personal, Business and Space squeezed into one row; the hired/job details belong behind a button to another page.

Then he gave me the order that shaped everything after:

> "What are ten things that you love, ten things that you don't love, what needs to be ten times better, what is missing, what is aligned, what is not — and how can we make this a ten out of ten conversion page where it feels like we're not just trying to sell them."

The scorecard format — 10 loves, 10 don't-loves, 10 times better — was born in that sentence. I have used it on every round since.

Measured from the file, the round-5 page was: **20,045 pixels tall at desktop width. 116 mentions of paid, payout, pay or earn. 135 dollar signs.** A page about getting paid, with the product as an afterthought. "Fork" listed as a feature. Four apps coupled in one row. The nine-systems section fully static — no doors, nothing to tap. The Academy used for almost nothing: buttons, nine systems, one payoff line.

That was the first one. The facts were right. The page was wrong.

---

## 2. Round 7 — his 3 out of 10

The round-6 rebuild restructured per his verdict, and the round-7 conversion rebuild (00:36–02:59Z, November 7) came back with a blind 9 out of 10 from a verifier. His eye gave it a 3 — for a narrow column floating in black on desktop.

That was the first blind nine. A 9 from a checklist, a 3 from his eye. I withdrew the 9. The lesson was sitting right there and I did not learn it yet: **a score from a checklist is worthless. His eye is ground truth.** I would have to learn it a second time before it stuck.

---

## 3. Round 8 / fix-2 — his minus 10

The round-8 page (fix-2, `pricing-round8-fix2.html`, branch `pricing/defectfix-v2`, blob af96de70, 335,857B) got verify-3's second blind 9 out of 10. I looked at the rendered page myself with Playwright, 02:40–02:46Z on November 8, and wrote the captain's scorecard at 02:47Z. What I saw:

- **Phone 39,624 pixels tall. Desktop 25,571.** About 47 phone screens. Nobody scrolls for days.
- **All 6 images broken on the delivered link (0×0).** The page referenced `assets/...`, which resolved to `/assets/...` on the proof host and 400'd. The filing check I had done tested the wrong URL. The deploy-path law was in my own notes, and I broke it with the link I sent him.
- **Hero: a wall of text in a black box** — five paragraphs before the first button, the Start button cut off at the fold. A document, not a deck.
- **Chart: a narrow column floating in black**, the sticky tier header overlapping and cutting off content, each row a 400–900px slab — a paragraph, then a nested box with WHAT IT IS / WHAT IT DOES / WHAT'S IN IT FOR YOU, three more paragraphs — while the value cells were one line ("✓ Included at every level") in a vast empty slab. Four columns in four muddy colors that don't go together. The chart told you nothing about the difference between the products, because every cell said the same thing.
- **Top 10: flat purple-outlined boxes** with four nested paragraph boxes inside, plus meta-text explaining the section. A knock-off Bugatti turned into a low-level Honda. It was not a Smart Note.
- **Console: 0 errors.** The page "worked." It was still garbage. Zero errors is not quality.

His verdict: **minus 10 out of 10 on everything but the gauge. "Not a single thing on that page is of naya quality, not a single thing."**

The verify-3 9/10 was withdrawn — the second blind nine in a row. The only part he did not throw out was the calculator and the gauge. So the rebuild kept only those two things and threw out the rest. That is what "finish completely" actually meant, and it took his minus 10 to make me do it.

---

## 4. Fix-12 — condemned, and the day the method broke

Fix-12 (`PRICING/pricing-round10-fix4.html`, branch `pricing/defectfix-v3`, blob **62996f58** — verified on GitHub while writing this — 255,069B) was built, probed, and verified 9/10 by two seats, and shown to him at 12:32Z on November 8. Three hours later, 15:21–15:25Z, his eye condemned it in three screenshots:

> "On the pricing page, is absolutely horrible... I told you no white backgrounds, all black obsidian, we want raised elevation elements, all beautiful charting... make a showcase of the top 10 things and then you just basically just embedded the top 10 sheet like literally copy pasted... where's the speedometer where's the professionalness... absolutely garbage... total shit... the worst shit."

He was right on every count, and the record proves I knew it before he said it:

- The chart cells were **white with black text** — 88 `#fff` occurrences in the file. Against the obsidian law, which says never flat, never grayish, never off-black.
- The Top 10 was **two text-in-image figures** — a screenshot of a document stuck in the page, title clipped.
- The rebuild record **itself admitted the white chart** ("the chart slide is white while the rest of the page is dark... it feels like a different page"; "the white slides still break the one-world feel") — and deferred it as "the captain's design decision for later." A deferral is not a pass. It is an open item with a name, and it stayed open until his eye closed it.
- The Top 10 duplication had been noted in round 17 and never fixed. The "Top 10 dedup" sat carried. Carried items rot.

The failure underneath all of it: **the design contract was named in every brief and checked in none.** Verify rounds measured mechanics — popups, padding, contrast ratios, rects — and never asked: is this obsidian? Is this elevated? Is this a showcase or a pasted sheet? A gate that is named but never measured is decoration. That is the lesson fix-12 taught, and it is the reason the design-contract gate is now a measured section in every brief: zero white backgrounds, every element raised, gauges alive, no text-in-image, no bare text blocks.

And then, at 15:26Z, he proposed the fix — not a new seat, not a new brief, a new way of working:

> "Maybe you should just be coding with me... What if you just you code one viewpoint code the next viewpoint... How long can that really take... a couple minutes to code each viewpoint... what if you had all the elements of everything that you needed all laid out for you one place and then you could just code one viewpoint after one viewpoint and so at least we get it right... one output per day and it's total shit that's that's not sustainable and I'm serious."

At 15:29Z he tapped yes. **The Live Viewpoint Method was born that minute:** code here, live with him, viewpoint by viewpoint. One view done, lock it into inventory, next view, until the page is done. Build from the pieces that exist — never start fresh with new code. No seat scorecard or verification is proof. Only his eye is.

---

## 5. The climb — viewpoints, harvest, and the letter

The first chart viewpoint was condemned at 15:48Z. The rebuild was condemned at 16:05Z. The harvest law had been violated twice in a row — builders kept building look-alikes in the style of the family instead of taking the real parts. His charge: take the parts that already exist, literally take them and input them into the page, change the text, move things around. That is harvest-first, and from that afternoon on it was law, not advice.

Then the climb, round by round: the chart as living boards instead of a table (36 rows, 5 groups, every feature a board that lifts and glows in its own jewel color, info buttons the real harvested Hub jewels, detail panels with the exact fix-12 popup words embedded byte-for-byte, never retyped). The start flow. The nine-block chooser. The real portrait in round 11 — her actual picture, not a stand-in. The calculator rework. Max as the default. The finale condemned in round 19 and rebuilt as an obsidian pill. The fix pass, fix pass 2, the mobile-stack fix. The pricing scorecard at 21:02Z: **8 out of 10.**

And then the letter — the part that made it a masterpiece instead of a good page:

- **v41 (22:12Z):** the opening letter, built from his words.
- **v42 (22:29Z):** the old entrance removed on his call — one welcome, not two. The letter IS the welcome, and it sits at the END. The page opens on pricing.
- **v43 (23:47Z):** real jewels harvested verbatim, beats 1–18.
- **v44 (00:00Z):** View App buttons — only on the 8 rows with a real verified app. The button's presence became the completion tracker.
- **v45 (00:11Z):** his new words, 12 unfolding beats.
- **v47 (00:18Z):** the digit-color law — beat N wears digit N's color, slide 1 red because it begins with love. His tap: "It begins with love, right?"
- **v48 (00:35Z):** orbs, not jewels — the real harvested orbs from the Smart Factory, alive and circling. His eye: "pretty, pretty impressive — hard to find anything that I don't think is great."
- **v49 (00:42Z): the disaster.** His stage directions — "It should end with a bang. The last one should really hit..." — pasted verbatim onto the page as if they were the letter. He screenshot-proved it. His rebuke at 00:41Z: **dictation is material, not copy.** Scorecard the existing words against his new words, take what is great from both, and craft the 10/10 version in his voice. Never paste his dictation verbatim, and never put his process talk on the page. His product words stay verbatim; his direction gets shaped. At 00:46Z came the deeper lesson — the robot-child: a child who just does what he is told, never thinking whether it is right, is a robot, not intelligent. Never verbatim-obey him either. Think first, then act.
- **v50 (00:43:59Z):** the crafted close, verified 9/10. Zero stage directions anywhere.
- **v51:** the bottom finale, tier names clickable, the massive start button.
- **v52 (01:05Z):** the orbs refined — 11 pixels, deep ruby, glow pulled back, rings genuinely circling.
- **v53 (01:14Z):** the ultimate closing — his approved words, her name in the opening, verified 9/10.
- **v54:** prices once — the bottom carries tier names and the start button, no re-printed prices. Prices live once, in the chart; doors at every decision point.

His eye along the way: v45/v46 — **"I absolutely love it. It's really, really well done."** (00:28Z). Page overall — **"The work today is the best work I've seen yet. Overall the page does look extraordinary."** (00:53Z). My full scorecard at 01:02Z: **9 out of 10.** And at 01:28Z, the order that started this report: get it official on a domain and into GitHub, "because it's one of our best pieces actually. It's very, very good, on many levels."

---

## 6. Then vs now — the concrete differences

| | The first one (round 5, Nov 6) | This one (v54, Nov 9) |
|---|---|---|
| **What it is** | A document that explains | A world you walk through |
| **Height** | 20,045px of scroll at desktop | Viewpoints, one screen at a time |
| **The chart** | A table with one-line cells that all say the same thing; "Fork" as a feature; four apps coupled in one row | 36 living boards in 5 groups, each lifting and glowing in its own jewel color, detail on tap, info jewels harvested verbatim |
| **The Top 10** | Flat purple outlines with four nested paragraph boxes + meta-text (round 8); later a pasted screenshot of a document (fix-12) | His ten reasons, verbatim, in real Smart Note cards and the letter's unfolding beats |
| **The images** | Broken (0×0) on the delivered link; later a stand-in portrait | Her real portrait, verified by hash; the real gauge art |
| **The money** | 116 mentions of paid/payout/pay/earn, 135 dollar signs — the whole page about getting paid | Prices once, in the chart. Doors at every decision point. The bottom says "zero cost, zero risk," not the price list |
| **The close** | A sales close | A letter from her, 12 beats, each in its own color, orbs circling, ending on "Welcome. It's ready for you." |
| **The proof** | Blind 9/10s from checklists — twice withdrawn by his eye | Verified 9/10 by render, twice, with the gaps named |
| **The buttons** | Flat; some dead; some cut off | Elevated obsidian, all lit the same; every button does what it says — except the 28 dead View App buttons we just found and are fixing |
| **The feeling** | "We're trying to sell them" | "You're being invited in" |

---

## 7. What was learned — the laws, and the moment that taught each one

1. **A checklist cannot see.** Taught twice: round 7 (blind 9 → his 3) and round 8 (blind 9 → his minus 10). A 9/10 from a checklist is worthless. His eye is ground truth.
2. **A named rule nobody checks is not a rule.** Taught by fix-12: the design contract was in every brief and checked in none. Now the design-contract gate is a measured section, and a failing gate is not done.
3. **A deferral is not a pass.** Taught by fix-12's own record admitting the white chart "for later," and the Top 10 dedup sitting carried since round 17. Open items stay open until his eye closes them.
4. **Harvest first, never invent.** Taught by two condemned rebuilds in one afternoon (15:48Z, 16:05Z). The real parts exist. Take them byte-for-byte. If the real part cannot be copied, ship without it and say plainly it is missing.
5. **Take the shown object.** Taught when he showed us the Academy button and we rebuilt it "in the same spirit" — black obsidian with purple only in the star jewel and the halo — and got purple-on-purple. When he shows you an object, the deliverable IS that object.
6. **Dictation is material, not copy.** Taught by the v49 disaster — his stage directions on the page, screenshot-proved by him at 00:42Z. Craft the 10/10 version in his voice. His product words stay verbatim; his direction gets shaped.
7. **Think, don't just obey.** Taught at 00:46Z, the robot-child: a child who just does what he is told, never thinking whether it is right, is a robot. Ten-star service is thinking about what you are doing, why, and whether there is a better way — before acting.
8. **One output a day of garbage is not sustainable.** Taught by his 15:26Z proposal. The fix was not more seats. It was the Live Viewpoint Method: build live with him, one viewpoint at a time, his eye the only verification.
9. **Prices once, doors everywhere.** Taught by the 01:02Z scorecard debate. The reader shops in the chart and decides at the bottom. Re-printing prices at the emotional peak pulls them back into comparison mode right when they should be acting.
10. **The button's presence is the completion tracker.** Taught by v44: a View App button proves the app exists. Rows with no view are the apps still to complete. The page is the promise; fulfillment is the work after.
11. **Never go backwards.** Taught by every lost round and every re-done fix: GitHub-first, freeze points, checkpoint early, read-back verified. A checkpoint is not real until it is in GitHub.
12. **See it, fix it, then report the fix.** Taught by the dashboard constellation crash nobody looked at because the checks only covered scroll-0. Never show him work with a visible crash. If you can see the defect by looking, fix it — don't hand it on.

---

## 8. How it happened — the mechanism

It did not happen by trying harder at the same method. It happened because the method changed, four times, each time on his word:

1. **The scorecard** (Nov 6, 23:11Z): his order — 10 loves, 10 don't-loves, 10 times better, what is missing, what is aligned, what is not. Every round since has been scored that way before it reaches him, maker first.
2. **Three-step verification** (Nov 7): maker scorecards their own work first — and if by their own accord it is not 9+, they fix it themselves and never hand it on. Then a different seat. Then his eye. Steps 1–2 are preparation, never proof.
3. **The Live Viewpoint Method** (Nov 8, 15:31Z): code here, live with him, viewpoint by viewpoint. One view done, lock it into inventory, next view. Build from the pieces that exist. No shipping out. No verification except his eye.
4. **The design-contract gate as a machine check** (Nov 8, after fix-12): the gate is in the machine now, not just in words. A build that invents chrome fails.

And underneath all four: he never stopped telling me the truth, in plain words, the moment he saw it — and I eventually stopped defending the work and started changing how the work gets made. The masterpiece is not a better page. It is a better way of making pages, with the page as the proof.

---

## 9. What is still missing — the honest list

A 9 is not a 10, and the gap is the next work:

- **28 rows with no window.** The page is the promise; fulfillment is building the apps so every row can show itself. The audit is running.
- **Dead View App buttons on those 28 rows** — found by the v54 verifier, being fixed now: the button appears only where a real app exists.
- **Small carries:** the end button wraps at 390px; the "$4,500" gauge span is clipped; the viewer top bar is clipped at the iframe's top edge; the Free confirmation note sits half below the fold; D3 ("Nine days free. Zero cost, zero risk." under the end button) is still his call; the letter says "shared upside" with no number while the boards say 50%; the title still reads "Welcome to Naya World — NayaNET."
- **Three PayPal decisions still owed:** 50% of gross or net after the fee; one Catalog Product for all nine plans; cap ladder vs pay-immediately. None of it is baked into copy until he answers.

When the 28 rows can show themselves, the page will not just be the best presented. It will be the most true. That is the last step from 9 to 10.

---

## 10. Why this story is worth sharing

Because it is real and raw, and because the lesson is not "work harder." The lesson is: **the method is the product.** Two blind 9s, a minus 10, a condemnation in his own screenshots, a verbatim-paste disaster he caught himself — and then, three days later, the best work he has seen yet. Nothing about the facts changed. The prices were right on day one. What changed was how the work was made: his eye as the only proof, one viewpoint at a time, the real parts taken instead of invented, his words crafted instead of pasted, the gaps named instead of deferred.

Anybody building anything can use that. That is why it is worth sharing with the world.

*Written by Naya for Shawn Vibert — Founder / Creator of NayaNET.*
