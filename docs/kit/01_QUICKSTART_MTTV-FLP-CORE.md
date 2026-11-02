# Quickstart MTTV-FLP Core

*Collectif Les Fils de la Pensée (FLP) — coordination éditoriale : M. Gaillard*

**Pour qui.** Développeurs, ingénieurs données, architectes qui doivent faire tourner le noyau en
moins d'une heure et savoir, à la fin, s'ils ont le droit de s'en servir pour autre chose qu'une
démonstration.

**Ce que vous obtenez à la fin.** Une B-gate qui bascule, un contrat d'entrée qui distingue
l'absence du zéro, un quorum qui s'arrête tôt, et un handshake qui transporte la porosité
résiduelle de l'un vers l'autre — le tout sans dépendance hors bibliothèque standard.

**Référence.** version `1.2.1`, DOI de version `10.5281/zenodo.23869556`, concept
`10.5281/zenodo.20830060`.

---

## 1. Prérequis

| Élément | Exigence | Vérification |
|---|---|---|
| Python | 3.8 ou plus, **aucune dépendance externe** | `python -V` |
| Place disque | < 5 Mo pour le dépôt | — |
| Réseau | **aucun** pour les six graines et les modules `edge/` | — |
| Droits | aucun privilège particulier, aucun compte, aucune clé API | — |

Récupération :

```bash
git clone https://github.com/gaillard111/mttv-flp-core.git
cd mttv-flp-core
```

### Contrôle de santé en deux minutes, avant de coder

```bash
python tools/verifier_depot.py          # doit afficher : VERDICT : dépôt cohérent
python graines/graine_absence_zero.py   # doit se terminer sans exception
python graines/graine_une_horloge_deux_metiers.py
```

Si `verifier_depot.py` n'affiche pas « dépôt cohérent », **arrêtez** : votre copie ne correspond
pas à l'archive déposée, et tout ce que vous mesurerez ensuite ne sera pas citable.

---

## 2. Les six grandeurs, et rien d'autre

Tout le protocole tient dans six nombres et un booléen. Les confondre est la première cause
d'intégration ratée.

| Nom | Sens | Domaine | Où il vit |
|---|---|---|---|
| `p` | pression **mesurée** à ce pas | `[0,1]` | entrée du pas |
| `lecture` | une lecture a-t-elle eu lieu ? | `true` / `false` | entrée du pas — **jamais implicite** |
| `m` | mémoire de la pression | `[0,1]` | état |
| `h` | habitabilité : `1 − (0,85·m + 0,10·r + 0,05·c)` | `[0,1]` | dérivé |
| `r`, `c` | redondance et coût, dernières valeurs **connues** | `[0,1]` | état |
| `ρ` | porosité résiduelle du réseau mycélien | `[0,1]` | sortie du handshake |
| `Σ` | porosité structurelle de la B-gate | `[0,1]` | état de la B-gate |

Règle non négociable, mesurée dans [`edge/contrat_entree.py`](../../edge/contrat_entree.py:95) :
**`p = 0` signifie « calme mesuré », pas « aucune lecture »**. Une absence se déclare par
`lecture=false`. Sans ce bit, le système ne peut pas distinguer un capteur silencieux d'un monde
apaisé — et il rouvrira au douzième cycle nul, défaut dit de *fail-open*.

---

## 3. Initialisation du protocole

### 3.1 La B-gate — bascule locale

```python
from src.mttv_bgate_system import BGateTransduction

gate = BGateTransduction(alpha_psi=0.25, beta_bios=0.25, phi_tech=0.25)
rapport = gate.evaluer_porosite({"extraction": 0.40})

# rapport == {
#   "status": "B-GATE ACTIVÉE : Transition tétraédrique sp3 enclenchée. Flux prédateur neutralisé.",
#   "etats_sp3": {"Psi (Ψ)": 0.34, "Bios (B)": 0.47, "Phi (Φ)": 0.19},   # somme = 1,00
#   "porosite_Sigma": 0.0                                                # et c'est le défaut
# }
```

**Avertissement d'ingénierie, à lire une fois pour toutes.** `evaluer_porosite()` normalise
`Ψ + B + Φ` à 1, puis recalcule `Σ = 1 − (Ψ + B + Φ)` : `Σ` vaut donc **0 dès le premier appel**,
et `porosite_Sigma` est retourné à `0.0` indépendamment du flux. Conséquence pratique : toute
tension strictement positive déclenche la bascule ensuite. Deux conduites possibles, à choisir
explicitement dans votre code :

1. **traiter `Σ` comme un paramètre fixe** que vous possédez hors du noyau, et ne pas lire
   `porosite_Sigma` ;
2. **sérialiser un flux par instance** (`BGateTransduction()` neuf par décision) si vous voulez
   que le seuil nominal de 0,25 s'applique.

