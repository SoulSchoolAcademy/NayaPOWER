#!/usr/bin/env python3
"""Fail-closed source contract test for the GitHub webhook owner-aware persistence seam.

This is source-contract proof only. It intentionally does not claim live production
secret configuration or signed-delivery success.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WEBHOOK = (ROOT / "NAYANET/EXECUTION-BRIDGE/nayanet-github-webhook/index.ts").read_text(encoding="utf-8")
BIND = (ROOT / "supabase/migrations/20260924230000_harden_github_app_owner_binding_v1.sql").read_text(encoding="utf-8")
PERSIST = (ROOT / "supabase/migrations/20260924233100_repair_github_webhook_owner_aware_canonical_replay_v1.sql").read_text(encoding="utf-8")

def require(text: str, needle: str) -> None:
    assert needle in text, f"MISSING:{needle}"

def main() -> None:
    # Receiver must authenticate the external sender before owner resolution.
    require(WEBHOOK, 'const secret=Deno.env.get("GITHUB_WEBHOOK_SECRET")||"";')
    require(WEBHOOK, 'if(!secret)return json({ok:false,error:"GITHUB_WEBHOOK_SECRET_NOT_CONFIGURED"')
    require(WEBHOOK, 'if(!(await verifySignature(secret,body,signature)))return json({ok:false,error:"INVALID_GITHUB_SIGNATURE"}')
    require(WEBHOOK, 'const installationId=payload?.installation?.id;')
    require(WEBHOOK, 'p_installation_id:installationId')
    require(WEBHOOK, 'p_repository:repository')

    # Binding is explicit, unique, active, and service-role resolver only.
    require(BIND, "alter table public.nayanet_smart_connect_participation")
    require(BIND, "nayanet_smart_connect_github_bind")
    require(BIND, "GITHUB_BINDING_ALREADY_OWNED")
    require(BIND, "GITHUB_BINDING_NOT_FOUND")
    require(BIND, "GITHUB_BINDING_AMBIGUOUS")
    require(BIND, "grant execute on function public.nayanet_resolve_github_webhook_owner(bigint,text) to service_role")

    # Canonical persistence accepts service-role only for the explicit webhook action,
    # and independently re-resolves the owner. Ordinary user-scoped calls remain
    # auth.uid()-bound.
    require(PERSIST, "if auth.uid() is null then")
    require(PERSIST, "auth.role() <> 'service_role'")
    require(PERSIST, "p_action <> 'github_webhook_received'")
    require(PERSIST, "coalesce(p_execution_authorization->>'source','') <> 'github_app_webhook'")
    require(PERSIST, "GITHUB_WEBHOOK_OWNER_BINDING_MISMATCH")
    require(PERSIST, "v_actor_id := (p_execution_authorization->>'actor_id')::uuid")
    require(PERSIST, "where user_id=v_actor_id")
    require(PERSIST, "if p_action = 'intelligence.capture' then")

    # Replay must return original lineage rather than advance state/create a receipt.
    require(PERSIST, "if v_existing_event.id is not null and coalesce(v_existing_event.receipt_id,'') <> '' then")
    require(PERSIST, "'replayed',true")
    require(PERSIST, "return jsonb_build_object('replayed',true")

    print("GITHUB_WEBHOOK_OWNER_BOUND_SOURCE_CONTRACT=PASS")
    print("PRODUCTION_SECRET=NOT_CLAIMED")
    print("SIGNED_DELIVERY=NOT_CLAIMED")
    print("LIVE_PERSISTENCE=NOT_CLAIMED")

if __name__ == "__main__":
    main()
