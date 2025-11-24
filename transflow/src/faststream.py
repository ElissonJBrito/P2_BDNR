import os
import json
import asyncio
from aio_pika import connect_robust, Message, DeliveryMode, ExchangeType

RABBIT_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")
EXCHANGE_NAME = "transflow_exchange"
QUEUE_NAME = "corrida_finalizada"

async def publish_rabbit(message_obj: dict):
    """
    Publica mensagem persistente em exchange do tipo fanout (durável).
    """
    connection = await connect_robust(RABBIT_URL)
    async with connection:
        channel = await connection.channel()
        exchange = await channel.declare_exchange(EXCHANGE_NAME, ExchangeType.FANOUT, durable=True)
        body = json.dumps(message_obj).encode()
        message = Message(body=body, content_type="application/json", delivery_mode=DeliveryMode.PERSISTENT)
        await exchange.publish(message, routing_key="")

async def consume_rabbit(handler):
    """
    Consome mensagens da fila durável vinculada ao exchange; chama handler(payload_str).
    Reconnect implícito: função assume que chamador reaplica retry se necessário.
    """
    while True:
        try:
            connection = await connect_robust(RABBIT_URL)
            async with connection:
                channel = await connection.channel()
                exchange = await channel.declare_exchange(EXCHANGE_NAME, ExchangeType.FANOUT, durable=True)
                queue = await channel.declare_queue(QUEUE_NAME, durable=True)
                await queue.bind(exchange)
                async with queue.iterator() as queue_iter:
                    async for message in queue_iter:
                        async with message.process():
                            try:
                                payload = message.body.decode()
                                await handler(payload)
                            except Exception:
                                # Se handler falhar, rejeitar sem requeue (evita loop infinito)
                                # Para requeue use message.nack(requeue=True)
                                continue
        except Exception:
            # aguardar antes de tentar reconectar
            await asyncio.sleep(5)
            continue
