from .base import TransactionCommand
from app.models.product import Product

class ArrivalCommand(TransactionCommand):
    def execute(self):
        product = self.db.query(Product).filter(Product.id == self.product_id).first()
        if not product:
            raise ValueError(f"Product with id {self.product_id} not found")
        
        product.quantity += self.quantity
        self.log_transaction("ARRIVAL")
        self.db.commit()
