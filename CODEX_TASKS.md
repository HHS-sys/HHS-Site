# Codex Brief — Take HekmanHomeServices.ca From 8/10 to 10/10+

## Goal
Upgrade the existing static website without discarding its strongest design work. The result should feel premium, genuine, local and highly trustworthy for homeowners age 30–80 in London, Ontario, especially West London.

Read `AGENTS.md` before changing anything.

## Phase 1 — Audit before editing
1. Inspect the current production site and repository.
2. Run the existing build and validation scripts.
3. Audit mobile at 390×844 and 430×932, tablet and desktop.
4. Confirm the header/menu, sticky mobile actions, quote form, gallery filters, lightbox, videos, internal links and redirects work.
5. Identify any inaccurate or overly broad project claims, especially on the Westmount story.
6. Preserve the existing navy/cyan/red visual identity, premium typography and strong photography-led sections.

## Phase 2 — Add three accurate local stories

### A. Medway flooring and storage transformation
Create a new project story page and add it to the Projects page, relevant service pages, sitemap and internal links.

Suggested public title:
`Medway: More Storage, Better Flow and a Seamless Upper Level`

Do not use the street name as the public project title.

Required story points:
- Carpet removal in three rooms.
- New plank flooring carried through the upper level to coordinate with the previously completed main floor.
- Existing closet opening closed and relocated to make a larger closet on the other side of the wall.
- New double closet in the primary bedroom.
- New doors, casing and baseboards.
- Primed, seamless surfaces left ready for the homeowner's final paint.
- Budget-conscious collaboration: homeowner supplied flooring; Hekman provided trim and doors at cost.
- The project improved storage, daily function and resale appeal.
- Anonymous testimonial: `This team is amazing—so meticulous and detail-oriented. Love their work.`
- Note that the homeowner wants Hekman back.

Photo treatment:
- Use the strongest real before images showing carpet and the closet changes.
- Use one real installation image and the real door/floor/transition detail.
- If visual reconstructions are included because finished rooms were occupied, label each one clearly as a visual reconstruction based on the completed layout and materials.
- The reconstructed flooring must match the cool gray-brown installed plank shown in the real transition photo.

### B. Westmount porch and entry revitalization
Create a separate project story page and add it to the Projects page, Handyman/Exterior pages, sitemap and internal links.

Suggested public title:
`A Westmount Porch and Entry, Modernized by Neighbours`

Required story points:
- Repeat Westmount customer and local neighbour.
- Exterior/porch revitalization plus other handyman work completed over time.
- Show one clear before, one careful work-in-progress image and the strongest finished night photograph.
- Emphasize repair, cleanup of the exterior lines, lighting and a more modern welcome.
- Anonymous testimonial: efficient, professional and fantastic work; the client said Hekman modernized the front of the home and would recommend Rene for home repair and remodelling.
- Do not use the customer's name or address.

### C. Phased Westmount home transformation
Revise the existing Westmount project page so it is accurate, richer and clearly ongoing.

Suggested public title:
`Westmount: A Home Transformation Built in Thoughtful Phases`

Required story points:
- The project is ongoing and completed in phases around the clients' life, timing and budget.
- Show the strongest demolition, protection/preparation, drywall/paint, lighting, flooring, cabinet installation and completed-phase images.
- Explain that each phase is designed to connect with what came before and what is still planned.
- Include kitchen work, one powder-room renovation, flooring, lighting, layout, storage, trim and finishing without claiming incomplete work is finished.
- Do not describe the project as having multiple bathroom renovations. The confirmed bathroom scope is one powder room.
- The planned kitchen backsplash is white 2-inch by 10-inch subway tile in a ceiling-height herringbone pattern.
- Any kitchen rendering must be labelled `Design visualization — planned backsplash and final styling`.
- Add a visible `Project in progress` status treatment.

## Phase 3 — Strengthen the homepage
- Add a concise West London proof section featuring the three stories above.
- Add two short anonymized testimonials tied to their actual projects.
- Make the local positioning more specific: `Based in Westmount. Working throughout West London and nearby communities.`
- Keep the homepage curated. Do not add a huge photo dump.
- Use real people/team photography on the About or trust section.
- Make the primary value proposition clearer for both full renovations and smaller repair lists.

## Phase 4 — Improve readability and conversion for ages 30–80
- Review font sizes, line lengths, contrast and spacing.
- Keep body copy plain, warm and easy to scan.
- Keep buttons large and language direct.
- Ensure phone number, quote button and service-area confidence are easy to find.
- Avoid tiny all-caps text where it carries essential information.
- Confirm mobile menu never overlaps or exposes desktop links.

## Phase 5 — Curate media and clips
- Do not upload every supplied image.
- Select only the strongest visual evidence for each story.
- Create short clips from the supplied videos only where they add proof that still photos cannot.
- Preferred clip lengths: 6–15 seconds, or one 20–30 second sequence.
- No autoplay. Use `preload="none"` and an intentional poster image.
- Compress images responsibly and preserve originals in the repository.

## Phase 6 — Search, AI discovery and technical polish
- Add unique metadata, breadcrumbs, descriptive alt text and project-specific internal links.
- Update sitemap and llms content.
- Keep structured data factual and consistent.
- Add West London neighbourhood language naturally, not as a list repeated on every page.
- Confirm canonical URLs, 404, redirects, asset caching and security headers.
- Close or supersede stale implementation paths; do not merge the old Vercel Analytics PR without reviewing whether it matches the rebuilt site.

## Deliverable
Open a draft pull request to `main` containing:
- The three project-story improvements.
- Homepage/local-trust improvements.
- Mobile/readability fixes.
- Curated media additions.
- Updated sitemap/internal links.
- Validation results and screenshots at mobile and desktop sizes.

Do not merge automatically. The live site is in production and must be reviewed first.
