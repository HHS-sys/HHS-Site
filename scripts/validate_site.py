#!/usr/bin/env python3
"""Validate local routes, assets, metadata and basic HTML accessibility."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://www.hekmanhomeservices.ca"
PRIMARY = [
    ROOT / "index.html",
    ROOT / "services/index.html",
    *sorted((ROOT / "services").glob("*/index.html")),
    ROOT / "projects/index.html",
    *sorted((ROOT / "projects").glob("*/index.html")),
    ROOT / "about/index.html",
    ROOT / "contact/index.html",
    ROOT / "404.html",
]


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []
        self.title = ""
        self.in_title = False
        self.descriptions: list[str] = []
        self.canonicals: list[str] = []
        self.robots: list[str] = []
        self.social_image_alts: dict[str, list[str]] = {}
        self.stylesheets: list[str] = []
        self.scripts: list[str] = []
        self.h1_count = 0
        self.ids: set[str] = set()
        self.img_without_alt: list[str] = []
        self.meaningful_empty_alt: list[str] = []
        self.buttons_without_type = 0
        self.heading_text: list[str] = []
        self.scope_items: list[str] = []
        self.visible_text_nodes: list[str] = []
        self.videos: list[dict[str, str | None]] = []
        self._heading_tag = ""
        self._heading_parts: list[str] = []
        self._in_scope_list = False
        self._scope_item_parts: list[str] | None = None
        self._hidden_text_depth = 0

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = dict(attrs_list)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "title":
            self.in_title = True
        if tag == "meta" and attrs.get("name") == "description":
            self.descriptions.append(attrs.get("content", ""))
        if tag == "meta" and attrs.get("name") == "robots":
            self.robots.append(attrs.get("content", ""))
        social_key = attrs.get("property") or attrs.get("name")
        if tag == "meta" and social_key in ("og:image:alt", "twitter:image:alt"):
            self.social_image_alts.setdefault(social_key, []).append(attrs.get("content", ""))
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonicals.append(attrs.get("href", ""))
        if tag == "link" and attrs.get("rel") == "stylesheet":
            self.stylesheets.append(attrs.get("href", ""))
        if tag == "script" and attrs.get("src"):
            self.scripts.append(attrs["src"])
        if tag == "h1":
            self.h1_count += 1
        if re.fullmatch(r"h[1-6]", tag):
            self._heading_tag = tag
            self._heading_parts = []
        if tag == "img":
            source = attrs.get("src", "<unknown>")
            if "alt" not in attrs:
                self.img_without_alt.append(source)
            elif not (attrs.get("alt") or "").strip():
                classes = (attrs.get("class") or "").split()
                if source and attrs.get("aria-hidden") != "true" and "brand-logo" not in classes:
                    self.meaningful_empty_alt.append(source)
        if tag == "button" and "type" not in attrs:
            self.buttons_without_type += 1
        if tag == "video":
            self.videos.append(attrs)
        if tag in ("script", "style"):
            self._hidden_text_depth += 1
        if tag == "ul" and "scope-list" in (attrs.get("class") or "").split():
            self._in_scope_list = True
        if tag == "li" and self._in_scope_list:
            self._scope_item_parts = []
        for attribute in ("href", "src"):
            value = attrs.get(attribute)
            if value:
                self.links.append((attribute, value))

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False
        if tag == self._heading_tag:
            self.heading_text.append(" ".join("".join(self._heading_parts).split()))
            self._heading_tag = ""
            self._heading_parts = []
        if tag == "li" and self._scope_item_parts is not None:
            self.scope_items.append(" ".join("".join(self._scope_item_parts).split()))
            self._scope_item_parts = None
        if tag == "ul" and self._in_scope_list:
            self._in_scope_list = False
        if tag in ("script", "style"):
            self._hidden_text_depth = max(0, self._hidden_text_depth - 1)

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data
        if self._heading_tag:
            self._heading_parts.append(data)
        if self._scope_item_parts is not None:
            self._scope_item_parts.append(data)
        if not self._hidden_text_depth and data.strip():
            self.visible_text_nodes.append(data.strip())


def local_target(value: str) -> Path | None:
    if value.startswith(("#", "tel:", "mailto:", "data:", "javascript:")):
        return None
    parts = urlsplit(value)
    if parts.scheme or parts.netloc:
        return None
    path = unquote(parts.path)
    if not path:
        return None
    target = ROOT / path.lstrip("/")
    if path.endswith("/"):
        target /= "index.html"
    return target


def check() -> list[str]:
    errors: list[str] = []
    html_files = sorted(ROOT.rglob("*.html"))
    parsed: dict[Path, PageParser] = {}

    for page in html_files:
        parser = PageParser()
        parser.feed(page.read_text(encoding="utf-8"))
        parsed[page] = parser
        for attribute, value in parser.links:
            target = local_target(value)
            if target and not target.exists():
                errors.append(f"{page.relative_to(ROOT)}: missing {attribute} target {value}")

    for page, parser in parsed.items():
        for attribute, value in parser.links:
            parts = urlsplit(value)
            if attribute != "href" or not parts.fragment or parts.scheme or parts.netloc:
                continue
            target_page = page if not parts.path else local_target(value)
            target_parser = parsed.get(target_page) if target_page else None
            fragment = unquote(parts.fragment)
            if target_parser and fragment not in target_parser.ids:
                errors.append(f"{page.relative_to(ROOT)}: missing fragment target #{fragment} in {value}")

    titles: list[str] = []
    descriptions: list[str] = []
    for page in PRIMARY:
        parser = parsed.get(page)
        if not parser:
            errors.append(f"missing primary page {page.relative_to(ROOT)}")
            continue
        if not parser.title.strip():
            errors.append(f"{page.relative_to(ROOT)}: missing title")
        else:
            titles.append(parser.title.strip())
        if len(parser.descriptions) != 1 or not parser.descriptions[0].strip():
            errors.append(f"{page.relative_to(ROOT)}: needs one meta description")
        else:
            descriptions.append(parser.descriptions[0].strip())
        if len(parser.canonicals) != 1:
            errors.append(f"{page.relative_to(ROOT)}: needs one canonical link")
        elif not parser.canonicals[0].startswith(BASE_URL):
            errors.append(f"{page.relative_to(ROOT)}: canonical does not use production domain")
        expected_robots = "noindex,follow" if page.name == "404.html" else "index,follow,max-image-preview:large"
        if parser.robots != [expected_robots]:
            errors.append(f"{page.relative_to(ROOT)}: expected robots value {expected_robots}")
        if page.name != "404.html":
            for social_key in ("og:image:alt", "twitter:image:alt"):
                values = parser.social_image_alts.get(social_key, [])
                if len(values) != 1 or not values[0].strip():
                    errors.append(f"{page.relative_to(ROOT)}: needs one descriptive {social_key}")
            og_alt = parser.social_image_alts.get("og:image:alt", [""])[0]
            twitter_alt = parser.social_image_alts.get("twitter:image:alt", [""])[0]
            if og_alt and twitter_alt and og_alt != twitter_alt:
                errors.append(f"{page.relative_to(ROOT)}: social image alts do not match")
        if parser.h1_count != 1:
            errors.append(f"{page.relative_to(ROOT)}: expected one h1, found {parser.h1_count}")
        if not any(urlsplit(value).path == "/styles.css" for value in parser.stylesheets):
            errors.append(f"{page.relative_to(ROOT)}: shared stylesheet is missing")
        if not any(urlsplit(value).path == "/main.js" for value in parser.scripts):
            errors.append(f"{page.relative_to(ROOT)}: shared JavaScript is missing")
        if parser.img_without_alt:
            errors.append(f"{page.relative_to(ROOT)}: images missing alt {parser.img_without_alt}")
        if parser.meaningful_empty_alt:
            errors.append(f"{page.relative_to(ROOT)}: meaningful images have empty alt {parser.meaningful_empty_alt}")
        if parser.buttons_without_type:
            errors.append(f"{page.relative_to(ROOT)}: {parser.buttons_without_type} button(s) missing type")
        for heading in parser.heading_text:
            if heading.endswith("."):
                errors.append(f"{page.relative_to(ROOT)}: heading has a terminal period: {heading}")
        punctuated_scope = [item for item in parser.scope_items if re.search(r"[.!?]$", item)]
        if punctuated_scope:
            errors.append(f"{page.relative_to(ROOT)}: scope-list fragments have terminal punctuation {punctuated_scope}")
        for node in parser.visible_text_nodes:
            if re.search(r"[^\n]\s{2,}[^\n]", node):
                errors.append(f"{page.relative_to(ROOT)}: repeated visible whitespace in: {node[:90]}")
            if re.search(r"(?:\.\.|,,|!!|\?\?|!\?|\?!)", node):
                errors.append(f"{page.relative_to(ROOT)}: duplicate punctuation in: {node[:90]}")
        for video in parser.videos:
            if video.get("preload") != "none":
                errors.append(f"{page.relative_to(ROOT)}: video must use preload=none")
            if "autoplay" in video:
                errors.append(f"{page.relative_to(ROOT)}: video must not autoplay")
            for required_attribute in ("controls", "playsinline", "poster", "aria-label"):
                if required_attribute not in video:
                    errors.append(f"{page.relative_to(ROOT)}: video is missing {required_attribute}")

    for value, count in Counter(titles).items():
        if count > 1:
            errors.append(f"duplicate title used {count} times: {value}")
    for value, count in Counter(descriptions).items():
        if count > 1:
            errors.append(f"duplicate meta description used {count} times: {value}")

    for asset in ("styles.css", "mobile-fixes.css", "main.js", "favicon.svg", "hekman-logo.jpg", "robots.txt", "sitemap.xml", "llms.txt", "media-catalog.json", "vercel.json", ".vercelignore"):
        if not (ROOT / asset).is_file():
            errors.append(f"missing required asset {asset}")

    try:
        json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid vercel.json: {exc}")

    try:
        media_catalog = json.loads((ROOT / "media-catalog.json").read_text(encoding="utf-8"))
        expected_numbered = media_catalog["preservation"]["numberedProjectSeries"]["fileCount"]
        expected_named = media_catalog["preservation"]["namedSourcePhotoFiles"]["fileCount"]
        actual_numbered = len(list(ROOT.glob("project-[0-9][0-9][0-9].jpg")))
        actual_named = len(list(ROOT.glob("[0-9][0-9][0-9]-*.jpg")))
        if actual_numbered != expected_numbered:
            errors.append(f"media-catalog.json: expected {expected_numbered} numbered project images, found {actual_numbered}")
        if actual_named != expected_named:
            errors.append(f"media-catalog.json: expected {expected_named} named source photos, found {actual_named}")
        for collection in media_catalog.get("verifiedCollections", []):
            for filename in collection.get("assets", collection.get("sequence", [])):
                if not (ROOT / filename).is_file():
                    errors.append(f"media-catalog.json: missing collection asset {filename}")
            for sequence in collection.get("sequences", []):
                stages = sequence.get("stages", sequence.get("assets", []))
                if not stages:
                    errors.append(f"media-catalog.json: sequence has no stages or assets in {collection.get('id', '<unknown>')}")
                for stage in stages:
                    filename = stage if isinstance(stage, str) else stage.get("asset")
                    if filename and not (ROOT / filename).is_file():
                        errors.append(f"media-catalog.json: missing sequence asset {filename}")
            video = collection.get("video")
            if video and not (ROOT / video).is_file():
                errors.append(f"media-catalog.json: missing collection video {video}")
            for video in collection.get("videos", []):
                if not (ROOT / video).is_file():
                    errors.append(f"media-catalog.json: missing collection video {video}")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid media-catalog.json: {exc}")

    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    for raw_url in re.findall(r"url\((['\"]?)(.*?)\1\)", css):
        value = raw_url[1]
        target = local_target(value)
        if target and not target.exists():
            errors.append(f"styles.css: missing url target {value}")

    numbered_images = sorted(ROOT.glob("project-[0-9][0-9][0-9].jpg"))
    if len(numbered_images) != 169:
        errors.append(f"expected 169 numbered project images, found {len(numbered_images)}")

    image_changes = [
        path for path in ROOT.glob("*.jpg") if not path.is_file()
    ]
    if image_changes:
        errors.append("unexpected image entries found")

    projects_html = (ROOT / "projects/index.html").read_text(encoding="utf-8")
    gallery_count = projects_html.count('class="project-card reveal"')
    expected_gallery_count = media_catalog.get("displayStrategy", {}).get("projectGalleryPhotographs") if "media_catalog" in locals() else None
    if expected_gallery_count is not None and gallery_count != expected_gallery_count:
        errors.append(f"projects/index.html: expected {expected_gallery_count} gallery photographs, found {gallery_count}")

    visible_card_copy: list[tuple[str, str]] = []
    for page, markup in (("index.html", (ROOT / "index.html").read_text(encoding="utf-8")), ("projects/index.html", projects_html)):
        blocks = re.findall(r'<a class="[^"]*\bstory-card\b[^"]*"[^>]*>(.*?)</a>', markup, re.DOTALL)
        blocks += re.findall(r'<figure class="project-card reveal"[^>]*>(.*?)</figure>', markup, re.DOTALL)
        for block in blocks:
            copy = re.sub(r"<[^>]+>", " ", block)
            copy = " ".join(copy.split())
            visible_card_copy.append((page, copy))
    card_counts = Counter(copy for _, copy in visible_card_copy)
    for copy, count in card_counts.items():
        if copy and count > 1:
            errors.append(f"duplicate visible card copy used {count} times: {copy[:110]}")

    for page in PRIMARY:
        text = page.read_text(encoding="utf-8") if page.exists() else ""
        if "/assets/" in text:
            errors.append(f"{page.relative_to(ROOT)}: legacy /assets/ reference remains")
        for phrase in (
            "identified responsibly",
            "source image library",
            "complete numbered photo library",
            "preserved in the repository",
            "verified project group",
            "browse the work by category",
        ):
            if phrase in text.lower():
                errors.append(f"{page.relative_to(ROOT)}: internal-facing copy remains: {phrase}")
        visible_text = " ".join(parsed[page].visible_text_nodes) if page in parsed else ""
        if re.search(r"\b(?:lorem ipsum|todo|coming soon|placeholder)\b", visible_text, re.IGNORECASE):
            errors.append(f"{page.relative_to(ROOT)}: placeholder copy remains")
        for match in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.DOTALL):
            try:
                json.loads(match)
            except json.JSONDecodeError as exc:
                errors.append(f"{page.relative_to(ROOT)}: invalid JSON-LD: {exc}")

    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    for page in PRIMARY:
        if page.name == "404.html":
            continue
        relative = page.relative_to(ROOT)
        route = "/" if relative.as_posix() == "index.html" else f"/{relative.parent.as_posix()}/"
        if f"<loc>{BASE_URL}{route}</loc>" not in sitemap:
            errors.append(f"sitemap.xml: missing primary route {route}")

    for project_page in sorted((ROOT / "projects").glob("*/index.html")):
        route = f"/{project_page.relative_to(ROOT).parent.as_posix()}/"
        project_markup = project_page.read_text(encoding="utf-8")
        if '"@type":"Article"' not in project_markup:
            errors.append(f"{project_page.relative_to(ROOT)}: project story is missing Article structured data")
        if '"@type":"BreadcrumbList"' not in project_markup:
            errors.append(f"{project_page.relative_to(ROOT)}: project story is missing BreadcrumbList structured data")
        if '<meta property="og:type" content="article">' not in project_markup:
            errors.append(f"{project_page.relative_to(ROOT)}: project story must use og:type article")
        inbound_pages = {
            source_page
            for source_page, parser in parsed.items()
            if source_page != project_page
            and any(
                attribute == "href"
                and not urlsplit(value).scheme
                and not urlsplit(value).netloc
                and urlsplit(value).path == route
                for attribute, value in parser.links
            )
        }
        if not inbound_pages:
            errors.append(f"{project_page.relative_to(ROOT)}: project story has no inbound HTML link")

    public_html = "\n".join(page.read_text(encoding="utf-8") for page in html_files)
    for private_reference in ("pixie", "paige", "salon-after-2.jpg"):
        if private_reference.lower() in public_html.lower():
            errors.append(f"public HTML exposes private salon reference: {private_reference}")

    optimized_videos = media_catalog.get("videoDelivery", {}).get("optimizedFiles", []) if "media_catalog" in locals() else []
    for video in optimized_videos:
        path = ROOT / video
        if not path.is_file():
            errors.append(f"missing optimized video {video}")
        elif path.stat().st_size > 2_000_000:
            errors.append(f"optimized video exceeds 2 MB: {video}")

    medway_page = (ROOT / "projects/medway-flooring-storage/index.html").read_text(encoding="utf-8")
    porch_page = (ROOT / "projects/westmount-porch-entry/index.html").read_text(encoding="utf-8")
    westmount_page = (ROOT / "projects/westmount-1970s-transformation/index.html").read_text(encoding="utf-8")
    melrose_page = (ROOT / "projects/melrose-bathroom-layout/index.html").read_text(encoding="utf-8")
    hyde_park_page = (ROOT / "projects/hyde-park-kitchen-renewal/index.html").read_text(encoding="utf-8")
    blackfriars_page = (ROOT / "projects/blackfriars-leak-restoration/index.html").read_text(encoding="utf-8")
    salon_page = (ROOT / "projects/commercial-salon-repair/index.html").read_text(encoding="utf-8")
    pond_mills_page = (ROOT / "projects/pond-mills-home-repairs/index.html").read_text(encoding="utf-8")
    deck_page = (ROOT / "projects/multi-unit-deck-renewal/index.html").read_text(encoding="utf-8")
    about_page = (ROOT / "about/index.html").read_text(encoding="utf-8")
    homepage = (ROOT / "index.html").read_text(encoding="utf-8")

    for required in (
        "Carpet was removed from three rooms",
        "new double closet",
        "medway-floor-door-transition.jpg",
        "Anonymous Medway homeowner",
    ):
        if required not in medway_page:
            errors.append(f"Medway project page is missing required detail: {required}")
    if "winding" in medway_page.lower():
        errors.append("Medway project page exposes the former street-based project label")

    for required in (
        "repeat Westmount customer",
        "westmount-porch-work-in-progress.jpg",
        "westmount-porch-after-day.jpg",
        "westmount-porch-after-night.jpg",
    ):
        if required.lower() not in porch_page.lower():
            errors.append(f"Westmount porch page is missing required detail: {required}")

    for required in (
        "Project in progress",
        "one powder-room renovation",
        "white 2-inch by 10-inch subway tile",
        "herringbone pattern",
        "not the final after",
    ):
        if required.lower() not in westmount_page.lower():
            errors.append(f"Phased Westmount page is missing required detail: {required}")
    if "multiple bathroom" in westmount_page.lower() or "two bathroom" in westmount_page.lower():
        errors.append("Phased Westmount page overstates the confirmed one-powder-room scope")

    for required in ("Melrose area", "other side of an existing wall", "wall-hung toilet", "new dedicated utility room", "exercise room", "melrose-bathroom-tour.mp4"):
        if required.lower() not in melrose_page.lower():
            errors.append(f"Melrose project page is missing required detail: {required}")
    if re.search(r"\b(?:street|road|avenue|drive)\b", melrose_page, re.IGNORECASE):
        errors.append("Melrose project page may expose a location more precise than the Melrose area")

    for required in ("refaced", "purpose-built pantry", "dishwasher", "backsplash", "less than $20,000", "not a fixed package or a guarantee"):
        if required.lower() not in hyde_park_page.lower():
            errors.append(f"Hyde Park project page is missing required detail: {required}")

    for required in ("mold", "evidence of mice", "structural concerns", "knob-and-tube wiring", "coordinated the appropriate remediation team and qualified trades", "restored the drywall"):
        if required.lower() not in blackfriars_page.lower():
            errors.append(f"Blackfriars project page is missing required detail: {required}")
    for prohibited in ("we remediated the mold", "Hekman remediated the mold", "we replaced the knob-and-tube"):
        if prohibited.lower() in blackfriars_page.lower():
            errors.append(f"Blackfriars project page overstates regulated work: {prohibited}")

    for required in (
        "The repair disappears",
        "Moisture investigation",
        "salon-moisture-investigation.jpg",
        "salon-affected-wallboard.jpg",
        "salon-wall-ceiling-rebuild.jpg",
        "salon-restored-wall.jpg",
        "salon-restored-wall-detail.jpg",
        '"@type":"Article"',
    ):
        if required.lower() not in salon_page.lower():
            errors.append(f"Salon project page is missing required detail: {required}")
    for prohibited in ("pixie", "paige", "salon-after-2.jpg", "mould", "mold"):
        if prohibited.lower() in salon_page.lower():
            errors.append(f"Salon project page exposes an unsupported or private reference: {prohibited}")

    for required in (
        "home had not sold",
        "wet conditions around window wells",
        "problem weeping pipe",
        "localized grading",
        "downspout",
        "pond-mills-kitchen-floor-before.jpg",
        "pond-mills-kitchen-floor-after.jpg",
        "pond-mills-basement-subfloor-prep.jpg",
        "pond-mills-basement-floor-installation.jpg",
        "pond-mills-basement-floor-after.jpg",
        "pond-mills-flooring-finished-tour.mp4",
    ):
        if required.lower() not in pond_mills_page.lower():
            errors.append(f"Pond Mills project page is missing required detail: {required}")
    for prohibited in ("sold after", "then sold", "helped the home sell", "salon-"):
        if prohibited.lower() in pond_mills_page.lower():
            errors.append(f"Pond Mills project page contains an unsupported or mixed-job reference: {prohibited}")

    for required in (
        "multi-unit-decks-before.jpg",
        "project-101.jpg",
        "project-100.jpg",
        "project-104.jpg",
        "multi-unit-deck-repair-sequence.mp4",
        "anonymous multi-unit property",
    ):
        if required.lower() not in deck_page.lower():
            errors.append(f"Multi-unit deck page is missing required detail: {required}")
    for prohibited in ("permit", "code compliant", "engineered", "full replacement"):
        if prohibited.lower() in deck_page.lower():
            errors.append(f"Multi-unit deck page makes an unsupported claim: {prohibited}")

    numbered_markup = re.compile(r"<span>0([1-9])</span>")
    for page in PRIMARY:
        if not page.exists():
            continue
        count = len(numbered_markup.findall(page.read_text(encoding="utf-8")))
        expected = 4 if page == ROOT / "index.html" else 0
        if count != expected:
            errors.append(f"{page.relative_to(ROOT)}: expected {expected} numbered process markers, found {count}")

    for required in (
        'id="hekman-promise"',
        "Honest advice &amp; transparent pricing",
        "Approval before additional work",
        "two-year workmanship guarantee",
    ):
        if required.lower() not in about_page.lower():
            errors.append(f"About page is missing Hekman Promise detail: {required}")

    positioning = "Based in Westmount and working across London"
    if positioning not in homepage:
        errors.append("Homepage is missing the required all-London positioning statement")
    for neighbourhood in ("Sunningdale", "Old North", "Stoneybrook"):
        if neighbourhood not in homepage:
            errors.append(f"Homepage service area is missing {neighbourhood}")
        if neighbourhood not in (ROOT / "llms.txt").read_text(encoding="utf-8"):
            errors.append(f"llms.txt service area is missing {neighbourhood}")

    return errors


if __name__ == "__main__":
    problems = check()
    if problems:
        print(f"Validation failed with {len(problems)} issue(s):")
        for problem in problems:
            print(f"- {problem}")
        sys.exit(1)
    print(f"Validation passed for {len(PRIMARY)} primary pages.")
    print("All local HTML references resolve; metadata and accessibility basics passed.")
    print("All 169 numbered project images remain present.")
