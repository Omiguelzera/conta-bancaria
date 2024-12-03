from pydantic import BaseModel
from typing import List

class AccountBase(BaseModel):
    username: str
    password: str
    balance: float

class AccountCreta(AccountBase):
    password: str

class Account(AccountBase):
    id:int
    balance: float

    class Config:
        orm_mode= True

    
    