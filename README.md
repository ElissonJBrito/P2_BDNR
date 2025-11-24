# TransFlow — Protótipo Backend (P2_BDNR)

Repositório base: https://github.com/ElissonJBrito/P2_BDNR.git

Visão geral
- Protótipo de backend para gerenciar corridas urbanas com:
  - Persistência em MongoDB (coleção `corridas`).
  - Controle de saldo de motoristas em Redis.
  - Mensageria assíncrona via RabbitMQ (evento `corrida_finalizada`).
  - API com FastAPI; worker consumidor processa eventos e atualiza Redis/Mongo.
  - Gerador automático (opcional) que publica corridas aleatórias a cada 15 minutos.

Pré-requisitos
- Docker
- Docker Compose
- (Opcional) MongoDB Compass ou cliente para inspeção
- (Opcional) redis-cli

Estrutura do projeto (esperada)
- src/
  - main.py (FastAPI)
  - producer.py
  - consumer.py
  - faststream.py
  - database/
    - mongo_client.py
    - redis_client.py
  - models/
    - corrida_model.py
- docker-compose.yml
- Dockerfile
- requirements.txt
- .env
- README.md

Variáveis de ambiente (exemplo .env)
- MONGO_URL=mongodb://mongo:27017
- REDIS_URL=redis://redis:6379/0
- RABBITMQ_URL=amqp://guest:guest@rabbitmq/
- ENABLE_GENERATOR=true         # habilita gerador automático de corridas
- GENERATOR_INTERVAL_SECONDS=900 # intervalo em segundos (padrão 900 = 15min)

Como rodar (passo a passo)
1. Clone o repositório (se ainda não clonou):
   git clone https://github.com/ElissonJBrito/P2_BDNR.git
   cd P2_BDNR

2. Ajuste .env conforme necessário (ex.: ENABLE_GENERATOR=false para desabilitar).

3. Suba o ambiente:
   docker-compose up --build

Serviços / portas
- API FastAPI: http://localhost:8000
  - Docs interativa: http://localhost:8000/docs
- RabbitMQ management: http://localhost:15672 (guest/guest)
- MongoDB: mongodb://localhost:27017 (acesso via cliente)
- Redis: localhost:6379

Endpoints principais
- POST /corridas
  - Publica evento `corrida_finalizada` no broker.
  - Corpo mínimo (JSON):
    {
      "passageiro": {"nome": "João", "telefone": "99999-1111"},
      "motorista": {"nome": "Carla", "nota": 4.8},
      "origem": "Centro",
      "destino": "Inoã",
      "valor_corrida": 35.5,
      "forma_pagamento": "DigitalCoin"
    }
  - Retorno: { "message": "Evento publicado", "id_corrida": "..." }

- GET /corridas
  - Retorna lista de corridas persistidas no MongoDB.

- GET /corridas/forma_pagamento/{forma}
  - Filtra corridas por forma de pagamento.

- GET /saldo/{motorista}
  - Retorna saldo atual do motorista consultando Redis.

Exemplos curl
- Publicar corrida:
  curl -X POST http://localhost:8000/corridas \
    -H "Content-Type: application/json" \
    -d '{"passageiro":{"nome":"João","telefone":"99999-1111"},"motorista":{"nome":"Carla","nota":4.8},"origem":"Centro","destino":"Inoã","valor_corrida":35.5,"forma_pagamento":"DigitalCoin"}'

- Listar corridas:
  curl http://localhost:8000/corridas

- Ver saldo:
  curl http://localhost:8000/saldo/Carla

Fluxo assíncrono (como funciona)
1. POST /corridas → producer publica mensagem `corrida_finalizada` no RabbitMQ.
2. Worker (consumer) consome a fila:
   - Incrementa saldo do motorista no Redis de forma atômica (INCRBYFLOAT).
   - Insere/atualiza documento no MongoDB (index em id_corrida).
3. Após processamento, GET /corridas e GET /saldo/{motorista} refletem as alterações.

Gerador automático de corridas (15 minutos)
- Ativado pela variável ENABLE_GENERATOR (default true).
- Intervalo configurável via GENERATOR_INTERVAL_SECONDS (padrão 900s).
- Para testes locais, reduza temporalmente GENERATOR_INTERVAL_SECONDS para 30 ou 60.

Recomendações para estabilidade
- Garantir índices no MongoDB: indexar id_corrida (único) e forma_pagamento.
- Exchange/Queue duráveis e mensagens persistentes em RabbitMQ.
- Healthchecks/restart policies nos containers em docker-compose para produção.
- Logs do worker e app para depuração.

Verificação e debug
- Logs Docker:
  docker-compose logs -f app
  docker-compose logs -f worker
- Redis CLI:
  redis-cli -h localhost -p 6379 GET saldo:carla
- MongoDB: abrir MongoDB Compass e checar coleção `transflow.corridas`
- RabbitMQ UI: checar filas/exchanges em http://localhost:15672

Checklist para pontuação (garanta)
- POST/GET/GET por forma de pagamento funcionando (MongoDB) — 2,0 pts
- Saldo em Redis e GET /saldo/{motorista}; incremento automático ao processar corrida — 2,0 pts
- Mensageria assíncrona com RabbitMQ: producer no POST e consumer atualizando Redis/Mongo — 3,0 pts
- Docker Compose com app, worker, mongo, redis, rabbitmq e README explicativo — 1,0 pt

Soluções rápidas para problemas comuns
- Containers não sobem: docker-compose down -v && docker-compose up --build
- Mensagens não processadas: ver logs do worker; checar se exchange/queue estão com o mesmo nome.
- Conexões recusadas: confirmar variáveis de ambiente e portas.

Capturas de tela (para entrega)
- Inclua pelo menos:
  - /docs do FastAPI mostrando um POST funcionando.
  - RabbitMQ management exibindo fila/exchanges.
  - GET /saldo/{motorista} com saldo atualizado.
- Salve imagens em doc/ ou anexe na entrega.

Contato
- Este README foca em reproduzir o ambiente local e demonstrar o fluxo assíncrono completo. Ajustes em nomes/portas podem ser feitos diretamente no docker-compose.yml e no .env.
