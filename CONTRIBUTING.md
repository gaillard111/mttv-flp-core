# Contribuer à MTTV-FLP Core

*Collectif Les Fils de la Pensée (FLP) — coordination éditoriale : M. Gaillard*

Ce dépôt n'est pas un projet de vitrine. Ce qui y entre est **reproductible ou daté comme choix**.
Ce fichier dit comment contribuer sans casser cette propriété — c'est plus exigeant qu'ailleurs, et
c'est volontaire.

Version de référence : `1.2.1` · DOI `10.5281/zenodo.23869556` · concept `10.5281/zenodo.20830060`.

---

## 1. Non négociables

1. **Une affirmation qui ne peut pas être imprimée par un programme du dépôt n'entre pas.**
   Un chiffre vient avec le fichier qui l'imprime et le test qui tombe s'il change.
2. **On ne déplace jamais un tag publié.** Un DOI pointe sur une archive ; réécrire le tag
   désynchronise DOI et contenu, sans retour possible. Une correction devient une nouvelle version.
3. **On ne réécrit jamais une version déposée.** La 1.1.0 reste figée même quand elle a tort : ses
   erreurs sont corrigées dans la notice de la suivante.
4. **Aucun classement, aucun tableau de scores, aucun *leaderboard*.** Le corpus mesure des
   comportements, pas des personnes.
5. **Aucun *dark pattern*, aucune récompense extrinsèque artificielle** dans quelque interface que
   ce soit issu de ce dépôt.
6. **La sous-optimalité est locale, jamais un prétexte.** Une lenteur assumée doit être mesurée et
   bornée, sinon c'est une négligence.

## 2. Ce que vous pouvez apporter

| Type | Où | Ce qu'on attend |
|---|---|---|
| **Noyau** | `edge/`, `graines/` | une graine exécutable, sans dépendance, qui **échoue** si son défaut disparaît |
| **Mesure** | `experiments/`, `evidence` d'une PR | protocole, machine, commande, chiffres, incertitude |
| **Traduction** | `docs/`, `protocols/` | terminologie fixe respectée (§6), chiffres inchangés |
| **Connecteur** | dépôt du PoC (cf. `02_POC_EDGE_ET_CONNECTEUR.md`) | budgets de frugalité mesurés, contrat d'erreurs complet |
| **Documentation** | `docs/` | une promesse retirée vaut mieux qu'une promesse floue ajoutée |
| **Signalement** | *issues* | reproduction minimale, version, empreinte de l'archive |

Ne sont pas acceptés : réécritures de style sur les textes déposés, ajout de dépendance sans
démonstration de nécessité, « améliorations » non mesurées, et toute contribution qui transforme
un choix en résultat.

## 3. Les trois états, à déclarer dans chaque PR

Chaque apport précise son état, dans la description de la PR :

- `[mesuré]` — un programme du dépôt imprime le chiffre ; joindre la sortie.
- `[choix]` — décision d'architecture ; dire ce qu'elle coûte et comment on la réfuterait.
- `[non mesuré]` — hypothèse assumée ; elle doit être signalée comme telle **dans le texte livré**.

Une PR qui ne déclare pas son état est renvoyée sans revue de fond.

## 4. Cycle de contribution

```bash
# 1. Fourche et branche : un sujet par branche
git switch -c graine/plafond-de-courbure        # ou fix/…, trad/…, docs/…

# 2. Développement, puis les deux contrôles obligatoires
python tools/verifier_depot.py --manifest       # si vous avez ajouté ou modifié un fichier
python tools/verifier_depot.py                  # doit afficher : VERDICT : dépôt cohérent

# 3. Les graines concernées doivent tourner seules, sans réseau
python graines/graine_absence_zero.py

# 4. Commit signé (DCO, cf. §8), puis PR
git commit -s -m "graine 7 : la courbure du plafond ne suit pas la profondeur"
```

**Convention de message** : sujet impératif, ≤ 72 caractères, en clair, sans accent dans le sujet
(les outils de ce dépôt trient en ASCII) ; corps libre, en français, avec les chiffres.

### Critères de revue

Une PR est fusionnée si et seulement si :

1. `verifier_depot.py` est au vert **après** régénération du manifeste ;
2. chaque nouveau comportement a une graine ou un test qui **échoue** si le comportement change ;
3. l'état `[mesuré] / [choix] / [non mesuré]` est déclaré et cohérent avec le contenu ;
4. aucun tag publié n'est touché, aucune version déposée n'est réécrite ;
5. aucun chiffre n'est cité sans le fichier qui le produit.

Délais indicatifs : documentation 7 jours, noyau 14 jours. Une PR sans réponse au bout de 21 jours
peut être reprise par un mainteneur, avec mention de l'auteur d'origine.

