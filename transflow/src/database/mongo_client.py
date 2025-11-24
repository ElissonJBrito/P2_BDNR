import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client["transflow"]
corridas_collection = db["corridas"]

async def init_db():
    """
    Cria índices essenciais. Chamar em startup/consumer.
    """
    # cria índice único em id_corrida para upsert seguro
    await corridas_collection.create_index("id_corrida", unique=True)
    # índice para consultas por forma de pagamento
    await corridas_collection.create_index("forma_pagamento")
