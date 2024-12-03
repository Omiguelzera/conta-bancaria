from fastapi import FastAPI
from app.api import auth, transactions
from app.database import get_db

app = FastAPI()



# Incluir as rotas
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(transactions.router, prefix="/bank", tags=["transactions"])

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Banking API!"}