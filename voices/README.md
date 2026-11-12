# voices/ — Naya canonical voice assets

**Canonical voice reference:** `naya_reference.wav` (48 kHz, 37.3 s).
This is the voice identity Naya speaks with. It is the default reference used by
`tools/render_naya_voice.py` (Chatterbox pipeline; spec:
`BRAIN/10-INTERFACES/0003-NAYA-VOICE-CHATTERBOX-SPEC-V1.md`).

**Retired 2026-10-08:** the 2-byte placeholder `Naya VOICE.wav` was removed.
Nothing in-tree referenced it (verified by grep across py/js/md/json/html);
it dated from before the canonical reference existed and was a landmine for any
consumer expecting real audio. Do not reintroduce a stub at that path — point
new consumers at `naya_reference.wav`.

**Also here:** `Naya VOICE.wav.m4a` (0.9 MB preview render of the reference voice).

Rules:
- Never commit a stub where audio is expected — a missing file fails loud, a
  silent stub fails quiet.
- Voice identity changes are a protected decision (Shawn's ear); this directory
  records assets, not decisions.
