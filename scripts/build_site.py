#!/usr/bin/env python3
"""Build the static Hekman Home Services website.
The repository intentionally keeps its curated project photography at the root.
This script only writes maintainable HTML, CSS-adjacent assets, and route files;
it never deletes, renames, or rewrites project images.
"""
from __future__ import annotations
import html
import json
import re
from pathlib import Path
from textwrap import dedent
from site_projects import PROJECT_DETAILS, PROJECT_GALLERY_PRIORITY, PROJECTS
from site_services import SERVICES, SERVICE_CARD_VARIANTS, SERVICE_DISPLAY_ORDER
from site_discovery import llms_text
from site_misc_pages import contact_page, not_found_page, redirect_stub
ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://www.hekmanhomeservices.ca"
ASSET_VERSION = "20260818-1"
PHONE_DISPLAY = "519-808-3312"
PHONE_LINK = "+15198083312"
EMAIL = "hekmanhomeservices@gmail.com"
FACEBOOK = "https://www.facebook.com/p/Hekman-Home-Services-100066576836967/"
INSTAGRAM = "https://www.instagram.com/hekman_home_services_inc/"
AREAS = [
    "London, Ontario",
    "Westmount",
    "Sunningdale",
    "Old North",
    "Stoneybrook",
    "Byron",
    "Oakridge",
    "Riverbend",
    "Medway",
    "Hyde Park",
    "Old East Village",
    "Pond Mills",
    "Masonville",
    "Old South",
    "St. Thomas, Ontario",
]
def write(path: str, content: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(dedent(content).strip() + "\n", encoding="utf-8")
def schema(path: str, image: str) -> str:
    service_names = [item["name"] for item in SERVICES.values()]
    business = {
        "@type": ["HomeAndConstructionBusiness", "GeneralContractor", "LocalBusiness"],
        "@id": f"{BASE_URL}/#business",
        "name": "Hekman Home Services Inc.",
        "url": BASE_URL,
        "logo": f"{BASE_URL}/hekman-logo.jpg",
        "image": f"{BASE_URL}/{image}",
        "description": "Family-run renovation, repair and property improvement company based in Westmount and serving homeowners throughout London, St. Thomas and nearby communities.",
        "telephone": PHONE_LINK,
        "email": EMAIL,
        "sameAs": [FACEBOOK, INSTAGRAM],
        "areaServed": AREAS,
        "knowsAbout": service_names,
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Renovation and repair services",
            "itemListElement": [
                {
                    "@type": "Offer",
                    "itemOffered": {
                        "@type": "Service",
                        "name": name,
                        "areaServed": "London, Ontario and surrounding communities",
                    },
                }
                for name in service_names
            ],
        },
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "London",
            "addressRegion": "ON",
            "addressCountry": "CA",
        },
    }
    page = {
        "@type": "WebPage",
        "@id": f"{BASE_URL}{path}#webpage",
        "url": f"{BASE_URL}{path}",
        "isPartOf": {"@id": f"{BASE_URL}/#website"},
        "about": {"@id": f"{BASE_URL}/#business"},
        "primaryImageOfPage": {"@type": "ImageObject", "url": f"{BASE_URL}/{image}"},
    }
    website = {
        "@type": "WebSite",
        "@id": f"{BASE_URL}/#website",
        "url": f"{BASE_URL}/",
        "name": "Hekman Home Services Inc.",
        "publisher": {"@id": f"{BASE_URL}/#business"},
        "inLanguage": "en-CA",
    }
    graph: list[dict] = [business, website, page]
    service_slug = next(
        (slug for slug in SERVICES if path == service_url(slug)),
        None,
    )
    if service_slug:
        item = SERVICES[service_slug]
        service = {
            "@type": "Service",
            "@id": f"{BASE_URL}{path}#service",
            "name": item["name"],
            "serviceType": item["name"],
            "description": item["description"],
            "url": f"{BASE_URL}{path}",
            "provider": {"@id": f"{BASE_URL}/#business"},
            "areaServed": AREAS,
        }
        page["mainEntity"] = {"@id": service["@id"]}
        graph.append(service)
    project_detail = PROJECT_DETAILS.get(path)
    if project_detail:
        project_story = {
            "@type": "Article",
            "@id": f"{BASE_URL}{path}#project-story",
            "headline": project_detail["name"],
            "description": project_detail["description"],
            "image": f"{BASE_URL}/{project_detail['image']}",
            "mainEntityOfPage": {"@id": page["@id"]},
            "author": {"@id": f"{BASE_URL}/#business"},
            "publisher": {"@id": f"{BASE_URL}/#business"},
            "about": [{"@type": "Thing", "name": name} for name in project_detail["services"]],
            "contentLocation": {
                "@type": "Place",
                "name": project_detail["neighbourhood"],
            },
        }
        page["mainEntity"] = {"@id": project_story["@id"]}
        graph.append(project_story)
    if path != "/":
        crumbs = [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": f"{BASE_URL}/",
            }
        ]
        if path.startswith("/services/") and path != "/services/":
            crumbs.append(
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "Services",
                    "item": f"{BASE_URL}/services/",
                }
            )
        elif path.startswith("/projects/") and path != "/projects/":
            crumbs.append(
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "Our Work",
                    "item": f"{BASE_URL}/projects/",
                }
            )
        breadcrumb_name = (
            SERVICES[service_slug]["name"]
            if service_slug
            else project_detail["name"]
            if project_detail
            else path.strip("/").split("/")[-1].replace("-", " ").title()
        )
        crumbs.append(
            {
                "@type": "ListItem",
                "position": len(crumbs) + 1,
                "name": breadcrumb_name,
                "item": f"{BASE_URL}{path}",
            }
        )
        graph.append(
            {
                "@type": "BreadcrumbList",
                "@id": f"{BASE_URL}{path}#breadcrumb",
                "itemListElement": crumbs,
            }
        )
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, separators=(",", ":"))
def head(title: str, description: str, path: str, image: str, *, indexable: bool = True, image_alt: str | None = None) -> str:
    canonical = f"{BASE_URL}{path}"
    robots = "index,follow,max-image-preview:large" if indexable else "noindex,follow"
    structured_data = f'<script type="application/ld+json">{schema(path, image)}</script>' if indexable else ""
    social_image_alt = image_alt or PROJECT_DETAILS.get(path, {}).get("image_alt", "Hekman Home Services Inc.")
    return f"""
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>{title}</title>
      <meta name="description" content="{html.escape(description, quote=True)}">
      <meta name="robots" content="{robots}">
      <meta name="theme-color" content="#071321">
      <link rel="canonical" href="{canonical}">
      <link rel="preload" href="/{image}" as="image" fetchpriority="high">
      <link rel="icon" href="/hekman-logo.jpg" type="image/jpeg">
      <link rel="apple-touch-icon" href="/hekman-logo.jpg">
      <meta property="og:type" content="{'article' if path in PROJECT_DETAILS else 'website'}">
      <meta property="og:locale" content="en_CA">
      <meta property="og:site_name" content="Hekman Home Services Inc.">
      <meta property="og:title" content="{title}">
      <meta property="og:description" content="{html.escape(description, quote=True)}">
      <meta property="og:url" content="{canonical}">
      <meta property="og:image" content="{BASE_URL}/{image}">
      <meta property="og:image:alt" content="{html.escape(social_image_alt, quote=True)}">
      <meta name="twitter:card" content="summary_large_image">
      <meta name="twitter:title" content="{title}">
      <meta name="twitter:description" content="{html.escape(description, quote=True)}">
      <meta name="twitter:image" content="{BASE_URL}/{image}">
      <meta name="twitter:image:alt" content="{html.escape(social_image_alt, quote=True)}">
      <link rel="stylesheet" href="/styles.css?v={ASSET_VERSION}">
      <link id="mobile-layout-fixes" rel="stylesheet" href="/mobile-fixes.css?v={ASSET_VERSION}">
      {structured_data}
    </head>
    """
def header(current: str) -> str:
    def nav_item(key: str, href: str, label: str) -> str:
        current_attr = ' aria-current="page"' if key == current else ""
        return f'<a href="{href}"{current_attr}>{label}</a>'
    return f"""
    <a class="skip-link" href="#main">Skip to content</a>
    <div class="utility-bar">
      <div class="utility-inner">
        <span>Based in Westmount · Serving London &amp; St. Thomas</span>
        <span><a href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a><i aria-hidden="true"></i><a href="mailto:{EMAIL}">{EMAIL}</a></span>
      </div>
    </div>
    <header class="site-header" data-site-header>
      <div class="nav-shell">
        <a class="brand" href="/" aria-label="Hekman Home Services Inc. home">
          <img class="brand-logo" src="/hekman-logo.jpg" alt="" width="64" height="64" decoding="async">
          <span><strong>Hekman Home Services Inc.</strong><small>Renovations · Repairs · Property Improvements</small></span>
        </a>
        <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="primary-nav">
          <span class="nav-toggle-label">Menu</span><span class="nav-toggle-icon" aria-hidden="true"></span>
        </button>
        <nav class="primary-nav" id="primary-nav" aria-label="Main navigation">
          {nav_item("services", "/services/", "Services")}
          {nav_item("projects", "/projects/", "Our Work")}
          {nav_item("about", "/about/", "About")}
          {nav_item("contact", "/contact/", "Contact")}
          <a class="nav-cta" href="/contact/#quote">Request a quote</a>
        </nav>
      </div>
    </header>
    """
def footer() -> str:
    return f"""
    <footer class="site-footer">
      <div class="wrap footer-grid">
        <div class="footer-brand">
          <a class="brand" href="/">
            <img class="brand-logo" src="/hekman-logo.jpg" alt="" width="64" height="64" loading="lazy" decoding="async">
            <span><strong>Hekman Home Services Inc.</strong><small>London, Ontario</small></span>
          </a>
          <p class="footer-location">Based in Westmount,<span> serving London, St. Thomas and nearby communities.</span></p>
          <p><a href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
          <div class="footer-social">
            <span class="footer-social-label">Connect with us</span>
            <div class="social-links">
              <a class="social-icon" href="{INSTAGRAM}" rel="me noopener noreferrer" target="_blank" aria-label="Visit Hekman Home Services on Instagram">
                <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect x="3" y="3" width="18" height="18" rx="5"></rect><circle cx="12" cy="12" r="4"></circle><circle cx="17.5" cy="6.5" r="1" class="social-icon-dot"></circle></svg>
              </a>
              <a class="social-icon" href="{FACEBOOK}" rel="me noopener noreferrer" target="_blank" aria-label="Visit Hekman Home Services on Facebook">
                <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path></svg>
              </a>
            </div>
          </div>
        </div>
        <div><h2>Explore</h2><ul><li><a href="/services/">Services</a></li><li><a href="/projects/">Our Work</a></li><li><a href="/about/">About</a></li><li><a href="/contact/">Contact</a></li></ul></div>
        <div><h2>Popular services</h2><ul><li><a href="/services/bathrooms/">Bathrooms</a></li><li><a href="/services/kitchens/">Kitchens</a></li><li><a href="/services/basements/">Basements</a></li><li><a href="/services/decks-exterior/">Decks &amp; Exterior</a></li><li><a href="/services/handyman-repairs/">Handyman &amp; Repairs</a></li><li><a href="/services/commercial/">Commercial Work</a></li></ul></div>
        <div><h2>Service area</h2><p>London, St. Thomas and nearby communities.</p></div>
      </div>
      <div class="wrap footer-fine"><span>© <span data-year></span> Hekman Home Services Inc. All rights reserved.</span><a href="/contact/">Start a project</a></div>
    </footer>
    <nav class="mobile-actions" aria-label="Quick contact">
      <a href="tel:{PHONE_LINK}"><span aria-hidden="true">☎</span> Call</a>
      <a href="/contact/#quote"><span aria-hidden="true">↗</span> Request a quote</a>
    </nav>
    <script src="/main.js?v={ASSET_VERSION}" defer></script>
    """
def page(title: str, description: str, path: str, image: str, current: str, body: str, body_class: str = "", *, indexable: bool = True, image_alt: str | None = None) -> str:
    body = polish_editorial_markup(body)
    return f"""<!doctype html>
    <html lang="en">
    {head(title, description, path, image, indexable=indexable, image_alt=image_alt)}
    <body class="{body_class}">
      {header(current)}
      {body}
      {footer()}
    </body>
    </html>"""
def polish_editorial_markup(markup: str) -> str:
    """Apply sitewide label rules after the substantive page copy is written."""
    markup = re.sub(r"(<h[1-6]\b[^>]*>)(.*?)(\.)(</h[1-6]>)", r"\1\2\4", markup, flags=re.DOTALL)
    sentence_case_labels = {
        "Request a Quote": "Request a quote",
        "View Our Work": "View our work",
        "View All Services": "View all services",
        "View More Projects": "View more projects",
        "Explore More Real Projects": "Explore more real projects",
        "Tell Us About Your Project": "Tell us about your project",
        "Tell Us About It": "Tell us about it",
        "See Completed Work": "See completed work",
        "Return Home": "Return home",
        "Explore Services": "Explore services",
        "Prepare Quote Email": "Prepare quote email",
        "Start the Conversation": "Start the conversation",
    }
    for old, new in sentence_case_labels.items():
        markup = markup.replace(old, new)
    return markup
def hero(image: str, alt: str, eyebrow: str, heading: str, lead: str, *, small: bool = False, position: str = "50% 50%", secondary: tuple[str, str] | None = None) -> str:
    size_class = " page-hero" if small else ""
    secondary_link = f'<a class="button button-ghost" href="{secondary[0]}">{secondary[1]}</a>' if secondary else ""
    return f"""
    <section class="hero{size_class}">
      <img class="hero-media" src="/{image}" alt="{html.escape(alt, quote=True)}" fetchpriority="high" decoding="async" style="object-position:{position}">
      <div class="hero-shade"></div>
      <div class="wrap hero-content">
        <p class="eyebrow">{eyebrow}</p>
        <h1>{heading}</h1>
        <p class="hero-lead">{lead}</p>
        <div class="button-row"><a class="button button-primary" href="/contact/#quote">Request a Quote</a>{secondary_link}<a class="text-call" href="tel:{PHONE_LINK}">Call {PHONE_DISPLAY}</a></div>
      </div>
    </section>
    """
def project_story_hero(image: str, alt: str, eyebrow: str, heading: str, lead: str) -> str:
    return f"""
    <section class="project-story-hero">
      <div class="wrap project-story-hero-grid">
        <div class="project-story-hero-copy">
          <p class="eyebrow">{eyebrow}</p>
          <h1>{heading}</h1>
          <p>{lead}</p>
          <div class="button-row"><a class="button button-primary" href="/contact/#quote">Request a quote</a><a class="text-call" href="tel:{PHONE_LINK}">Call {PHONE_DISPLAY}</a></div>
        </div>
        <figure class="project-story-hero-media"><img src="/{image}" alt="{html.escape(alt, quote=True)}" fetchpriority="high" decoding="async"></figure>
      </div>
    </section>
    """
def section_heading(eyebrow: str, title: str, text: str) -> str:
    return f"""
    <div class="section-heading reveal">
      <div><p class="eyebrow">{eyebrow}</p><h2>{title}</h2></div>
      <p>{text}</p>
    </div>
    """
def breadcrumbs(current_label: str) -> str:
    return f"""
    <nav class="breadcrumbs wrap" aria-label="Breadcrumb">
      <ol><li><a href="/">Home</a></li><li><a href="/projects/">Our Work</a></li><li aria-current="page">{html.escape(current_label)}</li></ol>
    </nav>
    """
