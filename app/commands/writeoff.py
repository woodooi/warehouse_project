from .base import TransactionCommand
from app.models.product import Product

class WriteOffCommand(TransactionCommand):
    def execute(self):
        product = self.db.query(Product).filter(Product.id == self.product_id).first()
        if not product:
            raise ValueError(f"Product with id {self.product_id} not found")

        if product.quantity < self.quantity:
            raise ValueError("Insufficient stock for write-off")

        product.quantity -= self.quantity
        self.log_transaction("WRITE_OFF")
        self.db.commit()
