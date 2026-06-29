"""Fetch jobs from all known companies and print a one-line summary each."""

from registry import PLATFORMS

COMPANIES = [
    {"name": "ABN AMRO", "base_url": "https://www.werkenbijabnamro.nl/en", "platform": "getnoticed"},
    {"name": "BDO", "base_url": "https://www.werkenbijbdo.nl", "platform": "getnoticed"},
    {"name": "Randstad", "base_url": "https://www.werkenbijrandstad.nl", "platform": "getnoticed"},
]


def main():
    for company in COMPANIES:
        platform = PLATFORMS[company["platform"]]
        jobs = platform.fetch(company)
        print(f"{company['name']}: {len(jobs)} jobs")


if __name__ == "__main__":
    main()
