"""Greenhouse platform: public Boards API."""

import requests


def fetch(company: dict) -> list[dict]:
    """Fetch all jobs for a Greenhouse board.

    Args:
        company: dict with "name" and "token".

    Returns:
        List of raw job dicts, deduped by id.
    """
    url = f"https://boards-api.greenhouse.io/v1/boards/{company['token']}/jobs"
    data = requests.get(url, params={"content": "true", "page": 1}, timeout=20).json()
    total = data["meta"]["total"]
    unique = {j["id"]: j for j in data["jobs"]}

    page = 2
    while len(unique) < total:
        data = requests.get(url, params={"content": "true", "page": page}, timeout=20).json()
        for job in data["jobs"]:
            unique[job["id"]] = job
        page += 1

    if len(unique) != total:
        print(f"{company['name']}: collected {len(unique)}, meta said {total}")

    return list(unique.values())
