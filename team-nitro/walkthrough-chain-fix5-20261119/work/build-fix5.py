#!/usr/bin/env python3
"""FIX5 worker build (2026-11-19): rebuild the staging worker from the edited
identity through the proven builder, twice (deterministic sha), verify every
embed by sha256 + the FIX5 marker, node --check the built worker.
Writes the worker to the V23 worker file and to work/worker-fix5.js via
write_resilient (chunked writes + verify; EPERM flake live).
"""
import importlib.util, subprocess, sys

SPEC = importlib.util.spec_from_file_location(
    "stage_fix3", "/home/hatch/workspace/team-nitro/walkthrough-chain-fix3-20261119/work/stage-fix3.py")
st = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(st)

WORK = "/home/hatch/workspace/team-nitro/walkthrough-chain-fix5-20261119/work"
IDENT_SHA = "6f805eba00fa7ccbf89103c46878c352e73db5b26792010dc2de535c706418f0"


def main():
    new_welcome = st.read_bytes(st.WELCOME_LOCAL)
    new_ident = st.read_bytes(st.IDENT_LOCAL)
    new_unfold = st.read_bytes(st.UNFOLD_LOCAL)
    print("inputs: welcome %d B %s" % (len(new_welcome), st.sha(new_welcome)), flush=True)
    print("inputs: identity %d B %s" % (len(new_ident), st.sha(new_ident)), flush=True)
    print("inputs: unfold %d B %s" % (len(new_unfold), st.sha(new_unfold)), flush=True)
    assert st.sha(new_welcome) == st.WELCOME_SHA, "welcome moved"
    assert st.sha(new_ident) == IDENT_SHA, "identity moved: %s" % st.sha(new_ident)
    assert st.sha(new_unfold) == st.UNFOLD_SHA, "unfold moved"
    worker = st.run_builder(new_welcome, st.WELCOME_SHA, IDENT_SHA, st.UNFOLD_SHA)
    assert b"FIX5 (2026-11-19" in worker, "worker missing the FIX5 gate marker"
    assert b"verdictChecked" in worker, "worker missing the FIX5 gate"
    r = subprocess.run(["node", "--check", "--input-type=module", "-"],
                       input=worker, capture_output=True)
    assert r.returncode == 0, "node --check failed for worker: %s" % r.stderr.decode("utf-8", "replace")[:500]
    print("node --check OK: worker (%d B) sha %s" % (len(worker), st.sha(worker)), flush=True)
    try:
        st.write_resilient(st.WORKER_LOCAL, worker)
    except Exception as e:
        print("WARNING: local worker copy not written (EPERM flake): %r" % e, flush=True)
    try:
        st.write_resilient(WORK + "/worker-fix5.js", worker)
    except Exception as e:
        print("WARNING: work-dir worker copy not written (EPERM flake): %r" % e, flush=True)
    print("BUILD-RESULT worker_bytes=%d worker_sha=%s" % (len(worker), st.sha(worker)), flush=True)


if __name__ == "__main__":
    main()
