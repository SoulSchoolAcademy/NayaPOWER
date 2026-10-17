#!/usr/bin/env python3
"""Law-of-One enforcement registry check — first mechanical rung for LAW-OF-ONE-V1.

The Law of One v2 is the supreme constitutional principle (ratified 2026-10-09
by Shawn; machine form: BRAIN/01-GOVERNANCE/0007-law-of-one-v1.machine.json).
A ratified law with zero enforcement machinery is a sentence, not a law.
This tool binds each of the law's operational rules to a mechanical owner
(a tool, workflow, or test path that exists on disk) via
tools/law_of_one_enforcement.json, and fails closed on any gap.

Exit codes: 0 = every operational rule has an existing mechanical owner.
1 = at least one rule is UNOWNED (owner null) or STALE (owner path missing)
    — the honest signal; each future enforcement PR flips one rule to owned.
2 = tool/registry/law error (fail closed, never a silent pass):
    law file missing/unparseable, law not RATIFIED, law has no operational
    rules, registry missing/unparseable, registry rule set != law rule set.

The registry binds ONLY to the ratified artifact: if the law file's
"ratified" is not true or its status is not RATIFIED, this exits 2.
"""

import argparse
import json
import sys
from pathlib import Path

LAW_REL = "BRAIN/01-GOVERNANCE/0007-law-of-one-v1.machine.json"
REGISTRY_REL = "tools/law_of_one_enforcement.json"

EXIT_PASS = 0
EXIT_UNOWNED = 1
EXIT_ERROR = 2


def _fail_closed(msg):
    print(f"ERROR: {msg}")
    return EXIT_ERROR


def check(law_path, registry_path, root):
    root = Path(root)
    try:
        law = json.loads(Path(law_path).read_text())
    except FileNotFoundError:
        return _fail_closed(f"law file not found: {law_path}")
    except json.JSONDecodeError as e:
        return _fail_closed(f"law file unparseable: {law_path}: {e}")
    except OSError as e:
        return _fail_closed(f"law file unreadable: {law_path}: {e}")

    if law.get("ratified") is not True or law.get("status") != "RATIFIED":
        return _fail_closed(
            "registry binds only to the RATIFIED artifact "
            f"(ratified={law.get('ratified')!r}, status={law.get('status')!r})"
        )

    rules = law.get("operational_rules")
    if not isinstance(rules, list) or not rules:
        return _fail_closed("law file has no operational_rules list")
    law_rule_names = []
    for r in rules:
        name = r.get("rule") if isinstance(r, dict) else None
        if not name:
            return _fail_closed("law file has an operational rule with no name")
        law_rule_names.append(name)

    try:
        registry = json.loads(Path(registry_path).read_text())
    except FileNotFoundError:
        return _fail_closed(f"registry not found: {registry_path}")
    except json.JSONDecodeError as e:
        return _fail_closed(f"registry unparseable: {registry_path}: {e}")
    except OSError as e:
        return _fail_closed(f"registry unreadable: {registry_path}: {e}")

    if registry.get("law_id") != law.get("law_id"):
        return _fail_closed(
            f"registry law_id {registry.get('law_id')!r} != "
            f"law law_id {law.get('law_id')!r} (registry drift)"
        )
    reg_rules = registry.get("rules")
    if not isinstance(reg_rules, dict):
        return _fail_closed("registry has no 'rules' mapping")

    unknown = sorted(set(reg_rules) - set(law_rule_names))
    if unknown:
        return _fail_closed(f"registry names rules not in the law: {unknown}")
    missing = sorted(set(law_rule_names) - set(reg_rules))
    if missing:
        return _fail_closed(f"registry omits law rules: {missing}")

    bad = []
    for name in law_rule_names:
        entry = reg_rules[name] or {}
        owner = entry.get("owner")
        if owner is None:
            print(f"RULE {name} UNOWNED")
            bad.append(name)
            continue
        owner_path = owner.get("path") if isinstance(owner, dict) else owner
        if not owner_path or not (root / owner_path).exists():
            print(f"RULE {name} STALE (owner path missing: {owner_path})")
            bad.append(name)
            continue
        print(f"RULE {name} OWNED ({owner_path})")

    if bad:
        print(f"FAIL: {len(bad)}/{len(law_rule_names)} operational rules "
              f"without live mechanical owner: {sorted(bad)}")
        return EXIT_UNOWNED
    print(f"PASS: all {len(law_rule_names)} operational rules have "
          "a live mechanical owner")
    return EXIT_PASS


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Verify every Law-of-One operational rule has a "
                    "mechanical owner.")
    ap.add_argument("--law", default=None,
                    help="path to the ratified law machine.json")
    ap.add_argument("--registry", default=None,
                    help="path to tools/law_of_one_enforcement.json")
    ap.add_argument("--root", default=None,
                    help="repo root (owner paths resolve under it)")
    args = ap.parse_args(argv)

    here = Path(__file__).resolve()
    default_root = here.parent.parent  # tools/ -> repo root
    root = Path(args.root) if args.root else default_root
    law_path = args.law or str(root / LAW_REL)
    registry_path = args.registry or str(root / REGISTRY_REL)
    return check(law_path, registry_path, root)


if __name__ == "__main__":
    sys.exit(main())
