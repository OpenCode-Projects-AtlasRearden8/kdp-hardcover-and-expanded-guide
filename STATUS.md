# STATUS.md — KDP Hardcover and Expanded Guide

Last updated: 2026-11-07

## What was built

A focused beginner manual for KDP's *harder* post-first-launch buttons, delivered as Markdown sources plus a tested static-site build with an SVG decision flowchart.

### The manual (`docs/`, 10 pages)

1. **`index.md`** — who it's for, explicit differentiation from the three sibling guides (First KDP Book Roadmap, Series and Boxset, Publishing Beyond KDP), a four-point honest summary up front, disclaimers.
2. **`01-when-a-hardcover-earns-its-setup-cost.md`** — no-setup-fee vs. real per-unit economics, hardcover trim/page-count limits, a worked illustrative paperback-vs-hardcover table, five "earns its place" triggers, the "one-question test."
3. **`02-case-laminate-vs-jacket-math.md`** — the two finishes side by side (files, cost, durability, gift signal), the shared royalty formula, an illustrative jacket delta (~$1.50/unit at 300 pages), the price-floor consequence, five choosing questions, real file anatomy, and the publisher's actual choice with reasons.
4. **`03-expanded-distribution-tradeoffs.md`** — what ED does, the *ED ≠ going wide* distinction (visual vocabulary guardrail), the royalty mechanics in plain English, the durable five-step method for reading the numbers yourself, non-money tradeoffs (price floor, returns, channel pricing), when worth it / when not, calm procedure.
5. **`04-preorders-without-surprises.md`** — how KDP preorders work, the three classic surprises (slipped date, price change under early buyers, format mix-up) with hard rules and fixes, when preorders are right (and when they're not), a calm run-of-show.
6. **`05-author-copies-events-giveaways.md`** — what author copies are, cost = print cost, marketplace availability quirks (hardcover often US-only — verify), the giveaway-cost table and event-margin table, three honest uses (signing events incl. card-reader pitfalls, review mailouts, budgeted giveaways), ordering procedure, when author copies are the wrong tool.
7. **`06-royalty-differences-plain-english.md`** — the only two formulas needed, a one-table comparison across ebook tiers, paperback, both hardcover finishes, and ED; a 100-copy mixed-channel walkthrough; a lazily-priced-hardcover anti-example; ~60-day payment timing; surprising-differences list.
8. **`07-decision-flowchart.md`** — a hand-drawn SVG decision flowchart (8 questions, 4 endings: WAIT for reader data / SKIP ED / NO PREORDER / DONE) embedded raw in Markdown and rendered on the site page, plus a plain-sentence reading of the endings.
9. **`checklists.md`** — printable per-chapter checklists with verify-flags.
10. **`glossary.md`** — plain-English definitions (author copies, case laminate, ED vs. going wide, jacket, price floor, preorder rules, printing cost, returnability, trim size, etc.).

All numeric KDP claims are either explicitly marked **illustrative** or paired with a verify note pointing at the correct help page. Education-only, no affiliate links, no secrets, no personal data.

### The site (`site/`, generated)

Static HTML built by `build.py`: one page per chapter, sticky sidebar with `aria-current` marking, prev/home/next pager, footer with `Copyright (c) 2026 Asdale Dynamics, LLC` and the education-not-advice disclaimer. A distinct palette (calm violet, green "done" boxes, amber "watch out" boxes) and flowchart/print styles distinguish it from sibling guides' sites. Fully offline — no external fonts or CDNs. The flowchart page is print-friendly (print CSS hides nav/footer).

### The build

- **`build.py`** (Python, stdlib + `markdown`): converts `docs/*.md` in canonical `PAGE_ORDER` into `site/*.html` + copied CSS. Strict `discover_pages`: missing *or unexpected* docs fail the build. Deterministic outputs; stale HTML is cleaned. CLI: `python3 build.py [--docs DIR] [--out DIR] [--style FILE]`.
- **`test_build.py`** (pytest, **23 tests**): title extraction/escaping, canonical order, missing- and extra-doc failure, full build + assets, footer/disclaimer presence, nav correctness, stale cleanup, determinism, SVG-survives-Markdown test (fixture + real-content), CLI success/error, a no-secrets/no-email scan of output, and a content distinctness smoke test.

## How to run it

```bash
pip install markdown    # the only non-stdlib dependency
python3 build.py        # build docs/ -> site/
python3 -m pytest       # run the test suite
```

Then open `site/index.html` in a browser (no server needed); flowchart at `site/07-decision-flowchart.html`.

## Verification results

- `python3 -m pytest` → **23 passed**.
- `python3 build.py` → **built 10 pages -> site/**, exit 0; all 10 HTML files + `site/assets/style.css` present.
- Flowchart page spot-check: `<svg>` present, all eight question labels (Q1–Q8) render, all four ending boxes present.
- HTML balance check: all 10 pages parse with no unclosed/mismatched tags.
- Garble scan: no known-bad tokens in any `docs/` or `site/` file; bold-marker balance clean.
- No-secrets test passes (no `sk-…` tokens, no `@` emails in output).

## Known gaps

- **KDP numbers age.** Every rate, price floor, page-count limit, and preorder window in the manual is hedged and marked verify-current-help-docs; no automated check ties them to KDP's site (deliberately — no scraping, local-first).
- **Illustrative numbers, not a calculator.** The per-unit tables use invented round numbers. Companion repo `kdp-profit-planner` (calculator) pairs with this; this repo is the manual.
- **Flowchart is static SVG**, not interactive: good for reading and printing, but no clickable states or form inputs; a web-app version would be its own repo.
- **No ebook-side preorder guidance** beyond what touches print decisions — the sibling Series guide and Publishing Beyond guide own those topics.
- **Site is minimal by design** — no search, no dark mode; suggestions if it grows: print-optimized one-pager and a search box.
