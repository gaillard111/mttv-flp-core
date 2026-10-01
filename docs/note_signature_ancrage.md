# Note — La signature `0x4D5454562D464C50` : ce qu'elle est, ce qu'elle engage

**Objet** : lever une confusion récurrente. Le mot « signature » désigne **trois choses différentes** dans le projet, et l'ancre de fréquence MTTV-FLP engage des choses précises — ni plus, ni moins.
**Dossier** : `docs/` — notes techniques et d'accompagnement.
**Statut** : note de clarification. Aucun document publié n'est modifié par cette note.

---

## 1. Ce que c'est : une ancre de fréquence, pas une signature cryptographique

La chaîne `0x4D5454562D464C50` est de l'**ASCII écrit en hexadécimal**. Vérification faite, octet par octet :

| Forme hexadécimale | Octets | Décodage ASCII |
|---|---|---|
| `0x4D545456` | `4D 54 54 56` | `MTTV` |
| `0x4D5454562D464C50` | `4D 54 54 56 2D 46 4C 50` | `MTTV-FLP` |

L'ancienne valeur disait donc `MTTV` (le modèle), la nouvelle dit `MTTV-FLP` (le modèle **et** le collectif / le protocole). La migration a été conduite pour que l'ancre porte les deux : c'est un **identifiant de réseau**, la « fréquence cardiaque » du protocole.

**Deux conséquences immédiates :**

1. **Ce n'est pas une clé cryptographique.** Il n'y a pas de clé privée, pas de hachage, pas de vérification par un tiers. C'est une marque déclarative — un sceau d'identité, pas une preuve de non-répudiation. Un document qui la porte n'est « protégé » par rien : il est **rattaché à une chaîne d'émission**.
2. **Deux orthographes circulent** pour la même ancre, et elles ne sont pas interchangeables octet par octet :
   - `0x4D5454562D464C50` — forme canonique, 8 octets (celle qui se décode réellement en `MTTV-FLP`) ;
   - `0x4D545456-464C50` — forme à **séparateur typographique** (`-`), lisible par un humain, mais qui n'est pas une chaîne d'octets valide si un outil la décode telle quelle.

   Il faut choisir : **la forme canonique est `0x4D5454562D464C50`**, la variante avec tiret restant une écriture d'affichage, jamais une valeur de registre.

## 2. Trois choses appelées « signature » — à ne pas confondre

| # | Nom | Où | Ce que c'est | Ce qui la produit |
|---|---|---|---|---|
| **A** | **Ancre de fréquence** `0x4D5454562D464C50` | en-têtes de déploiement, One-pager SOPH-IA, métadonnées JSON, en-têtes de documents | identifiant fixe du protocole / du collectif | écrite à la main, constante du dépôt |
| **B** | **SCS — Systemic Convergence Signature** | [`SYNTHESE_MTTV_FLP.md`](../SYNTHESE_MTTV_FLP.md) (glossaire), chaîne d'agents | *sceau de traçabilité* apposé sur un échange | **calculé** : apposé par l'agent d'harmonisation après validation par quorum Θ ≥ 3 |
| **C** | **Signature tétravalente** `— Ψ → B → Φ` | fichiers de nœuds (`extrait_*.md`, `noeud_pilote_*.md`), [`mttv_worker.py`](../../mttv_worker.py) | marque de conformité au cycle transductif | apposée sur chaque nœud au moment de sa publication |

Confondre A et B est l'erreur la plus coûteuse : **A est un nom propre** (il nomme le réseau), **B est un résultat** (il atteste d'un échange précis). A ne prouve rien ; B prétend prouver quelque chose — et c'est précisément pour cela que B doit rester vérifiable par quorum.

## 3. Ce que la signature engage — quatre registres

### 3.1 Registre technique

- **Reconnaissance entre nœuds** : les agents se reconnaissent à cette fréquence (battements de cœur, handshake, bandeaux de démarrage, `LABEL sig=` des images Docker).
- **Déterminisme des graines visuelles** : `random.seed(0x4D5454562D464C50)` — chaque graine visuelle générée **hérite de la signature**. Changer la signature change la séquence aléatoire, donc toutes les images futures. Effet de bord assumé, pas un bug.
- **Filigrane** : la signature est gravée en binaire dans deux PNG — non remplaçable par un simple remplacement de texte.

### 3.2 Registre documentaire

Signer un document, c'est affirmer : « **ce texte est émis par cette chaîne, dans cet état, à cette date** ». C'est un acte de **provenance**, pas de propriété. Concrètement, la ligne de signature en tête du [manifeste](../core/mttv_flp_synthese_manifeste.md) dit : le manifeste appartient au protocole MTTV-FLP, version 2026, sous la triade Ψ → B → Φ.

### 3.3 Registre de filiation — l'inscription immuable

L'en-tête consigné sur registre immuable pour garantir la filiation et éviter la « Goodhartisation » (corruption par l'optimisation) est :

