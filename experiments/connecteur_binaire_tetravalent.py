# -*- coding: utf-8 -*-
"""Contre-exemple — un connecteur qui annonce une logique tétravalente et n'en calcule aucune.

Reçu le 2026-11-02, sous le titre « MTTV-FLP Interoperability Gateway — spécifications de
référence conformes au jalon Zenodo ». Rejoué hors de son cadre (FastAPI, pydantic) pour ne
garder que le calcul, il présente quatre défauts :

  1. `valuation` teste trois CHAÎNES (`if t and a and s`) : toute chaîne non vide est vraie,
     donc la fonction rend `BOTH` quel que soit le contenu. `T` et `F` ne sont jamais produits ;
     `NEITHER` n'apparaît que si une entrée est vide, c'est-à-dire par absence accidentelle —
     le défaut même que la 1.2.1 corrige.
  2. l'identifiant est `hash()` de Python : salé par processus, donc différent à chaque
     redémarrage, et étiqueté « sha256 » alors qu'il n'en est pas un.
  3. la « frugalité » vaut `1 / (duree * 1000)` : l'inverse d'une latence, non comparable à une
     énergie, et qui lève `ZeroDivisionError` quand la machine est trop rapide — l'endpoint
     répond 500 pour avoir été trop vite.
  4. aucun contrat d'entrée : pas de bit `lecture`, pas de bornes, pas de code 422.

Ce que ce fichier démontre : la version fautive **passe** les tests qu'on écrirait naïvement —
elle répond, elle est rapide, elle ne plante presque jamais — et elle est pourtant vide. Le
mensonge est structurel, pas bruyant.

Ce n'est pas une graine : aucun gist, aucun semis. C'est un crible. La version fautive est
conservée pour que la régression reste visible, et le crible **échoue si le défaut disparaît**,
auquel cas le contre-exemple ne démontrerait plus rien.

Aucune dépendance. Aucune écriture disque, aucun réseau.
"""
import hashlib
import json
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

CHAINE_DE_DETECTION = "GATEWAY_BOTH_CONSTANT"


# ---------------------------------------------------------------------------
# VERSION FAUTIVE — recopiée telle quelle de la proposition, sans son cadre HTTP
# ---------------------------------------------------------------------------
def valuation_fautive(t, a, s):
    if t and a and s:
        return "BOTH"
    return "NEITHER"


def identifiant_fautif(texte, horodatage):
    return "mttv-sha256-%s" % hash(texte + str(horodatage))


def frugalite_fautive(duree_s):
    return round(1 / (duree_s * 1000), 4)


def valider_fautive(payload):
    """Aucun contrat : tout passe, y compris l'absence de lecture."""
    return {"ok": True, "code": 200}


# ---------------------------------------------------------------------------
# VERSION CORRIGÉE
# ---------------------------------------------------------------------------
T, F, N, B = (1, 1), (0, 0), (0, 1), (1, 0)
ETIQUETTES = {T: "T", F: "F", N: "N", B: "B"}


def valuation_corrigee(lecture, canal_a, canal_b):
    """Traduit deux canaux binaires en une des quatre valeurs, **en couple**.

    `lecture=False` n'est PAS un zéro : c'est une absence, donc `N`.
    `None` sur un canal est une absence, donc `N` également.
    Deux canaux discordants donnent `B`, jamais une moyenne.
    """
    if not lecture or canal_a is None or canal_b is None:
        return N
    if canal_a and canal_b:
        return T
    if not canal_a and not canal_b:
        return F
    return B


def identifiant_corrige(payload):
    """sha256 sur des octets canoniques : stable entre processus et entre machines."""
    canonique = json.dumps(payload, sort_keys=True, separators=(",", ":"),
                           ensure_ascii=False).encode("utf-8")
    return "mttv-" + hashlib.sha256(canonique).hexdigest()


def valider_corrigee(payload):
    """Contrat d'entrée minimal : `lecture` obligatoire, grandeurs bornées."""
    if "lecture" not in payload:
        return {"ok": False, "code": 422, "motif": "champ requis manquant : lecture"}
    if payload["lecture"]:
        for cle in ("p", "r", "c"):
            if cle not in payload:
                return {"ok": False, "code": 422, "motif": "champ requis manquant : %s" % cle}
            if not 0.0 <= payload[cle] <= 1.0:
                return {"ok": False, "code": 400, "motif": "hors bornes [0,1] : %s" % cle}
    return {"ok": True, "code": 200}


