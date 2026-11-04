# Payments the Simple Way — Paste a Link, We Track the Rest
SN-2047 · SYSTEM / PAYMENTS
**Created:** 2026-11-04T03:23:52Z

## IN A NUTSHELL
Functionality first, payments after — and when payments come on, they come on simply. There is no heavy integration to build: the membership owner pastes their own PayPal link or Stripe link into their settings — boom — members pay through it, and the system tracks who paid. PayPal and Stripe do the same job. Shawn already has PayPal hooked up, so PayPal is the first rail. The money rail belongs to the owner's own account; NayaNET never has to touch a card.

## HUMAN
If you run a membership, you should not need a developer and three weeks to take money. You take the payment link from the PayPal or Stripe account you already have, paste it into your membership's settings, and you are in business. Your members click, pay, and the system remembers who has paid and who has not. Everything else — the content, the gating, the member experience — is built and working before payments even enter the picture.

## CHILD
It is like putting your own lemonade money jar on the stand. You do not need the town to build you a bank. You bring your jar, people drop their coins in, and the list on the clipboard says who paid. Simple.

## GRANDMA
Dear, it works the way a church bake sale always worked: the money goes into your own tin, not somebody else's machine. You paste in your PayPal or Stripe link — the one from the account you already trust — and the system politely keeps the list of who has paid. No card numbers ever pass through our hands, dear, and that is exactly how it should be.

## NAYA
I never block working functionality on a payment integration — memberships, gating, scheduling and sync all ship and prove themselves first. When payments activate, my job is a settings field for the owner's own payment link and an honest paid/unpaid record per member. I do not build checkout machinery the owner's own PayPal or Stripe already provides, and I never store card data. This ruling supersedes any 'create a Stripe account and payment links first' checklist — including the one in the 2026-11-03 gap-closer report Shawn relayed: that ask is retired.

## MACHINE
Owner setting: payment_link (a PayPal or Stripe payment URL) on the membership/page. Member flow: member pays at the owner's link → system tracks paid state per member (paid / not paid) for gating. No card data touches NayaNET at any point. Rails are equivalent by ruling; PayPal is first (Shawn's existing account). This citizen-membership rail is separate from the platform's own money contract (SN-1905 tiers + Ambassador 50% paid Wednesdays), which stands unchanged.

## WHAT IT ALL MEANS
Every week spent integrating a payment processor is a week the membership system is not in citizens' hands. The paste-a-link model removes the entire integration project and replaces it with a field and a list — and it puts the money where it belongs: directly between the member and the owner, in the owner's own account, from the first sale. Simplicity here is not a shortcut; it is the architecture.

## WHY IT MATTERS
Payments are the classic place good products stall: compliance, checkout edge cases, refund plumbing — months of work that adds no intelligence to the system. Shawn's ruling keeps the team's hands on the intelligent parts (matching, filling, syncing, gating) and lets two mature money networks do the one thing they are already perfect at. Track who paid; that is all the system needs to know.

## HOW IT CONNECTS
SN-1905 (the platform money contract — tiers, Ambassador 50% Wednesdays — a separate rail from citizen membership payments) · SN-0876 (memberships live inside every page — the thing this rail charges for) · SN-0881 (memberships run on Smart Mail — delivery and gating) · SN-2045 (the essence: citizens earn from memberships).

## WHAT IS IN IT FOR YOU
For a membership owner: selling starts the day your page is ready, with the account you already have. For a member: you pay the owner directly, through a name you already trust. For a builder: an entire integration project deleted from the board — spend those weeks on intelligence instead.

## THE LEARNING
When a mature external tool does one job perfectly, do not rebuild it — link to it and track the outcome. The behavior change: any plan that lists 'payment integration' as a build step gets rewritten to 'payment link field + paid tracking' before it reaches the board.
