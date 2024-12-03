from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.service.auth import AuthService
from app.models.account import Account
from app.database import get_db


router = APIRouter()

# OAuth2 esquema para pegar o token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Modelo de dados para LoginRequest
class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str

# Rota para gerar o token
@router.post("/token")
async def login_for_access_token(
    login_request: LoginRequest, db: AsyncSession = Depends(get_db)
):
    """
    Endpoint para login e criação de um token de acesso.
    """
    # Consulta assíncrona para obter a conta com o nome de usuário fornecido
    async with db.begin():  # Inicia uma transação
        result = await db.execute(select(Account).filter(Account.username == login_request.username))
        account = result.scalars().first()  # Obtém o primeiro resultado

    # Verifica se a conta existe
    if not account:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    # Verifica a senha usando o AuthService
    if not AuthService.verify_password(login_request.password, account.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    # Criação do token de acesso
    access_token = AuthService.create_access_token(data={"sub": account.username})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register")
async def register_user(register_request: RegisterRequest, db: AsyncSession = Depends(get_db)):

    # Verifica se o nome de usuário já existe
    async with db.begin():
        result = await db.execute(select(Account).filter(Account.username == register_request.username))
        existing_account = result.scalars().first()

    if existing_account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )

    hashed_password = AuthService.get_password_hash(register_request.password)


    new_account = Account(username=register_request.username, password=hashed_password)
    db.add(new_account)
    await db.commit()

    return {"message": "User registered successfully"}