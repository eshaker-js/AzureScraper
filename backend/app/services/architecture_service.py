# app/services/architecture_service.py

from typing import List, Dict, Any
from datetime import datetime, timezone

from pymongo import InsertOne
from pymongo.errors import BulkWriteError

from app.db import architectures  # your Motor collection


async def store_architectures(items: List[Dict[str, Any]]) -> int:
    """
    Inserts the given architecture items into MongoDB, adding a fetched_at timestamp.
    Returns the number of successfully inserted documents.
    """
    if not items:
        return 0

    # single timestamp for this batch
    ts = datetime.now(timezone.utc)

    # prepare bulk ops, enriching each item with `fetched_at`
    ops = []
    for item in items:
        item["fetched_at"] = ts
        ops.append(InsertOne(item))

    result = await architectures.bulk_write(ops, ordered=False)
    return result.inserted_count


async def get_architectures(skip: int = 0, limit: int = None) -> List[Dict[str, Any]]:
    cursor = architectures.find({})
    if skip:
        cursor = cursor.skip(skip)

    if limit is not None:
        docs = await cursor.limit(limit).to_list(length=limit)
    else:
        total = await architectures.count_documents({})
        docs = await cursor.to_list(length=total)

    # Convert each doc’s ObjectId to str
    sanitized = []
    for d in docs:
        d["id"] = str(d["_id"])  # create a string ID
        d.pop("_id", None)  # remove the original ObjectId
        sanitized.append(d)

    return sanitized
