import os
import asyncio
from httpx import AsyncClient
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import re
from .architecture_finder import fetch_architecture_objects

LEARN_BASE = "https://learn.microsoft.com/en-us"


# For some architecture pages, theres a 'potential use case' section
async def extract_use_cases(html: str) -> List[str]:
    soup = BeautifulSoup(html, "html.parser")  # We use BeautifulSoup to parse html pages
    header = soup.find(
        lambda t: t.name in ("h3", "h4") 
        and "potential use cases" in t.get_text(strip=True).lower()   # Find the 'potential use case' section
    )
    if not header:
        return [] # Not Found

    blocks = []
    for sib in header.find_next_siblings():  # If we found it, great, extract the text!
        if sib.name in ("h2", "h3", "h4"):
            break
        txt = sib.get_text(separator=" ", strip=True)
        if not txt:
            continue

        # Split on periods (or question marks/exclamations)
        sentences = re.split(r'(?<=[\.\?\!])\s+', txt)  # Split the text up into bullet points (for frontend)
        for s in sentences:
            s = s.strip()
            if s:
                blocks.append(s)
    return blocks 

async def enrich_architectures(skip: int, top: int) -> List[Dict[str, Any]]: # This is the function that POST calls
    items = await fetch_architecture_objects(skip, top)  # We first fetch architecture objets from the official api
    async with AsyncClient(timeout=20.0, trust_env=True) as client:
        enriched = []
        for item in items:
            url = LEARN_BASE + item["url"]  # luckily, the architecture objects come with a url path
            try:
                r = await client.get(url, follow_redirects=True)
                r.raise_for_status()
                uc = await extract_use_cases(r.text)  # Send url to extract potential use cases if the section is there
            except Exception:
                uc = ["Failed to scrape detail page"]
            enriched.append({**item, "useCases": uc})
    return enriched