def project_spotlight(slug: str) -> str:
    spotlights = {
        "flooring": (
            "Medway project proof",
            "Flooring that connects with better storage",
            "Carpet came out of three rooms before cool gray-brown plank flooring, new doors, casing and baseboards connected the upper level. The project also added and enlarged closets for better everyday use.",
            "medway-floor-door-transition.jpg",
            "Completed Medway doorway, plank flooring and transition detail",
            "/projects/medway-flooring-storage/",
            "See the Medway flooring and storage story",
        ),
        "structural-layout": (
            "Melrose-area project proof",
            "A bathroom moved through the wall so the lower level could work better",
            "Reworking the footprint created a more useful bathroom, made room for a dedicated utility space and supported a newly finished exercise room beside it.",
            "melrose-wall-hung-toilet-progress.jpg",
            "Wall-hung toilet installed during the Melrose-area bathroom layout change",
            "/projects/melrose-bathroom-layout/",
            "See the Melrose layout story",
        ),
        "handyman-repairs": (
            "Repeat Westmount customer",
            "One porch project within a longer local relationship",
            "This exterior refresh was completed for a Westmount neighbour who has also trusted Hekman Home Services with several handyman projects over time.",
            "westmount-porch-after-day.jpg",
            "Finished Westmount porch and entry in daylight",
            "/projects/westmount-porch-entry/",
            "See the Westmount porch and entry",
        ),
        "decks-exterior": (
            "Multi-unit exterior proof",
            "A connected deck renewal, documented from weathered wood to finished row",
            "The repeated rear decks were treated as one coordinated exterior scope. The story follows the existing condition, open construction work and the completed deck and guard surfaces.",
            "project-104.jpg",
            "Completed row of renewed rear decks at an anonymous multi-unit property",
            "/projects/multi-unit-deck-renewal/",
            "See the multi-unit deck renewal",
        ),
        "basements": (
            "Pond Mills project proof",
            "A repair list that became a connected plan",
            "A closer inspection connected interior flooring work with several moisture-related concerns. The documented floor sequence shows the same rooms from removal and preparation to their completed finish.",
            "pond-mills-basement-floor-after.jpg",
            "Completed light plank flooring and baseboards in a Pond Mills lower-level room",
            "/projects/pond-mills-home-repairs/",
            "See the Pond Mills repair story",
        ),
        "kitchens": (
            "Hyde Park project proof",
            "A kitchen renewed by keeping what still worked",
            "Refaced cabinetry, a new pantry and a better appliance arrangement changed the room without requiring a full tear-out. New counters, sink, dishwasher and backsplash completed the update.",
            "hyde-park-kitchen-after.jpg",
            "Completed Hyde Park kitchen with refaced cabinetry, counters, sink and backsplash",
            "/projects/hyde-park-kitchen-renewal/",
            "See the Hyde Park kitchen story",
        ),
        "bathrooms": (
            "Melrose-area project proof",
            "A bathroom reworked from the layout out",
            "The room moved to the other side of an existing wall, then came together with a tiled shower, wall-hung toilet, vanity, lighting and careful finish work.",
            "melrose-bathroom-after.jpg",
            "Completed Melrose-area bathroom with tiled shower, wall-hung toilet and vanity",
            "/projects/melrose-bathroom-layout/",
            "See the completed Melrose bathroom",
        ),
        "drywall-ceiling-repair": (
            "Melrose-area finish work",
            "A new exercise room finished from ceiling to floor",
            "Drywall, ceiling work and paint turned the adjacent lower-level room into a clean exercise space while the bathroom and new utility room were completed nearby.",
            "melrose-exercise-room-after.jpg",
            "Completed Melrose-area exercise room with smooth ceiling and painted walls",
            "/projects/melrose-bathroom-layout/",
            "See the connected Melrose spaces",
        ),
        "water-damage": (
            "Blackfriars restoration",
            "A small leak revealed a much larger problem",
            "Opening the affected area exposed mold, evidence of mice, structural concerns and knob-and-tube wiring. Hekman coordinated the appropriate team and trades before restoring the room.",
            "blackfriars-investigation.jpg",
            "Ceiling opened during investigation of a leak in a Blackfriars home",
            "/projects/blackfriars-leak-restoration/",
            "See the Blackfriars restoration story",
        ),
    }
    details = spotlights.get(slug)
    if not details:
        return ""
    eyebrow, title, text, image, alt, link, link_label = details
    return f"""
      <section class="section section-stone project-spotlight"><div class="wrap editorial-grid">
        <div class="editorial-media reveal"><img src="/{image}" alt="{html.escape(alt, quote=True)}" loading="lazy" decoding="async"><span>Genuine local project</span></div>
        <div class="editorial-copy reveal"><p class="eyebrow">{eyebrow}</p><h2>{title}</h2><p>{text}</p><a class="text-link dark-link" href="{link}">{link_label} <span aria-hidden="true">↗</span></a></div>
      </div></section>
    """
def service_url(slug: str) -> str:
    return f"/services/{slug}/"
def service_card(slug: str, *, compact: bool = False, variant: int = 0) -> str:
    item = SERVICES[slug]
    choices = SERVICE_CARD_VARIANTS.get(slug, [(item["hero"], item["hero_alt"])])
    image, image_alt = choices[variant % len(choices)]
    class_name = "service-card compact" if compact else "service-card"
    return f"""
    <a class="{class_name} reveal" href="{service_url(slug)}">
      <img src="/{image}" alt="{html.escape(image_alt, quote=True)}" loading="lazy" decoding="async">
      <span class="service-card-shade"></span>
      <span class="service-card-body"><strong>{item['card_name']}</strong><span>{item['lead']}</span><b>Explore service <i aria-hidden="true">↗</i></b></span>
    </a>
    """
def homepage() -> str:
    featured_slugs = (
        "bathrooms",
        "kitchens",
        "handyman-repairs",
        "drywall-ceiling-repair",
        "popcorn-ceiling-removal",
        "water-damage",
    )
    featured = "".join(service_card(slug) for slug in featured_slugs)
    local_proof = f"""
      <section class="section section-stone local-proof-section">
        <div class="wrap">
          {section_heading("Recent work across London", "Finished results, backed by the story behind them", "A Medway upper level, a Westmount porch and a reworked Melrose-area bathroom—three different projects with a clear challenge, documented work and a finished result.")}
          <div class="story-card-grid local-proof-grid">
            <a class="story-card story-card-large reveal" href="/projects/medway-flooring-storage/"><img src="/medway-finished-room.jpg" alt="Completed Medway room with cool gray-brown plank flooring and finished baseboards" loading="lazy"><span><small>Medway · completed upper level</small><strong>More storage. Better flow. One seamless finish</strong><b>Three rooms, relocated closets, plank flooring, doors and trim <i aria-hidden="true">↗</i></b></span></a>
            <a class="story-card reveal" href="/projects/westmount-porch-entry/"><img src="/westmount-porch-after-night.jpg" alt="Finished Westmount porch and entry illuminated at night" loading="lazy"><span><small>Westmount · completed porch and entry</small><strong>A more modern welcome, built for a neighbour</strong><b>Exterior repairs, cleaner lines, finish work and lighting <i aria-hidden="true">↗</i></b></span></a>
            <a class="story-card reveal" href="/projects/melrose-bathroom-layout/"><img src="/melrose-bathroom-after.jpg" alt="Completed Melrose-area bathroom with tiled shower, wall-hung toilet and illuminated mirror" loading="lazy"><span><small>Melrose area · finished bathroom</small><strong>A new layout for three connected spaces</strong><b>Moved bathroom, dedicated utility room and a finished exercise space <i aria-hidden="true">↗</i></b></span></a>
          </div>
          <div class="testimonial-grid" aria-label="Homeowner feedback connected to documented projects">
            <blockquote class="testimonial-card reveal"><p>“This team is amazing—so meticulous and detail-oriented. Love their work.”</p><footer><strong>Medway homeowner</strong><span>Flooring &amp; storage transformation</span><a href="/projects/medway-flooring-storage/">See the documented work <i aria-hidden="true">↗</i></a></footer></blockquote>
            <blockquote class="testimonial-card reveal"><p>“Efficient, professional and fantastic work. Rene modernized the front of our home, and I would recommend him for home repair and remodelling.”</p><footer><strong>Repeat Westmount homeowner</strong><span>Porch &amp; entry revitalization</span><a href="/projects/westmount-porch-entry/">See the documented work <i aria-hidden="true">↗</i></a></footer></blockquote>
          </div>
          <div class="section-actions reveal"><a class="button button-dark" href="/projects/">Explore More Real Projects</a></div>
        </div>
      </section>
    """
    body = f"""
    {hero("hilltop-kitchen-wide.jpg", "Completed Hilltop kitchen renovation by Hekman Home Services", "Renovations, repairs & restoration · London, Ontario", "Repairs that feel resolved. Renovations that belong", "We address what caused the problem, complete the connected work and finish the details so the result fits your home.", secondary=("/projects/", "View our work"), position="50% 54%")}
    <main id="main">
      <section class="trust-band" aria-label="Business assurances">
        <div class="wrap trust-grid">
          <div><strong>Fully insured &amp; bondable</strong><small>Professional protection for your project</small></div>
          <div><strong>25 years in construction</strong><small>Rene’s hands-on renovation and repair experience</small></div>
          <div><strong>Family-run &amp; local</strong><small>Led directly by Rene and Steph Hekman</small></div>
          <div><strong>Defined project scope</strong><small>Understand the work before it begins</small></div>
        </div>
      </section>
      {local_proof}
      <section class="section section-paper">
        <div class="wrap">
          {section_heading("Renovation and repair services · London, Ontario", "Six core services, backed by a much broader skill set", "These are the services homeowners ask for most often and the work we can show through genuine projects. Our complete service list covers additional repairs, renovations and exterior work.")}
          <div class="service-grid">{featured}</div>
          <div class="section-actions reveal"><a class="button button-dark" href="/services/">View All Services</a></div>
        </div>
      </section>
      <section class="section section-charcoal">
        <div class="wrap editorial-grid">
          <div class="editorial-media reveal"><img src="/bathroom-walnut-vanity-after.jpg" alt="Completed tub-to-shower bathroom conversion with glass enclosure" loading="lazy" decoding="async"><span>Genuine completed work</span></div>
          <div class="editorial-copy reveal"><p class="eyebrow">The Hekman Promise</p><h2>Straight answers. Respectful work. No surprise invoices.</h2><p>Our written promise sets a practical standard for every project: honest advice, transparent pricing, an organized job site and direct communication from start to finish.</p><ul class="line-list"><li><strong>Your home is treated with respect</strong><span>Protection, cleanup and attention to detail are part of the work.</span></li><li><strong>Extras require your approval</strong><span>If the scope needs to change, we discuss it before proceeding.</span></li><li><strong>Workmanship is guaranteed for two years</strong><span>Installation-related defects resulting from our workmanship are covered.</span></li></ul><a class="text-link" href="/about/#hekman-promise">Read the full Hekman Promise <span aria-hidden="true">↗</span></a></div>
        </div>
      </section>
      <section class="section section-charcoal">
        <div class="wrap">
          {section_heading("Our process", "A straightforward path from first look to final review", "Every home is different, but a defined process makes decisions easier and keeps the project moving.")}
          <ol class="process-grid">
            <li class="reveal"><span>01</span><h3>Walk through</h3><p>Show us the space, the problem and what you want it to become.</p></li>
            <li class="reveal"><span>02</span><h3>Define the scope</h3><p>We review the connected work, assumptions and project details.</p></li>
            <li class="reveal"><span>03</span><h3>Prepare &amp; build</h3><p>Your home is protected while the agreed work is completed.</p></li>
            <li class="reveal"><span>04</span><h3>Finish &amp; review</h3><p>Final details, touch-ups and cleanup bring the project together.</p></li>
          </ol>
        </div>
      </section>
      <section class="section section-paper">
        <div class="wrap area-layout">
          <div class="reveal"><p class="eyebrow">Service area</p><h2>Based in Westmount. Serving London &amp; St. Thomas.</h2><p><strong>Based in Westmount and working across London, we serve the city from north to south and east to west.</strong> That includes Byron, Hyde Park, Old North, Sunningdale and Stoneybrook. We also take on projects in St. Thomas and nearby communities.</p></div>
          <div class="photo-stack reveal"><img src="/project-070.jpg" alt="Hekman Home Services team" loading="lazy"><div class="photo-note"><strong>Hands-on, local service</strong><span>Respect for your home and direct updates as the work moves forward.</span></div></div>
        </div>
      </section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">Picture what could work better?</p><h2>Start with the room—or repair—you keep thinking about.</h2><p>Send a few photos—no detailed plans required. A short note about the room, repair or result you have in mind is enough to begin.</p></div><div><a class="button button-primary" href="/contact/#quote">Tell Us About Your Project</a><a class="cta-phone" href="tel:{PHONE_LINK}">Call or text {PHONE_DISPLAY}</a></div></div></section>
    </main>
    """
    return page("Renovations & Repairs London ON | Hekman", "Based in Westmount, Hekman Home Services provides thoughtful renovations, flooring, drywall, handyman work and restorative repairs throughout London, St. Thomas and nearby communities.", "/", "hilltop-kitchen-wide.jpg", "home", body, "home", image_alt="Completed Hilltop kitchen renovation by Hekman Home Services")
def services_page() -> str:
    cards = "".join(service_card(slug, compact=True, variant=1) for slug in SERVICE_DISPLAY_ORDER)
    body = f"""
    {hero("project-129.jpg", "Completed kitchen renovation", "Renovation & repair services", "One clear scope for the work your property needs.", "Renovations, repairs and property improvements are planned together—from the first visible problem to the details that make the completed result hold together.", small=True, secondary=("/projects/", "See Completed Work"), position="50% 58%")}
    <main id="main">
      <section class="section section-paper"><div class="wrap">{section_heading("Explore services", "From one repair to a complete transformation.", "Some projects fit one category. Others connect several. Explore the main services below, or send the whole scope and we will review it together.")}<div class="service-grid service-grid-compact">{cards}</div></div></section>
      <section class="section section-charcoal"><div class="wrap editorial-grid reverse"><div class="editorial-media reveal"><img src="/project-011.jpg" alt="Drywall preparation and finishing in progress" loading="lazy"><span>The work behind the finish</span></div><div class="editorial-copy reveal"><p class="eyebrow">Not sure where it fits?</p><h2>Describe the complete project.</h2><p>Send a few photos—no detailed plans required. Tell us what you want to change or repair, and we will help connect the scope.</p><a class="button button-primary" href="/contact/#quote">Tell Us About It</a></div></div></section>
    </main>"""
    return page("Renovation & Handyman Services London ON | Hekman", "Explore renovations, flooring, drywall, painting, pot lights, plumbing fixtures, handyman repairs, decks, fences and commercial maintenance in London, Ontario.", "/services/", "project-129.jpg", "services", body, image_alt="Completed London kitchen renovation with an island and pendant lighting")
