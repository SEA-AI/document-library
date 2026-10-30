# SEA.AI Customer Document Library

Official documentation and software for SEA.AI products.

SEA.AI makes machine vision systems for vessels. The systems use thermal and
optical cameras with AI to detect objects on the water. They act as a
collision avoidance assistant for the crew.

## Find your files

The easiest way is the document library website:
**https://sea-ai.github.io/document-library/**

You can also open your product's page here:

| Product | Page |
|---|---|
| Sentry | [Sentry](products/sentry/README.md) |
| Watchkeeper | [Watchkeeper](products/watchkeeper/README.md) |
| Brain | [Brain](products/brain/README.md) |
| Offshore | [Offshore](products/offshore/README.md) |
| Competition | [Competition](products/competition/README.md) |

## What you find here

- **User and installation manual (Sentry, Watchkeeper):** one manual for use, installation and care,
  as a PDF in English, German, French, Spanish, Portuguese, Italian and Arabic.
- **Software releases:** system software updates (`.oscar` files) for your SEA.AI system.
- **Desktop application:** SEA.AI Desktop for Windows and macOS.
- **CAD:** 2D drawings (PDF) and 3D models.
- **Technical documents:**
  - **Guides:** user guides, installation manuals, and integration and configuration guides.
  - **Wiring diagrams:** harness, interconnect, electrical and wiring diagrams.
  - **Datasheets:** product specifications.

Documents (PDF) open in your browser or download. Software and 3D models are on the
[Releases](../../releases) page, one release per version.

## Check a download

Each release includes a `SHA256SUMS` file with the checksum of every file in it. To confirm that a
download is complete and unchanged, compute its checksum and compare it with that list:

- Windows (Command Prompt): `certutil -hashfile <file> SHA256`
- macOS: `shasum -a 256 <file>`

## Before you update system software

Read the update steps first: in the user and installation manual (chapter "Update the software")
for Sentry and Watchkeeper, or in your product's guides. Software marked
"legacy" is an earlier version: ask SEA.AI support before installing it. If you are unsure which
version fits your system, contact SEA.AI support.

## Support

For help, contact SEA.AI support: https://www.sea.ai/contact/

## Copyright and terms of use

© 2026 SEA.AI. All rights reserved. The documents and software in this repository may be used only
under the [Terms of Use](LICENSE.md).
