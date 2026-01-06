from typing import List
from sqlalchemy.orm import Session
from app.observers.base import Observer
from app.commands.base import TransactionCommand
from app.repositories.product import ProductRepository

class WarehouseService:
    def __init__(self, db: Session):
        self.db = db
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, product_id: int):
        product = ProductRepository(self.db).get_by_id(product_id)
        if product:
            for observer in self._observers:
                observer.update(product)

    def process_transaction(self, command: TransactionCommand):
        command.execute()
        # After execution, notify attributes
        self.notify(command.product_id)
