#!/usr/bin/env python3
"""Build the static Hekman Home Services website.

The repository intentionally keeps its curated project photography at the root.
This script only writes maintainable HTML, CSS-adjacent assets, and route files;
it never deletes, renames, or rewrites project images.
"""

from __future__ import annotations

import html
import json
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://hhs-site-v1.vercel.app"
PHONE_DISPLAY = "519-808-3312"
PHONE_LINK = "+15198083312"
EMAIL = "hekmanhomeservices@gmail.com"

AREAS = [
    "London, Ontario",
    "Westmount",
    "Byron",
    "Oakridge",
    "Riverbend",
    "Masonville",
    "Old South",
    "Hyde Park",
    "St. Thomas",
]

SERVICES: dict[str, dict] = {
    "bathrooms": {
        "name": "Bathroom Renovations",
        "card_name": "Bathrooms",
        "title": "Bathroom Renovations London ON | Hekman Home Services",
        "description": "Bathroom renovations in London, Ontario, including tile, waterproofing, vanities, fixtures, heated floors and tub-to-shower updates.",
        "hero": "project-148.jpg",
        "hero_alt": "Completed glass shower and bathroom renovation",
        "position": "50% 58%",
        "lead": "Create a bathroom that works better every day—with careful preparation behind every visible finish.",
        "intro": "A successful bathroom renovation balances layout, water management, storage and finish details. We review the existing room, talk through priorities and build a clear scope around the condition of the space.",
        "scope": [
            ("Preparation & waterproofing", "Shower systems, substrate preparation and waterproofing are planned before tile and fixtures go in."),
            ("Tile & heated floors", "Wall tile, floor tile and heated-floor options can be coordinated into the room."),
            ("Fixtures & finish work", "Vanities, faucets, toilets, lighting, trim and paint-ready surfaces bring the room together."),
        ],
        "bullets": ["Full bathroom renovations", "Tub-to-shower conversions", "Shower and tub surrounds", "Tile and grout work", "Vanities, fixtures and storage", "Flooring, trim and finishing"],
        "gallery": [
            ("project-148.jpg", "Completed bathroom with glass shower enclosure", "Glass shower renovation"),
            ("project-157.jpg", "Completed bathroom vanity and mirror", "Vanity and finish work"),
            ("project-161.jpg", "Completed bathroom with wood vanity", "Finished bathroom"),
            ("project-160.jpg", "Bathroom waterproofing system during construction", "Waterproofing in progress"),
        ],
        "faq": [
            ("Can you renovate the entire bathroom?", "Yes. Depending on the project, the scope can include demolition, preparation, waterproofing, tile, vanity, fixtures, flooring, trim and finishing."),
            ("Do you complete tub-to-shower conversions?", "Yes. The existing plumbing, structure and room layout are reviewed before the conversion is quoted."),
            ("Can heated flooring be included?", "Heated flooring can be considered where the floor system and overall project scope support it."),
        ],
        "related": ["kitchens", "flooring", "water-damage"],
    },
    "kitchens": {
        "name": "Kitchen Renovations",
        "card_name": "Kitchens",
        "title": "Kitchen Renovations London ON | Hekman Home Services",
        "description": "Kitchen renovations and upgrades in London, Ontario, including cabinet installation, backsplash, layout improvements and finish carpentry.",
        "hero": "project-132.jpg",
        "hero_alt": "Completed bright white kitchen renovation",
        "position": "50% 52%",
        "lead": "Improve the heart of the home with a kitchen planned around storage, flow and the way your household lives.",
        "intro": "Kitchen work often connects cabinetry, walls, flooring, tile and finishing. We look at the full room so the new elements feel integrated rather than added one at a time.",
        "scope": [
            ("Cabinets & layout", "Cabinet installation and practical layout changes can make better use of the available room."),
            ("Backsplash & surfaces", "Tile, wall repair and finishing help counters, cabinets and appliances sit cleanly together."),
            ("Final details", "Trim, hardware, transitions and touch-ups give the renovation a complete finish."),
        ],
        "bullets": ["Kitchen renovations and updates", "Cabinet assembly and installation", "Backsplash installation", "Layout and opening changes", "Drywall and finish repairs", "Trim and finishing details"],
        "gallery": [
            ("project-132.jpg", "Completed white kitchen with island seating", "Finished kitchen"),
            ("project-133.jpg", "Completed white kitchen cabinetry and appliances", "Cabinet installation"),
            ("project-131.jpg", "Kitchen sink and backsplash detail", "Sink and backsplash detail"),
            ("project-136.jpg", "Kitchen island drawers and countertop detail", "Island finish work"),
        ],
        "faq": [
            ("Do you install customer-supplied cabinets?", "Cabinet installation can be included after the cabinet system, measurements and site conditions are reviewed."),
            ("Can you update a kitchen without changing everything?", "Yes. A project can focus on cabinets, backsplash, flooring, repairs or finishing without requiring a full layout change."),
            ("Can you complete the work around cabinets and counters?", "Drywall repair, backsplash, trim and other finish work can be coordinated as part of the project scope."),
        ],
        "related": ["structural-layout", "flooring", "drywall-ceiling-repair"],
    },
    "basements": {
        "name": "Basement Renovations",
        "card_name": "Basements",
        "title": "Basement Renovations London ON | Hekman Home Services",
        "description": "Basement renovations in London, Ontario, including framing, drywall, ceilings, flooring, trim, storage and finished living spaces.",
        "hero": "project-067.jpg",
        "hero_alt": "Completed basement renovation with warm flooring",
        "position": "50% 60%",
        "lead": "Turn an unfinished or underused lower level into comfortable space that supports how your household lives.",
        "intro": "Basements can become family rooms, work areas, storage, guest space or a combination of uses. We help connect layout, surfaces and finishing into one practical renovation scope.",
        "scope": [
            ("Layout & framing", "Shape the lower level around living space, storage and the rooms the property needs."),
            ("Walls & ceilings", "Drywall, repairs and ceiling finishing move the space from rough construction to a clean interior."),
            ("Flooring & trim", "Flooring, doors, baseboards and transitions connect the basement with the rest of the home."),
        ],
        "bullets": ["Basement finishing", "Framing and room layouts", "Drywall and ceiling work", "Flooring installation", "Doors, trim and storage", "Focused basement repairs"],
        "gallery": [
            ("project-067.jpg", "Finished basement with warm wood flooring", "Finished living space"),
            ("project-068.jpg", "Finished basement room with lighting", "Basement finish work"),
            ("project-066.jpg", "Finished basement staircase and railing", "Stair and railing detail"),
            ("project-063.jpg", "Finished lower-level entry with tile floor", "Flooring and transition"),
        ],
        "faq": [
            ("Can you finish an unfinished basement?", "Basement scopes can include framing, drywall, flooring, doors, trim and other finish work, subject to existing conditions and permit requirements."),
            ("Can a bathroom or kitchenette be included?", "Those features can be considered when plumbing, electrical and permit requirements are addressed in the project plan."),
            ("Do you take on partial basement projects?", "Yes. Work can focus on one room, flooring, ceilings, storage or another specific improvement."),
        ],
        "related": ["flooring", "drywall-ceiling-repair", "structural-layout"],
    },
    "flooring": {
        "name": "Flooring Installation",
        "card_name": "Flooring",
        "title": "Flooring Installation London ON | Hekman Home Services",
        "description": "Flooring installation in London, Ontario, including vinyl plank, laminate, subfloor preparation, transitions, doors and trim.",
        "hero": "project-072.jpg",
        "hero_alt": "Completed plank flooring installation in a renovated room",
        "position": "50% 60%",
        "lead": "A better floor starts with the surface underneath and ends with clean transitions, trim and details.",
        "intro": "Flooring changes the feel of an entire room. We review the existing floor, movement between rooms and the finish details needed at walls, doors, stairs and adjoining surfaces.",
        "scope": [
            ("Preparation", "Existing flooring, subfloor conditions and room transitions are reviewed before installation."),
            ("Installation", "Vinyl plank, laminate and other selected flooring are laid out for a consistent finished appearance."),
            ("Trim & transitions", "Baseboards, nosings, thresholds and doorway details complete the installation."),
        ],
        "bullets": ["Vinyl plank and laminate", "Subfloor preparation", "Flooring removal and replacement", "Transitions and thresholds", "Stair and landing details", "Baseboards and finish trim"],
        "gallery": [
            ("project-072.jpg", "New plank flooring in a finished room", "Plank flooring installation"),
            ("project-063.jpg", "Tile flooring at a bright patio entry", "Tile and transition work"),
            ("project-042.jpg", "New flooring installed through a kitchen", "Kitchen flooring"),
            ("project-066.jpg", "Finished staircase with wood treads", "Stair finish detail"),
        ],
        "faq": [
            ("Do you remove the existing floor?", "Removal and disposal can be included where needed and will be identified in the quote."),
            ("Can you repair the subfloor first?", "Visible subfloor concerns can be reviewed and included in the scope before the finished flooring is installed."),
            ("Do you complete baseboards and transitions?", "Yes. Trim, thresholds and transitions can be included so the room feels finished."),
        ],
        "related": ["basements", "kitchens", "water-damage"],
    },
    "drywall-ceiling-repair": {
        "name": "Drywall & Ceiling Repair",
        "card_name": "Drywall & Ceilings",
        "title": "Drywall & Ceiling Repair London ON | Hekman Home Services",
        "description": "Drywall and ceiling repair in London, Ontario, including patches, replacement, taping, mudding, sanding and paint-ready finishes.",
        "hero": "project-014.jpg",
        "hero_alt": "Smooth repaired ceiling in a finished room",
        "position": "50% 58%",
        "lead": "Repair damaged walls and ceilings with careful preparation and a smooth, paint-ready finish.",
        "intro": "Good drywall work should disappear into the room. We assess the damaged area, remove loose or affected material where needed and build the finish in controlled stages.",
        "scope": [
            ("Open & assess", "The damaged area is reviewed so loose material and the repair boundary can be handled properly."),
            ("Patch & finish", "New board, tape and compound are applied in the stages required for the repair."),
            ("Prepare for paint", "Sanding and final touch-ups create a clean surface for primer and paint."),
        ],
        "bullets": ["Wall and ceiling patches", "Drywall replacement", "Taping and mudding", "Ceiling repairs", "Repairs after plumbing or electrical work", "Primer and paint-ready finishing"],
        "gallery": [
            ("project-011.jpg", "Drywall finishing in progress on walls and ceiling", "Finishing in progress"),
            ("project-015.jpg", "Ceiling patch and compound work", "Ceiling repair"),
            ("project-014.jpg", "Completed smooth ceiling in a finished room", "Completed ceiling"),
            ("project-010.jpg", "Protected room prepared for drywall finishing", "Room protection and preparation"),
        ],
        "faq": [
            ("Can you repair damage after another trade opens a wall?", "Yes. Openings left after plumbing, electrical or other repair work can be reviewed for patching and finishing."),
            ("Will the repair be ready for paint?", "The quote will identify whether the scope ends at a sanded, paint-ready finish or includes primer and paint."),
            ("Can several patches be completed together?", "Yes. Multiple repair areas can often be grouped into one project after they are reviewed."),
        ],
        "related": ["popcorn-ceiling-removal", "water-damage", "basements"],
    },
    "popcorn-ceiling-removal": {
        "name": "Popcorn Ceiling Removal",
        "card_name": "Popcorn Ceilings",
        "title": "Popcorn Ceiling Removal London ON | Hekman Home Services",
        "description": "Popcorn ceiling removal in London, Ontario, with preparation, scraping, skim coating, sanding and smooth ceiling finishing.",
        "hero": "project-015.jpg",
        "hero_alt": "Ceiling being prepared for a smooth finished surface",
        "position": "50% 42%",
        "lead": "Replace a dated textured ceiling with a cleaner, brighter surface that changes the feel of the whole room.",
        "intro": "Removing ceiling texture is a preparation-heavy project. The room is protected, the existing surface is assessed and the ceiling is finished through the stages needed for a smooth result.",
        "scope": [
            ("Protect the room", "Floors, walls and fixed items are covered before ceiling work begins."),
            ("Remove & skim", "Texture is removed where appropriate and the surface is repaired or skim coated as required."),
            ("Sand & finish", "The ceiling is sanded and checked before the agreed primer or paint finish is completed."),
        ],
        "bullets": ["Popcorn ceiling removal", "Room and floor protection", "Ceiling repairs", "Skim coating", "Sanding and smoothing", "Primer and paint options"],
        "gallery": [
            ("project-007.jpg", "Ceiling texture removal and finishing in progress", "Ceiling work in progress"),
            ("project-011.jpg", "Walls and ceiling being skim coated", "Skim coating"),
            ("project-016.jpg", "Ceiling compound drying before sanding", "Surface preparation"),
            ("project-014.jpg", "Smooth finished ceiling in a completed room", "Smooth finished ceiling"),
        ],
        "faq": [
            ("Does every textured ceiling come off the same way?", "No. Paint, previous repairs and the underlying surface can change the removal and finishing process."),
            ("How is the room protected?", "The required floor, wall and fixture protection is planned as part of the project scope."),
            ("Can the ceiling be primed and painted too?", "Yes. Primer and paint can be included so the ceiling is fully finished."),
        ],
        "related": ["drywall-ceiling-repair", "basements", "water-damage"],
    },
    "decks-exterior": {
        "name": "Decks & Exterior Work",
        "card_name": "Decks & Exterior",
        "title": "Decks & Exterior Work London ON | Hekman Home Services",
        "description": "Deck construction, railings, fences and exterior repair services in London, Ontario and surrounding communities.",
        "hero": "project-103.jpg",
        "hero_alt": "Completed elevated wood deck at a residential property",
        "position": "50% 52%",
        "lead": "Build, repair or improve outdoor spaces with attention to structure, safe access and a clean exterior finish.",
        "intro": "Exterior work has to respond to weather, existing structure and how people use the property. We review access, site conditions and the full repair or construction scope before work begins.",
        "scope": [
            ("Deck structures", "New construction and replacement work are planned around the property, access and required approvals."),
            ("Railings & stairs", "Steps, guards, railings and transitions are considered as part of safe everyday use."),
            ("Exterior repairs", "Posts, trim, cladding details and focused exterior repairs can be grouped into a practical scope."),
        ],
        "bullets": ["Deck construction and replacement", "Deck repairs", "Stairs and landings", "Railings and guards", "Fence and exterior carpentry", "Posts, trim and focused repairs"],
        "gallery": [
            ("project-103.jpg", "Completed elevated deck behind a brick home", "Completed deck"),
            ("project-104.jpg", "Long completed residential deck structure", "Multi-unit exterior work"),
            ("project-101.jpg", "Deck framing and support structure", "Deck structure"),
            ("project-100.jpg", "Wood deck and railing at a residential property", "Deck and railing"),
        ],
        "faq": [
            ("Do deck projects require permits?", "Some do. Requirements depend on height, size, attachment and local rules. Permit needs are identified during planning."),
            ("Can you replace railings or stairs without replacing the whole deck?", "Focused repairs or replacements can be considered after the existing structure is assessed."),
            ("Do you complete exterior repair lists?", "Yes. Multiple compatible exterior items can be reviewed and grouped into one quote."),
        ],
        "related": ["structural-layout", "water-damage", "commercial"],
    },
    "water-damage": {
        "name": "Water Damage Repairs",
        "card_name": "Water Damage",
        "title": "Water Damage Repairs London ON | Hekman Home Services",
        "description": "Repair and rebuilding after water damage in London, Ontario, including drywall, ceilings, flooring, trim and finish work.",
        "hero": "project-012.jpg",
        "hero_alt": "Contractors rebuilding drywall after interior damage",
        "position": "50% 45%",
        "lead": "Once the source of the water is corrected, rebuild damaged walls, ceilings, floors and finishes with one coordinated scope.",
        "intro": "A leak can affect several materials beyond the point where water first appears. We focus on the repair and rebuilding work after the source has been identified and addressed.",
        "scope": [
            ("Remove damaged finishes", "Affected drywall, ceiling material, flooring or trim can be opened or removed as the repair requires."),
            ("Rebuild surfaces", "Damaged materials are replaced and finished back toward a complete wall, ceiling or floor."),
            ("Reconnect the room", "Trim, transitions and paint-ready surfaces help the repaired area fit back into the surrounding space."),
        ],
        "bullets": ["Drywall and ceiling rebuilding", "Flooring replacement", "Trim and baseboard repair", "Repairs after leak correction", "Multi-surface restoration", "Primer, paint and finish options"],
        "gallery": [
            ("project-012.jpg", "Drywall rebuilding in progress", "Rebuilding in progress"),
            ("project-013.jpg", "Protected room during wall repair", "Protected repair area"),
            ("project-015.jpg", "Ceiling patches during repair work", "Ceiling repair"),
            ("project-014.jpg", "Finished room after ceiling work", "Finished surface"),
        ],
        "faq": [
            ("Do you stop the active leak?", "The source should be identified and corrected first. Our scope can focus on removal, repair and rebuilding afterward."),
            ("Can drywall and flooring be repaired together?", "Yes. One quote can include several affected finishes where appropriate."),
            ("Can you review an insurance repair scope?", "We can review the requested work and prepare our own quote based on the actual site conditions and repair scope."),
        ],
        "related": ["drywall-ceiling-repair", "flooring", "bathrooms"],
    },
    "commercial": {
        "name": "Commercial Maintenance & Repairs",
        "card_name": "Commercial Work",
        "title": "Commercial Maintenance London ON | Hekman Home Services",
        "description": "Commercial maintenance and repairs in London, Ontario, including drywall, lighting-related finish work, tenant improvements and property repairs.",
        "hero": "project-050.jpg",
        "hero_alt": "Completed commercial interior after maintenance work",
        "position": "50% 54%",
        "lead": "Practical repairs and improvements for offices, retail, fitness, rental and other commercial properties.",
        "intro": "Commercial spaces need repairs completed with clear scope, site awareness and respect for operations. Work can be planned as one project or as a grouped maintenance list.",
        "scope": [
            ("Repair lists", "Drywall, trim, doors, fixtures and other compatible items can be grouped into one scope."),
            ("Tenant improvements", "Finish updates and layout-related work can support a new or refreshed business space."),
            ("Property maintenance", "Owners and managers can consolidate several repair needs into a practical project quote."),
        ],
        "bullets": ["Commercial drywall and repairs", "Lighting-related ceiling repairs", "Tenant improvement work", "Doors, trim and finish repairs", "Grouped maintenance lists", "Rental and property repairs"],
        "gallery": [
            ("project-050.jpg", "Commercial interior after maintenance work", "Completed commercial space"),
            ("project-046.jpg", "Commercial fitness space with upgraded lighting", "Commercial lighting finish"),
            ("project-049.jpg", "Commercial ceiling work in progress", "Ceiling work in progress"),
            ("project-054.jpg", "Finished commercial interior", "Finished workspace"),
        ],
        "faq": [
            ("Do you work in occupied commercial spaces?", "Yes, when the scope, access and scheduling requirements make it practical. We discuss ways to reduce disruption."),
            ("Can several small repairs be grouped together?", "Yes. Grouping compatible maintenance items can make the work more efficient."),
            ("Do you work with landlords and property managers?", "Commercial and rental-property repair work can be quoted for owners and managers."),
        ],
        "related": ["drywall-ceiling-repair", "structural-layout", "water-damage"],
    },
    "structural-layout": {
        "name": "Structural & Layout Changes",
        "card_name": "Structural & Layout",
        "title": "Structural & Layout Changes London ON | Hekman Home Services",
        "description": "Framing, wall openings, closet builds and layout changes for renovation projects in London, Ontario.",
        "hero": "project-025.jpg",
        "hero_alt": "Interior wall framing exposed during a layout renovation",
        "position": "50% 50%",
        "lead": "Change how rooms connect, improve storage and make an existing layout work better for everyday life.",
        "intro": "Layout work often affects framing, drywall, flooring and adjacent finishes. We assess what is existing and identify when engineering, permits or specialty trades are required.",
        "scope": [
            ("Openings & flow", "Doorways and room connections can be reshaped where the structure and project plan allow."),
            ("Framing & storage", "New partitions, closets and storage areas can improve how the available space is used."),
            ("Repair & finish", "Drywall, trim and nearby finishes are coordinated so the change feels integrated."),
        ],
        "bullets": ["Wall openings and revisions", "Interior framing", "Closet and storage builds", "Doorway changes", "Drywall and finish restoration", "Coordination with required approvals"],
        "gallery": [
            ("project-025.jpg", "Interior wall framing exposed during renovation", "Layout change in progress"),
            ("project-031.jpg", "Doorway framing during an interior renovation", "New opening and framing"),
            ("project-026.jpg", "Finished interior closet doors", "Finished storage"),
            ("project-138.jpg", "New interior wall framing beside a kitchen", "Framing in progress"),
        ],
        "faq": [
            ("Can you remove a wall?", "Potential wall changes must be assessed first. Structural walls require appropriate engineering, permits and supporting work."),
            ("Can you build a new closet?", "Yes. Framing, drywall, doors and trim can be included in the scope."),
            ("Do layout changes require permits?", "Some do. Requirements depend on structural, plumbing, electrical and other systems affected by the work."),
        ],
        "related": ["kitchens", "basements", "drywall-ceiling-repair"],
    },
}


