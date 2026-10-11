#!/usr/bin/env bash
# Installation du module IA sur Raspberry Pi 5 (Raspberry Pi OS 64 bits) avec AI HAT+.
# Prérequis : sudo apt install hailo-all (fournit HailoRT et le paquet Python hailo_platform).
set -euo pipefail
IA="$(cd "$(dirname "$0")/.." && pwd)"
CIBLE=/opt/sentinelle/ia

sudo apt install -y python3-venv python3-opencv python3-picamera2 python3-yaml
id sentinelle >/dev/null 2>&1 || sudo useradd -r -m -G video sentinelle
sudo mkdir -p /opt/sentinelle /etc/sentinelle
sudo rsync -a --exclude travail --exclude .venv "$IA/" "$CIBLE/"
# venv avec accès aux paquets système (hailo_platform, picamera2, opencv d'apt)
sudo python3 -m venv --system-site-packages "$CIBLE/.venv"
sudo "$CIBLE/.venv/bin/pip" install -r "$CIBLE/requirements-pi.txt"
sudo mkdir -p "$CIBLE/travail" "$CIBLE/modeles"
sudo chown -R sentinelle:sentinelle /opt/sentinelle
[ -f /etc/sentinelle/env ] || { echo "SENTINELLE_JETON=a_definir" | sudo tee /etc/sentinelle/env >/dev/null; sudo chmod 600 /etc/sentinelle/env; }
sudo cp "$IA/deploiement/sentinelle-ia.service" /etc/systemd/system/
sudo systemctl daemon-reload
python3 -c "import hailo_platform" 2>/dev/null && echo "HailoRT : OK" || echo "ATTENTION : hailo_platform absent (sudo apt install hailo-all)"
echo "Copier le HEF dans $CIBLE/modeles/sentinelle_yolov8s.hef, adapter $CIBLE/configs/sentinelle.yaml,"
echo "puis : sudo systemctl enable --now sentinelle-ia"
