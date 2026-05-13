# 🔄 TransFlow — Backend com Banco de Dados Não-Relacional

Protótipo de sistema backend para gerenciamento de fluxo de dados, desenvolvido com **Python** e banco de dados **NoSQL**, containerizado com **Docker**. Projeto acadêmico com foco em modelagem de dados não-relacionais e construção de APIs estruturadas.

---

## 🚀 Tecnologias

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![NoSQL](https://img.shields.io/badge/NoSQL-Database-green?style=for-the-badge)

- **Python** — linguagem principal do backend
- **Banco de Dados Não-Relacional (NoSQL)** — modelagem e persistência de dados
- **Docker** — containerização para ambiente reproduzível
- **Dockerfile** — configuração do ambiente de execução

---

## 📐 Estrutura do Projeto

```
P2_BDNR/
└── transflow/
    ├── app/          # Lógica de negócio e rotas
    ├── models/       # Modelagem dos dados
    ├── database/     # Conexão e configuração do banco
    └── ...
Dockerfile            # Containerização da aplicação
README.md
```

---

## ✨ Funcionalidades

- 📦 **Modelagem NoSQL** — estruturação de documentos e coleções para representar fluxos de dados
- 🔄 **Gestão de fluxos** — criação, leitura e rastreamento de transações/registros
- 🐳 **Containerizado com Docker** — ambiente padronizado e portável
- 🔧 **Configuração via variáveis de ambiente** — sem credenciais expostas

---

## ⚙️ Como rodar localmente

### Pré-requisitos
- [Docker](https://www.docker.com/) instalado
- Python 3.10+ (para execução local sem Docker)

### Com Docker (recomendado)

```bash
# 1. Clone o repositório
git clone https://github.com/elissonbrito/P2_BDNR.git
cd P2_BDNR

# 2. Build da imagem
docker build -t transflow .

# 3. Suba o container
docker run -p 8000:8000 transflow
```

### Sem Docker

```bash
# 1. Clone e entre na pasta
git clone https://github.com/elissonbrito/P2_BDNR.git
cd P2_BDNR/transflow

# 2. Crie e ative o ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas configurações de banco

# 5. Suba a aplicação
uvicorn app.main:app --reload
```

---

## 🗃️ Modelagem de Dados

O projeto utiliza banco de dados não-relacional com foco em:

- **Documentos flexíveis** — estrutura adaptável a diferentes tipos de fluxo
- **Sem joins obrigatórios** — dados agrupados por contexto de uso
- **Escalabilidade horizontal** — preparado para crescimento da base

---

## 🧠 Decisões técnicas

| Decisão | Justificativa |
|---------|---------------|
| NoSQL em vez de SQL | Flexibilidade no esquema de dados para representar fluxos variáveis |
| Docker | Garante que o ambiente seja idêntico em qualquer máquina |
| Python | Ecossistema rico para dados e integração com diversas ferramentas |

---

## 📚 Aprendizados

Projeto desenvolvido na disciplina de **Banco de Dados Não-Relacional**, com foco em:
- Modelagem de dados em ambientes NoSQL
- Diferenças entre paradigmas relacional e não-relacional
- Containerização de aplicações Python com Docker
- Organização de projetos backend em Python

---

## 👤 Autor

**Élisson Jorge de Brito Conceição**  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/elissonjbrito/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/elissonbrito)
