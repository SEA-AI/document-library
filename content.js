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
        p:     'Compact fixed-mount EO/IR system for navigation safety and close-range detection.',
        docTypes: [
          { label: 'Support',  count: 4 },
          { label: 'Guides',   count: 1 },
          { label: 'Help',     count: 2 },
          { label: 'Info',     count: 8 }
        ]
      },
      {
        id:    'sentry',
        h3:    'Sentry',
        p:     'Full-perimeter EO/IR surveillance with AI auto-track and optical zoom capabilities.',
        docTypes: [
          { label: 'Support',  count: 6 },
          { label: 'Guides',   count: 4 },
          { label: 'Help',     count: 2 },
          { label: 'Info',     count: 7 }
        ]
      },
      {
        id:    'brain',
        h3:    'Brain',
        p:     'Advanced analytics and processing platform for real-time operational intelligence.',
        docTypes: [
          { label: 'Support',  count: 4 },
          { label: 'Guides',   count: 2 },
          { label: 'Info',     count: 7 }
        ]
      },
      {
        id:    'competition',
        h3:    'Competition',
        p:     'Competitive analysis and benchmarking tools for system evaluation.',
        docTypes: [
          { label: 'Support',  count: 2 },
          { label: 'Info',     count: 14 }
        ]
      },
      {
        id:    'offshore',
        h3:    'Offshore',
        p:     'Marine and offshore operations platform for extended deployment scenarios.',
        docTypes: [
          { label: 'Support',  count: 5 },
          { label: 'Info',     count: 20 }
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
