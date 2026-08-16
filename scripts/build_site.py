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
BASE_URL = "https://www.hekmanhomeservices.ca"
PHONE_DISPLAY = "519-808-3312"
PHONE_LINK = "+15198083312"
EMAIL = "hekmanhomeservices@gmail.com"
FACEBOOK = "https://www.facebook.com/p/Hekman-Home-Services-100066576836967/"
INSTAGRAM = "https://www.instagram.com/hekman_home_services_inc/"

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
        "hero": "bathroom-walnut-vanity-after.jpg",
        "hero_alt": "Completed tub-to-shower bathroom conversion with a walnut vanity and glass-block window",
        "position": "50% 52%",
        "lead": "Create a bathroom that works better every day—with careful preparation behind every visible finish.",
        "intro": "A successful bathroom renovation balances layout, water management, storage and finish details. We review the existing room, talk through priorities and build a clear scope around the condition of the space.",
        "scope": [
            ("Preparation & waterproofing", "Shower systems, substrate preparation and waterproofing are planned before tile and fixtures go in."),
            ("Tile & heated floors", "Wall tile, floor tile and heated-floor options can be coordinated into the room."),
            ("Fixtures & finish work", "Vanities, faucets, toilets, lighting, trim and paint-ready surfaces bring the room together."),
        ],
        "bullets": ["Full bathroom renovations", "Tub-to-shower conversions", "Shower and tub surrounds", "Tile and grout work", "Vanities, fixtures and storage", "Flooring, trim and finishing"],
        "gallery": [
            ("bathroom-glass-block-before.jpg", "Bathroom with a jetted tub and glass-block window before the tub-to-shower conversion", "Before: jetted-tub layout"),
            ("bathroom-glass-block-open-wall.jpg", "Jetted tub removed with the insulated wall and floor framing exposed", "During: opened wall and floor"),
            ("bathroom-walnut-vanity-after.jpg", "Completed tub-to-shower conversion with gray tile, a walnut vanity and sliding glass door", "After: glass shower conversion"),
            ("project-148.jpg", "Completed bathroom with glass shower enclosure", "Another glass shower renovation"),
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
        "hero": "hilltop-kitchen-wide.jpg",
        "hero_alt": "Completed Hilltop kitchen renovation with island seating",
        "position": "50% 52%",
        "lead": "Improve the heart of the home with a kitchen planned around storage, flow and the way your household lives.",
        "intro": "Kitchen work often connects cabinetry, plumbing, lighting, walls, flooring, tile and finishing. We look at the full room so the new elements feel integrated rather than added one at a time.",
        "scope": [
            ("Cabinets & layout", "Cabinet installation and practical layout changes can make better use of the available room."),
            ("Backsplash & surfaces", "Tile, wall repair and finishing help counters, cabinets and appliances sit cleanly together."),
            ("Lighting, plumbing & final details", "Pot lights, fixture and plumbing changes, trim, hardware, transitions and touch-ups are coordinated into the complete room."),
        ],
        "bullets": ["Kitchen renovations and updates", "Cabinet assembly and installation", "Backsplash installation", "Pot lights and lighting updates", "Plumbing and fixture changes", "Drywall, trim and finishing details"],
        "gallery": [
            ("hilltop-kitchen-wide.jpg", "Completed Hilltop kitchen with island seating", "Hilltop kitchen"),
            ("hilltop-kitchen-range.jpg", "White cabinetry and range wall in the Hilltop kitchen", "Cabinetry and range wall"),
            ("hilltop-kitchen-sink.jpg", "Sink, counter and backsplash in the completed Hilltop kitchen", "Sink and backsplash detail"),
            ("project-132.jpg", "Completed white kitchen with island seating", "Another completed kitchen"),
            ("kitchenette-before-wide.jpg", "Older kitchenette before cabinetry and repair work", "Before: existing kitchenette"),
            ("kitchenette-after-wide.jpg", "Completed kitchenette with walnut-look cabinets and gray counter", "Completed kitchenette"),
        ],
        "faq": [
            ("Do you install customer-supplied cabinets?", "Cabinet installation can be included after the cabinet system, measurements and site conditions are reviewed."),
            ("Can you update a kitchen without changing everything?", "Yes. A project can focus on cabinets, backsplash, flooring, repairs or finishing without requiring a full layout change."),
            ("Can you coordinate plumbing and pot lights?", "Yes. Kitchen scopes can include fixture plumbing, pot-light layouts and required trade coordination alongside cabinets, drywall and finish work."),
        ],
        "related": ["structural-layout", "flooring", "drywall-ceiling-repair"],
    },
    "basements": {
        "name": "Basement Renovations",
        "card_name": "Basements",
        "title": "Basement Renovations London ON | Hekman Home Services",
        "description": "Basement renovations in London, Ontario, including framing, drywall, ceilings, flooring, trim, storage and finished living spaces.",
        "hero": "hilltop-lower-level.jpg",
        "hero_alt": "Completed Hilltop lower-level renovation with fireplace and warm flooring",
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
            ("hilltop-lower-level.jpg", "Completed Hilltop lower-level living space with fireplace", "Hilltop lower level"),
            ("project-067.jpg", "Finished basement with warm wood flooring", "Finished living space"),
            ("hilltop-staircase.jpg", "Finished Hilltop staircase with dark railing", "Stair and railing detail"),
            ("hilltop-entry.jpg", "Finished lower-level entry and flooring transition", "Entry and transition"),
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
        "description": "Carpet, vinyl plank, laminate, hardwood and tile flooring installation in London, Ontario, with subfloor preparation and finish trim.",
        "hero": "project-072.jpg",
        "hero_alt": "Completed plank flooring installation in a renovated room",
        "position": "50% 60%",
        "lead": "Carpet, vinyl, laminate, hardwood and tile—installed with the right preparation underneath and clean details at every edge.",
        "intro": "Flooring changes the feel of an entire room. We work with carpet, vinyl plank, laminate, hardwood and tile, reviewing the existing surface, movement between rooms and the details needed at walls, doors, stairs and adjoining finishes.",
        "scope": [
            ("Removal & preparation", "Existing carpet or hard flooring can be removed, and visible subfloor conditions and transitions are reviewed before installation."),
            ("Material-specific installation", "Carpet, vinyl plank, laminate, hardwood and tile each receive the layout and installation approach the selected material requires."),
            ("Trim & transitions", "Baseboards, nosings, thresholds and doorway details complete the installation."),
        ],
        "bullets": ["Carpet installation and removal", "Vinyl plank and laminate", "Hardwood and engineered wood", "Tile flooring", "Subfloor preparation", "Transitions, stairs and finish trim"],
        "gallery": [
            ("project-072.jpg", "New plank flooring in a finished room", "Plank flooring installation"),
            ("project-038.jpg", "Engineered wood flooring being installed", "Hardwood installation in progress"),
            ("project-055.jpg", "Existing carpet documented before flooring work", "Carpet and room preparation"),
            ("project-042.jpg", "New flooring installed through a kitchen", "Kitchen flooring"),
            ("project-063.jpg", "Tile flooring at a bright patio entry", "Tile and transition work"),
            ("project-043.jpg", "Dark wood flooring in a finished room", "Wood flooring finish"),
            ("project-066.jpg", "Finished staircase with wood treads", "Stair finish detail"),
            ("project-060.jpg", "Click flooring installation beside a finished wall", "Flooring installation detail"),
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
        "description": "Drywall, ceiling and related insulation work in London, Ontario, including replacement, taping, mudding, sanding and paint-ready finishes.",
        "hero": "project-014.jpg",
        "hero_alt": "Smooth repaired ceiling in a finished room",
        "position": "50% 58%",
        "lead": "Repair damaged walls and ceilings with careful preparation and a smooth, paint-ready finish.",
        "intro": "Good drywall work should disappear into the room. We assess the damaged area, remove loose or affected material where needed, address accessible insulation within the repair scope and build the finish in controlled stages.",
        "scope": [
            ("Open & assess", "The damaged area is reviewed so loose material and the repair boundary can be handled properly."),
            ("Patch & finish", "New board, tape and compound are applied in the stages required for the repair."),
            ("Prepare for paint", "Sanding and final touch-ups create a clean surface for primer and paint."),
        ],
        "bullets": ["Wall and ceiling patches", "Drywall replacement", "Taping and mudding", "Ceiling repairs", "Insulation work in opened walls or ceilings", "Primer, painting and finish restoration"],
        "gallery": [
            ("project-011.jpg", "Drywall finishing in progress on walls and ceiling", "Finishing in progress"),
            ("project-015.jpg", "Ceiling patch and compound work", "Ceiling repair"),
            ("project-014.jpg", "Completed smooth ceiling in a finished room", "Completed ceiling"),
            ("project-010.jpg", "Protected room prepared for drywall finishing", "Room protection and preparation"),
            ("insulation-open-wall.jpg", "Opened wall and ceiling with insulation exposed during renovation", "Insulation and wall access"),
            ("insulation-drywall-stage.jpg", "Drywall being installed over insulated wall cavities", "Insulation and drywall stage"),
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
        "hero": "project-016.jpg",
        "hero_alt": "Textured ceiling documented before smooth-ceiling finishing",
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
            ("project-016.jpg", "Original textured ceiling and a patched opening before finishing", "Before: textured ceiling"),
            ("popcorn-ceiling-sander.jpg", "Dust-covered drywall sander used during popcorn ceiling removal", "Dust-controlled sanding equipment"),
            ("project-017.jpg", "Ceiling skim coating underway with the room protected", "Skim-coat stage"),
            ("popcorn-ceiling-primer.jpg", "Primer being rolled onto the smoothed ceiling", "Primer and finish stage"),
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
        "intro": "Exterior work has to respond to weather, existing structure and how people use the property. We review access, site conditions and the full scope—whether that is a deck, fence, gate, railing, post or focused repair—before work begins.",
        "scope": [
            ("Deck structures", "New construction and replacement work are planned around the property, access and required approvals."),
            ("Railings & stairs", "Steps, guards, railings and transitions are considered as part of safe everyday use."),
            ("Fences, gates & posts", "Privacy fencing, gates, post replacement and post-hole work can be planned around access, grade and the intended layout."),
        ],
        "bullets": ["Deck construction and replacement", "Deck repairs", "Stairs, railings and guards", "Privacy fences and gates", "Post-hole digging and auger work", "Posts, trim and focused repairs"],
        "gallery": [
            ("project-103.jpg", "Completed elevated deck behind a brick home", "Completed deck"),
            ("project-104.jpg", "Long completed residential deck structure", "Multi-unit exterior work"),
            ("project-100.jpg", "Wood deck and railing at a residential property", "Deck and railing"),
            ("fence-after-1.jpg", "Completed long-run wood privacy fence", "Privacy fence"),
            ("fence-after-2.jpg", "Completed wood privacy fence and posts", "Fence and post finish"),
            ("post-hole-digging.jpg", "Post hole being dug by hand beside a residential property", "Post-hole preparation"),
            ("post-hole-auger.jpg", "Powered auger digging a post hole", "Auger work"),
            ("project-101.jpg", "Deck framing and support structure", "Deck structure"),
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
        "hero": "salon-water-damage-1.jpg",
        "hero_alt": "Water-damaged ceiling opened for commercial repair",
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
            ("salon-water-damage-1.jpg", "Water-damaged ceiling opened to expose affected material", "Water damage documented"),
            ("salon-water-damage-2.jpg", "Second view of opened commercial ceiling after a leak", "Repair area opened"),
            ("salon-drywall-rebuild.jpg", "Commercial walls and ceiling after new drywall and compound", "Drywall rebuilding"),
            ("salon-after-1.jpg", "Finished Pixie and Paige salon interior after commercial repairs", "Completed commercial space"),
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
        "description": "Commercial maintenance and repairs in London, Ontario, including salon, fitness, retail, office-kitchen, drywall, lighting and repair work.",
        "hero": "salon-after-2.jpg",
        "hero_alt": "Completed Pixie and Paige salon interior after commercial repair work",
        "position": "50% 56%",
        "lead": "Responsive repair and improvement work for salons, fitness facilities, offices, retail, rentals and managed properties.",
        "intro": "Commercial spaces need repairs completed with a clear scope, awareness of customers and staff, and respect for day-to-day operations. Hekman Home Services can address one urgent repair, a tenant improvement or a grouped maintenance list across drywall, ceilings, pot lights, plumbing fixtures, painting, doors, trim, kitchenettes and other compatible work.",
        "scope": [
            ("Repair lists", "Drywall, trim, doors, fixtures and other compatible items can be grouped into one scope."),
            ("Occupied-space improvements", "Finish updates, lighting-related ceiling work and layout repairs can support salons, fitness facilities, retail and office spaces."),
            ("Property maintenance", "Business owners, landlords and property managers can consolidate several repair needs into one practical project quote."),
        ],
        "bullets": ["Commercial drywall and water-damage repairs", "Pot lights and ceiling finish work", "Salon, retail, office-kitchen and fitness-space improvements", "Plumbing fixtures, doors, trim and painting", "Grouped maintenance lists", "Rental and managed-property repairs"],
        "gallery": [
            ("salon-after-2.jpg", "Completed Pixie and Paige salon interior", "Salon commercial work"),
            ("salon-after-1.jpg", "Long view of finished salon stations and lighting", "Finished salon interior"),
            ("salon-water-damage-1.jpg", "Water-damaged commercial ceiling opened for repair", "Water-damage repair"),
            ("salon-drywall-rebuild.jpg", "Commercial room during drywall rebuilding", "Drywall restoration"),
            ("project-046.jpg", "Commercial fitness space with upgraded lighting", "Commercial lighting finish"),
            ("project-049.jpg", "Commercial ceiling work in progress", "Ceiling work in progress"),
            ("project-050.jpg", "Commercial fitness interior after maintenance work", "Completed fitness space"),
            ("project-054.jpg", "Finished commercial interior", "Finished workspace"),
            ("kitchenette-before-wide.jpg", "Dated office kitchen before the renovation", "Office kitchen before"),
            ("kitchenette-after-wide.jpg", "Completed office kitchen with new cabinets, counter and sink", "Office kitchen complete"),
        ],
        "faq": [
            ("Do you work in occupied commercial spaces?", "Yes, when the scope, access and scheduling requirements make it practical. We discuss ways to reduce disruption."),
            ("Can several small repairs be grouped together?", "Yes. Grouping compatible maintenance items can make the work more efficient."),
            ("Do you work with landlords and property managers?", "Commercial and rental-property repair work can be quoted for owners and managers."),
        ],
        "related": ["drywall-ceiling-repair", "structural-layout", "water-damage"],
    },
    "handyman-repairs": {
        "name": "Handyman Work & Home Repairs",
        "card_name": "Handyman & Repairs",
        "title": "Handyman & Home Repairs London ON | Hekman Home Services",
        "description": "Handyman and home repair services in London, Ontario, including doors, trim, plumbing fixtures, painting, drywall patching and grouped repair lists.",
        "hero": "project-027.jpg",
        "hero_alt": "Doorway and trim work during a residential repair project",
        "position": "50% 48%",
        "lead": "Take care of the repairs that keep getting postponed—from doors and trim to drywall patches, paint and bathroom fixtures.",
        "intro": "Not every project is a full renovation. Hekman Home Services can group compatible repairs into one practical scope, making it easier to address the small problems and finish details that affect how a home works every day.",
        "scope": [
            ("Doors & trim", "Interior doors, hardware, casing, baseboards and focused carpentry repairs can be reviewed together."),
            ("Patches & paint", "Drywall damage, ceiling patches, surface preparation and painting can restore worn or opened areas."),
            ("Fixtures & repair lists", "Bathroom and kitchen plumbing fixtures, caulking, hardware and other compatible maintenance items can be grouped into one visit."),
        ],
        "bullets": ["Interior door and hardware repairs", "Baseboards, casing and trim", "Drywall and ceiling patching", "Painting and touch-ups", "Bathroom and kitchen plumbing fixtures", "Grouped handyman and maintenance lists"],
        "gallery": [
            ("project-027.jpg", "Doorway and trim work during a residential repair", "Door and trim work"),
            ("project-026.jpg", "Finished double closet doors and interior trim", "Finished doors"),
            ("project-032.jpg", "Drywall patching and compound on an interior wall", "Drywall patching"),
            ("project-140.jpg", "Painting and finishing work in a bathroom", "Painting and finish work"),
            ("project-139.jpg", "Bathroom toilet and flooring installation detail", "Bathroom fixture work"),
            ("bathroom-walnut-vanity-after.jpg", "Completed bathroom with walnut vanity, fixtures and glass shower", "Bathroom finish details"),
        ],
        "faq": [
            ("Can I send a list of several repairs?", "Yes. Photos and a room-by-room list help us identify which compatible items can be completed in one scope."),
            ("Do you handle plumbing repairs?", "Fixture replacement and compatible bathroom or kitchen plumbing repairs can be reviewed, with licensed trade coordination used where the work requires it."),
            ("Can patching and painting be completed together?", "Yes. Drywall patching, surface preparation, primer and painting can be combined when that is the right finish for the repair."),
        ],
        "related": ["drywall-ceiling-repair", "bathrooms", "commercial"],
    },
    "structural-layout": {
        "name": "Structural & Layout Changes",
        "card_name": "Structural & Layout",
        "title": "Structural & Layout Changes London ON | Hekman Home Services",
        "description": "Framing, wall openings, closet builds and layout changes for renovation projects in London, Ontario.",
        "hero": "westmount-wall-opening-1.jpg",
        "hero_alt": "Westmount interior wall opening supported during a layout renovation",
        "position": "50% 50%",
        "lead": "Change how rooms connect, improve storage and make an existing layout work better for everyday life.",
        "intro": "Layout work often affects framing, drywall, flooring and adjacent finishes. We assess what is existing and work with engineers and designers where the project requires structural direction, drawings, permits or a coordinated design plan.",
        "scope": [
            ("Openings & flow", "Doorways and room connections can be reshaped where the structure, engineering and project plan allow."),
            ("Framing & storage", "New partitions, closets and storage areas can improve how the available space is used."),
            ("Repair & finish", "Drywall, trim and nearby finishes are coordinated so the change feels integrated."),
        ],
        "bullets": ["Wall openings and revisions", "Interior framing", "Engineer and designer coordination", "Closet, storage and doorway changes", "Drywall and finish restoration", "Permit and specialty-trade coordination"],
        "gallery": [
            ("westmount-wall-opening-1.jpg", "Westmount wall opening supported during structural work", "Westmount wall opening"),
            ("westmount-wall-opening-2.jpg", "Second view of the supported Westmount wall opening", "Structural stage"),
            ("westmount-living-finish.jpg", "Finished Westmount living area after the layout change", "Completed living space"),
            ("westmount-closet-finish.jpg", "Finished Westmount closets, doors and plank flooring", "Closets and finish work"),
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
    service_names = [item["name"] for item in SERVICES.values()]
    business = {
        "@type": ["HomeAndConstructionBusiness", "GeneralContractor", "LocalBusiness"],
        "@id": f"{BASE_URL}/#business",
        "name": "Hekman Home Services Inc.",
        "url": BASE_URL,
        "logo": f"{BASE_URL}/hekman-logo.jpg",
        "image": f"{BASE_URL}/{image}",
        "description": "Family-run renovation, repair and property improvement company serving London, Ontario and surrounding communities.",
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
        crumbs.append(
            {
                "@type": "ListItem",
                "position": len(crumbs) + 1,
                "name": SERVICES[service_slug]["name"] if service_slug else path.strip("/").split("/")[-1].replace("-", " ").title(),
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


def head(title: str, description: str, path: str, image: str, *, indexable: bool = True) -> str:
    canonical = f"{BASE_URL}{path}"
    robots = "index,follow,max-image-preview:large" if indexable else "noindex,follow"
    structured_data = f'<script type="application/ld+json">{schema(path, image)}</script>' if indexable else ""
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
      <meta property="og:type" content="website">
      <meta property="og:locale" content="en_CA">
      <meta property="og:site_name" content="Hekman Home Services Inc.">
      <meta property="og:title" content="{title}">
      <meta property="og:description" content="{html.escape(description, quote=True)}">
      <meta property="og:url" content="{canonical}">
      <meta property="og:image" content="{BASE_URL}/{image}">
      <meta property="og:image:alt" content="Completed work by Hekman Home Services Inc.">
      <meta name="twitter:card" content="summary_large_image">
      <meta name="twitter:title" content="{title}">
      <meta name="twitter:description" content="{html.escape(description, quote=True)}">
      <meta name="twitter:image" content="{BASE_URL}/{image}">
      <link rel="stylesheet" href="/styles.css">
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
        <span>Renovations &amp; repairs in London, Ontario</span>
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
            <img class="brand-logo" src="/hekman-logo.jpg" alt="" width="64" height="64" loading="lazy" decoding="async">
            <span><strong>Hekman Home Services Inc.</strong><small>London, Ontario</small></span>
          </a>
          <p>Thoughtful renovation, repair and property improvement work across London and nearby communities.</p>
          <p><a href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
          <p class="social-links"><a href="{INSTAGRAM}" rel="me noopener" target="_blank">Instagram</a><a href="{FACEBOOK}" rel="me noopener" target="_blank">Facebook</a></p>
        </div>
        <div><h2>Explore</h2><ul><li><a href="/services/">Services</a></li><li><a href="/projects/">Our Work</a></li><li><a href="/about/">About</a></li><li><a href="/contact/">Contact</a></li></ul></div>
        <div><h2>Popular services</h2><ul><li><a href="/services/bathrooms/">Bathrooms</a></li><li><a href="/services/kitchens/">Kitchens</a></li><li><a href="/services/basements/">Basements</a></li><li><a href="/services/decks-exterior/">Decks &amp; Exterior</a></li><li><a href="/services/handyman-repairs/">Handyman &amp; Repairs</a></li><li><a href="/services/commercial/">Commercial Work</a></li></ul></div>
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


def page(title: str, description: str, path: str, image: str, current: str, body: str, body_class: str = "", *, indexable: bool = True) -> str:
    return f"""<!doctype html>
    <html lang="en">
    {head(title, description, path, image, indexable=indexable)}
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
    featured = "".join(service_card(slug) for slug in ["bathrooms", "kitchens", "basements", "flooring", "drywall-ceiling-repair", "decks-exterior", "handyman-repairs", "structural-layout", "commercial"])
    body = f"""
    {hero("hilltop-kitchen-wide.jpg", "Completed Hilltop kitchen renovation by Hekman Home Services", "Renovations & repairs · London, Ontario", "Thoughtful London renovations, built from the inside out.", "Bathrooms, kitchens and basements. Carpet, vinyl and hardwood. Drywall, painting, insulation, pot lights and plumbing. Decks, fences, structural changes, home repairs and commercial maintenance—planned as one complete scope.", secondary=("/projects/", "View Our Work"), position="50% 54%")}
    <main id="main">
      <section class="trust-band" aria-label="Business assurances">
        <div class="wrap trust-grid">
          <div><span>01</span><strong>Fully insured &amp; bondable</strong><small>Professional protection for your project</small></div>
          <div><span>02</span><strong>2-year workmanship guarantee</strong><small>We stand behind our workmanship</small></div>
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
          <div class="editorial-media reveal"><img src="/bathroom-walnut-vanity-after.jpg" alt="Completed tub-to-shower bathroom conversion with glass enclosure" loading="lazy" decoding="async"><span>Genuine completed work</span></div>
          <div class="editorial-copy reveal"><p class="eyebrow">Craftsmanship you can see</p><h2>Good work starts behind the finish.</h2><p>What you see at the end depends on what happens first: understanding existing conditions, protecting the home, preparing surfaces and communicating when a project reveals something unexpected.</p><ul class="line-list"><li><strong>Plan the complete scope</strong><span>Look beyond one surface to the connected work around it.</span></li><li><strong>Prepare with care</strong><span>Protection, dust control and cleanup are part of the job.</span></li><li><strong>Finish the details</strong><span>Transitions, trim and touch-ups help the work feel intentional.</span></li></ul><a class="text-link" href="/about/">Meet Hekman Home Services <span aria-hidden="true">↗</span></a></div>
        </div>
      </section>
      <section class="section section-stone">
        <div class="wrap">
          {section_heading("Signature work", "Every property has its own story.", "Step inside a whole-home Hilltop transformation, a 1970s Westmount reinvention, detailed bathroom work and the restoration of a working London salon.")}
          <div class="project-preview">
            <a class="project-tile project-tall reveal" href="/projects/hilltop-home-transformation/"><img src="/hilltop-kitchen-angle.jpg" alt="Completed Hilltop kitchen renovation" loading="lazy"><span><small>Whole-home transformation</small>Hilltop, designed as one complete home</span></a>
            <a class="project-tile reveal" href="/projects/westmount-1970s-transformation/"><img src="/westmount-living-finish.jpg" alt="Finished Westmount living area after a layout change" loading="lazy"><span><small>1970s Westmount home</small>A new sense of flow</span></a>
            <a class="project-tile reveal" href="/projects/glass-block-bathroom-conversion/"><img src="/bathroom-walnut-vanity-after.jpg" alt="Completed tub-to-shower bathroom conversion" loading="lazy"><span><small>Before · during · after</small>Jetted tub to glass shower</span></a>
            <a class="project-tile project-wide reveal" href="/projects/pixie-paige-salon-repairs/"><img src="/salon-after-2.jpg" alt="Completed Pixie and Paige salon interior" loading="lazy"><span><small>Commercial · Pixie &amp; Paige</small>Repairing the damage without losing the character</span></a>
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
    return page("Renovations & Repairs London ON | Hekman Home Services", "Hekman Home Services provides London, Ontario renovations and repairs, including kitchens, bathrooms, flooring, drywall, handyman work and commercial maintenance.", "/", "hilltop-kitchen-wide.jpg", "home", body, "home")


def services_page() -> str:
    cards = "".join(service_card(slug, compact=True) for slug in SERVICES)
    body = f"""
    {hero("project-129.jpg", "Completed kitchen renovation", "Renovation & repair services", "Careful work for every part of the property.", "From bathrooms and kitchens to flooring, drywall, painting, pot lights, plumbing fixtures, doors, trim, insulation, fences, decks, handyman lists and commercial repairs—the connected work is planned as one complete scope.", small=True, secondary=("/projects/", "See Completed Work"), position="50% 58%")}
    <main id="main">
      <section class="section section-paper"><div class="wrap">{section_heading("Explore services", "From one repair to a complete transformation.", "Some projects fit one category. Others connect several. Explore the main services below, or send the whole scope and we will review it together.")}<div class="service-grid service-grid-compact">{cards}</div></div></section>
      <section class="section section-charcoal"><div class="wrap editorial-grid reverse"><div class="editorial-media reveal"><img src="/project-011.jpg" alt="Drywall preparation and finishing in progress" loading="lazy"><span>The work behind the finish</span></div><div class="editorial-copy reveal"><p class="eyebrow">Not sure where it fits?</p><h2>Describe the complete project.</h2><p>Photos, approximate measurements and a short explanation help us understand how the pieces connect. You do not need to sort the work into trades before contacting us.</p><a class="button button-primary" href="/contact/#quote">Tell Us About It</a></div></div></section>
    </main>"""
    return page("Renovation & Handyman Services London ON | Hekman", "Explore renovations, flooring, drywall, painting, pot lights, plumbing fixtures, handyman repairs, decks, fences and commercial maintenance in London, Ontario.", "/services/", "project-129.jpg", "services", body)


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
      </div>
    </section>
    """


def commercial_showcase() -> str:
    return f"""
    <section class="section section-paper commercial-showcase" id="pixie-paige">
      <div class="wrap">
        {section_heading("Commercial project spotlight", "Pixie & Paige salon: repair, rebuild and finish.", "One commercial maintenance project brought together water-damage repair, drywall restoration, lighting upgrades and a fixture repair while respecting the needs of an active salon.")}
        <article class="case-study reveal">
          <div class="case-study-copy">
            <p class="eyebrow">Pixie &amp; Paige · London</p>
            <h3>Restoring a working salon after a water leak</h3>
            <p>Damaged ceiling material was opened and removed so the affected area could be addressed. New drywall was installed, taped, finished and prepared for paint, with the surrounding commercial space brought back to a clean finish.</p>
            <ul>
              <li>Water-damaged ceiling and drywall removal</li>
              <li>Drywall rebuilding, taping, compound and finishing</li>
              <li>Lighting upgrades and related ceiling work</li>
              <li>Toilet repair and compatible maintenance items</li>
            </ul>
            <p class="case-note">The work moved through several affected areas of the salon—from opening damaged ceiling sections to rebuilding drywall and completing the surrounding finish.</p>
            <a class="text-link dark-link" href="/projects/pixie-paige-salon-repairs/">Read the full salon project story <span aria-hidden="true">↗</span></a>
          </div>
          <div class="case-study-media case-study-media-five">
            <figure><img src="/salon-water-damage-1.jpg" alt="Water-damaged ceiling opened at Pixie and Paige salon" loading="lazy"><figcaption>Damage documented</figcaption></figure>
            <figure><img src="/salon-water-damage-2.jpg" alt="Second affected ceiling area opened after the salon leak" loading="lazy"><figcaption>Affected material opened</figcaption></figure>
            <figure><img src="/salon-drywall-rebuild.jpg" alt="New drywall and compound during the salon rebuild" loading="lazy"><figcaption>Drywall rebuild</figcaption></figure>
            <figure><img src="/salon-after-1.jpg" alt="Completed Pixie and Paige salon stations and lighting" loading="lazy"><figcaption>Completed salon</figcaption></figure>
            <figure><img src="/salon-after-2.jpg" alt="Finished Pixie and Paige salon interior with mirrors and workstations" loading="lazy"><figcaption>Finished commercial space</figcaption></figure>
          </div>
        </article>
        <article class="case-study case-study-compact reveal">
          <div class="case-study-copy">
            <p class="eyebrow">Commercial facility work</p>
            <h3>Fitness-space ceiling and lighting improvements</h3>
            <p>Commercial ceiling access, lighting-related work and finishing were coordinated through an occupied fitness facility, with progress and completed-space photography kept together as one documented project.</p>
          </div>
          <div class="case-study-media case-study-media-three">
            <figure><img src="/project-045.jpg" alt="Commercial fitness-space ceiling and lighting detail" loading="lazy"><figcaption>Scope detail</figcaption></figure>
            <figure><img src="/project-049.jpg" alt="Commercial fitness-space ceiling work in progress" loading="lazy"><figcaption>Work in progress</figcaption></figure>
            <figure><img src="/project-046.jpg" alt="Completed fitness facility with upgraded lighting" loading="lazy"><figcaption>Completed facility</figcaption></figure>
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
    scope = "".join(f'<article class="proof-card reveal"><span>0{i}</span><h3>{title}</h3><p>{text}</p></article>' for i, (title, text) in enumerate(item["scope"], 1))
    bullets = "".join(f"<li>{bullet}</li>" for bullet in item["bullets"])
    gallery = "".join(f'<figure class="reveal"><img src="/{src}" alt="{html.escape(alt, quote=True)}" loading="lazy" decoding="async"><figcaption>{caption}</figcaption></figure>' for src, alt, caption in item["gallery"])
    faqs = "".join(f'<details class="reveal"><summary>{question}</summary><p>{answer}</p></details>' for question, answer in item["faq"])
    related = "".join(service_card(related_slug, compact=True) for related_slug in item["related"])
    showcase = bathroom_showcase() if slug == "bathrooms" else commercial_showcase() if slug == "commercial" else ""
    body = f"""
    {hero(item['hero'], item['hero_alt'], "London, Ontario", item['name'], item['lead'], small=True, position=item['position'])}
    <main id="main">
      <section class="section section-paper"><div class="wrap service-intro"><div class="reveal"><p class="eyebrow">Thoughtful project planning</p><h2>Built around what the space needs.</h2><p>{item['intro']}</p><a class="text-link dark-link" href="/contact/#quote">Discuss your project <span aria-hidden="true">↗</span></a></div><ul class="scope-list reveal">{bullets}</ul></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("What the work can include", "A complete scope, not disconnected pieces.", "The exact work depends on existing conditions, selected materials and the result you want.")}<div class="proof-grid">{scope}</div></div></section>
      {showcase}
      <section class="section section-stone"><div class="wrap">{section_heading("Details from real projects", "See what careful work looks like.", "Preparation, progress and finished spaces from Hekman Home Services work in London and nearby communities.")}<div class="gallery-grid">{gallery}</div><div class="section-actions reveal"><a class="button button-dark" href="/projects/">View More Projects</a></div></div></section>
      <section class="section section-paper"><div class="wrap faq-layout"><div class="reveal"><p class="eyebrow">Common questions</p><h2>Helpful before the walkthrough.</h2><p>The final scope depends on your property, materials and existing conditions.</p></div><div class="faq-list">{faqs}</div></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("Related services", "The connected work matters too.", "Many renovations involve more than one surface or room. These services are often part of the same conversation.")}<div class="service-grid related-grid">{related}</div></div></section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">Ready to talk it through?</p><h2>Show us the space.</h2><p>Send the location, a project description and the best way to reach you.</p></div><div><a class="button button-primary" href="/contact/#quote">Start Your Quote</a><a class="cta-phone" href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a></div></div></section>
    </main>"""
    return page(item["title"], item["description"], service_url(slug), item["hero"], "services", body, "service-page")


def hilltop_project_page() -> str:
    body = f"""
    {hero("hilltop-kitchen-wide.jpg", "Completed Hilltop kitchen and island", "Hekman project story · London, Ontario", "Hilltop: one home, one clear point of view.", "A whole-home transformation connecting the kitchen, bathroom, lower level, entry, stairs, flooring and finish details into a cohesive result.", small=True, position="50% 52%")}
    <main id="main">
      <section class="section section-paper"><div class="wrap service-intro story-summary"><div class="reveal"><p class="eyebrow">Whole-home transformation</p><h2>More than a collection of renovated rooms.</h2><p>Hilltop is the kind of project where every choice affects the next. The bright kitchen became an anchor, while flooring, stairs, the lower level, bathroom and entry were carried through with a consistent balance of warm wood, crisp white finishes and dark architectural details.</p><p>The completed-home photography shows how those decisions read together from one space to the next.</p></div><ul class="scope-list reveal"><li>Kitchen cabinetry, island and finish details</li><li>Bathroom renovation and glass shower</li><li>Lower-level living space</li><li>Flooring, stairs and transitions</li><li>Entry and interior finish work</li><li>Whole-home visual continuity</li></ul></div></section>
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
      <section class="section section-stone"><div class="wrap editorial-grid"><div class="editorial-media reveal"><img src="/hilltop-kitchen-wide.jpg" alt="Wide view across the Hilltop kitchen and dining space" loading="lazy"><span>A cohesive whole-home finish</span></div><div class="editorial-copy reveal"><p class="eyebrow">The design idea</p><h2>Consistency without making every room identical.</h2><p>Hilltop uses repeated cues—light cabinetry, warm flooring, dark railings and hardware, clean sightlines—to give the home a recognizable character. Each room still solves its own practical needs, but the transitions no longer feel accidental.</p><a class="text-link dark-link" href="/contact/#quote">Discuss a whole-home renovation <span aria-hidden="true">↗</span></a></div></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("Connected services", "The rooms are only part of the scope.", "Whole-home work brings layout, surfaces, storage and finishing into the same plan.")}<div class="service-grid related-grid">{service_card("kitchens", compact=True)}{service_card("bathrooms", compact=True)}{service_card("basements", compact=True)}</div></div></section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">Planning a bigger transformation?</p><h2>Start with the whole home.</h2><p>Show us the rooms, the frustrations and what you want the property to become.</p></div><div><a class="button button-primary" href="/contact/#quote">Request a Quote</a><a class="cta-phone" href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a></div></div></section>
    </main>"""
    return page("Hilltop Home Transformation | Hekman Home Services", "Explore Hekman Home Services’ Hilltop whole-home renovation in London, including the kitchen, bathrooms, lower level, stairs, flooring and finish work.", "/projects/hilltop-home-transformation/", "hilltop-kitchen-wide.jpg", "projects", body, "project-story-page")


def westmount_project_page() -> str:
    body = f"""
    {hero("westmount-living-finish.jpg", "Finished Westmount living room after the layout transformation", "1970s Westmount Beauty · London, Ontario", "A 1970s home, opened up and brought forward.", "The Westmount transformation reshaped how the home connects, then carried the new direction through flooring, trim, doors, stairs, closets, kitchen and bathroom work.", small=True, position="50% 52%")}
    <main id="main">
      <section class="section section-paper"><div class="wrap service-intro story-summary"><div class="reveal"><p class="eyebrow">Westmount Glow-Up</p><h2>Changing the flow meant starting with the structure.</h2><p>The old kitchen wall came down to change the relationship between the main living spaces. Temporary support and structural work came first; only then could the walls be closed and the new finish plan move forward.</p><p>Steph Hekman shaped the design direction for the project, connecting the layout change with new flooring, trim, doors, stairs, closets and room finishes throughout the home.</p></div><ul class="scope-list reveal"><li>Kitchen wall opening and layout change</li><li>Structural support during construction</li><li>Drywall closure and finish restoration</li><li>Flooring and stair updates</li><li>Trim, doors and closets</li><li>Kitchen and bathroom improvements</li></ul></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("From structure to finish", "The transformation happened in layers.", "These photographs follow the wall opening and the completed living and storage details that helped the 1970s home feel current again.")}<div class="story-mosaic story-mosaic-westmount">
        <figure class="story-feature"><img src="/westmount-wall-opening-1.jpg" alt="Temporary support at the Westmount wall opening" loading="lazy"><figcaption>Wall opening and temporary support</figcaption></figure>
        <figure><img src="/westmount-wall-opening-2.jpg" alt="Second view of structural support during the Westmount renovation" loading="lazy"><figcaption>Structural stage</figcaption></figure>
        <figure class="story-wide"><img src="/westmount-living-finish.jpg" alt="Completed Westmount living room with fireplace and new lighting" loading="lazy"><figcaption>Completed living space</figcaption></figure>
        <figure><img src="/westmount-closet-finish.jpg" alt="Finished Westmount closets, doors and plank flooring" loading="lazy"><figcaption>Closets, doors and flooring</figcaption></figure>
      </div></div></section>
      <section class="section section-stone"><div class="wrap">{section_heading("The work behind the reveal", "Open. Support. Close. Finish.", "A convincing layout transformation depends on the less glamorous stages being handled in the right order.")}<div class="proof-grid story-step-grid"><article class="proof-card reveal"><span>01</span><h3>Open the old layout</h3><p>Remove finishes and expose the conditions that determine the structural plan.</p></article><article class="proof-card reveal"><span>02</span><h3>Support the change</h3><p>Protect the structure while the new opening and required support are completed.</p></article><article class="proof-card reveal"><span>03</span><h3>Close the walls</h3><p>Restore drywall and connected surfaces around the new layout.</p></article><article class="proof-card reveal"><span>04</span><h3>Carry the finish through</h3><p>Connect flooring, trim, doors, closets, lighting and room details across the home.</p></article></div></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("Related expertise", "Layout work touches more than one trade.", "Structural planning, kitchen work and finished surfaces all have to meet cleanly.")}<div class="service-grid related-grid">{service_card("structural-layout", compact=True)}{service_card("kitchens", compact=True)}{service_card("flooring", compact=True)}</div></div></section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">Living with an outdated layout?</p><h2>Let’s look at what could open up.</h2><p>Send photos of the rooms and tell us how you want the home to work differently.</p></div><div><a class="button button-primary" href="/contact/#quote">Request a Quote</a><a class="cta-phone" href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a></div></div></section>
    </main>"""
    return page("1970s Westmount Home Transformation | Hekman Home Services", "See how Hekman Home Services transformed a 1970s Westmount home with a structural wall opening, new flow, flooring, trim, doors, closets and interior finishes.", "/projects/westmount-1970s-transformation/", "westmount-living-finish.jpg", "projects", body, "project-story-page")


def salon_project_page() -> str:
    body = f"""
    {hero("salon-after-2.jpg", "Completed Pixie and Paige salon after commercial repairs", "Commercial project · London, Ontario", "Pixie & Paige: restoring a working salon after a leak.", "Water-damaged ceiling and drywall, lighting upgrades and compatible maintenance work were coordinated into one commercial repair scope.", small=True, position="50% 56%")}
    <main id="main">
      <section class="section section-paper"><div class="wrap service-intro story-summary"><div class="reveal"><p class="eyebrow">Commercial repair &amp; restoration</p><h2>The damage crossed rooms. The repair had to connect them again.</h2><p>A water leak affected ceiling and drywall areas inside Pixie &amp; Paige. Damaged material was opened and removed, the areas were allowed to dry and prepared, then new drywall was installed, taped, compounded, sanded and painted.</p><p>The broader visit also included lighting upgrades, a toilet repair and related kitchenette work—grouping compatible maintenance so the salon could return to a clean, functional finish.</p></div><ul class="scope-list reveal"><li>Water-damaged ceiling and drywall removal</li><li>Drying and preparation of affected areas</li><li>New drywall, tape, compound and sanding</li><li>Primer, paint and finish restoration</li><li>Lighting upgrades</li><li>Fixture and kitchenette maintenance</li></ul></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("Inside the salon repair", "Damage, rebuild and the finished business space.", "The leak affected more than one viewpoint, so the story follows the scope across the salon rather than forcing a single-angle comparison.")}<div class="story-mosaic story-mosaic-salon">
        <figure class="story-feature"><img src="/salon-water-damage-1.jpg" alt="Water-damaged ceiling opened at Pixie and Paige salon" loading="lazy"><figcaption>Damage opened and documented</figcaption></figure>
        <figure><img src="/salon-water-damage-2.jpg" alt="Second affected ceiling area inside Pixie and Paige salon" loading="lazy"><figcaption>Another affected area</figcaption></figure>
        <figure><img src="/salon-drywall-rebuild.jpg" alt="New drywall and compound during the Pixie and Paige salon rebuild" loading="lazy"><figcaption>Drywall rebuild underway</figcaption></figure>
        <figure class="story-wide"><img src="/salon-after-1.jpg" alt="Completed Pixie and Paige salon stations and lighting" loading="lazy"><figcaption>Salon stations and lighting restored</figcaption></figure>
        <figure class="story-wide"><img src="/salon-after-2.jpg" alt="Finished Pixie and Paige salon with mirrors and workstations" loading="lazy"><figcaption>The completed salon</figcaption></figure>
      </div></div></section>
      <section class="section section-stone"><div class="wrap editorial-grid reverse"><div class="editorial-media reveal"><img src="/salon-after-1.jpg" alt="Long view through the completed salon interior" loading="lazy"><span>Commercial work with the business in mind</span></div><div class="editorial-copy reveal"><p class="eyebrow">Why the scope matters</p><h2>One repair visit can solve more than the visible damage.</h2><p>Commercial owners often have a primary problem and a list of connected maintenance needs. Grouping compatible drywall, ceiling, lighting, fixture and finish work creates a clearer path back to normal operations.</p><a class="text-link dark-link" href="/services/commercial/">Explore commercial maintenance <span aria-hidden="true">↗</span></a></div></div></section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">A repair affecting your business?</p><h2>Send us the scope and the space.</h2><p>Photos, access details and operating hours help us understand what the project requires.</p></div><div><a class="button button-primary" href="/contact/#quote">Request a Quote</a><a class="cta-phone" href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a></div></div></section>
    </main>"""
    return page("Pixie & Paige Salon Repairs | Hekman Home Services", "See Hekman Home Services repair water-damaged drywall and ceilings, upgrade lighting and complete maintenance work at Pixie & Paige salon in London, Ontario.", "/projects/pixie-paige-salon-repairs/", "salon-after-2.jpg", "projects", body, "project-story-page")


def kitchen_renewal_project_page() -> str:
    body = f"""
    {hero("kitchenette-after-wide.jpg", "Completed office kitchen with walnut-look cabinetry and gray counter", "Commercial kitchen project · London, Ontario", "A compact office kitchen, rebuilt around the work it needs to do.", "Old cabinetry came out, wall and plumbing access were addressed, and the staff space was rebuilt with clean-lined storage, a new counter, sink and finish details.", small=True, position="50% 52%")}
    <main id="main">
      <section class="section section-paper"><div class="wrap service-intro story-summary"><div class="reveal"><p class="eyebrow">Office kitchen · before · during · after</p><h2>A complete transformation without changing the room’s footprint.</h2><p>The original office kitchen had dark, aging cabinets, a worn counter and visible ceiling damage. Once the cabinetry was removed, the wall could be opened where needed for plumbing and repair access. New cabinet boxes and fronts were installed before the counter, sink, hardware, wall finish and ceiling were brought together.</p><p>The finished staff space keeps the practical appliances and familiar layout while giving the room more usable storage and a much cleaner working surface.</p></div><ul class="scope-list reveal"><li>Existing cabinetry and counter removal</li><li>Wall opening and plumbing access</li><li>Drywall patching and painting</li><li>New upper and lower cabinets</li><li>Counter, sink and hardware</li><li>Ceiling and final finish work</li></ul></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("The kitchen sequence", "The same wall, through every stage.", "A genuine before, build and completed series shows exactly how the old kitchen became the finished space.")}<div class="story-mosaic story-mosaic-kitchenette">
        <figure class="story-feature"><img src="/kitchenette-before-wide.jpg" alt="Wide view of the kitchen before renovation" loading="lazy"><figcaption>Before: existing kitchen</figcaption></figure>
        <figure><img src="/kitchenette-before-detail.jpg" alt="Existing cabinets, counter and ceiling damage before work" loading="lazy"><figcaption>Existing cabinetry and ceiling condition</figcaption></figure>
        <figure><img src="/kitchenette-wall-plumbing-stage.jpg" alt="Kitchen wall opened for plumbing and repair access" loading="lazy"><figcaption>Wall and plumbing access</figcaption></figure>
        <figure><img src="/kitchenette-cabinet-installation.jpg" alt="New kitchen cabinets being installed before the counter" loading="lazy"><figcaption>Cabinet installation</figcaption></figure>
        <figure class="story-wide"><img src="/kitchenette-after-detail.jpg" alt="Completed kitchen cabinetry, counter, sink and hardware" loading="lazy"><figcaption>After: cabinetry and counter complete</figcaption></figure>
        <figure class="story-wide"><img src="/kitchenette-after-wide.jpg" alt="Wide view of the completed compact kitchen" loading="lazy"><figcaption>The finished kitchen</figcaption></figure>
      </div></div></section>
      <section class="section section-stone"><div class="wrap">{section_heading("A closer look", "Walk through the completed cabinetry and counter.", "This short, compressed video waits until you press play, so it adds detail without slowing the first page load.")}<div class="video-grid video-grid-single"><figure class="work-video reveal"><video controls playsinline preload="metadata" poster="/kitchenette-after-detail.jpg" aria-label="Video walkthrough of completed kitchen cabinetry, sink and counter"><source src="/kitchenette-finish-tour.mp4" type="video/mp4">Your browser does not support embedded video.</video><figcaption><strong>Completed kitchen walkthrough</strong><span>Cabinet fronts, hardware, sink, counter and finished wall details.</span></figcaption></figure></div></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("Connected services", "Cabinets are only one part of a kitchen.", "Plumbing access, drywall, paint, trim and repair work all affect the finished result.")}<div class="service-grid related-grid">{service_card("commercial", compact=True)}{service_card("kitchens", compact=True)}{service_card("drywall-ceiling-repair", compact=True)}</div></div></section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">Have a kitchen that needs to work harder?</p><h2>Show us the room and the existing conditions.</h2><p>Wide photos and a short list of what you want to keep or change are enough to begin.</p></div><div><a class="button button-primary" href="/contact/#quote">Request a Quote</a><a class="cta-phone" href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a></div></div></section>
    </main>"""
    return page("Office Kitchen Renewal Before & After | Hekman", "See a genuine London office kitchen before, during and after renovation by Hekman Home Services, including cabinetry, plumbing access, drywall, counter and sink.", "/projects/kitchen-renewal/", "kitchenette-after-wide.jpg", "projects", body, "project-story-page")


def popcorn_project_page() -> str:
    body = f"""
    {hero("project-016.jpg", "Original textured ceiling before smoothing and finishing", "Ceiling transformation · London, Ontario", "From popcorn texture to a clean, modern ceiling.", "A preparation-heavy process documented from the original texture through sanding, skim coats, surface checks and primer.", small=True, position="50% 35%")}
    <main id="main">
      <section class="section section-paper"><div class="wrap service-intro story-summary"><div class="reveal"><p class="eyebrow">Popcorn ceiling removal</p><h2>The smooth finish is earned before the paint goes on.</h2><p>This London ceiling project moved through multiple rooms and multiple coats. The original texture and an existing ceiling patch were assessed first. The ceiling was sanded, coated and checked in stages, with the dining room and living space progressing at different points before final sanding and primer.</p><p>The dedicated ceiling sander helped control the surface work, while drop cloths and room protection kept the process contained.</p></div><ul class="scope-list reveal"><li>Existing texture and patch assessment</li><li>Floor, wall and opening protection</li><li>Mechanical ceiling sanding</li><li>Skim coating in controlled stages</li><li>Drying and surface checks</li><li>Final sanding, primer and paint preparation</li></ul></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("The ceiling process", "Before, during and finish stage.", "These images follow the same ceiling work from the original textured surface to the coated and primed stages.")}<div class="story-mosaic story-mosaic-popcorn">
        <figure class="story-feature"><img src="/project-016.jpg" alt="Textured ceiling and existing patch before smooth-ceiling work" loading="lazy"><figcaption>Before: texture and previous patch</figcaption></figure>
        <figure><img src="/popcorn-ceiling-sander.jpg" alt="Dust-covered ceiling sander used on the popcorn ceiling project" loading="lazy"><figcaption>The ceiling sander after use</figcaption></figure>
        <figure><img src="/project-017.jpg" alt="Skim coating underway with floors and walls protected" loading="lazy"><figcaption>Coating and room protection</figcaption></figure>
        <figure class="story-wide"><img src="/project-015.jpg" alt="Ceiling after texture removal and smooth coating work" loading="lazy"><figcaption>After removal: coating and surface correction</figcaption></figure>
        <figure class="story-wide"><img src="/popcorn-ceiling-primer.jpg" alt="Primer being rolled over the smoothed ceiling" loading="lazy"><figcaption>Primer and finish stage</figcaption></figure>
      </div></div></section>
      <section class="section section-stone"><div class="wrap">{section_heading("Why preparation leads the project", "Ceiling work touches the whole room.", "Protection, dust control and repeat surface checks matter just as much as the final coat.")}<div class="proof-grid"><article class="proof-card reveal"><span>01</span><h3>Protect the room</h3><p>Cover floors, isolate openings and plan access before overhead work begins.</p></article><article class="proof-card reveal"><span>02</span><h3>Build a flat surface</h3><p>Sand, coat, dry and repeat until the texture and repair lines no longer control the ceiling.</p></article><article class="proof-card reveal"><span>03</span><h3>Prime and inspect</h3><p>Primer helps reveal remaining imperfections before the ceiling receives its final finish.</p></article></div></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("Related services", "A ceiling issue may connect to other work.", "Drywall repairs, water damage and broader room renovations can be coordinated in the same conversation.")}<div class="service-grid related-grid">{service_card("popcorn-ceiling-removal", compact=True)}{service_card("drywall-ceiling-repair", compact=True)}{service_card("water-damage", compact=True)}</div></div></section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">Ready to lose the texture?</p><h2>Show us the ceiling and the rooms below it.</h2><p>Wide photos, close-ups and approximate room sizes are a useful place to start.</p></div><div><a class="button button-primary" href="/contact/#quote">Request a Quote</a><a class="cta-phone" href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a></div></div></section>
    </main>"""
    return page("Popcorn Ceiling Transformation London ON | Hekman Home Services", "See a Hekman Home Services popcorn ceiling project in London, Ontario, from the original textured ceiling through sanding, skim coating and primer.", "/projects/popcorn-ceiling-transformation/", "project-016.jpg", "projects", body, "project-story-page")


def glass_block_bathroom_project_page() -> str:
    body = f"""
    {hero("bathroom-walnut-vanity-after.jpg", "Completed glass shower conversion beside the original glass-block window", "Bathroom transformation", "From jetted tub to glass shower.", "One genuine bathroom sequence—from the original tub platform through demolition and open-wall work to the completed tiled shower.", small=True, position="50% 52%")}
    <main id="main">
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
      <section class="section section-charcoal"><div class="wrap">{section_heading("How the work connects", "A conversion is more than swapping one fixture.", "Demolition, access, water management and final fitting have to be planned as one sequence.")}<div class="proof-grid story-step-grid"><article class="proof-card reveal"><span>01</span><h3>Document the room</h3><p>Confirm what remains, what comes out and how the new shower fits the existing footprint.</p></article><article class="proof-card reveal"><span>02</span><h3>Open carefully</h3><p>Remove the tub platform and expose the wall and floor only where the new work requires access.</p></article><article class="proof-card reveal"><span>03</span><h3>Build the wet area</h3><p>Prepare the shower assembly, waterproofing, tile and plumbing connections in the correct order.</p></article><article class="proof-card reveal"><span>04</span><h3>Complete the room</h3><p>Fit the glass enclosure and reconnect trim, fixtures and surrounding finishes cleanly.</p></article></div></div></section>
      <section class="section section-paper"><div class="wrap">{section_heading("Related services", "Bathroom work often crosses several scopes.", "Flooring, drywall and fixture work can be reviewed as part of the same renovation.")}<div class="service-grid related-grid">{service_card("bathrooms", compact=True)}{service_card("flooring", compact=True)}{service_card("drywall-ceiling-repair", compact=True)}</div></div></section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">Considering a tub-to-shower conversion?</p><h2>Show us the whole bathroom.</h2><p>Wide photos, the existing fixtures and what you want to change are enough to start the conversation.</p></div><div><a class="button button-primary" href="/contact/#quote">Request a Quote</a><a class="cta-phone" href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a></div></div></section>
    </main>"""
    return page("Tub-to-Shower Bathroom Transformation | Hekman", "See a real jetted-tub-to-shower bathroom renovation by Hekman Home Services, documented from demolition and open-wall work through the finished glass shower.", "/projects/glass-block-bathroom-conversion/", "bathroom-walnut-vanity-after.jpg", "projects", body, "project-story-page")


PROJECTS = [
    # Kitchens: completed views and clearly identifiable installation details.
    ("hilltop-kitchen-wide.jpg", "kitchens", "Wide view of the completed Hilltop kitchen and island", "Hilltop kitchen", "Kitchen"),
    ("hilltop-kitchen-angle.jpg", "kitchens", "Angled view across the completed Hilltop kitchen", "Hilltop kitchen perspective", "Kitchen"),
    ("kitchenette-before-wide.jpg", "kitchens handyman commercial", "Office kitchen before cabinetry and repair work", "Office kitchen before", "Kitchen sequence"),
    ("kitchenette-wall-plumbing-stage.jpg", "kitchens handyman drywall commercial", "Office kitchen wall opened for plumbing and repair access", "Wall and plumbing access", "Kitchen sequence"),
    ("kitchenette-cabinet-installation.jpg", "kitchens handyman commercial", "New office kitchen cabinet boxes and fronts during installation", "Cabinet installation", "Kitchen sequence"),
    ("kitchenette-after-wide.jpg", "kitchens handyman commercial", "Completed office kitchen with walnut-look cabinets and gray counter", "Office kitchen after", "Kitchen sequence"),
    ("project-132.jpg", "kitchens", "Completed white kitchen with island seating", "White kitchen renovation", "Kitchen"),
    ("project-133.jpg", "kitchens", "Completed white kitchen cabinetry and appliances", "Cabinetry and appliance wall", "Kitchen"),
    ("project-135.jpg", "kitchens", "Completed kitchen cabinetry and counter detail", "Finished kitchen detail", "Kitchen"),
    ("project-136.jpg", "kitchens", "Kitchen island drawers and countertop", "Island storage detail", "Kitchen"),
    ("project-131.jpg", "kitchens", "Kitchen sink and backsplash detail", "Sink and backsplash", "Kitchen"),
    ("project-129.jpg", "kitchens", "Wide view of completed kitchen renovation", "Completed kitchen", "Kitchen"),
    ("project-113.jpg", "kitchens", "Kitchen cabinet installation in progress", "Cabinet installation", "Kitchen process"),
    ("project-107.jpg", "kitchens", "Kitchen renovation work in progress", "Kitchen build stage", "Kitchen process"),

    # Bathrooms: one verified tub-to-shower sequence plus separate projects shown individually.
    ("hilltop-bathroom-shower.jpg", "bathrooms", "Completed Hilltop bathroom with glass shower", "Hilltop glass shower", "Bathroom"),
    ("hilltop-bathroom-vanity.jpg", "bathrooms", "Completed Hilltop bathroom vanity and mirror", "Hilltop vanity", "Bathroom"),
    ("bathroom-glass-block-before.jpg", "bathrooms", "Bathroom with a jetted tub and glass-block window before conversion", "Before: jetted-tub layout", "Bathroom sequence"),
    ("bathroom-glass-block-demolition.jpg", "bathrooms", "Tiled jetted-tub platform partly removed during demolition", "Tub-platform demolition", "Bathroom sequence"),
    ("bathroom-glass-block-open-wall.jpg", "bathrooms insulation", "Tub removed with wall insulation and floor framing exposed", "Open wall and floor", "Bathroom sequence"),
    ("bathroom-walnut-vanity-after.jpg", "bathrooms flooring handyman", "Completed tub-to-shower conversion with a walnut vanity, gray tile and sliding glass door", "After: glass shower conversion", "Bathroom sequence"),
    ("project-144.jpg", "bathrooms", "Completed tiled bathroom shower", "Tiled shower", "Bathroom"),
    ("project-148.jpg", "bathrooms", "Completed bathroom with glass shower enclosure", "Glass shower renovation", "Bathroom"),
    ("project-150.jpg", "bathrooms", "Completed bathroom renovation with modern finishes", "Completed bathroom", "Bathroom"),
    ("project-155.jpg", "bathrooms flooring", "Existing tiled bathroom documented before renovation", "Existing bathroom before work", "Bathroom assessment"),
    ("project-157.jpg", "bathrooms", "Completed bathroom vanity and mirror", "Vanity and mirror", "Bathroom"),
    ("project-161.jpg", "bathrooms", "Completed bathroom with warm wood vanity", "Warm vanity finish", "Bathroom"),
    ("project-164.jpg", "bathrooms", "Completed bathroom with tiled wet area", "Bathroom finish", "Bathroom"),
    ("project-141.jpg", "bathrooms flooring", "Electric floor-heating system during bathroom construction", "Heated floor installation", "Bathroom process"),
    ("project-143.jpg", "bathrooms", "Bathroom tile and shower preparation in progress", "Tile preparation", "Bathroom process"),
    ("project-160.jpg", "bathrooms", "Waterproofing system during bathroom construction", "Shower waterproofing", "Bathroom process"),

    # Basements and lower-level finish work.
    ("hilltop-lower-level.jpg", "basements flooring", "Completed Hilltop lower-level living area with fireplace", "Hilltop lower level", "Basement"),
    ("project-067.jpg", "basements flooring", "Completed basement living space with wood flooring", "Finished basement", "Basement"),
    ("project-068.jpg", "basements", "Completed lower-level room with ceiling lighting", "Lower-level finish", "Basement"),
    ("project-066.jpg", "basements flooring", "Finished basement staircase and railing", "Stairs and railing", "Basement"),
    ("project-072.jpg", "basements flooring", "New plank flooring in a finished lower-level room", "Finished plank floor", "Basement flooring"),
    ("project-073.jpg", "basements flooring", "Continuous plank flooring through a finished lower level", "Lower-level flooring", "Basement flooring"),

    # Flooring: carpet conditions, subfloor, vinyl/plank, hardwood and tile.
    ("hilltop-staircase.jpg", "flooring basements", "Finished Hilltop staircase with dark railing", "Hilltop stairs", "Flooring / stairs"),
    ("hilltop-entry.jpg", "flooring basements", "Finished Hilltop entry and flooring transition", "Hilltop entry", "Flooring / transition"),
    ("project-037.jpg", "flooring", "Prepared subfloor with engineered hardwood materials on site", "Hardwood preparation", "Flooring"),
    ("project-038.jpg", "flooring", "Engineered wood flooring being installed", "Hardwood installation", "Flooring"),
    ("project-039.jpg", "flooring", "Wood-look flooring installation in progress", "Floor installation", "Flooring"),
    ("project-042.jpg", "flooring kitchens", "New plank flooring installed through a kitchen", "Kitchen plank flooring", "Flooring"),
    ("project-043.jpg", "flooring", "Dark wood flooring in a finished room", "Dark wood floor", "Flooring"),
    ("project-044.jpg", "flooring basements", "Light plank flooring in a completed room", "Light plank floor", "Flooring"),
    ("project-055.jpg", "flooring", "Existing carpet documented before flooring work", "Carpeted room assessment", "Carpet / preparation"),
    ("project-057.jpg", "flooring", "Plank flooring being installed in a residential room", "Plank installation", "Flooring process"),
    ("project-058.jpg", "flooring", "Click flooring installation detail", "Click-floor progress", "Flooring process"),
    ("project-060.jpg", "flooring", "Flooring installation and perimeter finishing in progress", "Installation detail", "Flooring process"),
    ("project-063.jpg", "flooring", "Tile flooring at a bright patio entry", "Tile and transition work", "Flooring"),
    ("hardwood-installation-detail.jpg", "flooring", "Dark engineered wood flooring being fastened during installation", "Engineered wood detail", "Flooring process"),

    # Drywall, ceilings and insulation.
    ("project-007.jpg", "drywall", "Ceiling surface repair in progress", "Ceiling preparation", "Drywall / ceiling"),
    ("project-010.jpg", "drywall", "Room protected for drywall and ceiling finishing", "Room protection", "Drywall / ceiling"),
    ("project-011.jpg", "drywall", "Drywall finishing in progress on walls and ceiling", "Taping and compound", "Drywall / ceiling"),
    ("project-014.jpg", "drywall", "Smooth finished ceiling in a completed room", "Smooth ceiling finish", "Drywall / ceiling"),
    ("project-015.jpg", "drywall", "Ceiling patch and compound work", "Ceiling repair", "Drywall / ceiling"),
    ("project-016.jpg", "drywall", "Ceiling compound drying before sanding", "Compound stage", "Drywall / ceiling"),
    ("project-017.jpg", "drywall", "Wall and ceiling finishing work in progress", "Finish preparation", "Drywall / ceiling"),
    ("popcorn-ceiling-sander.jpg", "drywall", "Dust-covered drywall sander used during popcorn ceiling removal", "Ceiling sanding equipment", "Popcorn ceiling"),
    ("popcorn-ceiling-primer.jpg", "drywall", "Primer being rolled onto a smoothed ceiling", "Ceiling primer stage", "Popcorn ceiling"),
    ("insulation-open-wall.jpg", "insulation drywall structural", "Opened wall and ceiling with insulation exposed", "Open-wall insulation", "Insulation"),
    ("insulation-drywall-stage.jpg", "insulation drywall", "Drywall being installed over insulated wall cavities", "Insulation and drywall", "Insulation"),
    ("insulation-open-ceiling.jpg", "insulation drywall", "Ceiling insulation exposed during repair work", "Ceiling insulation", "Insulation"),

    # Decks, fences, post work and other exterior carpentry.
    ("project-103.jpg", "exterior", "Completed elevated wood deck behind a brick home", "Completed elevated deck", "Deck"),
    ("project-104.jpg", "exterior", "Long completed residential deck structure", "Multi-unit deck work", "Deck"),
    ("project-100.jpg", "exterior", "Wood deck with completed railing", "Deck and railing", "Deck"),
    ("project-101.jpg", "exterior structural", "Deck framing and support-post structure", "Deck structure", "Deck process"),
    ("project-093.jpg", "exterior", "Deck boards and framing during construction", "Deck construction", "Deck process"),
    ("project-096.jpg", "exterior structural", "Residential deck framing in progress", "Deck framing", "Deck process"),
    ("fence-after-1.jpg", "exterior", "Completed long-run wood privacy fence", "Privacy fence", "Fence"),
    ("fence-after-2.jpg", "exterior", "Completed wood privacy fence and posts", "Fence and posts", "Fence"),
    ("post-hole-digging.jpg", "exterior", "Post hole being dug by hand beside a residential property", "Post-hole preparation", "Fence / post work"),
    ("post-hole-auger.jpg", "exterior", "Powered auger digging a post hole", "Powered auger work", "Fence / post work"),

    # Interior framing and layout work.
    ("westmount-wall-opening-1.jpg", "structural", "Temporary structural support at the Westmount wall opening", "Westmount wall opening", "Structural / layout"),
    ("westmount-wall-opening-2.jpg", "structural", "Second view of support during the Westmount layout change", "Westmount structural stage", "Structural / layout"),
    ("westmount-living-finish.jpg", "structural flooring", "Finished Westmount living room after the layout change", "Westmount living finish", "Structural / finish"),
    ("westmount-closet-finish.jpg", "structural flooring", "Finished Westmount closets, doors and plank flooring", "Westmount closets", "Layout / storage"),
    ("project-025.jpg", "structural", "Interior framing exposed during a layout renovation", "Layout opening", "Structural / layout"),
    ("project-031.jpg", "structural", "Doorway framing during an interior renovation", "New opening and framing", "Structural / layout"),
    ("project-138.jpg", "structural kitchens", "New wall framing beside a kitchen renovation", "Interior framing", "Structural / layout"),
    ("project-026.jpg", "structural", "Finished closet doors after an interior build", "Finished storage", "Layout / storage"),

    # Handyman, repair, painting and lighting work.
    ("project-027.jpg", "handyman structural", "Doorway and trim work during a residential repair", "Door and trim work", "Handyman repair"),
    ("project-032.jpg", "handyman drywall", "Drywall patching and compound on an interior wall", "Drywall patch", "Handyman repair"),
    ("project-140.jpg", "handyman bathrooms", "Painting and finish work in a bathroom", "Painting and finish work", "Handyman repair"),
    ("project-139.jpg", "handyman bathrooms", "Bathroom toilet and flooring installation detail", "Bathroom fixture detail", "Handyman repair"),
    ("drywall-potlight-progress-poster.jpg", "handyman drywall structural", "Drywall finishing and pot lights during an interior renovation", "Drywall and pot lights", "Lighting / drywall"),

    # Commercial projects: Pixie & Paige salon and a fitness facility.
    ("salon-water-damage-1.jpg", "commercial drywall", "Water-damaged ceiling opened at Pixie and Paige salon", "Salon water-damage repair", "Commercial"),
    ("salon-water-damage-2.jpg", "commercial drywall", "Second affected ceiling area opened after the salon leak", "Affected ceiling opened", "Commercial"),
    ("salon-drywall-rebuild.jpg", "commercial drywall", "New drywall and compound during the salon rebuild", "Salon drywall rebuild", "Commercial"),
    ("salon-after-1.jpg", "commercial", "Completed Pixie and Paige salon stations and lighting", "Finished salon interior", "Commercial"),
    ("salon-after-2.jpg", "commercial", "Finished Pixie and Paige salon with mirrors and workstations", "Pixie & Paige salon", "Commercial"),
    ("project-045.jpg", "commercial", "Commercial fitness-space ceiling and lighting detail", "Fitness-space scope", "Commercial"),
    ("project-049.jpg", "commercial drywall", "Commercial fitness-space ceiling work in progress", "Fitness-space progress", "Commercial"),
    ("project-046.jpg", "commercial", "Completed fitness facility with upgraded lighting", "Completed fitness facility", "Commercial"),
    ("project-050.jpg", "commercial", "Commercial fitness interior after maintenance work", "Commercial interior", "Commercial"),
    ("project-054.jpg", "commercial", "Finished commercial fitness-space interior", "Finished commercial space", "Commercial"),
]


def projects_page() -> str:
    cards = "".join(f'<figure class="project-card reveal" data-category="{categories}"><button class="project-image" type="button" data-lightbox aria-label="Enlarge {html.escape(label, quote=True)}"><img src="/{src}" alt="{html.escape(alt, quote=True)}" loading="lazy" decoding="async"></button><figcaption><span>{label}</span><small>{tag}</small></figcaption></figure>' for src, categories, alt, label, tag in PROJECTS)
    filters = [("all", "All Work"), ("kitchens", "Kitchens"), ("bathrooms", "Bathrooms"), ("basements", "Basements"), ("flooring", "Flooring"), ("drywall", "Drywall & Ceilings"), ("insulation", "Insulation"), ("exterior", "Decks & Fences"), ("structural", "Structural"), ("handyman", "Handyman & Repairs"), ("commercial", "Commercial")]
    buttons = "".join(f'<button type="button" class="filter-button{" active" if key == "all" else ""}" data-filter="{key}" aria-pressed="{"true" if key == "all" else "false"}">{label}</button>' for key, label in filters)
    body = f"""
    {hero("hilltop-kitchen-wide.jpg", "Completed Hilltop kitchen renovation", "Our work · London, Ontario", "Work that holds up to a closer look.", "Explore whole-home transformations, kitchens, bathrooms, basements, carpet, vinyl and hardwood flooring, drywall, pot lights, painting, insulation, decks, fences, handyman repairs, structural changes and commercial work.", small=True, position="50% 54%")}
    <main id="main">
      <section class="section section-paper"><div class="wrap">{section_heading("Project stories", "Six transformations. Six very different challenges.", "Step inside Hilltop, a 1970s Westmount home, a genuine tub-to-shower conversion, Pixie & Paige salon, a compact office kitchen and a London popcorn-ceiling transformation.")}
        <div class="story-card-grid">
          <a class="story-card story-card-large reveal" href="/projects/hilltop-home-transformation/"><img src="/hilltop-kitchen-angle.jpg" alt="Completed Hilltop kitchen" loading="lazy"><span><small>Whole-home transformation</small><strong>Hilltop</strong><b>Kitchen, bathroom, lower level, stairs and finish work <i aria-hidden="true">↗</i></b></span></a>
          <a class="story-card reveal" href="/projects/glass-block-bathroom-conversion/"><img src="/bathroom-walnut-vanity-after.jpg" alt="Completed tub-to-shower bathroom conversion" loading="lazy"><span><small>Before · during · after</small><strong>Jetted tub to glass shower</strong><b>Demolition, open-wall work, tile and enclosure <i aria-hidden="true">↗</i></b></span></a>
          <a class="story-card reveal" href="/projects/westmount-1970s-transformation/"><img src="/westmount-living-finish.jpg" alt="Finished Westmount living room" loading="lazy"><span><small>1970s Westmount Beauty</small><strong>A new sense of flow</strong><b>Wall opening, flooring, trim, doors and closets <i aria-hidden="true">↗</i></b></span></a>
          <a class="story-card reveal" href="/projects/pixie-paige-salon-repairs/"><img src="/salon-after-2.jpg" alt="Completed Pixie and Paige salon" loading="lazy"><span><small>Commercial repair</small><strong>Pixie &amp; Paige</strong><b>Water damage, drywall, lighting and maintenance <i aria-hidden="true">↗</i></b></span></a>
          <a class="story-card reveal" href="/projects/kitchen-renewal/"><img src="/kitchenette-after-wide.jpg" alt="Completed office kitchen with walnut-look cabinetry" loading="lazy"><span><small>Commercial · before · during · after</small><strong>Office kitchen renewal</strong><b>Cabinetry, plumbing access, drywall, counter and finish work <i aria-hidden="true">↗</i></b></span></a>
          <a class="story-card story-card-wide reveal" href="/projects/popcorn-ceiling-transformation/"><img src="/popcorn-ceiling-sander.jpg" alt="Ceiling sander used during popcorn ceiling removal" loading="lazy"><span><small>Before · during · finish stage</small><strong>Popcorn ceiling transformation</strong><b>Sand, skim, check and prime <i aria-hidden="true">↗</i></b></span></a>
        </div>
      </div></section>
      <section class="section section-stone"><div class="wrap">{section_heading("Work in motion", "Three short project videos.", "Each video is compressed, never autoplays and waits until you press play—giving you a closer look without slowing the first page load.")}<div class="video-grid video-grid-three"><figure class="work-video reveal"><video controls playsinline preload="none" poster="/bathroom-walnut-vanity-after.jpg" aria-label="Video of a jetted-tub bathroom being converted into a glass shower"><source src="/bathroom-glass-block-transformation.mp4" type="video/mp4">Your browser does not support embedded video.</video><figcaption><strong>Tub-to-shower transformation</strong><span>The verified bathroom sequence from demolition through completion.</span></figcaption></figure><figure class="work-video reveal"><video controls playsinline preload="none" poster="/kitchenette-after-detail.jpg" aria-label="Video walkthrough of the completed kitchen cabinetry and counter"><source src="/kitchenette-finish-tour.mp4" type="video/mp4">Your browser does not support embedded video.</video><figcaption><strong>Completed kitchen</strong><span>A closer view of the cabinets, hardware, sink and counter.</span></figcaption></figure><figure class="work-video reveal"><video controls playsinline preload="none" poster="/drywall-potlight-progress-poster.jpg" aria-label="Video of drywall finishing and pot lights during renovation"><source src="/drywall-potlight-progress.mp4" type="video/mp4">Your browser does not support embedded video.</video><figcaption><strong>Drywall &amp; pot-light progress</strong><span>Walls, ceiling repairs and new lighting during the finish stage.</span></figcaption></figure></div></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("Explore the work", "Find the room, surface or scope that matches your project.", "Filter through residential renovations, finish work, exterior construction and commercial repairs completed by Hekman Home Services.")}<div class="filter-bar" aria-label="Filter project photographs">{buttons}</div><div class="projects-grid" id="projects-grid" aria-live="polite">{cards}</div><p class="filter-status" data-filter-status>Showing all {len(PROJECTS)} photographs.</p></div></section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">Picture your own project?</p><h2>Start with a few details.</h2><p>Tell us what you want to change and where the property is located.</p></div><div><a class="button button-primary" href="/contact/#quote">Request a Quote</a><a class="cta-phone" href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a></div></div></section>
      <dialog class="lightbox" data-lightbox-dialog><button type="button" class="lightbox-close" data-lightbox-close aria-label="Close image">×</button><img src="" alt=""><p></p></dialog>
    </main>"""
    return page("Renovation Projects London ON | Hekman Home Services", "Explore genuine whole-home, kitchen, bathroom, basement, flooring, drywall, insulation, deck, fence, structural and commercial projects by Hekman Home Services.", "/projects/", "hilltop-kitchen-wide.jpg", "projects", body, "projects-page")


def about_page() -> str:
    body = f"""
    {hero("project-070.jpg", "Hekman Home Services team gathered around project plans", "About Hekman Home Services", "A husband-and-wife team, close to every project.", "Rene and Steph Hekman bring hands-on construction, thoughtful design and direct communication together for homes and properties across London, Ontario.", small=True, position="50% 42%")}
    <main id="main">
      <section class="section section-paper"><div class="wrap editorial-grid about-story"><div class="editorial-copy reveal"><p class="eyebrow">The Hekman approach</p><h2>The people you speak with are part of the work.</h2><p>Hekman Home Services is owned and operated by Rene and Steph Hekman. Together they combine more than 20 years of hands-on renovation and repair experience with the planning, sales and design perspective that helps a project feel considered from the first walkthrough to the final details.</p><p>That closeness matters. Existing conditions are discussed, choices are connected to the whole property and the client is never handed off to an anonymous process. The work stays grounded in a simple idea: fix it properly, communicate clearly and leave the space feeling complete.</p><p class="signature-line">Fix it. Sell it. Celebrate it.</p></div><div class="editorial-media reveal"><img src="/project-079.jpg" alt="Hekman Home Services team reviewing plans" loading="lazy"><span>Planning the work together</span></div></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("What guides the work", "Professional does not have to feel impersonal.", "The strongest projects come from good preparation, honest conversations and care for the property throughout the work.")}<div class="values-grid"><article class="reveal"><span>01</span><h3>Listen first</h3><p>Understand the problem, priorities and intended result before defining the work.</p></article><article class="reveal"><span>02</span><h3>Protect the property</h3><p>Preparation, dust control and cleanup are treated as part of the project.</p></article><article class="reveal"><span>03</span><h3>Communicate clearly</h3><p>When existing conditions affect the plan, explain what changed and why.</p></article><article class="reveal"><span>04</span><h3>Finish thoughtfully</h3><p>Trim, transitions and final details matter because they are what make the work feel complete.</p></article></div></div></section>
      <section class="section section-stone"><div class="wrap people-grid"><article class="person-card reveal"><img src="/project-075.jpg" alt="Rene Hekman, Director and Contractor at Hekman Home Services" loading="lazy"><div><p class="eyebrow">Director · Contractor</p><h2>Rene Hekman</h2><p>Rene leads construction in the field—from opening walls and solving repair conditions to the practical preparation and finish work that make a renovation hold together. His role stays hands-on throughout the project.</p></div></article><article class="person-card reveal"><img src="/project-076.jpg" alt="Steph Hekman, Customer Relations, Sales and Design at Hekman Home Services" loading="lazy"><div><p class="eyebrow">Customer Relations · Sales &amp; Design</p><h2>Steph Hekman</h2><p>Steph guides client communication, project planning and design decisions. Her eye for how rooms connect shaped transformations such as the 1970s Westmount project, where layout, flooring, trim, doors and finishes had to read as one home.</p></div></article></div></section>
      <section class="section section-paper"><div class="wrap area-layout"><div class="reveal"><p class="eyebrow">Local service</p><h2>Working throughout London and nearby communities.</h2><p>Based in London, Hekman Home Services works in neighbourhoods including Westmount, Byron, Oakridge, Riverbend, Masonville, Old South and Hyde Park, as well as St. Thomas and nearby areas.</p><a class="button button-dark" href="/contact/">Contact Rene &amp; Steph</a></div><div class="assurance-panel reveal"><strong>Fully insured &amp; bondable</strong><span>Professional protection for residential and commercial projects.</span><strong>2-year workmanship guarantee</strong><span>Workmanship is backed after the final walkthrough.</span><strong>Real project proof</strong><span>Explore completed spaces and the work behind them.</span></div></div></section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">Let’s discuss your property.</p><h2>Start with the space and the goal.</h2><p>We will help make sense of the connected work from there.</p></div><div><a class="button button-primary" href="/contact/#quote">Request a Quote</a><a class="cta-phone" href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a></div></div></section>
    </main>"""
    return page("About Rene & Steph Hekman | Hekman Home Services", "Meet Rene and Steph Hekman, the husband-and-wife team behind Hekman Home Services, providing hands-on renovations and repairs in London, Ontario.", "/about/", "project-070.jpg", "about", body, "about-page")


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
    return page("Page Not Found | Hekman Home Services", "The requested page could not be found.", "/404.html", "project-132.jpg", "", body, "error-page", indexable=False)


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
    write("projects/hilltop-home-transformation/index.html", hilltop_project_page())
    write("projects/westmount-1970s-transformation/index.html", westmount_project_page())
    write("projects/pixie-paige-salon-repairs/index.html", salon_project_page())
    write("projects/kitchen-renewal/index.html", kitchen_renewal_project_page())
    write("projects/popcorn-ceiling-transformation/index.html", popcorn_project_page())
    write("projects/glass-block-bathroom-conversion/index.html", glass_block_bathroom_project_page())
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
        "handyman.html": ("/services/handyman-repairs/", "Handyman & Home Repairs | Hekman Home Services"),
        "structural-layout.html": ("/services/structural-layout/", "Structural & Layout Changes | Hekman Home Services"),
    }
    for filename, (destination, title) in legacy.items():
        write(filename, redirect_stub(destination, title))
    write("reviews/index.html", redirect_stub("/projects/", "Our Work | Hekman Home Services"))

    project_urls = [
        "/projects/hilltop-home-transformation/",
        "/projects/westmount-1970s-transformation/",
        "/projects/pixie-paige-salon-repairs/",
        "/projects/kitchen-renewal/",
        "/projects/popcorn-ceiling-transformation/",
        "/projects/glass-block-bathroom-conversion/",
    ]
    urls = ["/", "/services/", *[service_url(slug) for slug in SERVICES], "/projects/", *project_urls, "/about/", "/contact/"]
    sitemap_urls = "\n".join(f"  <url><loc>{BASE_URL}{url}</loc></url>" for url in urls)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sitemap_urls}\n</urlset>')
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml")
    write("llms.txt", f"""
    # Hekman Home Services Inc.

    > Husband-and-wife-led renovation, repair and property improvement company serving London, Ontario and surrounding communities.

    Canonical website: {BASE_URL}/
    Phone: {PHONE_DISPLAY}
    Email: {EMAIL}

    ## Core services
    {chr(10).join(f'- {item["name"]}: {BASE_URL}{service_url(slug)}' for slug, item in SERVICES.items())}

    ## Service area
    London, Ontario, including Westmount, Byron, Oakridge, Riverbend, Masonville, Old South and Hyde Park; St. Thomas and nearby communities where appropriate.

    ## Selected project stories
    - Hilltop whole-home transformation: {BASE_URL}/projects/hilltop-home-transformation/
    - 1970s Westmount home transformation: {BASE_URL}/projects/westmount-1970s-transformation/
    - Pixie & Paige salon commercial repairs: {BASE_URL}/projects/pixie-paige-salon-repairs/
    - Office kitchen renewal, before through completion: {BASE_URL}/projects/kitchen-renewal/
    - Popcorn ceiling transformation: {BASE_URL}/projects/popcorn-ceiling-transformation/
    - Jetted-tub to glass-shower bathroom conversion: {BASE_URL}/projects/glass-block-bathroom-conversion/

    ## Business identity
    Hekman Home Services Inc. is led by Rene and Steph Hekman. The company provides residential renovation and repair work plus commercial maintenance and repairs. It is fully insured and bondable and provides a 2-year workmanship guarantee.

    Official social profiles:
    - Instagram: {INSTAGRAM}
    - Facebook: {FACEBOOK}
    """)


if __name__ == "__main__":
    build()
