#!/usr/bin/env python3
"""Write a demo vault with about 30 notes, to look at the graph view and the theme.

Usage:
  python3 scripts/make_demo_vault.py PATH [--mode light|dark] [--notes N]

PATH must not exist or must be an empty folder. The vault gets notes in three folders,
with tags, links, attachments, and links to notes that do not exist, so that the graph
shows all node types. It also gets a graph.json with color groups from the palette, and
an appearance.json that chooses the theme Lexmechanic and turns on the two snippets.
The notes are the same on each run. The script does not touch any other folder. Run
scripts/install.sh PATH to copy the theme into the vault. It uses only the standard library.
"""
import base64
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import graph_groups  # noqa: E402

PNG = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==")
FOLDERS = {"Projects": ["project", "work"], "Ideas": ["idea"], "Inbox": ["inbox", "idea"]}
WORDS = ["Garden", "Ledger", "Compass", "Orchard", "Lantern", "Harbor", "Quarry", "Meadow", "Atlas", "Cipher",
         "Beacon", "Folio", "Gazette", "Herbarium", "Index", "Journal", "Kiln", "Loom", "Mosaic", "Nocturne"]


def build(path, count=30, mode="light"):
    """Write the vault into path and return the list of note names."""
    path = Path(path)
    if path.exists() and any(path.iterdir()):
        raise SystemExit(f"{path} is not empty")
    rng = random.Random(7)
    names = []
    for i in range(count):
        names.append((f"{rng.choice(WORDS)} {i + 1:02d}", list(FOLDERS)[i % 3]))
    (path / ".obsidian").mkdir(parents=True)
    (path / "Attachments").mkdir()
    for n in (1, 2, 3):
        (path / "Attachments" / f"diagram-{n}.png").write_bytes(PNG)
    for i, (name, folder) in enumerate(names):
        (path / folder).mkdir(exist_ok=True)
        links = [f"[[{rng.choice(names)[0]}]]" for _ in range(rng.randint(1, 3))]
        if i % 5 == 0:
            links.append(f"[[Missing note {i // 5 + 1}]]")
        if i % 7 == 0:
            links.append(f"![[diagram-{i // 7 % 3 + 1}.png]]")
        tags = " ".join(f"#{t}" for t in FOLDERS[folder])
        (path / folder / f"{name}.md").write_text(
            f"---\ntags: [{', '.join(FOLDERS[folder])}]\n---\n# {name}\n\nA note in {folder}. {tags}\n\nSee " + ", ".join(links) + ".\n")
    groups = [graph_groups.group(s, graph_groups.palette(mode)) for s in ("tag:#idea=yellow", "tag:#project=blue", "path:Inbox=sand")]
    graph = json.loads((Path(__file__).resolve().parent.parent / "examples" / "graph.json").read_text())
    graph["colorGroups"] = groups
    (path / ".obsidian" / "graph.json").write_text(json.dumps(graph, indent=2) + "\n")
    (path / ".obsidian" / "appearance.json").write_text(json.dumps({
        "cssTheme": "Lexmechanic", "theme": "obsidian" if mode == "dark" else "moonstone",
        "enabledCssSnippets": ["lexmechanic-extras", "lexmechanic-fun"]}, indent=2) + "\n")
    (path / ".obsidian" / "app.json").write_text(json.dumps({"readableLineLength": True}) + "\n")
    return [n for n, _ in names]


def main(argv):
    if not argv or argv[0].startswith("-"):
        print(__doc__)
        return 2
    mode = argv[argv.index("--mode") + 1] if "--mode" in argv else "light"
    count = int(argv[argv.index("--notes") + 1]) if "--notes" in argv else 30
    names = build(argv[0], count, mode)
    print(f"wrote {len(names)} notes into {argv[0]}. Run: scripts/install.sh {argv[0]}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
