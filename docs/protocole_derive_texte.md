---
tags:
  - mttv-flp
  - rmp
  - protocole
  - falsifiabilite
  - transmission
license: CC-BY-NC-SA-4.0
language: fr
---

# Protocole — Dérive d'un texte selon le degré de contrainte

**Statut : protocole rédigé, non lancé.** À exécuter après validation. Coût estimé : une à deux heures, 12 à 18 personnes, aucun outil technique, aucun arbitrage doctrinal, aucun droit à trancher.

**Pourquoi ce protocole existe.** La RMP affirme une **zone critique doublement bornée** : trop peu de contrainte → dispersion ; trop de contrainte → rigidité ; entre les deux, la transduction. La thèse défendue oralement par le collectif ajoute que le langage possède une **souplesse et une compression** supérieures aux mathématiques. Ces deux propositions sont, en l'état, des **ancrages heuristiques** au sens du protocole Σ₂ (forme forte, mesure indépendante absente). Ce protocole construit la mesure manquante — sur le corpus lui-même, par des moyens ordinaires, sans banc d'essai.

---

## 1. Prédiction et falsificateur (à fixer AVANT de lancer)

| | |
|---|---|
| **Prédiction de la RMP** | La **rétention du sens** et la **fidélité** suivent une courbe **non monotone** en fonction du degré de contrainte : maximale dans une zone intermédiaire, dégradée aux deux extrémités (dispersion / rigidité) |
| **Falsificateur** | Si la rétention croît **monotonement** avec la contrainte, la RMP est **prise en défaut sur cette focale** — et il faut le consigner comme tel |
| **Seuil de décision** | Écart de rétention entre L1 et ses deux voisins (L0 et L2) **≥ 1 point sur 5**, sur au moins 2 chaînes sur 3, aux deux régimes testés |

**Aucun résultat ne sera interprété après coup.** Le seuil est posé ici pour qu'un résultat défavorable soit lisible comme défavorable.

## 2. Matériel textuel

Trois régimes pour un **même contenu source** (un passage inédit d'environ 100 mots, extrait de [`protocols/rmp_mecanisme_pre_transducteur.md`](../protocols/rmp_mecanisme_pre_transducteur.md) §3 — contenu que les participants n'ont pas lu) :

| Régime | Forme | Contrainte |
|---|---|---|
| **L0 — dispersion** | prose libre, aucune contrainte | quasi nulle |
| **L1 — zone critique** | prose contrainte : 3 phrases maximum, une idée par phrase | moyenne |
| **L2 — rigidité** | forme figée : quatrain rimé, 20 mots exacts | forte |

Le contenu doit être **le même** dans les trois régimes : seules la forme et la contrainte changent. Toute différence de contenu invalide la comparaison.

## 3. Dispositif — téléphone arabe contrôlé

- **3 chaînes par régime** (9 chaînes au total), **5 relais par chaîne** → 45 transmissions.
- Chaque relais reçoit **uniquement la production du relais précédent**, avec la consigne : *« Retiens ce texte, puis restitue-le de mémoire, dans la forme de ton choix. »*
- Les participants **ne connaissent pas l'hypothèse** ni les autres régimes. Un même participant ne figure pas deux fois dans une chaîne.
- Idéalement, les participants ne sont **pas membres du collectif** (éviter la résonance complice) ; à défaut, la moitié au moins doit être extérieure.

## 4. Mesures (trois juges indépendants, qui ne connaissent pas l'hypothèse)

1. **Rétention fonctionnelle** — la thèse centrale est-elle encore présente ? note de 0 à 5.
2. **Divergence** — distance de sens entre la production du relais 1 et celle du relais 5 : note de 0 à 5.
3. **Excès de sens** — le texte final produit-il *plus* que le texte initial (nouvelle implication, formulation qui ouvre) ? oui / non.

**Indicateur principal :** `Δκ_prose = (rétention L1) − (rétention L0)` et `Δκ_forme = (rétention L1) − (rétention L2)`. Les deux **doivent être positifs** pour que la double borne soit observée.

## 5. Fiche de résultat (à consigner dans le dépôt, quel qu'il soit)

| Régime | Chaîne | Rétention (0-5) | Divergence (0-5) | Excès de sens | Verdict |
|---|---|---|---|---|---|
| L0 | 1 | | | | |
| L1 | 1 | | | | |
| L2 | 1 | | | | |
| … | … | | | | |

À verser sous `tests/` ou `docs/`, avec la date, le nombre de participants et **les anomalies observées**. Un résultat qui infirme la RMP doit être déposé **au même endroit et avec la même visibilité** qu'un résultat confirmant — sans quoi le corpus perd la seule chose qui le différencie d'un dogme.

## 6. Ce que ce protocole ne prouve pas

- Il ne mesure **pas** la RMP en général, mais **une** focale : la transmission humaine d'un texte court, en une langue, sur un effectif réduit.
- Il ne compare **pas** directement langage et mathématiques ; il compare **trois degrés de contrainte dans une même langue**. La comparaison avec un texte mathématique serait une **seconde expérience**, avec un autre apparie­ment de contenu.
- Trois chaînes ne donnent **aucune** portée statistique. Elles donnent un **ordre de grandeur** et une **détection d'effet** — ce qui suffit à faire passer un ancrage de *heuristique* à *moyen*, ou à le réfuter.
- Un effet non monotone **ne valide pas** la RMP : il la rend **compatible** avec une mesure indépendante. C'est un gain de statut, non une preuve.

## 7. Conditions de lancement

1. Le **falsificateur du §1** est accepté par le collectif, tel quel, avant toute collecte.
2. Les **trois versions** (L0, L1, L2) du même contenu sont écrites et **figées** (fichier daté, commit) avant de recruter.
3. Les juges sont désignés **avant** la collecte et ne connaissent pas l'hypothèse.
4. Le lot est **rejouable** : contenu source, versions, fiches et verdict sont versionnés ensemble — un protocole qui ne peut pas être rejoué est le contre-exemple de sa propre thèse.