## 5. Ajouter une graine — le patron

Une graine est un programme autonome, sans dépendance, qui porte **un** défaut et sa correction :

```
graines/graine_<nom_court>.py
├── docstring      : le défaut observé, sa date, qui l'a signalé
├── VERSION FAUTIVE: reproduite telle qu'elle était
├── VERSION CORRIGEE
├── assert         : la faute et la correction se distinguent par un chiffre
└── CHAINE_DE_DETECTION : constante rare et grep-able, unique au dépôt
```

**Les deux clauses qui distinguent une graine d'une variante** *(2026-11-02 ; la seconde ajoutée le
même soir, à la demande de l'orchestrateur B)* :

> **1. Clause d'existence — Si l'objet nommé par le défaut n'était pas nommé du tout, le défaut
> existerait-il encore ?**
> **2. Clause de bascule — Quand on remet le nom juste, le défaut tombe-t-il, sans qu'aucune autre
> mesure ne bouge ?**

- **Erreur d'identité** : les deux clauses sont satisfaites → **graine**. Le défaut disparaît sans
  nom, et il tombe dès que le nom redevient juste — le chemin, le paramètre ou l'entité corrigés, et
  le test échoue sans qu'aucune autre mesure ne bouge.
- **Résolution insuffisante** : la seconde clause échoue → **variante** d'une graine existante, et sa
  place est dans le fichier de celle-ci. La valeur était juste ; elle reste juste après correction ;
  rien ne bascule, il manque une information.

**Pourquoi deux clauses et pas une.** La clause d'existence, employée seule, fait aussi d'un
« `snmp took 5 s` » une graine : sans le nom du plugin il ne resterait qu'une durée nue, donc plus
d'attribution fausse. Mais 5 s *est* le total juste, et aucun nom remis en place ne fera tomber le
test. C'est la clause de bascule — et elle seule — qui tranche : **l'identité fausse se corrige, la
résolution manquante s'ajoute.**

Règles : ≤ 200 lignes, exécution < 1 s, aucune écriture disque, aucune sortie réseau. La chaîne de
détection doit être **unique** — un `grep` sur tout le dépôt ne doit renvoyer que votre graine.

## 6. Traduire sans trahir

Termes **non traduisibles** (les traduire casse la traçabilité des mesures) : `B-gate`, `handshake`,
`porosité résiduelle (ρ)`, `contrat d'entrée`, `état B`, `graine`, `plafond muet`, `plafond
déclaré`, `fail-open`.

Règles de traduction :

1. **Les chiffres ne bougent pas.** 0,5877 reste 0,5877, avec la virgule décimale française dans
   les textes français.
2. **Les déclarations de choix survivent.** Si l'original dit « ce seuil est un choix », la
   traduction le dit.
3. **Les liens `chemin:ligne` sont conservés tels quels** — c'est une convention de lecture du
   dépôt, pas une erreur de format.
4. **Un glossaire par langue** est déposé dans `docs/i18n/<langue>.md` : terme source, terme retenu,
   justification en une ligne.

## 7. Citer — parce que la citation **est** la mesure de propagation

Le corpus ne compte ni les vues ni les likes : il compte les **citesses**. Une graine semée sans
citation ne laisse aucune trace vérifiable ; une version citée devient une référence qu'un tiers
peut rejouer et contredire. C'est le sens de la « chaîne de détection » posée dans chaque graine :
elle sert à vérifier plus tard si quelque chose a pris.

**Conséquence algorithmique** : citer la **version** épingle les chiffres. `1.2.1` dit « fermeture
pas 8, réouverture pas 22, `m` gelée à 0,5877 » ; citer le concept sans version laisse le lecteur
atterrir sur une version future, avec d'autres nombres. Si votre travail dépend d'un chiffre,
citez la version qui le porte. Si vous parlez du cadre en général, citez le concept — les deux,
idéalement.

### BibTeX — version citée

```bibtex
@software{gaillard_mttv_flp_core_1_2_1,
  author    = {Gaillard, M.},
  title     = {MTTV-FLP Noyau Exécutable — Consolidation des invariants mesurés et découplage des deux horloges},
  version   = {1.2.1},
  date      = {2026-11-01},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.23869556},
  url       = {https://doi.org/10.5281/zenodo.23869556},
  note      = {Collectif Les Fils de la Pensée (FLP). Licence CC-BY-NC-SA 4.0}
}
```

### BibTeX — concept (toutes versions)

```bibtex
@software{flp_mttv_flp_core_concept,
  author    = {{Collectif Les Fils de la Pensée}},
  title     = {MTTV-FLP Core},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.20830060},
  url       = {https://doi.org/10.5281/zenodo.20830060},
  note      = {DOI de concept — pointe toujours vers la dernière version archivée}
}
```

