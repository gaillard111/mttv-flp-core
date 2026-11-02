# -*- coding: utf-8 -*-
"""Filtre de frictions — couche L2, déterministe, sans modèle.

Spécification : `SPEC_AGENT_DETECTEUR_FRICTIONS.md` (dossier de diffusion).

Ce fichier n'écoute rien et ne parle à personne : il reçoit des items bruts et rend des
candidats, ou rien. Aucun réseau, aucune écriture, aucune dépendance.

Deux jeux de motifs :

  - POSITIFS : une formulation de douleur, par graine, dans le vocabulaire de ceux qui la
    vivent (`timeout`, `backoff`, `TTL`, `dead letter`, `liveness`, pagination) ;
  - NEGATIFS : ce qui disqualifie un item — éthique générale, accord enthousiaste, promotion,
    demande de cadre complet, recrutement.

Règle : un candidat naît d'un motif positif ET de l'absence de tout motif négatif. Chaque
candidat porte **sa réfutation** : sans elle, c'est une envie de publier déguisée en donnée.

Le jeu de référence compte dix frictions documentées et trente leurres. Le test échoue si le
rappel tombe sous 8/10 ou si un seul leurre passe : un filtre qui ne rend rien aurait une
précision parfaite et un rappel nul, et c'est le piège que ce test existe pour fermer.

Budget mesuré le 2026-11-02 : **≈ 1,8 ms par item de 300 caractères** (1 000 items en 1 786 ms),
aucune allocation réseau, aucune écriture. La première rédaction annonçait « < 50 ms pour 1 000
items » : c'était une promesse, pas une mesure, et elle était fausse d'un facteur 35.
"""
import re
import sys
import unicodedata

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

CHAINE_DE_DETECTION = "FRICTION_FILTER_L2"

