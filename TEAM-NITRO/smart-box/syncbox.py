#!/usr/bin/env python3
"""syncbox.py - the sickness's root, moved into the box.

The sync's working memory (.sync-state.json, .sync-heartbeat.json) and
the bake step (build_feed_live.py and its output hub-feed-live.json)
lived only on this one machine. This module moves them into the Smart
Box: the box holds verbatim copies of the state and the heartbeat, a
manifest with the sha256 of every piece (including the bake output and
the scripts, recorded by hash), and a rebuild that restores the local
files byte-identical from the box.

What this does NOT do, deliberately: it does not edit
sync-smart-notes.py or build_feed_live.py, and it does not change sync
behaviour for citizens. The live sync still reads its local files; the
box holds the authoritative copy beside them, and the recovery demo
proves a wiped machine rebuilds from the box. Repointing the sync to
read from the box is a later step, with its own proof - not smuggled
in here.

The bake output (hub-feed-live.json, ~5 MB) is recorded by hash, count,
and newest card - NOT copied whole into the box. Copying a 5 MB derived
file into the vault would make the box a second feed; the output is
rebuilt by re-running build_feed_live.py from Supabase + GitHub, and
the manifest hash proves the rebuild matches. The state file
(298,217 bytes) and heartbeat (131 bytes) ARE copied verbatim: they
are the working memory, and they are the size the box is built for.

Standard library only. No credentials, no secrets, no key material.
"""

import hashlib
import json
import os

STATE_NAME = ".sync-state.json"
HEARTBEAT_NAME = ".sync-heartbeat.json"
MANIFEST_NAME = "manifest.json"

DEFAULT_STATE_PATH = os.path.expanduser(
    "~/workspace/factory-pipeline/.sync-state.json")
DEFAULT_HEARTBEAT_PATH = os.path.expanduser(
    "~/workspace/factory-pipeline/.sync-heartbeat.json")
DEFAULT_FEED_PATH = os.path.expanduser(
    "~/workspace/factory-pipeline/hub-feed-live.json")
DEFAULT_SYNC_PY = os.path.expanduser(
    "~/workspace/factory-pipeline/sync-smart-notes.py")
DEFAULT_FEED_PY = os.path.expanduser(
    "~/workspace/factory-pipeline/build_feed_live.py")


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def _read_bytes(path):
    with open(path, "rb") as handle:
        return handle.read()


def capture_sync_state(box_dir, state_path=DEFAULT_STATE_PATH,
                       heartbeat_path=DEFAULT_HEARTBEAT_PATH,
                       feed_path=DEFAULT_FEED_PATH,
                       sync_py=DEFAULT_SYNC_PY, feed_py=DEFAULT_FEED_PY):
    """Copy the sync working memory into the box directory.

    Writes ``.sync-state.json`` and ``.sync-heartbeat.json`` verbatim
    into ``box_dir``, plus ``manifest.json`` naming every piece with
    its sha256, byte count, and source path. The bake output and the
    scripts are recorded by hash (and, for the feed, by card count) -
    see the module docstring for why the 5 MB feed is not copied.
    Returns the manifest dict. Raises FileNotFoundError when a
    required local file is missing - the capture never invents state.
    """
    os.makedirs(box_dir, exist_ok=True)
    state_bytes = _read_bytes(state_path)
    heartbeat_bytes = _read_bytes(heartbeat_path)
    state = json.loads(state_bytes.decode("utf-8"))
    heartbeat = json.loads(heartbeat_bytes.decode("utf-8"))

    with open(os.path.join(box_dir, STATE_NAME), "wb") as handle:
        handle.write(state_bytes)
    with open(os.path.join(box_dir, HEARTBEAT_NAME), "wb") as handle:
        handle.write(heartbeat_bytes)

    files = {
        STATE_NAME: {"sha256": sha256_bytes(state_bytes),
                     "bytes": len(state_bytes),
                     "source_path": state_path,
                     "files_tracked": len(state.get("files", {})),
                     "parser_version": state.get("parser_version", "")},
        HEARTBEAT_NAME: {"sha256": sha256_bytes(heartbeat_bytes),
                         "bytes": len(heartbeat_bytes),
                         "source_path": heartbeat_path,
                         "heartbeat": heartbeat},
    }
    manifest = {"kind": "sync-state-in-box",
                "files": files,
                "scripts": {
                    "sync-smart-notes.py": {
                        "sha256": sha256_file(sync_py),
                        "bytes": os.path.getsize(sync_py),
                        "source_path": sync_py},
                    "build_feed_live.py": {
                        "sha256": sha256_file(feed_py),
                        "bytes": os.path.getsize(feed_py),
                        "source_path": feed_py},
                }}
    feed_bytes = _read_bytes(feed_path)
    feed = json.loads(feed_bytes.decode("utf-8"))
    manifest["bake"] = {
        "output": "hub-feed-live.json",
        "sha256": sha256_bytes(feed_bytes),
        "bytes": len(feed_bytes),
        "source_path": feed_path,
        "notes": len(feed.get("notes", [])),
        "generated_from": feed.get("generated_from", ""),
        "recorded": "by hash only - the 5 MB derived output is rebuilt "
                    "by re-running build_feed_live.py; the hash proves "
                    "the rebuild matches",
    }
    with open(os.path.join(box_dir, MANIFEST_NAME), "w",
              encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, sort_keys=True)
        handle.write("\n")
    return manifest