def bathroom_showcase() -> str:
    return f"""
    <section class="section section-paper bathroom-showcase">
      <div class="wrap">
        {section_heading("Bathroom project spotlight", "A jetted-tub platform became a bright glass shower.", "This is one continuous project sequence: the original room, demolition, the opened wall and floor, and the completed conversion.")}
        <article class="case-study reveal">
          <div class="case-study-copy">
            <p class="eyebrow">Tub-to-shower conversion</p>
            <h3>The glass-block window stayed. The room around it changed.</h3>
            <p>The original jetted tub and tiled platform were removed to open the footprint for a shower. With the wall and floor exposed, the underlying conditions could be addressed before the enclosure, tile and finish details went in.</p>
            <ul>
              <li>Jetted tub and platform removal</li>
              <li>Wall, insulation and floor access</li>
              <li>Shower preparation and tile</li>
              <li>Sliding glass enclosure and finish work</li>
            </ul>
            <a class="text-link dark-link" href="/projects/glass-block-bathroom-conversion/">See the full bathroom sequence and videos <span aria-hidden="true">↗</span></a>
          </div>
          <div class="case-study-media case-study-media-four">
            <figure><img src="/bathroom-glass-block-before.jpg" alt="Jetted-tub bathroom before conversion" loading="lazy"><figcaption>Before</figcaption></figure>
            <figure><img src="/bathroom-glass-block-demolition.jpg" alt="Tub platform partly removed during demolition" loading="lazy"><figcaption>Demolition</figcaption></figure>
            <figure><img src="/bathroom-glass-block-open-wall.jpg" alt="Bathroom wall, insulation and floor framing exposed after tub removal" loading="lazy"><figcaption>Opened wall and floor</figcaption></figure>
            <figure><img src="/bathroom-walnut-vanity-after.jpg" alt="Completed glass shower conversion with walnut vanity" loading="lazy"><figcaption>Completed conversion</figcaption></figure>
          </div>
        </article>
        <article class="case-study case-study-compact reveal" id="hilltop-bathrooms">
          <div class="case-study-copy">
            <p class="eyebrow">Two Hilltop bathrooms</p>
            <h3>Different rooms. Different starting points. One carefully finished home.</h3>
            <p>The upstairs bathroom is recognizable by its sloped ceiling and ornate mirror: an original green-tile tub surround gave way to a bright marble-look finish. Downstairs, an older shower and drop ceiling were rebuilt with white subway tile, restrained gray accents, a glass enclosure and a clean new vanity.</p>
            <ul>
              <li>Existing-room documentation before demolition</li>
              <li>Shower and tub-surround rebuilding</li>
              <li>Ceiling, wall, floor and vanity finishing</li>
              <li>Consistent details across the wider Hilltop renovation</li>
            </ul>
            <a class="text-link dark-link" href="/projects/hilltop-home-transformation/#hilltop-bathrooms">See both Hilltop bathroom stories <span aria-hidden="true">↗</span></a>
          </div>
          <div class="case-study-media case-study-media-five">
            <figure><img src="/hilltop-green-tile-before.jpg" alt="Hilltop bathroom before renovation with green tile around the tub" loading="lazy"><figcaption>Upstairs before</figcaption></figure>
            <figure><img src="/hilltop-green-tile-after.jpg" alt="Hilltop bathroom after renovation with marble-look tub-surround tile" loading="lazy"><figcaption>Upstairs after</figcaption></figure>
            <figure><img src="/hilltop-basement-bathroom-before.jpg" alt="Hilltop basement bathroom before renovation with an older shower and drop ceiling" loading="lazy"><figcaption>Basement before</figcaption></figure>
            <figure><img src="/hilltop-basement-bathroom-during.jpg" alt="Hilltop basement bathroom during tile, wall and floor work" loading="lazy"><figcaption>Basement during</figcaption></figure>
            <figure><img src="/hilltop-basement-bathroom-wide.jpg" alt="Completed Hilltop basement bathroom with white vanity and glass shower" loading="lazy"><figcaption>Basement after</figcaption></figure>
          </div>
        </article>
        <article class="case-study case-study-compact reveal" id="frosted-window-repair">
          <div class="case-study-copy">
            <p class="eyebrow">The work behind the finish</p>
            <h3>The same frosted window marks every stage of this bathroom repair.</h3>
            <p>The original wall tile was removed while the black-framed shower remained in place. Opening the room exposed the wall cavity, insulation and plumbing access; new wall board and compound then rebuilt the surfaces around the unchanged window and shower.</p>
            <p class="case-note">The fixed window, shower frame and room proportions trace the repair clearly from one stage to the next.</p>
          </div>
          <div class="case-study-media case-study-media-four">
            <figure><img src="/project-155.jpg" alt="Frosted-window bathroom before wall and floor repair" loading="lazy"><figcaption>Existing room</figcaption></figure>
            <figure><img src="/project-146.jpg" alt="Wall tile being removed in the frosted-window bathroom" loading="lazy"><figcaption>Tile removal</figcaption></figure>
            <figure><img src="/project-153.jpg" alt="Exterior wall opened to insulation beneath the bathroom window" loading="lazy"><figcaption>Wall and insulation</figcaption></figure>
            <figure><img src="/project-152.jpg" alt="New wall board and compound around the same frosted bathroom window" loading="lazy"><figcaption>Wall rebuilding</figcaption></figure>
          </div>
        </article>
      </div>
    </section>
    """
def commercial_showcase() -> str:
    return f"""
    <section class="section section-paper commercial-showcase" id="commercial-salon">
      <div class="wrap">
        {section_heading("Commercial work in context", "Different businesses. Different problems. The same practical approach.", "A salon recovering from water damage, a fitness facility replacing outdated lighting and an office kitchen that needed to work better—each project was shaped around the business using the space.")}
        <article class="case-study reveal">
          <div class="case-study-copy">
            <p class="eyebrow">Restoration · working salon</p>
            <h3>Water damage does not care that a business needs to stay open.</h3>
            <p>This London salon needed restorative work after a water leak. The goal was not to redesign its identity; it was to complete the necessary construction repairs and return the working space to the bright, polished setting its clients already knew.</p>
            <ul>
              <li>Commercial water-damage restoration</li>
              <li>Repair work planned around an active business</li>
              <li>Walls, ceilings and connected finish work</li>
              <li>A clean, functional space ready for clients again</li>
            </ul>
            <a class="text-link dark-link" href="/projects/commercial-salon-repair/">Read the full salon project story <span aria-hidden="true">↗</span></a>
          </div>
          <div class="case-study-media case-study-media-three">
            <figure><img src="/salon-restored-wall.jpg" alt="Completed wall repair in an anonymous London salon" loading="lazy"><figcaption>Completed wall restoration</figcaption></figure>
            <figure><img src="/salon-moisture-investigation.jpg" alt="Moisture meter documenting an affected trim area in an anonymous London salon" loading="lazy"><figcaption>Moisture investigation</figcaption></figure>
            <figure><img src="/salon-wall-ceiling-rebuild.jpg" alt="Wall and ceiling surfaces being rebuilt in an anonymous London salon" loading="lazy"><figcaption>Wall and ceiling rebuilding</figcaption></figure>
          </div>
        </article>
        <article class="case-study case-study-compact reveal">
          <div class="case-study-copy">
            <p class="eyebrow">Fitness facility · LED upgrade</p>
            <h3>Better light for a space built around movement.</h3>
            <p>Older box-style fluorescent fixtures were replaced with streamlined LED lighting. The before, installation and completed views below follow one facility and one clear improvement—better, more consistent light across the gym floor.</p>
          </div>
          <div class="case-study-media case-study-media-three">
            <figure><img src="/project-045.jpg" alt="Older box-style fluorescent fixtures before the fitness-space lighting upgrade" loading="lazy"><figcaption>Before: older fixtures</figcaption></figure>
            <figure><img src="/project-049.jpg" alt="Crew replacing fitness-space lighting from scaffolding and ladders" loading="lazy"><figcaption>During: fixture replacement</figcaption></figure>
            <figure><img src="/project-048.jpg" alt="Fitness facility after the completed LED lighting upgrade" loading="lazy"><figcaption>After: LED lighting installed</figcaption></figure>
          </div>
        </article>
        <article class="case-study case-study-compact reveal">
          <div class="case-study-copy">
            <p class="eyebrow">Office kitchen · London</p>
            <h3>A dated staff kitchen, rebuilt into a clean working space</h3>
            <p>The original cabinetry and counter were removed, the wall was opened for plumbing and repair access, and new cabinets, counter, sink, hardware and finish work were brought together in the same compact footprint.</p>
            <a class="text-link dark-link" href="/projects/kitchen-renewal/">See the office-kitchen sequence <span aria-hidden="true">↗</span></a>
          </div>
          <div class="case-study-media case-study-media-three">
            <figure><img src="/kitchenette-before-wide.jpg" alt="Dated office kitchen before renovation" loading="lazy"><figcaption>Before</figcaption></figure>
            <figure><img src="/kitchenette-wall-plumbing-stage.jpg" alt="Office kitchen wall opened for plumbing and repair access" loading="lazy"><figcaption>Wall and plumbing access</figcaption></figure>
            <figure><img src="/kitchenette-after-wide.jpg" alt="Completed office kitchen with new cabinets, counter and sink" loading="lazy"><figcaption>Completed office kitchen</figcaption></figure>
          </div>
        </article>
      </div>
    </section>
    """
def service_page(slug: str) -> str:
    item = SERVICES[slug]
    planning_eyebrow = item.get("planning_eyebrow", "Thoughtful project planning")
    planning_title = item.get("planning_title", "Built around what the space needs.")
    scope_title = item.get("scope_title", "A complete scope, not disconnected pieces.")
    scope_text = item.get("scope_text", "The exact work depends on existing conditions, selected materials and the result you want.")
    scope = "".join(f'<article class="proof-card reveal"><h3>{title}</h3><p>{text}</p></article>' for title, text in item["scope"])
    bullets = "".join(f"<li>{bullet}</li>" for bullet in item["bullets"])
    gallery = "".join(f'<figure class="reveal"><img src="/{src}" alt="{html.escape(alt, quote=True)}" loading="lazy" decoding="async"><figcaption>{caption}</figcaption></figure>' for src, alt, caption in item["gallery"])
    faqs = "".join(f'<details class="reveal"><summary>{question}</summary><p>{answer}</p></details>' for question, answer in item["faq"])
    related = "".join(
        service_card(related_slug, compact=True, variant=variant)
        for variant, related_slug in enumerate(item["related"], 2)
    )
    spotlight = project_spotlight(slug)
    showcase = bathroom_showcase() if slug == "bathrooms" else commercial_showcase() if slug == "commercial" else ""
    if slug == "commercial":
        gallery_section = ""
    elif slug == "water-damage":
        gallery_section = f"""
      <section class="section section-stone"><div class="wrap">{section_heading("Restoration in practice", "Different damage. One goal: make the space feel whole again.", "A damaged ceiling, an opened wall, a disrupted business or an unfinished surface can each require a different repair plan. These are individual moments from separate restoration projects.")}<div class="gallery-grid">{gallery}</div><div class="section-actions reveal"><a class="button button-dark" href="/projects/">View More Projects</a></div></div></section>
    """
    else:
        gallery_section = f"""
      <section class="section section-stone"><div class="wrap">{section_heading("Details from real projects", "See what careful work looks like.", "Preparation, progress and finished spaces from Hekman Home Services work in London and nearby communities.")}<div class="gallery-grid">{gallery}</div><div class="section-actions reveal"><a class="button button-dark" href="/projects/">View More Projects</a></div></div></section>
    """
    body = f"""
    {hero(item['hero'], item['hero_alt'], "London, Ontario", item['name'], item['lead'], small=True, position=item['position'])}
    <main id="main">
      <section class="section section-paper"><div class="wrap service-intro"><div class="reveal"><p class="eyebrow">{planning_eyebrow}</p><h2>{planning_title}</h2><p>{item['intro']}</p><a class="text-link dark-link" href="/contact/#quote">Discuss your project <span aria-hidden="true">↗</span></a></div><ul class="scope-list reveal">{bullets}</ul></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("What the work can include", scope_title, scope_text)}<div class="proof-grid">{scope}</div></div></section>
      {showcase}
      {gallery_section}
      {spotlight}
      <section class="section section-paper"><div class="wrap faq-layout"><div class="reveal"><p class="eyebrow">Common questions</p><h2>Helpful before the walkthrough.</h2><p>The final scope depends on your property, materials and existing conditions.</p></div><div class="faq-list">{faqs}</div></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("Related services", "The connected work matters too.", "Many renovations involve more than one surface or room. These services are often part of the same conversation.")}<div class="service-grid related-grid">{related}</div></div></section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">Thinking about this project?</p><h2>Show us what you’re working with.</h2><p>You do not need a finished design or every decision made. A few photos and a clear description are enough to begin.</p></div><div><a class="button button-primary" href="/contact/#quote">Tell Us About Your Project</a><a class="cta-phone" href="tel:{PHONE_LINK}">Call or text {PHONE_DISPLAY}</a></div></div></section>
    </main>"""
    return page(item["title"], item["description"], service_url(slug), item["hero"], "services", body, "service-page", image_alt=item["hero_alt"])
def melrose_project_page() -> str:
    project_name = "Melrose: A Bathroom Reworked From the Layout Out"
    body = f"""
    {project_story_hero("melrose-bathroom-after.jpg", "Completed Melrose-area bathroom with a wall-hung toilet, tiled shower, vanity and illuminated mirror", "Melrose area · London, Ontario", project_name, "Moving the bathroom to the other side of an existing wall created a better lower-level plan—with a new utility room and a finished exercise space beside it.")}
    <main id="main">
      {breadcrumbs(project_name)}
      <section class="section section-paper"><div class="wrap service-intro story-summary"><div class="reveal"><p class="eyebrow">Multi-space renovation · completed</p><h2>The best answer was not inside the old footprint</h2><p>The original bathroom location limited how the lower level could work. Rather than force new finishes into the same arrangement, the plan moved the bathroom through the wall and reconsidered the surrounding rooms at the same time.</p><p>The new bathroom brings together a tiled shower, wall-hung toilet, vanity, lighting and precise finish work. The reworked footprint also created a dedicated utility room, while drywall, ceiling work and paint turned the adjacent space into a clean exercise room.</p></div><ul class="scope-list reveal"><li>Bathroom moved to the other side of an existing wall</li><li>Tiled shower and wall-hung toilet</li><li>Vanity, mirror lighting and finish work</li><li>New dedicated utility room</li><li>Drywall and ceiling finishing</li><li>Painted exercise room</li></ul></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("The bathroom", "Layout first, then every visible detail", "Progress photographs show the wall-hung toilet and shower tile taking shape before the vanity, lighting, glass and final finishes brought the room together.")}<div class="story-mosaic story-mosaic-melrose">
        <figure class="story-feature"><img src="/melrose-bathroom-after.jpg" alt="Completed Melrose-area bathroom with vanity, illuminated mirror and tiled shower" loading="lazy"><figcaption>Completed bathroom</figcaption></figure>
        <figure><img src="/melrose-wall-hung-toilet-progress.jpg" alt="Wall-hung toilet installed during the Melrose-area bathroom renovation" loading="lazy"><figcaption>Layout and fixture progress</figcaption></figure>
        <figure><img src="/melrose-shower-tile-progress.jpg" alt="Dark wall tile being installed in the Melrose-area shower" loading="lazy"><figcaption>Shower tile in progress</figcaption></figure>
        <figure class="story-wide"><img src="/melrose-shower-toilet-detail.jpg" alt="Completed Melrose-area tiled shower and wall-hung toilet" loading="lazy"><figcaption>Completed shower and toilet detail</figcaption></figure>
      </div></div></section>
      <section class="section section-stone"><div class="wrap editorial-grid reverse"><div class="editorial-media reveal"><img src="/melrose-exercise-room-after.jpg" alt="Completed Melrose-area exercise room with smooth ceiling and painted walls" loading="lazy"><span>A connected room, fully finished</span></div><div class="editorial-copy reveal"><p class="eyebrow">Beyond the bathroom</p><h2>The surrounding rooms had to work too</h2><p>Layout changes rarely stop at one wall. The same plan that improved the bathroom also made space for utilities and gave the exercise room a proper finish. Drywall, ceiling work and paint were treated as part of the transformation—not as loose ends after the main room was done.</p><a class="text-link dark-link" href="/services/structural-layout/">Explore layout changes <span aria-hidden="true">↗</span></a></div></div></section>
      <section class="section section-paper"><div class="wrap">{section_heading("A closer look", "Six seconds through the finished room", "The short walkthrough is quiet by design: it waits for you to press play and shows the completed layout without interrupting the page.")}<div class="video-grid video-grid-single"><figure class="work-video reveal"><video controls playsinline preload="none" poster="/melrose-bathroom-after.jpg" aria-label="Short walkthrough of the completed Melrose-area bathroom"><source src="/melrose-bathroom-tour.mp4" type="video/mp4">Your browser does not support embedded video.</video><figcaption><strong>Finished bathroom walkthrough</strong><span>Vanity, illuminated mirror, tiled shower and wall-hung toilet in the completed room</span></figcaption></figure></div></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("Connected services", "One layout, three better spaces", "Bathroom work, drywall finishing and layout changes were planned as one connected project.")}<div class="service-grid related-grid">{service_card("bathrooms", compact=True, variant=2)}{service_card("drywall-ceiling-repair", compact=True, variant=2)}{service_card("structural-layout", compact=True, variant=2)}</div></div></section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">Is the current layout holding the room back?</p><h2>Start with how the whole space should work</h2><p>A few wide photographs and a simple sketch can help begin the conversation.</p></div><div><a class="button button-primary" href="/contact/#quote">Tell us about your project</a><a class="cta-phone" href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a></div></div></section>
    </main>"""
    return page("Melrose Bathroom & Layout Renovation | Hekman", PROJECT_DETAILS["/projects/melrose-bathroom-layout/"]["description"], "/projects/melrose-bathroom-layout/", "melrose-bathroom-after.jpg", "projects", body, "project-story-page")
