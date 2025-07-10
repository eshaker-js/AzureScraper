import os
import asyncio
from httpx import AsyncClient
from bs4 import BeautifulSoup
from typing import List, Dict, Any

from .architecture_finder import fetch_architecture_objects

LEARN_BASE = "https://learn.microsoft.com/en-us"

async def extract_use_cases(html: str) -> List[str]:
    soup = BeautifulSoup(html, "html.parser")
    header = soup.find(
        lambda t: t.name in ("h3", "h4")
        and "potential use cases" in t.get_text(strip=True).lower()
    )
    if not header:
        return ["No official use case was scraped from the architecture's page"]

    blocks = []
    for sib in header.find_next_siblings():
        if sib.name in ("h2", "h3", "h4"):
            break
        txt = sib.get_text(separator=" ", strip=True)
        if txt:
            blocks.append(txt)
    return blocks

async def enrich_architectures(skip: int, top: int) -> List[Dict[str, Any]]:
    """
    1) Fetch the batch from the Learn API
    2) For each item, scrape its detail page for use cases
    3) Return a list of dicts with a new 'useCases' field
    """
    items = await fetch_architecture_objects(skip, top)
    async with AsyncClient(timeout=20.0, trust_env=True) as client:
        enriched = []
        for item in items:
            url = LEARN_BASE + item["url"]
            try:
                r = await client.get(url, follow_redirects=True)
                r.raise_for_status()
                uc = await extract_use_cases(r.text)
            except Exception:
                uc = ["Failed to scrape detail page"]
            enriched.append({**item, "useCases": uc})
    return enriched