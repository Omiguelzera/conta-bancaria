from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.transactions import TransactionCreate
from app.service.transation_service import create_transaction
from app.service.auth import get_current_user

router = APIRouter()    

@router.post("/transactions")
async def create_transaction_route(transaction: TransactionCreate, current_user: str = Depends(get_current_user)):
    try:
        transaction = create_transaction(transaction, current_user)
        return transaction
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.get("/transactions/{account_id}")
async def get_transactions(account_id: int, current_user: str = Depends(get_current_user)):
    return {"message": "get transactions logic"}