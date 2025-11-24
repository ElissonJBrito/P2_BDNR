from pydantic import BaseModel, Field
from typing import Optional

class Passageiro(BaseModel):
    nome: str
    telefone: str

class Motorista(BaseModel):
    nome: str
    nota: Optional[float] = None

class Corrida(BaseModel):
    id_corrida: Optional[str] = None
    passageiro: Passageiro
    motorista: Motorista
    origem: str
    destino: str
    valor_corrida: float
    forma_pagamento: str