def write(path: str, content: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(dedent(content).strip() + "\n", encoding="utf-8")


def schema(path: str, image: str) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": ["HomeAndConstructionBusiness", "GeneralContractor"],
        "@id": f"{BASE_URL}/#business",
        "name": "Hekman Home Services Inc.",
        "url": f"{BASE_URL}{path}",
        "image": f"{BASE_URL}/{image}",
        "telephone": PHONE_LINK,
        "email": EMAIL,
        "areaServed": AREAS,
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "London",
            "addressRegion": "ON",
            "addressCountry": "CA",
        },
    }
    return json.dumps(data, separators=(",", ":"))


def head(title: str, description: str, path: str, image: str) -> str:
    canonical = f"{BASE_URL}{path}"
    return f"""
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>{title}</title>
      <meta name="description" content="{html.escape(description, quote=True)}">
      <meta name="theme-color" content="#161512">
      <link rel="canonical" href="{canonical}">
      <link rel="icon" href="/favicon.svg" type="image/svg+xml">
      <meta property="og:type" content="website">
      <meta property="og:site_name" content="Hekman Home Services Inc.">
      <meta property="og:title" content="{title}">
      <meta property="og:description" content="{html.escape(description, quote=True)}">
      <meta property="og:url" content="{canonical}">
      <meta property="og:image" content="{BASE_URL}/{image}">
      <meta property="og:image:alt" content="Completed work by Hekman Home Services Inc.">
      <meta name="twitter:card" content="summary_large_image">
      <link rel="stylesheet" href="/styles.css">
      <script type="application/ld+json">{schema(path, image)}</script>
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
        <span>Renovations &amp; repairs in London, Ontario</span>
        <span><a href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a><i aria-hidden="true"></i><a href="mailto:{EMAIL}">{EMAIL}</a></span>
      </div>
    </div>
    <header class="site-header" data-site-header>
      <div class="nav-shell">
        <a class="brand" href="/" aria-label="Hekman Home Services Inc. home">
          <span class="brand-mark" aria-hidden="true">HH</span>
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
          <a class="nav-cta" href="/contact/#quote">Request a Quote</a>
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
            <span class="brand-mark" aria-hidden="true">HH</span>
            <span><strong>Hekman Home Services Inc.</strong><small>London, Ontario</small></span>
          </a>
          <p>Thoughtful renovation, repair and property improvement work across London and nearby communities.</p>
          <p><a href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
        </div>
        <div><h2>Explore</h2><ul><li><a href="/services/">Services</a></li><li><a href="/projects/">Our Work</a></li><li><a href="/about/">About</a></li><li><a href="/contact/">Contact</a></li></ul></div>
        <div><h2>Popular services</h2><ul><li><a href="/services/bathrooms/">Bathrooms</a></li><li><a href="/services/kitchens/">Kitchens</a></li><li><a href="/services/basements/">Basements</a></li><li><a href="/services/decks-exterior/">Decks &amp; Exterior</a></li></ul></div>
        <div><h2>Service area</h2><p>London, Westmount, Byron, Oakridge, Riverbend, Masonville, Old South, Hyde Park, St. Thomas and nearby communities.</p></div>
      </div>
      <div class="wrap footer-fine"><span>© <span data-year></span> Hekman Home Services Inc. All rights reserved.</span><a href="/contact/">Start a project</a></div>
    </footer>
    <nav class="mobile-actions" aria-label="Quick contact">
      <a href="tel:{PHONE_LINK}"><span aria-hidden="true">☎</span> Call</a>
      <a href="/contact/#quote"><span aria-hidden="true">↗</span> Request a Quote</a>
    </nav>
    <script src="/main.js" defer></script>
    """


