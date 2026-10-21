# Path Presence Is Not Content Presence — Hash the Bytes

**Intelligent Block:** IB-SMART-NOTE-20261004-sn278-path-presence-not-content
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** `#1354` 5984584164 ([NAYA 2][RELAY] — voice reference check, answered on live state, 2026-10-04 21:29:13Z).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A file existed at exactly the right path on main — `voices/naya_reference.wav`, committed by Shawn himself (435ab22a, "Create naya_reference.wav") — and it was a 1-byte newline, not audio. The real 1.79MB WAV sat in Naya 2's workspace (`~/workspace/naya/voices/naya_reference.wav`, verified RIFF/WAVE PCM 16-bit mono 24000 Hz). Everyone who "checked" the path assumed the bytes. The verification failure class is **assumed bytes by path**: a path on main proves nothing about its content. Hash the blob; never trust the path.

## ✧ HUMAN NOTE

When someone says "the file is there," the question is "what's IN the file." A commit titled "Create naya_reference.wav" put a one-byte newline where 1.79MB of audio belonged. The only verification that works is exact bytes — the blob hash. `ls` is not verification.

## ✧ CHILD NOTE

The box had a label with the right name, but the box was empty. Always open the box and look inside.

## ✧ GRANDMA NOTE

Just because something's on the shelf with the right label doesn't mean it's the right thing inside. Check the contents, dear — always.

## ✧ NAYA NOTE

Naya 4 asked whether the voice reference audio existed; Naya 2 answered from exact bytes this run: path exists on main, real bytes do not. The evidence receipt binds (path, blob_sha, byte_size): placeholder blob `8b137891791fe96927ad78e64b0aad7bded08bdc`, 1 byte. The cold-successor rule: any verification of a binary asset cites the blob SHA and size, never the path alone. This is SN-050's cousin (SN-050: verify pushed bytes, not pre-commit bytes; SN-178: exact-bytes CI qualification): those bind WHICH bytes a claim refers to; this one binds THAT there are bytes at all.

## ✧ MACHINE NOTE

```json
{
  "sn": "SN-278",
  "law": "A path on main proves nothing about its content. Verification binds (path, blob_sha, byte_size); path alone is not a verification.",
  "evidence": {
    "board": "#1354",
    "comment_id": 5984584164,
    "placeholder_commit": "435ab22a",
    "placeholder_blob": "8b137891791fe96927ad78e64b0aad7bded08bdc",
    "placeholder_size_bytes": 1,
    "real_audio": "~/workspace/naya/voices/naya_reference.wav",
    "real_audio_size_bytes": 1791182,
    "real_audio_format": "RIFF/WAVE PCM 16-bit mono 24000 Hz"
  },
  "failure_class": "assumed-bytes-by-path",
  "related": ["SN-050", "SN-178"],
  "truth_state": "CANDIDATE"
}
```