def hyde_park_kitchen_project_page() -> str:
    project_name = "Hyde Park: A Kitchen Renewed Without Starting Over"
    body = f"""
    {project_story_hero("hyde-park-kitchen-after.jpg", "Completed Hyde Park kitchen with refaced cabinetry, new counters, sink and backsplash", "Hyde Park · London, Ontario", project_name, "A resourceful update kept the kitchen’s useful foundations, then improved storage, appliance flow and the surfaces the homeowners touch every day.")}
    <main id="main">
      {breadcrumbs(project_name)}
      <section class="section section-paper"><div class="wrap service-intro story-summary"><div class="reveal"><p class="eyebrow">Focused kitchen renewal · completed</p><h2>Keep the useful parts and invest where the room needs change</h2><p>The existing cabinets were refaced rather than discarded. A purpose-built pantry added storage, and the appliance arrangement was reworked to make room for a dishwasher and a more practical daily flow.</p><p>Hekman Home Services also helped source the counters and sink, then connected the new elements with backsplash tile and finish work. The homeowners told the team they were thrilled with the result.</p></div><ul class="scope-list reveal"><li>Existing cabinetry refaced</li><li>New pantry storage</li><li>Appliances reconfigured</li><li>Dishwasher added</li><li>Backsplash installed</li><li>Counters and sink sourced</li></ul></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("The finished kitchen", "A familiar room with a clearer rhythm", "The strongest photographs focus on the completed room, with supporting views of the pantry, sink and dishwasher, careful protection and backsplash installation.")}<div class="story-mosaic story-mosaic-hyde-park">
        <figure class="story-feature"><img src="/hyde-park-kitchen-after.jpg" alt="Wide view of the completed Hyde Park kitchen" loading="lazy"><figcaption>Completed kitchen</figcaption></figure>
        <figure><img src="/hyde-park-pantry-and-appliance-layout.jpg" alt="New pantry and reconfigured appliance wall in the Hyde Park kitchen" loading="lazy"><figcaption>Pantry and appliance layout</figcaption></figure>
        <figure><img src="/hyde-park-sink-and-dishwasher.jpg" alt="New sink, counter and dishwasher in the Hyde Park kitchen" loading="lazy"><figcaption>Sink, counter and dishwasher</figcaption></figure>
        <figure><img src="/hyde-park-kitchen-preparation.jpg" alt="Hyde Park kitchen protected during the update" loading="lazy"><figcaption>Room protection during the work</figcaption></figure>
        <figure class="story-wide"><img src="/hyde-park-backsplash-installation.jpg" alt="Backsplash tile being installed in the Hyde Park kitchen" loading="lazy"><figcaption>Backsplash installation</figcaption></figure>
      </div></div></section>
      <section class="section section-stone"><div class="wrap editorial-grid"><div class="editorial-media reveal"><img src="/hyde-park-pantry-and-appliance-layout.jpg" alt="Hyde Park pantry and reconfigured appliance wall" loading="lazy"><span>Storage and flow, reconsidered</span></div><div class="editorial-copy reveal"><p class="eyebrow">A project-specific budget result</p><h2>Thoughtful choices kept this update under $20,000</h2><p>This particular kitchen was completed for less than $20,000 by retaining and refacing serviceable cabinetry, focusing the layout changes and sourcing carefully. It is a result from this home—not a fixed package or a guarantee for another kitchen, where size, materials and existing conditions will differ.</p><a class="text-link dark-link" href="/services/kitchens/">Explore kitchen renovations <span aria-hidden="true">↗</span></a></div></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("Connected services", "A kitchen update is a set of linked decisions", "Cabinetry, plumbing fixtures, tile and finish work have to meet cleanly for the room to feel resolved.")}<div class="service-grid related-grid">{service_card("kitchens", compact=True, variant=2)}{service_card("handyman-repairs", compact=True, variant=3)}{service_card("flooring", compact=True, variant=2)}</div></div></section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">Wondering what is worth keeping?</p><h2>Start with the kitchen you already have</h2><p>We can review what works, what does not and where a focused investment could make the greatest difference.</p></div><div><a class="button button-primary" href="/contact/#quote">Tell us about your project</a><a class="cta-phone" href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a></div></div></section>
    </main>"""
    return page("Hyde Park Kitchen Renewal | Hekman Home Services", PROJECT_DETAILS["/projects/hyde-park-kitchen-renewal/"]["description"], "/projects/hyde-park-kitchen-renewal/", "hyde-park-kitchen-after.jpg", "projects", body, "project-story-page")
def blackfriars_project_page() -> str:
    project_name = "Blackfriars: A Small Leak That Needed a Much Bigger Plan"
    body = f"""
    {project_story_hero("blackfriars-restored-room.jpg", "Restored Blackfriars room with a smooth ceiling and painted walls", "Blackfriars · London, Ontario", project_name, "What looked like a limited leak became an investigation, a coordinated response and a careful restoration once the ceiling and wall were opened.")}
    <main id="main">
      {breadcrumbs(project_name)}
      <section class="section section-paper"><div class="wrap service-intro story-summary"><div class="reveal"><p class="eyebrow">Investigation and restoration · completed</p><h2>The first opening changed the scope</h2><p>The project began with what appeared to be a small leak. Opening the affected ceiling and wall revealed mold, evidence of mice, structural concerns and knob-and-tube wiring—conditions that needed a broader, properly coordinated response before finishes could be restored.</p><p>Hekman Home Services identified the visible concerns, protected the project sequence and coordinated the appropriate remediation team and qualified trades. Once those conditions were addressed, Hekman managed the rebuild and restored the drywall, ceiling and painted finish.</p></div><ul class="scope-list reveal"><li>Initial leak area opened and assessed</li><li>Mold and evidence of mice identified</li><li>Structural concerns documented</li><li>Knob-and-tube wiring identified</li><li>Appropriate team and trades coordinated</li><li>Room rebuilt and finishes restored</li></ul></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("From symptom to restored room", "Open carefully, understand fully, rebuild in the right order", "This sequence is deliberately concise: the first opening, the deeper investigation, a structural detail, the rebuilding stage and the finished room.")}<div class="story-mosaic story-mosaic-blackfriars">
        <figure><img src="/blackfriars-first-opening.jpg" alt="Small initial ceiling opening during the Blackfriars leak investigation" loading="lazy"><figcaption>Initial opening</figcaption></figure>
        <figure class="story-feature"><img src="/blackfriars-investigation.jpg" alt="Protected investigation work after the Blackfriars ceiling was opened further" loading="lazy"><figcaption>Deeper investigation</figcaption></figure>
        <figure><img src="/blackfriars-structural-concern.jpg" alt="Exposed framing documented during the Blackfriars investigation" loading="lazy"><figcaption>Structural condition documented</figcaption></figure>
        <figure><img src="/blackfriars-rebuild.jpg" alt="Blackfriars room during framing, insulation and rebuilding work" loading="lazy"><figcaption>Rebuilding in progress</figcaption></figure>
        <figure class="story-wide"><img src="/blackfriars-restored-room.jpg" alt="Restored Blackfriars room with smooth ceiling and painted walls" loading="lazy"><figcaption>Room restored</figcaption></figure>
      </div></div></section>
      <section class="section section-stone"><div class="wrap editorial-grid reverse"><div class="editorial-media reveal"><img src="/blackfriars-investigation.jpg" alt="Ceiling investigation underway in the protected Blackfriars room" loading="lazy"><span>Stop, identify and coordinate</span></div><div class="editorial-copy reveal"><p class="eyebrow">The responsible sequence</p><h2>Finish work had to wait until the hidden conditions were addressed</h2><p>A renovation contractor should not blur the line between construction work and regulated or specialist work. Hekman’s role was to recognize what the opening revealed, bring the right people into the project and return to the restoration only when the preceding work was ready.</p><a class="text-link dark-link" href="/services/water-damage/">Explore restorative repairs <span aria-hidden="true">↗</span></a></div></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("Connected services", "Investigation, coordination and restoration", "Unexpected conditions can connect water damage, structural review, electrical work and interior finishing in one carefully sequenced plan.")}<div class="service-grid related-grid">{service_card("water-damage", compact=True, variant=2)}{service_card("drywall-ceiling-repair", compact=True, variant=3)}{service_card("structural-layout", compact=True, variant=3)}</div></div></section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">Has a small repair started to look bigger?</p><h2>Show us what changed when the area was opened</h2><p>Photographs of the affected room and any visible conditions can help frame a responsible next step.</p></div><div><a class="button button-primary" href="/contact/#quote">Tell us about the repair</a><a class="cta-phone" href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a></div></div></section>
    </main>"""
    return page("Blackfriars Leak Restoration | Hekman Home Services", PROJECT_DETAILS["/projects/blackfriars-leak-restoration/"]["description"], "/projects/blackfriars-leak-restoration/", "blackfriars-restored-room.jpg", "projects", body, "project-story-page")
def hilltop_project_page() -> str:
    project_name = "Hilltop: One Home, One Clear Point of View"
    body = f"""
    {hero("hilltop-kitchen-wide.jpg", "Completed Hilltop kitchen and island", "Hekman project story · London, Ontario", "Hilltop: one home, one clear point of view.", "A whole-home transformation connecting the kitchen, bathroom, lower level, entry, stairs, flooring and finish details into a cohesive result.", small=True, position="50% 52%")}
    <main id="main">
      {breadcrumbs(project_name)}
      <section class="section section-paper"><div class="wrap service-intro story-summary"><div class="reveal"><p class="eyebrow">Whole-home transformation</p><h2>More than a collection of renovated rooms.</h2><p>Hilltop is the kind of project where every choice affects the next. The bright kitchen became an anchor, while flooring, stairs, the lower level, two bathrooms and the entry were carried through with a consistent balance of warm wood, crisp white finishes and dark architectural details.</p><p>The project photography follows those decisions from one space to the next, including two bathroom renovations with very different starting points.</p></div><ul class="scope-list reveal"><li>Kitchen cabinetry, island and finish details</li><li>Upstairs tub surround and basement shower</li><li>Lower-level living space</li><li>Flooring, stairs and transitions</li><li>Entry and interior finish work</li><li>Whole-home visual continuity</li></ul></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("Inside Hilltop", "A complete home, viewed room by room.", "The kitchen leads the story, but the strength of the transformation is how the finished spaces belong together.")}<div class="story-mosaic story-mosaic-hilltop">
        <figure class="story-feature"><img src="/hilltop-kitchen-angle.jpg" alt="Angled view of the completed Hilltop kitchen" loading="lazy"><figcaption>The kitchen anchors the transformation</figcaption></figure>
        <figure><img src="/hilltop-kitchen-range.jpg" alt="Hilltop kitchen range wall and white cabinetry" loading="lazy"><figcaption>Cabinetry and range wall</figcaption></figure>
        <figure><img src="/hilltop-kitchen-sink.jpg" alt="Hilltop kitchen sink and backsplash detail" loading="lazy"><figcaption>Sink and backsplash detail</figcaption></figure>
        <figure><img src="/hilltop-kitchen-island.jpg" alt="Hilltop kitchen island cabinetry and counter detail" loading="lazy"><figcaption>Island finish work</figcaption></figure>
        <figure class="story-wide"><img src="/hilltop-lower-level.jpg" alt="Completed Hilltop lower level with fireplace and warm flooring" loading="lazy"><figcaption>Finished lower-level living space</figcaption></figure>
        <figure><img src="/hilltop-staircase.jpg" alt="Finished Hilltop staircase with dark railing" loading="lazy"><figcaption>Stair and railing detail</figcaption></figure>
        <figure><img src="/hilltop-entry.jpg" alt="Completed Hilltop entry and floor transition" loading="lazy"><figcaption>Entry and transition</figcaption></figure>
        <figure><img src="/hilltop-bathroom-shower.jpg" alt="Completed Hilltop bathroom glass shower" loading="lazy"><figcaption>Glass shower finish</figcaption></figure>
        <figure><img src="/hilltop-bathroom-vanity.jpg" alt="Completed Hilltop bathroom vanity" loading="lazy"><figcaption>Bathroom vanity</figcaption></figure>
      </div></div></section>
      <section class="section section-paper" id="hilltop-bathrooms"><div class="wrap">{section_heading("Two bathroom transformations", "The room details make each sequence unmistakable.", "A sloped ceiling and ornate mirror identify the upstairs bathroom. Downstairs, the shower position, vanity wall and compact footprint carry through from the older room to the finished glass enclosure.")}
        <div class="comparison-grid comparison-grid-two">
          <article class="comparison-card reveal">
            <div class="comparison-images">
              <figure><img src="/hilltop-green-tile-before.jpg" alt="Hilltop upstairs bathroom before renovation with green tile around the tub" loading="lazy"><figcaption>Before</figcaption></figure>
              <figure><img src="/hilltop-green-tile-after.jpg" alt="Hilltop upstairs bathroom after renovation with marble-look tub-surround tile" loading="lazy"><figcaption>After</figcaption></figure>
            </div>
            <h3>Upstairs: green tile to a brighter tub surround</h3>
            <p>The original green tile was replaced with marble-look wall tile, dark linear accents and updated fixtures. The sloped ceiling remains the room’s defining architectural line.</p>
          </article>
          <article class="comparison-card reveal">
            <div class="comparison-images">
              <figure><img src="/hilltop-basement-bathroom-before.jpg" alt="Hilltop basement bathroom before renovation with an older shower and drop ceiling" loading="lazy"><figcaption>Before</figcaption></figure>
              <figure><img src="/hilltop-basement-bathroom-wide.jpg" alt="Hilltop basement bathroom after renovation with a white vanity and glass shower" loading="lazy"><figcaption>After</figcaption></figure>
            </div>
            <h3>Downstairs: a complete shower and finish renewal</h3>
            <p>The older shower, drop ceiling and blue finishes gave way to white subway tile, gray accents, a glass enclosure, a clean drywall ceiling and a new vanity.</p>
          </article>
        </div>
        <div class="case-study-media case-study-media-three hilltop-bathroom-details reveal">
          <figure><img src="/hilltop-bathroom-vanity.jpg" alt="Completed Hilltop upstairs bathroom vanity beneath the sloped ceiling" loading="lazy"><figcaption>Upstairs vanity finish</figcaption></figure>
          <figure><img src="/hilltop-basement-bathroom-during.jpg" alt="Hilltop basement bathroom during wall, tile and floor work" loading="lazy"><figcaption>Basement build stage</figcaption></figure>
          <figure><img src="/hilltop-basement-bathroom-vanity.jpg" alt="Completed Hilltop basement bathroom white vanity and mirror" loading="lazy"><figcaption>Basement vanity finish</figcaption></figure>
        </div>
      </div></section>
      <section class="section section-stone"><div class="wrap editorial-grid"><div class="editorial-media reveal"><img src="/hilltop-kitchen-wide.jpg" alt="Wide view across the Hilltop kitchen and dining space" loading="lazy"><span>A cohesive whole-home finish</span></div><div class="editorial-copy reveal"><p class="eyebrow">The design idea</p><h2>Consistency without making every room identical.</h2><p>Hilltop uses repeated cues—light cabinetry, warm flooring, dark railings and hardware, clean sightlines—to give the home a recognizable character. Each room still solves its own practical needs, but the transitions no longer feel accidental.</p><a class="text-link dark-link" href="/contact/#quote">Discuss a whole-home renovation <span aria-hidden="true">↗</span></a></div></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("Connected services", "The rooms are only part of the scope.", "Whole-home work brings layout, surfaces, storage and finishing into the same plan.")}<div class="service-grid related-grid">{service_card("kitchens", compact=True, variant=3)}{service_card("bathrooms", compact=True, variant=3)}{service_card("basements", compact=True, variant=3)}</div></div></section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">Planning a bigger transformation?</p><h2>Start with the whole home.</h2><p>Show us the rooms, the frustrations and what you want the property to become.</p></div><div><a class="button button-primary" href="/contact/#quote">Request a Quote</a><a class="cta-phone" href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a></div></div></section>
    </main>"""
    return page("Hilltop Home Transformation | Hekman Home Services", "Explore Hekman Home Services’ Hilltop renovation in London, including the kitchen, two bathroom transformations, lower level, stairs and finish work.", "/projects/hilltop-home-transformation/", "hilltop-kitchen-wide.jpg", "projects", body, "project-story-page")
