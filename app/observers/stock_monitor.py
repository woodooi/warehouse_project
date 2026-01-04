from .base import Observer
from app.models.product import Product
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StockMonitor(Observer):
    def update(self, product: Product):
        if product.quantity < product.min_stock:
             logger.warning(f"ALERT: Product {product.name} (ID: {product.id}) is below minimum stock! Current: {product.quantity}, Min: {product.min_stock}")
