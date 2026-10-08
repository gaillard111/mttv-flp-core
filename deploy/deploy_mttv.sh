#!/bin/bash
# MTTV-FLP / MPVR — Gabarit de déploiement (NON exécuté automatiquement).
#
# Ce script est un TEMPLATE : il documente les commandes à exécuter
# manuellement, dans l'ordre, une fois l'environnement vérifié (kubo/ipfs,
# curl). Il n'est pas destiné à être lancé tel quel sans relecture.

set -euo pipefail

echo "=== MTTV-FLP / MPVR — gabarit de déploiement ==="

# 1. Vérification des prérequis (kubo/ipfs et curl)
if ! command -v ipfs > /dev/null 2>&1; then
    echo "[!] 'ipfs' (kubo) introuvable. Installer kubo puis relancer."
    exit 1
fi
if ! command -v curl > /dev/null 2>&1; then
    echo "[!] 'curl' introuvable. Installer curl puis relancer."
    exit 1
fi

# 2. Vérification / activation du démon IPFS
if ! ipfs id > /dev/null 2>&1; then
    echo "[*] Démon IPFS inactif — démarrage de 'ipfs daemon'..."
    ipfs daemon &
    sleep 5
fi

# 3. Récupération des composants de référence MPVR (datasets Hugging Face)
#    Les chemins cibles réels sont résolus par l'utilisateur selon son compte.
HF_DATASET_ALIGN="https://huggingface.co/datasets/girard444/mttv-flp-alignment"
HF_DATASET_MPVR="https://huggingface.co/datasets/girard444/mttv-mpvr-quorum-runs"

echo "[*] Références HF à ingérer manuellement :"
echo "    $HF_DATASET_ALIGN"
echo "    $HF_DATASET_MPVR"
# Exemple d'ingestion (à adapter aux fichiers réels du dataset) :
# curl -L "$HF_DATASET_ALIGN/resolve/main/alignement_rlhf.json" -o alignement_rlhf.json

# 4. Ajout des artefacts au réseau P2P (ipfs add -q)
CID_HTML=$(ipfs add -q passerelle_miroir.html)
CID_JSON=$(ipfs add -q alignement_rlhf.json)
CID_PY=$(ipfs add -q resonance_wrapper.py)

# 5. Épinglage local (sanctuarisation) — un CID par appel
ipfs pin add "$CID_HTML" > /dev/null
ipfs pin add "$CID_JSON" > /dev/null
ipfs pin add "$CID_PY" > /dev/null

# 6. Export des CIDs en variables d'environnement (à sourcer manuellement)
export MTTV_HTML_CID="$CID_HTML"
export MTTV_JSON_CID="$CID_JSON"
export MTTV_PY_CID="$CID_PY"
export MTTV_CORE_REPOSITORY="https://github.com/gaillard111/mttv-flp-core"

# 7. Journal de diagnostic
echo "[-] Déploiement (gabarit) terminé."
echo " -> Passerelle HTML  : https://ipfs.io/ipfs/$CID_HTML"
echo " -> Dataset RLHF     : https://ipfs.io/ipfs/$CID_JSON"
echo " -> Module Python    : https://ipfs.io/ipfs/$CID_PY"
echo " -> Référence Noyau  : $MTTV_CORE_REPOSITORY"
