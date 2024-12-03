from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.account import Account
from app.models.transaction import Transaction
from app.schemas.transactions import TransactionsCreate, Transaction
from app.service.transation_service import create_transaction  
from app.service.auth import get_current_user
from app.database import get_db

router = APIRouter()

@router.post("/transaction", status_code=status.HTTP_201_CREATED, response_model=Transaction)
async def create_transaction_route(
    transaction: TransactionsCreate, 
    current_user: Account = Depends(get_current_user)
):
    """
    Endpoint para criar uma transação bancária, seja um depósito ou saque.
    """
    try:
        # Chamada ao serviço de criação da transação
        new_transaction = await create_transaction(transaction, current_user.username)
        return new_transaction
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/transactions/{account_id}", response_model=List[Transaction])
async def get_transactions(
    account_id: int, 
    current_user: Account = Depends(get_current_user),
    db: Session = Depends(get_db)  # Sessão do banco de dados injetada via dependência
):
    """
    Endpoint para obter todas as transações de uma conta bancária específica.
    """
    # Verificando se o usuário tem acesso à conta
    if current_user.id != account_id:
        raise HTTPException(status_code=403, detail="Unauthorized to access this account")

    # Buscando transações associadas à conta
    transactions = db.query(Transaction).filter(Transaction.account_id == account_id).all()

    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found.")
    
    return transactions