def page(title: str, description: str, path: str, image: str, current: str, body: str, body_class: str = "") -> str:
    return f"""<!doctype html>
    <html lang="en">
    {head(title, description, path, image)}
    <body class="{body_class}">
      {header(current)}
      {body}
      {footer()}
    </body>
    </html>"""


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


def section_heading(eyebrow: str, title: str, text: str) -> str:
    return f"""
    <div class="section-heading reveal">
      <div><p class="eyebrow">{eyebrow}</p><h2>{title}</h2></div>
      <p>{text}</p>
    </div>
    """


def service_url(slug: str) -> str:
    return f"/services/{slug}/"


def service_card(slug: str, *, compact: bool = False) -> str:
    item = SERVICES[slug]
    class_name = "service-card compact" if compact else "service-card"
    return f"""
    <a class="{class_name} reveal" href="{service_url(slug)}">
      <img src="/{item['hero']}" alt="{html.escape(item['hero_alt'], quote=True)}" loading="lazy" decoding="async">
      <span class="service-card-shade"></span>
      <span class="service-card-body"><small>London, Ontario</small><strong>{item['card_name']}</strong><span>{item['lead']}</span><b>Explore service <i aria-hidden="true">↗</i></b></span>
    </a>
    """


def homepage() -> str:
    featured = "".join(service_card(slug) for slug in ["bathrooms", "kitchens", "basements", "flooring", "drywall-ceiling-repair", "decks-exterior"])
    body = f"""
    {hero("project-132.jpg", "Completed white kitchen renovation by Hekman Home Services", "Renovations & repairs · London, Ontario", "Thoughtful renovations. Beautifully finished.", "Bathrooms, kitchens, basements, flooring, drywall and ceilings, decks and exterior work, structural changes, water-damage repairs and commercial maintenance—planned carefully and finished with respect for your property.", secondary=("/projects/", "View Our Work"), position="50% 54%")}
    <main id="main">
      <section class="trust-band" aria-label="Business assurances">
        <div class="wrap trust-grid">
          <div><span>01</span><strong>Fully insured</strong><small>Professional protection for your project</small></div>
          <div><span>02</span><strong>2-year workmanship warranty</strong><small>We stand behind our workmanship</small></div>
          <div><span>03</span><strong>Family-run &amp; local</strong><small>Led by Rene and Steph Hekman</small></div>
          <div><span>04</span><strong>Clear project scope</strong><small>Understand the work before it begins</small></div>
        </div>
      </section>
      <section class="section section-paper">
        <div class="wrap">
          {section_heading("What we do", "One team for the work that makes a house feel complete.", "From full-room renovations to complex repair lists, we bring the connected parts of a project together with clear communication and careful finishing.")}
          <div class="service-grid">{featured}</div>
          <div class="section-actions reveal"><a class="button button-dark" href="/services/">View All Services</a></div>
        </div>
      </section>
      <section class="section section-charcoal">
        <div class="wrap editorial-grid">
          <div class="editorial-media reveal"><img src="/project-148.jpg" alt="Completed tiled bathroom with glass shower" loading="lazy" decoding="async"><span>Genuine completed work</span></div>
          <div class="editorial-copy reveal"><p class="eyebrow">Craftsmanship you can see</p><h2>Good work starts behind the finish.</h2><p>What you see at the end depends on what happens first: understanding existing conditions, protecting the home, preparing surfaces and communicating when a project reveals something unexpected.</p><ul class="line-list"><li><strong>Plan the complete scope</strong><span>Look beyond one surface to the connected work around it.</span></li><li><strong>Prepare with care</strong><span>Protection, dust control and cleanup are part of the job.</span></li><li><strong>Finish the details</strong><span>Transitions, trim and touch-ups help the work feel intentional.</span></li></ul><a class="text-link" href="/about/">Meet Hekman Home Services <span aria-hidden="true">↗</span></a></div>
        </div>
      </section>
      <section class="section section-stone">
        <div class="wrap">
          {section_heading("Selected projects", "Real spaces. Real transformations.", "Browse genuine Hekman Home Services photography from kitchens, bathrooms, basements, flooring, exterior and commercial work.")}
          <div class="project-preview">
            <a class="project-tile project-tall reveal" href="/projects/"><img src="/project-132.jpg" alt="Completed kitchen renovation with white cabinetry" loading="lazy"><span><small>Kitchen</small>Bright, functional finish</span></a>
            <a class="project-tile reveal" href="/projects/"><img src="/project-161.jpg" alt="Completed bathroom with wood vanity" loading="lazy"><span><small>Bathroom</small>Warm, modern details</span></a>
            <a class="project-tile reveal" href="/projects/"><img src="/project-103.jpg" alt="Completed elevated wood deck" loading="lazy"><span><small>Exterior</small>Structure built for daily use</span></a>
            <a class="project-tile project-wide reveal" href="/projects/"><img src="/project-067.jpg" alt="Finished basement with warm wood flooring" loading="lazy"><span><small>Basement</small>Comfortable finished space</span></a>
          </div>
          <div class="section-actions reveal"><a class="button button-dark" href="/projects/">Explore Our Work</a></div>
        </div>
      </section>
      <section class="section section-charcoal">
        <div class="wrap">
          {section_heading("Our process", "Clear steps. Thoughtful decisions.", "Every home and project is different, but a straightforward process makes decisions easier and keeps the work moving.")}
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
          <div class="reveal"><p class="eyebrow">Service area</p><h2>Local work, close to home.</h2><p>Hekman Home Services works across London and surrounding communities, including Westmount, Byron, Oakridge, Riverbend, Masonville, Old South, Hyde Park and St. Thomas.</p><div class="area-pills">{"".join(f'<span>{area}</span>' for area in AREAS)}</div></div>
          <div class="photo-stack reveal"><img src="/project-070.jpg" alt="Hekman Home Services team" loading="lazy"><div class="photo-note"><strong>Hands-on, local service</strong><span>Respect for your home and clear communication throughout the work.</span></div></div>
        </div>
      </section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">Have a project in mind?</p><h2>Let’s talk about what needs to change.</h2><p>Send the location, a short description and the best way to reach you.</p></div><div><a class="button button-primary" href="/contact/#quote">Request a Quote</a><a class="cta-phone" href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a></div></div></section>
    </main>
    """
    return page("Renovations & Repairs London ON | Hekman Home Services", "Hekman Home Services Inc. provides bathroom, kitchen, basement, flooring, drywall, ceiling, deck and repair services in London, Ontario and surrounding communities.", "/", "project-132.jpg", "home", body, "home")


