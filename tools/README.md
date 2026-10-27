# `tools/` — outillage du dépôt

↑ [Retour au README du dépôt](../README.md) · [Index général](../EXPANSION.md)

Un seul outil, sans dépendance, en lecture seule : il ne corrige rien, il constate. Un
ménage qui n'est pas outillé se défait en trois semaines.

## [`verifier_depot.py`](verifier_depot.py)

```bash
python tools/verifier_depot.py              # vérifie, code de sortie 0 ou 1
python tools/verifier_depot.py --manifest   # régénère MANIFESTE_FICHIERS.sha256
python tools/verifier_depot.py --liste      # détail de ce qui a été contrôlé
```

Six contrôles :

| # | Contrôle | Ce qu'il attrape |
|---|---|---|
| 1 | Liens internes | fichier cité inexistant. **Le suffixe `:N` est retiré avant vérification** — l'oublier produit des dizaines de faux positifs |
| 2 | Doublons exacts (sha256) | copies non déclarées. Les trois copies de `hf/space/` sont déclarées assumées |
| 3 | Copies de déploiement | divergence entre `src/` (ou `mpvr-glocal/src/`) et `hf/space/` |
| 4 | **Navigation** | document **inatteignable** depuis le README (il existe, il est publié, personne n'y arrive), dossier sans porte d'entrée `README.md`/`INDEX.md`. C'est un lien mort invisible : aucun 404, juste un fichier que personne ne trouve |
| 5 | Affirmations | réapparition d'un décompte de fichiers périmé ou d'un badge de version périmé ; disparition d'un chiffre qui doit rester (seuil `0,6849`, DOI de version) |
| 6 | Manifeste | fichier non inscrit, absent, ou empreinte modifiée |

État au 2026-10-27 : **`VERDICT : dépôt cohérent`**, 6 contrôles sur 6 — et
**0 document orphelin sur 54**, contre 21 sur 43 avant le ménage.

## Quand le lancer

Avant **chaque** release, et après toute modification d'un lien, d'un chiffre cité ou
d'un fichier de `hf/space/`. Si le manifeste change, c'est un choix : le régénérer et
l'inscrire dans le même commit.

## Où aller ensuite

- **Ce que le manifeste recense** → [`../MANIFESTE_FICHIERS.sha256`](../MANIFESTE_FICHIERS.sha256)
- **L'historique des versions** → [`../CHANGELOG.md`](../CHANGELOG.md)
