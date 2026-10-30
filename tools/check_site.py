"""Test the document library website, locally or live, as an anonymous visitor.

Checks:
  - the page loads with no failed request, script error or console error on the site itself
  - the page loads nothing from hosts outside ALLOWED_HOSTS
  - every catalog product has a card on the page (it must be in content.js)
  - the file lists show exactly the listings catalog.json defines (product, type, name)
  - every document link is on the site, opens in a new tab and serves the file at catalog size
  - every software and CAD link downloads the release file at catalog size, without cookies
  - clicking a PDF opens a tab that loads that document

Usage (from the repository root):
    uv run --with requests --with playwright python tools/check_site.py          # this repo, served as Pages would
    uv run --with requests --with playwright python tools/check_site.py --url https://sea-ai.github.io/document-library/

First run on a new machine: `uv run --with playwright playwright install chromium`.
"""

import argparse
import functools
import http.server
import sys
import threading
from pathlib import Path
from urllib.parse import urlparse

import requests
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PREFIX = "/document-library"
# Hosts the page may load from besides its own (web font).
ALLOWED_HOSTS = {"fonts.googleapis.com", "fonts.gstatic.com"}


def serve_repo(root: Path) -> tuple[str, http.server.ThreadingHTTPServer]:
    """Serve the repository under /document-library/, the path GitHub Pages uses."""

    class Handler(http.server.SimpleHTTPRequestHandler):
        def translate_path(self, path: str) -> str:
            if not path.startswith(PREFIX + "/"):
                return str(root / "__missing__")
            return super().translate_path(path[len(PREFIX):])

        def log_message(self, *args: object) -> None:
            pass

    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Handler, directory=str(root)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{server.server_address[1]}{PREFIX}/", server


def expected_listings(catalog: dict) -> set[tuple[str, str, str]]:
    return {(p, t, f["title"]) for f in catalog["files"] for p, t in f["products"].items()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--url", help="live site URL; default: serve this repository")
    parser.add_argument("--repo-dir", type=Path, default=ROOT, help="repository to serve (default: this one)")
    args = parser.parse_args()

    server = None
    site = args.url if args.url else None
    if site is None:
        site, server = serve_repo(args.repo_dir.resolve())
    if not site.endswith("/"):
        site += "/"
    own_host = urlparse(site).netloc

    catalog = requests.get(site + "catalog.json", timeout=30).json()
    sizes = {f["title"]: f["size"] for f in catalog["files"]}
    failures: list[str] = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        ctx = browser.new_context(accept_downloads=True)
        page = ctx.new_page()
        problems: list[str] = []
        hosts: set[str] = set()
        page.on("request", lambda r: hosts.add(urlparse(r.url).netloc) if r.url.startswith("http") else None)
        page.on("requestfailed", lambda r: problems.append(f"failed {r.url}"))
        page.on("response", lambda r: problems.append(f"{r.status} {r.url}") if r.status >= 400 else None)
        page.on("pageerror", lambda e: problems.append(f"script error {e}"))
        page.on("console", lambda m: problems.append(f"console error {m.text}") if m.type == "error" else None)
        page.goto(site, wait_until="networkidle")
        page.wait_for_function("window.MANIFEST && window.MANIFEST.products", timeout=15000)
        own = [p for p in problems if site in p or p.startswith(("script error", "console error"))]
        print(f"Page load: {len(own)} problems on the site, {len(problems) - len(own)} elsewhere {problems[:3]}")
        failures += own

        foreign = sorted(hosts - ALLOWED_HOSTS - {own_host})
        print(f"Hosts loaded: {sorted(hosts)}; not allowed: {foreign or 'none'}")
        if foreign:
            failures.append(f"page loads from hosts outside the allowlist: {foreign}")

        links = page.evaluate("""() => { const out = [];
          for (const p of Object.keys(window.MANIFEST.products))
            for (const s of window.SECTIONS) {
              showFileListModal(p, s.id);
              document.querySelectorAll('a.file-link').forEach(a =>
                out.push({p, s: s.id, t: a.closest('[data-type]').dataset.type, name: a.dataset.title,
                          href: a.href, target: a.target}));
            }
          closeFileListModal(); return out; }""")
        carded = page.evaluate("ids => ids.filter(id => document.querySelector('#' + id + ' .doc-type-link'))",
                               list(catalog["products"]))
        missing_cards = sorted(set(catalog["products"]) - set(carded))
        print(f"Product cards: {len(carded)}/{len(catalog['products'])} catalog products have a card {missing_cards or ''}")
        if missing_cards:
            failures.append(f"no product card for {missing_cards}: add them to content.js products.items")

        got = {(l["p"], l["t"], l["name"]) for l in links}
        want = expected_listings(catalog)
        print(f"Listings: {len(links)} shown, {len(want)} in catalog, identical: {got == want}")
        if got != want:
            failures.append(f"listings differ: missing {sorted(want - got)[:3]}, extra {sorted(got - want)[:3]}")

        checked: dict[str, bool] = {}
        for link in links:
            if link["href"] in checked:
                continue
            on_site = link["href"].startswith(site)
            if on_site:
                resp = requests.get(link["href"], timeout=120)
                size = len(resp.content)
            else:
                resp = requests.head(link["href"], allow_redirects=True, timeout=120)
                size = int(resp.headers.get("content-length", -1))
            ok = (resp.status_code == 200 and size == sizes[link["name"]]
                  and "text/html" not in resp.headers.get("content-type", "")
                  and (link["target"] == "_blank") == on_site)
            checked[link["href"]] = ok
            if not ok:
                failures.append(f"{link['name']}: HTTP {resp.status_code}, {size} bytes, target '{link['target']}'")
        docs = sum(1 for h in checked if h.startswith(site))
        print(f"Files: {sum(checked.values())}/{len(checked)} OK "
              f"({docs} documents on the site, {len(checked) - docs} release downloads)")

        first_pdf = next((l for l in links if l["href"].startswith(site) and l["name"].lower().endswith(".pdf")), None)
        if first_pdf:
            page.evaluate("([p, s]) => showFileListModal(p, s)", [first_pdf["p"], first_pdf["s"]])
            loaded: list[str] = []
            # Headless Chromium has no PDF viewer: it saves the PDF and reports it on the opener.
            ctx.on("page", lambda tab: tab.on("download", lambda d: loaded.append(d.url)))
            page.on("download", lambda d: loaded.append(d.url))
            page.on("popup", lambda tab: tab.on("load", lambda: loaded.append(tab.url)))
            page.locator(f'a.file-link[data-title="{first_pdf["name"]}"]').first.click()
            for _ in range(120):
                if loaded:
                    break
                page.wait_for_timeout(250)
            ok = first_pdf["href"] in loaded
            print(f"PDF click opens the document in a tab: {ok}")
            if not ok:
                failures.append(f"PDF click loaded {loaded}")
        browser.close()

    if server:
        server.shutdown()
    print("RESULT: " + ("PASS" if not failures else "FAIL\n  " + "\n  ".join(failures[:20])))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
