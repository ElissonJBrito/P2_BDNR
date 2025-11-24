import os
import uuid
import asyncio
import random
from fastapi import FastAPI
from typing import List
from .models.corrida_model import Corrida
from .producer import publish_corrida_event_sync
from .database.mongo_client import corridas_collection, init_db
from .database.redis_client import get_balance

GENERATOR_ENABLED = os.getenv("ENABLE_GENERATOR", "true").lower() in ("1", "true", "yes")
GENERATOR_INTERVAL = int(os.getenv("GENERATOR_INTERVAL_SECONDS", str(15 * 60)))  # padrão 15 minutos

app = FastAPI(title="TransFlow API")

@app.on_event("startup")
async def startup_event():
    # inicializar índices no Mongo
    try:
        await init_db()
    except Exception:
        pass

    # iniciar gerador periódico em background se habilitado
    if GENERATOR_ENABLED:
        asyncio.create_task(corrida_generator_loop())

@app.post("/corridas", status_code=202)
async def create_corrida(corrida: Corrida):
    # garante id_corrida
    if not corrida.id_corrida:
        corrida.id_corrida = str(uuid.uuid4())
    # publica evento assíncrono (o consumer fará o insert no Mongo)
    publish_corrida_event_sync(corrida.dict())
    return {"message": "Evento publicado", "id_corrida": corrida.id_corrida}

@app.get("/corridas", response_model=List[Corrida])
async def list_corridas():
    docs = await corridas_collection.find().to_list(length=1000)
    return docs

@app.get("/corridas/forma_pagamento/{forma}")
async def corridas_por_forma(forma: str):
    docs = await corridas_collection.find({"forma_pagamento": forma}).to_list(length=1000)
    return docs

@app.get("/saldo/{motorista}")
async def get_saldo_endpoint(motorista: str):
    saldo = await get_balance(motorista)
    return {"motorista": motorista, "saldo": saldo}

async def corrida_generator_loop():
    """
    Gera corridas aleatórias e publica a cada GENERATOR_INTERVAL segundos.
    Mantém loop infinito no background.
    """
    nomes_passageiros = ["João", "Maria", "Pedro", "Ana", "Lucas", "Carla", "Roberto"]
    nomes_motoristas = ["Carla", "Miguel", "Rita", "Paulo", "Mariana"]
    formas = ["DigitalCoin", "Dinheiro", "Cartao"]
    bairros = ["Centro", "Inoã", "Vila", "Bairro Alto", "Jardim"]

    await asyncio.sleep(5)  # pequena espera antes de iniciar
    while True:
        try:
            corrida = {
                "id_corrida": str(uuid.uuid4()),
                "passageiro": {"nome": random.choice(nomes_passageiros), "telefone": f"9{random.randint(1000,9999)}-{random.randint(1000,9999)}"},
                "motorista": {"nome": random.choice(nomes_motoristas), "nota": round(random.uniform(4.0, 5.0), 1)},
                "origem": random.choice(bairros),
                "destino": random.choice(bairros),
                "valor_corrida": round(random.uniform(5.0, 80.0), 2),
                "forma_pagamento": random.choice(formas)
            }
            publish_corrida_event_sync(corrida)
        except Exception:
            # logs poderiam ser adicionados aqui
            pass
        await asyncio.sleep(GENERATOR_INTERVAL)
