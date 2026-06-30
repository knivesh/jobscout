"""Utilities for persisting raw fetch results."""

import json
import re
from pathlib import Path


def slugify(name: str) -> str:
    """Convert a company name to a safe filename stem."""
    return re.sub(r"[^\w]+", "_", name.lower()).strip("_")


def save_raw(company_name: str, jobs: list[dict], run_ts: str) -> Path:
    """Write jobs to data/raw/{run_ts}/{slug}.json and return the path."""
    path = Path("data") / "raw" / run_ts / f"{slugify(company_name)}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=2)
    return path
