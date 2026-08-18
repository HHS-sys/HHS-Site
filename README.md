# Hekman Home Services Inc. website

Static HTML, CSS and vanilla JavaScript website for Hekman Home Services Inc., deployed through Vercel.

## Structure

- Primary pages use directory-based clean routes such as `/services/`, `/projects/` and `/contact/`.
- Service pages live below `/services/<service>/`.
- Shared presentation assets remain at `/styles.css` and `/main.js`.
- The curated project photography remains unchanged at repository root as `project-###.jpg`.
- Legacy flat HTML routes are retained as lightweight redirects, with matching Vercel redirects.

## Build

Page content and shared site structure are maintained in `scripts/build_site.py`.

```bash
python3 scripts/build_site.py
```

The build only writes site text files. It does not delete, rename or edit project photography.

## Local preview

```bash
python3 -m http.server 4173
```

Then visit `http://127.0.0.1:4173/`.

## Direct quote delivery

The contact form posts to the Vercel Function at `/api/quote`. Configure the
server-only variables listed in `.env.example` in Vercel. `RESEND_API_KEY` must
never be exposed to the browser or committed to git, and the domain in
`QUOTE_FROM_EMAIL` must be verified with the email provider before launch.

Before promoting the form to production:

1. Configure the variables for both Preview and Production.
2. Verify `hekmanhomeservices.ca` as a Resend sending domain.
3. Add a Vercel Firewall rate limit for `POST /api/quote/` (recommended: five
   requests per IP in ten minutes).
4. Enable Vercel Web Analytics for the project.
5. Send a labelled preview enquiry, confirm it arrives at the fixed business
   inbox, and confirm Reply addresses the customer email.

Run the API checks with:

```bash
node scripts/test_quote_api.js
```
