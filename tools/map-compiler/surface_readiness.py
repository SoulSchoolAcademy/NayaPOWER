"""Evidence-first public surface census for existing Living Map compiler.

Opt-in only: the hourly workflow must not acquire 25 new network requests
without first measuring cost. Public HTTP response != functional/AAA approval.
Does not authenticate, read user data, create state, or grant release authority.
"""
import datetime
import json
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request

HOST = "https://nayanet.live"
QUALITY_DIMENSIONS = (
    "Visual Excellence", "Functional Completeness", "Intelligence", "Honesty",
    "Performance", "Reliability & Continuity", "Accessibility", "Craft",
)


def load_registry(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    assert data["schema_version"] == "nayanet.surface-registry.proposed.v1"
    rows = data["surfaces"]
    assert rows and len({r["id"] for r in rows}) == len(rows)
    assert len({r["path"] for r in rows}) == len(rows)
    ids = {r["id"] for r in rows}
    for row in rows:
        assert row["path"].startswith("/") and "://" not in row["path"]
        assert row["critical_journey"] and row["owner_area"]
        assert set(row["assessments"]["dimension_scores"]) == set(QUALITY_DIMENSIONS)
        assert all(x in ids for x in row["depends_on"])
    return data


def grade_surface(item):
    """Conservative quality floor; does NOT validate external PROVE receipts."""
    a = item["assessments"]
    vals = list(a["dimension_scores"].values())
    if not all(isinstance(v, (int, float)) and not isinstance(v, bool)
               and 0 <= v <= 10 for v in vals):
        return "UNASSESSED"
    if any(v < 9.5 for v in vals):
        return "BELOW_9_5"
    if not a["independent_verifier_identity"] or (
            a["independent_verifier_identity"] == a["author_identity"]):
        return "UNVERIFIED"
    if not a["source_sha"] or a["source_sha"] != a["deployed_sha"]:
        return "UNVERIFIED"
    if not a["verified_receipts"] or not a["freshness_at"]:
        return "UNVERIFIED"
    if a["positive_real_user_test"] is not True or a["adversarial_negative_test"] is not True:
        return "UNVERIFIED"
    if not a["governed_release_approval"]:
        return "READY_FOR_SHIP_REVIEW"
    # Proof links in editable registry files are NOT themselves authenticated
    # external receipts. Final acceptance belongs to PROVE/VERIFY + LAW.
    return "EXTERNAL_ACCEPTANCE_VALIDATION_REQUIRED"


def probe_surface(path, opener=urllib.request.urlopen, timeout=7):
    """HEAD only, cheap, anonymous; route signal never equals function."""
    req = urllib.request.Request(HOST + path, method="HEAD",
        headers={"User-Agent": "NayaNET-Living-Map/1.0"})
    try:
        with opener(req, timeout=timeout) as response:
            uri = urllib.parse.urlsplit(response.geturl())
            status = int(response.status)
            return {"http_status":status, "reachable":200 <= status < 400,
                    "redirected":uri.path != path or bool(uri.query),
                    "effective_path":uri.path}
    except urllib.error.HTTPError as e:
        if e.code == 405:
            # Static Smart Notes reject HEAD but serve normal GET. A bounded
            # Range GET checks reachability without reading the body; no
            # private or authenticated content is requested.
            get = urllib.request.Request(HOST + path, method="GET",
                headers={"User-Agent":"NayaNET-Living-Map/1.0",
                         "Range":"bytes=0-0"})
            try:
                with opener(get, timeout=timeout) as response:
                    uri = urllib.parse.urlsplit(response.geturl())
                    status = int(response.status)
                    return {"http_status":status,"reachable":200 <= status < 400,
                            "redirected":uri.path != path or bool(uri.query),
                            "effective_path":uri.path,
                            "head_unsupported_get_fallback":True}
            except Exception as exc:
                return {"http_status":405,"reachable":None,
                        "redirected":False,"effective_path":path,
                        "error":"GET fallback unavailable: "+type(exc).__name__}
        return {"http_status":int(e.code),"reachable":False,
                "redirected":False,"effective_path":path,"error":"HTTP response"}
    except Exception as e:
        return {"http_status":None,"reachable":None,"redirected":False,
                "effective_path":path,"error":type(e).__name__}


def audit_registry(registry, probe=probe_surface):
    rows = []
    for item in registry["surfaces"]:
        signal = probe(item["path"])
        rows.append({"id":item["id"],"path":item["path"],
                     "purpose":item["purpose"],"owner_area":item["owner_area"],
                     "critical_journey":item["critical_journey"],
                     "quality_gate":grade_surface(item),**signal})
    reachable = sum(r["reachable"] is True for r in rows)
    unknown = sum(r["quality_gate"] == "UNASSESSED" for r in rows)
    status = ("red" if any(r["reachable"] is False for r in rows)
              else "unknown" if any(r["reachable"] is None for r in rows)
              else "amber")  # Even 25/25 200 is never GREEN.
    return {"status":status,
            "measured_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "evidence":f"{reachable}/{len(rows)} public routes reachable; {unknown} "
                       "unassessed. No independently validated AAA/9+ claim.",
            "coverage_complete":bool(registry["coverage_complete"]),
            "surface_count":len(rows),
            "public_reachable":reachable,
            "unassessed":unknown,
            "official_9_plus_count":None,  # requires independent trusted receipts
            "rows":rows}
