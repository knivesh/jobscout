"""Fetch jobs from all known companies and print a one-line summary each."""

from datetime import datetime, timezone

from registry import PLATFORMS
from utils.storage import save_raw

COMPANIES = [
    {"name": "ABN AMRO", "base_url": "https://www.werkenbijabnamro.nl/en", "platform": "getnoticed"},
    {"name": "BDO", "base_url": "https://www.werkenbijbdo.nl", "platform": "getnoticed"},
    {"name": "Randstad", "base_url": "https://www.werkenbijrandstad.nl", "platform": "getnoticed"},
    {"name": "Adyen", "token": "adyen", "platform": "greenhouse"},
    {"name": "Databricks", "token": "databricks", "platform": "greenhouse"},
]


def main():
    """Fetch all companies and save raw results."""
    run_ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for company in COMPANIES:
        platform = PLATFORMS[company["platform"]]
        jobs = platform.fetch(company)
        path = save_raw(company["name"], jobs, run_ts, company["platform"])
        print(f"{company['name']}: {len(jobs)} jobs -> {path}")


if __name__ == "__main__":
    main()
