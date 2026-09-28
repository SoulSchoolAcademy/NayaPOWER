# Naya Activation Portal v1

Static, activation-only page for the NayaNET human authorization ceremony.

## Deploy
Upload this directory to Cloudflare Pages/Workers as a static site. The public URL is intentionally not hard-coded because Cloudflare assigns it.

## Supabase dashboard
After deployment, add the exact activation URL to Supabase Auth URL configuration / allowed redirect URLs. The email template must contain the Supabase verification link/token expected by the Auth flow.

## Security
Only the Supabase project URL and publishable browser key are included. Never put SUPABASE_USER_ACCESS_TOKEN, SUPABASE_USER_REFRESH_TOKEN, service-role keys, or GitHub Actions credentials in this folder.

## Architecture
Activation = ignition switch.
Hub = cockpit.
Runtime = engine.
Intelligent Blocks = durable intelligence.

The human should not manually log into every node. Browser sessions may refresh/expire/revoke normally; the long-lived governed runtime identity is a separate architecture concern.