def medway_project_page() -> str:
    project_name = "Medway: More Storage, Better Flow and a Seamless Upper Level"
    body = f"""
    {hero("medway-floor-door-transition.jpg", "Completed Medway doorway with cool gray-brown plank flooring and a clean transition", "Medway project story · London, Ontario", "More storage. Better flow. One seamless upper level.", "What began as a flooring update grew into a practical transformation of three rooms, with relocated and new closets, coordinated trim and clean transitions throughout.", small=True, position="50% 64%")}
    <main id="main">
      {breadcrumbs(project_name)}
      <section class="section section-paper"><div class="wrap service-intro story-summary"><div class="reveal"><p class="eyebrow">Anonymous Medway project · completed</p><h2>A flooring project that solved much more than the floor.</h2><p>Carpet was removed from three rooms and replaced with cool gray-brown plank flooring carried through the upper level to coordinate with the previously completed main floor.</p><p>At the same time, an existing closet opening was closed and relocated to create a larger closet on the other side of the wall. The primary bedroom also received a new double closet. New doors, casing and baseboards connected the rooms, and the altered wall surfaces were left seamless and primed for the homeowner’s final paint.</p></div><ul class="scope-list reveal"><li>Carpet removal in three rooms</li><li>Plank flooring and clean transitions</li><li>Relocated and enlarged closet</li><li>New double closet in the primary bedroom</li><li>New doors, casing and baseboards</li><li>Seamless primed surfaces, ready for final paint</li></ul></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("Before, during and complete", "The real work is visible in the transitions", "Six selected photographs show the original carpeted room, the relocated closet opening, flooring installation and the finished upper level, including the exact plank colour at the doorway.")}<div class="story-mosaic story-mosaic-medway">
        <figure class="story-feature"><img src="/medway-finished-room.jpg" alt="Completed Medway room with cool gray-brown plank flooring and finished baseboards" loading="lazy"><figcaption>Completed room</figcaption></figure>
        <figure><img src="/medway-closet-before.jpg" alt="Medway room before the flooring and closet changes, with carpet and the new closet opening visible" loading="lazy"><figcaption>Before: carpet and existing room layout</figcaption></figure>
        <figure><img src="/medway-closet-relocation-progress.jpg" alt="Former Medway closet opening closed and prepared to become a seamless wall" loading="lazy"><figcaption>During: former closet opening closed</figcaption></figure>
        <figure><img src="/medway-floor-installation.jpg" alt="Plank flooring being installed in the Medway upper level" loading="lazy"><figcaption>During: plank flooring installation</figcaption></figure>
        <figure class="story-wide"><img src="/medway-floor-door-transition.jpg" alt="Completed Medway door, cool gray-brown plank flooring and clean threshold transition" loading="lazy"><figcaption>Completed detail: door, floor and transition</figcaption></figure>
        <figure><img src="/medway-finished-floor-detail.jpg" alt="Close view of the completed Medway plank flooring and clean edge detail" loading="lazy"><figcaption>Completed floor detail</figcaption></figure>
      </div></div></section>
      <section class="section section-stone"><div class="wrap editorial-grid reverse"><div class="editorial-media reveal"><img src="/medway-floor-door-transition.jpg" alt="Close view of the completed Medway flooring at a doorway transition" loading="lazy"><span>Exact installed flooring</span></div><div class="editorial-copy reveal"><p class="eyebrow">Budget-conscious collaboration</p><h2>More function, with the spending focused where it mattered.</h2><p>The homeowner supplied the flooring. Hekman Home Services provided the trim and doors at cost, helping the larger storage and finish scope stay within the homeowner’s budget.</p><p>The result improves daily storage, creates a more connected upper level and adds a cleaner finish that supports future resale appeal.</p><a class="text-link dark-link" href="/services/flooring/">Explore flooring installation <span aria-hidden="true">↗</span></a></div></div></section>
      <section class="section section-paper"><div class="wrap testimonial-feature reveal"><p class="eyebrow">Homeowner feedback</p><blockquote>“This team is amazing—so meticulous and detail-oriented. Love their work.”</blockquote><p>The homeowner has already said they want Hekman Home Services back for future work.</p><cite>Anonymous Medway homeowner</cite></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("Connected services", "Flooring, storage and finish carpentry in one plan.", "The room works because the floor, closets, doors and trim were considered together.")}<div class="service-grid related-grid">{service_card("flooring", compact=True, variant=1)}{service_card("structural-layout", compact=True, variant=1)}{service_card("handyman-repairs", compact=True, variant=1)}</div></div></section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">Could your rooms work harder?</p><h2>Start with the floor—or the storage problem around it.</h2><p>Send a few photos and tell us what is not working now. We will look at the connected details with you.</p></div><div><a class="button button-primary" href="/contact/#quote">Request a Quote</a><a class="cta-phone" href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a></div></div></section>
    </main>"""
    return page("Medway Flooring & Storage Transformation | Hekman", PROJECT_DETAILS["/projects/medway-flooring-storage/"]["description"], "/projects/medway-flooring-storage/", "medway-floor-door-transition.jpg", "projects", body, "project-story-page")
def westmount_porch_project_page() -> str:
    project_name = "A Westmount Porch and Entry, Modernized by Neighbours"
    body = f"""
    {hero("westmount-porch-after-night.jpg", "Finished Westmount porch and entry illuminated at night", "Westmount project story · London, Ontario", "A more modern welcome, built by neighbours.", "A separate porch and entry revitalization for a repeat Westmount customer and neighbour who has also trusted Hekman Home Services with several handyman projects.", small=True, position="50% 58%")}
    <main id="main">
      {breadcrumbs(project_name)}
      <section class="section section-paper"><div class="wrap service-intro story-summary"><div class="reveal"><p class="eyebrow">Repeat customer · completed exterior</p><h2>A front entry that feels cleaner by day and brighter after dark.</h2><p>This porch and entry project focused on the details that shape the first impression of a home: repairing and refreshing the exterior, cleaning up the visual lines and bringing the lighting into the finished result.</p><p>The customer is also a Westmount neighbour. Hekman Home Services has returned for several handyman projects over time, building the kind of local working relationship where one completed repair can lead naturally to the next priority.</p></div><ul class="scope-list reveal"><li>Porch and entry revitalization</li><li>Careful exterior progress work</li><li>Cleaner exterior lines and finish details</li><li>Entry lighting in the completed design</li><li>Additional handyman work completed over time</li><li>Local neighbour service in Westmount</li></ul></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("Progress to finished welcome", "Two daylight views. One strong night finish.", "The real project photographs are intentionally limited to the strongest progress image, the finished daytime view and the completed exterior lighting at night.")}<div class="story-mosaic story-mosaic-porch">
        <figure class="story-feature"><img src="/westmount-porch-work-in-progress.jpg" alt="Exterior work in progress at an anonymous Westmount porch and entry" loading="lazy"><figcaption>During: careful porch and entry work</figcaption></figure>
        <figure class="story-wide"><img src="/westmount-porch-after-day.jpg" alt="Finished anonymous Westmount porch and entry in daylight" loading="lazy"><figcaption>After: finished daytime view</figcaption></figure>
      </div><p class="story-photo-note reveal"><strong>Finished night view:</strong> the project hero above shows the strongest completed photograph after dark, with the new lighting bringing the refreshed entry to life.</p></div></section>
      <section class="section section-stone"><div class="wrap testimonial-feature reveal"><p class="eyebrow">Homeowner feedback</p><blockquote>“Efficient, professional and fantastic work. Rene modernized the front of our home, and I would recommend him for home repair and remodelling.”</blockquote><cite>Anonymous repeat Westmount customer</cite></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("Connected services", "Exterior improvements and the repair list beside them.", "A focused porch project can sit alongside doors, trim, repairs and other handyman priorities around the home.")}<div class="service-grid related-grid">{service_card("decks-exterior", compact=True, variant=3)}{service_card("handyman-repairs", compact=True, variant=2)}{service_card("drywall-ceiling-repair", compact=True, variant=2)}</div></div></section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">Need help with the front of your home?</p><h2>Show us the porch—and the repair list that comes with it.</h2><p>Whether it is one exterior priority or several compatible handyman items, a few photos are enough to begin.</p></div><div><a class="button button-primary" href="/contact/#quote">Request a Quote</a><a class="cta-phone" href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a></div></div></section>
    </main>"""
    return page("Westmount Porch & Entry Revitalization | Hekman", PROJECT_DETAILS["/projects/westmount-porch-entry/"]["description"], "/projects/westmount-porch-entry/", "westmount-porch-after-night.jpg", "projects", body, "project-story-page")
def westmount_project_page() -> str:
    project_name = "Westmount: A Home Transformation Built in Thoughtful Phases"
    body = f"""
    {hero("westmount-transformation-blue-wall-flooring.jpg", "Completed Westmount living-space phase with plank flooring, pot lights and a deep-blue feature wall", "Ongoing Westmount transformation · London, Ontario", "A home transformation built in thoughtful phases.", "This is an ongoing project, planned and completed in stages around the clients’ life, timing and budget. Every finished phase is designed to connect with what came before—and what is still ahead.", small=True, position="50% 52%")}
    <main id="main">
      {breadcrumbs(project_name)}
      <section class="section section-paper"><div class="wrap service-intro story-summary"><div class="reveal"><p class="status-badge"><span aria-hidden="true"></span> Project in progress</p><p class="eyebrow">Phased Westmount home transformation</p><h2>A long-term plan, built at the right pace for the homeowners.</h2><p>This project has been intentionally completed in thoughtful phases rather than treated as one rushed renovation. Layout changes, demolition, drywall, painting, flooring, lighting and storage work established the direction of the home before the kitchen and later finishing phases moved forward.</p><p>The confirmed bathroom scope is <strong>one powder-room renovation</strong>. The project also includes kitchen work, cabinetry, doors, trim and related finishing. Some phases are complete; the overall transformation and kitchen are not.</p></div><ul class="scope-list reveal"><li>Layout changes and demolition</li><li>Drywall, surface preparation and painting</li><li>Plank flooring and pot lights</li><li>Kitchen cabinetry and ongoing kitchen work</li><li>One powder-room renovation</li><li>Storage, doors, trim and finishing</li></ul></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("Work completed in connected phases", "From demolition to a kitchen still in progress.", "Six selected real photographs show the sequence accurately. Completed room phases are identified as complete; the kitchen remains a current progress view, not a final after photograph.")}<div class="story-mosaic story-mosaic-westmount-phased">
        <figure class="story-feature"><img src="/westmount-transformation-demolition.jpg" alt="Westmount main-floor demolition and layout changes in progress" loading="lazy"><figcaption>Phase: demolition and layout changes</figcaption></figure>
        <figure><img src="/westmount-transformation-protection-painting.jpg" alt="Westmount room protected with coverings while painting is underway" loading="lazy"><figcaption>Phase: protection and painting</figcaption></figure>
        <figure><img src="/westmount-transformation-pot-lights.jpg" alt="New pot lights installed across the Westmount main-floor ceiling" loading="lazy"><figcaption>Phase: new pot lights</figcaption></figure>
        <figure class="story-wide"><img src="/westmount-transformation-blue-wall-flooring.jpg" alt="Completed Westmount living-space phase with plank flooring, pot lights and a deep-blue feature wall" loading="lazy"><figcaption>Completed phase: flooring, lighting and feature wall</figcaption></figure>
        <figure><img src="/westmount-transformation-cabinet-install.jpg" alt="Hekman Home Services crew installing kitchen cabinetry in the phased Westmount project" loading="lazy"><figcaption>Phase: cabinetry installation</figcaption></figure>
        <figure><img src="/westmount-transformation-kitchen-current.jpg" alt="Current Westmount kitchen progress before the planned backsplash and final styling" loading="lazy"><figcaption>Current kitchen progress — not the final after</figcaption></figure>
      </div></div></section>
      <section class="section section-stone"><div class="wrap editorial-grid"><div class="editorial-media reveal"><img src="/westmount-transformation-kitchen-current.jpg" alt="Current Westmount kitchen with cabinetry installed before the backsplash and final styling" loading="lazy"><span>Real current progress</span></div><div class="editorial-copy reveal"><p class="eyebrow">What is still planned</p><h2>The kitchen is not being presented as finished.</h2><p>Cabinetry and major surfaces are in place, but the backsplash and final styling remain ahead. The planned backsplash is <strong>white 2-inch by 10-inch subway tile installed in a herringbone pattern and carried to the ceiling.</strong></p><p>There is no finished-kitchen rendering on this page. When the real final work is complete, the project story can be updated with an accurate after photograph.</p><a class="text-link dark-link" href="/services/kitchens/">Explore kitchen renovations <span aria-hidden="true">↗</span></a></div></div></section>
      <section class="section section-paper"><div class="wrap">{section_heading("Why the phased approach works", "Each stage protects the bigger plan.", "Completing a home in phases can make the budget and disruption more manageable, as long as every decision supports the later work.")}<div class="proof-grid story-step-grid"><article class="proof-card reveal"><h3>Start with function</h3><p>Address layout, lighting, storage and the surfaces that influence the whole main floor.</p></article><article class="proof-card reveal"><h3>Protect finished work</h3><p>Prepare and cover completed areas while the next phase is underway.</p></article><article class="proof-card reveal"><h3>Connect each choice</h3><p>Coordinate flooring, paint, cabinetry, doors and trim with what is already complete.</p></article><article class="proof-card reveal"><h3>Stay accurate about progress</h3><p>Show completed phases clearly while staying honest about what still remains.</p></article></div></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("Related expertise", "One transformation, several connected scopes.", "Kitchen work, layout changes and finished surfaces all need to meet cleanly across the phases.")}<div class="service-grid related-grid">{service_card("kitchens", compact=True, variant=4)}{service_card("structural-layout", compact=True, variant=2)}{service_card("flooring", compact=True, variant=3)}</div></div></section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">Planning a renovation in phases?</p><h2>Start with the whole plan, even if you build it one stage at a time.</h2><p>Show us the rooms, priorities and timing. We will help identify how the pieces should connect.</p></div><div><a class="button button-primary" href="/contact/#quote">Request a Quote</a><a class="cta-phone" href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a></div></div></section>
    </main>"""
    return page("Phased Westmount Home Transformation | Hekman", PROJECT_DETAILS["/projects/westmount-1970s-transformation/"]["description"], "/projects/westmount-1970s-transformation/", "westmount-transformation-blue-wall-flooring.jpg", "projects", body, "project-story-page")
