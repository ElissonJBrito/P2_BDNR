TransFlow - Protótipo backend

Passos de instalação
1. Certifique-se de ter Docker e Docker Compose instalados.
2. No terminal, na pasta do projeto (onde está docker-compose.yml), execute:
   docker-compose up --build

Variáveis de ambiente
- MONGO_URL (ex: mongodb://mongo:27017)
- REDIS_URL (ex: redis://redis:6379/0)
- RABBITMQ_URL (ex: amqp://guest:guest@rabbitmq/)

Como usar / testar
1. API estará em http://localhost:8000
2. Endpoints:
   - POST /corridas
     Corpo JSON (exemplo):
     {
       "passageiro": {"nome": "João", "telefone": "99999-1111"},
       "motorista": {"nome": "Carla", "nota": 4.8},
       "origem": "Centro",
       "destino": "Inoã",
       "valor_corrida": 35.50,
       "forma_pagamento": "DigitalCoin"
     }
     Retorna 202 e publica evento no RabbitMQ. O worker consumirá e atualizará Redis e MongoDB.

   - GET /corridas
   - GET /corridas/forma_pagamento/{forma}
   - GET /saldo/{motorista}

Testes rápidos
1. Suba o compose:
   docker-compose up --build
2. POST uma corrida (por curl ou Postman). Em alguns instantes (consumer processando), você poderá:
   - Consultar GET /corridas para ver a corrida persistida.
   - Consultar GET /saldo/carla para ver o saldo atualizado.

Observações
- O consumer é executado no serviço "worker".
- Interface de gerenciamento do RabbitMQ disponível em http://localhost:15672 (usuário guest/guest).
- Para capturar tela do sistema em execução: acesse http://localhost:8000/docs (docs do FastAPI) e a interface do RabbitMQ.
