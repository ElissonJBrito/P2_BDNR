import os
from redis.asyncio import Redis

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
redis = Redis.from_url(REDIS_URL, decode_responses=True)

async def increment_balance_atomic(motorista: str, amount: float):
    """
    Usa INCRBYFLOAT (operador atômico do Redis) para incrementar o saldo.
    Retorna o novo saldo como float.
    """
    key = f"saldo:{motorista.lower()}"
    # Garantir chave existe: INCRBYFLOAT cria se não existir, então só chamar
    new_val = await redis.incrbyfloat(key, amount)
    # retorna float
    return float(new_val)

async def get_balance(motorista: str):
    key = f"saldo:{motorista.lower()}"
    val = await redis.get(key)
    if val is None:
        return 0.0
    try:
        return float(val)
    except Exception:
        return 0.0
