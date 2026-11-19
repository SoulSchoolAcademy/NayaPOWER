#!/bin/bash
# Decode loop: reads "@@FILE <relpath> <nbytes> <sha256>" + one base64 line
# from stdin (python's stdout) and writes each file with size+sha verification,
# retrying through EPERM flake windows. Shell writes land; python writes do not.
LIB=/home/hatch/workspace/icon-library
ok=0; fail=0; consec=0
while IFS= read -r hdr; do
  case "$hdr" in
    "@@FILE "*)
      set -- $hdr
      rel=$2; nbytes=$3; sha=$4
      IFS= read -r b64 || { echo "STREAM-EOF after $rel"; fail=$((fail+1)); continue; }
      dest="$LIB/$rel"
      mkdir -p "$(dirname "$dest")"
      if [ -s "$dest" ] && [ "$(stat -c%s "$dest")" = "$nbytes" ] && [ "$(sha256sum "$dest" | cut -d' ' -f1)" = "$sha" ]; then
        ok=$((ok+1)); consec=0; continue
      fi
      done=0
      for t in $(seq 1 15); do
        printf '%s' "$b64" | base64 -d > "$dest" 2>/dev/null
        if [ -s "$dest" ] && [ "$(stat -c%s "$dest")" = "$nbytes" ] && [ "$(sha256sum "$dest" | cut -d' ' -f1)" = "$sha" ]; then
          done=1; break
        fi
        sleep 1
      done
      if [ "$done" = 1 ]; then ok=$((ok+1)); consec=0; else echo "FAIL $rel"; fail=$((fail+1)); consec=$((consec+1)); fi
      if [ "$consec" -ge 5 ]; then echo "ABORT-POISONED-SESSION ok=$ok fail=$fail"; exit 3; fi
      ;;
    "@@DONE") echo "STREAM-DONE ok=$ok fail=$fail" ;;
    "@@NOTE"*) echo "$hdr" ;;
    *) echo "BAD-HDR: $hdr" ;;
  esac
done
echo "DECODE-RESULT ok=$ok fail=$fail"
echo "counts: 512=$(ls "$LIB/orbs/512" | wc -l) 192=$(ls "$LIB/orbs/192" | wc -l) logo=$(ls "$LIB/logo" | wc -l)"
