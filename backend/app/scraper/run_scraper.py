# scraper/run_scraper.py

import os
import asyncio
import json
from httpx import AsyncClient
from bs4 import BeautifulSoup

from architecture_finder import fetch_architecture_objects

LEARN_BASE = "https://learn.microsoft.com/en-us"


async def extract_use_cases(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")

    header = soup.find(
        lambda t: t.name in ("h3", "h4")
        and "potential use cases" in t.get_text(strip=True).lower()
    )
    if not header:
        return []

    # 2) Iterate over siblings until the next header
    text_blocks = []
    for sib in header.find_next_siblings():
        # stop as soon as you hit another section header
        if sib.name in ("h2", "h3", "h4"):
            break
        # grab any visible text from this block
        if hasattr(sib, "get_text"):
            txt = sib.get_text(separator=" ", strip=True)
            if txt:
                text_blocks.append(txt)

    return text_blocks


async def run(skip: int = 0, top: int = 5):
    async with AsyncClient(timeout=20.0, trust_env=True) as client:
        # 1) Fetch the API batch
        items = await fetch_architecture_objects(skip, top)
        enriched = []

        # 2) For each item, pull detail page
        for item in items:
            page_url = LEARN_BASE + item["url"]
            try:
                resp = await client.get(page_url, follow_redirects=True)
                resp.raise_for_status()
                use_cases = await extract_use_cases(resp.text)
            except Exception as e:
                print(f"⚠️ Failed to fetch/use-case-scrape {page_url}: {e}")
                use_cases = []

            # 3) Combine
            enriched.append({**item, "useCases": use_cases})

        # 4) Output
        print(json.dumps(enriched, indent=2))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Fetch and enrich Azure architectures with use cases"
    )
    parser.add_argument("--skip", type=int, default=0, help="How many to skip")
    parser.add_argument("--top", type=int, default=5, help="How many to fetch")
    args = parser.parse_args()

    asyncio.run(run(skip=args.skip, top=args.top))
