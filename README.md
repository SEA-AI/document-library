# SEA.AI Customer Document Library

This repository contains official customer documentation and software for SEA.AI products.

SEA.AI makes machine vision systems for vessels. The systems use thermal and
optical cameras with AI to detect objects on the water. They act as a
collision avoidance assistant for the crew.

## Find your files

Browse everything on the document library website: https://sea-ai.github.io/document-library/

Or open your product's page here. It lists every document and software file for that product.

| Product | Page |
|---|---|
| Sentry | [products/sentry](products/sentry/README.md) |
| Watchkeeper | [products/watchkeeper](products/watchkeeper/README.md) |
| Brain | [products/brain](products/brain/README.md) |
| Offshore | [products/offshore](products/offshore/README.md) |
| Competition | [products/competition](products/competition/README.md) |

- **Documents** (PDF): user guides, installation manuals, drawings and specifications. They sit
  in each product's `documents/` folder; documents for several products sit in
  `shared/documents/`. Open one to read it in the browser, or download it.
- **Software and CAD**: system software updates (`.oscar`), the SEA.AI Desktop application and
  3D CAD data. They are on the [Releases](../../releases) page, one release per version. Each
  release includes a `SHA256SUMS` file to check your download.

## Support

For help, contact [support email or URL].

## Copyright

© [year] SEA.AI. All rights reserved. [Add license terms.]

---

## For maintainers

`catalog.json` lists every published file: its title, the products that show it, its document
type on each product's page (`Support`, `Guides`, `Help`, `Info`), where it is stored, its size
and its SHA-256. Release files also record the asset name GitHub stored (`asset`), since GitHub
rewrites spaces to dots; `tools/validate_catalog.py --releases` reports the right value.

**The website** is `index.html`, `content.js` and `assets/`, served by GitHub Pages from the
root of `develop`. The page reads `catalog.json` directly, so a merged change to the catalog is
live within minutes. Page text is in `content.js`; layout, style and behaviour in `index.html`.

**Add or replace a document:** put the PDF in `products/<product>/documents/` (or
`shared/documents/` if several products use it), add or update its entry in `catalog.json`, run
`python tools/build_readmes.py`, and open a pull request. Get size and checksum with
`python -c "import hashlib,os,sys; p=sys.argv[1]; print(os.path.getsize(p), hashlib.sha256(open(p,'rb').read()).hexdigest())" <file>`.

**Publish software or CAD:** create a new release, tag `<component>-<version>` (for example
`sentry-software-4.5-0`, `desktop-1.2.5`, `sentry-cad-2026.11`). Upload each file with its
display name as the asset label, plus a `SHA256SUMS` file. Then add the release and its files to
`catalog.json` in a pull request. Never replace the files of an existing release: publish a new
version.

**Checks:** every pull request runs `tools/validate_catalog.py --releases` and
`tools/build_readmes.py --check`. Locally: `pip install jsonschema`, then the same commands.

Everything in this repository is public. Never add internal or customer-specific material.