def rebuild_from_box(box_dir, out_dir):
    """Rebuild the local sync state from the box. Returns a list of
    {"name", "sha256", "match"} - one per restored file.

    The out directory's files are written from the box copies, then
    byte-checked against the manifest: a rebuild that does not match
    the manifest hash is reported as match False, never silently
    accepted. Raises FileNotFoundError when the box or manifest is
    missing.
    """
    manifest_path = os.path.join(box_dir, MANIFEST_NAME)
    with open(manifest_path, encoding="utf-8") as handle:
        manifest = json.load(handle)
    os.makedirs(out_dir, exist_ok=True)
    results = []
    for name in (STATE_NAME, HEARTBEAT_NAME):
        data = _read_bytes(os.path.join(box_dir, name))
        out_path = os.path.join(out_dir, name)
        with open(out_path, "wb") as handle:
            handle.write(data)
        digest = sha256_bytes(data)
        results.append({"name": name, "sha256": digest,
                        "match": digest == manifest["files"][name]["sha256"]})
    return results


def sync_state_blocks(manifest, owner="shawn"):
    """The captured sync state as blocks, so the map knows it.

    One block per captured file (state, heartbeat) plus one for the
    bake record. ``where`` carries the box path and the manifest hash;
    the state file's tracked-file count is the block's ``about``.
    """
    blocks = []
    for name, info in sorted(manifest["files"].items()):
        blocks.append({
            "id": "%s:file:sync-%s" % (owner, name.replace(".", "-")),
            "kind": "file",
            "what": "sync working memory: %s" % name,
            "about": ["sync-state", "files-tracked-%d"
                      % info.get("files_tracked", 0)],
            "who": {"owner": owner, "for": "citizen"},
            "when": {"created": "", "updated": ""},
            "where": {"github_path": "",
                      "local_path": info["source_path"],
                      "supabase_row": "",
                      "box_sha256": info["sha256"],
                      "bytes": info["bytes"]},
            "visibility": "private",
            "body": "",
            "links": [],
            "source": "factory-pipeline sync",
            "proof": "syncbox: captured verbatim into the box",
            "essence": "The sync's working memory, held in the box.",
            "owner_shared_choice": False,
            "body_open_to": [],
            "raw": info,
        })
    bake = manifest.get("bake", {})
    blocks.append({
        "id": "%s:file:sync-bake-hub-feed-live" % owner,
        "kind": "file",
        "what": "bake step: hub-feed-live.json (%d notes)"
                % bake.get("notes", 0),
        "about": ["sync-state", "bake"],
        "who": {"owner": owner, "for": "citizen"},
        "when": {"created": "", "updated": ""},
        "where": {"github_path": "",
                  "local_path": bake.get("source_path", ""),
                  "supabase_row": "",
                  "box_sha256": bake.get("sha256", ""),
                  "bytes": bake.get("bytes", 0)},
        "visibility": "private",
        "body": "",
        "links": [],
        "source": "factory-pipeline bake (build_feed_live.py)",
        "proof": "syncbox: bake output recorded by hash",
        "essence": "The bake step, recorded in the box by hash.",
        "owner_shared_choice": False,
        "body_open_to": [],
        "raw": bake,
    })
    return blocks
