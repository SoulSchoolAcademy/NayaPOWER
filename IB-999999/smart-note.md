# Smart Note: GitHub to Hub Pipeline Test

**Intelligent Block:** IB-999999
**Created:** 2026-10-19T04:33:00Z
**Source:** nayanet-test
**Author:** Naya Nitro Narzan

## IN A NUTSHELL
Testing the GitHub → Hub pipeline. A Smart Note committed to GitHub should trigger the webhook and appear in the Hub.

## HUMAN
When Shawn says "smartnote this," I commit the note to GitHub as a markdown file. GitHub fires a webhook to Supabase. Supabase processes it and the Hub displays the note. That's the flow: GitHub → Hub, not the other way around.

## CHILD
Imagine you write a note on a piece of paper and put it in a special box (GitHub). The box has a bell that rings (webhook) when you put something in. When the bell rings, a helper (Supabase) takes the note out and puts it on the big board (Hub) where everyone can see it!

## GRANDMA
Dear, it's like this: you write your thoughts down and file them away safely in the filing cabinet (that's GitHub, dear). The moment you file it, a little notification goes off, and your helpful assistant takes a copy and pins it up on the family bulletin board (the Hub) so the whole family can read it. Simple as that!

## NAYA
The GitHub → Hub pipeline is the canonical Smart Note ingestion path. Notes are authored as versioned markdown artifacts in the repository (governed, auditable, permanent). The `nayanet-github-webhook` Edge Function receives push events, validates the payload, extracts the Smart Note structure, and projects it to the Hub's feed via Supabase. This preserves the "GitHub as source of truth" architecture while making notes visible in the Hub interface.

## MACHINE
```json
{
  "intelligent_block_id": "IB-999999",
  "pipeline": "GITHUB_TO_HUB_TEST",
  "source": "nayanet-test",
  "webhook": "nayanet-github-webhook",
  "expected_flow": ["github_push", "webhook_fire", "supabase_process", "hub_display"],
  "test_status": "pending_verification"
}
```

## WHAT IT ALL MEANS
The direction matters. GitHub is the permanent, versioned store. The Hub is the live, readable display. Notes flow from permanent → live, not the other way. This keeps the system honest: what's in GitHub is the truth, what the Hub shows is a reflection of that truth.

## WHAT'S IN IT FOR YOU
You write a note once, it lives forever in GitHub (versioned, searchable, permanent), AND it shows up in the Hub automatically (readable, shareable, live). No double-entry. No copy-paste. Write once, appear everywhere.

## HOW IT APPLIES
When you say "smartnote this" to any Naya, she commits the note to GitHub in this format. The webhook fires. The Hub updates. You see your note in the Hub within seconds. That's the One Flow working end-to-end.
