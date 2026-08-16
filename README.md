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
