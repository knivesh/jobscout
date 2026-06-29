# CLAUDE.md

Guidance for Claude Code working in this repo.

## Project Goal

A small, personal, locally-run job radar: monitors NL employer career sites and
surfaces new job postings (focus on ML / data roles). Not production software —
favour simplicity over completeness.

## Working Style (important)

Keep it simple. When in doubt, do less.

- Simple, readable code over clever/abstract code.
- Plain functions; use a class only when it genuinely simplifies state. No deep inheritance.
- Stdlib first. Ask before adding any dependency.
- Don't add features, config, logging, or error handling I didn't ask for. Suggest, don't build.
- One file = one job. Smallest change that satisfies the request.
- If ambiguous, ask — don't guess.

## Conventions

- Python 3.14 via `uv`. Use `uv add` / `uv run`, never bare `pip`.
- Google-style docstrings; one line is fine for simple functions.
- Clear names over comments. Comment only the non-obvious "why".

## Platform Contract

Each career-site platform = one file in `platforms/` (e.g. `getnoticed.py`),
exposing one function with the same signature and output shape:

    fetch(company) -> list[dict]

All platforms return the SAME dict shape so results merge without special-casing.
Register new platforms in `registry.py` (name -> module). This rule is the backbone —
don't break it.

## Commands

```bash
uv sync                  # install deps
uv run python main.py    # run
uv run jupyter notebook  # explore
```

## Architecture

- `main.py` — entry point
- `platforms/` — one module per platform (the `fetch()` contract)
- `registry.py` — platform name -> module
- `notebooks/` — exploration before promoting a site to a platform module

## Platforms

### GetNoticed (one recipe — other platforms differ)

ABN AMRO, BDO, Randstad run on GetNoticed and share a JSON vacancy API:

GET <base_url>/api/vacancy/   params: sort=created, sortDir=DESC, pageNumber=<n>
Response: { vacancies: [...], facets: {...}, meta: { num_total_hits, totalPageCount } }

- Page-based pagination; collect all pages, dedupe by `id`. `meta.num_total_hits` = expected total.
- Keep each vacancy object **as-is** — do not select, rename, or drop fields. (Field selection is a later parsing phase.)
- Endpoint may be `/api/vacancy/` or `/en/api/vacancy/`; each company stores its own base URL.
- Needs browser `User-Agent` + `X-Requested-With: XMLHttpRequest`.

| Site | Base URL |
|------|----------|
| ABN AMRO | `https://www.werkenbijabnamro.nl` |
| BDO | `https://www.werkenbijbdo.nl` |
| Randstad | `https://www.werkenbijrandstad.nl` |

## Out of Scope (until I ask)

No saving/DB/files · no tests · no deployment/scheduling/Docker/CI · no alerts ·
no filtering/cleaning (this phase only fetches raw jobs).

For now: just fetch and print/return results.
