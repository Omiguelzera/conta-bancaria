from pydantic import BaseModel
from typing import List

# Modelo base para transações
class TransactionsBase(BaseModel):
    amount: float
    transaction_type: str  # 'deposit' ou 'withdrawal'
    account_id: int

# Modelo usado para criação de transações
class TransactionsCreate(TransactionsBase):
    pass

# Modelo para resposta de transações
class Transaction(TransactionsBase):
    id: int  # Id da transação no banco de dados

    class Config:
        orm_mode = True  # Permite que o Pydantic converta objetos SQLAlchemy para Pydantic
