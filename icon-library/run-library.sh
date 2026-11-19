#!/bin/bash
# Driver: logos (cp with retry through flake windows) then the render stream.
cd ~/workspace/icon-library || exit 1
for i in $(seq 1 15); do
  cp ~/workspace/user/files/icons/naya-icon-192.png ~/workspace/user/files/icons/naya-icon-512.png ~/workspace/user/files/icons/apple-touch-icon.png logo/ 2>/dev/null
  ok=1
  for f in naya-icon-192.png naya-icon-512.png apple-touch-icon.png; do
    [ -s "logo/$f" ] || ok=0
  done
  [ "$ok" = 1 ] && break
  sleep 1
done
[ "$ok" = 1 ] || echo "LOGO-DEFERRED (session write-blocked; rerun fixes)"
echo "logos:"; sha256sum logo/*
python3 render-stream.py | bash decode-stream.sh