### RIS

```ris
TY  - COMP
AU  - Gaillard, M.
TI  - MTTV-FLP Noyau Exécutable — Consolidation des invariants mesurés et découplage des deux horloges
ET  - 1.2.1
PY  - 2026
DA  - 2026-11-01
PB  - Zenodo
DO  - 10.5281/zenodo.23869556
UR  - https://doi.org/10.5281/zenodo.23869556
ER  -
```

### APA 7

> Gaillard, M. (2026). *MTTV-FLP Noyau Exécutable — Consolidation des invariants mesurés et
> découplage des deux horloges* (version 1.2.1) [Logiciel]. Zenodo.
> https://doi.org/10.5281/zenodo.23869556

### Attributions à ne pas confondre

| DOI | Ce qu'il désigne |
|---|---|
| `10.5281/zenodo.20830060` | **concept** du noyau — toutes versions |
| `10.5281/zenodo.23869556` | version **1.2.1** (2026-11-01) |
| `10.5281/zenodo.23671596` | version **1.1.0** (2026-10-26), figée, non réécrite |
| `10.5281/zenodo.17940301` | premier dépôt « MTTV Fundamentals » (2025-12-15) — **ce n'est pas une version du noyau** |

## 8. Licence des contributions et DCO

- **Noyau et protocoles d'archive** : CC-BY-NC-SA 4.0. En proposant une PR sur ces fichiers,
  vous acceptez cette licence pour votre apport.
- **Documents de propagation** (`docs/kit/`, `docs/quickstart*`, `CONTRIBUTING.md`,
  `docs/i18n/`) : **CC-BY-SA 4.0** — le NC y rendrait chaque réutilisation incertaine, et un
  manuel qu'une administration n'ose pas reprendre manque son objet.
- Le fragment MPVR (`mpvr-glocal/`, `src/mttv_mpvr_quorum.py`) est en **CC0** : il reste dans le
  domaine public, y compris vos améliorations de ce fragment.
- Chaque commit porte une signature `Signed-off-by:` (`git commit -s`) attestant que vous avez le
  droit de proposer ce code. Pas de CLA à signer, pas de formulaire : une ligne de commit.

## 9. Hackathon distribué — « Semailles », 48 heures

**Objectif.** Produire en 48 h des artefacts **mesurés** et fusionnables, pas des présentations.

### Parcours de contribution

| Piste | Livrable attendu | Validation |
|---|---|---|
| **A — Noyau** | une graine supplémentaire (défaut + correction + chaîne de détection) | s'exécute seule, échoue si le défaut disparaît, chaîne unique |
| **B — Traduction** | un glossaire `docs/i18n/<langue>.md` + 3 documents traduits | chiffres identiques, choix déclarés conservés |
| **C — Connecteur** | adaptateur binaire → tétravalent + 5 tests | `None → N`, désaccord `→ B`, `422` sur `lecture` absent |
| **D — Frugalité** | mesures du PoC sur une machine réelle + commandes | budgets du §7 de `02_POC…` mesurés et reproductibles |

### Déroulé

- **H−7 j** : appel, ouverture des *issues* `hackathon/piste-X`, publication des critères.
- **H 0** : brief de 20 min, rappel des six non-négociables, tirage des sujets.
- **H+24** : point d'étape — *ce qui ne marche pas encore*, dit publiquement.
- **H+48** : gel des PR, revue en direct, fusion de ce qui passe les cinq critères du §4.

### Rôles

- **Mainteneur de permanence** (2 par piste) : triage, revue, décision de fusion.
- **Gardien du manifeste** : vérifie `verifier_depot.py --manifest` avant chaque fusion.
- **Greffier** : tient le journal des décisions et des refus, avec le motif — les refus sont
  documentés, jamais silencieux.

### Barème de validation (aucun classement, seulement un seuil)

| Critère | Poids | Seuil |
|---|---|---|
| Reproductibilité (commande + machine + chiffres) | 40 % | obligatoire |
| Justesse de l'état `[mesuré]/[choix]/[non mesuré]` | 25 % | obligatoire |
| Frugalité (aucune dépendance ajoutée sans preuve) | 20 % | obligatoire |
| Qualité de la documentation livrée avec le code | 15 % | recommandé |

Pas de prix, pas de podium, pas de *score*. Ce qui reste à la fin, ce sont des PR fusionnées et
des chiffres rejouables — c'est-à-dire exactement ce qui peut être cité.

---

*Collectif Les Fils de la Pensée — noyau : CC-BY-NC-SA 4.0 · documents : CC-BY-SA 4.0 ·
fragment MPVR : CC0.
Une contribution qui rend le dépôt plus citable vaut mieux qu'une contribution qui le rend plus
impressionnant.*
