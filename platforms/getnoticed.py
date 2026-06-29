"""GetNoticed platform: shared JSON vacancy API (ABN AMRO, BDO, Randstad)."""

import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Firefox/152.0",
    "Accept": "application/json, text/plain, */*",
    "X-Requested-With": "XMLHttpRequest",
    "Accept-Language": "en-US,en;q=0.9",
}


def fetch(company: dict) -> list[dict]:
    """Fetch all vacancies for a GetNoticed-based company.

    Args:
        company: dict with "name" and "base_url".

    Returns:
        List of raw vacancy dicts, deduped by id.
    """
    url = f"{company['base_url']}/api/vacancy/"
    page = 1
    unique = {}
    total_pages = 1

    while page <= total_pages:
        params = {"sort": "created", "sortDir": "DESC", "pageNumber": page}
        data = requests.get(url, params=params, headers=HEADERS, timeout=20).json()
        total_pages = data["meta"]["totalPageCount"]
        for vacancy in data["vacancies"]:
            unique[vacancy["id"]] = vacancy
        page += 1

    if len(unique) != data["meta"]["num_total_hits"]:
        print(f"{company['name']}: collected {len(unique)}, meta said {data['meta']['num_total_hits']}")

    return list(unique.values())
