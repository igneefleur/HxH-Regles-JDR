# -*- coding: utf-8 -*-
"""Extrait les compétences de competences.md et fabrique le script de workflow
qui génère l'échelle de difficulté (13 paliers) pour chacune."""
import json
import re
from pathlib import Path

SRC = Path("docs/content/regles/personnage/competences.md")
OUT = Path("scripts/wf_palier_generated.js")
SKIP = {"Course", "Crochetage"}  # déjà faites à la main (témoins)

lines = SRC.read_text(encoding="utf-8").splitlines()

skills = []
for i, line in enumerate(lines):
    if line.startswith("#### "):
        name = line[5:].strip()
        carac = groupes = desc = None
        for k in range(i + 1, min(i + 8, len(lines))):
            m = re.search(r"Caractéristique : (.+?)<br>Groupes : (.+?)</p>", lines[k])
            if m:
                carac, groupes = m.group(1), m.group(2)
                for j in range(k + 1, min(k + 6, len(lines))):
                    s = lines[j].strip()
                    if s and not s.startswith("<"):
                        desc = s
                        break
                break
        if carac and desc and name not in SKIP:
            skills.append({"name": name, "carac": carac, "groupes": groupes, "desc": desc})

TIERS = [
    ["Triviale", 0, "minimum humain moyen : ce que tout le monde fait sans apprentissage"],
    ["Très facile", 20, "action dont chacun a l'habitude"],
    ["Facile", 40, "demande déjà un peu de méthode"],
    ["Moyenne", 80, "un peu de connaissance ou d'expérience"],
    ["Difficile", 120, "problématique pour une personne ordinaire ; vrai talent ou chance"],
    ["Très difficile", 180, "limite supérieure de ce qu'une personne normale peut franchir"],
    ["Absurde", 240, "seuls les plus grands ou les surdoués réussissent avec régularité"],
    ["Quasi impossible", 320, "même les meilleurs au monde échouent le plus souvent"],
    ["Impossible", 400, "à la lisière du réel, miraculeux mais physiquement concevable"],
    ["Surhumaine", 520, "défie la logique, au-delà de ce que l'humain permet"],
    ["Prodigieuse", 640, "tenu pour irréalisable, exige une capacité surhumaine"],
    ["Insurmontable", 780, "frôle l'absolu, presque hors de portée même des plus exceptionnels"],
    ["Irréel", 920, "hors de la réalité, exige une capacité surnaturelle (Nen)"],
]

STYLE = ("Style impératif : français, 3e personne, JAMAIS « nous » ou « vous », "
         "JAMAIS le tiret cadratin « — ». Chaque exemple est court (une phrase nominale "
         "ou très brève), concret et varié.")

FEWSHOT = (
    "Exemples de calibrage (ne pas recopier) :\n"
    "- Course (compétence qui monte jusqu'au sommet grâce au Nen) : Triviale = « Trottiner "
    "tranquillement, marcher d'un bon pas. » ; Prodigieuse = « Courir cent mètres en deux "
    "secondes. » ; Irréel = « Rivaliser un instant avec un trait de lumière. » (les 13 paliers remplis).\n"
    "- Crochetage (compétence mécanique : un non-initié ne fait rien, et elle plafonne) : "
    "Triviale = VIDE ; Très facile = « Un cadenas bon marché ou un simple loquet. » ; Impossible = "
    "« La serrure mécanique la plus retorse jamais conçue. » ; Surhumaine, Prodigieuse, Insurmontable, "
    "Irréel = VIDES (une serrure reste mécanique)."
)

TEMPLATE = r'''export const meta = {
  name: 'echelles-competences',
  description: "Genere l'echelle de difficulte (13 paliers) pour chaque competence",
  phases: [{ title: 'Echelles', detail: 'un agent par competence' }],
}

const TIERS = __TIERS__;
const SKILLS = __SKILLS__;
const STYLE = __STYLE__;
const FEWSHOT = __FEWSHOT__;

const SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['name', 'examples'],
  properties: {
    name: { type: 'string' },
    examples: { type: 'array', minItems: 13, maxItems: 13, items: { type: 'string' } },
  },
};

phase('Echelles')
const results = (await parallel(SKILLS.map((s) => () =>
  agent(
    STYLE + "\n\n" + FEWSHOT + "\n\n" +
    "Competence : " + s.name + " (Caracteristique : " + s.carac + " ; Groupes : " + s.groupes + ").\n" +
    "Description : " + s.desc + "\n\n" +
    "Pour CHAQUE palier ci-dessous, donne UN exemple court et concret d'une chose realisable en « " + s.name + " » a ce niveau de difficulte. " +
    "Laisse la chaine VIDE (\"\") quand rien n'est realisable a ce palier : paliers bas vides si la competence est specialisee et qu'un non-initie ne peut rien faire ; paliers hauts vides si la competence est ordinaire et plafonne avant le surnaturel. Calibre chaque exemple sur le SENS du palier.\n\n" +
    "Paliers (dans l'ordre) :\n" +
    TIERS.map((t, i) => i + ". " + t[0] + " (" + t[1] + ") : " + t[2]).join("\n") +
    "\n\nRends {name, examples} : examples = 13 chaines dans l'ordre des paliers (chaine vide pour un palier hors de portee).",
    { label: s.name, phase: 'Echelles', schema: SCHEMA, effort: 'medium' }
  )
))).filter(Boolean);

return { skills: results };
'''

js = (TEMPLATE
      .replace("__TIERS__", json.dumps(TIERS, ensure_ascii=False))
      .replace("__SKILLS__", json.dumps(skills, ensure_ascii=False))
      .replace("__STYLE__", json.dumps(STYLE, ensure_ascii=False))
      .replace("__FEWSHOT__", json.dumps(FEWSHOT, ensure_ascii=False)))

OUT.write_text(js, encoding="utf-8")
print(f"OK - {len(skills)} competences -> {OUT}")
