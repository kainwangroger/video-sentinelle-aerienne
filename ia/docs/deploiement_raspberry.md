# Déploiement sur Raspberry Pi 5 + AI HAT+ 26 TOPS

## 1. Système

1. Raspberry Pi OS 64 bits (Bookworm ou plus récent), à jour : `sudo apt update && sudo apt full-upgrade`.
2. AI HAT+ monté sur le connecteur PCIe, refroidissement actif du Pi (ventilateur officiel).
3. Logiciels Hailo : `sudo apt install hailo-all` puis redémarrage.
4. Vérification : `hailortcli fw-control identify` (doit afficher HAILO8).
   Noter la version de HailoRT : le HEF doit être compilé avec un DFC compatible.
5. PCIe Gen 3 (débit) : `sudo raspi-config` → Advanced → PCIe Speed → Gen 3.

## 2. Module IA

```bash
git clone <dépôt> && cd <dépôt>/ia
deploiement/installer_pi.sh          # dépendances Python, dossiers, service systemd
cp sentinelle_yolov8s_hailo8.hef modeles/sentinelle_yolov8s.hef
nano configs/sentinelle.yaml         # source caméra, zone d'intérêt, liaison
```

Le jeton de la liaison est placé dans `/etc/sentinelle/env` (`SENTINELLE_JETON=...`, droits 600),
le certificat de la station dans `/etc/sentinelle/station_ca.pem` (fournis par le lot réseau).

## 3. Lancement

```bash
# essai manuel sur vidéo enregistrée
python -m sentinelle_ia --config configs/sentinelle.yaml --source videos/essai.mp4 --sequence BANC-01
# service (démarrage automatique, redémarrage en cas d'arrêt)
sudo systemctl enable --now sentinelle-ia
journalctl -u sentinelle-ia -f
```

Le lot embarqué choisit le **mode de lancement** (service au démarrage, ou commande depuis la
station). Le module ne commande jamais l'aéronef.

## 4. Mesures sur banc

```bash
python outils/mesurer_embarque.py --config configs/sentinelle.yaml --duree 1800 --rapport rapports/banc_30min.md
```
Débit, latence image-décision, température, mémoire, charge. Le courant est relevé sur
l'instrument du banc. Essai prolongé : vérifier l'absence de bridage thermique (`vcgencmd get_throttled`).

## 5. Montage

Alimentation par convertisseur régulé 5 V / 5 A depuis la batterie, fixation anti-vibration,
câblage protégé. Le bilan de masse et de courant est validé avec le lot mécanique et électronique
avant tout vol.
