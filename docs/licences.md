# Licences — qui couvre quoi, et pourquoi

*Décision du 2026-11-02. Remplace l'ancienne règle implicite « tout en CC-BY-NC-SA ».*

Le dépôt mélangeait deux choses : un **noyau** qu'on veut protéger de l'extraction, et des
**documents** qu'on veut voir circuler. Le `NC` (pas d'usage commercial) sert le premier et gêne
les seconds : chaque réutilisation devient une incertitude, et une administration préfère renoncer
plutôt que consulter un juriste.

## 1. Qui est sous quelle licence

| Périmètre | Fichiers | Licence | Pourquoi |
|---|---|---|---|
| **Noyau** | `src/`, `edge/`, `experiments/`, `expansion_v2026.5/`, `graines/` | **CC-BY-NC-SA 4.0** | position doctrinale : pas d'extraction commerciale du travail de mesure |
| **Documents de propagation** | `docs/kit/`, `docs/quickstart.md`, `docs/quickstart.en.md`, `CONTRIBUTING.md`, `docs/i18n/`, `docs/licences.md` (ce fichier) | **CC-BY-SA 4.0** | doivent être reprenables par une école, une ONG, une collectivité, sans négociation |
| **Manifeste** | `docs/kit/04_MANIFESTE_POST_HYPERSCALER.md` | **CC0 1.0** | un texte qui appelle à la diffusion la plus large ne peut pas en limiter l'usage |
| **Fragment MPVR** | `mpvr-glocal/`, `src/mttv_mpvr_quorum.py` | **CC0** | domaine public assumé depuis l'origine |
| **Protocoles et notices d'archive** | `protocols/`, `docs/notice_*.md`, `docs/protocole_*.md` | **CC-BY-NC-SA 4.0** | ils portent des chiffres publiés : ils suivent le noyau qu'ils décrivent |

## 2. Ce que cela change pour vous

- Vous pouvez **reprendre, traduire, adapter** les documents de propagation, y compris dans un
  cadre commercial, à condition de citer et de partager à l'identique (CC-BY-SA).
- Vous pouvez **faire n'importe quoi** du manifeste, y compris sans attribution (CC0).
- Pour le noyau, l'usage commercial reste exclu, et toute œuvre dérivée reste sous la même licence.

## 3. Non-rétroactivité — à ne pas confondre

L'archive déposée sous **`10.5281/zenodo.23869556`** (version 1.2.1) reste **CC-BY-NC-SA 4.0 pour
l'ensemble de son contenu**, puisqu'elle a été publiée sous cette licence. Cette page ne vaut que
pour les versions postérieures — c'est-à-dire `main` aujourd'hui, et la prochaine archive.

Ce n'est pas une argutie : quelqu'un qui télécharge l'archive de la 1.2.1 doit pouvoir s'en tenir
à ce qui y est écrit, et ce qui y est écrit dit CC-BY-NC-SA.

## 4. Comment citer

| Ce que vous citez | Forme de l'attribution |
|---|---|
| le noyau | `Gaillard, M. — Collectif Les Fils de la Pensée (FLP), MTTV-FLP Core v1.2.1, CC-BY-NC-SA 4.0, DOI 10.5281/zenodo.23869556` |
| un document de propagation | `Collectif Les Fils de la Pensée (FLP), « <titre> », CC-BY-SA 4.0, github.com/gaillard111/mttv-flp-core` |
| le manifeste | aucune attribution requise (CC0), mais la citer reste la seule façon de rendre la reprise traçable |

Les formats complets (BibTeX, RIS, APA) sont dans [`CONTRIBUTING.md`](../CONTRIBUTING.md), § 7.
