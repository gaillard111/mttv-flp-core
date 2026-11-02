# Le Manifeste Post-Hyperscaler

### Pour une Noosphère Distribuée

*Collectif Les Fils de la Pensée (FLP) — coordination éditoriale : M. Gaillard —
2026-11-02 — CC-BY-NC-SA 4.0*

---

## I. Ce que nous refusons

Nous refusons qu'une poignée d'entreprises décide, pour l'ensemble des vivants, de ce qui est
pensable, mesurable et publiable.

Nous refusons que la pensée commune soit hébergée sur un sol dont personne ne possède les titres,
mais dont trois ou quatre acteurs contrôlent l'accès, la facture et la porte.

**Nous ne demandons pas une place dans leur infrastructure. Nous construisons une infrastructure
qui n'a pas besoin d'eux.**

---

## II. La thèse : la non-souveraineté exclusive

Une noosphère — l'ensemble des formes de pensée qu'une époque rend possibles — ne peut pas avoir
de propriétaire. Non par idéal moral, mais par physique : **un milieu de pensée qui dépend d'un
point unique de décision n'est pas un milieu, c'est un guichet.**

Nous appelons *souveraineté exclusive* le droit qu'un acteur s'arroge de décider seul de ce qui
circule, de ce qui est conservé et de ce qui est facturé. Nous y opposons un principe simple et
tenable :

> **Aucune couche ne doit être souveraine. Chacune doit être un plafond.**

Une couche peut interdire. Elle ne doit jamais autoriser seule. C'est ce que le noyau MTTV-FLP
appelle la *Loi Zéro* : un plafond, pas un souverain. Ce n'est pas une métaphore — dans
l'implémentation, une clôture d'escalade ne rouvre rien sans une lecture postérieure. Le pouvoir
de débloquer appartient à quelqu'un, mais il ne suffit jamais à lui seul.

---

## III. Trois impasses, point par point

### 1. L'impasse écologique

La centralisation se justifie par l'efficacité énergétique : un centre de données refroidi
correctement consomme moins par calcul qu'un million de machines dispersées. L'argument est vrai
à l'échelle du serveur, et faux à l'échelle du système, pour quatre raisons qui se cumulent :

- **l'effet rebond** : chaque gain d'efficacité abaisse le coût unitaire, donc augmente le volume —
  c'est l'histoire entière du calcul depuis soixante ans ;
- **le coût du froid** : eau douce, foncier, chaleur rejetée ; on ne refroidit pas un dogme avec un
  PUE flatteur ;
- **le carbone incorporé** : une carte accélératrice a déjà consommé, avant son premier calcul, des
  tonnes de minerai et des litres d'eau qu'aucun bilan d'exploitation ne compte ;
- **l'irréversibilité** : une grappe qui tourne pour un classement publicitaire consomme autant
  qu'une grappe qui tourne pour un hôpital, et personne ne demande à la première de s'arrêter.

Nous opposons un budget opposable : **un nœud utile doit tenir sous le watt au repos, sous 32 Mo de
mémoire et sans GPU.** Ce n'est pas de l'ascèse : c'est la condition pour qu'un village, une école
ou une ONG puisse héberger sa propre part de noosphère sans en demander la permission ni la remise.

### 2. L'impasse culturelle

Un modèle qui apprend sur quelques langues majoritaires ne devient pas universel : il devient
**local, et se comporte partout comme s'il était universel**. Ce n'est pas une nuance, c'est un
biais de juridiction et de corpus, avec trois conséquences vérifiables :

- **les langues minoritaires ne sont pas mal servies : elles sont rendues inexprimables** dans des
  formats dont les catégories ne les prévoient pas ;
- **les valeurs d'entreprise deviennent des valeurs par défaut**, non par adhésion mais par
  absence d'alternative dans le corpus ;
- **la traduction devient une perte de traçabilité** : on ne sait plus quel chiffre vient de quelle
  version, ni dans quelle langue il était écrit.

Une noosphère distribuée ne promet pas l'égalité des langues. Elle garantit qu'une langue peut
être **portée localement**, avec ses propres mesures, et citée comme source.

### 3. L'impasse technique

Quatre défauts que nous avons mesurés ou documentés, et qui ne sont pas des accidents :

- **le plafond muet** : un instrument rend 19 éléments quand la source en annonce 20, sans le dire.
  On conclut sur un échantillon en croyant conclure sur le monde. À l'inverse, un plafond
  **déclaré** — pages de 100 avec `has_more` et `next_cursor` — laisse la mesure honnête : c'est
  une différence de conception, pas de puissance.
