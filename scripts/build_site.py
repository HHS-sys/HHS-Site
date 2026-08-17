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
    "Sunningdale",
    "Old North",
    "Stoneybrook",
    "Byron",
    "Oakridge",
    "Riverbend",
    "Medway",
    "Hyde Park",
    "Old East Village",
    "Masonville",
    "Old South",
    "St. Thomas",
]

PROJECT_DETAILS: dict[str, dict] = {
    "/projects/melrose-bathroom-layout/": {
        "name": "Melrose: A Bathroom Reworked From the Layout Out",
        "description": "A Melrose-area bathroom and lower-level project that moved the room through a wall, added a utility room and finished a new exercise room.",
        "image": "melrose-bathroom-after.jpg",
        "image_alt": "Completed Melrose-area bathroom with a wall-hung toilet, tiled shower, vanity and illuminated mirror",
        "neighbourhood": "Melrose area, London, Ontario",
        "status": "Completed",
        "services": ["Bathroom layout change", "Utility-room construction", "Drywall, ceiling and paint"],
    },
    "/projects/hyde-park-kitchen-renewal/": {
        "name": "Hyde Park: A Kitchen Renewed Without Starting Over",
        "description": "A Hyde Park kitchen renewal with refaced cabinetry, a new pantry, reconfigured appliances, dishwasher, backsplash, counters and sink.",
        "image": "hyde-park-kitchen-after.jpg",
        "image_alt": "Completed Hyde Park kitchen with refaced cabinetry, new counters, sink and backsplash",
        "neighbourhood": "Hyde Park, London, Ontario",
        "status": "Completed",
        "services": ["Cabinet refacing", "Pantry and appliance layout", "Backsplash, counters and sink"],
    },
    "/projects/blackfriars-leak-restoration/": {
        "name": "Blackfriars: A Small Leak That Needed a Much Bigger Plan",
        "description": "A Blackfriars leak investigation and restoration that uncovered mold, evidence of mice, structural concerns and knob-and-tube wiring.",
        "image": "blackfriars-restored-room.jpg",
        "image_alt": "Restored Blackfriars room with a smooth finished ceiling and painted walls",
        "neighbourhood": "Blackfriars, London, Ontario",
        "status": "Completed",
        "services": ["Investigation and project coordination", "Structural and trade coordination", "Drywall, ceiling and finish restoration"],
    },
    "/projects/medway-flooring-storage/": {
        "name": "Medway: More Storage, Better Flow and a Seamless Upper Level",
        "description": "An anonymous Medway flooring and storage project with carpet removal in three rooms, relocated and new closets, plank flooring, doors, casing and baseboards.",
        "image": "medway-floor-door-transition.jpg",
        "image_alt": "Completed Medway doorway with cool gray-brown plank flooring and a clean transition",
        "neighbourhood": "Medway, London, Ontario",
        "status": "Completed",
        "services": ["Flooring installation", "Closet and storage changes", "Doors, casing and baseboards"],
    },
    "/projects/westmount-porch-entry/": {
        "name": "A Westmount Porch and Entry, Modernized by Neighbours",
        "description": "A repeat Westmount customer’s porch and entry revitalization, shown through careful progress work, a daytime completion view and the finished exterior lighting at night.",
        "image": "westmount-porch-after-night.jpg",
        "image_alt": "Finished Westmount porch and entry illuminated at night",
        "neighbourhood": "Westmount, London, Ontario",
        "status": "Completed",
        "services": ["Exterior repairs", "Porch and entry finishing", "Handyman work"],
    },
    "/projects/westmount-1970s-transformation/": {
        "name": "Westmount: A Home Transformation Built in Thoughtful Phases",
        "description": "An ongoing Westmount transformation completed in phases around the clients’ timing and budget, including layout, flooring, lighting, kitchen work and one powder room.",
        "image": "westmount-transformation-blue-wall-flooring.jpg",
        "image_alt": "Completed Westmount living-space phase with plank flooring, pot lights and a deep-blue feature wall",
        "neighbourhood": "Westmount, London, Ontario",
        "status": "Project in progress",
        "services": ["Layout changes", "Kitchen work", "One powder-room renovation", "Flooring, lighting and finishing"],
    },
}

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
            ("hilltop-green-tile-before.jpg", "Hilltop bathroom with its original green-tile tub surround", "Hilltop before: green-tile surround"),
            ("hilltop-green-tile-after.jpg", "Completed Hilltop tub surround with marble-look tile and dark accent trim", "Hilltop after: rebuilt tub surround"),
            ("hilltop-basement-bathroom-before.jpg", "Hilltop basement bathroom before the shower, ceiling and finishes were renewed", "Hilltop basement bathroom before"),
            ("hilltop-basement-bathroom-wide.jpg", "Completed Hilltop basement bathroom with white vanity and glass shower", "Hilltop basement bathroom after"),
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
            ("medway-floor-door-transition.jpg", "Completed Medway door, cool gray-brown plank flooring and clean transition", "Medway completed transition"),
            ("medway-floor-installation.jpg", "Plank flooring being installed in the Medway upper level", "Medway installation in progress"),
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
        "name": "Restoration & Damage Repairs",
        "card_name": "Restoration & Damage",
        "title": "Water Damage & Restoration Repairs London ON | Hekman",
        "description": "Restorative construction and water-damage repairs in London, Ontario, including damaged drywall, ceilings, flooring, trim, insulation and finish work.",
        "hero": "salon-water-damage-2.jpg",
        "hero_alt": "Damaged ceiling opened to reveal the area requiring restorative repair",
        "position": "50% 45%",
        "lead": "When damage interrupts a home or business, rebuild the affected space with one clear plan—from opening the problem area to restoring the final finish.",
        "intro": "Restoration work rarely begins as a planned renovation. It may start with a leak, a damaged ceiling, an opened wall or a repair that left the room unfinished. Once the source and any immediate safety concerns have been addressed, Hekman Home Services can coordinate the construction work that puts the affected space back together.",
        "scope": [
            ("Understand what was affected", "Document the visible damage and identify which walls, ceilings, floors, insulation or finishes belong in the repair scope."),
            ("Open, repair & rebuild", "Remove affected finishes where required, complete the agreed rebuilding work and coordinate the connected surfaces in the right order."),
            ("Make the space feel whole again", "Drywall, trim, transitions, primer and paint bring the repair back into the surrounding home or business."),
        ],
        "bullets": ["Repairs after leaks and water damage", "Damaged drywall and ceiling rebuilding", "Insulation and wall-cavity restoration", "Flooring, trim and baseboard repair", "Residential and commercial restoration", "Primer, paint and final finish work"],
        "gallery": [
            ("salon-water-damage-2.jpg", "Damaged ceiling opened to expose the affected construction", "Ceiling damage opened for investigation and repair"),
            ("salon-drywall-rebuild.jpg", "Ceiling and wall surfaces being rebuilt with new drywall and compound", "Wall and ceiling surfaces rebuilt after repairs"),
            ("salon-after-1.jpg", "Bright working salon after water-damage restoration", "Salon returned to working condition"),
            ("project-014.jpg", "Smooth completed ceiling after repair and finish work", "A smooth ceiling finish restored"),
        ],
        "faq": [
            ("Do you stop the active leak?", "The source should be identified and corrected first. Our scope can focus on removal, repair and rebuilding afterward."),
            ("Can drywall and flooring be repaired together?", "Yes. One quote can include several affected finishes where appropriate."),
            ("Can you review an insurance repair scope?", "We can review the requested work and prepare our own quote based on the actual site conditions and repair scope."),
        ],
        "related": ["drywall-ceiling-repair", "commercial", "handyman-repairs"],
    },
    "commercial": {
        "name": "Commercial Maintenance & Repairs",
        "card_name": "Commercial Work",
        "title": "Commercial Maintenance London ON | Hekman Home Services",
        "description": "Commercial maintenance and repairs in London, Ontario, including salon, fitness, retail, office-kitchen, drywall, lighting and repair work.",
        "hero": "salon-after-2.jpg",
        "hero_alt": "Completed London salon interior after commercial repair work",
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
            ("salon-after-2.jpg", "Completed London salon interior", "Salon commercial work"),
            ("project-045.jpg", "Original box-style fluorescent fixtures in a London fitness facility", "Before: older light fixtures"),
            ("project-049.jpg", "Hekman Home Services team replacing commercial lighting from scaffolding and ladders", "During: lighting replacement"),
            ("project-048.jpg", "Fitness facility illuminated by the completed LED lighting upgrade", "After: LED lighting"),
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
            ("westmount-porch-after-day.jpg", "Finished anonymous Westmount porch and entry in daylight", "Westmount porch and entry"),
            ("medway-floor-door-transition.jpg", "Completed Medway door, flooring and transition detail", "Door and flooring finish"),
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
        "hero": "westmount-transformation-demolition.jpg",
        "hero_alt": "Westmount main-floor demolition and layout changes in progress",
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
            ("westmount-transformation-demolition.jpg", "Westmount main-floor demolition and layout changes in progress", "Westmount layout phase"),
            ("medway-closet-before.jpg", "Medway room with carpet and the new closet opening visible", "Medway closet layout"),
            ("medway-closet-relocation-progress.jpg", "Former Medway closet opening closed and prepared as a seamless wall", "Closet opening relocated"),
            ("medway-floor-door-transition.jpg", "Completed Medway doorway, flooring and clean transition", "Connected doors, trim and flooring"),
        ],
        "faq": [
            ("Can you remove a wall?", "Potential wall changes must be assessed first. Structural walls require appropriate engineering, permits and supporting work."),
            ("Can you build a new closet?", "Yes. Framing, drywall, doors and trim can be included in the scope."),
            ("Do layout changes require permits?", "Some do. Requirements depend on structural, plumbing, electrical and other systems affected by the work."),
        ],
        "related": ["kitchens", "basements", "drywall-ceiling-repair"],
    },
}


