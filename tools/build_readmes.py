"""Write products/<id>/README.md, the per-product index, from catalog.json.

Usage:
    python tools/build_readmes.py           # write the files
    python tools/build_readmes.py --check   # fail if any file is out of date (CI)
"""

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent


def render(catalog: dict, product: str) -> str:
    name = catalog["products"][product]
    entries = sorted((e for e in catalog["files"] if product in e["products"]), key=lambda e: e["title"].lower())
    lines = [
        f"# {name}",
        "",
        "Generated from `catalog.json` by `tools/build_readmes.py`. Do not edit by hand.",
        "",
        "## Documents",
        "",
        "| Document | Type |",
        "|---|---|",
    ]
    for e in entries:
        if "path" in e:
            lines.append(f"| [{e['title']}]({quote('../../' + e['path'])}) | {e['products'][product]} |")
    lines += ["", "## Software and CAD", "", "| File | Type | Release |", "|---|---|---|"]
    for e in entries:
        if "release" in e:
            release = catalog["releases"][e["release"]]["title"]
            url = f"https://github.com/{catalog['repository']}/releases/tag/{e['release']}"
            lines.append(f"| {e['title']} | {e['products'][product]} | [{release}]({url}) |")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="fail if a README is out of date")
    args = parser.parse_args()

    catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    stale = []
    for product in catalog["products"]:
        path = ROOT / "products" / product / "README.md"
        text = render(catalog, product)
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                stale.append(path.relative_to(ROOT).as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8", newline="\n")
    if stale:
        print("Out of date, run python tools/build_readmes.py: " + ", ".join(stale))
        return 1
    print("Product READMEs " + ("up to date" if args.check else "written"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
