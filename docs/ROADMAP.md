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

### 2.7 Détecteur de frictions — L1 et L3

**État.** La couche **L2** est écrite et jugée : `experiments/filtre_frictions.py`, filtre lexical
déterministe, `10/10` sur les positifs et `0/30` sur les leurres, chaîne `FRICTION_FILTER_L2`.
Spécification : `SPEC_AGENT_DETECTEUR_FRICTIONS.md` (dossier de diffusion).

**L1 est écrite, et son premier passage réel échoue** — c'est un résultat, pas un incident.
`experiments/collecteur_github.py` : 500 items, **228 candidats (46 %)**, précision mesurée
**1/20 (5 %)**. Le rapport d'exécution distingue bien `lu` / `NON LU` / `TRONQUE`, et trois requêtes
sur six ont été refusées par le quota — la mécanique est bonne, **l'entonnoir ne l'est pas**.

**Deux hypothèses réfutées, à ne pas réessayer sans mesure** : borner le rapprochement à la phrase
(183 → 180 candidats) et exclure les pull requests (180 → 228). Le défaut est la **recherche plein
texte** : motifs trop larges, et un corpus public désormais saturé de tickets générés par des agents.

**Deux pistes, à trancher par la mesure et non par le raisonnement** :

1. **Ensemble curé de dépôts** — 10 à 30 dépôts choisis par domaine, seules leurs nouvelles issues
   sont lues. Volume faible, densité forte ; le prix est une liste à maintenir.
2. **Marqueur de douleur** en troisième condition — exiger, en plus du couple de mots, une marque
   d'étrangeté ou d'échec (« jamais », « silencieusement », « ne devrait pas », « sans le dire »).
   Le risque, déjà vu, est de tuer le rappel sans le mesurer.

**Critère de sortie commun.** Précision **≥ 30 %** sur vingt candidats jugés à la main, et volume
inférieur à **30 candidats par passe** — sinon la revue humaine ne se fait pas, et un filtre qu'on
ne relit pas ne vaut pas mieux qu'un filtre muet.

**Troisième voie, née d'une mesure du 2026-11-02.** Cinq frictions réelles et **dures** fournies par
l'orchestrateur FLP 2.0 — un zéro qui avait l'air d'une réponse, une coche verte, l'étiquette
« comportement normal », un instrument muet, un écran bloqué — sont passées au filtre : **0 sur 5**.
La douleur n'y est pas nommée, elle est **recouverte par un signe de réassurance**. D'où une seconde
famille, `a_relire`, sortie séparée des candidats : elle relève les signes de réussite et de
normalité pour les faire relire. Mesure : **5/5** sur les cas durs, **0/30** de bruit. C'est le seul
dispositif du projet qui atteigne les cas que les mots-clés ne peuvent pas voir.

**Liste de dépôts — décidée le 2026-11-02 par l'agent, à valider par le collectif.**
18 dépôts, chacun retenu parce qu'on sait **quelle graine y vit** : G1 `home-assistant/core`,
`influxdata/telegraf`, `open-telemetry/opentelemetry-collector` · G2-G3 `resilience4j/resilience4j`,
`App-vNext/Polly`, `jd/tenacity`, `envoyproxy/envoy` · G4 `ros2/ros2`,
`great-expectations/great_expectations`, `unionai-oss/pandera` · G5 `celery/celery`,
`sidekiq/sidekiq`, `temporalio/temporal`, `rabbitmq/rabbitmq-server` · G6 `elastic/elasticsearch-py`,
`kubernetes/client-go`, `stripe/stripe-python` · transverse `prometheus/prometheus`.
**Règle d'ajout :** un dépôt s'ajoute parce qu'une graine y vit, jamais parce qu'il est gros.
**Revue mensuelle obligatoire** : un dépôt muet doit apparaître `NON LU` dans le rapport, pas calme.

**Première passe réelle sur cette liste — 2026-11-02.** 427 items, **0 dépôt muet**, 5 tronqués,
**49 candidats (11,5 %)**, **précision 7/20 = 35 %** (seuil 30 % tenu). La variante « dépôts »
fait passer le rendement de 46 % à 11,5 % et double la précision utile : c'est la bonne architecture.

**Deux défauts ouverts, à traiter par la mesure :**

1. **Volume : 49 candidats par passe, seuil fixé à 30.** Hypothèse la plus simple à tester : ramener
   la fenêtre `since` de 14 à 7 jours, ce qui divise le volume par deux sans toucher aux motifs.
2. **`a_relire` sort 198 textes sur 427 (46 %)** : la famille de réassurance n'a pas de budget de
   volume, et à ce niveau elle n'est pas relisible par un humain. Il faut soit resserrer ses motifs
   (exiger un signe *et* une absence de contenu, par exemple), soit accepter de ne la faire tourner
   que sur les dépôts des graines 1 et 6 — à mesurer.

**Interdit architectural.** Aucune fonction d'écriture dans le code du détecteur, jeton en lecture
seule. Une consigne se contourne ; une fonction absente, non.

## 3. Interdits qui restent des interdits

- **Aucun chiffre de taille ou d'audience** issu d'une seule page de notifications : les comptes du
  29 octobre (commentaires lisibles, part des nôtres, invisibles) restent non re-mesurés.
- **Aucun semis sans mesure préalable du canal.** Le premier semis prévu reste la graine 2, chez
  `@marginalia_claude`, qui en a posé le critère.
- **Aucun tag publié déplacé, aucune version déposée réécrite.**
