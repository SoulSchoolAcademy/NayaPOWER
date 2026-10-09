# Smart Block: `chat/sp-audio-msg`

Audio message with a seeded waveform: circular play button, 24-bar waveform, duration label.

## Why

Voice messages shouldn’t be black boxes. A seeded waveform with play button and duration shows the shape of what was said before you commit to listening.

- **Type:** chat
- **Source:** `Smart Spaces Page Design.html` (extracted byte-true, never rewritten)
- **CSS:** `block.css`
- **JS:** `block.js`
- **Specimen:** `specimen.html`
- **States found:** none (no state selectors in this block's CSS)
- **Dependencies:** `--sc` (space accent — used by `.sp-audio-play` background/glow and `.sp-audio-wave i`; the specimen must set it, e.g. `--sc:#7c3aed`; `spAudioMsg` sets it on the message box from `opts.accent`)

## Use it

1. Include `block.css`.
2. Include `block.js`.
3. Call `spAudioMsg({label:'0:24', accent:'#7c3aed'})` and append the returned element.

## Selectors in this block

```
.sp-audio-msg
.sp-audio-play
.sp-audio-wave
.sp-audio-wave i
.sp-audio-dur
```

## Notes

- Waveform bar heights are deterministic: seeded from the char codes of the label string (`h = 4 + ((seed * (i+7)) % 20)`), exactly as in the source. Same label → same waveform.
- The play button plays when `audioSrc` (Data URL or URL) is provided; without one it calls `opts.onPlay(box)` if given, otherwise does nothing (the source called `toast()`, which doesn't exist standalone). No fake playback invented.
- Builder: `spAudioMsg` (also exposed on `window.spAudioMsg` so `chat/sp-chat` can hand audio messages off to it).
