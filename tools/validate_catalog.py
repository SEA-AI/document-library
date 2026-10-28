"""Check that catalog.json and the repository agree. CI runs this on every pull request.

Checks:
  - catalog.json matches schema/catalog.schema.json
  - every product and release a file names is declared; every release holds a file
  - categories fit the file: .oscar in software, desktop-* releases in desktop, *-cad-* releases
    in cad; documents never in software or desktop
  - each document entry names one product and sits in products/<id>/documents/ (a document for
    several products is copied into each folder); the file name equals the title
  - every document exists, matches its size and sha256, and is under 100 MB (git limit)
  - every file in a documents folder is listed in the catalog
  - no product lists two files with the same title
  - every online manual names a declared product, and its English link is its main link
  - with --releases: every release exists on GitHub with an asset labelled with each title,
    of the catalog size and stored under the catalog's asset name (uses GITHUB_TOKEN if set)

Usage:
    pip install jsonschema
    python tools/validate_catalog.py [--releases]
"""

import argparse
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAX_GIT_FILE = 100 * 1024 * 1024
DOC_DIRS = ("products/*/documents",)


def expected_path(entry: dict) -> str:
    return f"products/{next(iter(entry['products']))}/documents/{entry['title']}"


def expected_category(entry: dict) -> str | None:
    """The category a release file must have, from its type and release; None for documents."""
    if entry["title"].lower().endswith(".oscar"):
        return "software"
    release = entry.get("release", "")
    if release.startswith("desktop-"):
        return "desktop"
    if "-cad-" in release:
        return "cad"
    return None


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def check_schema(catalog: dict) -> list[str]:
    try:
        import jsonschema
    except ImportError:
        return ["jsonschema is not installed: pip install jsonschema"]
    schema = json.loads((ROOT / "schema" / "catalog.schema.json").read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    return [f"schema: {'/'.join(map(str, e.path)) or '(root)'}: {e.message}" for e in validator.iter_errors(catalog)]


def check_catalog(catalog: dict) -> list[str]:
    errors = []
    files = catalog["files"]
    used_releases = set()
    for entry in files:
        name = entry["title"]
        for product in entry["products"]:
            if product not in catalog["products"]:
                errors.append(f"{name}: unknown product '{product}'")
        expected = expected_category(entry)
        for product, category in entry["products"].items():
            if expected and category != expected:
                errors.append(f"{name}: category on {product} should be '{expected}', is '{category}'")
            if "path" in entry and category in ("software", "desktop"):
                errors.append(f"{name}: documents cannot be in '{category}'")
        if "release" in entry:
            used_releases.add(entry["release"])
            if entry["release"] not in catalog["releases"]:
                errors.append(f"{name}: release '{entry['release']}' is not declared in releases")
            continue
        if len(entry["products"]) != 1:
            errors.append(f"{name}: a document entry names one product; copy the file into each product's folder")
        if entry["path"] != expected_path(entry):
            errors.append(f"{name}: path should be {expected_path(entry)}")
        path = ROOT / entry["path"]
        if not path.is_file():
            errors.append(f"{entry['path']}: listed but missing")
            continue
        if path.stat().st_size != entry["size"]:
            errors.append(f"{entry['path']}: size {path.stat().st_size}, catalog says {entry['size']}")
        if path.stat().st_size >= MAX_GIT_FILE:
            errors.append(f"{entry['path']}: over 100 MB, publish it in a release instead")
        if sha256(path) != entry["sha256"]:
            errors.append(f"{entry['path']}: sha256 differs from catalog")

    for tag in sorted(set(catalog["releases"]) - used_releases):
        errors.append(f"release '{tag}' holds no file")

    listed = {e["path"] for e in files if "path" in e}
    for pattern in DOC_DIRS:
        for path in sorted(ROOT.glob(f"{pattern}/*")):
            rel = path.relative_to(ROOT).as_posix()
            if rel not in listed:
                errors.append(f"{rel}: not listed in catalog.json")

    for kind, keys in (("path", [e["path"] for e in files if "path" in e]),
                       ("release asset", [(e["release"], e["title"]) for e in files if "release" in e])):
        for key, count in Counter(keys).items():
            if count > 1:
                errors.append(f"{kind} listed {count} times: {key}")

    per_product = Counter((p, e["title"]) for e in files for p in e["products"])
    for (product, title), count in per_product.items():
        if count > 1:
            errors.append(f"{product}: {count} files titled '{title}'")

    for product, manual in catalog.get("manuals", {}).items():
        if product not in catalog["products"]:
            errors.append(f"manual '{manual['title']}': unknown product '{product}'")
        if manual["languages"]["en"] != manual["url"]:
            errors.append(f"manual '{manual['title']}': languages.en should equal url")
    return errors


def check_releases(catalog: dict) -> list[str]:
    errors = []
    headers = {"Accept": "application/vnd.github+json"}
    if os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    for tag in sorted(catalog["releases"]):
        url = f"https://api.github.com/repos/{catalog['repository']}/releases/tags/{tag}"
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as resp:
                assets = {(a.get("label") or a["name"]): a for a in json.load(resp)["assets"]}
        except urllib.error.HTTPError as exc:
            errors.append(f"release '{tag}': GitHub returned {exc.code}")
            continue
        for entry in catalog["files"]:
            if entry.get("release") != tag:
                continue
            asset = assets.get(entry["title"])
            if asset is None:
                errors.append(f"release '{tag}': no asset labelled '{entry['title']}'")
                continue
            if asset["size"] != entry["size"]:
                errors.append(f"release '{tag}': '{entry['title']}' is {asset['size']} bytes, catalog says {entry['size']}")
            if asset["name"] != entry["asset"]:
                errors.append(f"release '{tag}': '{entry['title']}' is stored as asset '{asset['name']}', catalog says '{entry['asset']}'")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--releases", action="store_true", help="also check the release assets on GitHub")
    args = parser.parse_args()

    catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    errors = check_schema(catalog)
    if not errors:
        errors = check_catalog(catalog)
        if args.releases:
            errors += check_releases(catalog)
    for error in errors:
        print(f"ERROR {error}")
    docs = sum(1 for e in catalog["files"] if "path" in e)
    print(f"{len(catalog['files'])} files ({docs} documents, {len(catalog['files']) - docs} release assets "
          f"in {len(catalog['releases'])} releases): {'FAILED' if errors else 'OK'}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