def services_page() -> str:
    cards = "".join(service_card(slug, compact=True) for slug in SERVICES)
    body = f"""
    {hero("project-129.jpg", "Completed kitchen renovation", "Renovation & repair services", "Careful work for every part of the property.", "Full-room renovations, focused repairs and the finishing work that connects everything together.", small=True, secondary=("/projects/", "See Completed Work"), position="50% 58%")}
    <main id="main">
      <section class="section section-paper"><div class="wrap">{section_heading("Explore services", "From one repair to a complete transformation.", "Some projects fit one category. Others connect several. Explore the main services below, or send the whole scope and we will review it together.")}<div class="service-grid service-grid-compact">{cards}</div></div></section>
      <section class="section section-charcoal"><div class="wrap editorial-grid reverse"><div class="editorial-media reveal"><img src="/project-011.jpg" alt="Drywall preparation and finishing in progress" loading="lazy"><span>The work behind the finish</span></div><div class="editorial-copy reveal"><p class="eyebrow">Not sure where it fits?</p><h2>Describe the complete project.</h2><p>Photos, approximate measurements and a short explanation help us understand how the pieces connect. You do not need to sort the work into trades before contacting us.</p><a class="button button-primary" href="/contact/#quote">Tell Us About It</a></div></div></section>
    </main>"""
    return page("Renovation Services London ON | Hekman Home Services", "Explore renovation and repair services in London, Ontario, including bathrooms, kitchens, basements, flooring, drywall, ceilings, decks and more.", "/services/", "project-129.jpg", "services", body)


