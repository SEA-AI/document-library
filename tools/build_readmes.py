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


DESKTOP_OS = {"WIN_": "Windows", "MAC_": "macOS", "LINUX_": "Linux"}  # file name prefix -> system


def section(e: dict) -> str:
    """Which part of the product page lists a file."""
    if e["title"].lower().endswith(".oscar"):
        return "software"
    if e.get("release", "").startswith("desktop-"):
        return "desktop"
    if "-cad-" in e.get("release", ""):
        return "cad"
    return "documents"


def render(catalog: dict, product: str) -> str:
    """Sections in fixed order: software releases, SEA.AI Desktop, 3D CAD models, documents."""
    name = catalog["products"][product]
    base = f"https://github.com/{catalog['repository']}/releases"
    entries = [e for e in catalog["files"] if product in e["products"]]

    def link(e: dict) -> str:
        if "path" in e:
            return f"[{e['title']}]({quote('../../' + e['path'])})"
        return f"[{e['title']}]({base}/download/{e['release']}/{quote(e['asset'])})"

    def release(e: dict) -> str:
        return f"[{catalog['releases'][e['release']]['title']}]({base}/tag/{e['release']})"

    def files(kind: str) -> list[dict]:
        return [e for e in entries if section(e) == kind]

    lines = ["<!-- Generated from catalog.json by tools/build_readmes.py. Do not edit by hand. -->", f"# {name}"]

    software = sorted(files("software"), key=lambda e: ("(legacy)" in release(e), e["title"].lower()))
    if software:
        lines += ["", "## Software releases", "", "| File | Release |", "|---|---|"]
        lines += [f"| {link(e)} | {release(e)} |" for e in software]

    order = list(DESKTOP_OS)
    os_of = lambda e: next((p for p in order if e["title"].startswith(p)), "")  # noqa: E731
    desktop = sorted(files("desktop"), key=lambda e: (order.index(os_of(e)) if os_of(e) else len(order), e["title"]))
    if desktop:
        lines += ["", "## SEA.AI Desktop", "", "| Operating system | File | Release |", "|---|---|---|"]
        lines += [f"| {DESKTOP_OS.get(os_of(e), 'Other')} | {link(e)} | {release(e)} |" for e in desktop]

    cad = sorted(files("cad"), key=lambda e: e["title"].lower())
    if cad:
        lines += ["", "## 3D CAD models", "", "| File | Release |", "|---|---|"]
        lines += [f"| {link(e)} | {release(e)} |" for e in cad]

    documents = sorted(files("documents"), key=lambda e: e["title"].lower())
    if documents:
        lines += ["", "## Documents", "", "| Document | Type |", "|---|---|"]
        lines += [f"| {link(e)} | {e['products'][product]} |" for e in documents]

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