Ne construisez pas de régulation sur `porosite_Sigma`. Le défaut est documenté dans le module
([`Observations`](../../src/mttv_bgate_system.py:77)) et sa correction relève
d'une décision du collectif, pas d'un contournement local.

### 3.2 Le contrat d'entrée — la porte et sa mémoire

```python
import sys
sys.path.insert(0, "edge")
from contrat_entree import Porte

porte = Porte(mode="C")          # C = contrat d'entrée explicite (A et B2 sont des témoins)

# Un pas normal : la pression est mesurée
porte.pas(p=0.95, r=0.35, c=0.25, lecture=True)

# Un pas sans lecture : rien n'est deviné, la mémoire gèle
porte.pas(lecture=False)

# Lever un verrou d'escalade ne rouvre RIEN : cela exige une lecture postérieure
porte.clore(par="operateur:alice")
porte.pas(p=0.0, lecture=True)   # c'est cette lecture qui autorise la réouverture
```

États observables : `porte.m`, `porte.ferme`, `porte.porosite`, `porte.peremption`,
`porte.escalade`, `porte.attente_lecture`, `porte.clos_par`.

Chiffres de référence, à retrouver chez vous : fermeture au **pas 8**, réouverture au **pas 22**,
et sous absence prolongée **aucune** réouverture avec `m` gelée à **0,5877**.

### 3.3 Le quorum poreux et le handshake

```python
import sys
sys.path.insert(0, "src")
sys.path.insert(0, "mpvr-glocal/src")
from mttv_mpvr_quorum import MicroQuorumPoreux

quorum = MicroQuorumPoreux(total_noeuds=7, tolerance_panne=0.5)
diagnostic = quorum.evaluer_avec_handshake_mycelien(
    flux_signal={"input_flux": "basse_continue"},
    bgate_output=rapport,          # le rapport de la B-gate, section 3.1
)

# diagnostic["couplage_mycelien"] expose : protocole, resolution,
# porosite_residuelle, tolerance_effective, seuil_minimal_viable_effectif
```

**Second avertissement.** Dans `src/`, `MicroQuorumPoreux.evaluer_contexte()` tire
`noeud_fonctionnel` et `signal_coherent` avec `random` : c'est un **démonstrateur de politique
d'arrêt précoce**, pas un instrument de mesure. Pour mesurer, utilisez `graines/` et `edge/`.

Le couplage est monotone et documenté :

```
tolerance_effective   = clamp(tolerance_nominale + (ρ − 0.5) · sensibilite, 0, 1)
seuil_minimal_viable  = floor(total_noeuds · (1 − tolerance_effective))
```

`ρ > 0,5` ouvre et économise ; `ρ = 0,5` restitue le comportement nominal ; `ρ < 0,5` referme et
exige davantage de nœuds concordants.

---

## 4. Établissement du handshake — les quatre temps

| Temps | Émetteur | Charge utile | Attendu en retour |
|---|---|---|---|
| 1. **Annonce** | appelant | `proto`, `node_id`, capacités (`tetravalent`, `lecture_bool`) | `session_id`, version acceptée |
| 2. **État** | nœud | `etats_sp3` (Ψ, B, Φ), `porosite_Sigma`, `rho` | accusé, `etat_tetravalent` calculé |
| 3. **Transduction** | appelant | rapport B-gate + `flux_signal` | `diagnostic` (résolution, `ρ`, tolérance, seuil) |
| 4. **Validation** | appelant | décision + `lecture` | clôture, ou `attente_lecture=true` |

Le temps 4 est celui qu'on rate : **une clôture sans lecture postérieure n'est pas une
autorisation**, c'est un silence. Mesuré : fermeture pas 8, escalade pas 30, clôture seule →
aucune sortie, clôture **puis** lecture → réouverture pas **47**.

### Enveloppe d'échange, format proposé `mttv/handshake@1`

Ce format n'est pas dans l'archive Zenodo : c'est une **proposition de transport**, alignée champ
pour champ sur ce que le noyau produit réellement. Adoptez-la ou remplacez-la, mais versionnez-la.

