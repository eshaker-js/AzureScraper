import asyncio
import httpx
import json
from typing import List, Dict, Any

async def fetch_architecture_objects(skip: int, top: int) -> List[Dict[str, Any]]:
    """
    Fetch Azure architecture objects directly from the Learn API.
    """
    url = "https://learn.microsoft.com/api/contentbrowser/search/architectures"
    params = {
        "$skip": skip,
        "$top": 5,  # Adjust as needed, max is 100
        "expanded": "azure",
        "locale": "en-us",
    }

    async with httpx.AsyncClient(timeout=15.0, trust_env=True) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        payload = resp.json()
        # if you want to inspect the entire payload:
        # print(json.dumps(payload, indent=2))
        return payload.get("results", [])

async def main():
    results = await fetch_architecture_objects(0)
    print(f"\n✅ Fetched {len(results)} items\n")

    # Option A: dump the entire list at once
    #print(json.dumps(results, indent=2))


    for obj in results:
        print(json.dumps(obj, indent=2))
        print("-" * 40)

if __name__ == "__main__":
    asyncio.run(main())
