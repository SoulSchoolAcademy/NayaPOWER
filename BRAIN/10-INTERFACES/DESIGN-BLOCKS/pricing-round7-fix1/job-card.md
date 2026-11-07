# Job Card — "Congratulations, You're Hired"
**Filed:** 2026-11-07 (pricing round 7 fix1, F9). **Status:** filed object, in use (earning slide).
**Source:** the hired beat, rebuilt as an object in fix1 (F9). It must read as an object a stranger would screenshot and send.
**Construction:** `.job-card` — badge "NAYA · NEW HIRE" + gold seal "★ HIRED" + the same copy ("we decided to hire everyone") + the job-pay line (first payout day 10, then daily) + the job-why line (the 50% locks in once we're paid — cancellation is forward-only, so what you've earned stays earned) + the earn-terms object (50% / Same-day / Day 10, on the page plainly per Addition 12 supersession (a)) + the You're Hired Q&A in Shawn's words + "Conditional, never typical — computed from your invites, never promised. Potential, not promise." + a text-link to the hired page (one conversion action only — the button is the claim, never a second action). Cinema hostess at the edge.
```css
.job-card{max-width:880px; margin:0 auto; padding:32px; border-radius:20px; text-align:center;
    border:2px solid rgba(255,191,61,.9); position:relative; overflow:hidden;
    background:linear-gradient(135deg,#2a2a35 0%,#0a0a0f 50%,#23232e 100%);
    box-shadow:inset 0 1px 0 rgba(255,255,255,.2), inset 0 -2px 4px rgba(0,0,0,.5),
      0 16px 40px rgba(0,0,0,.6), 0 0 44px rgba(255,191,61,.25);}
```
