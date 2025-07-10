from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")  # Initialize MongoDB with env variables for docker, fallback localhost
client = AsyncIOMotorClient(MONGO_URI)
db = client.get_default_database()
architectures = db.architectures
