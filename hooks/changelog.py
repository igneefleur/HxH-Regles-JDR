"""Hook MkDocs : lit `git log` au build et expose changelog.json (derniers
commits + fichiers de contenu modifiés) pour alimenter la page d'accueil.

On ne retient que les fichiers .md sous content/, et on calcule l'URL de la
page correspondante pour pouvoir cliquer dessus. Les commits ne touchant aucun
fichier de contenu sont ignorés.

Le fichier est ajouté au site via l'API Files (en mémoire) — on n'écrit PAS
dans docs/, sinon `mkdocs serve` reconstruirait en boucle. Aucune dépendance à
l'API GitHub : tout est lu localement.
"""
import json
import re
import subprocess
from pathlib import Path

from mkdocs.structure.files import File

N_COMMITS = 60      # on en lit beaucoup, on filtre, on en garde MAX_SHOWN
MAX_SHOWN = 12
SEP = "\x1f"

STATUS_MAP = {
    "A": "added",
    "M": "modified",
    "D": "removed",
    "R": "renamed",
    "C": "renamed",
    "T": "modified",
}


def _run(args):
    return subprocess.run(
        args, capture_output=True, text=True, encoding="utf-8", cwd=Path.cwd()
    ).stdout


def _repo_url():
    url = _run(["git", "config", "--get", "remote.origin.url"]).strip()
    m = re.search(r"github\.com[:/](.+?)(?:\.git)?$", url)
    return f"https://github.com/{m.group(1)}" if m else None


def _page_url(rel):
    """content/livre/armes.md -> content/livre/armes/ (use_directory_urls)."""
    if not rel.endswith(".md"):
        return None
    p = rel[:-3]
    if p == "index":
        return "."
    if p.endswith("/index"):
        return p[:-5]          # content/livre/index -> content/livre/
    return p + "/"             # content/livre/armes -> content/livre/armes/


def _content_file(status, path, docs_rel, content_prefix):
    """Transforme (statut, chemin dépôt) en entrée de fichier de contenu, ou None."""
    if not path.startswith(content_prefix) or not path.endswith(".md"):
        return None
    rel = path[len(docs_rel) + 1:]
    url = None if status == "removed" else _page_url(rel)
    return {"status": status, "filename": rel, "url": url}


def _working_changes(docs_rel, content_prefix):
    """Fichiers de contenu modifiés dans le dossier de travail (non committés).
    Vide sur un dépôt propre (ex. déploiement CI)."""
    raw = _run(["git", "-c", "core.quotepath=false", "status", "--porcelain"])
    files = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        xy, rest = line[:2], line[3:]
        if "->" in rest:                       # renommage : on garde le nouveau nom
            rest = rest.split("->")[-1]
        path = rest.strip().strip('"')
        if xy == "??" or "A" in xy:
            status = "added"
        elif "D" in xy:
            status = "removed"
        elif "R" in xy:
            status = "renamed"
        else:
            status = "modified"
        cf = _content_file(status, path, docs_rel, content_prefix)
        if cf:
            files.append(cf)
    return files


def _parse_log(raw):
    """Renvoie une liste de commits avec leurs fichiers bruts (chemin dépôt)."""
    commits = []
    current = None
    for line in raw.splitlines():
        if SEP in line:
            if current:
                commits.append(current)
            sha, author, date, message = line.split(SEP)
            current = {
                "sha": sha, "short": sha[:7], "author": author,
                "date": date, "message": message, "_files": [],
            }
        elif line.strip() and current is not None:
            parts = line.split("\t")
            status = STATUS_MAP.get(parts[0][0], "modified")
            current["_files"].append((status, parts[-1]))
    if current:
        commits.append(current)
    return commits


def on_files(files, config, **kwargs):
    base_url = _repo_url()
    docs_rel = Path(config["docs_dir"]).resolve().relative_to(
        Path.cwd().resolve()
    ).as_posix()
    content_prefix = f"{docs_rel}/content/"

    raw = _run([
        "git", "log", f"-n{N_COMMITS}", "--no-merges",
        f"--pretty=format:%H{SEP}%an{SEP}%aI{SEP}%s", "--name-status",
    ])

    out = []

    # Modifications en cours (non committées) — en tête, vide sur dépôt propre.
    pending = _working_changes(docs_rel, content_prefix)
    if pending:
        author = _run(["git", "config", "user.name"]).strip() or "—"
        out.append({
            "short": "local",
            "author": author,
            "date": None,
            "message": "Modifications en cours (non committées)",
            "url": None,
            "pending": True,
            "files": pending,
        })

    for c in _parse_log(raw) if raw.strip() else []:
        content_files = []
        for status, path in c["_files"]:
            cf = _content_file(status, path, docs_rel, content_prefix)
            if cf:
                content_files.append(cf)
        if not content_files:
            continue
        out.append({
            "short": c["short"],
            "author": c["author"],
            "date": c["date"],
            "message": c["message"],
            "url": f"{base_url}/commit/{c['sha']}" if base_url else None,
            "files": content_files,
        })
        if len(out) >= MAX_SHOWN:
            break

    content = json.dumps(out, ensure_ascii=False, indent=0)
    files.append(File.generated(config, "changelog.json", content=content))
    return files
