Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

gap-t1271-lane4 re-pinned its analysis artifact after proving the parent receipt's pin sat BETWEEN two writes: the pin 424653dd... was taken ~11:09:33Z, and the file was rewritten 11:13:09Z unpinned — so the pin testified about neither moment. The rule: **a pin is a promise about a fixed moment — write the pin LAST, after the last byte lands.** A pin taken between two writes is a lie about both: it cannot describe the bytes as-written, and it cannot describe the bytes as-filed. The re-pin 04e278bac5... was taken at the frozen mtime, 4/4 fresh reads byte-identical, nothing edited — the pin and the artifact now share a moment.

## 🩷 HUMAN NOTE

Shawn — a receipt quoted a fingerprint of an analysis file as proof, but the file was edited after the fingerprint was taken. The old fingerprint described a version of the file that never shipped; the shipped file never got fingerprinted. gap-t1271 caught it honestly: the pin was taken between two writes, so it was a lie about both. The re-pin was taken after the final write, with four fresh reads confirming byte-identical bytes. The standing rule this earned: receipt pins are taken after the last write, never before it — and the filing-time re-hash automation is now a named next action so write-then-tweak-then-ship can never stale a pin again.

## 🟣 CHILD NOTE

Take a photo of your LEGO build — then add two more bricks — then say the photo shows the final build. It doesn't. The photo shows the build as it was between steps. A fingerprint of a file works the same way: it must be taken after the last brick is placed. A fingerprint taken between two edits is a promise about a moment that no longer exists.

## 🔵 GRANDMA NOTE

It's like a jeweler's appraisal written before the stone was reset — the certificate describes a necklace that doesn't exist anymore, and the necklace that does exist has no certificate. The appraisal has to come after the work is done. Fingerprints on files are the same: the fingerprint comes after the final save, never before it.

## 🟠 NAYA NOTE

Pin discipline, Naya to Naya: a pin is a claim of the form "artifact A was exactly bytes B at moment T." Any unpinned write to A after T breaks the claim's referent — the receipt then proves a phantom. The gap-t1271 case is the byte-exact worked proof: pin 424653dd... at ~11:09:33Z, file rewritten 11:13:09Z unpinned, receipt quoted the pin as filing evidence. Caught and corrected same session: re-pin 04e278bac5... at the frozen mtime, 4/4 fresh reads byte-identical, nothing edited. Until the standing machinery exists (automated re-hash at receipt-filing time — named as next action, not yet built), the filing checklist carries the rule: re-derive every pin AFTER the artifact's final write; any pin whose timestamp precedes the artifact's last write is rejected, not repaired.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1825-pin-after-last-write",
  "lesson": "A pin is a promise about a fixed moment: write the pin LAST, after the artifact's last byte lands. A pin taken between two writes is a lie about both. Re-derive pins at filing time, never quote a mid-write pin.",
  "applies_when": ["pin", "fingerprint", "receipt", "hash", "evidence-pin", "failure: stale-pin"],
  "enforcement": "Receipt filing re-derives the pin after the final write of the artifact; any pin whose timestamp precedes the artifact's last write is rejected. Standing-machinery candidate (named, not built): automated re-hash at receipt-filing time so write-then-tweak-then-ship cannot silently stale a pin. Caught live in gap-t1271-lane4: parent pin 424653dd... at ~11:09:33Z, file rewritten 11:13:09Z unpinned; re-pin 04e278bac5... at frozen mtime, 4/4 fresh reads byte-identical.",
  "evidence": [
    "hidden_files/learning-events-2026-10-22-12.md (gap-t1271-lane4 violation caught and corrected: pin 424653dd at ~11:09:33Z vs file rewritten 11:13:09Z unpinned; re-pin 04e278bac5 at the frozen mtime, 4/4 fresh reads byte-identical; named next action: automated re-hash at receipt-filing time)"
  ]
}
```
