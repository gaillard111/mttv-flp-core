# `deploy/` — déploiement et auto-hébergement

↑ [Retour au README du dépôt](../README.md) · [Index général](../EXPANSION.md)

Matériel d'exploitation : hébergement conteneurisé, service systemd, healthcheck,
déploiement IPFS. C'est ici qu'on entre si l'on veut **faire tourner** le code ailleurs
que sur son poste.

## Contenu

| Élément | Rôle |
|---|---|
| [`DEPLOY_HIDORA.md`](DEPLOY_HIDORA.md) | Déploiement chez un hébergeur (Hidora) — `deploy_mttv.sh` |
| [`deploy_ipfs.sh`](deploy_ipfs.sh) | Publication sur IPFS (kubo) |
| [`mttv/`](mttv/) | Conteneurisation : `Dockerfile`, `docker-compose.yml`, `entrypoint.sh`, `healthcheck.py`, `mttv.service`, `.env.example` |

## Deux avertissements

1. **`.env.example` n'est pas un secret** : il ne contient que des noms de variables.
   Aucune clé n'est versionnée, et aucune ne doit l'être.
2. **`https://docs.hidora.com` ne répond pas** depuis ce poste (échec de résolution,
   mesuré le 2026-10-27). Ce n'est pas la preuve que le service a disparu — seulement
   que cette adresse n'est pas vérifiable ici. `https://hidora.com` répond en 200.

## Où aller ensuite

- **Ce qu'on déploie** → [`../src/`](../src/) et [`../expansion_v2026.5/`](../expansion_v2026.5/)
- **Les dépendances** → [`mttv/requirements.txt`](mttv/requirements.txt)
- **Les tests avant de déployer** → [`../tests/README.md`](../tests/README.md)
