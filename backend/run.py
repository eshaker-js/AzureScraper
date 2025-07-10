
import uvicorn
import sys 
import asyncio

if sys.platform.startswith("win"):
    # 🛠️ Tell asyncio to use the SelectorEventLoop on Windows
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
