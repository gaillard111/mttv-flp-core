# PoC Edge et connecteur d'interopérabilité — cahier des charges

*Collectif Les Fils de la Pensée (FLP) — coordination éditoriale : M. Gaillard*

**But.** Rendre le noyau MTTV-FLP utilisable par un agent ou un LLM qui ne sait produire que du
binaire, sur une machine à 15 € par mois, avec une question falsifiable à la clé — pas une
démonstration impressionnante.

**Question à laquelle le PoC répond.** *Un nœud de 32 Mo de RAM, sans GPU et sans base de données,
peut-il tenir 10 000 pas de transduction avec un contrat d'entrée strict, sans perdre la mémoire
gelée ni confondre l'absence avec le calme ?* Réponse attendue : oui, ou un chiffre qui dit non.

---

## 1. Périmètre

| Dans le périmètre | Hors périmètre |
|---|---|
| Un binaire/service unique, sans dépendance lourde | entraînement, inférence de modèle, GPU |
| Le noyau : B-gate, contrat d'entrée, quorum, handshake | une interface graphique |
| Un connecteur REST **et** gRPC pour agents existants | un annuaire central, une fédération de nœuds |
| Un journal append-only rejouable | une base de données relationnelle ou un broker |
| Mesures de frugalité reproductibles | des benchmarks comparatifs contre des hyperscalers |

## 2. Infrastructure cible

| Cible | Référence basse | Référence haute | Notes |
|---|---|---|---|
| Carte | Raspberry Pi Zero 2 W (512 Mo, quad-core 1 GHz) | Raspberry Pi 4 (2 Go) | ARM64, Debian 12 |
| VPS | 1 vCPU, 512 Mo, 10 Go | 1 vCPU, 1 Go | sans GPU, sans swap conseillé |
| Système | Linux, `systemd`, horloge NTP | idem | pas de conteneur obligatoire |
| Runtime | Python 3.11 (stdlib) **ou** Go ≥ 1.21 (binaire statique) | idem | le Go est recommandé pour les budgets mémoire |
| Persistance | un fichier journal `jsonl` + `fsync` groupé | SQLite optionnelle | aucune dépendance obligatoire à une base |
| Réseau | sortant facultatif ; entrant 1 port TCP | TLS terminaison locale | fonctionne hors ligne |

## 3. Architecture — trois composants, aucun broker

```
        ┌──────────────────────────── nœud (1 processus) ────────────────────────────┐
        │                                                                            │
appelant│  ┌──────────────┐   ┌────────────────────┐   ┌──────────────────────────┐   │
LLM ────┼─▶│ connecteur   │──▶│ noyau MTTV-FLP     │──▶│ journal append-only      │   │
agent   │  │ (REST/gRPC)  │◀──│ B-gate · contrat   │   │ seq, trace, empreinte    │   │
        │  │ adaptateur   │   │ quorum · handshake │   │ rejouable à l'identique  │   │
        │  └──────────────┘   └────────────────────┘   └──────────────────────────┘   │
        │        │                     ▲                                            │
        │        │  traduction         │  métriques locales (aucune télémétrie sortante)
        │        ▼                     │                                            │
        │   binaire → {T,F,N,B}   /metrics (Prometheus, opt-in)                     │
        └────────────────────────────────────────────────────────────────────────────┘
```

**Invariant d'architecture.** Aucune décision n'est déléguée à un centre : la B-gate décide
localement, le réseau mesure, le quorum valide. Le connecteur **traduit**, il ne décide pas.

## 4. API REST minimale (v1)

Cinq routes, c'est tout. Charge utile en `application/json`, `Content-Type` strict, taille max
8 Ko, profondeur JSON max 6.

| Méthode | Route | Rôle | Idempotence |
|---|---|---|---|
| `POST` | `/v1/sessions` | ouvre une session de handshake | non (retourne `session_id`) |
| `POST` | `/v1/sessions/{id}/steps` | un pas de transduction | **oui**, via `seq` |
| `GET` | `/v1/sessions/{id}` | état courant, sans effet de bord | oui |
| `POST` | `/v1/translate` | traduit un état binaire en `{T,F,N,B}` | oui |
| `GET` | `/healthz` · `/readyz` | vivacité / disponibilité | oui |

### 4.1 Ouvrir une session

```http
POST /v1/sessions
{ "proto": "mttv/handshake@1", "node_id": "edge-zurich-01",
  "capacites": ["tetravalent", "lecture_bool"] }
```