```yaml
# mttv/handshake@1 — un pas de transduction triadique
proto: mttv/handshake@1
session_id: "0f8a-…"                 # opaque, fourni par le pair
node_id: "edge-zurich-01"
seq: 42                              # monotone, anti-rejeu

# --- 1. Ce que le nœud rapporte de son état interne (B-gate) ---
etat_sp3:
  psi: 0.26                          # Ψ : production / souffle
  bios: 0.36                         # B  : biomasse préservée
  phi: 0.13                          # Φ  : dérive technique
  sigma: 0.25                        # Σ  : porosité structurelle (voir avertissement §3.1)
                                     # invariant : psi + bios + phi + sigma = 1,00
bascule: active                      # active | stable

# --- 2. Le contrat d'entrée. `lecture=false` n'est PAS un zéro ---
entree:
  lecture: true                      # obligatoire, jamais implicite
  p: 0.00                            # pression mesurée, valide seulement si lecture=true
  r: 0.05                            # redondance connue
  c: 0.05                            # coût connu
  reveil: false                      # canal séparé, pour ne pas confondre calme et silence

# --- 3. L'état logique, en couples. Quatre valeurs, pas quatre quarts ---
etat_tetravalent: T                  # T=[1,1]  F=[0,0]  N=[0,1]  B=[1,0]
                                     # B (both) = discordance entre canaux : la porte ne rouvre pas

# --- 4. Ce que le réseau mycélien en retient ---
handshake:
  rho: 0.42                          # porosité résiduelle transmise au quorum
  tolerance_effective: 0.46          # clamp(0.5 + (0.42−0.5)·0.5, 0, 1)
  seuil_minimal_viable: 3            # floor(7 · (1 − 0.46))

# --- 5. Traçabilité : sans elle, rien n'est réfutable ---
trace:
  horodatage: "2026-11-01T22:49:38Z"
  version_noyau: "1.2.1"
  doi: "10.5281/zenodo.23869556"
  programme: "edge/contrat_entree.py"   # quel fichier imprime ce chiffre
```

### Traduction binaire → tétravalent

Un agent classique produit des sorties binaires (vrai/faux, oui/non, 0/1). La traduction est
**représentationnelle** : elle n'invente aucune dynamique, elle nomme l'état.

| Situation observable | Couple | Valeur |
|---|---|---|
| deux canaux concordent, le fait est affirmé | `[1,1]` | `T` |
| deux canaux concordent, le fait est nié | `[0,0]` | `F` |
| aucune information : pas de lecture, ou canal muet | `[0,1]` | `N` |
| les canaux se contredisent | `[1,0]` | `B` |

Trois règles d'implémentation, qui évitent 90 % des bugs :

1. **`None` n'est jamais `0`.** Une valeur manquante donne `N`, pas `F`.
2. **La discordance est un état, pas une pénalité.** Sous `B`, la mémoire gèle et rien ne rouvre ;
   on ne « moyenne » pas deux canaux qui se contredisent.
3. **Les seuils de discordance sont des choix**, à exposer en configuration : `0,15` sur le
   premier canal, `0,25` sur le second dans l'implémentation de référence
   ([`edge/discordance.py`](../../edge/discordance.py:52)). Aucun historique de
   mesures simultanées ne les justifie encore — écrivez-le dans votre documentation.

---

## 5. Recette — cinq assertions à passer avant de brancher quoi que ce soit

```python
# 1. Le noyau est intact
assert subprocess.run(["python", "tools/verifier_depot.py"]).returncode == 0

# 2. L'absence ne rouvre pas
porte = Porte("C"); [porte.pas(p=0.95, lecture=True) for _ in range(3)]
for _ in range(30): porte.pas(lecture=False)
assert not porte.ferme or porte.escalade is True

# 3. Le calme mesuré rouvre
porte = Porte("C"); [porte.pas(p=0.95, lecture=True) for _ in range(10)]
for _ in range(20): porte.pas(p=0.0, lecture=True)
assert porte.ferme is False

# 4. La clôture seule ne suffit pas
porte = Porte("C"); [porte.pas(lecture=False) for _ in range(25)]
if porte.escalade:
    porte.clore(par="test")
    assert porte.attente_lecture is True

# 5. Le handshake ne perd pas la porosité
diag = quorum.evaluer_avec_handshake_mycelien({"input_flux": "x"}, rapport)
assert 0.0 <= diag["couplage_mycelien"]["porosite_residuelle"] <= 1.0
```

## 6. Pièges connus, en vrac

- **Flux tronqué.** Un instrument peut rendre moins que ce qu'il annonce : 19 commentaires lus
  quand le post en annonce 20, profondeur figée à 5 quel que soit le paramètre. Si votre source
  pagine, suivez `next_cursor` jusqu'à `has_more=false`, sinon vous concluez sur un échantillon.
- **Confondre `ρ` et `Σ`.** `ρ` est la porosité **résiduelle du réseau**, mesurée après
  transduction ; `Σ` est la porosité **structurelle d'un nœud**. Elles ne se comparent pas.
- **Prendre la notice pour une preuve.** [`docs/notice_v1.2.0.md`](../../docs/notice_v1.2.0.md:1)
  liste ce qui est mesuré et ce qui est arbitré. Un chiffre sans fichier n'est pas un chiffre.

---

*Collectif Les Fils de la Pensée — CC-BY-NC-SA 4.0. Si vous publiez un résultat obtenu avec ce
noyau, citez la version : `10.5281/zenodo.23869556`.*
