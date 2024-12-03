from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database import Base


class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    transaction_type = Column(String)
    account_id = Column(Integer, ForeignKey("account.id"))


    account = relationship("Account", back_populates="transactions")