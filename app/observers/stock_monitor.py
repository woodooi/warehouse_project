from .base import Observer
from app.models.product import Product
import logging

# Configure logging
logging.basicConfig(level=logging.INFO) # логуємо все починаючи з INFO 
logger = logging.getLogger(__name__) # створюємо логування на ім'я файлу

class StockMonitor(Observer):
    def update(self, product: Product):
        if product.quantity < product.min_stock:
             logger.warning(f"ALERT: Product {product.name} (ID: {product.id}) is below minimum stock! Current: {product.quantity}, Min: {product.min_stock}")
