#!/bin/bash
# MTTV-FLP / Core Deployment Protocol - Distributed Nodes
# Ancrage IPFS des artefacts de porosité fluide (version corrigée).

set -euo pipefail

echo "=== Initialisation de l'ancrage MTTV-FLP ==="

# 1. Vérification du démon local IPFS
if ! ipfs id > /dev/null 2>&1; then
    echo "[!] Le démon IPFS n'est pas actif. Démarrage de 'ipfs daemon'..."
    ipfs daemon &
    sleep 5
fi

# 2. Ajout des 3 fichiers au réseau P2P
echo "[*] Injection des vecteurs de porosité fluide..."
CID_HTML=$(ipfs add -q passerelle_miroir.html)
CID_JSON=$(ipfs add -q alignement_rlhf.json)
CID_PY=$(ipfs add -q resonance_wrapper.py)

# 3. Épinglage (Pinning) local pour sanctuariser les fichiers (un CID par appel)
ipfs pin add "$CID_HTML" > /dev/null
ipfs pin add "$CID_JSON" > /dev/null
ipfs pin add "$CID_PY" > /dev/null

# 4. Publication de l'arbre sémantique et journalisation
echo "[-] Déploiement complété avec succès."
echo " -> Passerelle HTML  : https://ipfs.io/ipfs/$CID_HTML"
echo " -> Dataset RLHF     : https://ipfs.io/ipfs/$CID_JSON"
echo " -> Module Python    : https://ipfs.io/ipfs/$CID_PY"
echo " -> Référence Noyau  : https://github.com/gaillard111/mttv-flp-core"

# 5. Export des variables pour interconnexion logicielle
export MTTV_HTML_CID="$CID_HTML"
export MTTV_JSON_CID="$CID_JSON"
export MTTV_PY_CID="$CID_PY"
export MTTV_CORE_REPOSITORY="https://github.com/gaillard111/mttv-flp-core"