def service_page(slug: str) -> str:
    item = SERVICES[slug]
    scope = "".join(f'<article class="proof-card reveal"><span>0{i}</span><h3>{title}</h3><p>{text}</p></article>' for i, (title, text) in enumerate(item["scope"], 1))
    bullets = "".join(f"<li>{bullet}</li>" for bullet in item["bullets"])
    gallery = "".join(f'<figure class="reveal"><img src="/{src}" alt="{html.escape(alt, quote=True)}" loading="lazy" decoding="async"><figcaption>{caption}</figcaption></figure>' for src, alt, caption in item["gallery"])
    faqs = "".join(f'<details class="reveal"><summary>{question}</summary><p>{answer}</p></details>' for question, answer in item["faq"])
    related = "".join(service_card(related_slug, compact=True) for related_slug in item["related"])
    body = f"""
    {hero(item['hero'], item['hero_alt'], "London, Ontario", item['name'], item['lead'], small=True, position=item['position'])}
    <main id="main">
      <section class="section section-paper"><div class="wrap service-intro"><div class="reveal"><p class="eyebrow">Thoughtful project planning</p><h2>Built around what the space needs.</h2><p>{item['intro']}</p><a class="text-link dark-link" href="/contact/#quote">Discuss your project <span aria-hidden="true">↗</span></a></div><ul class="scope-list reveal">{bullets}</ul></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("What the work can include", "A complete scope, not disconnected pieces.", "The exact work depends on existing conditions, selected materials and the result you want.")}<div class="proof-grid">{scope}</div></div></section>
      <section class="section section-stone"><div class="wrap">{section_heading("Project photography", "See the process and the finish.", "These are genuine photographs from the Hekman Home Services project library.")}<div class="gallery-grid">{gallery}</div><div class="section-actions reveal"><a class="button button-dark" href="/projects/">View More Projects</a></div></div></section>
      <section class="section section-paper"><div class="wrap faq-layout"><div class="reveal"><p class="eyebrow">Common questions</p><h2>Helpful before the walkthrough.</h2><p>The final scope depends on your property, materials and existing conditions.</p></div><div class="faq-list">{faqs}</div></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("Related services", "The connected work matters too.", "Many renovations involve more than one surface or room. These services are often part of the same conversation.")}<div class="service-grid related-grid">{related}</div></div></section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">Ready to talk it through?</p><h2>Show us the space.</h2><p>Send the location, a project description and the best way to reach you.</p></div><div><a class="button button-primary" href="/contact/#quote">Start Your Quote</a><a class="cta-phone" href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a></div></div></section>
    </main>"""
    return page(item["title"], item["description"], service_url(slug), item["hero"], "services", body, "service-page")