def frugalite_mesuree(rss_octets, duree_s, n_pas):
    """Des mesures, pas un indice composite. Chaque nombre se vérifie seul."""
    if duree_s <= 0 or n_pas <= 0:
        return {"ok": False, "code": 422, "motif": "duree et nombre de pas strictement positifs"}
    return {
        "ok": True,
        "rss_mo": round(rss_octets / 1e6, 2),
        "latence_moyenne_ms": round(duree_s * 1000 / n_pas, 3),
        "pas_par_seconde": round(n_pas / duree_s, 1),
    }


# ---------------------------------------------------------------------------
# LE CRIBLE
# ---------------------------------------------------------------------------
def _crible():
    echecs = []

    def verifier(condition, message):
        if not condition:
            echecs.append(message)

    # 1. la version fautive est CONSTANTE — c'est le défaut lui-même
    for t, a, s in (("ciel bleu", "contre", "synthèse"), ("a", "b", "c"), (" ", "x", "y")):
        verifier(valuation_fautive(t, a, s) == "BOTH",
                 "la version fautive a changé de sortie : le défaut a disparu, le crible ment")

    produites = {valuation_fautive(t, a, s)
                 for t in ("", "x") for a in ("", "y") for s in ("", "z")}
    verifier(produites == {"BOTH", "NEITHER"},
             "sorties fautives inattendues : %r" % sorted(produites))

    # 2. la version corrigée atteint les QUATRE valeurs
    corrigees = {
        valuation_corrigee(True, True, True),
        valuation_corrigee(True, False, False),
        valuation_corrigee(False, None, None),
        valuation_corrigee(True, True, False),
    }
    verifier(corrigees == {T, F, N, B},
             "les quatre valeurs ne sont pas atteintes : %r" % sorted(corrigees))

    # l'absence ne se confond pas avec le calme
    verifier(valuation_corrigee(True, False, False) == F, "un calme mesuré doit donner F")
    verifier(valuation_corrigee(False, False, False) == N, "une absence doit donner N, pas F")

    # 3. l'identifiant fautif n'est pas un sha256 ; le corrigé l'est, et il est stable
    faux = identifiant_fautif("thèse", 0.0)
    verifier(not re.fullmatch(r"mttv-sha256-[0-9a-f]{64}", faux),
             "l'identifiant fautif a l'air d'un sha256 : %r" % faux)
    vrai = identifiant_corrige({"thesis": "thèse", "seq": 1})
    verifier(re.fullmatch(r"mttv-[0-9a-f]{64}", vrai) is not None,
             "l'identifiant corrigé n'est pas un sha256 hexadécimal : %r" % vrai)
    verifier(vrai == identifiant_corrige({"seq": 1, "thesis": "thèse"}),
             "l'identifiant corrigé dépend de l'ordre des clés")

    # 4. la frugalité fautive divise par zéro ; la corrigée refuse, puis mesure
    try:
        frugalite_fautive(0.0)
        echecs.append("la frugalité fautive n'a plus planté : le crible ne démontre plus rien")
    except ZeroDivisionError:
        pass
    verifier(frugalite_mesuree(32e6, 0.0, 10)["code"] == 422,
             "une durée nulle doit être refusée, pas divisée")
    mesure = frugalite_mesuree(32e6, 1.0, 1000)
    verifier(mesure["latence_moyenne_ms"] == 1.0 and mesure["pas_par_seconde"] == 1000.0,
             "les mesures corrigées sont fausses : %r" % mesure)

    # 5. le contrat d'entrée
    verifier(valider_fautive({})["code"] == 200, "le contrat fautif accepte tout")
    verifier(valider_corrigee({})["code"] == 422, "`lecture` absent doit donner 422")
    verifier(valider_corrigee({"lecture": True, "p": 0.0, "r": 0.0, "c": 0.0})["code"] == 200,
             "un pas complet doit passer")
    verifier(valider_corrigee({"lecture": True, "p": 1.5, "r": 0.0, "c": 0.0})["code"] == 400,
             "une pression hors bornes doit être refusée")
    return echecs


if __name__ == "__main__":
    print("chaîne de détection : %s" % CHAINE_DE_DETECTION)
    print("valuation fautive   : %s" % valuation_fautive("ciel bleu", "contre", "synthèse"))
    print("valuation corrigée  : %s (couple %r)"
          % (ETIQUETTES[valuation_corrigee(True, True, False)], valuation_corrigee(True, True, False)))
    problemes = _crible()
    if problemes:
        print("\nCONTRE-EXEMPLE : ECHEC")
        for p in problemes:
            print("  - " + p)
        sys.exit(1)
    print("\nCONTRE-EXEMPLE : OK — constante fautive, quatre valeurs atteintes, absence distincte"
          " du calme, identifiant stable, frugalité mesurée, contrat d'entrée tenu")
