# i18n — glossaire anglais

*Collectif Les Fils de la Pensée (FLP) — coordination éditoriale : M. Gaillard*

Ce fichier fixe la terminologie de la version anglaise. Il existe pour une raison précise : une
traduction qui arrondit un seuil, ou qui rend « choix » par « result », falsifie un document qui se
voulait vérifiable. Toute nouvelle traduction ajoute sa ligne ici avant d'être relue.

## 1. Termes non traduits

Ces termes restent en français dans la version anglaise : les traduire romprait la correspondance
avec les fichiers, les mesures et les citations existantes.

| Terme | Pourquoi il ne se traduit pas |
|---|---|
| `B-gate` | nom du module et de la bascule ; déjà un composé anglais |
| `handshake` | idem, et nom du protocole (`mttv/handshake@1`) |
| `fail-open` | nom du défaut mesuré ; le renommer rendrait le défaut introuvable |
| `graine` / `graines` | nom du dossier et des six programmes ; renvoie à `graines/*.py` |
| `porosité résiduelle (ρ)` | la traduction anglaise est utilisée, mais `ρ` reste l'identifiant |
| `plafond muet`, `plafond déclaré` | paire mesurée ; rendue par *silent ceiling* / *declared ceiling*, avec le français en note à la première occurrence |

## 2. Correspondances retenues

| Français | Anglais | Justification |
|---|---|---|
| contrat d'entrée | **input contract** | littéral, et c'est un contrat au sens d'API |
| état B (Belnap-Dunn) | **state B** | la lettre est un identifiant logique, pas une initiale |
| valeur tétravalente | **tetravalent value** | — |
| couple (encodage) | **pair** | `T=[1,1]` est une paire, pas un vecteur |
| habitabilité (`h`) | **habitability** | grandeur, pas propriété morale |
| péremption | **staleness** | désigne le compteur de pas sans lecture ; *expiry* prêterait à confusion avec un délai |
| escalade | **escalation** | — |
| clôture | **closure** | l'acte de lever le verrou, distinct de la réouverture |
| réouverture | **reopening** | — |
| choix (état de connaissance) | **choice / decision** — jamais *result* | c'est le cœur de la règle des trois états |
| mesuré | **measured** | avec le fichier qui l'imprime |
| non mesuré | **not measured** | — |
| politique d'arrêt précoce | **early-stop policy** | — |
| quorum poreux | **porous quorum** | — |
| démonstrateur | **demonstrator** | jamais *prototype* au sens de « bientôt prêt » |

## 3. Règles de traduction

1. **Les chiffres ne bougent pas.** `0,5877` devient `0.5877` (séparateur décimal), mais la valeur
   est identique. Aucun arrondi, aucune « simplification ».
2. **Les déclarations de choix survivent.** Si le document source dit qu'un seuil est un choix, la
   traduction le dit. Une traduction qui promeut un choix en résultat est refusée.
3. **Les liens `chemin:ligne` sont conservés** : c'est la convention de lecture du dépôt.
4. **Les statuts de commande restent en français** quand ils sont imprimés par un programme
   (`"B-GATE ACTIVÉE : …"`, `VERDICT : dépôt cohérent`). Traduire une sortie de programme rend le
   document non reproductible.
5. **Toute traduction cite la version** dont elle est issue : `1.2.1`, `10.5281/zenodo.23869556`.

## 4. État des traductions

| Document | Français | Anglais | État |
|---|---|---|---|
| Quickstart | [`docs/quickstart.md`](../quickstart.md) | [`docs/quickstart.en.md`](../quickstart.en.md) | version 1.2.1, chiffres vérifiés ligne à ligne |
| Contribution | [`CONTRIBUTING.md`](../../CONTRIBUTING.md) | — | à faire |
| Manifeste | [`docs/kit/04_MANIFESTE_POST_HYPERSCALER.md`](../kit/04_MANIFESTE_POST_HYPERSCALER.md) | — | **volontairement en français** : le registre politique s'adresse d'abord à un public francophone |
| Kit — index | [`docs/kit/README.md`](../kit/README.md) | — | à faire, si le PoC trouve preneur |