```json
{ "session_id": "0f8a2c…", "proto": "mttv/handshake@1", "version_noyau": "1.2.1",
  "seuils": { "fermeture": 0.45, "ouverture": 0.15, "discorde_p": 0.15, "discorde_r": 0.25 } }
```

### 4.2 Un pas

Requête — **`lecture` est obligatoire** : son absence est une erreur `422`, jamais un défaut
implicite à `true`.

```json
{ "seq": 42,
  "entree": { "lecture": true, "p": 0.0, "r": 0.05, "c": 0.05, "reveil": false },
  "etat_sp3": { "psi": 0.31, "bios": 0.44, "phi": 0.14, "sigma": 0.25 } }
```

Réponse :

```json
{ "seq": 42,
  "etat": { "m": 0.4120, "h": 0.6423, "ferme": true,
            "porosite": 0.20, "peremption": 0, "escalade": false, "attente_lecture": false },
  "etat_tetravalent": "B",
  "handshake": { "rho": 0.42, "tolerance_effective": 0.46, "seuil_minimal_viable": 3 },
  "trace": { "programme": "edge/contrat_entree.py", "version": "1.2.1" } }
```

### 4.3 Codes d'erreur — la partie qu'on bâcle toujours

| Code | Cas | Conduite de l'appelant |
|---|---|---|
| `400` | JSON invalide, `seq` non monotone | corriger, ne pas réémettre à l'aveugle |
| `422` | champ requis manquant (`lecture`, `p`, `r`, `c`) | **ne jamais combler par 0** |
| `409` | `seq` déjà vu avec un contenu différent | rejeu détecté : abandonner la session |
| `429` | plus de 50 pas/s | backoff exponentiel, pas de retry immédiat |
| `503` | journal non inscriptible | arrêter : un nœud qui ne trace plus ne mesure plus |

**Anti-patron à refuser explicitement** : une API qui accepte `p` absent et le traite comme `0`
reproduit le défaut de *fail-open* que la version 1.2.1 corrige. Si votre client ne peut pas dire
« je n'ai pas lu », il doit envoyer `lecture=false`, et l'API doit répondre `N`, jamais `F`.

### 4.4 Authentification et anti-rejeu

- HMAC-SHA256 par nœud, secret de 32 octets, en-têtes `X-Mttv-Node`, `X-Mttv-Seq`,
  `X-Mttv-Signature` (signature sur `seq || corps`).
- Fenêtre de fraîcheur 60 s ; `seq` strictement croissant par session ; cache des 512 derniers
  `seq` en mémoire (≈ 32 Ko).
- Rotation de secret à 90 jours ; aucun secret dans le journal.
- Aucune télémétrie sortante par défaut. `/metrics` est local et opt-in.

## 5. Variante gRPC (pour agents déjà instrumentés)

```proto
syntax = "proto3";
package mttv.v1;

service Handshake {
  rpc Ouvrir (Ouverture) returns (Session);
  rpc Pas    (PasRequete) returns (PasReponse);
  rpc Etat   (SessionRef) returns (PasReponse);
  rpc Traduire (EtatBinaire) returns (EtatTetravalent);
}

message PasRequete {
  string session_id = 1;
  uint64 seq = 2;
  bool   lecture = 3;         // obligatoire : proto3 ne distingue pas false de absent
  optional double p = 4;      // présence explicite, donc absence représentable
  optional double r = 5;
  optional double c = 6;
  bool   reveil = 7;
  EtatSp3 etat_sp3 = 8;
}

enum ValeurTetravalente { T = 0; F = 1; N = 2; B = 3; }
```

Deux règles de schéma : `optional` sur les grandeurs mesurées, et un `enum` nommé — pas un
entier nu. `proto3` sans `optional` rend `p=0` et `p` absent indiscernables, exactement le défaut
que le modèle corrige.

## 6. Adaptateur binaire → tétravalent

Le connecteur reçoit des sorties binaires et doit nommer l'état sans inventer de dynamique.

| Entrée | Règle | Sortie |
|---|---|---|
| deux canaux concordants, fait affirmé | `a=V, b=V` | `T` `[1,1]` |
| deux canaux concordants, fait nié | `a=F, b=F` | `F` `[0,0]` |
| aucune information (timeout, `None`, canal muet) | `a=?`, `b=?` | `N` `[0,1]` |
| désaccord | `a=V`, `b=F` | `B` `[1,0]` |

**Le mapping des grandeurs est un choix, et il doit être écrit comme tel.** Proposition de départ,
à documenter dans le README de votre intégration :

