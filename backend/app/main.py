# backend/app/main.py
from fastapi import FastAPI, Query, HTTPException
from typing import List, Dict, Any
from app.scraper.architecture_finder import fetch_architecture_objects
from app.services.architecture_service import store_architectures, get_architectures
from pymongo.errors import BulkWriteError

app = FastAPI(
    title="Azure Architecture Scraper",
    version="0.1.0",
)

@app.post("/architectures", summary="Fetch a page of Azure architectures")
async def scrape_architectures(
    skip: int = Query(0, ge=0, description="How many items to skip"),
    top:  int = Query(5, ge=1, le=100, description="How many items to fetch")
):
    """
    Uses $skip/$top to page through the Learn API.
    """
    try:
        results: List[Dict[str, Any]] = await fetch_architecture_objects(skip, top)
        next_skip = skip + len(results)
        inserted = await store_architectures(results)

    except BulkWriteError as bwe:
        # catch duplicate‐key or other bulk‐write issues
        raise HTTPException(status_code=409, detail="Some items were duplicates") 
    except Exception as e:
        # covers both fetch errors and any uncaught DB errors
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "status":   "loaded",
        "inserted": inserted,
        "next":     f"/architectures?skip={skip+len(results)}&top={top}"
    }


@app.get(
    "/architectures",
    summary="Read stored architectures",
)
async def read_architectures(
    skip: int = Query(0, ge=0, description="How many items to skip"),
    limit: int = Query(None, ge=1, description="Max number of items to return")
):
    try:
        items: List[Dict[str, Any]] = await get_architectures(skip, limit)
        return {
            "status": "success",
            "count": len(items),
            "results": items
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))