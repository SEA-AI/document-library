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
CATEGORIES = {  # page order and headings; the website uses the same ids and labels
    "software": "Software releases",
    "desktop": "Desktop application",
    "cad": "CAD: 2D drawings and 3D models",
    "guides": "Guides",
    "wiring": "Wiring diagrams",
    "datasheets": "Datasheets",
}


def sort_key(catalog: dict, e: dict) -> tuple:
    """Current versions before legacy ones; desktop installers by operating system; then by title."""
    legacy = "(legacy)" in catalog["releases"].get(e.get("release", ""), {}).get("title", "")
    os_rank = next((i for i, prefix in enumerate(DESKTOP_OS) if e["title"].startswith(prefix)), len(DESKTOP_OS))
    return legacy, os_rank, e["title"].lower()


def render(catalog: dict, product: str) -> str:
    """One section per category, in CATEGORIES order; empty categories are left out."""
    name = catalog["products"][product]
    base = f"https://github.com/{catalog['repository']}/releases"

    def link(e: dict) -> str:
        if "path" in e:
            return f"[{e['title']}]({quote('../../' + e['path'])})"
        return f"[{e['title']}]({base}/download/{e['release']}/{quote(e['asset'])})"

    def release(e: dict) -> str:
        return f"[{catalog['releases'][e['release']]['title']}]({base}/tag/{e['release']})"

    lines = ["<!-- Generated from catalog.json by tools/build_readmes.py. Do not edit by hand. -->", f"# {name}"]
    manual = catalog.get("manuals", {}).get(product)
    if manual:
        languages = " · ".join(f"[{code.upper()}]({url})" for code, url in manual["languages"].items())
        lines += ["", "## User manual", "",
                  f"[{manual['title']}]({manual['url']}), software {manual['version']}: {manual['summary'].lower()}.",
                  "", f"Online in: {languages}. [Printable PDF]({manual['pdf']})."]
    for category, heading in CATEGORIES.items():
        files = sorted((e for e in catalog["files"] if e["products"].get(product) == category),
                       key=lambda e: sort_key(catalog, e))
        if not files:
            continue
        lines += ["", f"## {heading}", ""]
        if category == "software":
            lines += ["| File | Release |", "|---|---|"] + [f"| {link(e)} | {release(e)} |" for e in files]
        elif category == "desktop":
            os_name = lambda e: next((v for k, v in DESKTOP_OS.items() if e["title"].startswith(k)), "Other")  # noqa: E731
            lines += ["| Operating system | File | Release |", "|---|---|---|"]
            lines += [f"| {os_name(e)} | {link(e)} | {release(e)} |" for e in files]
        elif category == "cad":
            lines += ["| File | Kind |", "|---|---|"]
            lines += [f"| {link(e)} | {'3D model' if 'release' in e else '2D drawing'} |" for e in files]
        else:
            lines += ["| Document |", "|---|"] + [f"| {link(e)} |" for e in files]
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
