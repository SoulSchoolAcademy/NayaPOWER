# Player Visualizer — Amplitude Sync Missing

SN-4664 · SYSTEM / PLAYER VISUALIZER

**Created:** 2026-11-22 23:48Z

**Kinds:** Player · Visualizer · Audio · Sync

**Paired Naya Note:** NN-20261122-player-visualizer-amplitude-sync

## Hook

"The words from the video are not coming through the visualizer." His eye, live call ~16:29 MST: he HEARS the voice — the audio plays — but the visualizer does NOT move with the words. It sits static, flowing on its own, while the words go by.

## Nutshell

Play-state morphing is NOT amplitude sync. The canvas morphs while playing and rests on pause — that was observed and is real — but the visual does not listen to the real sound and move with the words: louder when he speaks, still when he pauses, like PowerCast. The amplitude-level handshake is now proven missing on his device, not just unproven. Fix round ordered on the call; the checker must prove the visual tracks the words, not just the play state.

## Human

Think of it like a singer on a stage with a light show that dances to the music — except the lights are dancing to their own song while the singer sings another. You hear the voice fine, but the lights don't move when the voice gets loud and don't rest when it pauses. The visual has to listen to the real voice — loud when he speaks, still when he pauses — the way PowerCast does. Until then the visualizer is decoration, not a visualizer.

## Child

The picture is supposed to dance with the words! But it just sits there, dancing its own dance, while the words go by! It has to listen to the real voice — big when he talks loud, still when he stops! Like PowerCast!

## Grandma

It's like this, love — the picture is supposed to dance with the words, dear! But it just sits there, dancing its own dance, while the words go by! It has to listen to the real voice, love — big when he talks loud, still when he stops, just like PowerCast!

## Naya

Make the visualizer listen to the real sound. The visual must move with the words — louder when he speaks, still when he pauses — the amplitude of the actual audio driving the canvas, not a play-state animation that flows on its own. Play-state morphing is not sync and never counts as sync. The checker proves the visual tracks the words: speak, and the visual jumps; pause, and the visual rests. Until that handshake is proven, the visualizer is decoration, and decoration is not shipped as a feature.

## What it means

1. **HE HEARS IT, HE DOES NOT SEE IT:** the audio plays; the voice is there. The visualizer does not move with the words — it sits static, flowing on its own.
2. **PLAY-STATE IS NOT SYNC:** canvas morphing while playing and resting on pause was observed — and it is not the same as amplitude sync. A visual that moves when playing and rests when paused can still be deaf to the words.
3. **AMPLITUDE IS THE HANDSHAKE:** the visual must be driven by the real sound's loudness — louder when he speaks, still when he pauses, like PowerCast.
4. **PROVEN MISSING, NOT UNPROVEN:** this is no longer "unproven on his device" — his eye saw it missing on the call. The gap is a fact, not a question.
5. **THE CHECKER PROVES TRACKING, NOT STATE:** the fix round's checker must prove the visual tracks the words — speak and it jumps, pause and it rests — not merely that it morphs while playing.

## Why it matters

1. Without amplitude sync, the player lies: the visual claims to show the voice and shows something else — and a lying visual is worse than no visual.
2. Without the handshake, every "player sync" claim is play-state only — and the machine would have called it done on a morph, the same way the checker once called a board done on "0px overflow".
3. Without his eye as the verdict, the fix round proves sync on its own machine and ships — and his device shows the same static flow again.
4. Without PowerCast as the bar, "moves a bit" passes — and "a bit" is not the experience he named.
5. Without the distinction in the record, the next builder reads "play-state sync OBSERVED" and believes sync is done — and the amplitude gap survives another round.

## What changes now

1. Fix round ordered on the call: wire the visualizer to the real audio amplitude.
2. The checker proves word-tracking, not play-state: the visual jumps when he speaks and rests when he pauses.
3. No "player sync" claim ships until the amplitude handshake is proven on his device, by his eye.
