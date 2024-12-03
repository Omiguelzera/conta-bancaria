from app.models.transaction import Transaction
from app.models.account import Account
from app.database import SessionLocal

async def create_transaction(transaction_data, username: str):
    db = SessionLocal()
    account = db.query(Account).filter(Account.username == username).first()

    if transaction_data.type == "deposit":
        if transaction_data.amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        account.balance += transaction_data.amount
    elif transaction_data.type == "withdraw":
        if transaction_data.amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if account.balance < transaction_data.amount:
            raise ValueError("Insufficient funds")
        account.balance -= transaction_data.amount

    db.add(account)
    db.commit()
    db.refresh(account)

    new_transaction = Transaction(
        amount=transaction_data.amount,
        type=transaction_data.type,
        account_id=account.id
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    
    return new_transaction
