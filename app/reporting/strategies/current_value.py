from .base import ReportStrategy
import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.product import Product
from app.repositories.product import ProductRepository
from typing import Dict, Any

class CurrentValueStrategy(ReportStrategy):
    def generate(self, db: Session, date: datetime.date) -> Dict[str, Any]:
        products = ProductRepository(db).get_all()
        total_value = sum(p.quantity * p.price for p in products)
        product_details = [
            {"id": p.id, "name": p.name, "quantity": p.quantity, "price": p.price, "value": p.quantity * p.price}
            for p in products
        ]
        return {
            "report_type": "Current Inventory Value",
            "total_value": total_value,
            "total_quantity": sum(p.quantity for p in products),
            "details": product_details
        }
