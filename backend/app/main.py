from fastapi import FastAPI, Query, HTTPException
from typing import List, Dict, Any
from app.scraper.run_scraper import enrich_architectures
from app.services.architecture_service import store_architectures, get_architectures
from pymongo.errors import BulkWriteError
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from app.db import architectures  

app = FastAPI(
    title="Azure Architecture Scraper",
    version="0.1.0",
)

origins = os.getenv("ALLOWED_ORIGINS", "").split(",")   # Allow origins in the env variable (docker) so that backend accepts frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Make sure entries in the database have a unique column, chose url, this is to avoid duplicates
    await architectures.create_index("url", unique=True)
    yield

@app.post("/architectures", summary="Fetch a page of Azure architectures") # On post we scrape more data
async def scrape_architectures(
    skip: int = Query(0, ge=0, description="How many items to skip"),
    top: int = Query(5, ge=1, le=100, description="How many items to fetch"),
):
    try:
        enriched: List[Dict[str, Any]] = await enrich_architectures(skip, top)  # Call the enrich function (documented in file)
        next_skip = skip + len(enriched)
        inserted = await store_architectures(enriched) # Store newly scraped data

    except BulkWriteError as bwe:
        # catch duplicate‐key or other bulk‐write issues
        raise HTTPException(status_code=409, detail="Some items were duplicates")
    except Exception as e:
        # covers both fetch errors and any uncaught DB errors
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "status": "loaded",
        "inserted": inserted,
        "next": f"/architectures?skip={next_skip}&top={top}",
    }


@app.get(  # Defaults to reading all the rows in the database
    "/architectures",
    summary="Read stored architectures",
)
async def read_architectures(
    skip: int = Query(0, ge=0, description="How many items to skip"), 
    limit: int = Query(None, ge=1, description="Max number of items to return"),
):
    try:
        items: List[Dict[str, Any]] = await get_architectures(skip, limit)
        return {"status": "success", "count": len(items), "results": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
