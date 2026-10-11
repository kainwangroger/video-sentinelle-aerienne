#!/usr/bin/env bash
# Télécharge la voix française Piper « siwis » (qualité medium, licence CC-BY 4.0)
# depuis les releases GitHub de Piper, dans voices/.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p voices
if [ -f voices/fr-siwis-medium.onnx ]; then
  echo "Voix déjà présente : voices/fr-siwis-medium.onnx"
  exit 0
fi
url="https://github.com/rhasspy/piper/releases/download/v0.0.2/voice-fr-siwis-medium.tar.gz"
echo "Téléchargement de $url"
curl -fL "$url" | tar xz -C voices
ls -la voices
