# backend/app/main.py
from fastapi import FastAPI, Query, HTTPException
from typing import List, Dict, Any
from app.scraper.architecture_finder import fetch_architecture_objects

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
        return {
            "status": "success",
            "count": len(results),
            "results": results,
            "next": f"/architectures?skip={next_skip}&top={top}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
