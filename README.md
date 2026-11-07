# KDP Hardcover and Expanded Guide

A calm, plain-English manual for KDP's *harder* buttons — the ones you meet after your first paperback:

- **When a hardcover earns its setup cost** (and when it's a trophy, not a tool)
- **Case laminate vs. dust jacket math** — two finishes, two file sets, two cost stories
- **Expanded distribution tradeoffs** — libraries and bookstores in exchange for a lower royalty (and how ED differs from "going wide")
- **Preorders without surprises** — the price-change and date-slip rules that bite
- **Author copies for events and giveaways** — your best per-unit deal in KDP, used well
- **Royalty differences in plain English** — one table comparing every channel's take
- **A decision flowchart** — the whole guide as one walkable diagram, rendered as SVG on the site

One chapter, one decision. Every numeric claim is either marked *illustrative* or paired with a **verify against current KDP help documentation** note. No affiliate links, no hype.

Everything here is grounded in the real experience of publishing *The Massive AI Manual* — a book from [Asdale Dynamics, LLC](https://dylanasdale.github.io) that explains AI "like a friend would" — including its own hardcover edition through KDP.

**Related sibling guides (separate repos):** *First KDP Book Roadmap Guide* (your first launch), *Series and Boxset KDP Guide* (series and box sets), and *Publishing Beyond KDP Guide* (wide platforms). This guide deliberately covers none of those topics in depth.

**Important:** this repository contains education, not legal, tax, or accounting advice, and no affiliate links or upsells. KDP's rates, floors, and limits change; the guide's *method* is durable, but *always* verify current numbers against Amazon's help documentation before you press any button.

## What's in this repo

| Path | What it is |
| --- | --- |
| `docs/` | The manual's source: one Markdown file per chapter, plus `checklists.md` and `glossary.md` |
| `build.py` | Tested build script that renders `docs/` into a static HTML site |
| `assets/style.css` | The site's stylesheet (flowchart-aware, includes print rules) |
| `site/` | Generated static site (`index.html`, one page per chapter, the SVG decision flowchart) |
| `test_build.py` | Test suite for the build script: `pytest` |
| `STATUS.md` | What was built, how to verify, known gaps |

## Run it

You need Python 3.10+ and the `markdown` package (`pip install markdown`).

```bash
# Build the site (docs/ -> site/)
python3 build.py

# Custom paths
python3 build.py --docs docs --out site --style assets/style.css

# Run the test suite
python3 -m pytest
```

The generated `site/` is fully static — open `site/index.html` in a browser, no server needed. The decision flowchart lives at `site/07-decision-flowchart.html` and is print-friendly.

## Reuse this guide's structure

Copy the structure freely: one Markdown file per chapter, a `PAGE_ORDER` list in `build.py`, worked-*method* examples with clearly labeled illustrative numbers, checklists, a glossary, and one SVG decision page. The build script and content are MIT-licensed (see `LICENSE`), attributed to `Copyright (c) 2026 Asdale Dynamics, LLC`.

## Credits

Written and maintained by **Asdale Dynamics, LLC** — publishers of beginner-friendly AI education, books, guides, and small-business/author tools. Learn more at [dylanasdale.github.io](https://dylanasdale.github.io).

## License

MIT — see [LICENSE](LICENSE). Copyright line: `Copyright (c) 2026 Asdale Dynamics, LLC`.
