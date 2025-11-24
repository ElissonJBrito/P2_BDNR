import asyncio
from .faststream import publish_rabbit

async def publish_corrida_event(corrida_dict: dict):
    await publish_rabbit({"event": "corrida_finalizada", "data": corrida_dict})

def publish_corrida_event_sync(corrida_dict: dict):
    """
    Usar em rota FastAPI sem bloquear. Cria task no loop corrente.
    """
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(publish_corrida_event(corrida_dict))
    except RuntimeError:
        # Sem loop em execução (cenário de script), executa diretamente
        asyncio.run(publish_corrida_event(corrida_dict))