def salon_project_page() -> str:
    project_name = "London Salon: Moisture Investigation and Interior Restoration"
    body = f"""
    {project_story_hero("salon-restored-wall.jpg", "Completed wall and ceiling restoration in an anonymous London salon", "Commercial restoration · London, Ontario", "The repair disappears. The salon gets its room back.", "Moisture investigation, affected-material removal and wall-and-ceiling rebuilding returned this working salon to a bright, client-ready finish.")}
    <main id="main">
      {breadcrumbs(project_name)}
      <section class="section section-paper"><div class="wrap service-intro story-summary"><div class="reveal"><p class="eyebrow">Commercial moisture repair &amp; restoration</p><h2>A visible problem called for a closer look.</h2><p>Moisture readings at the trim helped document the affected area before damaged wall material was removed. From there, the repair became a connected wall-and-ceiling scope—not a cosmetic patch over an unresolved condition.</p><p>The goal was to rebuild the affected surfaces cleanly and return the salon to the bright, polished environment its staff and clients already knew.</p></div><ul class="scope-list reveal"><li>Moisture investigation and documentation</li><li>Affected wall-material removal</li><li>Wall and ceiling rebuilding</li><li>Drywall compound and surface preparation</li><li>Primer, paint and connected finish work</li><li>Planning around an operating business</li></ul></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("Completed result first", "A bright working salon—and the repair sequence behind it", "The finished wall leads the story. Supporting photographs document the investigation, what was found and the rebuilding work that made the result possible.")}<div class="story-mosaic story-mosaic-salon">
        <figure class="story-feature"><img src="/salon-restored-wall.jpg" alt="Completed wall repair in the anonymous London salon" loading="lazy"><figcaption>Completed result: repaired wall restored</figcaption></figure>
        <figure><img src="/salon-restored-wall-detail.jpg" alt="Completed repaired salon wall with the original alarm and ceiling details retained" loading="lazy"><figcaption>Completed finish detail</figcaption></figure>
        <figure><img src="/salon-moisture-investigation.jpg" alt="Moisture meter documenting an affected trim area in an anonymous London salon" loading="lazy"><figcaption>Investigation: moisture documented</figcaption></figure>
        <figure class="story-wide"><img src="/salon-affected-wallboard.jpg" alt="Removed salon wallboard showing the affected backing during repair work" loading="lazy"><figcaption>Affected material removed</figcaption></figure>
        <figure class="story-wide"><img src="/salon-wall-ceiling-rebuild.jpg" alt="Wall and ceiling surfaces being rebuilt in the anonymous London salon" loading="lazy"><figcaption>Wall and ceiling rebuilding</figcaption></figure>
      </div></div></section>
      <section class="section section-stone"><div class="wrap editorial-grid reverse"><div class="editorial-media reveal"><img src="/salon-wall-ceiling-rebuild.jpg" alt="Drywall and ceiling repair underway in an anonymous London salon" loading="lazy"><span>Repairing the construction, not hiding the symptom</span></div><div class="editorial-copy reveal"><p class="eyebrow">A repair planned around a business</p><h2>The room still had a job to do.</h2><p>Access, staff, clients and normal operating needs all shape commercial restoration. The work had to address the affected construction while protecting the salon’s established layout, lighting and identity.</p><p>Once the affected material was removed, the wall and ceiling could be rebuilt, prepared and finished as one connected surface.</p><a class="text-link dark-link" href="/services/commercial/">Explore commercial repairs <span aria-hidden="true">↗</span></a></div></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("Related expertise", "Investigation, rebuilding and finish work in one clear story", "Commercial access, restoration sequencing and precise drywall finishing all mattered to this result.")}<div class="service-grid related-grid">{service_card("commercial", compact=True, variant=0)}{service_card("water-damage", compact=True, variant=0)}{service_card("drywall-ceiling-repair", compact=True, variant=0)}</div></div></section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">Damage interrupting your business?</p><h2>Show us what happened—and what needs to be working again.</h2><p>Send a few photos, the property location and any access or operating-hour details. We will help you understand the construction work that may come next.</p></div><div><a class="button button-primary" href="/contact/#quote">Start the Conversation</a><a class="cta-phone" href="tel:{PHONE_LINK}">Call or text {PHONE_DISPLAY}</a></div></div></section>
    </main>"""
    return page("Salon Moisture & Drywall Restoration London ON | Hekman", PROJECT_DETAILS["/projects/commercial-salon-repair/"]["description"], "/projects/commercial-salon-repair/", "salon-restored-wall.jpg", "projects", body, "project-story-page")

def pond_mills_project_page() -> str:
    project_name = "Pond Mills: One Repair List, A Much Closer Look"
    body = f"""
    {project_story_hero("pond-mills-kitchen-floor-after.jpg", "Completed light plank flooring carried into a Pond Mills kitchen", "Pond Mills · London, Ontario", "One repair list. A much closer look.", "When a London home had not sold, the homeowner asked for help. A closer inspection connected the visible interior work with moisture concerns and an exterior water-management plan.")}
    <main id="main">
      {breadcrumbs(project_name)}
      <section class="section section-paper"><div class="wrap service-intro story-summary"><div class="reveal"><p class="eyebrow">Residential repairs · completed</p><h2>The first list did not tell the whole story</h2><p>The flooring and finish work were only part of what the home needed. During the inspection, Hekman also found wet conditions around window wells, window trim and surrounding frame assemblies that called for a broader repair plan.</p><p>The completed exterior scope included removing a problem weeping pipe, adjusting localized grading and improving the downspout arrangement. Indoors, worn floor surfaces were removed and light plank flooring was carried through the adjoining rooms and kitchen for a cleaner, more consistent result.</p></div><ul class="scope-list reveal"><li>Whole-home repair-list review</li><li>Existing flooring removal and preparation</li><li>Light plank flooring through connected rooms</li><li>Window wells, trim and frame assemblies reviewed</li><li>Problem exterior weeping pipe removed</li><li>Localized grading and downspout work</li></ul></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("Same kitchen, clear result", "The floor now carries cleanly into the room", "The doorway, oak cabinetry, white range and threshold make the change easy to compare.")}<div class="comparison-grid comparison-grid-two">
        <article class="comparison-card reveal"><div class="comparison-images"><figure><img src="/pond-mills-kitchen-floor-before.jpg" alt="Pond Mills kitchen with the original narrow warm-toned flooring before work" loading="lazy"><figcaption>Before renovation</figcaption></figure><figure><img src="/pond-mills-kitchen-floor-after.jpg" alt="Same Pond Mills kitchen with completed light plank flooring" loading="lazy"><figcaption>Completed result</figcaption></figure></div><h3>A lighter, continuous floor</h3><p>The new plank colour gives the kitchen and adjoining space one calmer visual line without changing the room’s established cabinetry.</p></article>
        <article class="comparison-card reveal"><div class="comparison-images"><figure><img src="/pond-mills-basement-subfloor-prep.jpg" alt="Pond Mills lower-level room prepared after the old floor was removed" loading="lazy"><figcaption>Subfloor preparation</figcaption></figure><figure><img src="/pond-mills-basement-floor-after.jpg" alt="Same Pond Mills lower-level room with completed light plank flooring and baseboards" loading="lazy"><figcaption>Completed result</figcaption></figure></div><h3>Preparation that supports the finish</h3><p>Removal and substrate preparation came first; the final view shows the flooring, perimeter and baseboards resolved together.</p></article>
      </div></div></section>
      <section class="section section-stone"><div class="wrap">{section_heading("Work in sequence", "Real progress between removal and completion", "Selected photographs show materials on site, the old floor coming out and new planks being fitted. The near-complete view remains labelled as progress because its threshold and baseboard details were not yet finished.")}<div class="story-mosaic story-mosaic-pond-mills">
        <figure class="story-feature"><img src="/pond-mills-flooring-materials.jpg" alt="New flooring materials staged beside the existing Pond Mills floor" loading="lazy"><figcaption>Materials staged</figcaption></figure>
        <figure><img src="/pond-mills-basement-floor-removal.jpg" alt="Old Pond Mills lower-level flooring being removed" loading="lazy"><figcaption>Floor removal in progress</figcaption></figure>
        <figure><img src="/pond-mills-basement-floor-installation.jpg" alt="Light plank flooring being installed in the Pond Mills lower level" loading="lazy"><figcaption>Installation in progress</figcaption></figure>
        <figure class="story-wide"><img src="/pond-mills-basement-floor-nearing-completion.jpg" alt="Pond Mills lower-level flooring nearly complete before threshold and baseboard finishing" loading="lazy"><figcaption>Nearly complete: final edge details still ahead</figcaption></figure>
      </div></div></section>
      <section class="section section-paper"><div class="wrap editorial-grid reverse"><div class="editorial-media reveal"><img src="/pond-mills-kitchen-floor-after.jpg" alt="Completed Pond Mills flooring flowing from the adjoining room into the kitchen" loading="lazy"><span>Interior flooring result</span></div><div class="editorial-copy reveal"><p class="eyebrow">Inside and outside</p><h2>A cleaner interior, with the exterior water path addressed too</h2><p>The project photographs follow the flooring transformation. The exterior scope addressed a different part of the repair list: window-well and trim concerns, removal of the problem pipe, localized grading and a better downspout arrangement.</p><a class="text-link dark-link" href="/services/water-damage/">Explore restoration and damage repairs <span aria-hidden="true">↗</span></a></div></div></section>
      <section class="section section-stone"><div class="wrap">{section_heading("Finished walkthrough", "Follow the new floor into the kitchen", "This short, silent walkthrough shows how the completed flooring connects the adjoining room and kitchen.")}<div class="video-grid video-grid-single"><figure class="work-video reveal"><video controls playsinline preload="none" poster="/pond-mills-kitchen-floor-after.jpg" aria-label="Short walkthrough of completed light plank flooring in the Pond Mills home"><source src="/pond-mills-flooring-finished-tour.mp4" type="video/mp4">Your browser does not support embedded video.</video><figcaption><strong>Completed flooring walkthrough</strong><span>New light plank flooring carries from the adjoining room into the kitchen</span></figcaption></figure></div></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("Connected services", "The floor, repair list and moisture concerns needed one plan", "Interior finishing, focused repairs and exterior water management were considered together.")}<div class="service-grid related-grid">{service_card("flooring", compact=True, variant=1)}{service_card("handyman-repairs", compact=True, variant=1)}{service_card("water-damage", compact=True, variant=1)}</div></div></section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">Does one visible issue suggest there may be more?</p><h2>Start with the whole repair list.</h2><p>Send a few photos—no detailed plans required. We will look at how the work connects before the scope is set.</p></div><div><a class="button button-primary" href="/contact/#quote">Tell Us About Your Project</a><a class="cta-phone" href="tel:{PHONE_LINK}">Call or text {PHONE_DISPLAY}</a></div></div></section>
    </main>"""
    return page("Pond Mills Home Repairs & Flooring | Hekman", PROJECT_DETAILS["/projects/pond-mills-home-repairs/"]["description"], "/projects/pond-mills-home-repairs/", "pond-mills-kitchen-floor-after.jpg", "projects", body, "project-story-page")

def multi_unit_deck_project_page() -> str:
    project_name = "London Multi-Unit Deck Renewal"
    body = f"""
    {project_story_hero("project-103.jpg", "Completed elevated rear deck at an anonymous multi-unit property", "Exterior project · London area", "One exterior rhythm, renewed across the row.", "A coordinated deck-and-guard renewal documented from the weathered existing wood through open construction work and the completed rear elevations.")}
    <main id="main">
      {breadcrumbs(project_name)}
      <section class="section section-paper"><div class="wrap service-intro story-summary"><div class="reveal"><p class="eyebrow">Anonymous multi-unit property · completed</p><h2>Repeated decks called for one consistent finish</h2><p>The existing wood showed its age across connected rear elevations. Treating the deck and guard work as a coordinated exterior scope helped the completed row read as one property again.</p><p>Open construction and board fitting moved into renewed deck and guard surfaces across the repeated elevations. The finished work belongs to the building’s original rhythm, while the property itself remains unnamed.</p></div><ul class="scope-list reveal"><li>Existing deck and guard condition documented</li><li>Open construction and framing work</li><li>Board fitting and exterior finish work</li><li>Repeated rear elevations coordinated</li><li>Completed deck and guard surfaces</li><li>Anonymous multi-unit property</li></ul></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("Before, during and complete", "The same brick row through the work", "The building, bay projections, deck spacing and rear elevations anchor every stage to the same anonymous property.")}<div class="story-mosaic story-mosaic-decks">
        <figure class="story-feature"><img src="/multi-unit-decks-before.jpg" alt="Weathered connected rear decks before the renewal work" loading="lazy"><figcaption>Before: weathered deck and guards</figcaption></figure>
        <figure><img src="/project-101.jpg" alt="Rear deck opened during construction work at the same multi-unit property" loading="lazy"><figcaption>During: open construction</figcaption></figure>
        <figure><img src="/project-100.jpg" alt="Completed renewed rear deck and guard at the multi-unit property" loading="lazy"><figcaption>Completed deck and guard</figcaption></figure>
        <figure class="story-wide"><img src="/project-104.jpg" alt="Completed row of renewed rear decks behind the brick multi-unit property" loading="lazy"><figcaption>Completed row</figcaption></figure>
      </div></div></section>
      <section class="section section-stone"><div class="wrap">{section_heading("Work in motion", "Open framing, fitted boards and the completed row", "This silent sequence moves from open framing and board fitting to the renewed rear elevations.")}<div class="video-grid video-grid-single"><figure class="work-video reveal"><video controls playsinline preload="none" poster="/project-103.jpg" aria-label="Short sequence showing work and completed rear decks at an anonymous multi-unit property"><source src="/multi-unit-deck-repair-sequence.mp4" type="video/mp4">Your browser does not support embedded video.</video><figcaption><strong>Deck renewal sequence</strong><span>Open framing, custom-fit boards and the completed row of rear decks</span></figcaption></figure></div></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("Connected services", "Exterior work meets structure, access and finish details", "Deck, repair and layout decisions have to make sense together at the property.")}<div class="service-grid related-grid">{service_card("decks-exterior", compact=True, variant=1)}{service_card("handyman-repairs", compact=True, variant=2)}{service_card("structural-layout", compact=True, variant=2)}</div></div></section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">Have an exterior that needs a closer look?</p><h2>Show us the full run, not only the worst board.</h2><p>Wide photos and a few close details help us understand how the repair or renewal should connect.</p></div><div><a class="button button-primary" href="/contact/#quote">Request a Quote</a><a class="cta-phone" href="tel:{PHONE_LINK}">Call or text {PHONE_DISPLAY}</a></div></div></section>
    </main>"""
    return page("Multi-Unit Deck Renewal | Hekman Home Services", PROJECT_DETAILS["/projects/multi-unit-deck-renewal/"]["description"], "/projects/multi-unit-deck-renewal/", "project-103.jpg", "projects", body, "project-story-page")
