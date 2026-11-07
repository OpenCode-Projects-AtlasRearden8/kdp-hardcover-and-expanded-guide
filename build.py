#!/usr/bin/env python3
"""Build the static HTML site from the Markdown manual in docs/.

Usage:
    python3 build.py [--docs DOCS_DIR] [--out OUT_DIR] [--style STYLE_FILE]

Defaults: docs/ -> site/, stylesheet from assets/style.css.

No network access, no secrets, stdlib + `markdown` package only.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import markdown

PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_DOCS = PROJECT_ROOT / "docs"
DEFAULT_OUT = PROJECT_ROOT / "site"
DEFAULT_STYLE = PROJECT_ROOT / "assets" / "style.css"

BRAND = "KDP Hardcover and Expanded Guide"
TAGLINE = "KDP's harder buttons — hardcover, laminate vs. jacket, ED, preorders — explained like a friend would"
PUBLISHER = "Asdale Dynamics, LLC"
HUB_URL = "https://dylanasdale.github.io"
COPYRIGHT_LINE = "Copyright (c) 2026 Asdale Dynamics, LLC"
DISCLAIMER = (
    "Education only &mdash; not legal, tax, or accounting advice. "
    "KDP numbers change; always verify against Amazon's current help documentation."
)

# Reading order: file stems. "index" is first and serves as the home page.
PAGE_ORDER = [
    "index",
    "01-when-a-hardcover-earns-its-setup-cost",
    "02-case-laminate-vs-jacket-math",
    "03-expanded-distribution-tradeoffs",
    "04-preorders-without-surprises",
    "05-author-copies-events-giveaways",
    "06-royalty-differences-plain-english",
    "07-decision-flowchart",
    "checklists",
    "glossary",
]

MD_EXTENSIONS = ["extra", "sane_lists", "toc"]

H1_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.DOTALL)


def html_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def slugify(source: Path) -> str:
    """File stem, which serves as the slug ('index' is the home page)."""
    return source.stem


def page_title(html_body: str, source: Path) -> str:
    """Extract the first <h1> text as a plain-text title; fall back to the stem."""
    match = H1_RE.search(html_body)
    if not match:
        return slugify(source).replace("-", " ").title()
    # Strip inner markup (e.g. anchors produced by the toc extension), then
    # escape so the title is safe to interpolate into HTML.
    text = re.sub(r"<[^>]+>", "", match.group(1))
    return html_escape(text.strip())


def page_body(html_body: str) -> str:
    """Article HTML with the leading <h1> removed (it is rendered separately)."""
    return H1_RE.sub("", html_body, count=1).strip()


def discover_pages(docs_dir: Path) -> list[Path]:
    """Markdown sources in canonical reading order; error on missing files."""
    found = {p.stem: p for p in docs_dir.glob("*.md")}
    missing = [slug for slug in PAGE_ORDER if slug not in found]
    if missing:
        raise SystemExit(f"build: missing expected docs: {', '.join(missing)}")
    order = {slug: i for i, slug in enumerate(PAGE_ORDER)}
    extras = sorted(s for s in found if s not in order)
    if extras:
        raise SystemExit(
            "build: unexpected docs not in PAGE_ORDER: " + ", ".join(extras)
        )
    return [found[slug] for slug in PAGE_ORDER]


def render_page(source: Path, sources: list[Path], titles: dict[Path, str],
                bodies: dict[Path, str], style_href: str) -> str:
    """Full standalone HTML document for one page."""
    sidebar_items = []
    for other in sources:
        current = ' aria-current="page"' if other == source else ""
        sidebar_items.append(
            f"<li><a href='{other.stem}.html'{current}>{titles[other]}</a></li>"
        )
    sidebar = "\n".join(sidebar_items)

    pos = sources.index(source)
    prev_link = (
        f"<span><a href='{sources[pos - 1].stem}.html'>&larr; Prev</a></span>"
        if pos > 0
        else "<span></span>"
    )
    next_link = (
        f"<span><a href='{sources[pos + 1].stem}.html'>Next &rarr;</a></span>"
        if pos + 1 < len(sources)
        else "<span></span>"
    )
    pager = (
        f"<nav class='pager' aria-label='Pager'>{prev_link}"
        f"<span><a href='index.html'>Home</a></span>{next_link}</nav>"
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titles[source]} &middot; {html_escape(BRAND)}</title>
<meta name="description" content="Beginner-friendly guide to KDP hardcovers, case laminate vs. jacket, expanded distribution, preorders, author copies, and royalty differences. {DISCLAIMER}">
<link rel="stylesheet" href="{style_href}">
</head>
<body>
<header class="site">
  <div class="inner">
    <a class="brand" href="index.html">{html_escape(BRAND)}</a>
    <span class="tagline">{html_escape(TAGLINE)}</span>
  </div>
</header>
<div class="layout">
<nav class="sidebar" aria-label="Pages">
<h2>Manual</h2>
<ul>
{sidebar}
</ul>
</nav>
<main>
<article>
<h1>{titles[source]}</h1>
{bodies[source]}
{pager}
</article>
</main>
</div>
<footer class="site">
  <div class="inner">
    <p>{COPYRIGHT_LINE}. Published by {PUBLISHER} &middot; <a href="{HUB_URL}">{HUB_URL}</a>.</p>
    <p>{DISCLAIMER}</p>
  </div>
</footer>
</body>
</html>
"""


def build(docs_dir: Path, out_dir: Path, style_path: Path) -> dict:
    """Render every markdown source to a standalone HTML page. Returns stats."""
    sources = discover_pages(docs_dir)

    md = markdown.Markdown(extensions=MD_EXTENSIONS)
    titles: dict[Path, str] = {}
    bodies: dict[Path, str] = {}
    for src in sources:
        md.reset()
        html_body = md.convert(src.read_text(encoding="utf-8"))
        titles[src] = page_title(html_body, src)
        bodies[src] = page_body(html_body)

    style_href = f"assets/{style_path.name}"

    out_dir.mkdir(parents=True, exist_ok=True)
    assets_dir = out_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    (assets_dir / style_path.name).write_text(
        style_path.read_text(encoding="utf-8"), encoding="utf-8"
    )

    for src in sources:
        html = render_page(src, sources, titles, bodies, style_href)
        (out_dir / f"{src.stem}.html").write_text(html, encoding="utf-8")

    # Remove stale HTML files from previous builds.
    for stale in out_dir.glob("*.html"):
        if stale.stem not in {s.stem for s in sources}:
            stale.unlink()

    return {
        "pages": len(sources),
        "titles": {src.stem: titles[src] for src in sources},
        "out_dir": str(out_dir),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build the static site from docs/ markdown."
    )
    parser.add_argument("--docs", type=Path, default=DEFAULT_DOCS)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--style", type=Path, default=DEFAULT_STYLE)
    args = parser.parse_args(argv)
    for required in (args.docs, args.style):
        if not required.exists():
            print(f"build: required path not found: {required}", file=sys.stderr)
            return 2
    stats = build(args.docs, args.out, args.style)
    print(f"built {stats['pages']} pages -> {stats['out_dir']}")
    for slug, title in stats["titles"].items():
        print(f"  {slug} :: {title}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
