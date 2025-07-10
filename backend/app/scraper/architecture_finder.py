import asyncio
import httpx
import json
from typing import List, Dict, Any


async def fetch_architecture_objects(skip: int, top: int) -> List[Dict[str, Any]]:
    # Fetch Azure cloud architectures directly from the API that is accessed on the site
    url = "https://learn.microsoft.com/api/contentbrowser/search/architectures"
    params = {
        "$skip": skip,  # The skip parameter indicates how many results to skip
        "$top": 5,  # The top parameter indicates how many results to fetch
        "expanded": "azure",
        "locale": "en-us",
    }

    async with httpx.AsyncClient(timeout=15.0, trust_env=True) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        payload = resp.json()
        # The api returns a payload with categories and sort features, as well as results
        return payload.get("results", []) # We are only interested in the results (these hold Architecture objects with valuable metadata)