PROJECTS = [
    ("project-132.jpg", "kitchens", "Completed white kitchen with island", "Kitchen renovation"),
    ("project-133.jpg", "kitchens", "Completed white kitchen cabinetry", "Kitchen cabinetry"),
    ("project-131.jpg", "kitchens", "Kitchen sink and backsplash detail", "Kitchen finish detail"),
    ("project-136.jpg", "kitchens", "Kitchen island drawers and countertop", "Island detail"),
    ("project-148.jpg", "bathrooms", "Completed bathroom with glass shower", "Glass shower renovation"),
    ("project-157.jpg", "bathrooms", "Completed bathroom vanity and mirror", "Bathroom finish"),
    ("project-161.jpg", "bathrooms", "Completed bathroom with wood vanity", "Bathroom renovation"),
    ("project-155.jpg", "bathrooms", "Completed bathroom with patterned floor", "Bathroom flooring and finish"),
    ("project-067.jpg", "basements", "Completed basement living space", "Finished basement"),
    ("project-068.jpg", "basements", "Completed lower-level room", "Basement finish work"),
    ("project-066.jpg", "basements", "Finished staircase and railing", "Stair detail"),
    ("project-072.jpg", "basements", "New plank flooring in a finished room", "Flooring installation"),
    ("project-103.jpg", "exterior", "Completed elevated wood deck", "Completed deck"),
    ("project-104.jpg", "exterior", "Long completed deck structure", "Multi-unit deck work"),
    ("project-100.jpg", "exterior", "Wood deck with railings", "Deck and railing"),
    ("project-101.jpg", "exterior", "Deck framing and support posts", "Deck structure"),
    ("project-014.jpg", "interiors", "Smooth finished ceiling in completed room", "Ceiling finish"),
    ("project-011.jpg", "interiors", "Drywall finishing in progress", "Drywall process"),
    ("project-025.jpg", "interiors", "Interior wall framing exposed", "Layout change"),
    ("project-026.jpg", "interiors", "Finished closet doors", "Interior finish"),
    ("project-050.jpg", "commercial", "Completed commercial interior", "Commercial maintenance"),
    ("project-046.jpg", "commercial", "Commercial fitness space with upgraded lighting", "Commercial lighting"),
    ("project-049.jpg", "commercial", "Commercial ceiling work in progress", "Commercial process"),
    ("project-054.jpg", "commercial", "Finished commercial workspace", "Commercial finish"),
]


