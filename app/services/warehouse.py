from typing import List
from sqlalchemy.orm import Session
from app.observers.base import Observer
from app.commands.base import TransactionCommand
from app.models.product import Product

class WarehouseService:
    def __init__(self, db: Session):
        self.db = db
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, product_id: int):
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if product:
            for observer in self._observers:
                observer.update(product)

    def process_transaction(self, command: TransactionCommand):
        command.execute()
        # After execution, notify attributes
        self.notify(command.product_id)
