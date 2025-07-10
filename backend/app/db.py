from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://localhost:27017/azure_scraper")
db = client.get_default_database()
architectures = db.architectures