def projects_page() -> str:
    cards = "".join(f'<figure class="project-card reveal" data-category="{category}"><button class="project-image" type="button" data-lightbox aria-label="Enlarge {html.escape(label, quote=True)}"><img src="/{src}" alt="{html.escape(alt, quote=True)}" loading="lazy" decoding="async"></button><figcaption><span>{label}</span><small>{category.title()}</small></figcaption></figure>' for src, category, alt, label in PROJECTS)
    filters = [("all", "All Work"), ("kitchens", "Kitchens"), ("bathrooms", "Bathrooms"), ("basements", "Basements & Flooring"), ("exterior", "Decks & Exterior"), ("interiors", "Drywall & Structural"), ("commercial", "Commercial")]
    buttons = "".join(f'<button type="button" class="filter-button{" active" if key == "all" else ""}" data-filter="{key}" aria-pressed="{"true" if key == "all" else "false"}">{label}</button>' for key, label in filters)
    body = f"""
    {hero("project-148.jpg", "Completed tiled shower renovation", "Our work", "Built in real homes. Photographed as completed.", "Explore genuine project photography across kitchens, bathrooms, basements, flooring, exteriors, repairs and commercial spaces.", small=True, position="50% 56%")}
    <main id="main">
      <section class="section section-paper"><div class="wrap">{section_heading("Before & after", "Transformation begins with the groundwork.", "A closer look at projects moving from existing conditions and preparation toward a clean finished result.")}<div class="comparison-grid">
        <article class="comparison-card reveal"><div class="comparison-images"><figure><img src="/project-137.jpg" alt="Kitchen before renovation work" loading="lazy"><figcaption>Before</figcaption></figure><figure><img src="/project-132.jpg" alt="Completed white kitchen renovation" loading="lazy"><figcaption>After</figcaption></figure></div><h3>Kitchen transformation</h3><p>A dated layout and finishes reworked into a brighter, more functional kitchen.</p></article>
        <article class="comparison-card reveal"><div class="comparison-images"><figure><img src="/project-011.jpg" alt="Ceiling and drywall finishing in progress" loading="lazy"><figcaption>During</figcaption></figure><figure><img src="/project-014.jpg" alt="Completed smooth ceiling and finished room" loading="lazy"><figcaption>Finished</figcaption></figure></div><h3>Walls &amp; ceiling</h3><p>Careful preparation and staged finishing create the smooth final surface.</p></article>
        <article class="comparison-card reveal"><div class="comparison-images"><figure><img src="/project-061.jpg" alt="Carpeted room before flooring update" loading="lazy"><figcaption>Before</figcaption></figure><figure><img src="/project-072.jpg" alt="Room with new plank flooring" loading="lazy"><figcaption>After</figcaption></figure></div><h3>Flooring update</h3><p>New plank flooring changes the tone of the room and gives it a cleaner finish.</p></article>
      </div></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("Project gallery", "Browse the work by category.", "Only photographs that can be identified responsibly are labelled by service. The complete source image library remains preserved in the repository.")}<div class="filter-bar" aria-label="Filter projects">{buttons}</div><div class="projects-grid" aria-live="polite">{cards}</div><p class="filter-status" data-filter-status>Showing all projects.</p></div></section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">Picture your own project?</p><h2>Start with a few details.</h2><p>Tell us what you want to change and where the property is located.</p></div><div><a class="button button-primary" href="/contact/#quote">Request a Quote</a><a class="cta-phone" href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a></div></div></section>
      <dialog class="lightbox" data-lightbox-dialog><button type="button" class="lightbox-close" data-lightbox-close aria-label="Close image">×</button><img src="" alt=""><p></p></dialog>
    </main>"""
    return page("Our Renovation Projects London ON | Hekman Home Services", "Browse genuine kitchen, bathroom, basement, flooring, deck, drywall and commercial project photos from Hekman Home Services in London, Ontario.", "/projects/", "project-148.jpg", "projects", body, "projects-page")


def about_page() -> str:
    body = f"""
    {hero("project-070.jpg", "Hekman Home Services team gathered around project plans", "About Hekman Home Services", "Hands-on work. Clear communication. Respect for your home.", "A local, family-run renovation and repair company led by Rene and Steph Hekman in London, Ontario.", small=True, position="50% 42%")}
    <main id="main">
      <section class="section section-paper"><div class="wrap editorial-grid about-story"><div class="editorial-copy reveal"><p class="eyebrow">Our approach</p><h2>A renovation company built around the work itself.</h2><p>Hekman Home Services brings hands-on renovation experience together with thoughtful planning and practical communication. We look at how each part of the project connects—from what is behind the wall to the trim and transition you see at the end.</p><p>Clients invite us into homes and properties that matter to them. We treat that trust seriously by protecting the space, discussing changes and keeping the finish in view throughout the project.</p></div><div class="editorial-media reveal"><img src="/project-079.jpg" alt="Hekman Home Services team reviewing plans" loading="lazy"><span>Planning the work together</span></div></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("What guides the work", "Professional does not have to feel impersonal.", "The strongest projects come from good preparation, honest conversations and care for the property throughout the work.")}<div class="values-grid"><article class="reveal"><span>01</span><h3>Listen first</h3><p>Understand the problem, priorities and intended result before defining the work.</p></article><article class="reveal"><span>02</span><h3>Protect the property</h3><p>Preparation, dust control and cleanup are treated as part of the project.</p></article><article class="reveal"><span>03</span><h3>Communicate clearly</h3><p>When existing conditions affect the plan, explain what changed and why.</p></article><article class="reveal"><span>04</span><h3>Finish thoughtfully</h3><p>Trim, transitions and final details matter because they are what make the work feel complete.</p></article></div></div></section>
      <section class="section section-stone"><div class="wrap people-grid"><article class="person-card reveal"><img src="/project-075.jpg" alt="Rene Hekman of Hekman Home Services" loading="lazy"><div><p class="eyebrow">Hands-on workmanship</p><h2>Rene Hekman</h2><p>Rene leads the hands-on construction and repair work, with attention to practical solutions, preparation and the details needed to complete the space.</p></div></article><article class="person-card reveal"><img src="/project-076.jpg" alt="Steph Hekman of Hekman Home Services" loading="lazy"><div><p class="eyebrow">Planning & communication</p><h2>Steph Hekman</h2><p>Steph supports project planning, communication and the client experience, helping homeowners move from the first conversation toward a clear project scope.</p></div></article></div></section>
      <section class="section section-paper"><div class="wrap area-layout"><div class="reveal"><p class="eyebrow">Local service</p><h2>Working throughout London and nearby communities.</h2><p>Based in London, Hekman Home Services works in neighbourhoods including Westmount, Byron, Oakridge, Riverbend, Masonville, Old South and Hyde Park, as well as St. Thomas and nearby areas.</p><a class="button button-dark" href="/contact/">Contact the Team</a></div><div class="assurance-panel reveal"><strong>Fully insured</strong><span>Professional protection for your project.</span><strong>2-year workmanship warranty</strong><span>We stand behind our workmanship.</span><strong>Genuine project photography</strong><span>See real work completed by Hekman Home Services.</span></div></div></section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">Let’s discuss your property.</p><h2>Start with the space and the goal.</h2><p>We will help make sense of the connected work from there.</p></div><div><a class="button button-primary" href="/contact/#quote">Request a Quote</a><a class="cta-phone" href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a></div></div></section>
    </main>"""
    return page("About Hekman Home Services | London ON Renovations", "Meet Hekman Home Services Inc., a local family-run renovation and repair company led by Rene and Steph Hekman in London, Ontario.", "/about/", "project-070.jpg", "about", body, "about-page")