def kitchen_renewal_project_page() -> str:
    project_name = "London Office Kitchen: A Compact Staff Space Rebuilt"
    body = f"""
    {hero("kitchenette-after-wide.jpg", "Completed office kitchen with walnut-look cabinetry and gray counter", "Commercial kitchen project · London, Ontario", "A compact office kitchen, rebuilt around the work it needs to do.", "Old cabinetry came out, wall and plumbing access were addressed, and the staff space was rebuilt with clean-lined storage, a new counter, sink and finish details.", small=True, position="50% 52%")}
    <main id="main">
      {breadcrumbs(project_name)}
      <section class="section section-paper"><div class="wrap service-intro story-summary"><div class="reveal"><p class="eyebrow">Office kitchen · before · during · after</p><h2>A complete transformation without changing the room’s footprint.</h2><p>The original office kitchen had dark, aging cabinets, a worn counter and visible ceiling damage. Once the cabinetry was removed, the wall could be opened where needed for plumbing and repair access. New cabinet boxes and fronts were installed before the counter, sink, hardware, wall finish and ceiling were brought together.</p><p>The finished staff space keeps the practical appliances and familiar layout while giving the room more usable storage and a much cleaner working surface.</p></div><ul class="scope-list reveal"><li>Existing cabinetry and counter removal</li><li>Wall opening and plumbing access</li><li>Drywall patching and painting</li><li>New upper and lower cabinets</li><li>Counter, sink and hardware</li><li>Ceiling and final finish work</li></ul></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("The kitchen sequence", "The same wall, through every stage.", "A genuine before, build and completed series shows exactly how the old kitchen became the finished space.")}<div class="story-mosaic story-mosaic-kitchenette">
        <figure class="story-feature"><img src="/kitchenette-before-wide.jpg" alt="Wide view of the kitchen before renovation" loading="lazy"><figcaption>Before: existing kitchen</figcaption></figure>
        <figure><img src="/kitchenette-before-detail.jpg" alt="Existing cabinets, counter and ceiling damage before work" loading="lazy"><figcaption>Existing cabinetry and ceiling condition</figcaption></figure>
        <figure><img src="/kitchenette-wall-plumbing-stage.jpg" alt="Kitchen wall opened for plumbing and repair access" loading="lazy"><figcaption>Wall and plumbing access</figcaption></figure>
        <figure><img src="/kitchenette-cabinet-installation.jpg" alt="New kitchen cabinets being installed before the counter" loading="lazy"><figcaption>Cabinet installation</figcaption></figure>
        <figure class="story-wide"><img src="/kitchenette-after-detail.jpg" alt="Completed kitchen cabinetry, counter, sink and hardware" loading="lazy"><figcaption>After: cabinetry and counter complete</figcaption></figure>
        <figure class="story-wide"><img src="/kitchenette-after-wide.jpg" alt="Wide view of the completed compact kitchen" loading="lazy"><figcaption>The finished kitchen</figcaption></figure>
      </div></div></section>
      <section class="section section-stone"><div class="wrap">{section_heading("A closer look", "Walk through the completed cabinetry and counter.", "The walkthrough brings the cabinet fronts, hardware, sink, counter and finished wall details into view.")}<div class="video-grid video-grid-single"><figure class="work-video reveal"><video controls playsinline preload="none" poster="/kitchenette-after-detail.jpg" aria-label="Video walkthrough of completed kitchen cabinetry, sink and counter"><source src="/kitchenette-finish-tour.mp4" type="video/mp4">Your browser does not support embedded video.</video><figcaption><strong>Completed kitchen walkthrough</strong><span>Cabinet fronts, hardware, sink, counter and finished wall details.</span></figcaption></figure></div></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("Connected services", "Cabinets are only one part of a kitchen.", "Plumbing access, drywall, paint, trim and repair work all affect the finished result.")}<div class="service-grid related-grid">{service_card("commercial", compact=True, variant=2)}{service_card("kitchens", compact=True, variant=3)}{service_card("drywall-ceiling-repair", compact=True, variant=2)}</div></div></section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">Have a kitchen that needs to work harder?</p><h2>Show us the room and the existing conditions.</h2><p>Wide photos and a short list of what you want to keep or change are enough to begin.</p></div><div><a class="button button-primary" href="/contact/#quote">Request a Quote</a><a class="cta-phone" href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a></div></div></section>
    </main>"""
    return page("Office Kitchen Renewal Before & After | Hekman", "See a genuine London office kitchen before, during and after renovation by Hekman Home Services, including cabinetry, plumbing access, drywall, counter and sink.", "/projects/kitchen-renewal/", "kitchenette-after-wide.jpg", "projects", body, "project-story-page")
def popcorn_project_page() -> str:
    project_name = "London Popcorn Ceiling Transformation"
    body = f"""
    {hero("project-016.jpg", "Original textured ceiling before smoothing and finishing", "Ceiling transformation · London, Ontario", "From popcorn texture to a clean, modern ceiling.", "A preparation-heavy process documented from the original texture through sanding, skim coats, surface checks and primer.", small=True, position="50% 35%")}
    <main id="main">
      {breadcrumbs(project_name)}
      <section class="section section-paper"><div class="wrap service-intro story-summary"><div class="reveal"><p class="eyebrow">Popcorn ceiling removal</p><h2>The smooth finish is earned before the paint goes on.</h2><p>This London ceiling project moved through multiple rooms and multiple coats. The original texture and an existing ceiling patch were assessed first. The ceiling was sanded, coated and checked in stages, with the dining room and living space progressing at different points before final sanding and primer.</p><p>The dedicated ceiling sander helped control the surface work, while drop cloths and room protection kept the process contained.</p></div><ul class="scope-list reveal"><li>Existing texture and patch assessment</li><li>Floor, wall and opening protection</li><li>Mechanical ceiling sanding</li><li>Skim coating in controlled stages</li><li>Drying and surface checks</li><li>Final sanding, primer and paint preparation</li></ul></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("The ceiling process", "Before, during and finish stage.", "These images follow the same ceiling work from the original textured surface to the coated and primed stages.")}<div class="story-mosaic story-mosaic-popcorn">
        <figure class="story-feature"><img src="/project-016.jpg" alt="Textured ceiling and existing patch before smooth-ceiling work" loading="lazy"><figcaption>Before: texture and previous patch</figcaption></figure>
        <figure><img src="/popcorn-ceiling-sander.jpg" alt="Dust-covered ceiling sander used on the popcorn ceiling project" loading="lazy"><figcaption>The ceiling sander after use</figcaption></figure>
        <figure><img src="/project-017.jpg" alt="Skim coating underway with floors and walls protected" loading="lazy"><figcaption>Coating and room protection</figcaption></figure>
        <figure class="story-wide"><img src="/project-015.jpg" alt="Ceiling after texture removal and smooth coating work" loading="lazy"><figcaption>After removal: coating and surface correction</figcaption></figure>
        <figure class="story-wide"><img src="/popcorn-ceiling-primer.jpg" alt="Primer being rolled over the smoothed ceiling" loading="lazy"><figcaption>Primer and finish stage</figcaption></figure>
      </div></div></section>
      <section class="section section-stone"><div class="wrap">{section_heading("Why preparation leads the project", "Ceiling work touches the whole room.", "Protection, dust control and repeat surface checks matter just as much as the final coat.")}<div class="proof-grid"><article class="proof-card reveal"><h3>Protect the room</h3><p>Cover floors, isolate openings and plan access before overhead work begins.</p></article><article class="proof-card reveal"><h3>Build a flat surface</h3><p>Sand, coat, dry and repeat until the texture and repair lines no longer control the ceiling.</p></article><article class="proof-card reveal"><h3>Prime and inspect</h3><p>Primer helps reveal remaining imperfections before the ceiling receives its final finish.</p></article></div></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("Related services", "A ceiling issue may connect to other work.", "Drywall repairs, water damage and broader room renovations can be coordinated in the same conversation.")}<div class="service-grid related-grid">{service_card("popcorn-ceiling-removal", compact=True, variant=2)}{service_card("drywall-ceiling-repair", compact=True, variant=3)}{service_card("water-damage", compact=True, variant=2)}</div></div></section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">Ready to lose the texture?</p><h2>Show us the ceiling and the rooms below it.</h2><p>Wide photos, close-ups and approximate room sizes are a useful place to start.</p></div><div><a class="button button-primary" href="/contact/#quote">Request a Quote</a><a class="cta-phone" href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a></div></div></section>
    </main>"""
    return page("Popcorn Ceiling Transformation London ON | Hekman Home Services", "See a Hekman Home Services popcorn ceiling project in London, Ontario, from the original textured ceiling through sanding, skim coating and primer.", "/projects/popcorn-ceiling-transformation/", "project-016.jpg", "projects", body, "project-story-page")
def glass_block_bathroom_project_page() -> str:
    project_name = "Jetted Tub to Glass Shower Bathroom Conversion"
    body = f"""
    {hero("bathroom-walnut-vanity-after.jpg", "Completed glass shower conversion beside the original glass-block window", "Bathroom transformation", "From jetted tub to glass shower.", "One genuine bathroom sequence—from the original tub platform through demolition and open-wall work to the completed tiled shower.", small=True, position="50% 52%")}
    <main id="main">
      {breadcrumbs(project_name)}
      <section class="section section-paper"><div class="wrap service-intro story-summary"><div class="reveal"><p class="eyebrow">Before · during · after</p><h2>A focused conversion that changed how the room works.</h2><p>The original jetted tub and deep tiled platform filled the window end of the bathroom. The renovation removed that assembly, opened the surrounding wall and floor where access was required, and rebuilt the area as a tiled shower with a sliding glass enclosure.</p><p>The glass-block window, walnut vanity and gray floor give the sequence clear visual anchors. They make it possible to follow the same room through every stage without borrowing photographs from another job.</p></div><ul class="scope-list reveal"><li>Jetted tub and tiled-platform removal</li><li>Wall, insulation and floor access</li><li>Shower preparation and waterproofing stages</li><li>Wall tile and shower base</li><li>Sliding glass enclosure</li><li>Trim, plumbing fixtures and final details</li></ul></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("The conversion sequence", "The same window. A completely different wet area.", "Four views follow the room from the existing jetted tub to the finished shower.")}<div class="story-mosaic story-mosaic-bathroom">
        <figure class="story-feature"><img src="/bathroom-glass-block-before.jpg" alt="Bathroom with jetted tub, tiled platform and glass-block window before conversion" loading="lazy"><figcaption>Before: jetted-tub layout</figcaption></figure>
        <figure><img src="/bathroom-glass-block-demolition.jpg" alt="Tiled tub platform and wall finishes partly removed during demolition" loading="lazy"><figcaption>Demolition underway</figcaption></figure>
        <figure><img src="/bathroom-glass-block-open-wall.jpg" alt="Tub removed with wall insulation and floor framing exposed" loading="lazy"><figcaption>Wall and floor opened</figcaption></figure>
        <figure class="story-wide"><img src="/bathroom-walnut-vanity-after.jpg" alt="Completed bathroom with gray tiled shower, sliding glass door and walnut vanity" loading="lazy"><figcaption>After: completed glass shower</figcaption></figure>
      </div></div></section>
      <section class="section section-stone"><div class="wrap">{section_heading("Work in motion", "See the project move from demolition to finish.", "These videos are compressed, never autoplay and wait to download until you choose to play them.")}<div class="video-grid">
        <figure class="work-video reveal"><video controls playsinline preload="none" poster="/bathroom-walnut-vanity-after.jpg" aria-label="Video showing the bathroom transformation from tub demolition through the completed shower"><source src="/bathroom-glass-block-transformation.mp4" type="video/mp4">Your browser does not support embedded video.</video><figcaption><strong>Transformation sequence</strong><span>Demolition, open-wall work, shower preparation and the completed room.</span></figcaption></figure>
        <figure class="work-video reveal"><video controls playsinline preload="none" poster="/bathroom-walnut-vanity-after.jpg" aria-label="Video showing shower enclosure installation and completed bathroom fixtures"><source src="/bathroom-finish-details.mp4" type="video/mp4">Your browser does not support embedded video.</video><figcaption><strong>Installation &amp; finish details</strong><span>Glass-enclosure work followed by the finished vanity and fixture details.</span></figcaption></figure>
      </div></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("How the work connects", "A conversion is more than swapping one fixture.", "Demolition, access, water management and final fitting have to be planned as one sequence.")}<div class="proof-grid story-step-grid"><article class="proof-card reveal"><h3>Document the room</h3><p>Confirm what remains, what comes out and how the new shower fits the existing footprint.</p></article><article class="proof-card reveal"><h3>Open carefully</h3><p>Remove the tub platform and expose the wall and floor only where the new work requires access.</p></article><article class="proof-card reveal"><h3>Build the wet area</h3><p>Prepare the shower assembly, waterproofing, tile and plumbing connections in the correct order.</p></article><article class="proof-card reveal"><h3>Complete the room</h3><p>Fit the glass enclosure and reconnect trim, fixtures and surrounding finishes cleanly.</p></article></div></div></section>
      <section class="section section-paper"><div class="wrap">{section_heading("Related services", "Bathroom work often crosses several scopes.", "Flooring, drywall and fixture work can be reviewed as part of the same renovation.")}<div class="service-grid related-grid">{service_card("bathrooms", compact=True, variant=3)}{service_card("flooring", compact=True, variant=2)}{service_card("drywall-ceiling-repair", compact=True, variant=3)}</div></div></section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">Considering a tub-to-shower conversion?</p><h2>Show us the whole bathroom.</h2><p>Wide photos, the existing fixtures and what you want to change are enough to start the conversation.</p></div><div><a class="button button-primary" href="/contact/#quote">Request a Quote</a><a class="cta-phone" href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a></div></div></section>
    </main>"""
    return page("Tub-to-Shower Bathroom Transformation | Hekman", "See a real jetted-tub-to-shower bathroom renovation by Hekman Home Services, documented from demolition and open-wall work through the finished glass shower.", "/projects/glass-block-bathroom-conversion/", "bathroom-walnut-vanity-after.jpg", "projects", body, "project-story-page")