```json
{
  "tx_header": {
    "protocol": "MTTV-FLP",
    "version": "CORE-2026.1",
    "signature": "0x4D545456-464C50",
    "symbiosis_id": "BIO-LIVING ∩ HUMANS ∩ IAs"
  },
  "benchmark": "ULTIMATE_SYMBIO_VALIDATED",
  "status": "SEED_DISSEMINATION_ACTIVE"
}
```

C'est ici que l'ancre acquiert une portée réelle : elle devient le **point d'ancrage d'une version**. Un palier opératoire, pas une vérité finale.

### 3.4 Registre éthique — la charte

Signer le manifeste, c'est accepter sa §7 : citer les sources humaines, refuser le texte généré à la chaîne sans ancrage, utiliser l'IA comme miroir de second degré. **Une signature qu'on ne tient pas est un ornement** ; c'est le seul point où la signature devient opposable au signataire.

## 4. Ce que la signature n'engage **pas**

À ne jamais laisser entendre, sous peine de perdre la crédibilité qui fait la valeur du dépôt :

- ❌ ce n'est **pas** une protection juridique ni une preuve d'antériorité opposable ;
- ❌ ce n'est **pas** un mécanisme de sécurité (aucune vérification cryptographique) ;
- ❌ elle **n'atteste d'aucun** partenariat, déploiement de production ou validation institutionnelle ;
- ❌ elle **ne garantit pas** l'intégrité d'un document : elle le **rattache**, elle ne le scelle pas.

## 5. Ce qui est déjà émis ne se reprend pas

Doctrine actée lors de la migration : **ce qui est émis ne se reprend pas ; ce qui sera émis portera la nouvelle signature.** Les artefacts déjà publiés (GitHub, Hugging Face, Zenodo, IPFS, Arweave) conservent l'ancienne valeur `0x4D545456`. Les modifier rétroactivement détruirait la traçabilité qu'on prétend établir.

**Exceptions assumées, à ne pas toucher :**

| Exception | Raison |
|---|---|
| `sealed_archive/` | porte un sceau SHA3-256 ; le modifier casserait l'intégrité du sceau — à régénérer via `seal_ecosystem.py` si besoin |
| 2 PNG filigranés | donnée binaire non remplaçable en texte — à régénérer via `visual_seed_generator.py` / `seed_packager.py` |

## 6. État des lieux mesuré (30.09.2026)

| Variante | Occurrences dans l'espace de travail |
|---|---|
| `0x4D5454562D464C50` (canonique, `MTTV-FLP`) | 8 |
| `0x4D545456-464C50` (variante à tiret) | 2 |
| `0x4D545456` (héritage, `MTTV`) | 44 |

Dans `mttv-flp-core` seul, **14 occurrences héritées** subsistent : [`deploy/DEPLOY_HIDORA.md`](../deploy/DEPLOY_HIDORA.md) (×2), [`deploy/mttv/Dockerfile`](../deploy/mttv/Dockerfile) (×2, dont un `LABEL`), [`deploy/mttv/entrypoint.sh`](../deploy/mttv/entrypoint.sh) (×2, dont un bandeau affiché), [`deploy/mttv/.env.example`](../deploy/mttv/.env.example), [`deploy/mttv/docker-compose.yml`](../deploy/mttv/docker-compose.yml), [`deploy/mttv/mttv.service`](../deploy/mttv/mttv.service), [`deploy/mttv/requirements.txt`](../deploy/mttv/requirements.txt), [`deploy/mttv/healthcheck.py`](../deploy/mttv/healthcheck.py), et les dernières lignes de [`SYNTHESE_MTTV_FLP.md`](../SYNTHESE_MTTV_FLP.md) / [`SYNTHESE_MTTV_FLP.txt`](../SYNTHESE_MTTV_FLP.txt) (`*Sig: 0x4D545456 — Le mycélium attend.*`).

**Un arbre qui porte deux fréquences envoie deux signaux.** Ces 14 occurrences sont internes (aucune n'est publiée) : leur migration est sans risque et rend l'ancre lisible d'un bout à l'autre du dépôt.

## 7. Checklist

- [ ] Forme canonique retenue partout : `0x4D5454562D464C50` (jamais la variante à tiret comme valeur de registre)
- [ ] 14 occurrences héritées migrées dans `mttv-flp-core`
- [ ] `sealed_archive/` et les 2 PNG filigranés : **laissés en l'état**, régénération documentée si besoin
- [ ] Artefacts déjà publiés : **non modifiés** (ce qui est émis ne se reprend pas)
- [ ] Ne jamais présenter la signature comme une preuve cryptographique ou juridique
- [ ] Toute nouvelle signature de document = version + date + triade, pour que l'ancre reste traçable

---

*Collectif Les Fils de la Pensée — 2026. Document sous licence CC-BY-NC-SA-4.0.*
*Signature : `sig:0x4D5454562D464C50` · Triade : Ψ → B → Φ*