| Grandeur | Proxy proposé | Pourquoi c'est un choix |
|---|---|---|
| `p` (pression) | confiance normalisée de l'appelant sur `[0,1]` | une probabilité n'est pas une pression ; la mise à l'échelle est arbitraire |
| `r` (redondance) | `1 − |score_canalA − score_canalB|` | suppose deux canaux comparables, ce qui est souvent faux |
| `c` (coût) | coût mesuré du dernier appel (tokens, ms) normalisé | la normalisation dépend de votre infrastructure |

Ce que l'adaptateur **ne doit jamais** faire : moyenner deux canaux contradictoires pour fabriquer
un `0,5` tiède. Sous désaccord, l'état est `B`, la mémoire gèle, la porte ne rouvre pas — c'est
mesuré (40 pas comptés, `h` figé à 0,4529).

## 7. Budgets de frugalité — contraintes opposables

Ces seuils sont le cœur du dossier : ils rendent la promesse vérifiable, donc falsifiable.

| Ressource | Cible | Mesure acceptée |
|---|---|---|
| Mémoire résidente | **≤ 32 Mo** (Python) · ≤ 8 Mo (Go) | `ps -o rss=`, 10 000 pas, session ouverte |
| Taille de l'artefact | ≤ 2 Mo (binaire Go) · ≤ 100 Ko de code | `du -sh` |
| Démarrage à froid | **≤ 200 ms** | `hyperfine --warmup 3` |
| Latence d'un pas | p50 ≤ 1 ms · **p99 ≤ 5 ms** | 100 000 pas, journal désactivé puis activé |
| État par session | **≤ 256 octets** sérialisés | dump JSON de l'état |
| Bande passante | **≤ 512 octets** par pas, aller-retour | compteur socket |
| Journal | ≤ 1 Mo / jour / nœud à 1 pas/s | rotation à 32 Mo, 3 fichiers |
| CPU au repos | < 1 % d'un vCPU | `pidstat` 60 s |
| Énergie | < 1 W au repos sur Pi Zero 2 W | mesure USB ou `vcgencmd measure_volts` + ampèremètre |
| Dépendances | **0** hors bibliothèque standard | `pip freeze` vide, `go list -deps` limité à la stdlib |
| Télémétrie | 0 requête sortante par défaut | `tcpdump` 1 h, aucun paquet inattendu |

**Méthode imposée.** Tout chiffre publié doit venir d'une commande reproductible écrite dans le
`README` du PoC, avec la machine, l'OS et le commit. Un budget sans commande est un vœu.

## 8. Validation du PoC — trois épreuves et des seuils de réussite

1. **Charge** : 10 clients, 50 pas/s, 10 minutes. Réussite si p99 ≤ 5 ms, RSS ≤ 32 Mo, zéro `5xx`.
2. **Endurance** : 1 pas/s pendant 24 h. Réussite si le journal est rejouable à l'identique
   (même empreinte de l'état final), mémoire stable à ±10 %, aucune dérive d'horloge > 1 s.
3. **Déterminisme** : rejouer le journal sur une seconde machine doit produire **les mêmes
   chiffres**, y compris `m` gelée et numéro de pas de réouverture. Toute divergence est un bug,
   pas une tolérance.

Épreuve de refus, aussi importante : envoyer 100 pas avec `lecture` absent. Attendu : `422` à
chaque fois. Un seul `200` invalide le PoC.

## 9. Livrables et calendrier (3 semaines, une personne)

| Semaine | Livrable | Critère d'acceptation |
|---|---|---|
| 1 | service + journal + `/healthz`, budgets mesurés à vide | épreuve 3 passe sur 1 000 pas |
| 2 | REST complet, adaptateur, HMAC, `422` partout où il faut | épreuves 1 et 3 passent |
| 3 | gRPC, `/metrics`, endurance 24 h, README reproductible | épreuve 2 passe, budgets tenus |

## 10. Ce que ce PoC ne fera pas

- Il ne prouvera pas la robustesse du modèle : il prouvera qu'un nœud frugal tient ses contrats.
- Il ne recommandera pas de mapping `p/r/c` comme canonique : ce sera un choix documenté, daté,
  remplaçable.
- Il n'utilisera pas `BGateTransduction` en régulation continue sans trancher le défaut `Σ → 0`
  ([`Observations`](../../src/mttv_bgate_system.py:77)).

---

*Collectif Les Fils de la Pensée — document : CC-BY-SA 4.0 · noyau cité : CC-BY-NC-SA 4.0.
Référence noyau : `10.5281/zenodo.23869556`.*
