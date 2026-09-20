# 🔱 NAYANET — MEDIA + POWERCAST BLUEPRINT

## Purpose

Make media a learning interface rather than a decorative content feed.

## Powercast

Powercast is a core Naya Power experience featuring Shawn + Naya and can contain:

- video;
- audio;
- chapters;
- transcript;
- contextual prompts;
- Ask Naya about this;
- save insight;
- continue learning;
- Five-Day Challenge entry points.

## Playback

Required baseline:

- explicit play control;
- pause;
- progress;
- volume/mute;
- captions/transcript where available;
- responsive player;
- mobile-safe controls;
- keyboard controls where supported;
- honest unavailable-media state.

## Voice

Browser speech output may provide Naya voice where supported.

Browser dictation may provide speech input where supported.

Neither capability may be treated as universally available.

## Media intelligence

Future Naya runtime should be able to associate media with intelligence events:

`media → transcript → timestamp → insight → note → report → optional contribution`

## Embed behavior

Audio/video can operate inside the Cloudflare-hosted iframe when initiated by user interaction.

Do not assume autoplay across browser policies.

## Design law

The media player should feel like part of the intelligence instrument, not an unrelated third-party widget.
