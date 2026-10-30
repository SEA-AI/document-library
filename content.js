// ─────────────────────────────────────────────────────────────────────────────
//  SEA.AI Document Library — Content Configuration
//
//  Edit this file to update any copy on the page.
//  The page reads entirely from this object — no strings live in index.html.
// ─────────────────────────────────────────────────────────────────────────────

var CONTENT = {

  // ── NAV ────────────────────────────────────────────────────────────────────
  nav: {
    sector:     'Docs',
    links: [
      { label: 'Watchkeeper', href: '#watchkeeper' },
      { label: 'Sentry',      href: '#sentry'      },
      { label: 'Brain',       href: '#brain'       },
      { label: 'Competition', href: '#competition' },
      { label: 'Offshore',    href: '#offshore'    }
    ],
    ctaBack:    'Return to SEA.AI',
    mobileBack: '← SEA.AI'
  },

  // ── HERO ───────────────────────────────────────────────────────────────────
  hero: {
    h1:        'SEA.AI<br /><em>Product Documentation</em>',
    lead:      'Technical documentation, guides, and resources for SEA.AI products. Find support materials, integration guides, and product specifications.',
    copyright: ''
  },

  // ── PRODUCTS ───────────────────────────────────────────────────────────────
  products: {
    label: 'Products',
    h2:    'Browse documentation by<br /><em>product</em>',
    items: [
      {
        id:    'watchkeeper',
        h3:    'Watchkeeper',
        img:   'assets/images/products/watchkeeper.png',
        imgAlt: 'SEA.AI Watchkeeper',
        p:     'Compact fixed-mount EO/IR system for navigation safety and close-range detection.',
        docTypes: [
          { label: 'User and installation manual', count: 7 },
          { label: 'Software releases',            count: 2 },
          { label: 'Desktop application',          count: 2 },
          { label: 'CAD',                          count: 3 },
          { label: 'Guides',                       count: 0 },
          { label: 'Wiring diagrams',              count: 3 },
          { label: 'Datasheets',                   count: 2 }
        ]
      },
      {
        id:    'sentry',
        h3:    'Sentry',
        img:   'assets/images/products/sentry.png',
        imgAlt: 'SEA.AI Sentry',
        p:     'Full-perimeter EO/IR surveillance with AI auto-track and optical zoom capabilities.',
        docTypes: [
          { label: 'User and installation manual', count: 7 },
          { label: 'Software releases',            count: 2 },
          { label: 'Desktop application',          count: 2 },
          { label: 'CAD',                          count: 4 },
          { label: 'Guides',                       count: 2 },
          { label: 'Wiring diagrams',              count: 4 },
          { label: 'Datasheets',                   count: 1 }
        ]
      },
      {
        id:    'brain',
        h3:    'Brain',
        img:   'assets/images/products/brain.png',
        imgAlt: 'SEA.AI Brain',
        p:     'Advanced analytics and processing platform for real-time operational intelligence.',
        docTypes: [
          { label: 'User and installation manual', count: 0 },
          { label: 'Software releases',            count: 1 },
          { label: 'Desktop application',          count: 2 },
          { label: 'CAD',                          count: 1 },
          { label: 'Guides',                       count: 2 },
          { label: 'Wiring diagrams',              count: 3 },
          { label: 'Datasheets',                   count: 1 }
        ]
      },
      {
        id:    'competition',
        h3:    'Competition',
        img:   'assets/images/products/competition.png',
        imgAlt: 'SEA.AI Competition',
        p:     'Competitive analysis and benchmarking tools for system evaluation.',
        docTypes: [
          { label: 'User and installation manual', count: 0 },
          { label: 'Software releases',            count: 2 },
          { label: 'Desktop application',          count: 2 },
          { label: 'CAD',                          count: 2 },
          { label: 'Guides',                       count: 3 },
          { label: 'Wiring diagrams',              count: 6 },
          { label: 'Datasheets',                   count: 0 }
        ]
      },
      {
        id:    'offshore',
        h3:    'Offshore',
        img:   'assets/images/products/offshore.webp',
        imgAlt: 'SEA.AI Offshore',
        p:     'Marine and offshore operations platform for extended deployment scenarios.',
        docTypes: [
          { label: 'User and installation manual', count: 0 },
          { label: 'Software releases',            count: 1 },
          { label: 'Desktop application',          count: 2 },
          { label: 'CAD',                          count: 4 },
          { label: 'Guides',                       count: 5 },
          { label: 'Wiring diagrams',              count: 12 },
          { label: 'Datasheets',                   count: 0 }
        ]
      }
    ]
  },

  // ── FOOTER ─────────────────────────────────────────────────────────────────
  footer: {
    brandP: 'Technical documentation and product resources from SEA.AI.',
    copyright: '© 2026 SEA.AI GmbH · Linz, Austria · All rights reserved.',
    cols: [
      {
        h4: 'Products',
        links: [
          { label: 'Watchkeeper', href: '#watchkeeper' },
          { label: 'Sentry',      href: '#sentry'      },
          { label: 'Brain',       href: '#brain'       },
          { label: 'Competition', href: '#competition' },
          { label: 'Offshore',    href: '#offshore'    }
        ]
      },
      {
        h4: 'About',
        links: [
          { label: 'About SEA.AI', href: 'https://www.sea.ai/about/' }
        ]
      }
    ]
  }
};
