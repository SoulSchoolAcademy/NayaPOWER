import argparse, hashlib, json
from pathlib import Path

DRIFT = "REGISTRY_RUNTIME_CONTENT_DRIFT"

def canonical_hash(lesson):
    try:
        lesson = json.dumps(json.loads(lesson), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    except (ValueError, TypeError):
        lesson = str(lesson)
    return hashlib.sha256(lesson.encode("utf-8")).hexdigest()

def lineage_valid(verify):
    checks = verify["checks"]
    p = verify["persisted"]
    ev = p["receipt"].get("evidence", {})
    object_local = (
        ev.get("event_row_id") == p["event"]["id"]
        and ev.get("intelligent_block_id") == p["block"]["intelligent_block_id"]
        and ev.get("lineage_id") == p["lineage"]["id"]
        and ev.get("relationship_id") == p["relationship"]["relationship_id"]
        and ev.get("index_id") == p["index"]["id"]
        and ev.get("checkpoint_id") == p["checkpoint"]["id"]
        and p["receipt"]["action"] == "intelligence_commit"
    )
    non_checkpoint = [v for k, v in checks.items() if not k.startswith("checkpoint_links_")]
    checkpoint = [v for k, v in checks.items() if k.startswith("checkpoint_links_")]
    return all(non_checkpoint) and (all(checkpoint) or object_local)

def assess(expected, verify, verify_only):
    if not verify.get("independent_verification"):
        raise ValueError("REGISTRY_RUNTIME_VERIFY_NOT_INDEPENDENT")
    if not lineage_valid(verify):
        raise ValueError("REGISTRY_RUNTIME_LINEAGE_INVALID")
    block = verify["persisted"]["block"]
    actual = block["content"]["lesson"]
    actual_hash = canonical_hash(actual)
    exact = actual_hash == expected["content_hash"] and actual == expected["expected_content"]
    if exact:
        return {"status": "REUSE_VERIFIED", "action": "REUSE", "actual_hash": actual_hash,
                "intelligent_block_id": block["intelligent_block_id"]}
    return {
        "status": DRIFT,
        "action": "FAIL_CLOSED" if verify_only else "SUPERSEDE",
        "actual_hash": actual_hash,
        "expected_hash": expected["content_hash"],
        "old_block_row_id": block["block_id"],
        "old_intelligent_block_id": block["intelligent_block_id"],
    }

def supersede_request(capture, expected, verify, grant_id):
    block = verify["persisted"]["block"]
    return {
        "mode": "supersede",
        "p_authority_grant_id": grant_id,
        "p_superseded_block_id": block["block_id"],
        "p_title": capture["title"],
        "p_content": expected["expected_content"],
        "p_block_type": block.get("block_type", "GOVERNED_INTELLIGENCE"),
        "p_understanding_state": "CANDIDATE",
        "p_owner_scope": block.get("owner_scope", "PRIVATE"),
        "p_project_id": "NayaNET",
        "p_idempotency_key": "SMART-NOTE-RECONCILE-" + expected["content_hash"][:24],
        "p_connections": expected.get("resolved_connections", []),
        "p_topic": capture.get("topic"),
        "p_category": capture.get("category", "SMART_NOTE"),
    }

def validate_supersede(expected, old_verify, response):
    if response.get("ok") is not True or response.get("status") != "SUPERSEDED":
        raise ValueError("SUPERSESSION_RUNTIME_FAILED")
    old = old_verify["persisted"]["block"]
    new = response["result"]
    if new.get("supersedes_block_id") != old.get("block_id"):
        raise ValueError("SUPERSESSION_CHAIN_MISMATCH")
    lesson = (new.get("content") or {}).get("lesson")
    if lesson != expected["expected_content"] or canonical_hash(lesson) != expected["content_hash"]:
        raise ValueError("SUPERSESSION_CONTENT_MISMATCH")
    return {
        "status": "REGISTRY_RUNTIME_CONTENT_RECONCILED",
        "prior_lineage_preserved": True,
        "prior_block_row_id": old["block_id"],
        "prior_intelligent_block_id": old["intelligent_block_id"],
        "new_block_row_id": new["block_id"],
        "new_intelligent_block_id": new["intelligent_block_id"],
        "content_hash": expected["content_hash"],
    }

def verify_supersession(expected, old_verify, block_verify, marker):
    if not lineage_valid(old_verify):
        raise ValueError("SUPERSESSION_PRIOR_LINEAGE_INVALID")
    if block_verify.get("ok") is not True or block_verify.get("status") != "BLOCK_VERIFIED":
        raise ValueError("SUPERSESSION_NEW_BLOCK_UNVERIFIED")
    old = old_verify["persisted"]["block"]
    new = block_verify["persisted"]["block"]
    if old.get("status") != "SUPERSEDED":
        raise ValueError("SUPERSESSION_OLD_NOT_SUPERSEDED")
    if old.get("superseded_by_block_id") != new.get("block_id"):
        raise ValueError("SUPERSESSION_FORWARD_LINK_MISMATCH")
    if new.get("supersedes_block_id") != old.get("block_id"):
        raise ValueError("SUPERSESSION_BACK_LINK_MISMATCH")
    lesson = new["content"]["lesson"]
    if lesson != expected["expected_content"] or canonical_hash(lesson) != expected["content_hash"]:
        raise ValueError("SUPERSESSION_CURRENT_CONTENT_MISMATCH")
    prior = old_verify["persisted"]
    return {
        "ok": True,
        "status": "SUPERSESSION_RECONCILED",
        "independent_verification": True,
        "checks": {
            "prior_lineage_valid": True,
            "supersession_chain_valid": True,
            "current_content_exact": True,
        },
        "persisted": {
            "block": new,
            "event": prior["event"],
            "lineage": prior["lineage"],
            "relationship": prior["relationship"],
            "index": prior["index"],
            "checkpoint": prior["checkpoint"],
            "receipt": prior["receipt"],
        },
        "supersession_proof": {
            **marker,
            "prior_lineage": {
                "event_id": prior["event"]["id"],
                "lineage_id": prior["lineage"]["id"],
                "relationship_id": prior["relationship"]["relationship_id"],
                "index_id": prior["index"]["id"],
                "checkpoint_id": prior["checkpoint"]["id"],
                "receipt_id": prior["receipt"]["id"],
            },
        },
    }

def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def dump(p, v): Path(p).write_text(json.dumps(v, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")

def main():
    ap=argparse.ArgumentParser()
    sub=ap.add_subparsers(dest="cmd", required=True)
    a=sub.add_parser("assess"); a.add_argument("--expected",required=True); a.add_argument("--verify",required=True); a.add_argument("--verify-only",action="store_true"); a.add_argument("--out",required=True)
    b=sub.add_parser("build-supersede"); b.add_argument("--capture",required=True); b.add_argument("--expected",required=True); b.add_argument("--verify",required=True); b.add_argument("--grant-id",required=True); b.add_argument("--out",required=True)
    c=sub.add_parser("validate-supersede"); c.add_argument("--expected",required=True); c.add_argument("--old-verify",required=True); c.add_argument("--response",required=True); c.add_argument("--out",required=True)
    v=sub.add_parser("verify-supersession"); v.add_argument("--expected",required=True); v.add_argument("--old-verify",required=True); v.add_argument("--block-verify",required=True); v.add_argument("--marker",required=True); v.add_argument("--out",required=True)
    args=ap.parse_args()
    if args.cmd=="assess": dump(args.out, assess(load(args.expected),load(args.verify),args.verify_only))
    elif args.cmd=="build-supersede": dump(args.out, supersede_request(load(args.capture),load(args.expected),load(args.verify),args.grant_id))
    elif args.cmd=="validate-supersede": dump(args.out, validate_supersede(load(args.expected),load(args.old_verify),load(args.response)))
    else: dump(args.out, verify_supersession(load(args.expected),load(args.old_verify),load(args.block_verify),load(args.marker)))

if __name__=="__main__": main()