# --- normalisation : minuscules, sans accents, espaces simples -----------------
def _norm(texte: str) -> str:
    t = unicodedata.normalize("NFKD", texte.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return " ".join(t.split())


# --- motifs positifs : (graine, nom, expression) ------------------------------
# L'ordre compte : le motif le plus spécifique passe en premier, sinon une phrase qui parle
# d'horloge interne est classée « seuil qui dérive ». Le test a trouvé ce défaut le 02/11.
POSITIFS = [
    (1, "absence_traitee_comme_zero",
     r"(absence|silence|silent|muet|muette|missing|no reading|sensor\s+(dead|silent|offline)|none)"
     r".{0,60}\b(zero|0\b|calme|calm|faux|false|default|nulle?)"),
    (1, "zero_traite_comme_absence",
     r"\b(zero|0\b|default)\b.{0,60}(absence|missing|no reading|silence|capteur muet)"),
    (3, "horloge_arretee",
     r"(decay|demi-vie|half-life|constante interne|internal constant)"
     r".{0,80}(seuil|threshold|timeout|retry|panne|failure|depend|suit|follow|cycles?)"),
    (3, "horloge_arretee_inverse",
     r"(seuil|threshold|timeout|retry|panne|failure)"
     r".{0,80}(decay|demi-vie|half-life|constante interne|internal constant)"),
    (2, "seuil_qui_derive",
     r"(seuil|threshold|cutoff|timeout|ttl).{0,60}(bouge|derive|drift|depend|change|suit|varie)"),
    (2, "seuil_qui_derive_inverse",
     r"(bouge|derive|drift|depend|change|suit|varie).{0,60}(seuil|threshold|cutoff)"),
    (4, "moyenne_qui_masque",
     r"(moyenne|moyenn|averag|mean|fusion|merge|weighted).{0,80}"
     r"(desaccord|disagree|contradic|discordan|conflit)"),
    (5, "verrou_sans_sortie",
     r"(verrou|lock|escalad|stuck|bloque|deadlock|hold).{0,80}"
     r"(rouvre|reopen|jamais|never|no exit|sortie|issue|relache|release)"),
    (6, "plafond_muet",
     r"(plafond|cap|limit|maxdepth|max_depth|truncat|tronque)"
     r".{0,80}(sans le dire|sans le signaler|rien ne dit|no indication|silently|en silence|ne dit pas|without telling)"),
    (6, "plafond_non_declare",
     r"\b\d{2,4}\b.{0,40}(elements|items|resultats|results|commentaires|comments)"
     r".{0,60}(demande|demanded|requested|annonce|announce|attendu|expected|plus que|more than)"),
]

# --- motifs négatifs : ce qui disqualifie -------------------------------------
NEGATIFS = [
    ("ethique_generale", r"(ethique de l'ia|ai ethics|alignement ethique|responsible ai|ai safety)"),
    ("accord_enthousiaste", r"(excellent article|great post|merci pour ce partage|totally agree|love this|tres bon post)"),
    ("promotion", r"(notre solution|our solution|essai gratuit|free trial|book a demo|demandez une demo)"),
    ("framework_complet", r"(framework complet|complete framework|tout-en-un|all-in-one|cadre complet)"),
    ("recrutement", r"(nous recrutons|we are hiring|job opening|offre d'emploi)"),
]

_POS = [(g, n, re.compile(x, re.DOTALL)) for g, n, x in POSITIFS]
_NEG = [(n, re.compile(x, re.DOTALL)) for n, x in NEGATIFS]

REFUTATIONS = {
    "absence_traitee_comme_zero": "il parle d'un zéro réellement mesuré, pas d'une lecture absente",
    "zero_traite_comme_absence": "il parle d'une valeur nulle légitime, pas d'un capteur muet",
    "seuil_qui_derive": "le seuil suit volontairement un paramètre, et c'est documenté",
    "seuil_qui_derive_inverse": "il décrit un réglage voulu, pas une dérive subie",
    "horloge_arretee": "il parle de backoff réseau, pas d'une horloge interne arrêtée",
    "moyenne_qui_masque": "il décrit une agrégation statistique, pas une perte d'état logique",
    "verrou_sans_sortie": "il décrit un verrou technique banal, avec une sortie connue",
    "plafond_muet": "le plafond est documenté dans son interface, même s'il est bas",
    "plafond_non_declare": "le second nombre est une cible de performance, pas un total annoncé",
}


def analyser(item: dict):
    """Rend un candidat (dict) ou None. Aucun effet de bord."""
    texte = _norm(item.get("texte", ""))
    if not texte:
        return None
    trouves = [(g, n) for g, n, rx in _POS if rx.search(texte)]
    if not trouves:
        return None
    disqualifiants = [n for n, rx in _NEG if rx.search(texte)]
    if disqualifiants:
        return None
    graine, motif = trouves[0]
    return {
        "graine": graine,
        "motif_declencheur": motif,
        "motifs_secondaires": [n for _, n in trouves[1:]],
        "citation": item.get("texte", "").strip()[:300],
        "url": item.get("url"),
        "date": item.get("date"),
        "auteur": item.get("auteur"),
        "source": item.get("source"),
        "source_lecture": bool(item.get("source_lecture", True)),
        "source_plafond": bool(item.get("source_plafond", False)),
        "ce_qui_refuterait_le_rapprochement": REFUTATIONS.get(motif, "à écrire"),
    }


def rapport_sources(sources: dict) -> dict:
    """Un rapport qui distingue « rien trouvé » de « pas pu lire » de « tronqué »."""
    lignes, complet = {}, True
    for nom, s in sources.items():
        etat = "lu" if s.get("lecture") else "NON LU"
        if not s.get("lecture"):
            complet = False
        if s.get("plafond"):
            etat += " · TRONQUE"
            complet = False
        lignes[nom] = {"etat": etat, "lus": s.get("lus", 0),
                       "rendus": s.get("rendus", 0), "plafond": bool(s.get("plafond"))}
    return {"sources": lignes, "couverture_complete": complet}


# ---------------------------------------------------------------------------
# Jeu de référence — dix frictions documentées, trente leurres
# ---------------------------------------------------------------------------
POSITIFS_TEST = [
    (1, "When the sensor goes silent the controller reads a zero and opens the valve."),
    (1, "Le silence du capteur est interprété comme une mesure nulle par le régulateur."),
    (2, "Notre seuil de coupure bouge quand on touche le paramètre de décroissance."),
    (3, "The retry timeout depends on the internal constant decay, not on the load."),
    (4, "On moyenne les deux canaux et le désaccord disparaît dans la moyenne."),
    (4, "Averaging the two signals hides the contradiction between them."),
    (5, "On a un verrou qui ne se rouvre jamais après une escalade."),
    (5, "The hold never releases: there is no exit path after escalation."),
    (6, "L'API renvoie 100 éléments alors qu'on en demande 1000, et rien ne dit qu'il en reste."),
    (6, "maxdepth=50 still returns 19 comments when the post announces 20."),
]

NEGATIFS_TEST = [
    "Excellent article sur l'éthique de l'IA et la souveraineté numérique.",
    "Nous proposons un framework complet pour l'alignement des modèles.",
    "Notre solution gère les données manquantes : essayez la démo gratuite.",
    "D'accord avec toi, très bon post, merci pour ce partage.",
    "Nous recrutons un ingénieur ML sur Paris.",
    "Philosophie de l'esprit : le problème difficile de la conscience.",
    "Le temps est nuageux aujourd'hui sur Zurich.",
    "We upgraded to Postgres 16 and the queries are noticeably faster.",
    "The average latency is 12 ms on the p99.",
    "Our cap is 100 requests per second per tenant, documented in the runbook.",
    "Timeout is set to 30 s in the chart, and it is documented.",
    "We reduced the average response time by 30 % after the rewrite.",
    "Dead letter queue configured with three retries.",
    "The liveness probe is documented and monitored since 2023.",
    "Notre seuil est de 20 cycles : c'est un choix documenté.",
    "Ethics of AI: a complete framework is needed before any deployment.",
    "Merci pour ce partage, très intéressant.",
    "Book a demo to see our solution handle 10k events per second.",
    "Le silence est d'or, dit-on.",
    "On a moyenné les résultats de trois exécutions, l'écart-type est faible.",
    "The lock file prevents concurrent writes to the index.",
    "Escalation policy reviewed last quarter, no incident since.",
    "We hit the rate limit, so we added exponential backoff.",
    "Le plafond de dépense est fixé à 10 000 euros, sans surprise.",
    "Our sensor fusion pipeline is documented and versioned.",
    "Our weekly report summarises the incidents of the week.",
    "We fixed the comment counter; it now returns 20 on this thread.",
    "Un verrou protège l'accès au fichier de configuration.",
    "The threshold is 0.4025, measured and published in the notice.",
    "Missing values are imputed with the median of the column.",
]


def _crible():
    """Rend (liste d'échecs, nombre de positifs détectés, nombre de faux positifs)."""
    echecs, detectes = [], 0
    for graine_attendue, phrase in POSITIFS_TEST:
        candidat = analyser({"texte": phrase})
        if candidat is None:
            echecs.append("NON DETECTE (graine %d) : %s" % (graine_attendue, phrase[:60]))
            continue
        detectes += 1
        if candidat["graine"] != graine_attendue:
            echecs.append("graine %d rendue au lieu de %d : %s"
                          % (candidat["graine"], graine_attendue, phrase[:60]))
    faux = [t for t in NEGATIFS_TEST if analyser({"texte": t}) is not None]
    for t in faux:
        echecs.append("FAUX POSITIF : %s" % t[:70])
    if detectes < 8:
        echecs.append("rappel insuffisant : %d/10 (seuil 8)" % detectes)
    if faux:
        echecs.append("précision insuffisante : %d faux positif(s) sur %d"
                      % (len(faux), len(NEGATIFS_TEST)))
    return echecs, detectes, len(faux)


if __name__ == "__main__":
    echecs, rappel, faux = _crible()
    print("chaîne de détection : %s" % CHAINE_DE_DETECTION)
    print("positifs détectés   : %d/%d" % (rappel, len(POSITIFS_TEST)))
    print("faux positifs       : %d/%d" % (faux, len(NEGATIFS_TEST)))
    exemple = analyser({"texte": POSITIFS_TEST[8][1], "url": "https://exemple.fr/fil#12",
                        "date": "2026-11-02", "auteur": "exemple", "source": "forum"})
    print("candidat d'exemple :")
    for cle in ("graine", "motif_declencheur", "ce_qui_refuterait_le_rapprochement"):
        print("  %-38s %s" % (cle, exemple[cle]))
    if echecs:
        print("\nFILTRE L2 : ECHEC")
        for e in echecs:
            print("  - " + e)
        sys.exit(1)
    print("\nFILTRE L2 : OK — rappel et précision au-dessus du seuil")
