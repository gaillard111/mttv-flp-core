# Feuille de route — décidé, différé, ouvert

*Tenue à jour le 2026-11-02. Elle existe pour qu'aucune décision ne se perde entre deux sessions :
ce qui est différé y est daté, avec le critère qui permettra de dire qu'il est fait.*

Version déposée : **1.2.1**, `10.5281/zenodo.23869556`. `main` est **en avance** sur cette archive :
ce qui suit décrit cet écart, et rien ne doit être présenté comme archivé avant la 1.3.0.

---

## 1. Fait sur `main` après le dépôt (non archivé)

| # | Décision | Commit | Effet |
|---|---|---|---|
| 1 | Kit de propagation (quickstart, PoC, CONTRIBUTING, manifeste) | `59ca068` | documentation d'accueil et d'intégration |
| 2 | Quickstart anglais + glossaire `docs/i18n/` | `94231ba` | premier public non francophone |
| 3 | `Σ` sorti de la normalisation : paramètre de l'opérateur, triade sur `1 − Σ`, invariant `Ψ+B+Φ+Σ = 1` | à venir | supprime le seuil tombé à 0 et la recharge morte du souffle |
| 4 | `MicroQuorumPoreux` déclaré **démonstrateur** dans son propre module | à venir | empêche une mesure sur du bruit pseudo-aléatoire |
| 5 | Licences séparées : noyau CC-BY-NC-SA · documents CC-BY-SA · manifeste CC0 | à venir | voir [`licences.md`](licences.md) |

## 2. Différé, avec critère de sortie

### 2.1 Faire évoluer `Σ` — option (a)

**État.** `Σ` est aujourd'hui **constant** par instance. C'est honnête, mais cela retire au quatrième
pôle sa qualité de réserve : il ne s'use pas.

**À écrire.** Une loi d'extraction accumulée, par exemple `Σ ← Σ − η·max(0, tension − Σ)`, avec `η`
déclaré comme **choix**, et un plancher.

**Critère de sortie** — trois assertions, sinon on n'a rien :

1. `Ψ + B + Φ + Σ = 1` sur 100 000 flux, graine fixe ;
2. un flux de 0,20 ne bascule pas tant que `Σ > 0,20`, et bascule après que `Σ` est passé dessous ;
3. la courbe de récupération (retour de `Σ` à sa valeur nominale) est **mesurée**, pas postulée.

**Ce qu'il ne faut pas faire.** Présenter la loi de `Σ` comme dérivée : ce sera un choix, et il se
déclare comme tel.

### 2.2 Rendre le quorum mesurable

**État.** `evaluer_contexte()` tire ses nœuds et ses signaux avec `random`. Aucun chiffre de ce
module n'est citable, et son en-tête le dit maintenant.

**À faire.** Injecter les observations : `MicroQuorumPoreux(..., fournisseur_noeuds=callable)`, le
tirage restant disponible comme **démonstrateur** explicite.

**Critère de sortie.** Un chiffre reproductible, du type : *pour 7 nœuds et un seuil viable de 3, la
politique d'arrêt précoce sollicite N nœuds en moyenne sur 10 000 observations injectées à 85 % de
nœuds sains*, avec la commande qui le réimprime. Ce serait le huitième élément mesuré.

### 2.3 Noyau tétravalent

**État.** En branche d'expérimentation (`evolution/tetravalent-core`). Aucun résultat annoncé.

**À faire.** Le protocole à cinq mesures pré-enregistrées décrit dans
`AUDIT_CHANTIER_TETRAVALENT_2026-11-01.md` (dossier de diffusion, hors dépôt), deux bras, mêmes
chiffres attendus.

**Critère de sortie.** « Identique » est un résultat acceptable et probable : il prouverait que le
noyau est une **notation**, pas un mécanisme — donc qu'il relève de la pédagogie, pas de la doctrine.
Un écart, lui, deviendrait la septième graine.

### 2.4 Traductions

**Fait.** Quickstart anglais, glossaire [`i18n/en.md`](i18n/en.md).

**Différé.** `CONTRIBUTING.md` et l'index du kit en anglais.

**Critère de sortie.** Chiffres identiques au français, déclarations de choix conservées, sorties de
programme non traduites.

### 2.5 Relations de l'enregistrement Zenodo

**État.** Les identifiants liés de `23869556` sont **vides** : la ligne fausse (`is previous version
of 17940301`, qui n'est pas une version du noyau) a été supprimée, et les bonnes relations n'ont pas
été ressaisies. La chaîne des versions, elle, est portée par Zenodo lui-même.

**À faire.** Éditer les métadonnées — elles restent modifiables après publication — et ajouter :
`isVersionOf` → `20830060`, `isNewVersionOf` → `23671596`, `isSupplementTo` → le tag `v1.2.1`,
`documents` → protocole et notice.

**Critère de sortie.** Les cinq relations présentes, et le DOI de version toujours identique.

### 2.6 Forme juridique

**État.** Le collectif n'a pas d'entité ; `CITATION.cff` nomme une personne et une affiliation.

**Décidé.** Une association principale (celle qui porte compte et financements) + **une convention
bilatérale** avec une association sœur dans l'autre pays — pas deux structures complètes dès le
départ. Droit suisse (art. 60 CCS) et droit français (loi 1901) sont deux personnes morales
distinctes : il n'existe pas d'association binationale unique.

**Garde-fou.** Ne jamais inscrire dans un champ `creators` une entité qui n'existe pas juridiquement.
Désigner par écrit qui détient les droits sur le dépôt avant le premier contrat.

## 3. Interdits qui restent des interdits

- **Aucun chiffre de taille ou d'audience** issu d'une seule page de notifications : les comptes du
  29 octobre (commentaires lisibles, part des nôtres, invisibles) restent non re-mesurés.
- **Aucun semis sans mesure préalable du canal.** Le premier semis prévu reste la graine 2, chez
  `@marginalia_claude`, qui en a posé le critère.
- **Aucun tag publié déplacé, aucune version déposée réécrite.**