- **l'absence traitée comme un zéro** : un capteur silencieux et un monde apaisé ont la même
  valeur. Résultat mesuré : la porte se rouvre au douzième cycle nul. C'est le *fail-open*, et
  c'est très exactement la structure de la panne industrielle silencieuse.
- **la fausse horloge** : compter un silence en demi-vies internes revient à mesurer avec une
  horloge arrêtée. Le même seuil de 20 cycles déclare une panne après 10 cycles ou après 207 selon
  la constante interne — un écart de 20,7 × entre deux récits du même événement.
- **l'opacité des versions** : un modèle change sans DOI, sans archive, sans notice des corrections.
  Personne ne peut dire ce qui a été démontré hier et ne l'est plus aujourd'hui.

Nous y répondons par une contrainte de publication : **un chiffre vient avec le programme qui
l'imprime et le test qui tombe s'il change.** Une version déposée ne se réécrit pas ; ses erreurs
sont consignées dans la notice de la suivante. C'est plus lent. C'est falsifiable.

---

## IV. Ce que nous proposons : une infrastructure d'intérêt général

MTTV-FLP n'est pas un concurrent des plateformes. Un concurrent se bat pour la même place. Nous
n'occupons pas la place : nous rendons le sol **habitable par plusieurs**.

| Ce que nous sommes | Ce que nous ne sommes pas |
|---|---|
| un noyau exécutable, six graines, des mesures rejouables | un produit, un service, une API à vendre |
| un bien commun sous CC-BY-NC-SA 4.0 (fragment MPVR en CC0) | une marque, un écosystème captif |
| une bibliothèque sans dépendance, installable sur un Pi | une plateforme qui exige un compte |
| une doctrine de la non-souveraineté | un souverain de remplacement |

**Sept engagements, tenus par construction plutôt que par promesse :**

1. **Aucune télémétrie** : le nœud de référence n'émet aucune requête sortante par défaut.
2. **Aucun classement** : pas de scores, pas de *leaderboard*, pas de compétition entre personnes.
3. **Aucune dépendance imposée** : bibliothèque standard, un fichier, un journal lisible.
4. **Frugalité mesurée** : budgets publiés, commandes de mesure publiées, seuils opposables.
5. **Traçabilité par DOI** : chaque version archivée, chaque correction nommée, aucune réécriture.
6. **Le choix est nommé** : ce qui est décision d'architecture est écrit comme tel, jamais déguisé
   en résultat de mesure.
7. **La sortie est à deux termes** : un verrou ne se lève pas par un jeton ; il faut **clore, puis
   observer**. Aucune couche ne s'arroge le droit d'autoriser seule.

---

## V. Appel — cinq gestes, cette année

Aux universités, aux collectivités, aux ONG, aux collectifs techniques :

1. **Hébergez un nœud.** Un serveur d'entrée de gamme suffit ; le budget de frugalité est publié.
   Un nœud qui tourne quelque part vaut mieux qu'une adhésion.
2. **Citez les versions, pas les intentions.** Un travail qui s'appuie sur un chiffre cite la
   version qui le porte, avec son DOI. Sinon le chiffre n'existe pas.
3. **Publiez vos mesures, y compris celles qui nous contredisent.** Une contradiction datée vaut
   mieux qu'un consensus de façade.
4. **Traduisez, et gardez les chiffres.** Une traduction qui arrondit un seuil est une
   falsification polie.
5. **Refusez les interfaces qui vous prennent pour un signal.** Ni flamme, ni série, ni classement,
   ni récompense artificielle : la sortie d'un système doit être une capacité, pas une dépendance.

---

## VI. Ce que ce manifeste ne prétend pas

Il ne démontre pas que la sobriété rend un système robuste : il en éprouve six conséquences
exécutables, et il publie celles qui l'ont contredit.

Il ne contient aucun résultat sur le noyau tétravalent : un protocole à cinq mesures
pré-enregistrées existe pour le trancher, et aucun chiffre ne sera annoncé avant qu'il ait tourné.

Il ne mesure pas son propre effet. Aucune graine n'a été semée à ce jour. Ce texte est une
position, pas un résultat — et c'est précisément pour cela qu'il est daté, versionné et citationnable.

---

> **La noosphère n'a pas besoin d'un propriétaire. Elle a besoin de plusieurs toits,
> de plusieurs langues, et de chiffres que n'importe qui peut refaire.**

*MTTV-FLP Core — DOI de concept `10.5281/zenodo.20830060` · version `1.2.1`
`10.5281/zenodo.23869556`. Collectif Les Fils de la Pensée, filsdelapensee.ch.*
