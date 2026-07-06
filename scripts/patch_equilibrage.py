# -*- coding: utf-8 -*-
"""Rééquilibrage par difficulté de visée : plus une zone est facile à toucher, moins elle punit.
- Mollet (zone la PLUS facile à toucher) : retire la Paralysie (un mollet est un muscle, pas un
  nerf -> gêne d'appui et chute, pas paralysie) et ramène les malus −20/−40/−60/−80 à −10/−20/−25/−35.
  À terre dès le degré 3, test d'Inconscience au degré 4 ; le degré 5 (amputation) reste inchangé.
- Genou D3 : −80 -> −40.   - Aine D3 : −60 -> −45.   (le malus d'action plafonne à −50 = l'Œil)
Usage : python scripts/patch_equilibrage.py"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
P = Path("scripts/blessures_audit.json")
ds = json.loads(P.read_text(encoding="utf-8"))

FIX = {
    ("Mollet", 1): {
        "effet": "Le muscle du mollet se déchire d'un coup et la jambe se dérobe sous le poids du corps, chaque pas devient incertain. Le blessé subit un Saignement de −5 PV et −10 aux actions physiques exigeant un appui sur cette jambe.",
        "tr": "Le médecin immobilise le mollet et le met au repos, le temps que les fibres musculaires se ressoudent. Lève le malus de −10.",
    },
    ("Mollet", 2): {
        "effet": "La lame ouvre le mollet et tranche le faisceau musculaire en profondeur, le sang coule à flots de la plaie béante. Le blessé subit un Saignement de −10 PV et −20 aux actions d'appui sur cette jambe.",
        "tr": "Le médecin suture les faisceaux musculaires tranchés, puis impose une immobilisation. Retire le saignement et lève le malus de −20.",
    },
    ("Mollet", 3): {
        "effet": "Le tendon d'Achille cède en partie sous la lame et le pied ne répond plus, la jambe lâche et le corps s'effondre. Le blessé subit un Saignement de −10 PV, l'état À terre et −25 aux actions d'appui sur cette jambe : la course et le saut lui sont impossibles.",
        "tr": "Le médecin suture le tendon d'Achille et répare les chairs, puis une rééducation rend sa souplesse au pied. Retire le saignement, retire l'état À terre et lève le malus de −25.",
    },
    ("Mollet", 4): {
        "effet": "Le tibia se brise net et le mollet est broyé jusqu'à l'os, la jambe ne porte plus rien et s'écroule sous une douleur fulgurante. Le blessé subit un Saignement de −15 PV, l'état À terre, sa jambe est hors d'usage et n'autorise plus aucun appui, et il subit −35 à toute action physique au sol. Au début de son prochain tour, le blessé doit réussir un test d'Impassibilité Difficulté Très difficile ou tomber Inconscient.",
        "tr": "Le médecin réduit et fixe le tibia, reconstruit les muscles broyés du mollet, puis une rééducation redresse la jambe. Retire le saignement, lève le malus de −35, retire l'état À terre, retire l'état Inconscient et rend l'usage de la jambe.",
    },
    ("Genou", 3): {
        "effet": "La rotule éclate et les ligaments croisés cèdent, l'articulation ne tient plus du tout et aucun appui n'est possible. Le blessé subit un Saignement de −10 PV, la jambe est hors d'usage, le blessé subit −40 à toute action physique impliquant cette jambe et subit l'état À terre.",
    },
    ("Aine", 3): {
        "effet": "L'os iliaque se fend et la tête du fémur sort de son logement : le bassin ne répond plus et la jambe se dérobe sous le poids du corps. Le blessé subit un Saignement de −10 PV, l'état À terre, l'état Immobilisé, l'état Paralysie partielle de la jambe et −45 à toute action prenant appui sur la jambe.",
        "tr": "Le médecin réduit la luxation de la hanche et fixe l'os iliaque fêlé. Retire le saignement. Retire l'état À terre. Retire l'état Immobilisé. Retire l'état Paralysie partielle. Lève le malus de −45.",
    },
}

for (zone, degre), fix in FIX.items():
    e = next(x for x in ds[zone] if x["degre"] == degre)
    if "effet" in fix:
        e["effet"] = fix["effet"]
    if "tr" in fix:
        e["traitement"]["description"] = fix["tr"]

P.write_text(json.dumps(ds, ensure_ascii=False, indent=1), encoding="utf-8")
print("OK -", len(FIX), "entrées rééquilibrées (Mollet D1-D4, Genou D3, Aine D3)")
