import asyncio
import json
import os
from .faststream import consume_rabbit
from .database.redis_client import increment_balance_atomic, redis
from .database.mongo_client import corridas_collection, init_db

async def handle_message(raw_payload: str):
    obj = json.loads(raw_payload)
    if obj.get("event") != "corrida_finalizada":
        return
    corrida = obj.get("data", {})
    motorista = corrida.get("motorista", {}).get("nome", "").strip()
    if not motorista:
        return
    motorista_key = motorista.lower()
    try:
        valor = float(corrida.get("valor_corrida", 0.0))
    except Exception:
        valor = 0.0
    # Atualiza saldo no Redis (atômico via INCRBYFLOAT)
    await increment_balance_atomic(motorista_key, valor)
    # Insere/atualiza no MongoDB por id_corrida
    idc = corrida.get("id_corrida")
    if idc:
        await corridas_collection.update_one({"id_corrida": idc}, {"$set": corrida}, upsert=True)
    else:
        # se não tiver id, insere um documento único (pouco provável)
        await corridas_collection.insert_one(corrida)

async def main():
    # inicializa índices mongo (garante collection preparada)
    try:
        await init_db()
    except Exception:
        pass
    # tenta ping no Redis antes de consumir (não bloqueia muito)
    for _ in range(5):
        try:
            await redis.ping()
            break
        except Exception:
            await asyncio.sleep(1)
    # consume_rabbit já faz reconnect loop internamente
    await consume_rabbit(handle_message)

if __name__ == "__main__":
    asyncio.run(main())
