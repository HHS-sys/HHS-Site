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
PRIMARY = [
    ROOT / "index.html",
    ROOT / "services/index.html",
    *sorted((ROOT / "services").glob("*/index.html")),
    ROOT / "projects/index.html",
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
        self.stylesheets: list[str] = []
        self.scripts: list[str] = []
        self.h1_count = 0
        self.img_without_alt: list[str] = []
        self.buttons_without_type = 0

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = dict(attrs_list)
        if tag == "title":
            self.in_title = True
        if tag == "meta" and attrs.get("name") == "description":
            self.descriptions.append(attrs.get("content", ""))
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonicals.append(attrs.get("href", ""))
        if tag == "link" and attrs.get("rel") == "stylesheet":
            self.stylesheets.append(attrs.get("href", ""))
        if tag == "script" and attrs.get("src"):
            self.scripts.append(attrs["src"])
        if tag == "h1":
            self.h1_count += 1
        if tag == "img" and "alt" not in attrs:
            self.img_without_alt.append(attrs.get("src", "<unknown>"))
        if tag == "button" and "type" not in attrs:
            self.buttons_without_type += 1
        for attribute in ("href", "src"):
            value = attrs.get(attribute)
            if value:
                self.links.append((attribute, value))

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data


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
        if parser.h1_count != 1:
            errors.append(f"{page.relative_to(ROOT)}: expected one h1, found {parser.h1_count}")
        if "/styles.css" not in parser.stylesheets:
            errors.append(f"{page.relative_to(ROOT)}: shared stylesheet is missing")
        if "/main.js" not in parser.scripts:
            errors.append(f"{page.relative_to(ROOT)}: shared JavaScript is missing")
        if parser.img_without_alt:
            errors.append(f"{page.relative_to(ROOT)}: images missing alt {parser.img_without_alt}")
        if parser.buttons_without_type:
            errors.append(f"{page.relative_to(ROOT)}: {parser.buttons_without_type} button(s) missing type")

    for value, count in Counter(titles).items():
        if count > 1:
            errors.append(f"duplicate title used {count} times: {value}")
    for value, count in Counter(descriptions).items():
        if count > 1:
            errors.append(f"duplicate meta description used {count} times: {value}")

    for asset in ("styles.css", "main.js", "favicon.svg", "robots.txt", "sitemap.xml", "vercel.json"):
        if not (ROOT / asset).is_file():
            errors.append(f"missing required asset {asset}")

    try:
        json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid vercel.json: {exc}")

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

    for page in PRIMARY:
        text = page.read_text(encoding="utf-8") if page.exists() else ""
        if "/assets/" in text:
            errors.append(f"{page.relative_to(ROOT)}: legacy /assets/ reference remains")

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