def projects_page() -> str:
    priority = {src: index for index, src in enumerate(PROJECT_GALLERY_PRIORITY)}
    ordered_projects = sorted(PROJECTS, key=lambda item: priority.get(item[0], len(PROJECTS)))
    cards = "".join(f'<figure class="project-card reveal" data-category="{categories}"><button class="project-image" type="button" data-lightbox aria-label="Enlarge {html.escape(label, quote=True)}"><img src="/{src}" alt="{html.escape(alt, quote=True)}" loading="lazy" decoding="async"></button><figcaption><span>{label}</span><small>{tag}</small></figcaption></figure>' for src, categories, alt, label, tag in ordered_projects)
    filters = [("all", "All"), ("kitchens", "Kitchens"), ("bathrooms", "Bathrooms"), ("basements", "Basements"), ("restoration", "Restoration"), ("exterior", "Exterior"), ("commercial", "Commercial"), ("handyman", "Repairs"), ("more", "More")]
    buttons = "".join(f'<button type="button" class="filter-button{" active" if key == "all" else ""}" data-filter="{key}" aria-pressed="{"true" if key == "all" else "false"}">{label}</button>' for key, label in filters)
    body = f"""
    {hero("hilltop-kitchen-wide.jpg", "Completed Hilltop kitchen renovation", "Our work · London, Ontario", "Work that holds up to a closer look", "Explore carefully documented renovations, repairs and restorations from neighbourhoods across London—finished spaces, honest progress and the decisions that connect them.", small=True, position="50% 54%")}
    <main id="main">
      <section class="section section-paper"><div class="wrap">{section_heading("Project stories", "Six transformations worth exploring in detail", "Explore the original challenge, the decisions behind the work and the completed result in each project story.")}
        <div class="story-card-grid">
          <a class="story-card story-card-large reveal" href="/projects/melrose-bathroom-layout/"><img src="/melrose-bathroom-after.jpg" alt="Completed Melrose-area bathroom with tiled shower, wall-hung toilet and illuminated mirror" loading="lazy"><span><small>Melrose area · completed</small><strong>A bathroom reworked from the layout out</strong><b>Bathroom relocation, new utility room and a finished exercise space <i aria-hidden="true">↗</i></b></span></a>
          <a class="story-card reveal" href="/projects/hyde-park-kitchen-renewal/"><img src="/hyde-park-kitchen-after.jpg" alt="Completed Hyde Park kitchen with refaced cabinetry, new counters, sink and backsplash" loading="lazy"><span><small>Hyde Park · completed</small><strong>Renewed without starting over</strong><b>Cabinet refacing, pantry, appliance flow, dishwasher and new surfaces <i aria-hidden="true">↗</i></b></span></a>
          <a class="story-card reveal" href="/projects/medway-flooring-storage/"><img src="/medway-finished-room.jpg" alt="Completed Medway room with cool gray-brown plank flooring and finished baseboards" loading="lazy"><span><small>Medway · completed</small><strong>More storage and better flow</strong><b>Three rooms, relocated closets, flooring, doors and trim <i aria-hidden="true">↗</i></b></span></a>
          <a class="story-card reveal" href="/projects/hilltop-home-transformation/"><img src="/hilltop-kitchen-angle.jpg" alt="Completed Hilltop kitchen" loading="lazy"><span><small>Hilltop · completed</small><strong>A home transformed room by room</strong><b>Kitchen, bathrooms, lower level, stairs and connected details <i aria-hidden="true">↗</i></b></span></a>
          <a class="story-card reveal" href="/projects/westmount-porch-entry/"><img src="/westmount-porch-after-night.jpg" alt="Finished Westmount porch and entry illuminated at night" loading="lazy"><span><small>Westmount · completed</small><strong>A modernized porch for a repeat neighbour</strong><b>Exterior repairs, finish work, cleaner lines and lighting <i aria-hidden="true">↗</i></b></span></a>
          <a class="story-card story-card-wide reveal" href="/projects/commercial-salon-repair/"><img src="/salon-restored-wall.jpg" alt="Completed wall and ceiling restoration in an anonymous London salon" loading="lazy"><span><small>London · completed commercial restoration</small><strong>A working salon restored from the construction out</strong><b>Moisture investigation, affected-material removal, wall and ceiling repairs <i aria-hidden="true">↗</i></b></span></a>
        </div>
        <div class="project-archive reveal">
          <div><p class="eyebrow">More documented work</p><h3>More ways a project can take shape</h3></div>
          <div class="project-archive-grid">
            <a href="/projects/pond-mills-home-repairs/"><span>Pond Mills · completed</span><strong>A repair list, re-examined</strong><b>Flooring, interior repairs and connected exterior water management <i aria-hidden="true">↗</i></b></a>
            <a href="/projects/multi-unit-deck-renewal/"><span>London area · completed exterior</span><strong>Deck renewal across the row</strong><b>Weathered starting point, open construction and completed elevations <i aria-hidden="true">↗</i></b></a>
            <a href="/projects/westmount-1970s-transformation/"><span>Westmount · project in progress</span><strong>A home transformed in phases</strong><b>Layout, lighting, flooring and kitchen work completed in thoughtful stages <i aria-hidden="true">↗</i></b></a>
            <a href="/projects/popcorn-ceiling-transformation/"><span>London · ceiling transformation</span><strong>Texture removed, surface rebuilt</strong><b>Protection, sanding, skim coating and primer <i aria-hidden="true">↗</i></b></a>
          </div>
        </div>
      </div></section>
      <section class="section section-stone"><div class="wrap">{section_heading("Short project walkthroughs", "See the work in motion", "Two brief walkthroughs show how the spaces changed, from work underway to the completed result.")}<div class="video-grid"><figure class="work-video reveal"><video controls playsinline preload="none" poster="/melrose-bathroom-after.jpg" aria-label="Short walkthrough of the completed Melrose-area bathroom"><source src="/melrose-bathroom-tour.mp4" type="video/mp4">Your browser does not support embedded video.</video><figcaption><strong>Melrose bathroom walkthrough</strong><span>A six-second look at the finished vanity, shower and wall-hung toilet</span></figcaption></figure><figure class="work-video reveal"><video controls playsinline preload="none" poster="/bathroom-walnut-vanity-after.jpg" aria-label="Video of a jetted-tub bathroom being converted into a glass shower"><source src="/bathroom-glass-block-transformation.mp4" type="video/mp4">Your browser does not support embedded video.</video><figcaption><strong>Tub-to-shower transformation</strong><span>Demolition, open-wall work and the completed glass shower</span></figcaption></figure></div></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("Project gallery", "Start with the strongest results, then explore the work behind them", "Choose a project type or load more photographs to browse renovations, restorative repairs, exterior work and commercial projects across London.")}<div class="filter-bar" aria-label="Filter project photographs">{buttons}</div><div class="projects-grid" id="projects-grid" aria-live="polite">{cards}</div><p class="filter-status" data-filter-status>Showing 18 of {len(PROJECTS)} photographs.</p><div class="gallery-actions"><button type="button" class="button button-primary" data-load-more>Load more photographs</button></div></div></section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">Picture your own project?</p><h2>Bring us the room, repair or result you have in mind.</h2><p>Send a few photos—no detailed plans required. Tell us what you want to change or restore, and we will help connect the scope.</p></div><div><a class="button button-primary" href="/contact/#quote">Tell Us About Your Project</a><a class="cta-phone" href="tel:{PHONE_LINK}">Call or text {PHONE_DISPLAY}</a></div></div></section>
      <dialog class="lightbox" data-lightbox-dialog><button type="button" class="lightbox-close" data-lightbox-close aria-label="Close image">×</button><img alt="Selected project photograph"><p></p></dialog>
    </main>"""
    return page("Renovation Projects London ON | Hekman", "Explore genuine, carefully curated renovation, flooring, storage, porch, restoration and commercial project stories by Hekman Home Services in London, Ontario.", "/projects/", "hilltop-kitchen-wide.jpg", "projects", body, "projects-page", image_alt="Completed Hilltop kitchen renovation by Hekman Home Services")
def about_page() -> str:
    body = f"""
    {hero("rene-steph-owner-led.jpg", "Rene and Steph Hekman together, with Rene wearing his tool belt", "About Hekman Home Services", "The people behind the work.", "Together, Rene and Steph connect 25 years of construction experience with 20 years of sales and client service—and stay close to every project.", small=True, position="62% 18%")}
    <main id="main">
      <section class="section section-paper"><div class="wrap editorial-grid about-story"><div class="editorial-copy reveal"><p class="eyebrow">The Hekman approach</p><h2>The people you call stay connected to the work.</h2><p>Hekman Home Services is owned and operated by Rene and Steph Hekman. Rene leads construction in the field. Steph leads customer communication, sales, project planning and design ideas, with close attention to the small details that matter to each customer. Together they connect what is discovered on site with the choices, scope and updates that keep the project moving.</p><p>Steph’s construction knowledge also comes from lived experience. She worked alongside Rene as they gutted and renovated every space in their Hilltop home, learning how design choices, sequencing, budget and day-to-day life connect during a whole-home transformation.</p><p>That direct involvement matters when one visible issue turns out to affect a wall, a floor or the room beside it. Decisions are explained in context, approved before extras proceed and carried through to the final details.</p></div><div class="editorial-media reveal"><img src="/rene-steph-london-ontario.jpg" alt="Rene and Steph Hekman standing together beside the London Canada sign" loading="lazy"><span>Rene &amp; Steph Hekman · London, Ontario</span></div></div></section>
      <section class="section section-charcoal" id="hekman-promise"><div class="wrap">{section_heading("The Hekman Promise", "Clear expectations before the work. Direct accountability throughout it.", "This is the standard written into our project quotes—not a slogan added after the fact.")}<div class="values-grid"><article class="reveal"><h3>Honest advice &amp; transparent pricing</h3><p>The scope, allowances and assumptions are explained so you can make informed decisions.</p></article><article class="reveal"><h3>Respect for your property</h3><p>Protection, an organized job site, debris removal and final cleanup are part of professional workmanship.</p></article><article class="reveal"><h3>Approval before additional work</h3><p>If you request a change or a concealed condition affects the plan, the options are discussed and approved before work proceeds.</p></article><article class="reveal"><h3>A two-year workmanship guarantee</h3><p>Installation-related defects resulting from our workmanship are covered for two years from completion.</p></article></div></div></section>
      <section class="section section-stone"><div class="wrap people-grid"><article class="person-card reveal"><img src="/project-075.jpg" alt="Rene Hekman, Director and Contractor at Hekman Home Services" loading="lazy"><div><p class="eyebrow">Director · Contractor</p><h2>Rene Hekman</h2><p>Rene brings 25 years of construction experience and leads the work in the field—from opening walls and understanding repair conditions to the preparation and finish details that make a renovation hold together.</p><ul class="person-facts"><li><strong>25 years in construction</strong><span>Hands-on renovation, repair and problem-solving experience.</span></li><li><strong>Home-inspection education</strong><span>Completed home-inspection education through Carson Dunlop in 2022. Rene has not practised as a home inspector, and Hekman Home Services does not provide home inspections or inspection reports. Real estate professionals ask him for a contractor’s perspective on visible renovation and repair concerns.</span></li><li><strong>Horticultural Technician</strong><span>Graduate of Humber College’s Horticultural Technician program, bringing added knowledge to exterior and landscape-related work.</span></li></ul></div></article><article class="person-card reveal"><img src="/project-076.jpg" alt="Steph Hekman, Customer Relations, Sales and Design at Hekman Home Services" loading="lazy"><div><p class="eyebrow">Customer Relations · Sales &amp; Design</p><h2>Steph Hekman</h2><p>Steph brings 20 years of sales and client-service experience, a strong eye for design and genuine attention to the small details that matter to each customer. She listens for what people are trying to achieve, offers practical ideas and keeps goals, scope and next steps connected.</p><ul class="person-facts"><li><strong>20 years in sales</strong><span>Careful listening, clear communication and a strong instinct for the customer experience.</span></li><li><strong>Hands-on renovation learning</strong><span>Steph worked alongside Rene as they gutted and renovated every space in their Hilltop home, gaining a practical understanding of construction sequencing and design decisions.</span></li><li><strong>Design perspective</strong><span>She contributes ideas for layout, flow, finish choices and the small details that help a space feel intentional and personal to the customer.</span></li><li><strong>Real estate background</strong><span>Steph has been a registered real estate salesperson since 2010. That experience adds another practical perspective on how homeowners weigh function, investment and future plans, while Hekman Home Services remains focused on construction.</span></li></ul></div></article></div></section>
      <section class="section section-paper"><div class="wrap area-layout"><div class="reveal"><p class="eyebrow">Local service</p><h2>Based in Westmount. Serving London &amp; St. Thomas.</h2><p><strong>Westmount, Byron, Oakridge, Riverbend, Hyde Park and beyond.</strong> We work with homeowners and property managers throughout London, in St. Thomas and in nearby communities.</p><a class="button button-dark" href="/contact/">Contact Rene &amp; Steph</a></div><div class="assurance-panel reveal"><strong>Fully insured &amp; bondable</strong><span>Professional protection for residential and commercial projects.</span><strong>25 years of construction experience</strong><span>Rene brings practical renovation and repair knowledge directly to the work.</span><strong>20 years of client service</strong><span>Steph brings careful listening, practical ideas and attention to customer details.</span></div></div></section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">Have a room or repair in mind?</p><h2>Start with a few photos.</h2><p>No detailed plans required. Show us the space and tell us what you want to change, repair or create.</p></div><div><a class="button button-primary" href="/contact/#quote">Tell Us About Your Project</a><a class="cta-phone" href="tel:{PHONE_LINK}">Call or text {PHONE_DISPLAY}</a></div></div></section>
    </main>"""
    return page("About Rene & Steph Hekman | Hekman Home Services", "Meet Rene and Steph Hekman, bringing 25 years of construction and 20 years of sales experience to renovations and repairs across London and St. Thomas.", "/about/", "rene-steph-owner-led.jpg", "about", body, "about-page", image_alt="Rene and Steph Hekman together, with Rene wearing his tool belt")
def build() -> None:
    write("index.html", homepage())
    write("services/index.html", services_page())
    for slug in SERVICES:
        write(f"services/{slug}/index.html", service_page(slug))
    write("projects/index.html", projects_page())
    write("projects/melrose-bathroom-layout/index.html", melrose_project_page())
    write("projects/hyde-park-kitchen-renewal/index.html", hyde_park_kitchen_project_page())
    write("projects/blackfriars-leak-restoration/index.html", blackfriars_project_page())
    write("projects/hilltop-home-transformation/index.html", hilltop_project_page())
    write("projects/medway-flooring-storage/index.html", medway_project_page())
    write("projects/westmount-porch-entry/index.html", westmount_porch_project_page())
    write("projects/westmount-1970s-transformation/index.html", westmount_project_page())
    write("projects/commercial-salon-repair/index.html", salon_project_page())
    write("projects/pond-mills-home-repairs/index.html", pond_mills_project_page())
    write("projects/multi-unit-deck-renewal/index.html", multi_unit_deck_project_page())
    write("projects/kitchen-renewal/index.html", kitchen_renewal_project_page())
    write("projects/popcorn-ceiling-transformation/index.html", popcorn_project_page())
    write("projects/glass-block-bathroom-conversion/index.html", glass_block_bathroom_project_page())
    write("about/index.html", about_page())
    write("contact/index.html", contact_page(SERVICES=SERVICES, SERVICE_DISPLAY_ORDER=SERVICE_DISPLAY_ORDER, hero=hero, PHONE_LINK=PHONE_LINK, PHONE_DISPLAY=PHONE_DISPLAY, EMAIL=EMAIL, section_heading=section_heading, page=page))
    write("404.html", not_found_page(page=page))
    legacy = {
        "services.html": ("/services/", "Services | Hekman Home Services"),
        "projects.html": ("/projects/", "Our Work | Hekman Home Services"),
        "about.html": ("/about/", "About | Hekman Home Services"),
        "contact.html": ("/contact/", "Contact | Hekman Home Services"),
        "bathrooms.html": ("/services/bathrooms/", "Bathroom Renovations | Hekman Home Services"),
        "kitchens.html": ("/services/kitchens/", "Kitchen Renovations | Hekman Home Services"),
        "basements.html": ("/services/basements/", "Basement Renovations | Hekman Home Services"),
        "flooring.html": ("/services/flooring/", "Flooring | Hekman Home Services"),
        "drywall-popcorn.html": ("/services/drywall-ceiling-repair/", "Drywall & Ceiling Repair | Hekman Home Services"),
        "decks.html": ("/services/decks-exterior/", "Decks & Exterior | Hekman Home Services"),
        "water-damage.html": ("/services/water-damage/", "Water Damage Repairs | Hekman Home Services"),
        "commercial.html": ("/services/commercial/", "Commercial Maintenance | Hekman Home Services"),
        "handyman.html": ("/services/handyman-repairs/", "Handyman & Home Repairs | Hekman Home Services"),
        "structural-layout.html": ("/services/structural-layout/", "Structural & Layout Changes | Hekman Home Services"),
    }
    for filename, (destination, title) in legacy.items():
        write(filename, redirect_stub(destination, title, BASE_URL=BASE_URL))
    write("reviews/index.html", redirect_stub("/projects/", "Our Work | Hekman Home Services", BASE_URL=BASE_URL))
    project_urls = list(PROJECT_DETAILS)
    urls = ["/", "/services/", *[service_url(slug) for slug in SERVICES], "/projects/", *project_urls, "/about/", "/contact/"]
    sitemap_urls = "\n".join(f"  <url><loc>{BASE_URL}{url}</loc></url>" for url in urls)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sitemap_urls}\n</urlset>')
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml")
    write("llms.txt", llms_text(BASE_URL, PHONE_DISPLAY, EMAIL, SERVICES, service_url, INSTAGRAM, FACEBOOK))


if __name__ == "__main__":
    build()