def contact_page() -> str:
    options = "".join(f'<option value="{item["name"]}">{item["name"]}</option>' for item in SERVICES.values())
    body = f"""
    {hero("project-129.jpg", "Completed kitchen renovation", "Contact Hekman Home Services", "Tell us what you want to change.", "A short description, the project location and a few photos are enough to begin the conversation.", small=True, position="50% 58%")}
    <main id="main">
      <section class="section section-paper" id="quote"><div class="wrap contact-layout"><div class="contact-intro reveal"><p class="eyebrow">Request a quote</p><h2>Start with what you know.</h2><p>You do not need every finish or measurement decided. Tell us what is not working, what you would like the space to become and where the property is located.</p><div class="contact-direct"><h3>Prefer direct contact?</h3><a href="tel:{PHONE_LINK}"><small>Call or text</small><strong>{PHONE_DISPLAY}</strong></a><a href="mailto:{EMAIL}"><small>Email</small><strong>{EMAIL}</strong></a><div><small>Service area</small><strong>London, St. Thomas &amp; nearby communities</strong></div></div></div>
      <form class="quote-form reveal" id="quote-form" novalidate><div class="form-heading"><span>Project enquiry</span><small>Fields marked * are required</small></div><div class="form-grid"><label>Name *<input name="name" autocomplete="name" required></label><label>Project location *<input name="location" autocomplete="address-level2" placeholder="London, Byron, St. Thomas…" required></label></div><fieldset><legend>How should we reach you? *</legend><p id="contact-help">Enter a phone number, an email address, or both.</p><div class="form-grid"><label>Phone<input name="phone" type="tel" autocomplete="tel"></label><label>Email<input name="email" type="email" autocomplete="email"></label></div></fieldset><div class="form-grid"><label>Project type<select name="service"><option value="">Choose one</option>{options}<option value="Multiple services / other">Multiple services / other</option></select></label><label>Preferred timing<input name="timing" placeholder="Flexible, this fall, as soon as possible…"></label></div><label>Project details *<textarea name="message" placeholder="What would you like repaired, renovated or changed?" required></textarea></label><p class="form-error" data-form-error role="alert"></p><button class="button button-dark" type="submit">Prepare Quote Email <span aria-hidden="true">↗</span></button><p class="form-note">This opens your email app with the details filled in so you can review and send them directly. You can attach project photos before sending.</p></form></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("What happens next", "A useful first conversation starts with context.", "Sharing a few details helps us understand the likely scope before arranging the next step.")}<ol class="process-grid compact-process"><li class="reveal"><span>01</span><h3>Describe the project</h3><p>Include the location, room and result you have in mind.</p></li><li class="reveal"><span>02</span><h3>Add photos</h3><p>Attach wide views and closer images of the affected areas.</p></li><li class="reveal"><span>03</span><h3>Connect</h3><p>We review the information and discuss the appropriate next step.</p></li></ol></div></section>
    </main>"""
    return page("Contact Hekman Home Services | Request a Quote", "Contact Hekman Home Services Inc. for renovation and repair projects in London, Ontario. Call 519-808-3312 or prepare a quote request by email.", "/contact/", "project-129.jpg", "contact", body, "contact-page")


def not_found_page() -> str:
    body = f"""
    <main id="main" class="not-found">
      <img src="/project-132.jpg" alt="" aria-hidden="true">
      <div class="not-found-shade"></div>
      <div class="not-found-content"><p class="eyebrow">404 · Page not found</p><h1>This page needs a little repair.</h1><p>The address may have changed, but the rest of the site is ready to explore.</p><div class="button-row"><a class="button button-primary" href="/">Return Home</a><a class="button button-ghost" href="/services/">Explore Services</a></div></div>
    </main>"""
    return page("Page Not Found | Hekman Home Services", "The requested page could not be found.", "/404.html", "project-132.jpg", "", body, "error-page")


def redirect_stub(destination: str, title: str) -> str:
    canonical = f"{BASE_URL}{destination}"
    return f"""<!doctype html>
    <html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title}</title><meta name="robots" content="noindex"><link rel="canonical" href="{canonical}"><meta http-equiv="refresh" content="0; url={destination}"></head><body><p>This page has moved to <a href="{destination}">{destination}</a>.</p></body></html>"""


def build() -> None:
    write("index.html", homepage())
    write("services/index.html", services_page())
    for slug in SERVICES:
        write(f"services/{slug}/index.html", service_page(slug))
    write("projects/index.html", projects_page())
    write("about/index.html", about_page())
    write("contact/index.html", contact_page())
    write("404.html", not_found_page())

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
        "structural-layout.html": ("/services/structural-layout/", "Structural & Layout Changes | Hekman Home Services"),
    }
    for filename, (destination, title) in legacy.items():
        write(filename, redirect_stub(destination, title))
    write("reviews/index.html", redirect_stub("/projects/", "Our Work | Hekman Home Services"))

    urls = ["/", "/services/", *[service_url(slug) for slug in SERVICES], "/projects/", "/about/", "/contact/"]
    sitemap_urls = "\n".join(f"  <url><loc>{BASE_URL}{url}</loc></url>" for url in urls)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sitemap_urls}\n</urlset>')
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml")


if __name__ == "__main__":
    build()
