from fastapi import APIRouter, HTTPException, status
from app.schemas.account import AccountCreate
from app.service.auth import get_password_hash
from app.models.account import Account
from app.database import SessionLocal

router = APIRouter()

@router.post("/register", response_model=AccountCreate, status_code=status.HTTP_201_CREATED)
async def create_account(account: AccountCreate):
    db = SessionLocal()
    existing_user = db.query(Account).filter(Account.username == account.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered.")
    
    hashed_password = get_password_hash(account.password)
    new_account = Account(username=account.username, password=hashed_password)
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    
    return new_account
