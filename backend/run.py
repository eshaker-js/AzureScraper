
import uvicorn
import sys 
import asyncio

if sys.platform.startswith("win"): # Needed this for Async and windows locally (doesnt matter in docker)
    from asyncio import WindowsSelectorEventLoopPolicy
    asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,    
        log_level="info"
    )
