---
tags:
  - mttv-flp
  - arbitrages
  - regles-de-conduite
  - transmission
license: CC-BY-NC-SA-4.0
language: fr
---

# Règles de transmission — conduite d'un agent sur ce corpus

**Objet.** Ce que l'agent doit faire, et surtout ne pas faire, quand il reprend le dépôt. Ces règles
sont écrites ici pour une raison mesurée : un agent n'a pas de mémoire d'une session à l'autre, et
**une consigne qui n'est pas dans un fichier n'existe pas**.

Elles sont datées du **2026-11-21**, au lendemain d'une tentative refusée (deux graines « Post-Riemann »,
voir le [registre des refus](arbitrages_rmp.md:155)).

---

## R1. Ne pas rendre la décision à l'utilisateur

**Énoncé par 👤 le 2026-11-21, 10 h 25 UTC : « Règle absolue, à appliquer TOUJOURS, sans exception. »**
L'outil de question (`ask_followup_question`) est **interdit** ; aucune exception.

Conséquences opératoires :

1. **Décider, puis exécuter.** Une alternative ne se propose pas en menu, elle se tranche et se motive.
2. **Si une information manque** : la chercher dans le corpus — fichier, `grep`, exécution. C'est
   presque toujours là qu'elle est, et la chercher est le travail.
3. **Si elle n'y est pas** : écrire le manque **comme tel** — « non mesuré », « non trouvé », « à
   produire » — au lieu de le convertir en question. Un manque déclaré est une donnée ; un manque
   converti en question est un **transfert de charge**.
4. **Les options écartées restent utiles** : elles vont au registre des refus avec leur motif, pas
   dans une question posée.

**Pourquoi cette règle n'est pas de la politesse.** C'est la contrepartie, du côté de l'agent, de la
[graine 9](../graines/graine_unknown_troisieme_etat.py:46) : *l'inconnu n'est pas une absence*. Une
question posée à la place d'un manque déclaré fait exactement ce que la graine interdit — elle range
l'inconnu avec le connu, et elle le fait porter par quelqu'un d'autre. Le troisième état existe :
il s'écrit.

## R2. Où sont les traces, et laquelle fait foi

| Objet | Emplacement | Fait foi ? |
|---|---|---|
| Refus motivés, chiffrés, datés | [`arbitrages_rmp.md`](arbitrages_rmp.md:155) §F | **oui** — c'est la trace |
| Mesures contradictoires, re-exécutables | [`../experiments/audit_graines_post_riemann.py`](../experiments/audit_graines_post_riemann.py:1) | **oui** — la commande reproduit le chiffre |
| Registre des chaînes de détection | [`../graines/README.md`](../graines/README.md:123) | **oui** — relevé par commande |
| Dossiers de synthèse rédigés hors dépôt | nom de dossier daté, sur le poste de travail, non versionné | **non** — confort de lecture, pas preuve |

**La distinction est celle du corpus : une trace, non un confort.** Un document de synthèse peut
disparaître sans perte : ce qu'il contenait de probant est dans les trois premières lignes du tableau.
Un document de synthèse qui serait *seul* à porter un chiffre est un défaut, pas un dossier.

## R3. La règle de fond, qui survit à la tentative

**Une graine n'est pas un texte : c'est une preuve de nécessité.** Elle exige :

1. un défaut **daté, reproduit et chiffré** — pas un thème, pas un cap épistémologique ;
2. la version **fautive livrée dans le fichier**, pour que l'assert de nécessité morde contre elle ;
3. un chiffre qui **ne contredit pas** une décision déjà prise dans le noyau ;
4. deux ou trois **systèmes réels nommés**, pas des catégories ;
5. une chaîne de détection **inscrite au registre** des chaînes.

Un défaut qui échoue l'un de ces cinq points n'est pas une graine ; il va au registre des refus. Ce
n'est pas une perte : c'est là que le corpus range ce qu'il a appris en le refusant.

## R3 bis. Tout compte déclaré se dérive, il ne se récite pas

**Trois fois le 2026-11-21, un instrument a péri par son décompte et non par sa logique.**

| Instrument | Ce qu'il déclarait | Ce qui était vrai |
|---|---|---|
| [`graines/README.md`](../graines/README.md:123) | « ces huit chaînes sont les seules valides » | le catalogue en portait **neuf** |
| `ETALON_8_2026-11-03.md` | « un par graine, […] couvre les sept défauts » | neuf graines depuis le 2026-11-11 |
| [`_verifier_etalon.py`](../../80_ARCHIVES/_VRAC_FLP/mttv-flp-diffusion/_verifier_etalon.py:1) | `ATTENDUS` figé à huit emplacements | neuf graines + une classe B = **dix** |

Dans les trois cas la **règle** était juste et le **nombre** faux. Aucune de ces trois erreurs n'a été
trouvée en relisant l'intention : elles ont été trouvées en exécutant (`grep`, `ast`, vérificateur).

**Corollaire.** Un compte écrit dans un document ou dans un programme porte la commande qui le
dérive, ou il reçoit ce compte **en paramètre**. Un nombre figé sans commande est une date de
péremption que personne n'a lue.
