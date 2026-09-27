"""Mutation harness: every fail-closed path must be caught by a test.

Run from the repo root. Restores both files afterwards, always.
"""
import subprocess, sys, shutil
from pathlib import Path

KERNEL = Path("kernel/nayapower_kernel.py")
REG = Path("kernel/brain_registry.py")

MUTANTS = [
    ("count check removed", REG,
     "    if len(records) != len(NODE_NAMES):",
     "    if False:"),
    ("truncated manifest tolerated", KERNEL,
     "        except (BrainIntegrityError, KernelIntegrityError) as exc:",
     "        except (KeyboardInterrupt, SystemExit) as exc:"),
    ("integrity block removed entirely", KERNEL,
     "        except (BrainIntegrityError, KernelIntegrityError) as exc:\n"
     "            return DecisionResult(\n"
     "                allowed=False,\n"
     "                executed=False,\n"
     "                truth_state=TruthState.BLOCKED,\n"
     "                blocked_by=Node.KNOW,\n"
     "                trace=(Node.SELF, Node.KNOW),\n"
     "                evidence=(f\"KNOW.kernel_integrity:{exc}\",),\n"
     "            )",
     "        except (BrainIntegrityError, KernelIntegrityError) as exc:\n"
     "            raise"),
    ("hardcoded order reintroduced", KERNEL,
     "        names = load_canonical_node_names(base)",
     "        names = ('SELF','LAW','ACT','KNOW','PROVE','CONNECT','VERIFY','LEARN','EVOLVE')"),
    ("node_order ignores manifest", KERNEL,
     "        return cls._manifest_order(str(root) if root is not None else None)",
     "        return (Node.SELF, Node.LAW, Node.ACT, Node.KNOW, Node.PROVE,\n"
     "                Node.CONNECT, Node.VERIFY, Node.LEARN, Node.EVOLVE)"),
    ("duplicate id check removed", REG,
     "        if node_id in seen_ids:",
     "        if False:"),
    ("duplicate name check removed", REG,
     "        if name in seen_names:",
     "        if False:"),
    ("missing name tolerated", REG,
     '        if not isinstance(name, str) or not name.strip():\n'
     '            problems.append(f"node_{position}_missing_name:{node_id}")\n'
     '            continue',
     '        name = name or "UNNAMED"'),
    ("missing manifest tolerated", REG,
     '        raise BrainIntegrityError(f"missing_manifest:{CANONICAL_MANIFEST_PATH}")',
     '        return {"kernel_id": None, "status": None, "node_count": 0, "nodes": []}'),
    ("unparseable json tolerated", REG,
     '        raise BrainIntegrityError(f"unparseable_manifest:{exc}") from exc',
     '        manifest = {"nodes": []}'),
    ("unknown node name silently dropped", KERNEL,
     "            except ValueError as exc:",
     "            except ValueError:\n                continue"),
    ("integrity failure reports allowed", KERNEL,
     "                allowed=False,\n                executed=False,\n                truth_state=TruthState.BLOCKED,\n                blocked_by=Node.KNOW,",
     "                allowed=True,\n                executed=True,\n                truth_state=TruthState.UNKNOWN,\n                blocked_by=None,"),
    ("only first problem reported", REG,
     '    if problems:\n        raise BrainIntegrityError(";".join(problems))',
     '    if problems:\n        raise BrainIntegrityError(problems[0])'),
    ("non-object node tolerated", REG,
     '        if not isinstance(node, dict):\n'
     '            problems.append(f"node_{position}_is_not_an_object")\n'
     '            continue',
     '        if not isinstance(node, dict):\n            continue'),
]


def suite() -> tuple[int, str]:
    p = subprocess.run([sys.executable, "-m", "pytest", "-q"],
                       capture_output=True, text=True)
    tail = [l for l in p.stdout.splitlines() if "passed" in l or "failed" in l or "error" in l]
    return p.returncode, (tail[-1] if tail else p.stdout[-200:])


def main() -> int:
    backups = {p: p.read_text(encoding="utf-8") for p in (KERNEL, REG)}
    base_code, base_tail = suite()
    print(f"baseline (must be green): {base_tail}")
    if base_code != 0:
        print("BASELINE IS RED - fix that before trusting mutants")
        return 1

    survivors = []
    try:
        for name, path, find, repl in MUTANTS:
            text = backups[path]
            if find not in text:
                print(f"  !! PATTERN NOT FOUND  {name}")
                survivors.append(name + " (pattern not found)")
                continue
            path.write_text(text.replace(find, repl, 1), encoding="utf-8")
            code, tail = suite()
            caught = code != 0
            print(f"  {'CAUGHT ' if caught else 'SURVIVED'}  {name:36} {tail}")
            if not caught:
                survivors.append(name)
            path.write_text(text, encoding="utf-8")
    finally:
        for p, text in backups.items():
            p.write_text(text, encoding="utf-8")

    code, tail = suite()
    print(f"\nrestored: {tail}")
    print(f"mutants: {len(MUTANTS)}  survivors: {len(survivors)}")
    for s in survivors:
        print(f"  SURVIVOR: {s}")
    return 1 if survivors else 0


if __name__ == "__main__":
    raise SystemExit(main())
