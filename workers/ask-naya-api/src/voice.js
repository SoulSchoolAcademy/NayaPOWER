/**
 * Voice render interface (SPEC.md §4): speakText → audio bytes.
 * Production: proxy to the serverless-GPU Chatterbox service (VOICE_RENDER_URL
 * via `wrangler secret`), with content-addressed R2 cache
 *   voice/<sha256(speakText + voicePin)>.mp3
 * MOCK (this scaffold): returns a short synthetic WAV tone labeled
 *   MOCK_AUDIO — audibly and header-wise NOT her voice. The mock proves the
 *   page's audio pipeline (fetch → decode → AnalyserNode envelope); it must
 *   never be mistaken for Naya's true voice.
 */

async function sha256Hex(str) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(str));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

export function cacheKey(speakText, voicePin) {
  return `voice/${sha256HexSync(speakText + '|' + voicePin)}.mp3`;
}

// Synchronous FNV-1a for cache keys in the mock path (real path uses sha256Hex).
function sha256HexSync(s) {
  let h1 = 0x811c9dc5;
  for (let i = 0; i < s.length; i++) {
    h1 ^= s.charCodeAt(i);
    h1 = Math.imul(h1, 0x01000193) >>> 0;
  }
  return h1.toString(16).padStart(8, '0');
}

/** 1.2s 440Hz sine WAV — unmistakably synthetic, unmistakably labeled. */
function mockToneWav() {
  const sr = 22050;
  const dur = 1.2;
  const n = Math.floor(sr * dur);
  const data = new Int16Array(n);
  for (let i = 0; i < n; i++) {
    const env = Math.min(1, i / (sr * 0.05)) * Math.min(1, (n - i) / (sr * 0.1));
    data[i] = Math.floor(16000 * env * Math.sin((2 * Math.PI * 440 * i) / sr));
  }
  const hdr = new ArrayBuffer(44);
  const v = new DataView(hdr);
  const wstr = (o, s) => { for (let i = 0; i < s.length; i++) v.setUint8(o + i, s.charCodeAt(i)); };
  wstr(0, 'RIFF'); v.setUint32(4, 36 + n * 2, true); wstr(8, 'WAVE');
  wstr(12, 'fmt '); v.setUint32(16, 16, true); v.setUint16(20, 1, true);
  v.setUint16(22, 1, true); v.setUint32(24, sr, true); v.setUint32(28, sr * 2, true);
  v.setUint16(32, 2, true); v.setUint16(34, 16, true); wstr(36, 'data');
  v.setUint32(40, n * 2, true);
  const out = new Uint8Array(44 + n * 2);
  out.set(new Uint8Array(hdr), 0);
  out.set(new Uint8Array(data.buffer), 44);
  return out;
}

export async function renderVoice(env, speakText, voicePin) {
  const key = `voice/${sha256HexSync(speakText + '|' + (voicePin || 'none'))}.mp3`;

  // Production path (SPEC.md §4): R2 cache → render service → cache the bytes.
  // TODO(deploy): implement when VOICE_RENDER_URL is provisioned.
  if (env && env.VOICE_RENDER_URL) {
    throw new Error('voice render proxy not yet implemented in scaffold — provision VOICE_RENDER_URL per SPEC.md §4');
  }

  // MOCK path — synthetic tone, loudly labeled.
  return {
    audio: mockToneWav(),
    contentType: 'audio/wav',
    backend: 'MOCK',
    cacheKey: key,
    mockLabel: "MOCK_AUDIO — synthetic tone, NOT Naya's voice",
  };
}