# Keep the customer-facing hierarchy intentional. The first five services are
# the core order approved for the homepage and service index.
SERVICE_DISPLAY_ORDER = [
    "bathrooms",
    "drywall-ceiling-repair",
    "kitchens",
    "flooring",
    "basements",
    "handyman-repairs",
    "decks-exterior",
    "water-damage",
    "commercial",
    "structural-layout",
    "popcorn-ceiling-removal",
]


# Cards use verified alternatives so the site does not repeat one hero image on
# the homepage, service index and every related-service section. These are not
# inferred before/after pairings; each image is used only as individual proof of
# the service shown.
SERVICE_CARD_VARIANTS: dict[str, list[tuple[str, str]]] = {
    "bathrooms": [
        ("hilltop-green-tile-after.jpg", "Completed Hilltop bathroom with a marble-look tub surround"),
        ("hilltop-basement-bathroom-wide.jpg", "Completed Hilltop basement bathroom with a glass shower"),
        ("project-148.jpg", "Completed bathroom with a glass shower enclosure"),
        ("project-161.jpg", "Completed bathroom with a warm wood vanity and black fixtures"),
        ("bathroom-walnut-vanity-after.jpg", "Completed tub-to-shower conversion with a walnut vanity"),
    ],
    "drywall-ceiling-repair": [
        ("project-011.jpg", "Drywall and ceiling finishing in progress"),
        ("project-007.jpg", "Drywall preparation during an interior renovation"),
        ("insulation-drywall-stage.jpg", "Drywall being installed over insulated wall cavities"),
        ("project-152.jpg", "Wall-board rebuilding around a frosted bathroom window"),
        ("project-014.jpg", "Completed smooth ceiling after repair and finishing"),
    ],
    "kitchens": [
        ("hilltop-kitchen-range.jpg", "Completed Hilltop kitchen cabinetry and range wall"),
        ("project-132.jpg", "Completed white kitchen with island seating"),
        ("kitchenette-after-wide.jpg", "Completed office kitchen with new cabinetry and counter"),
        ("project-114.jpg", "Completed kitchen renovation with bright cabinetry"),
        ("hilltop-kitchen-sink.jpg", "Completed Hilltop kitchen sink and backsplash detail"),
    ],
    "flooring": [
        ("project-043.jpg", "Dark wood flooring in a completed room"),
        ("project-042.jpg", "New plank flooring carried through a kitchen"),
        ("project-038.jpg", "Engineered wood flooring installation in progress"),
        ("project-072.jpg", "Completed plank flooring in a renovated room"),
        ("hardwood-installation-detail.jpg", "Hardwood flooring installation detail"),
    ],
    "basements": [
        ("project-067.jpg", "Finished basement living space with warm wood flooring"),
        ("project-072.jpg", "Completed plank flooring in a finished lower-level room"),
        ("hilltop-lower-level.jpg", "Completed Hilltop lower level with fireplace and warm flooring"),
        ("project-044.jpg", "Finished basement with new resilient plank flooring"),
    ],
    "handyman-repairs": [
        ("project-140.jpg", "Interior closet and storage work in progress"),
        ("project-027.jpg", "Interior doorway and trim work during renovation"),
        ("project-035.jpg", "Completed room repairs, flooring and finish work"),
        ("project-108.jpg", "Cabinet installation and interior finish work"),
    ],
    "decks-exterior": [
        ("fence-after-1.jpg", "Completed long-run wood privacy fence"),
        ("project-101.jpg", "Deck framing and exterior support structure"),
        ("post-hole-auger.jpg", "Powered auger digging a residential post hole"),
        ("project-104.jpg", "Completed long residential deck structure"),
        ("project-103.jpg", "Completed elevated wood deck at a residential property"),
    ],
    "water-damage": [
        ("salon-water-damage-2.jpg", "Damaged ceiling opened for restorative repair"),
        ("salon-drywall-rebuild.jpg", "Ceiling and wall surfaces being rebuilt with drywall and compound"),
        ("salon-after-1.jpg", "Working salon returned to a clean finish after water damage"),
        ("project-014.jpg", "Smooth completed ceiling after repair and finishing"),
    ],
    "commercial": [
        ("project-048.jpg", "Commercial fitness space after an LED lighting upgrade"),
        ("kitchenette-after-wide.jpg", "Completed staff kitchen in a London commercial property"),
        ("salon-after-1.jpg", "Completed London salon stations and lighting"),
        ("project-049.jpg", "Commercial lighting replacement in progress from scaffolding and ladders"),
        ("salon-after-2.jpg", "Finished London salon interior"),
    ],
    "structural-layout": [
        ("westmount-transformation-demolition.jpg", "Westmount demolition and layout changes in progress"),
        ("medway-closet-relocation-progress.jpg", "Former Medway closet opening closed for the new layout"),
        ("project-138.jpg", "Framed wall opening during an interior renovation"),
        ("medway-closet-before.jpg", "Medway room with the new closet opening visible"),
    ],
    "popcorn-ceiling-removal": [
        ("popcorn-ceiling-sander.jpg", "Drywall sander used during popcorn ceiling removal"),
        ("popcorn-ceiling-primer.jpg", "Primer being applied to a newly smoothed ceiling"),
        ("project-017.jpg", "Ceiling skim coating underway in a protected room"),
        ("project-016.jpg", "Textured ceiling before smooth-ceiling finishing"),
        ("project-015.jpg", "Ceiling surface correction and compound work"),
    ],
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
        "description": "Family-run renovation, repair and property improvement company based in Westmount and serving homeowners throughout London and nearby communities.",
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


def head(title: str, description: str, path: str, image: str, *, indexable: bool = True) -> str:
    canonical = f"{BASE_URL}{path}"
    robots = "index,follow,max-image-preview:large" if indexable else "noindex,follow"
    structured_data = f'<script type="application/ld+json">{schema(path, image)}</script>' if indexable else ""
    social_image_alt = PROJECT_DETAILS.get(path, {}).get("image_alt", "Completed work by Hekman Home Services Inc.")
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
      <meta property="og:image:alt" content="{html.escape(social_image_alt, quote=True)}">
      <meta name="twitter:card" content="summary_large_image">
      <meta name="twitter:title" content="{title}">
      <meta name="twitter:description" content="{html.escape(description, quote=True)}">
      <meta name="twitter:image" content="{BASE_URL}/{image}">
      <link rel="stylesheet" href="/styles.css">
      <link id="mobile-layout-fixes" rel="stylesheet" href="/mobile-fixes.css">
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
        <span>Based in Westmount · Serving London &amp; area</span>
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
          <p>Based in Westmount. Working throughout London and nearby communities.</p>
          <p><a href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
          <p class="social-links"><a href="{INSTAGRAM}" rel="me noopener" target="_blank">Instagram</a><a href="{FACEBOOK}" rel="me noopener" target="_blank">Facebook</a></p>
        </div>
        <div><h2>Explore</h2><ul><li><a href="/services/">Services</a></li><li><a href="/projects/">Our Work</a></li><li><a href="/about/">About</a></li><li><a href="/contact/">Contact</a></li></ul></div>
        <div><h2>Popular services</h2><ul><li><a href="/services/bathrooms/">Bathrooms</a></li><li><a href="/services/kitchens/">Kitchens</a></li><li><a href="/services/basements/">Basements</a></li><li><a href="/services/decks-exterior/">Decks &amp; Exterior</a></li><li><a href="/services/handyman-repairs/">Handyman &amp; Repairs</a></li><li><a href="/services/commercial/">Commercial Work</a></li></ul></div>
        <div><h2>Service area</h2><p>All of London—including Westmount, Sunningdale, Old North, Stoneybrook, Byron, Oakridge, Medway and nearby communities.</p></div>
      </div>
      <div class="wrap footer-fine"><span>© <span data-year></span> Hekman Home Services Inc. All rights reserved.</span><a href="/contact/">Start a project</a></div>
    </footer>
    <nav class="mobile-actions" aria-label="Quick contact">
      <a href="tel:{PHONE_LINK}"><span aria-hidden="true">☎</span> Call</a>
      <a href="/contact/#quote"><span aria-hidden="true">↗</span> Request a quote</a>
    </nav>
    <script src="/main.js" defer></script>
    """


def page(title: str, description: str, path: str, image: str, current: str, body: str, body_class: str = "", *, indexable: bool = True) -> str:
    body = polish_editorial_markup(body)
    return f"""<!doctype html>
    <html lang="en">
    {head(title, description, path, image, indexable=indexable)}
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
            "Westmount exterior proof",
            "A cleaner porch, a brighter entry and a more modern welcome",
            "Careful progress work, refreshed exterior lines and lighting changed how this repeat customer’s home feels from the street—during the day and after dark.",
            "westmount-porch-after-night.jpg",
            "Finished Westmount porch and entry illuminated at night",
            "/projects/westmount-porch-entry/",
            "See the porch revitalization",
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
      <span class="service-card-body"><small>London, Ontario</small><strong>{item['card_name']}</strong><span>{item['lead']}</span><b>Explore service <i aria-hidden="true">↗</i></b></span>
    </a>
    """


def homepage() -> str:
    featured = "".join(service_card(slug) for slug in SERVICE_DISPLAY_ORDER[:9])
    local_proof = f"""
      <section class="section section-stone local-proof-section">
        <div class="wrap">
          {section_heading("Recent work across London", "Real spaces, resolved with care", "A moved bathroom in the Melrose area, a resourceful kitchen renewal in Hyde Park and a small Blackfriars leak that revealed much more—three projects shaped by different homes and honest problem-solving.")}
          <div class="story-card-grid local-proof-grid">
            <a class="story-card story-card-large reveal" href="/projects/melrose-bathroom-layout/"><img src="/melrose-bathroom-after.jpg" alt="Completed Melrose-area bathroom with tiled shower, wall-hung toilet and illuminated mirror" loading="lazy"><span><small>Melrose area · completed</small><strong>A new layout for three connected spaces</strong><b>Moved bathroom, dedicated utility room and a finished exercise space <i aria-hidden="true">↗</i></b></span></a>
            <a class="story-card reveal" href="/projects/hyde-park-kitchen-renewal/"><img src="/hyde-park-kitchen-after.jpg" alt="Completed Hyde Park kitchen with refaced cabinetry, new counters, sink and backsplash" loading="lazy"><span><small>Hyde Park · completed</small><strong>Renewed without starting over</strong><b>Refaced cabinets, pantry, appliances, dishwasher, counters and backsplash <i aria-hidden="true">↗</i></b></span></a>
            <a class="story-card reveal" href="/projects/blackfriars-leak-restoration/"><img src="/blackfriars-restored-room.jpg" alt="Restored Blackfriars room with a smooth ceiling and painted walls" loading="lazy"><span><small>Blackfriars · restoration</small><strong>Restored after the real problem was understood</strong><b>Investigation, specialist coordination, rebuilding and finish restoration <i aria-hidden="true">↗</i></b></span></a>
          </div>
          <div class="testimonial-grid" aria-label="Anonymous homeowner testimonials">
            <blockquote class="testimonial-card reveal"><p>“This team is amazing—so meticulous and detail-oriented. Love their work.”</p><footer>Anonymous Medway homeowner</footer></blockquote>
            <blockquote class="testimonial-card reveal"><p>“Efficient, professional and fantastic work. Rene modernized the front of our home, and I would recommend him for home repair and remodelling.”</p><footer>Anonymous repeat Westmount customer</footer></blockquote>
          </div>
          <div class="section-actions reveal"><a class="button button-dark" href="/projects/">Explore More Real Projects</a></div>
        </div>
      </section>
    """
    body = f"""
    {hero("hilltop-kitchen-wide.jpg", "Completed Hilltop kitchen renovation by Hekman Home Services", "Renovations, repairs & restoration · London, Ontario", "Good work should feel like it belongs", "Based in Westmount and working across London, Hekman Home Services brings renovations, restorative repairs and the details between them into one thoughtful plan.", secondary=("/projects/", "View our work"), position="50% 54%")}
    <main id="main">
      <section class="trust-band" aria-label="Business assurances">
        <div class="wrap trust-grid">
          <div><span>01</span><strong>Fully insured &amp; bondable</strong><small>Professional protection for your project</small></div>
          <div><span>02</span><strong>20+ years of hands-on experience</strong><small>Renovation and repair knowledge in the field</small></div>
          <div><span>03</span><strong>Family-run &amp; local</strong><small>Led by Rene and Steph Hekman</small></div>
          <div><span>04</span><strong>Clear project scope</strong><small>Understand the work before it begins</small></div>
        </div>
      </section>
      {local_proof}
      <section class="section section-paper">
        <div class="wrap">
          {section_heading("What we do", "One team for the work that makes a house feel complete", "From full-room renovations to complex repair lists, we bring the connected parts of a project together with clear communication and careful finishing.")}
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
          <div class="reveal"><p class="eyebrow">Service area</p><h2>Based in Westmount. Working across London.</h2><p><strong>North, south, east and west—we work throughout the city and nearby communities.</strong> That includes Westmount, Sunningdale, Old North, Stoneybrook, Byron, Oakridge, Riverbend, Medway, Hyde Park, Old South and beyond.</p><div class="area-pills">{"".join(f'<span>{area}</span>' for area in AREAS)}</div></div>
          <div class="photo-stack reveal"><img src="/project-070.jpg" alt="Hekman Home Services team" loading="lazy"><div class="photo-note"><strong>Hands-on, local service</strong><span>Respect for your home and clear communication throughout the work.</span></div></div>
        </div>
      </section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">Picture what could work better?</p><h2>Start with the room—or repair—you keep thinking about.</h2><p>Send a few photos and tell us what is not working now. Rene and Steph will help turn that starting point into a practical next step.</p></div><div><a class="button button-primary" href="/contact/#quote">Tell Us About Your Project</a><a class="cta-phone" href="tel:{PHONE_LINK}">Call or text {PHONE_DISPLAY}</a></div></div></section>
    </main>
    """
    return page("Renovations & Repairs London ON | Hekman", "Based in Westmount, Hekman Home Services provides thoughtful renovations, flooring, drywall, handyman work and restorative repairs throughout London and nearby communities.", "/", "hilltop-kitchen-wide.jpg", "home", body, "home")


def services_page() -> str:
    cards = "".join(service_card(slug, compact=True, variant=1) for slug in SERVICE_DISPLAY_ORDER)
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
          <div class="case-study-media case-study-media-four">
            <figure><img src="/salon-after-1.jpg" alt="Long view through the restored London salon interior" loading="lazy"><figcaption>Working space restored</figcaption></figure>
            <figure><img src="/salon-after-2.jpg" alt="Completed salon with mirrors, stations and lighting" loading="lazy"><figcaption>Ready to welcome clients</figcaption></figure>
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
    scope = "".join(f'<article class="proof-card reveal"><span>0{i}</span><h3>{title}</h3><p>{text}</p></article>' for i, (title, text) in enumerate(item["scope"], 1))
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
      <section class="section section-paper"><div class="wrap service-intro"><div class="reveal"><p class="eyebrow">Thoughtful project planning</p><h2>Built around what the space needs.</h2><p>{item['intro']}</p><a class="text-link dark-link" href="/contact/#quote">Discuss your project <span aria-hidden="true">↗</span></a></div><ul class="scope-list reveal">{bullets}</ul></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("What the work can include", "A complete scope, not disconnected pieces.", "The exact work depends on existing conditions, selected materials and the result you want.")}<div class="proof-grid">{scope}</div></div></section>
      {showcase}
      {gallery_section}
      {spotlight}
      <section class="section section-paper"><div class="wrap faq-layout"><div class="reveal"><p class="eyebrow">Common questions</p><h2>Helpful before the walkthrough.</h2><p>The final scope depends on your property, materials and existing conditions.</p></div><div class="faq-list">{faqs}</div></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("Related services", "The connected work matters too.", "Many renovations involve more than one surface or room. These services are often part of the same conversation.")}<div class="service-grid related-grid">{related}</div></div></section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">Thinking about this project?</p><h2>Show us what you’re working with.</h2><p>You do not need a finished design or every decision made. A few photos and a clear description are enough to begin.</p></div><div><a class="button button-primary" href="/contact/#quote">Tell Us About Your Project</a><a class="cta-phone" href="tel:{PHONE_LINK}">Call or text {PHONE_DISPLAY}</a></div></div></section>
    </main>"""
    return page(item["title"], item["description"], service_url(slug), item["hero"], "services", body, "service-page")


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
    body = f"""
    {hero("hilltop-kitchen-wide.jpg", "Completed Hilltop kitchen and island", "Hekman project story · London, Ontario", "Hilltop: one home, one clear point of view.", "A whole-home transformation connecting the kitchen, bathroom, lower level, entry, stairs, flooring and finish details into a cohesive result.", small=True, position="50% 52%")}
    <main id="main">
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
      <section class="section section-paper"><div class="wrap">{section_heading("Why the phased approach works", "Each stage protects the bigger plan.", "Completing a home in phases can make the budget and disruption more manageable, as long as every decision supports the later work.")}<div class="proof-grid story-step-grid"><article class="proof-card reveal"><span>01</span><h3>Start with function</h3><p>Address layout, lighting, storage and the surfaces that influence the whole main floor.</p></article><article class="proof-card reveal"><span>02</span><h3>Protect finished work</h3><p>Prepare and cover completed areas while the next phase is underway.</p></article><article class="proof-card reveal"><span>03</span><h3>Connect each choice</h3><p>Coordinate flooring, paint, cabinetry, doors and trim with what is already complete.</p></article><article class="proof-card reveal"><span>04</span><h3>Finish without pretending</h3><p>Show completed phases proudly while staying clear about what still remains.</p></article></div></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("Related expertise", "One transformation, several connected scopes.", "Kitchen work, layout changes and finished surfaces all need to meet cleanly across the phases.")}<div class="service-grid related-grid">{service_card("kitchens", compact=True, variant=4)}{service_card("structural-layout", compact=True, variant=2)}{service_card("flooring", compact=True, variant=3)}</div></div></section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">Planning a renovation in phases?</p><h2>Start with the whole plan, even if you build it one stage at a time.</h2><p>Show us the rooms, priorities and timing. We will help identify how the pieces should connect.</p></div><div><a class="button button-primary" href="/contact/#quote">Request a Quote</a><a class="cta-phone" href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a></div></div></section>
    </main>"""
    return page("Phased Westmount Home Transformation | Hekman", PROJECT_DETAILS["/projects/westmount-1970s-transformation/"]["description"], "/projects/westmount-1970s-transformation/", "westmount-transformation-blue-wall-flooring.jpg", "projects", body, "project-story-page")


def salon_project_page() -> str:
    body = f"""
    {hero("salon-after-1.jpg", "Restored London salon after water-damage repairs", "Commercial restoration · London, Ontario", "A working salon, restored after water damage.", "When an unexpected leak interrupted the space, the goal was clear: complete the necessary restoration work and help the business feel ready for clients again.", small=True, position="50% 56%")}
    <main id="main">
      <section class="section section-paper"><div class="wrap service-intro story-summary"><div class="reveal"><p class="eyebrow">Commercial repair &amp; restoration</p><h2>Restoration is not about making a space unrecognizable. It is about making it feel whole again.</h2><p>This salon already had its own look, purpose and daily rhythm. After water damage, the work was about repairing the affected construction and returning the interior to the clean, bright setting the business and its clients expected.</p><p>That is an important difference. A planned renovation begins with what someone wants to change. Restoration begins with something that should never have happened—and a responsibility to put the space back together thoughtfully.</p></div><ul class="scope-list reveal"><li>Commercial water-damage restoration</li><li>Repair planning for an active business</li><li>Damaged wall and ceiling construction</li><li>Drywall and connected surface restoration</li><li>Primer, paint and finish work</li><li>A clean return to normal operations</li></ul></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("The completed space", "Bright, functional and ready for clients again.", "The restored interior feels like the salon clients already knew—clean, polished and ready to get back to business.")}<div class="story-mosaic story-mosaic-salon">
        <figure class="story-feature"><img src="/salon-after-1.jpg" alt="Long view through the restored London salon interior" loading="lazy"><figcaption>The working salon restored</figcaption></figure>
        <figure class="story-wide"><img src="/salon-after-2.jpg" alt="Completed salon with mirrors, stations and lighting" loading="lazy"><figcaption>Ready to welcome clients</figcaption></figure>
      </div></div></section>
      <section class="section section-stone"><div class="wrap editorial-grid reverse"><div class="editorial-media reveal"><img src="/salon-after-1.jpg" alt="Restored salon stations and finished commercial interior" loading="lazy"><span>Restoration with the business in mind</span></div><div class="editorial-copy reveal"><p class="eyebrow">When damage disrupts business</p><h2>The repair has to respect more than the building.</h2><p>Access, working hours, staff, clients and the need to reopen all shape a commercial restoration. Clear planning helps the construction work move forward without losing sight of what the business needs from the space.</p><a class="text-link dark-link" href="/services/water-damage/">Explore restoration and damage repairs <span aria-hidden="true">↗</span></a></div></div></section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">Damage interrupting your business?</p><h2>Show us what happened—and what needs to be working again.</h2><p>Send a few photos, the property location and any access or operating-hour details. We will help you understand the construction work that may come next.</p></div><div><a class="button button-primary" href="/contact/#quote">Start the Conversation</a><a class="cta-phone" href="tel:{PHONE_LINK}">Call or text {PHONE_DISPLAY}</a></div></div></section>
    </main>"""
    return page("Commercial Salon Water-Damage Restoration London ON | Hekman", "See a London salon returned to a bright working finish after water damage, with commercial restoration by Hekman Home Services.", "/projects/commercial-salon-repair/", "salon-after-1.jpg", "projects", body, "project-story-page")


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
      <section class="section section-stone"><div class="wrap">{section_heading("A closer look", "Walk through the completed cabinetry and counter.", "This short, compressed video waits until you press play, so it adds detail without slowing the first page load.")}<div class="video-grid video-grid-single"><figure class="work-video reveal"><video controls playsinline preload="none" poster="/kitchenette-after-detail.jpg" aria-label="Video walkthrough of completed kitchen cabinetry, sink and counter"><source src="/kitchenette-finish-tour.mp4" type="video/mp4">Your browser does not support embedded video.</video><figcaption><strong>Completed kitchen walkthrough</strong><span>Cabinet fronts, hardware, sink, counter and finished wall details.</span></figcaption></figure></div></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("Connected services", "Cabinets are only one part of a kitchen.", "Plumbing access, drywall, paint, trim and repair work all affect the finished result.")}<div class="service-grid related-grid">{service_card("commercial", compact=True, variant=2)}{service_card("kitchens", compact=True, variant=3)}{service_card("drywall-ceiling-repair", compact=True, variant=2)}</div></div></section>
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
      <section class="section section-charcoal"><div class="wrap">{section_heading("Related services", "A ceiling issue may connect to other work.", "Drywall repairs, water damage and broader room renovations can be coordinated in the same conversation.")}<div class="service-grid related-grid">{service_card("popcorn-ceiling-removal", compact=True, variant=2)}{service_card("drywall-ceiling-repair", compact=True, variant=3)}{service_card("water-damage", compact=True, variant=2)}</div></div></section>
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
      <section class="section section-paper"><div class="wrap">{section_heading("Related services", "Bathroom work often crosses several scopes.", "Flooring, drywall and fixture work can be reviewed as part of the same renovation.")}<div class="service-grid related-grid">{service_card("bathrooms", compact=True, variant=3)}{service_card("flooring", compact=True, variant=2)}{service_card("drywall-ceiling-repair", compact=True, variant=3)}</div></div></section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">Considering a tub-to-shower conversion?</p><h2>Show us the whole bathroom.</h2><p>Wide photos, the existing fixtures and what you want to change are enough to start the conversation.</p></div><div><a class="button button-primary" href="/contact/#quote">Request a Quote</a><a class="cta-phone" href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a></div></div></section>
    </main>"""
    return page("Tub-to-Shower Bathroom Transformation | Hekman", "See a real jetted-tub-to-shower bathroom renovation by Hekman Home Services, documented from demolition and open-wall work through the finished glass shower.", "/projects/glass-block-bathroom-conversion/", "bathroom-walnut-vanity-after.jpg", "projects", body, "project-story-page")


PROJECT_ARCHIVE = [
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

    # Bathrooms: Hilltop's two rooms, a verified tub-to-shower conversion,
    # a frosted-window repair sequence, and separate completed projects.
    ("hilltop-green-tile-before.jpg", "bathrooms", "Hilltop upstairs bathroom with its original green-tile tub surround", "Hilltop upstairs bathroom before", "Hilltop bathroom sequence"),
    ("hilltop-green-tile-after.jpg", "bathrooms", "Hilltop upstairs bathroom with a rebuilt marble-look tub surround", "Hilltop upstairs bathroom after", "Hilltop bathroom sequence"),
    ("hilltop-bathroom-vanity.jpg", "bathrooms", "Completed Hilltop upstairs bathroom vanity beneath the sloped ceiling", "Hilltop upstairs vanity", "Hilltop bathroom sequence"),
    ("hilltop-basement-bathroom-before.jpg", "bathrooms", "Hilltop basement bathroom before the shower, ceiling and finish renewal", "Hilltop basement bathroom before", "Hilltop bathroom sequence"),
    ("hilltop-basement-bathroom-during.jpg", "bathrooms drywall flooring", "Hilltop basement bathroom during shower tile, wall and floor work", "Hilltop basement bathroom during", "Hilltop bathroom sequence"),
    ("hilltop-basement-bathroom-wide.jpg", "bathrooms", "Completed Hilltop basement bathroom with white vanity and glass shower", "Hilltop basement bathroom after", "Hilltop bathroom sequence"),
    ("hilltop-basement-bathroom-vanity.jpg", "bathrooms", "Completed Hilltop basement bathroom white vanity and framed mirror", "Hilltop basement vanity", "Hilltop bathroom sequence"),
    ("hilltop-bathroom-shower.jpg", "bathrooms", "Completed Hilltop basement shower with white subway tile and gray accents", "Hilltop basement shower", "Hilltop bathroom sequence"),
    ("bathroom-glass-block-before.jpg", "bathrooms", "Bathroom with a jetted tub and glass-block window before conversion", "Before: jetted-tub layout", "Bathroom sequence"),
    ("bathroom-glass-block-demolition.jpg", "bathrooms", "Tiled jetted-tub platform partly removed during demolition", "Tub-platform demolition", "Bathroom sequence"),
    ("bathroom-glass-block-open-wall.jpg", "bathrooms insulation", "Tub removed with wall insulation and floor framing exposed", "Open wall and floor", "Bathroom sequence"),
    ("bathroom-walnut-vanity-after.jpg", "bathrooms flooring handyman", "Completed tub-to-shower conversion with a walnut vanity, gray tile and sliding glass door", "After: glass shower conversion", "Bathroom sequence"),
    ("project-155.jpg", "bathrooms flooring", "Frosted-window bathroom before wall and floor repair", "Frosted-window bathroom before", "Bathroom repair sequence"),
    ("project-146.jpg", "bathrooms drywall", "Wall tile removal in the same frosted-window bathroom", "Tile removal", "Bathroom repair sequence"),
    ("project-153.jpg", "bathrooms drywall insulation", "Bathroom exterior wall opened to insulation below the frosted window", "Wall and insulation access", "Bathroom repair sequence"),
    ("project-152.jpg", "bathrooms drywall", "New wall board and compound around the same frosted bathroom window", "Wall rebuilding", "Bathroom repair sequence"),
    ("project-144.jpg", "bathrooms", "Completed tiled bathroom shower", "Tiled shower", "Bathroom"),
    ("project-148.jpg", "bathrooms", "Completed bathroom with glass shower enclosure", "Glass shower renovation", "Bathroom"),
    ("project-161.jpg", "bathrooms", "Completed bathroom with warm wood vanity", "Warm vanity finish", "Bathroom"),
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
    ("westmount-transformation-demolition.jpg", "structural drywall", "Westmount main-floor demolition and layout changes in progress", "Westmount layout changes", "Ongoing transformation"),
    ("westmount-transformation-blue-wall-flooring.jpg", "flooring structural", "Completed Westmount living-space phase with plank flooring, pot lights and a deep-blue feature wall", "Westmount completed phase", "Flooring / lighting"),
    ("westmount-transformation-cabinet-install.jpg", "kitchens handyman", "Hekman Home Services crew installing kitchen cabinetry in the phased Westmount project", "Westmount cabinet installation", "Kitchen in progress"),
    ("westmount-transformation-kitchen-current.jpg", "kitchens", "Current Westmount kitchen progress before the planned backsplash and final styling", "Westmount kitchen progress", "Not the final after"),
    ("project-025.jpg", "structural", "Interior framing exposed during a layout renovation", "Layout opening", "Structural / layout"),
    ("project-031.jpg", "structural", "Doorway framing during an interior renovation", "New opening and framing", "Structural / layout"),
    ("project-138.jpg", "structural kitchens", "New wall framing beside a kitchen renovation", "Interior framing", "Structural / layout"),
    ("project-026.jpg", "structural", "Finished closet doors after an interior build", "Finished storage", "Layout / storage"),

    # Handyman, repair, painting and lighting work.
    ("project-027.jpg", "handyman structural", "Doorway and trim work during a residential repair", "Door and trim work", "Handyman repair"),
    ("project-032.jpg", "handyman drywall", "Drywall patching and compound on an interior wall", "Drywall patch", "Handyman repair"),
    ("project-140.jpg", "handyman", "Closet shelf and hanging system being installed", "Closet storage installation", "Handyman / storage"),
    ("project-139.jpg", "handyman bathrooms", "Bathroom toilet and flooring installation detail", "Bathroom fixture detail", "Handyman repair"),
    ("drywall-potlight-progress-poster.jpg", "handyman drywall structural", "Drywall finishing and pot lights during an interior renovation", "Drywall and pot lights", "Lighting / drywall"),

    # Restoration examples are separate projects unless a continuity note above
    # explicitly identifies a verified sequence.
    ("salon-water-damage-2.jpg", "restoration drywall", "Damaged ceiling opened to expose the affected construction", "Ceiling damage opened for repair", "Restoration"),
    ("salon-drywall-rebuild.jpg", "restoration drywall", "Ceiling and wall surfaces being rebuilt with drywall and compound", "Drywall restoration in progress", "Restoration"),
    ("salon-after-1.jpg", "commercial restoration", "Working London salon returned to a bright finish after water damage", "Salon restored after water damage", "Commercial restoration"),
    ("salon-after-2.jpg", "commercial restoration", "Completed salon interior with mirrors and workstations", "Restored working salon", "Commercial restoration"),

    # One verified fitness-facility lighting sequence: old fixtures, installation
    # from scaffolding and ladders, then the completed LED lighting.
    ("project-045.jpg", "commercial", "Older box-style fluorescent fixtures before a fitness-space lighting upgrade", "Before: older light fixtures", "Commercial lighting"),
    ("project-049.jpg", "commercial", "Crew replacing commercial lighting from scaffolding and ladders", "During: fixture replacement", "Commercial lighting"),
    ("project-048.jpg", "commercial", "Fitness facility illuminated by the completed LED lighting upgrade", "After: LED lighting", "Commercial lighting"),
]


# A deliberately edited selection for the public gallery. The broader archive
# above remains available for future stories without turning this page into a
# near-duplicate image dump.
PROJECTS = [
    ("melrose-bathroom-after.jpg", "bathrooms structural", "Completed Melrose-area bathroom with vanity, illuminated mirror and tiled shower", "Melrose bathroom", "Completed layout change"),
    ("melrose-wall-hung-toilet-progress.jpg", "bathrooms structural", "Wall-hung toilet installed during the Melrose-area bathroom renovation", "Melrose fixture progress", "Bathroom process"),
    ("melrose-shower-tile-progress.jpg", "bathrooms", "Dark wall tile being installed in the Melrose-area shower", "Melrose shower tile", "Bathroom process"),
    ("melrose-shower-toilet-detail.jpg", "bathrooms", "Completed Melrose-area tiled shower and wall-hung toilet", "Melrose finish detail", "Completed bathroom"),
    ("melrose-exercise-room-finishing.jpg", "drywall handyman", "Ceiling and paint finishing underway in the Melrose-area exercise room", "Melrose exercise room progress", "Drywall and paint"),
    ("melrose-exercise-room-after.jpg", "basements drywall", "Completed Melrose-area exercise room with smooth ceiling and painted walls", "Melrose exercise room", "Completed lower level"),
    ("hyde-park-kitchen-after.jpg", "kitchens", "Wide view of the completed Hyde Park kitchen", "Hyde Park kitchen", "Completed renewal"),
    ("hyde-park-pantry-and-appliance-layout.jpg", "kitchens handyman", "New pantry and reconfigured appliance wall in the Hyde Park kitchen", "Hyde Park pantry", "Storage and layout"),
    ("hyde-park-sink-and-dishwasher.jpg", "kitchens handyman", "New sink, counter and dishwasher in the Hyde Park kitchen", "Hyde Park sink wall", "Kitchen finish"),
    ("hyde-park-kitchen-preparation.jpg", "kitchens handyman", "Hyde Park kitchen protected during the update", "Hyde Park preparation", "Room protection"),
    ("hyde-park-backsplash-installation.jpg", "kitchens", "Backsplash tile being installed in the Hyde Park kitchen", "Hyde Park backsplash", "Tile installation"),
    ("blackfriars-first-opening.jpg", "restoration drywall", "Small initial ceiling opening during the Blackfriars leak investigation", "Blackfriars first opening", "Investigation"),
    ("blackfriars-investigation.jpg", "restoration drywall", "Protected investigation work after the Blackfriars ceiling was opened further", "Blackfriars investigation", "Restoration process"),
    ("blackfriars-structural-concern.jpg", "restoration structural", "Exposed framing documented during the Blackfriars investigation", "Blackfriars framing", "Condition documented"),
    ("blackfriars-rebuild.jpg", "restoration drywall insulation structural", "Blackfriars room during framing, insulation and rebuilding work", "Blackfriars rebuild", "Restoration process"),
    ("blackfriars-restored-room.jpg", "restoration drywall", "Restored Blackfriars room with smooth ceiling and painted walls", "Blackfriars restored room", "Completed restoration"),
    ("medway-finished-room.jpg", "flooring handyman", "Completed Medway room with cool gray-brown plank flooring and finished baseboards", "Medway finished room", "Completed flooring"),
    ("medway-finished-floor-detail.jpg", "flooring", "Close view of the completed Medway plank flooring and clean edge detail", "Medway floor detail", "Completed flooring"),
    ("hilltop-kitchen-wide.jpg", "kitchens", "Wide view of the completed Hilltop kitchen and island", "Hilltop kitchen", "Completed kitchen"),
    ("hilltop-kitchen-range.jpg", "kitchens", "Hilltop kitchen range wall and white cabinetry", "Hilltop range wall", "Kitchen detail"),
    ("hilltop-lower-level.jpg", "basements flooring", "Completed Hilltop lower-level living area with fireplace", "Hilltop lower level", "Completed basement"),
    ("hilltop-staircase.jpg", "basements flooring", "Finished Hilltop staircase with dark railing", "Hilltop staircase", "Flooring and stairs"),
    ("hilltop-green-tile-before.jpg", "bathrooms", "Hilltop upstairs bathroom with its original green-tile tub surround", "Hilltop bathroom before", "Verified sequence"),
    ("hilltop-green-tile-after.jpg", "bathrooms", "Hilltop upstairs bathroom with a rebuilt marble-look tub surround", "Hilltop bathroom after", "Verified sequence"),
    ("hilltop-basement-bathroom-before.jpg", "bathrooms basements", "Hilltop basement bathroom before the shower, ceiling and finish renewal", "Hilltop basement bath before", "Verified sequence"),
    ("hilltop-basement-bathroom-wide.jpg", "bathrooms basements", "Completed Hilltop basement bathroom with white vanity and glass shower", "Hilltop basement bath after", "Verified sequence"),
    ("bathroom-glass-block-before.jpg", "bathrooms", "Bathroom with a jetted tub and glass-block window before conversion", "Jetted-tub layout", "Bathroom before"),
    ("bathroom-glass-block-demolition.jpg", "bathrooms", "Tiled jetted-tub platform partly removed during demolition", "Tub-platform demolition", "Bathroom process"),
    ("bathroom-glass-block-open-wall.jpg", "bathrooms insulation", "Tub removed with wall insulation and floor framing exposed", "Bathroom wall opened", "Bathroom process"),
    ("bathroom-walnut-vanity-after.jpg", "bathrooms flooring", "Completed tub-to-shower conversion with a walnut vanity, gray tile and sliding glass door", "Glass-shower conversion", "Completed bathroom"),
    ("kitchenette-before-wide.jpg", "kitchens commercial", "Office kitchen before cabinetry and repair work", "Office kitchen before", "Verified sequence"),
    ("kitchenette-wall-plumbing-stage.jpg", "kitchens commercial drywall", "Office kitchen wall opened for plumbing and repair access", "Office kitchen wall access", "Verified sequence"),
    ("kitchenette-cabinet-installation.jpg", "kitchens commercial handyman", "New office kitchen cabinet boxes and fronts during installation", "Office cabinet installation", "Verified sequence"),
    ("kitchenette-after-wide.jpg", "kitchens commercial", "Completed office kitchen with walnut-look cabinets and gray counter", "Office kitchen after", "Completed kitchen"),
    ("westmount-transformation-demolition.jpg", "structural drywall", "Westmount main-floor demolition and layout changes in progress", "Westmount layout work", "Ongoing transformation"),
    ("westmount-transformation-blue-wall-flooring.jpg", "flooring structural", "Completed Westmount living-space phase with plank flooring, pot lights and a deep-blue feature wall", "Westmount completed phase", "Flooring and lighting"),
    ("westmount-transformation-cabinet-install.jpg", "kitchens handyman", "Hekman Home Services crew installing kitchen cabinetry in the phased Westmount project", "Westmount cabinetry", "Kitchen in progress"),
    ("westmount-transformation-kitchen-current.jpg", "kitchens", "Current Westmount kitchen progress before the planned backsplash and final styling", "Westmount kitchen progress", "Not the final after"),
    ("westmount-porch-work-in-progress.jpg", "exterior handyman", "Exterior work in progress at an anonymous Westmount porch and entry", "Westmount porch progress", "Exterior process"),
    ("westmount-porch-after-night.jpg", "exterior handyman", "Finished Westmount porch and entry illuminated at night", "Westmount porch after", "Completed exterior"),
    ("project-016.jpg", "drywall", "Original textured ceiling and patch before smooth-ceiling work", "Popcorn ceiling before", "Ceiling sequence"),
    ("project-017.jpg", "drywall", "Skim coating underway with the room protected", "Ceiling skim coat", "Ceiling sequence"),
    ("popcorn-ceiling-primer.jpg", "drywall", "Primer being rolled onto a smoothed ceiling", "Smooth ceiling primer", "Ceiling sequence"),
    ("project-103.jpg", "exterior", "Completed elevated wood deck behind a brick home", "Elevated deck", "Completed exterior"),
    ("project-101.jpg", "exterior structural", "Deck framing and support-post structure", "Deck structure", "Exterior process"),
    ("fence-after-1.jpg", "exterior", "Completed long-run wood privacy fence", "Privacy fence", "Completed exterior"),
    ("post-hole-digging.jpg", "exterior", "Post hole being dug by hand beside a residential property", "Post-hole preparation", "Exterior process"),
    ("post-hole-auger.jpg", "exterior", "Powered auger digging a post hole", "Powered auger work", "Exterior process"),
    ("project-045.jpg", "commercial", "Older box-style fluorescent fixtures before a fitness-space lighting upgrade", "Fitness lighting before", "Commercial sequence"),
    ("project-049.jpg", "commercial", "Crew replacing commercial lighting from scaffolding and ladders", "Fitness lighting installation", "Commercial sequence"),
    ("project-048.jpg", "commercial", "Fitness facility illuminated by the completed LED lighting upgrade", "Fitness lighting after", "Commercial sequence"),
    ("salon-water-damage-2.jpg", "restoration commercial drywall", "Damaged salon ceiling opened to expose the affected construction", "Salon ceiling opened", "Commercial restoration"),
    ("salon-drywall-rebuild.jpg", "restoration commercial drywall", "Salon ceiling and wall surfaces being rebuilt with drywall and compound", "Salon rebuild", "Commercial restoration"),
    ("salon-after-1.jpg", "restoration commercial", "Working London salon returned to a bright finish after water damage", "Salon restored", "Completed restoration"),
]


def projects_page() -> str:
    cards = "".join(f'<figure class="project-card reveal" data-category="{categories}"><button class="project-image" type="button" data-lightbox aria-label="Enlarge {html.escape(label, quote=True)}"><img src="/{src}" alt="{html.escape(alt, quote=True)}" loading="lazy" decoding="async"></button><figcaption><span>{label}</span><small>{tag}</small></figcaption></figure>' for src, categories, alt, label, tag in PROJECTS)
    filters = [("all", "All work"), ("restoration", "Restoration & damage"), ("kitchens", "Kitchens"), ("bathrooms", "Bathrooms"), ("basements", "Basements"), ("flooring", "Flooring"), ("drywall", "Drywall & ceilings"), ("insulation", "Insulation"), ("exterior", "Decks & fences"), ("structural", "Structural"), ("handyman", "Handyman & repairs"), ("commercial", "Commercial")]
    buttons = "".join(f'<button type="button" class="filter-button{" active" if key == "all" else ""}" data-filter="{key}" aria-pressed="{"true" if key == "all" else "false"}">{label}</button>' for key, label in filters)
    body = f"""
    {hero("hilltop-kitchen-wide.jpg", "Completed Hilltop kitchen renovation", "Our work · London, Ontario", "Work that holds up to a closer look", "Explore carefully documented renovations, repairs and restorations from neighbourhoods across London—finished spaces, honest progress and the decisions that connect them.", small=True, position="50% 54%")}
    <main id="main">
      <section class="section section-paper"><div class="wrap">{section_heading("Project stories", "Real homes, real stages and clear project facts", "These selected London stories lead with the problem each room needed to solve. In-progress work is labelled clearly, specialist coordination is described accurately and homeowners remain anonymous.")}
        <div class="story-card-grid">
          <a class="story-card story-card-large reveal" href="/projects/melrose-bathroom-layout/"><img src="/melrose-bathroom-after.jpg" alt="Completed Melrose-area bathroom with tiled shower, wall-hung toilet and illuminated mirror" loading="lazy"><span><small>Melrose area · completed</small><strong>A bathroom reworked from the layout out</strong><b>Bathroom relocation, new utility room and a finished exercise space <i aria-hidden="true">↗</i></b></span></a>
          <a class="story-card reveal" href="/projects/hyde-park-kitchen-renewal/"><img src="/hyde-park-kitchen-after.jpg" alt="Completed Hyde Park kitchen with refaced cabinetry, new counters, sink and backsplash" loading="lazy"><span><small>Hyde Park · completed</small><strong>Renewed without starting over</strong><b>Cabinet refacing, pantry, appliance flow, dishwasher and new surfaces <i aria-hidden="true">↗</i></b></span></a>
          <a class="story-card reveal" href="/projects/blackfriars-leak-restoration/"><img src="/blackfriars-restored-room.jpg" alt="Restored Blackfriars room with a smooth ceiling and painted walls" loading="lazy"><span><small>Blackfriars · restoration</small><strong>A small leak that needed a bigger plan</strong><b>Investigation, specialist coordination, rebuilding and finish restoration <i aria-hidden="true">↗</i></b></span></a>
          <a class="story-card reveal" href="/projects/medway-flooring-storage/"><img src="/medway-finished-room.jpg" alt="Completed Medway room with cool gray-brown plank flooring and finished baseboards" loading="lazy"><span><small>Medway · completed</small><strong>More storage and better flow</strong><b>Three rooms, relocated closets, flooring, doors and trim <i aria-hidden="true">↗</i></b></span></a>
          <a class="story-card reveal" href="/projects/hilltop-home-transformation/"><img src="/hilltop-kitchen-angle.jpg" alt="Completed Hilltop kitchen" loading="lazy"><span><small>Whole-home transformation</small><strong>Hilltop</strong><b>Kitchen, bathrooms, lower level, stairs and finish work <i aria-hidden="true">↗</i></b></span></a>
          <a class="story-card reveal" href="/projects/westmount-1970s-transformation/"><img src="/westmount-transformation-blue-wall-flooring.jpg" alt="Completed Westmount living-space phase with plank flooring, pot lights and a deep-blue feature wall" loading="lazy"><span><small><em class="status-chip">Project in progress</em> · Westmount</small><strong>A transformation built in phases</strong><b>Kitchen, one powder room, layout, flooring, lighting and storage <i aria-hidden="true">↗</i></b></span></a>
          <a class="story-card reveal" href="/projects/glass-block-bathroom-conversion/"><img src="/bathroom-walnut-vanity-after.jpg" alt="Completed tub-to-shower bathroom conversion" loading="lazy"><span><small>Before · during · after</small><strong>Jetted tub to glass shower</strong><b>Demolition, open-wall work, tile and enclosure <i aria-hidden="true">↗</i></b></span></a>
          <a class="story-card story-card-wide reveal" href="/projects/commercial-salon-repair/"><img src="/salon-after-1.jpg" alt="Restored London salon interior" loading="lazy"><span><small>Commercial restoration</small><strong>A working salon restored after water damage</strong><b>Construction repairs planned around the needs of the business <i aria-hidden="true">↗</i></b></span></a>
        </div>
      </div></section>
      <section class="section section-stone"><div class="wrap">{section_heading("Work in motion", "Short, useful views of the work", "These two quiet clips add context without taking over the page. They never autoplay and wait to load until you choose to watch.")}<div class="video-grid"><figure class="work-video reveal"><video controls playsinline preload="none" poster="/melrose-bathroom-after.jpg" aria-label="Short walkthrough of the completed Melrose-area bathroom"><source src="/melrose-bathroom-tour.mp4" type="video/mp4">Your browser does not support embedded video.</video><figcaption><strong>Melrose bathroom walkthrough</strong><span>A six-second look at the finished vanity, shower and wall-hung toilet</span></figcaption></figure><figure class="work-video reveal"><video controls playsinline preload="none" poster="/bathroom-walnut-vanity-after.jpg" aria-label="Video of a jetted-tub bathroom being converted into a glass shower"><source src="/bathroom-glass-block-transformation.mp4" type="video/mp4">Your browser does not support embedded video.</video><figcaption><strong>Tub-to-shower transformation</strong><span>Demolition, open-wall work and the completed glass shower</span></figcaption></figure></div></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("Explore the work", "Find the kind of project that feels familiar.", "Planning a room renovation, repairing damage, updating a commercial space or finally tackling a long repair list? Choose a category to see related work.")}<div class="filter-bar" aria-label="Filter project photographs">{buttons}</div><div class="projects-grid" id="projects-grid" aria-live="polite">{cards}</div><p class="filter-status" data-filter-status>Showing all {len(PROJECTS)} photographs.</p></div></section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">Picture your own project?</p><h2>Show us what’s not working. Tell us what better looks like.</h2><p>Whether you are imagining a complete transformation, dealing with damage or finally tackling the repairs that have piled up, you do not need every answer before reaching out. A few photos and an honest conversation are enough to begin.</p></div><div><a class="button button-primary" href="/contact/#quote">Tell Us About Your Project</a><a class="cta-phone" href="tel:{PHONE_LINK}">Call or text {PHONE_DISPLAY}</a></div></div></section>
      <dialog class="lightbox" data-lightbox-dialog><button type="button" class="lightbox-close" data-lightbox-close aria-label="Close image">×</button><img src="" alt=""><p></p></dialog>
    </main>"""
    return page("Renovation Projects London ON | Hekman", "Explore genuine, carefully curated renovation, flooring, storage, porch, restoration and commercial project stories by Hekman Home Services in London, Ontario.", "/projects/", "hilltop-kitchen-wide.jpg", "projects", body, "projects-page")


def about_page() -> str:
    body = f"""
    {hero("project-070.jpg", "Hekman Home Services team gathered around project plans", "About Hekman Home Services", "A husband-and-wife team, close to every project.", "Rene and Steph Hekman bring hands-on construction, thoughtful design and direct communication together for homes and properties across London, Ontario.", small=True, position="50% 42%")}
    <main id="main">
      <section class="section section-paper"><div class="wrap editorial-grid about-story"><div class="editorial-copy reveal"><p class="eyebrow">The Hekman approach</p><h2>The people you speak with are part of the work.</h2><p>Hekman Home Services is owned and operated by Rene and Steph Hekman. Together they combine more than 20 years of hands-on renovation and repair experience with the planning, sales and design perspective that helps a project feel considered from the first walkthrough to the final details.</p><p>That closeness matters. Existing conditions are discussed, choices are connected to the whole property and the client is never handed off to an anonymous process. The work stays grounded in a simple idea: fix it properly, communicate clearly and leave the space feeling complete.</p><p class="signature-line">Fix it. Sell it. Celebrate it.</p></div><div class="editorial-media reveal"><img src="/project-079.jpg" alt="Hekman Home Services team reviewing plans" loading="lazy"><span>Planning the work together</span></div></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("What guides the work", "Professional does not have to feel impersonal.", "The strongest projects come from good preparation, honest conversations and care for the property throughout the work.")}<div class="values-grid"><article class="reveal"><span>01</span><h3>Listen first</h3><p>Understand the problem, priorities and intended result before defining the work.</p></article><article class="reveal"><span>02</span><h3>Protect the property</h3><p>Preparation, dust control and cleanup are treated as part of the project.</p></article><article class="reveal"><span>03</span><h3>Communicate clearly</h3><p>When existing conditions affect the plan, explain what changed and why.</p></article><article class="reveal"><span>04</span><h3>Finish thoughtfully</h3><p>Trim, transitions and final details matter because they are what make the work feel complete.</p></article></div></div></section>
      <section class="section section-stone"><div class="wrap people-grid"><article class="person-card reveal"><img src="/project-075.jpg" alt="Rene Hekman, Director and Contractor at Hekman Home Services" loading="lazy"><div><p class="eyebrow">Director · Contractor</p><h2>Rene Hekman</h2><p>Rene leads construction in the field—from opening walls and solving repair conditions to the practical preparation and finish work that make a renovation hold together. His role stays hands-on throughout the project.</p></div></article><article class="person-card reveal"><img src="/project-076.jpg" alt="Steph Hekman, Customer Relations, Sales and Design at Hekman Home Services" loading="lazy"><div><p class="eyebrow">Customer Relations · Sales &amp; Design</p><h2>Steph Hekman</h2><p>Steph guides client communication, project planning and design decisions. Her eye for how rooms connect shaped transformations such as the 1970s Westmount project, where layout, flooring, trim, doors and finishes had to read as one home.</p></div></article></div></section>
      <section class="section section-paper"><div class="wrap area-layout"><div class="reveal"><p class="eyebrow">Local service</p><h2>Based in Westmount. Working across London.</h2><p><strong>North, south, east and west—we work throughout the city and nearby communities.</strong> Hekman Home Services serves Westmount, Sunningdale, Old North, Stoneybrook, Byron, Oakridge, Riverbend, Medway, Hyde Park, Old South and beyond.</p><a class="button button-dark" href="/contact/">Contact Rene &amp; Steph</a></div><div class="assurance-panel reveal"><strong>Fully insured &amp; bondable</strong><span>Professional protection for residential and commercial projects.</span><strong>20+ years of hands-on experience</strong><span>Practical renovation and repair knowledge brought directly to the work.</span><strong>Real project proof</strong><span>Explore completed spaces and the work behind them.</span></div></div></section>
      <section class="cta-section"><div class="wrap cta-panel reveal"><div><p class="eyebrow">Let’s discuss your property.</p><h2>Start with the space and the goal.</h2><p>We will help make sense of the connected work from there.</p></div><div><a class="button button-primary" href="/contact/#quote">Request a Quote</a><a class="cta-phone" href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a></div></div></section>
    </main>"""
    return page("About Rene & Steph Hekman | Hekman Home Services", "Meet Rene and Steph Hekman, the husband-and-wife team behind Hekman Home Services, providing hands-on renovations and repairs in London, Ontario.", "/about/", "project-070.jpg", "about", body, "about-page")


def contact_page() -> str:
    options = "".join(
        f'<option value="{SERVICES[slug]["name"]}">{SERVICES[slug]["name"]}</option>'
        for slug in SERVICE_DISPLAY_ORDER
    )
    body = f"""
    {hero("project-129.jpg", "Completed kitchen renovation", "Contact Hekman Home Services", "Tell us what you want to change.", "A short description, the project location and a few photos are enough to begin the conversation.", small=True, position="50% 58%")}
    <main id="main">
      <section class="section section-paper" id="quote"><div class="wrap contact-layout"><div class="contact-intro reveal"><p class="eyebrow">Request a quote</p><h2>Start with what you know.</h2><p>You do not need every finish or measurement decided. Tell us what is not working, what you would like the space to become and where the property is located.</p><div class="contact-direct"><h3>Prefer direct contact?</h3><a href="tel:{PHONE_LINK}"><small>Call or text</small><strong>{PHONE_DISPLAY}</strong></a><a href="mailto:{EMAIL}"><small>Email</small><strong>{EMAIL}</strong></a><div><small>Service area</small><strong>London &amp; nearby communities</strong></div></div></div>
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
    write("projects/melrose-bathroom-layout/index.html", melrose_project_page())
    write("projects/hyde-park-kitchen-renewal/index.html", hyde_park_kitchen_project_page())
    write("projects/blackfriars-leak-restoration/index.html", blackfriars_project_page())
    write("projects/hilltop-home-transformation/index.html", hilltop_project_page())
    write("projects/medway-flooring-storage/index.html", medway_project_page())
    write("projects/westmount-porch-entry/index.html", westmount_porch_project_page())
    write("projects/westmount-1970s-transformation/index.html", westmount_project_page())
    write("projects/commercial-salon-repair/index.html", salon_project_page())
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
        "/projects/melrose-bathroom-layout/",
        "/projects/hyde-park-kitchen-renewal/",
        "/projects/blackfriars-leak-restoration/",
        "/projects/hilltop-home-transformation/",
        "/projects/medway-flooring-storage/",
        "/projects/westmount-porch-entry/",
        "/projects/westmount-1970s-transformation/",
        "/projects/commercial-salon-repair/",
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

    > Husband-and-wife-led renovation, repair and property improvement company based in Westmount and serving homeowners throughout London and nearby communities.

    Canonical website: {BASE_URL}/
    Phone: {PHONE_DISPLAY}
    Email: {EMAIL}

    ## Core services
    {chr(10).join(f'- {item["name"]}: {BASE_URL}{service_url(slug)}' for slug, item in SERVICES.items())}

    ## Service area
    Based in Westmount. Working throughout London and nearby communities—north, south, east and west. This includes Westmount, Sunningdale, Old North, Stoneybrook, Byron, Oakridge, Riverbend, Medway, Hyde Park, Old South and other London neighbourhoods.

    ## Selected project stories
    - Melrose-area bathroom and lower-level layout: {BASE_URL}/projects/melrose-bathroom-layout/
      The bathroom moved to the other side of an existing wall and was completed with a tiled shower, wall-hung toilet, vanity, lighting and finish work. The connected plan also created a utility room and finished an exercise room with drywall, ceiling work and paint. The public location is limited to the Melrose area, London, Ontario.
    - Hyde Park kitchen renewal: {BASE_URL}/projects/hyde-park-kitchen-renewal/
      Existing cabinets were refaced, a pantry was built, appliances were reconfigured, a dishwasher was added and the counters, sink and backsplash were renewed. This project was completed for under $20,000; that result is not a fixed package or guarantee for another kitchen.
    - Blackfriars leak investigation and restoration: {BASE_URL}/projects/blackfriars-leak-restoration/
      A small leak opening revealed mold, evidence of mice, structural concerns and knob-and-tube wiring. Hekman Home Services identified the visible conditions, coordinated the appropriate remediation team and qualified trades, then managed the rebuild and finish restoration.
    - Medway flooring and storage transformation: {BASE_URL}/projects/medway-flooring-storage/
      Carpet was removed in three rooms. New plank flooring, relocated and new closets, doors, casing and baseboards improved storage and flow. Surfaces were left seamlessly primed for the homeowner's final paint.
    - Westmount porch and entry revitalization: {BASE_URL}/projects/westmount-porch-entry/
      A completed exterior project for an anonymous repeat Westmount customer and neighbour, including porch and entry work, refreshed exterior lines and lighting.
    - Phased Westmount home transformation, ongoing: {BASE_URL}/projects/westmount-1970s-transformation/
      An ongoing project completed around the clients' timing and budget. The confirmed scope includes layout changes, kitchen work, one powder-room renovation, flooring, pot lights, storage, doors, trim and finishing. The kitchen is not complete; a white 2-inch by 10-inch herringbone backsplash to the ceiling is planned.
    - Hilltop whole-home transformation: {BASE_URL}/projects/hilltop-home-transformation/
    - Commercial salon water-damage repair: {BASE_URL}/projects/commercial-salon-repair/
    - Office kitchen renewal, before through completion: {BASE_URL}/projects/kitchen-renewal/
    - Popcorn ceiling transformation: {BASE_URL}/projects/popcorn-ceiling-transformation/
    - Jetted-tub to glass-shower bathroom conversion: {BASE_URL}/projects/glass-block-bathroom-conversion/

    ## Business identity
    Hekman Home Services Inc. is led by Rene and Steph Hekman. The company provides residential renovation and repair work plus commercial maintenance and repairs. It is fully insured and bondable and brings more than 20 years of hands-on experience to its work.

    Official social profiles:
    - Instagram: {INSTAGRAM}
    - Facebook: {FACEBOOK}
    """)


if __name__ == "__main__":
    build()
