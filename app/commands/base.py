from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from app.models.transaction import TransactionHistory
from app.models.product import Product

class TransactionCommand(ABC):
    def __init__(self, db: Session, product_id: int, quantity: int):
        self.db = db
        self.product_id = product_id
        self.quantity = quantity

    @abstractmethod
    def execute(self):
        pass

    def log_transaction(self, transaction_type: str):
        history = TransactionHistory(
            product_id=self.product_id,
            type=transaction_type,
            quantity=self.quantity
        )
        self.db.add(history)
